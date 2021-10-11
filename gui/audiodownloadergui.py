import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import threading
from os.path import sep

from kivy.app import App
from kivy.config import Config
from kivy.metrics import dp
from kivy.properties import BooleanProperty
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.scrollview import ScrollView
from kivy.uix.settings import SettingOptions
from kivy.uix.settings import SettingSpacer
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.utils import platform

from kivy.core.clipboard import Clipboard

from filechooserpopup import LoadFileChooserPopup, SaveFileChooserPopup, SelectOrCreateDirFileChooserPopup, FileToClipLoadFileChooserPopup, FileToShareLoadFileChooserPopup
from gui.confirmpopup import ConfirmPopup

from audiogui import AudioGUI
from audiogui import FILE_ACTION_LOAD
from constants import *
from configmanager import ConfigManager
from audiocontroller import AudioController
from gui.guiutil import GuiUtil
from selectablerecycleboxlayout import SelectableRecycleBoxLayout
from dirutil import DirUtil
from septhreadexec import SepThreadExec

STATUS_BAR_ERROR_SUFFIX = ' --> ERROR ...'
FILE_ACTION_SAVE = 1
FILE_ACTION_SELECT_OR_CREATE_DIR = 2
FILE_ACTION_SELECT_FILE_TO_SPLIT = 3
FILE_ACTION_SELECT_FILE_TO_SHARE = 4
NO_INTERNET = False

class WindowManager(ScreenManager):
	pass

class AudioDownloadSelectableRecycleBoxLayout(SelectableRecycleBoxLayout):
	''' Adds selection and focus behaviour to the view. '''
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
	
	def moveItemUp(self):
		currentSelIdx, nodes = self.get_nodes()
		
		if not nodes:
			return
		
		if not currentSelIdx:
			# currentSelIdx == 0 --> first item is moved up
			# which means it will become the last item !
			newSelIdx = -1
		else:
			newSelIdx = currentSelIdx - 1
			
		self.updateLineValues(AudioDownloadSelectableRecycleBoxLayout.MOVE_DIRECTION_UP, currentSelIdx, newSelIdx)
		self.select_node(nodes[newSelIdx])

		# supplements the refocusOnRequestInput() called in the
		# SelectableLabel.apply_selection() method, but is useful when
		# the moved item is no longer visible !
		self.appGUI.refocusOnFirstRequestInput()

	def moveItemDown(self):
		currentSelIdx, nodes = self.get_nodes()
		
		if not nodes:
			return
		
		if currentSelIdx == len(nodes) - 1:
			# moving down last item puts it at first item position
			newSelIdx = 0
		else:
			newSelIdx = currentSelIdx + 1
			
		self.updateLineValues(AudioDownloadSelectableRecycleBoxLayout.MOVE_DIRECTION_DOWN, currentSelIdx, newSelIdx)
		self.select_node(nodes[newSelIdx])
		
		# supplements the refocusOnRequestInput() called in the
		# SelectableLabel.apply_selection() method, but is useful when
		# the moved item is no longer visible !
		self.appGUI.refocusOnFirstRequestInput()
	
	def updateLineValues(self, moveDirection, movedItemSelIndex, movedItemNewSeIndex):
		movedValue = self.parent.data[movedItemSelIndex]['text']
		
		if moveDirection == AudioDownloadSelectableRecycleBoxLayout.MOVE_DIRECTION_DOWN:
			if movedItemSelIndex > movedItemNewSeIndex:
				# we are moving down the last list item. The item will be inserted at top
				# of the list
				self.parent.data.pop(movedItemSelIndex)
				self.parent.data.insert(0, {'text': movedValue, 'selectable': True})
			else:
				replacedValue = self.parent.data[movedItemNewSeIndex]['text']
				self.parent.data.pop(movedItemSelIndex)
				self.parent.data.insert(movedItemSelIndex, {'text': replacedValue, 'selectable': True})
				
				self.parent.data.pop(movedItemNewSeIndex)
				self.parent.data.insert(movedItemNewSeIndex, {'text': movedValue, 'selectable': True})
		else:
			# handling moving up
			if movedItemSelIndex == 0:
				# we are moving up the first item. The first item will be appended to the
				# end of the list
				self.parent.data.pop(movedItemSelIndex)
				self.parent.data.append({'text': movedValue, 'selectable': True})
			else:
				replacedValue = self.parent.data[movedItemNewSeIndex]['text']
				self.parent.data.pop(movedItemSelIndex)
				self.parent.data.insert(movedItemSelIndex, {'text': replacedValue, 'selectable': True})
				
				self.parent.data.pop(movedItemNewSeIndex)
				self.parent.data.insert(movedItemNewSeIndex, {'text': movedValue, 'selectable': True})
		
		# appGUI.recycleViewCurrentSelIndex is used by the
		# deleteRequest() and updateRequest() appGUI methods
		self.appGUI.recycleViewCurrentSelIndex = movedItemNewSeIndex


