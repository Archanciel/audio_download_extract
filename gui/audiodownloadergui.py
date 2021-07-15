import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import threading
from os.path import sep

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.metrics import dp
from kivy.properties import BooleanProperty
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.scrollview import ScrollView
from kivy.uix.settings import SettingOptions
from kivy.uix.settings import SettingSpacer
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.utils import platform

from kivy.core.clipboard import Clipboard

from filechooserpopup import LoadFileChooserPopup, SaveFileChooserPopup, SelectOrCreateDirFileChooserPopup, FileToSplitLoadFileChooserPopup, FileToShareLoadFileChooserPopup
from gui.confirmpopup import ConfirmPopup
from audiosplittergui import AudioSplitterGUI   # must be kept to avoid Builder error
from audiosharegui import AudioShareGUI         # must be kept to avoid Builder error

from audiogui import AudioGUI
from constants import *
from configmanager import ConfigManager
from audiocontroller import AudioController
from gui.guiutil import GuiUtil
from helppopup import HelpPopup

# WARNING: without importing AudioSplitterGUI, the AudioSplitterGUI methods
# called when pressing a button defined in the audiosplittergui.kv file
# raises an error AttributeError: 'AudioSplitterGUI' object has no attribute
# <method name>
from audiosplittergui import AudioSplitterGUI

# global var in order tco avoid multiple call to CryptpPricerGUI __init__ !

RV_LIST_ITEM_SPACING_ANDROID = 2
RV_LIST_ITEM_SPACING_WINDOWS = 0.5
STATUS_BAR_ERROR_SUFFIX = ' --> ERROR ...'
FILE_ACTION_LOAD = 0
FILE_ACTION_SAVE = 1
FILE_ACTION_SELECT_OR_CREATE_DIR = 2
FILE_ACTION_SELECT_FILE_TO_SPLIT = 3
FILE_ACTION_SELECT_FILE_TO_SHARE = 4
AUDIODOWNLOADER_VERSION = 'AudioDownloader 1.1'
NO_INTERNET = False

class WindowManager(ScreenManager):
	pass

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
								 RecycleBoxLayout):
	''' Adds selection and focus behaviour to the view. '''
	
	MOVE_DIRECTION_UP = 'moveItemUp'
	MOVE_DIRECTION_DOWN = 'moveItemDown'
	
	# required to authorise unselecting a selected item
	touch_deselect_last = BooleanProperty(True)
	
	def get_nodes(self):
		nodes = self.get_selectable_nodes()
		
		if self.nodes_order_reversed:
			nodes = nodes[::-1]
			
		if not nodes:
			return None, None
		
		selected = self.selected_nodes
		
		if not selected:  # nothing selected
			return None, None
		
		if len(nodes) == 1:  # the only selectable node is selected already
			return None, None
		
		currentSelIdx = nodes.index(selected[-1])
		self.clear_selection()
		
		return currentSelIdx, nodes
	
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
			
		self.updateLineValues(SelectableRecycleBoxLayout.MOVE_DIRECTION_UP, currentSelIdx, newSelIdx)
		self.select_node(nodes[newSelIdx])

		# supplements the refocusOnRequestInput() called in the
		# SelectableLabel.apply_selection() method, but is useful when
		# the moved item is no longer visible !
		self.cryptoPricerGUI.refocusOnRequestInput()

	def moveItemDown(self):
		currentSelIdx, nodes = self.get_nodes()
		
		if not nodes:
			return
		
		if currentSelIdx == len(nodes) - 1:
			# moving down last item puts it at first item position
			newSelIdx = 0
		else:
			newSelIdx = currentSelIdx + 1
			
		self.updateLineValues(SelectableRecycleBoxLayout.MOVE_DIRECTION_DOWN, currentSelIdx, newSelIdx)
		self.select_node(nodes[newSelIdx])
		
		# supplements the refocusOnRequestInput() called in the
		# SelectableLabel.apply_selection() method, but is useful when
		# the moved item is no longer visible !
		self.cryptoPricerGUI.refocusOnRequestInput()
	
	def updateLineValues(self, moveDirection, movedItemSelIndex, movedItemNewSeIndex):
		movedValue = self.parent.data[movedItemSelIndex]['text']
		
		if moveDirection == SelectableRecycleBoxLayout.MOVE_DIRECTION_DOWN:
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
		
		# cryptoPricerGUI.recycleViewCurrentSelIndex is used by the
		# deleteRequest() and updateRequest() cryptoPricerGUI methods
		self.cryptoPricerGUI.recycleViewCurrentSelIndex = movedItemNewSeIndex