class SelectableLabel(RecycleDataViewBehavior, Label):
	''' Add selection support to the Label '''
	index = None
	selected = BooleanProperty(False)
	selectable = BooleanProperty(True)
	
	def refresh_view_attrs(self, rv, index, data):
		''' Catch and handle the view changes '''
		self.rv = rv
		self.audioDownloaderGUI = rv.rootGUI
		self.index = index
		
		return super(SelectableLabel, self).refresh_view_attrs(
			rv, index, data)
	
	def on_touch_down(self, touch):
		''' Add selection on touch down '''
		if len(self.audioDownloaderGUI.requestListRVSelBoxLayout.selected_nodes) == 1:
			# here, the user manually deselects the selected item. When
			# on_touch_down is called, if the item is selected, the
			# requestListRVSelBoxLayout.selected_nodes list has one element !
			self.audioDownloaderGUI.requestInput.text = ''

			# appGUI.recycleViewCurrentSelIndex is used by the
			# deleteRequest() and updateRequest() appGUI methods
			self.audioDownloaderGUI.recycleViewCurrentSelIndex = -1

		if super(SelectableLabel, self).on_touch_down(touch):
			return True
		if self.collide_point(*touch.pos) and self.selectable:
			return self.parent.select_with_touch(self.index, touch)
	
	def apply_selection(self, rv, index, is_selected):
		# instance variable used in .kv file to change the selected item
		# color !
		self.selected = is_selected
		
		if is_selected:
			selItemValue = rv.data[index]['text']

			# appGUI.recycleViewCurrentSelIndex is used by the
			# deleteRequest() and updateRequest() appGUI methods
			self.audioDownloaderGUI.recycleViewCurrentSelIndex = index
			self.audioDownloaderGUI.requestInput.text = selItemValue
		
		self.audioDownloaderGUI.refocusOnFirstRequestInput()
		self.audioDownloaderGUI.enableStateOfRequestListSingleItemButtons()


class SettingScrollOptions(SettingOptions):
	'''
	This class is used in the Kivy Settings dialog to display in a scrollable way
	the long list of time zones

	Source URL: https://github.com/kivy/kivy/wiki/Scollable-Options-in-Settings-panel
	'''

	def _create_popup(self, instance):
		# global oORCA
		# create the popup

		content = GridLayout(cols=1, spacing='5dp')
		scrollview = ScrollView(do_scroll_x=False)
		scrollcontent = GridLayout(cols=1, spacing='5dp', size_hint=(None, None))
		scrollcontent.bind(minimum_height=scrollcontent.setter('height'))
		self.popup = popup = Popup(content=content, title=self.title, size_hint=(0.5, 0.9), auto_dismiss=False)

		# we need to open the popup first to get the metrics
		popup.open()
		# Add some space on top
		content.add_widget(Widget(size_hint_y=None, height=dp(2)))
		# add all the options
		uid = str(self.uid)
		
		for option in self.options:
			state = 'down' if option == self.value else 'normal'
			btn = ToggleButton(text=option, state=state, group=uid, size=(popup.width, dp(55)), size_hint=(None, None))
			btn.bind(on_release=self._set_option)
			scrollcontent.add_widget(btn)

		# finally, add a cancel button to return on the previous panel
		scrollview.add_widget(scrollcontent)
		content.add_widget(scrollview)
		content.add_widget(SettingSpacer())
		# btn = Button(text='Cancel', size=((oORCA.iAppWidth/2)-sp(25), dp(50)),size_hint=(None, None))
		btn = Button(text='Cancel', size=(popup.width, dp(50)), size_hint=(0.9, None))
		btn.bind(on_release=popup.dismiss)
		content.add_widget(btn)