class SelectableLabel(RecycleDataViewBehavior, Label):
	''' Add selection support to the Label '''
	index = None
	selected = BooleanProperty(False)
	selectable = BooleanProperty(True)
	
	def refresh_view_attrs(self, rv, index, data):
		''' Catch and handle the view changes '''
		self.rv = rv
		self.cryptoPricerGUI = rv.parent.parent.parent
		self.index = index
		
		return super(SelectableLabel, self).refresh_view_attrs(
			rv, index, data)
	
	def on_touch_down(self, touch):
		''' Add selection on touch down '''
		if len(self.cryptoPricerGUI.requestListRVSelBoxLayout.selected_nodes) == 1:
			# here, the user manually deselects the selected item. When
			# on_touch_down is called, if the item is selected, the
			# requestListRVSelBoxLayout.selected_nodes list has one element !
			self.cryptoPricerGUI.requestInput.text = ''

			# cryptoPricerGUI.recycleViewCurrentSelIndex is used by the
			# deleteRequest() and updateRequest() cryptoPricerGUI methods
			self.cryptoPricerGUI.recycleViewCurrentSelIndex = -1

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

			# cryptoPricerGUI.recycleViewCurrentSelIndex is used by the
			# deleteRequest() and updateRequest() cryptoPricerGUI methods
			self.cryptoPricerGUI.recycleViewCurrentSelIndex = index
			self.cryptoPricerGUI.requestInput.text = selItemValue
		
		self.cryptoPricerGUI.refocusOnRequestInput()
		self.cryptoPricerGUI.enableStateOfRequestListSingleItemButtons()