class AudioDownloaderGUI(AudioGUI):
	requestInput = ObjectProperty()
	outputLabel = ObjectProperty()
	statusBarScrollView = ObjectProperty()
	statusBarTextInput = ObjectProperty()
	recycleViewCurrentSelIndex = -1

	def __init__(self, **kwargs):
		super(AudioDownloaderGUI, self).__init__(**kwargs)
	
	def _finish_init(self, dt):
		"""
		Due to using WindowManager for managing multiple screens, the content
		of this method can no longer be located in the __init__ ctor method,
		but must be called by Clock.schedule_once() (located in the base
		class).
		
		:param dt:
		"""
		super(AudioDownloaderGUI, self)._finish_init(dt)

		if self.error:
			# Error set by base class.
			# The case if the configuration manager could not load the config file
			return
		
		if os.name == 'posix':
			if GuiUtil.onSmartPhone():
				self.boxLayoutContainingStatusBar.height = "73dp"
				self.toggleAppSizeButton.width = 150
				self.downloadButton.width = 300
			else:
				self.boxLayoutContainingStatusBar.height = "43dp"
				self.toggleAppSizeButton.width = 80
				self.downloadButton.width = 190

		else:
			self.toggleAppSizeButton.text = 'Half'  # correct on Windows !
			self.boxLayoutContainingStatusBar.height = "63dp"
			self.toggleAppSizeButton.width = 40
			self.downloadButton.width = 80

		self.audioController = AudioController(self, self.configMgr)
		self.appSize = self.configMgr.appSize
		self.defaultAppPosAndSize = self.configMgr.appSize
		self.appSizeHalfProportion = float(self.configMgr.appSizeHalfProportion)
		self.applyAppPosAndSize()
		self.movedRequestNewIndex = -1
		self.movingRequest = False
		self.currentLoadedFathFileName = ''
		self.outputLineBold = True
		self.downloadVideoInfoDic = None
		self.originalPlaylistTitle = None
		self.modifiedPlaylistTitle = None
		self.singleVideoTitle = None
		self.downloadThreadCreated = False  # used to fix a problem on Android
											# where two download threads are
											# created after clicking on 'Yes'
											# button on the ConfirmPopup dialog
		self.downloadObjectTitleThreadCreated = False
		self.playlistOrSingleVideoDownloadPath = None
		self.accessError = None
		
		self._doOnStart()
	
	def _doOnStart(self):
		'''
		Testing at app start if the clipboard contains a valid playlist
		playlistObject. If it is the case, the videos referenced in the
		playlist will be downloaded and if we are on Windows, their audio will
		be extracted.

		Since an information popup is displayed in case of valid playlistObject,
		this must be performed here and not in AudioDownloaderGUI.__init__ where
		no popup can be displayed.

		:return:

		test urls:
		
		- multiple videos with time frames (test audio downloader two files with
		time frames)
		https://www.youtube.com/playlist?list=PLzwWSJNcZTMSFWGrRGKOypqN29MlyuQvn
		- 2 videos no time frames (test audio downloader two files)
		https://www.youtube.com/playlist?list=PLzwWSJNcZTMRGA1T1vOn500RuLFo_lGJv
		
		- unique video:
		https://youtu.be/EHsi_KPKFqU
		'''
		if not self.loadHistoryDataIfSet():
			return
		
		self.downloadFromClipboard()
		
	def downloadFromClipboard(self):
		"""
		Method called either at application start or when pressing the
		download button defined in the audiodownloadergui.kv file.
		"""
		self.playlistOrSingleVideoUrl = Clipboard.paste()
		
		self.disableButtons()
		
		if not self.downloadObjectTitleThreadCreated:
			sepThreadExec = SepThreadExec(callerGUI=self,
			                              func=self.getDownloadObjectTitleOnNewThread,
			                              endFunc=self.executeDownload)
			
			self.downloadObjectTitleThreadCreated = True

			sepThreadExec.start()
			
	def executeDownload(self):
		self.enableButtons()
		
		if self.accessError is None:
			# the case if the url is neither pointing to a playlist nor to a
			# single video. Here, an error message was displayed in the UI !
			
			if self.singleVideoTitle is None:
				# url obtained from clipboard points to a playlist
				downloadObjectTitle = self.originalPlaylistTitle
				confirmPopupTitle = "Go on with processing playlist ..."
			else:
				# url obtained from clipboard points to a single video
				downloadObjectTitle = self.singleVideoTitle
				confirmPopupTitle = "Go on with downloading audio for video ... "
			
			confirmPopupCallbackFunction = self.onConfirmPopupAnswer
			
			self.popup = self.createConfirmPopup(confirmPopupTitle=confirmPopupTitle,
			                                     confirmPopupMsg=downloadObjectTitle,
			                                     confirmPopupCallbackFunction=confirmPopupCallbackFunction)
			self.popup.open()
		else:
			pass
	
	def getDownloadObjectTitleOnNewThread(self):
		_, self.originalPlaylistTitle, self.singleVideoTitle, self.accessError = \
			self.audioController.getPlaylistObjectAndTitlesForUrl(self.playlistOrSingleVideoUrl)
	
		self.downloadObjectTitleThreadCreated = False
		
	def enableButtons(self):
		self.downloadButton.disabled = False
		self.clearResultOutputButton.disabled = False

	def disableButtons(self):
		self.downloadButton.disabled = True
		self.clearResultOutputButton.disabled = True

	def onConfirmPopupAnswer(self, instance, answer):
		"""
		Method called when one of the ConfirmPopup button is pushed.
		
		:param instance:
		:param answer:
		:return:
		"""
		if answer == 'yes':  # 'yes' is set in confirmpopup.kv file
			# if answer is yes, the playlist dir will be created as sub dir
			# off the audio dir or the single video will be downloaded in the
			# default single video dir as defined in the audiodownloader.ini
			# file.
			self.playlistOrSingleVideoDownloadPath = self.getRootAudiobookPath()
			self.downloadPlaylistOrSingleVideoAudio()
			self.popup.dismiss()
		elif answer == 'no':
			self.popup.dismiss()
		elif answer == 'set_folder':  # 'set_folder' is set in confirmpopup.kv file
			self.popup.dismiss()
			self.openSelectOrCreateDirPopup()
	
	def rvListSizeSettingsChanged(self):
		if os.name == 'posix':
			rvListItemSpacing = RV_LIST_ITEM_SPACING_ANDROID
		else:
			rvListItemSpacing = RV_LIST_ITEM_SPACING_WINDOWS
			
		self.setRVListSizeParms(self.rvListItemHeight,
								self.rvListMaxVisibleItems,
								rvListItemSpacing)
		if self.showRequestList:
			self.adjustRequestListSize()
	
	def toggleAppPosAndSize(self):
		if self.appSize == self.configMgr.APP_SIZE_HALF:
			self.appSize = self.configMgr.APP_SIZE_FULL

			if self.defaultAppPosAndSize == self.configMgr.APP_SIZE_FULL:
				# on the smartphone, we do not want to reposition the cursor ob
				# the input field since this would display the keyboard !
				self.refocusOnFirstRequestInput()
		else:
			self.appSize = self.configMgr.APP_SIZE_HALF

			# the case on the smartphone. Here, positioning the cursor on
			# the input field after having pressed the 'half' button
			# automatically displays the keyboard
			self.refocusOnFirstRequestInput()

		self.applyAppPosAndSize()

	def applyAppPosAndSize(self):
		if self.appSize == self.configMgr.APP_SIZE_HALF:
			sizeHintY = float(self.appSizeHalfProportion)
			self.size_hint_y = sizeHintY
			self.pos_hint = {'x': 0, 'y': 1 - sizeHintY}
			self.toggleAppSizeButton.text = 'Full'
		else:
			self.size_hint_y = 1
			self.pos_hint = {'x': 0, 'y': 0}
			self.toggleAppSizeButton.text = 'Half'
	
	def submitRequest(self):
		'''
		Submit the request, output the result and add the request to the
		request list
		:return:
		'''
		self.executeOnlineRequestOnNewThread(asyncOnlineRequestFunction=self.submitRequestOnNewThread, kwargs={})

	def submitRequestOnNewThread(self):
		'''
		Submit the request, output the result and add the request to the
		request list
		:return:
		'''
		# Get the request from the TextInput
		requestStr = self.requestInput.text
		
		fullRequestStrNoOptions = ''
		fullRequestStrWithNoSaveModeOptions = None
		fullRequestStrWithSaveModeOptionsForHistoryList = None
		fullCommandStrForStatusBar = None
		
		try:
			# purpose of the data obtained from the business layer:
			#   outputResultStr - for the output text zone
			#   fullRequestStrNoOptions - for the request history list
			#   fullRequestStrWithNoSaveModeOptions - for the status bar
			#   fullCommandStrWithSaveModeOptionsForHistoryList - for the request history list
			outputResultStr, fullRequestStrNoOptions, fullRequestStrWithNoSaveModeOptions, fullRequestStrWithSaveModeOptionsForHistoryList, fullCommandStrForStatusBar = self.audioController.getPrintableResultForInput(
				requestStr)
		except Exception as e:
			outputResultStr = "ERROR - request '{}' could not be executed. Error info: {}.".format(requestStr, e)
		
		self.outputResult(outputResultStr)
		
		fullRequestListEntry = {'text': fullRequestStrNoOptions, 'selectable': True}

		if fullRequestStrWithSaveModeOptionsForHistoryList != None:
			if fullRequestListEntry in self.requestListRV.data:
				# if the full request string corresponding to the full request string with options is already
				# in the history list, it is removed before the full request string with options is added
				# to the list. Otherwise, this would create a duplicate !
				self.requestListRV.data.remove(fullRequestListEntry)

			fullRequestStrWithSaveModeOptionsListEntry = {'text': fullRequestStrWithSaveModeOptionsForHistoryList, 'selectable': True}
			
			# used to avoid replacing btc usd 20/12/20 all -vs100usd by btc usd 20/12/20 00:00 all -vs100usd !
			fullRequestStrWithSaveModeOptionsListEntryNoZeroTime = {'text': fullRequestStrWithSaveModeOptionsForHistoryList.replace(' 00:00', ''), 'selectable': True}

			if not fullRequestStrWithSaveModeOptionsListEntry in self.requestListRV.data and \
				not fullRequestStrWithSaveModeOptionsListEntryNoZeroTime in self.requestListRV.data:
				self.requestListRV.data.append(fullRequestStrWithSaveModeOptionsListEntry)

			# Reset the ListView
			self.resetListViewScrollToEnd()
		elif fullRequestStrNoOptions != '' and not fullRequestListEntry in self.requestListRV.data:
			# Add the full request to the ListView if not already in

			# if an identical full request string with options is in the history, it is not
			# removed automatically. If the user wants to get rid of it, he must do it exolicitely
			# using the delete button !
			self.requestListRV.data.append(fullRequestListEntry)

			# Reset the ListView
			self.resetListViewScrollToEnd()

		if self.showRequestList:
			self.adjustRequestListSize()

		self.clearHistoryListSelection()
		self.manageStateOfGlobalRequestListButtons()
		self.emptyRequestFields()

		# displaying request in status bar

		if 'ERROR' in outputResultStr:
			self.updateStatusBar(requestStr + STATUS_BAR_ERROR_SUFFIX)
		else:
			if fullRequestStrWithSaveModeOptionsForHistoryList:
				if requestStr != fullRequestStrWithSaveModeOptionsForHistoryList:
					# the case when an option with save mode was added as a partial request !
					# Also, if an option was cancelled (-v0 for example) and another option
					# in save mode remains isLoadAtStartChkboxActive (-fschf for example)
					self.updateStatusBar(requestStr + ' --> ' + fullCommandStrForStatusBar)
				else:
					# here, a full request with option(s) in save mode was executed
					self.updateStatusBar(fullCommandStrForStatusBar)
			else:
				if not fullRequestStrWithNoSaveModeOptions:
					# here, neither options in save mode nor options without save mode are in the request.
					# This happens either if a full request with no option was executed or if the isLoadAtStartChkboxActive
					# option(s) were cancelled (-v0 or/and -f0)
					fullCommandStrForStatusBar = fullRequestStrNoOptions

				if fullRequestStrWithNoSaveModeOptions and requestStr != fullRequestStrWithNoSaveModeOptions:
					# the case when an option without save mode was added as a partial request !
					self.updateStatusBar(requestStr + ' --> ' + fullCommandStrForStatusBar)
				else:
					# here, a full request with option without save mode was executed
					self.updateStatusBar(fullCommandStrForStatusBar)


		self.replayAllButton.disabled = False
		self.clearResultOutputButton.disabled = False

		# self.resultOutput.do_cursor_movement('cursor_pgdown')
		self.refocusOnFirstRequestInput()

	def ensureLowercase(self):
		'''
		Ensure the input text control only contains lower cases.
		'''
		# Get the request from the TextInput
		requestStr = self.requestInput.text
		self.requestInput.text = requestStr.lower()

	def clearOutput(self):
		self.outputLabel.text = ''
		
		if 'History' not in self.statusBarTextInput.text:
			self.statusBarTextInput.text = ''

		self.clearResultOutputButton.disabled = True
		self.refocusOnFirstRequestInput()
	
	def emptyRequestFields(self):
		self.requestInput.text = ''
	
	def clearHistoryListSelection(self):
		self.requestListRV._get_layout_manager().clear_selection()
	
	def replaceRequest(self, *args):
		# Remove the selected item
		self.requestListRV.data.pop(self.recycleViewCurrentSelIndex)

		# Get the request from the TextInputs
		requestStr = self.requestInput.text

		# Add the updated data to the list if not already in
		requestListEntry = {'text': requestStr, 'selectable': True}

		if not requestListEntry in self.requestListRV.data:
			self.requestListRV.data.insert(self.recycleViewCurrentSelIndex, requestListEntry)

		self.refocusOnFirstRequestInput()
	
	def replayAllRequests(self):
		"""
		Method linked to the Replay All button in kv file.
		"""
		self.executeOnlineRequestOnNewThread(asyncOnlineRequestFunction=self.replayAllRequestsOnNewThread, kwargs={})

	def executeOnlineRequestOnNewThread(self, asyncOnlineRequestFunction, kwargs):
		"""
		This generic method first disable the buttons whose usage could disturb
		the passed asyncFunction. It then executes the asyncFunction on a new thread.
		When the asyncFunction is finished, it reenables the disabled buttons.
		
		:param asyncOnlineRequestFunction:
		:param kwargs: keyword args dic for the asyncOnlineRequestFunction
		"""
		self.replayAllButton.disabled = True
		self.clearResultOutputButton.disabled = True

		t = threading.Thread(target=asyncOnlineRequestFunction, args=(), kwargs=kwargs)
		t.daemon = True
		t.start()

	def replayAllRequestsOnNewThread(self):
		# output blank line
		self.outputResult('')
		self.outputLineBold = True

		for listEntry in self.requestListRV.data:
			requestStr = listEntry['text']

			try:
				outputResultStr, _, _, _, _ = self.audioController.getPrintableResultForInput(requestStr)
			except Exception as e:
				outputResultStr = "ERROR - request '{}' could not be executed. Error info: {}.".format(requestStr, e)

			self.outputResult(outputResultStr)

		self.replayAllButton.disabled = False
		self.clearResultOutputButton.disabled = False

		# self.resultOutput.do_cursor_movement('cursor_pgdown')
		self.refocusOnFirstRequestInput()

	def isRequest(self, statusBarStr):
		if STATUS_BAR_ERROR_SUFFIX in statusBarStr:
			return True
		
		return False
	
	def updateStatusBar(self, messageStr):
		self.statusBarTextInput.text = messageStr

	# --- file chooser code ---

	def dismissPopup(self):
		'''
		Act as a call back function for the cancel button of the load and save dialog
		'''
		self.popup.dismiss()

	def openFileLoadPopup(self):
		self.dropDownMenu.dismiss()
		popupTitle = self.buildFileChooserPopupTitle(FILE_ACTION_LOAD)
		self.popup = LoadFileChooserPopup(title=popupTitle,
										  rootGUI=self,
										  load=self.load,
										  cancel=self.dismissPopup)
		self.popup.open()
	
	def openFileSavePopup(self):
		self.dropDownMenu.dismiss()
		popupTitle = self.buildFileChooserPopupTitle(FILE_ACTION_SAVE)
		self.popup = SaveFileChooserPopup(title=popupTitle,
										  rootGUI=self,
										  cancel=self.dismissPopup)
		loadAtStartFilePathName = self.configMgr.loadAtStartPathFilename
		self.popup.setCurrentLoadAtStartFile(loadAtStartFilePathName)
		self.popup.open()

	def openSelectOrCreateDirPopup(self):
		self.dropDownMenu.dismiss()
		popupTitle = self.buildFileChooserPopupTitle(FILE_ACTION_SELECT_OR_CREATE_DIR, self.singleVideoTitle)
		
		self.popup = SelectOrCreateDirFileChooserPopup(title=popupTitle,
													   rootGUI=self,
													   playlistOrSingleVideoUrl=self.playlistOrSingleVideoUrl,
													   originalPlaylistTitle=self.originalPlaylistTitle,
													   singleVideoTitle=self.singleVideoTitle,
													   load=self.load,
													   cancel=self.dismissPopup)
		self.popup.open()

	def openFileToClipLoadPopup(self):
		self.dropDownMenu.dismiss()
		popupTitle = self.buildFileChooserPopupTitle(FILE_ACTION_SELECT_FILE_TO_SPLIT)
		self.popup = FileToClipLoadFileChooserPopup(title=popupTitle,
													rootGUI=self,
													load=self.load,
													cancel=self.dismissPopup)
		self.popup.open()

	def openShareAudioPopup(self):
		self.dropDownMenu.dismiss()
		popupTitle = self.buildFileChooserPopupTitle(FILE_ACTION_SELECT_FILE_TO_SHARE)
		self.popup = FileToShareLoadFileChooserPopup(title=popupTitle,
													 rootGUI=self,
													 load=self.load,
													 cancel=self.dismissPopup)
		self.popup.open()

	def buildFileChooserPopupTitle(self, fileAction, singleVideoTitle=None):
		"""
		In case of FILE_ACTION_SELECT_OR_CREATE_DIR, this means we are asking the user
		to select or create a dir where either playlist video audios or single video audio
		will ba downloaded. If a playlist is to be downloaded, the passed singleVideoTitle
		is None.
		
		:param fileAction:
		:param singleVideoTitle:
		:return:
		"""
		if fileAction == FILE_ACTION_LOAD:
			popupTitleAction = LoadFileChooserPopup.LOAD_FILE_POPUP_TITLE
		elif fileAction == FILE_ACTION_SAVE:
			popupTitleAction = SaveFileChooserPopup.SAVE_FILE_POPUP_TITLE
		elif fileAction == FILE_ACTION_SELECT_OR_CREATE_DIR:
			if singleVideoTitle is not None:
				return SaveFileChooserPopup.SELECT_OR_CREATE_DIR_SINGLE_VIDEO_POPUP_TITLE
			else:
				# if a playlist is downloaded, the passed singleVideoTitle is None
				return SaveFileChooserPopup.SELECT_OR_CREATE_DIR_PLAYLIST_POPUP_TITLE
		elif fileAction == FILE_ACTION_SELECT_FILE_TO_SPLIT:
			return SaveFileChooserPopup.SELECT_FILE_TO_CLIP
		else:
			# fileAction == FILE_ACTION_SELECT_FILE_TO_SHARE
			return SaveFileChooserPopup.SELECT_FILE_TO_SHARE

		loadAtStartFilePathName = self.configMgr.loadAtStartPathFilename
		
		if loadAtStartFilePathName == self.currentLoadedFathFileName:
			loadAtStartFileName = loadAtStartFilePathName.split(sep)[-1]
			if loadAtStartFileName != '':
				popupTitle = "{} ({} loaded at start)".format(popupTitleAction, loadAtStartFileName)
			else:
				popupTitle = "{} (no file loaded)".format(popupTitleAction)
		else:
			loadFileName = self.currentLoadedFathFileName.split(sep)[-1]
			popupTitle = "{} ({} loaded)".format(popupTitleAction, loadFileName)
		
		return popupTitle
	
	def load(self, path, filename):
		if not filename:
			# no file selected. Load dialog remains open ..
			return
		
		currentLoadedFathFileName = os.path.join(path, filename[0])
		self.loadHistoryFromPathFilename(currentLoadedFathFileName)
		self.dismissPopup()
		self.displayFileActionOnStatusBar(currentLoadedFathFileName, FILE_ACTION_LOAD)

	def displayFileActionOnStatusBar(self, pathFileName, actionType, isLoadAtStart=None):
		if actionType == FILE_ACTION_LOAD:
			self.updateStatusBar('History file loaded:\n{}'.format(pathFileName))
		else:
			if isLoadAtStart:
				self.updateStatusBar('History saved to file: {}.\nLoad at start activated.'.format(pathFileName))
			else:
				self.updateStatusBar('History saved to file: {}'.format(pathFileName))

	def loadHistoryFromPathFilename(self, pathFileName):
		self.currentLoadedFathFileName = pathFileName
		dataFileNotFoundMessage = self.buildFileNotFoundMessage(pathFileName)
		
		if not self.ensureDataPathFileNameExist(pathFileName, dataFileNotFoundMessage):
			return

		with open(pathFileName) as stream:
			lines = stream.readlines()

		lines = list(map(lambda line: line.strip('\n'), lines))
		histoLines = [{'text' : val, 'selectable': True} for val in lines]
		self.requestListRV.data = histoLines
		self.requestListRVSelBoxLayout.clear_selection()

		# Reset the ListView
		self.resetListViewScrollToEnd()

		self.manageStateOfGlobalRequestListButtons()
		self.refocusOnFirstRequestInput()

	def saveHistoryToFile(self, existingPathOnly, savingPathFileName, isLoadAtStart):
		"""
		
		:param existingPathOnly: this is the current path in the FileChooser dialog
		:param savingPathFileName: path + file name specified by the user in the
			   path file name TextInput save dialog field
		:param isLoadAtStart: value of the load at start CheckBox
		"""
		asciiOnlyPathFileName = savingPathFileName.encode("ascii", "ignore").decode()

		if asciiOnlyPathFileName != savingPathFileName:
			message = self.buildNonAsciiFilePathNameMessage(savingPathFileName)
			self.displayPopupWarning(message)
			return
		
		self.currentLoadedFathFileName = savingPathFileName
		pathContainedInFilePathName = DirUtil.extractPathFromPathFileName(savingPathFileName)
		savingPathNotExistMessage = self.buildDataPathContainedInFilePathNameNotExistMessage(pathContainedInFilePathName)
		
		if not self.ensureDataPathExist(pathContainedInFilePathName, savingPathNotExistMessage):
			# data path defined specified in saved file path name does not exist. Error popup is displayed.
			return

		with open(savingPathFileName, 'w') as stream:
			for listEntry in self.requestListRV.data:
				line = listEntry['text']
				line = line + '\n'
				stream.write(line)

		# saving in config file if the saved file
		# is to be loaded at application start
		if isLoadAtStart:
			self.configMgr.loadAtStartPathFilename = savingPathFileName
		else:
			if self.configMgr.loadAtStartPathFilename == savingPathFileName:
				self.configMgr.loadAtStartPathFilename = ''

		self.configMgr.saveConfig()
		self.displayFileActionOnStatusBar(savingPathFileName, FILE_ACTION_SAVE, isLoadAtStart)
		self.refocusOnFirstRequestInput()

	# --- end file chooser code ---

	def buildDataPathContainedInFilePathNameNotExistMessage(self, path):
		return 'Path ' + path + ' does not exist ! Either create the directory or modify the path.'
	
	def buildNonAsciiFilePathNameMessage(self, savingPathFileName):
		return 'Save path file name {}\ncontains non ascii characters. File not saved !'.format(savingPathFileName)
	
	def isLoadAtStart(self, filePathName):
		return self.configMgr.loadAtStartPathFilename == filePathName

	def statusBarTextChanged(self):
		width_calc = self.statusBarScrollView.width
		for line_label in self.statusBarTextInput._lines_labels:
			width_calc = max(width_calc, line_label.width + 20)   # add 20 to avoid automatically creating a new line
		self.statusBarTextInput.width = width_calc
	
	def downloadPlaylistOrSingleVideoAudio(self):
		"""
		This method launch downloading audios for the videos referenced in the playlist
		URL or the audio of the single video if the URL points to a video, this in a
		new thread.
		"""
		if not self.downloadThreadCreated:
			sepThreadExec = SepThreadExec(callerGUI=self,
			                              func=self.downloadPlaylistOrSingleVideoAudioOnNewThread)

			self.downloadThreadCreated = True   # used to fix a problem on Android
												# where two download threads are
												# created after clicking on 'Yes'
												# button on the ConfirmPopup dialog

			sepThreadExec.start()
			
	def downloadPlaylistOrSingleVideoAudioOnNewThread(self):
		"""
		This method executed on a separated thread launch downloading audios for
		the videos referenced in a playlist or the audio of a single video.
		"""
		self.audioController.downloadVideosReferencedInPlaylistOrSingleVideo(self.playlistOrSingleVideoUrl,
		                                                                     self.playlistOrSingleVideoDownloadPath,
		                                                                     self.originalPlaylistTitle,
		                                                                     self.modifiedPlaylistTitle,
		                                                                     self.singleVideoTitle)
	
		self.downloadThreadCreated = False  # used to fix a problem on Android
											# where two download threads are
											# created after clicking on 'Yes'
											# button on the ConfirmPopup dialog
	
	def setMessage(self, msgText):
		pass
	
	def createConfirmPopup(self,
						   confirmPopupTitle,
						   confirmPopupMsg,
						   confirmPopupCallbackFunction):
		"""

		:param confirmPopupTitle:
		:param confirmPopupMsg:
		:param confirmPopupCallbackFunction: function called when the user click on
											 yes or no button
		:param isPlayListToDownload
		:return:
		"""
		popupSize = None
		msgWidth = 100
		
		if platform == 'android':
			if GuiUtil.onSmartPhone():
				popupSize = (1350, 100)
				msgWidth = 65
			else:
				popupSize = (980, 100)
				msgWidth = 65
		elif platform == 'win':
			popupSize = (500, 100)
			msgWidth = 68
		
		confirmPopupFormattedMsg = GuiUtil.reformatString(confirmPopupMsg, msgWidth)
		self.confirmPopup = ConfirmPopup(text=confirmPopupFormattedMsg)
		self.confirmPopup.bind(on_answer=confirmPopupCallbackFunction)
		
		popup = Popup(title=confirmPopupTitle,
					  content=self.confirmPopup,
					  size_hint=(None, None),
					  pos_hint={'top': 0.8},
					  size=popupSize,
					  auto_dismiss=False)
		
		return popup

	def getRootAudiobookPath(self):
		"""
		Method called by FileChooserPopup.fillDriveOrMemoryList() in order to determine
		the value of the disk/memory item selected by default when opening the
		FileChooserPopup or its sub class.
		
		:return:
		"""
		if self.originalPlaylistTitle is not None:
			# downloading playlist
			return self.audiobookPath
		else:
			# downloading single video
			return self.audiobookSingleVideoPath

	def outputResult(self, resultStr):
		super(AudioDownloaderGUI, self).outputResult(resultStr)
		
		self.clearResultOutputButton.disabled = False


class AudioDownloaderGUIMainApp(App):
	"""
	WARNING: class nme can not be AudioDownloaderGUIApp since this will cause
	the audiodownloadergui.kv file to be loaded twice: once by the
	Builder.load_file('audiodownloadergui.kv') and once by the automatic
	loading of a kv file with class name minus 'app' in the same dir as the
	app class definition file. Loading twice the kv file causes
	'kivy.uix.popup.PopupException: Popup can have only one widget as content'
	exception.

	(See https://stackoverflow.com/questions/48694764/kivy-popup-can-have-only-one-widget-as-content)
	"""
	settings_cls = SettingsWithTabbedPanel
	
	def build(self): # implicitely looks for a kv file of name cryptopricergui.kv which is
					 # class name without App, in lowercases
					
		# Builder is a global Kivy instance used
		# in widgets that you can use to load other
		# kv files in addition to the default ones.
		from kivy.lang import Builder
		
		# Loading Multiple .kv files
		Builder.load_file('filechooser.kv')
		Builder.load_file('okpopup.kv')
		Builder.load_file('confirmpopup.kv')
		Builder.load_file('customdropdown.kv')
		Builder.load_file('audiodownloadergui.kv')
		Builder.load_file('audioclippergui.kv')
		Builder.load_file('audiosharegui.kv')
		
		windowManager = Builder.load_file('windowmanager.kv')
	
		if os.name != 'posix':
			# running app om Windows
			Config.set('graphics', 'width', '600')
			Config.set('graphics', 'height', '500')
			Config.write()
			
			# avoiding red dot put on Kivy screen after mouse right-click
			# WARNING: on Android, this makes impossible to open the history
			# list as well as causing a kvy.uix.WidgetEception when trying
			# to open the CustomDropdown menu !
			Config.set('input', 'mouse', 'mouse,disable_multitouch')
	
		self.title = 'AudioDownloader GUI'
		self.audioDownloaderGUI = windowManager.get_screen('audioDownloaderScreen')
	
		return windowManager

	def on_pause(self):
		# Here you can save data if needed
		return True

	def on_resume(self):
		# Here you can check if any data needs replacing (usually nothing)
		pass

	def build_config(self, config):
		'''
		Defaults set in this method will be overwritten by the values obtained from the
		app ini file.
		
		:param config:
		:return:
		'''
		from kivy.utils import platform

		if platform == 'android':
			config.setdefaults(ConfigManager.CONFIG_SECTION_LAYOUT,
							   {ConfigManager.CONFIG_KEY_APP_SIZE: ConfigManager.APP_SIZE_HALF})
			config.setdefaults(ConfigManager.CONFIG_SECTION_GENERAL, {
				ConfigManager.CONFIG_KEY_DATA_PATH: ConfigManager.DEFAULT_DATA_PATH_ANDROID})
			config.setdefaults(ConfigManager.CONFIG_SECTION_GENERAL, {
				ConfigManager.CONFIG_KEY_SINGLE_VIDEO_DATA_PATH: ConfigManager.DEFAULT_SINGLE_VIDEO_DATA_PATH_ANDROID})
			config.setdefaults(ConfigManager.CONFIG_SECTION_LAYOUT, {
				ConfigManager.CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT: ConfigManager.DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_ANDROID})
		elif platform == 'ios':
			config.setdefaults(ConfigManager.CONFIG_SECTION_LAYOUT,
							   {ConfigManager.CONFIG_KEY_APP_SIZE: ConfigManager.APP_SIZE_HALF})
			config.setdefaults(ConfigManager.CONFIG_SECTION_GENERAL, {
				ConfigManager.CONFIG_KEY_DATA_PATH: ConfigManager.DEFAULT_DATA_PATH_IOS})
			config.setdefaults(ConfigManager.CONFIG_SECTION_GENERAL, {
				ConfigManager.CONFIG_KEY_SINGLE_VIDEO_DATA_PATH: ConfigManager.DEFAULT_SINGLE_VIDEO_DATA_PATH_IOS})
			config.setdefaults(ConfigManager.CONFIG_SECTION_LAYOUT, {
				ConfigManager.CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT: ConfigManager.DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_ANDROID})
		elif platform == 'win':
			config.setdefaults(ConfigManager.CONFIG_SECTION_LAYOUT,
							   {ConfigManager.CONFIG_KEY_APP_SIZE: ConfigManager.APP_SIZE_FULL})
			config.setdefaults(ConfigManager.CONFIG_SECTION_GENERAL, {
				ConfigManager.CONFIG_KEY_DATA_PATH: ConfigManager.DEFAULT_DATA_PATH_WINDOWS})
			config.setdefaults(ConfigManager.CONFIG_SECTION_GENERAL, {
				ConfigManager.CONFIG_KEY_SINGLE_VIDEO_DATA_PATH: ConfigManager.DEFAULT_SINGLE_VIDEO_DATA_PATH_WINDOWS})
			config.setdefaults(ConfigManager.CONFIG_SECTION_LAYOUT, {
				ConfigManager.CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT: ConfigManager.DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_WINDOWS})

		config.setdefaults(ConfigManager.CONFIG_SECTION_LAYOUT, {
			ConfigManager.CONFIG_KEY_HISTO_LIST_VISIBLE_SIZE: ConfigManager.DEFAULT_CONFIG_HISTO_LIST_VISIBLE_SIZE})
		config.setdefaults(ConfigManager.CONFIG_SECTION_LAYOUT, {
			ConfigManager.CONFIG_KEY_APP_SIZE_HALF_PROPORTION: ConfigManager.DEFAULT_CONFIG_KEY_APP_SIZE_HALF_PROPORTION})

	def build_settings(self, settings):
		# removing kivy default settings page from the settings dialog
		self.use_kivy_settings = False

		settings.register_type('scrolloptions', SettingScrollOptions)

		# add 'General' settings pannel
		settings.add_json_panel("General", self.config, data=("""
			[
				{"type": "path",
					"title": "Playlist video audio files location",
					"desc": "Set the directory where the downloaded playlist video audio files are stored",
					"section": "General",
					"key": "datapath"
				},
				{"type": "path",
					"title": "Single video audio file location",
					"desc": "Set the directory where the downloaded single video audio file is stored",
					"section": "General",
					"key": "singlevideodatapath"
				}
			]""")  # "key": "dataPath" above is the key in the app config file.
				)  # To use another drive, simply define it as datapath value
				   # in the app config file

		# add 'Layout' settings pannel
		settings.add_json_panel("Layout", self.config, data=("""
			[
				{"type": "options",
					"title": "Default app size",
					"desc": "Set the app size at start up",
					"section": "Layout",
					"key": "defaultappsize",
					"options": ["Full", "Half"]
				},
				{"type": "numeric",
					"title": "History list item height",
					"desc": "Set the height of each item in the history list",
					"section": "Layout",
					"key": "histolistitemheight"
				},
				{"type": "numeric",
					"title": "History list visible item number",
					"desc": "Set the number of items displayed in the history list",
					"section": "Layout",
					"key": "histolistvisiblesize"
				},
				{"type": "numeric",
					"title": "Half size application proportion",
					"desc": "Set the proportion of vertical screen size the app occupies so that the smartphone keyboard does not hide part of the application. Must be between 0 and 1",
					"section": "Layout",
					"key": "appsizehalfproportion"
				}
			]""")
								)
	def on_config_change(self, config, section, key, value):
		if config is self.config:
			if key == ConfigManager.CONFIG_KEY_APP_SIZE:
				appSize = config.getdefault(ConfigManager.CONFIG_SECTION_LAYOUT, ConfigManager.CONFIG_KEY_APP_SIZE, "Half").upper()

				if appSize == "HALF":
					self.audioDownloaderGUI.appSize = ConfigManager.APP_SIZE_HALF
				else:
					self.audioDownloaderGUI.appSize = ConfigManager.APP_SIZE_FULL

				self.audioDownloaderGUI.applyAppPosAndSize()
			elif key == ConfigManager.CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT:
				self.audioDownloaderGUI.rvListItemHeight = int(config.getdefault(ConfigManager.CONFIG_SECTION_LAYOUT, ConfigManager.CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT, ConfigManager.DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_ANDROID))
				self.audioDownloaderGUI.rvListSizeSettingsChanged()
			elif key == ConfigManager.CONFIG_KEY_HISTO_LIST_VISIBLE_SIZE:
				self.audioDownloaderGUI.rvListMaxVisibleItems = int(config.getdefault(ConfigManager.CONFIG_SECTION_LAYOUT, ConfigManager.CONFIG_KEY_HISTO_LIST_VISIBLE_SIZE, ConfigManager.DEFAULT_CONFIG_HISTO_LIST_VISIBLE_SIZE))
				self.audioDownloaderGUI.rvListSizeSettingsChanged()
			elif key == ConfigManager.CONFIG_KEY_APP_SIZE_HALF_PROPORTION:
				self.audioDownloaderGUI.appSizeHalfProportion = float(config.getdefault(ConfigManager.CONFIG_SECTION_LAYOUT, ConfigManager.CONFIG_KEY_APP_SIZE_HALF_PROPORTION, ConfigManager.DEFAULT_CONFIG_KEY_APP_SIZE_HALF_PROPORTION))
				self.audioDownloaderGUI.applyAppPosAndSize()
	
	def get_application_config(self):
		'''
		Redefining super class method to control the name and location of the
		application	settings ini file. WARNING: this method is necessary for
		the appconfig file to be updated when a value was changed with the
		Kivy settings dialog.

		:return: the app config file path name
		'''
		configFilePathName = DirUtil.getConfigFilePathName()
		
		return configFilePathName
	
	def open_settings(self, *largs):
		self.audioDownloaderGUI.dropDownMenu.dismiss()
		super().open_settings()


if __name__ == '__main__':
	dbApp = AudioDownloaderGUIMainApp()

	dbApp.run()