class SettingScrollOptions(SettingOptions):
	'''
	This class is used in the Kivy Settings dialog to display in a sccrollable way
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
	showRequestList = False
	recycleViewCurrentSelIndex = -1

	def __init__(self, **kwargs):
		super(AudioDownloaderGUI, self).__init__(**kwargs)

		# due to separate customdropdown kv file, import
		# can not be placed elsewhere with other import
		# sentences.
		from gui.customdropdown import CustomDropDown
		self.dropDownMenu = CustomDropDown(owner=self)

		if os.name == 'posix':
			configPath = '/sdcard/audiodownloader.ini'
		else:
			configPath = 'c:\\temp\\audiodownloader.ini'

		self.configMgr = ConfigManager(configPath)
		self.audioController = AudioController(self, AUDIO_DIR, self.configMgr)
		self.dataPath = self.configMgr.dataPath
	
	def _finish_init(self, dt):
		"""
		Due to using WindowManager for managing multiple screens, the content
		of this method can no longer be located in the __init__ ctor method,
		but must be called by Clock.schedule_once() (located in the base
		class).
		
		:param dt:
		"""
		if os.name == 'posix':
			requestListRVSpacing = RV_LIST_ITEM_SPACING_ANDROID
			if GuiUtil.onSmartPhone():
				self.boxLayoutContainingStatusBar.height = "73dp"
			else:
				self.boxLayoutContainingStatusBar.height = "43dp"

		else:
			requestListRVSpacing = RV_LIST_ITEM_SPACING_WINDOWS
			self.toggleAppSizeButton.text = 'Half'  # correct on Windows !
			self.boxLayoutContainingStatusBar.height = "63dp"

		self.setRVListSizeParms(int(self.configMgr.histoListItemHeight),
								int(self.configMgr.histoListVisibleSize),
								requestListRVSpacing)
		self.appSize = self.configMgr.appSize
		self.defaultAppPosAndSize = self.configMgr.appSize
		self.appSizeHalfProportion = float(self.configMgr.appSizeHalfProportion)
		self.applyAppPosAndSize()
		self.movedRequestNewIndex = -1
		self.movingRequest = False
		self.currentLoadedFathFileName = ''
		self.outputLineBold = True
		self.singleVideoDownloadDir = SINGLE_VIDEO_AUDIO_DIR
		
		self._doOnStart()
	
	def _doOnStart(self):
		'''
		Testing at app start if the clipboard contains a valid playlist playlistObject.
		If it is th case, the videos referenced in the playlist will be downloaded and
		if we are on Windows, their audio will be extracted.

		Since a information popup is displayed in case of valid playlistObject, this must be performed
		here and not in AudioDownloaderGUI.__init__ where no popup can be displayed.

		:return:

		test urls:
		multiple videos with time frames (test audio downloader two files with time frames)
		https://www.youtube.com/playlist?list=PLzwWSJNcZTMSFWGrRGKOypqN29MlyuQvn
		2 videos no time frames (test audio downloader two files)
		https://www.youtube.com/playlist?list=PLzwWSJNcZTMRGA1T1vOn500RuLFo_lGJv
		'''
		self.loadHistoryDataIfSet()
		self.playlistOrSingleVideoUrl = Clipboard.paste()
		
		downloadVideoInfoDic, videoTitle = self.getDownloadVideoInfoDicOrSingleVideoTitleFortUrl(
			self.playlistOrSingleVideoUrl)
		self.singleVideoTitle = videoTitle
		isPlayListToDownload = False
		
		if downloadVideoInfoDic is not None:
			# playlist url obtained from clipboard
			downloadObjectTitle = downloadVideoInfoDic.getPlaylistTitle()
			confirmPopupTitle = "Go on with processing playlist ..."
			isPlayListToDownload = True
		elif videoTitle is not None:
			# single video url obtained from clipboard
			downloadObjectTitle = videoTitle
			confirmPopupTitle = "Go on with downloading audio for video ... "
		elif 'mp3' in self.playlistOrSingleVideoUrl:
			# This is useful in order to facilitate opening the AudioSplitterGUI
			# screen during its development. Once dev is finished, this code
			# can be commented out.
			# example:
			# D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks\\Various\\Wear a mask. Help slow the spread of Covid-19..mp3

			# audioSplitterGUI = self.manager.get_screen('audioSplitterScreen')
			# audioSplitterGUI.initSoundFile(sourceAudioFilePathName=self.playlistOrSingleVideoUrl)
			# self.parent.current = "audioSplitterScreen"
			# self.manager.transition.direction = "left"
			# return

			audioShareGUI = self.manager.get_screen('audioShareScreen')
			audioShareGUI.initSoundFile(sharedAudioFilePathName=self.playlistOrSingleVideoUrl)
			self.parent.current = "audioShareScreen"
			self.manager.transition.direction = "left"
			return

		else:
			# the case if the url is neither pointing to a playlist nor to a
			# single video. Here, an error message was displayed in the UI !
			return
		
		confirmPopupCallbackFunction = self.onPopupAnswer
		
		self.popup = self.createConfirmPopup(isPlayListToDownload,
											 confirmPopupTitle,
											 downloadObjectTitle,
											 confirmPopupCallbackFunction)
		self.popup.open()
	
	def loadHistoryDataIfSet(self):
		'''
		Testing at app start if data path defined in settings does exist
		and if history file loaded at start app does exist. Since a warning popup
		is displayed in case of invalid data, this must be performed here and
		not in audioDownloaderGUI.__init__ where no popup could be displayed.
		:return:
		'''
		dataPathNotExistMessage = self.buildDataPathNotExistMessage(self.dataPath)
		
		if self.ensureDataPathExist(self.dataPath, dataPathNotExistMessage):
			# loading the load at start history file if defined
			historyFilePathFilename = self.configMgr.loadAtStartPathFilename
			dataFileNotFoundMessage = self.buildFileNotFoundMessage(historyFilePathFilename)
			
			if historyFilePathFilename != '' and self.ensureDataPathFileNameExist(
					historyFilePathFilename, dataFileNotFoundMessage):
				self.loadHistoryFromPathFilename(historyFilePathFilename)
				self.displayFileActionOnStatusBar(historyFilePathFilename, FILE_ACTION_LOAD)
	
	def onPopupAnswer(self, instance, answer):
		if answer == 'yes':  # 'yes' is set in confirmpopup.kv file
			self.downloadPlaylistOrSingleVideoAudio(self.playlistOrSingleVideoUrl,
													self.singleVideoTitle)
			self.popup.dismiss()
		elif answer == 'no':
			self.popup.dismiss()
		elif answer == 'set_folder':  # 'set_folder' is set in confirmpopup.kv file
			self.popup.dismiss()
			self.openSelectOrCreateDirPopup(self.playlistOrSingleVideoUrl,
											self.singleVideoTitle)
	
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

	def setRVListSizeParms(self,
						   rvListItemHeight,
						   rvListMaxVisibleItems,
						   rvListItemSpacing):
		self.rvListItemHeight = rvListItemHeight
		self.rvListMaxVisibleItems = rvListMaxVisibleItems
		self.maxRvListHeight = self.rvListMaxVisibleItems * self.rvListItemHeight
		
		# setting RecycleView list item height from config
		self.requestListRVSelBoxLayout.default_size = None, self.rvListItemHeight
		self.requestListRVSelBoxLayout.spacing = rvListItemSpacing
	
	def ensureDataPathExist(self, dataPath, message):
		'''
		Display a warning in a popup if the data path defined in the settings
		does not exist and return False. If path ok, returns True. This prevents
		exceptions at load or save or settings save time.
		:return:
		'''
		if not (os.path.isdir(dataPath)):
			self.displayPopupWarning(message)
			
			return False
		else:
			return True
	
	def displayPopupWarning(self, message):
		popupSize = None
		
		if platform == 'android':
			if GuiUtil.onSmartPhone():
				popupSize = (980, 350)
			else:				
				popupSize = (980, 250)
		elif platform == 'win':
			popupSize = (330, 150)
		
		# this code ensures that the popup content text does not exceeds
		# the popup borders
		sizingLabel = Label(text=message)
		sizingLabel.bind(size=lambda s, w: s.setter('text_size')(s, w))
		
		popup = Popup(title='AudioDownloader WARNING', content=sizingLabel,
					  auto_dismiss=True, size_hint=(None, None),
					  size=popupSize)
		popup.open()
	
	def ensureDataPathFileNameExist(self, dataPathFileName, message):
		'''
		Display a warning in a popup if the passed data path file name
		does not exist and return False. If dataPathFileName ok, returns True.
		This prevents exceptions at load or save or settings save time.
		:return:
		'''
		if not (os.path.isfile(dataPathFileName)):
			self.displayPopupWarning(message)
			
			return False
		else:
			return True

	def toggleAppPosAndSize(self):
		if self.appSize == self.configMgr.APP_SIZE_HALF:
			self.appSize = self.configMgr.APP_SIZE_FULL

			if self.defaultAppPosAndSize == self.configMgr.APP_SIZE_FULL:
				# on the smartphone, we do not want to reposition the cursor ob
				# the input field since this would display the keyboard !
				self.refocusOnRequestInput()
		else:
			self.appSize = self.configMgr.APP_SIZE_HALF

			# the case on the smartphone. Here, positioning the cursor on
			# the input field after having pressed the 'half' button
			# automatically displays the keyboard
			self.refocusOnRequestInput()

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

	def toggleRequestList(self):
		'''
		called by 'History' toggle button to toggle the display of the history
		request list.
		'''
		if self.showRequestList:
			# RecycleView request history list is currently displayed and
			# will be hidden
			self.boxLayoutContainingRV.height = '0dp'
			
			# when hidding the history request list, an item can be selected.
			# For this reason, the disableStateOfRequestListSingleItemButtons()
			# must be called explicitely called, otherwise the history request
			# list items specific buttons remain isLoadAtStartChkboxActive !
			self.disableStateOfRequestListSingleItemButtons()
			self.showRequestList = False
		else:
			# RecycleView request history list is currently hidden and
			# will be displayed
			self.adjustRequestListSize()
			self.showRequestList = True
			self.resetListViewScrollToEnd()
		
		self.refocusOnRequestInput()

	def adjustRequestListSize(self):
		listItemNumber = len(self.requestListRV.data)
		self.boxLayoutContainingRV.height = min(listItemNumber * self.rvListItemHeight, self.maxRvListHeight)

		return listItemNumber

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
		self.clearResultOutputButton.disabled = False
		
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
		self.requestInput.text = ''

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
		self.refocusOnRequestInput()

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
		self.refocusOnRequestInput()

	def resetListViewScrollToEnd(self):
		maxVisibleItemNumber = self.rvListMaxVisibleItems
		listLength = len(self.requestListRV.data)

		if listLength > maxVisibleItemNumber:
			# for the moment, I do not know how to scroll to end of RecyclweView !
			# listView.scroll_to(listLength - maxVisibleItemNumber)
			pass
		else:
			if self.showRequestList:
				listItemNumber = self.adjustRequestListSize()
				if listItemNumber == 0:
					self.showRequestList = False
					self.manageStateOfGlobalRequestListButtons()

	def manageStateOfGlobalRequestListButtons(self):
		'''
		Enable or disable history request list related controls according to
		the status of the list: filled with items or empty.

		Only handles state of the request history list buttons which
		operates on the list globally, not on specific items of the list.
		
		Those buttons are:
			Display/hide request history list button
			Replay all button
			Save request history list menu item button
		'''
		if len(self.requestListRV.data) == 0:
			# request list is empty
			self.toggleHistoButton.state = 'normal'
			self.toggleHistoButton.disabled = True
			self.replayAllButton.disabled = True
			self.boxLayoutContainingRV.height = '0dp'
			self.dropDownMenu.saveButton.disabled = True
		else:
			self.toggleHistoButton.disabled = False
			self.replayAllButton.disabled = False
			self.dropDownMenu.saveButton.disabled = False

	def refocusOnRequestInput(self):
		# defining a delay of 0.5 sec ensure the
		# refocus works in all situations, moving
		# up and down comprised (0.1 sec was not
		# sufficient for item move ...)
		Clock.schedule_once(self._refocusTextInput, 0.5)

	def _refocusTextInput(self, *args):
		'''
		This method is here to be used as callback by Clock and must not be called directly
		:param args:
		:return:
		'''
		self.requestInput.focus = True

	def deleteRequest(self, *args):
		# deleting selected item from RecycleView list
		self.requestListRV.data.pop(self.recycleViewCurrentSelIndex)
		
		remainingItemNb = len(self.requestListRV.data)
		
		if remainingItemNb == 0:
			# no more item in RecycleView list
			self.disableStateOfRequestListSingleItemButtons()
			self.toggleHistoButton.disabled = True
			self.showRequestList = False
			self.requestInput.text = ''
		
		currentSelItemIdx = self.requestListRVSelBoxLayout.selected_nodes[0]
		
		if currentSelItemIdx >= remainingItemNb:
			# the case if the last item was deleted. Then, the new last item
			# is selected
			lastItemIdx = remainingItemNb - 1
			self.requestListRVSelBoxLayout.selected_nodes = [lastItemIdx]
			self.recycleViewCurrentSelIndex = lastItemIdx

		if self.showRequestList:
			self.adjustRequestListSize()

		self.manageStateOfGlobalRequestListButtons()

		self.refocusOnRequestInput()
	
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

		self.refocusOnRequestInput()

	def enableStateOfRequestListSingleItemButtons(self):
		"""
		This method handles the states of the single items of the request
		history list.
		"""
		if len(self.requestListRVSelBoxLayout.selected_nodes):
			# here, a request list item is selected and the
			# requestListRVSelBoxLayout.selected_nodes list has one
			# element !
			self.deleteButton.disabled = False
			self.replaceButton.disabled = False
			self.moveUpButton.disabled = False
			self.moveDownButton.disabled = False
		else:
			self.disableStateOfRequestListSingleItemButtons()
	
	def disableStateOfRequestListSingleItemButtons(self):
		self.deleteButton.disabled = True
		self.replaceButton.disabled = True
		self.moveUpButton.disabled = True
		self.moveDownButton.disabled = True

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
		self.refocusOnRequestInput()

	def openDropDownMenu(self, widget):
		self.dropDownMenu.open(widget)

	def isRequest(self, statusBarStr):
		if STATUS_BAR_ERROR_SUFFIX in statusBarStr:
			return True
		
		return False
	
	def displayHelp(self):
		self.dropDownMenu.dismiss()

		popup = HelpPopup(title=AUDIODOWNLOADER_VERSION)
		popup.open()

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
										  load=self.load,
										  cancel=self.dismissPopup)
		loadAtStartFilePathName = self.configMgr.loadAtStartPathFilename
		self.popup.setCurrentLoadAtStartFile(loadAtStartFilePathName)
		self.popup.open()

	def openSelectOrCreateDirPopup(self,
								   playlistOrSingleVideoUrl,
								   singleVideoTitle):
		self.dropDownMenu.dismiss()
		popupTitle = self.buildFileChooserPopupTitle(FILE_ACTION_SELECT_OR_CREATE_DIR)
		self.popup = SelectOrCreateDirFileChooserPopup(title=popupTitle,
													   rootGUI=self,
													   playlistOrSingleVideoUrl=playlistOrSingleVideoUrl,
													   singleVideoTitle=singleVideoTitle,
													   load=self.load,
													   cancel=self.dismissPopup)
		self.popup.open()

	def openFileToSplitLoadPopup(self):
		self.dropDownMenu.dismiss()
		popupTitle = self.buildFileChooserPopupTitle(FILE_ACTION_SELECT_FILE_TO_SPLIT)
		self.popup = FileToSplitLoadFileChooserPopup(title=popupTitle,
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

	def buildFileChooserPopupTitle(self, fileAction):
		if fileAction == FILE_ACTION_LOAD:
			popupTitleAction = LoadFileChooserPopup.LOAD_FILE_POPUP_TITLE
		elif fileAction == FILE_ACTION_SAVE:
			popupTitleAction = SaveFileChooserPopup.SAVE_FILE_POPUP_TITLE
		elif fileAction == FILE_ACTION_SELECT_OR_CREATE_DIR:
			popupTitle = SaveFileChooserPopup.SELECT_OR_CREATE_DIR_POPUP_TITLE
			return popupTitle
		elif fileAction == FILE_ACTION_SELECT_FILE_TO_SPLIT:
			popupTitle = SaveFileChooserPopup.SELECT_FILE_TO_SPLIT
			return popupTitle
		else:
			# fileAction == FILE_ACTION_SELECT_FILE_TO_SHARE
			popupTitle = SaveFileChooserPopup.SELECT_FILE_TO_SHARE
			return popupTitle

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
		self.refocusOnRequestInput()

	def saveHistoryToFile(self, existingPathOnly, savingPathFileName, isLoadAtStart):
		"""
		
		:param existingPathOnly: this is the current path in the FileChooser dialog
		:param savingPathFileName: path + file name specified by the user in the
			   path file name TextInput save dialog field
		:param isLoadAtStart: value of the load at start CheckBox
		"""
		if not savingPathFileName:
			# no file selected. Save dialog remains open ...
			return
		
		asciiOnlyPathFileName = savingPathFileName.encode("ascii", "ignore").decode()

		if asciiOnlyPathFileName != savingPathFileName:
			message = self.buildNonAsciiFilePathNameMessage(savingPathFileName)
			self.displayPopupWarning(message)
			return
		
		self.currentLoadedFathFileName = savingPathFileName
		pathElemLst = savingPathFileName.split(sep)
		pathContainedInFilePathName = sep.join(pathElemLst[:-1])
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

		self.configMgr.storeConfig()
		self.displayFileActionOnStatusBar(savingPathFileName, FILE_ACTION_SAVE, isLoadAtStart)
		self.refocusOnRequestInput()

	# --- end file chooser code ---

	def buildDataPathNotExistMessage(self, path):
		return 'Data path ' + path + '\nas defined in the settings does not exist !\nEither create the directory or change the\ndata path value using the Settings menu.'

	def buildDataPathDefinedInSettingsNotExistMessage(self, path):
		return 'Data path ' + path + '\nas defined in the settings does not exist !\nEither create the directory or change the\ndata path value using the Settings menu.'

	def buildDataPathContainedInFilePathNameNotExistMessage(self, path):
		return 'Path ' + path + '\ndoes not exist !\nEither create the directory or\nmodify the path.'

	def buildFileNotFoundMessage(self, filePathFilename):
		return 'Data file\n' + filePathFilename + '\nnot found. No history loaded.'
	
	def buildNonAsciiFilePathNameMessage(self, savingPathFileName):
		return 'Save path file name {}\ncontains non ascii characters. File not saved !'.format(savingPathFileName)
	
	def isLoadAtStart(self, filePathName):
		return self.configMgr.loadAtStartPathFilename == filePathName

	def statusBarTextChanged(self):
		width_calc = self.statusBarScrollView.width
		for line_label in self.statusBarTextInput._lines_labels:
			width_calc = max(width_calc, line_label.width + 20)   # add 20 to avoid automatically creating a new line
		self.statusBarTextInput.width = width_calc
	
	# --- start AudioDownloaderGUI new code ---
	
	def getDownloadVideoInfoDicOrSingleVideoTitleFortUrl(self, url):
		"""
		As the passed URL points either to a playlist or to a single video, the
		method returns either a DownloadVideoInfoDic in case of playlist URL or
		None and a video title in case of single video URL.

		:param url: playlist or single video url
		:return: downloadVideoInfoDic, videoTitle
		"""
		self.downloadVideoInfoDic, videoTitle = self.audioController.getDownloadVideoInfoDicOrSingleVideoTitleFortUrl(
			url)
		
		return self.downloadVideoInfoDic, videoTitle
	
	def downloadPlaylistOrSingleVideoAudio(self, playlistOrSingleVideoUrl, singleVideoTitle):
		"""
		This method launch downloading audios for the videos referenced in the playlist
		URL or the audio of the single video if the URL points to a video, this in a
		new thread.

		:param playlistOrSingleVideoUrl: URL pointing to a playlist or to a single
										 video
		:param singleVideoTitle: None in case of playlist, not None in case of single
								 video. Avoids re-obtaining the single video title.
		"""
		self.playlistOrSingleVideoUrl = playlistOrSingleVideoUrl
		self.singleVideoTitle = singleVideoTitle
		
		t = threading.Thread(target=self.downloadPlaylistOrSingleVideoAudioOnNewThread, args=())
		t.daemon = True
		t.start()
	
	def downloadPlaylistOrSingleVideoAudioOnNewThread(self):
		"""
		This method executed on a separated thread launch downloading audios for
		the videos referenced in a playlist or the audio of a single video.
		"""
		self.audioController.downloadVideosReferencedInPlaylistOrSingleVideo(self.playlistOrSingleVideoUrl,
																			 self.downloadVideoInfoDic,
																			 self.singleVideoTitle)
	
	def setMessage(self, msgText):
		pass
	
	def getConfirmation(self, title, msgText):
		self.popup = self.createConfirmPopup(title, msgText, self.onConfirmPopupAnswer)
		self.popup.open()
	
	def onConfirmPopupAnswer(self, instance, answer):
		answer = answer == 'yes'
		self.popup.dismiss()
		
		return answer
	
	def createConfirmPopup(self,
						   isPlayListToDownload,
						   confirmPopupTitle,
						   confirmPopupMsg,
						   confirmPopupCallbackFunction):
		"""

		:param confirmPopupTitle:
		:param confirmPopupMsg:
		:param confirmPopupCallbackFunction: function called when the user click on
											 yes or no button
		:return:
		"""
		popupSize = None
		msgWidth = 100
		
		if platform == 'android':
			popupSize = (980, 600)
			msgWidth = 45
		elif platform == 'win':
			popupSize = (500, 200)
			msgWidth = 54
		
		confirmPopupFormattedMsg = self.formatPopupConfirmMsg(confirmPopupMsg, msgWidth)
		confirmPopup = ConfirmPopup(text=confirmPopupFormattedMsg)
		if isPlayListToDownload:
			confirmPopup.ids.set_folder_btn.disabled = True
		else:
			confirmPopup.ids.set_folder_btn.disabled = False
			
		confirmPopup.bind(on_answer=confirmPopupCallbackFunction)
		popup = Popup(title=confirmPopupTitle,
					  content=confirmPopup,
					  size_hint=(None, None),
					  pos_hint={'top': 0.8},
					  size=popupSize,
					  auto_dismiss=False)
		
		return popup
	
	def formatPopupConfirmMsg(self, rawMsg, maxLineWidth, replaceUnderscoreBySpace=False):
		resizedMsg = GuiUtil.splitLineToLines(rawMsg, maxLineWidth, replaceUnderscoreBySpace)
		
		return resizedMsg
	
	def displayError(self, msg):
		pass


# --- end AudioDownloaderGUI new code ---


class AudioDownloaderGUIApp(App):
	settings_cls = SettingsWithTabbedPanel
	audioDownloaderGUI = None
	
	def build(self): # implicitely looks for a kv file of name cryptopricergui.kv which is
					 # class name without App, in lowercases
					
		# Builder is a global Kivy instance used
		# in widgets that you can use to load other
		# kv files in addition to the default ones.
		from kivy.lang import Builder
		
		# Loading Multiple .kv files
		Builder.load_file('filechooser.kv')
		Builder.load_file('confirmpopup.kv')
		Builder.load_file('customdropdown.kv')
		Builder.load_file('audiodownloadergui.kv')
		Builder.load_file('audiosplittergui.kv')
		Builder.load_file('audiosharegui.kv')
		windowManager = Builder.load_file('windowmanager.kv')
	
		if os.name != 'posix':
			# running app om Windows
			Config.set('graphics', 'width', '600')
			Config.set('graphics', 'height', '500')
			Config.write()

		self.title = 'AudioDownloader GUI'
		#self.audioDownloaderGUI = AudioDownloaderGUI()

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
			config.setdefaults(ConfigManager.CONFIG_SECTION_LAYOUT, {
				ConfigManager.CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT: ConfigManager.DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_ANDROID})
		elif platform == 'ios':
			config.setdefaults(ConfigManager.CONFIG_SECTION_LAYOUT,
							   {ConfigManager.CONFIG_KEY_APP_SIZE: ConfigManager.APP_SIZE_HALF})
			config.setdefaults(ConfigManager.CONFIG_SECTION_GENERAL, {
				ConfigManager.CONFIG_KEY_DATA_PATH: ConfigManager.DEFAULT_DATA_PATH_IOS})
			config.setdefaults(ConfigManager.CONFIG_SECTION_LAYOUT, {
				ConfigManager.CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT: ConfigManager.DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_ANDROID})
		elif platform == 'win':
			config.setdefaults(ConfigManager.CONFIG_SECTION_LAYOUT,
							   {ConfigManager.CONFIG_KEY_APP_SIZE: ConfigManager.APP_SIZE_FULL})
			config.setdefaults(ConfigManager.CONFIG_SECTION_GENERAL, {
				ConfigManager.CONFIG_KEY_DATA_PATH: ConfigManager.DEFAULT_DATA_PATH_WINDOWS})
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
					"title": "Data files location",
					"desc": "Set the directory where the app data files like history files are stored",
					"section": "General",
					"key": "dataPath"
				}
			]""")  # "key": "dataPath" above is the key in the app config file.
								)   # To use another drive, simply define it as datapath value
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
					self.root.appSize = ConfigManager.APP_SIZE_HALF
				else:
					self.root.appSize = ConfigManager.APP_SIZE_FULL

				self.root.applyAppPosAndSize()
			elif key == ConfigManager.CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT:
				self.root.rvListItemHeight = int(config.getdefault(ConfigManager.CONFIG_SECTION_LAYOUT, ConfigManager.CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT, ConfigManager.DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_ANDROID))
				self.root.rvListSizeSettingsChanged()
			elif key == ConfigManager.CONFIG_KEY_HISTO_LIST_VISIBLE_SIZE:
				self.root.rvListMaxVisibleItems = int(config.getdefault(ConfigManager.CONFIG_SECTION_LAYOUT, ConfigManager.CONFIG_KEY_HISTO_LIST_VISIBLE_SIZE, ConfigManager.DEFAULT_CONFIG_HISTO_LIST_VISIBLE_SIZE))
				self.root.rvListSizeSettingsChanged()
			elif key == ConfigManager.CONFIG_KEY_APP_SIZE_HALF_PROPORTION:
				self.root.appSizeHalfProportion = float(config.getdefault(ConfigManager.CONFIG_SECTION_LAYOUT, ConfigManager.CONFIG_KEY_APP_SIZE_HALF_PROPORTION, ConfigManager.DEFAULT_CONFIG_KEY_APP_SIZE_HALF_PROPORTION))
				self.root.applyAppPosAndSize()

	def get_application_config(self, defaultpath="c:/temp/%(appname)s.ini"):
		'''
		Redefining super class method to control the name and location of the application
		settings ini file
		:param defaultpath: used under Windows
		:return:
		'''
		if platform == 'android':
			defaultpath = '/sdcard/%(appname)s.ini'
		elif platform == 'ios':
			defaultpath = '~/Documents/%(appname)s.ini'
		elif platform == 'win':
			defaultpath = defaultpath.replace('/', sep)

		return os.path.expanduser(defaultpath) % {
			'appname': 'audiodownloader', 'appdir': self.directory}


if __name__ == '__main__':
	dbApp = AudioDownloaderGUIApp()

	dbApp.run()
