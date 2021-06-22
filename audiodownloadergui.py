import threading
from os.path import sep

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.metrics import dp
from kivy.properties import BooleanProperty
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.scrollview import ScrollView
from kivy.uix.settings import SettingOptions
from kivy.uix.settings import SettingSpacer
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.core.clipboard import Clipboard

# new AudioDownloaderGUI import statements
from kivy.properties import StringProperty

from constants import *
from configmanager import ConfigManager
from audiocontroller import AudioController
from guiutil import GuiUtil

# global var in order tco avoid multiple call to AudioDownloaderGUI __init__ !
RV_LIST_ITEM_SPACING_ANDROID = 2
RV_LIST_ITEM_SPACING_WINDOWS = 0.5

AUDIODOWNLOADER_VERSION = 'AudioDownloader 1.1'
FILE_LOADED = 0
FILE_SAVED = 1
fromAppBuilt = False


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
		self.audioDownloaderGUI.refocusOnRequestInput()

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
		self.audioDownloaderGUI.refocusOnRequestInput()

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
		
		# audioDownloaderGUI.recycleViewCurrentSelIndex is used by the
		# deleteRequest() and updateRequest() audioDownloaderGUI methods
		self.audioDownloaderGUI.recycleViewCurrentSelIndex = movedItemNewSeIndex

class SelectableLabel(RecycleDataViewBehavior, Label):
	''' Add selection support to the Label '''
	index = None
	selected = BooleanProperty(False)
	selectable = BooleanProperty(True)
	
	def refresh_view_attrs(self, rv, index, data):
		''' Catch and handle the view changes '''
		self.rv = rv
		self.index = index
		
		return super(SelectableLabel, self).refresh_view_attrs(
			rv, index, data)
	
	def on_touch_down(self, touch):
		''' Add selection on touch down '''
		
		audioDownloaderGUI = self.rv.parent.parent
		
		if len(audioDownloaderGUI.requestListRVSelBoxLayout.selected_nodes) == 1:
			# here, the user manually deselects the selected item. When
			# on_touch_down is called, if the item is selected, the
			# requestListRVSelBoxLayout.selected_nodes list has one element !
			audioDownloaderGUI.requestInput.text = ''
			
			# audioDownloaderGUI.recycleViewCurrentSelIndex is used by the
			# deleteRequest() and updateRequest() audioDownloaderGUI methods
			audioDownloaderGUI.recycleViewCurrentSelIndex = -1
		
		if super(SelectableLabel, self).on_touch_down(touch):
			return True
		if self.collide_point(*touch.pos) and self.selectable:
			return self.parent.select_with_touch(self.index, touch)
	
	def apply_selection(self, rv, index, is_selected):
		# instance variable used in .kv file to change the selected item
		# color !
		self.selected = is_selected
		
		audioDownloaderGUI = rv.parent.parent
		
		if is_selected:
			selItemValue = rv.data[index]['text']
			
			# audioDownloaderGUI.recycleViewCurrentSelIndex is used by the
			# deleteRequest() and updateRequest() audioDownloaderGUI methods
			audioDownloaderGUI.recycleViewCurrentSelIndex = index
			audioDownloaderGUI.requestInput.text = selItemValue
			audioDownloaderGUI.refocusOnRequestInput()

		audioDownloaderGUI.enableStateOfRequestListSingleItemButtons()

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

class LoadDialog(FloatLayout):
	load = ObjectProperty(None)
	cancel = ObjectProperty(None)
	fileChooser = ObjectProperty(None)

class SaveDialog(FloatLayout):
	save = ObjectProperty(None)
	cancel = ObjectProperty(None)
	fileChooser = ObjectProperty(None)
	loadAtStartChkb = ObjectProperty(None)
	filePathName = ObjectProperty(None)
	owner = None

	def toggleLoadAtStart(self, active):
		if active:
			self.owner.updateStatusBar('Load at start activated')
		else:
			self.owner.updateStatusBar('')

	def saveFileSelected(self, filePathName):
		self.filePathName.text = filePathName

		if self.owner.isLoadAtStart(filePathName):
			self.loadAtStartChkb.active = True
			self.owner.updateStatusBar('Load at start active')
		else:
			self.loadAtStartChkb.active = False
			self.owner.updateStatusBar('')

class CustomDropDown(DropDown):
	saveButton = ObjectProperty(None)

	def __init__(self, owner):
		super().__init__()
		self.owner = owner

	def showLoad(self):
		message = 'Audio dir ' + AUDIO_DIR + '\nas defined in the settings does not exist !\nEither create the directory or change the\naudio dir value using the Settings menu.'

		if self.owner.ensureDataPathExist(AUDIO_DIR, message):
			self.owner.openLoadHistoryFileChooser()

	def showSave(self):
		message = 'Data path ' + self.owner.dataPath + '\nas defined in the settings does not exist !\nEither create the directory or change the\ndata path value using the Settings menu.'

		if self.owner.ensureDataPathExist(self.owner.dataPath, message):
			self.owner.openSaveHistoryFileChooser()

	def help(self):
		self.owner.displayHelp()

class ScrollablePopup(Popup):
	contentBox = ObjectProperty()
	scrollView = ObjectProperty

	def setContentPageList(self, formatedTextPageList):
		self.formatedTextPageList = formatedTextPageList
		self.currentPage = 0
		self.setContentTextToCurrentPage()

	def setContentTextToCurrentPage(self):
		self.contentBox.content.text = self.formatedTextPageList[self.currentPage]

	def previousPage(self):
		self.currentPage -= 1

		if self.currentPage < 0:
			self.currentPage = 0

		self.setContentTextToCurrentPage()
		self.scrollView.scroll_y = 0 # force scrolling to bottom

	def nextPage(self):
		self.currentPage += 1

		if self.currentPage == len(self.formatedTextPageList):
			self.currentPage = len(self.formatedTextPageList) - 1

		self.setContentTextToCurrentPage()
		self.scrollView.scroll_y = 1 # force scrolling to top


class AudioDownloaderGUI(BoxLayout):
	requestInput = ObjectProperty()
	resultOutput = ObjectProperty()
	statusBarScrollView = ObjectProperty()
	statusBarTextInput = ObjectProperty()
	showRequestList = False
	recycleViewCurrentSelIndex = -1

	def __init__(self, **kwargs):
		global fromAppBuilt

		if not fromAppBuilt:
			return

		super(AudioDownloaderGUI, self).__init__(**kwargs)
		self.dropDownMenu = CustomDropDown(owner=self)

		if os.name == 'posix':
			configPath = '/storage/emulated/0/audiodownloader.ini'
			requestListRVSpacing = RV_LIST_ITEM_SPACING_ANDROID
		else:
			configPath = 'c:\\temp\\audiodownloader.ini'
			requestListRVSpacing = RV_LIST_ITEM_SPACING_WINDOWS
			self.toggleAppSizeButton.text = 'Half'  # correct on Windows !

		self.configMgr = ConfigManager(configPath)
		self.audioController = AudioController(self, AUDIO_DIR, self.configMgr)
		self.dataPath = self.configMgr.dataPath

		self.setRVListSizeParms(int(self.configMgr.histoListItemHeight),
		                        int(self.configMgr.histoListVisibleSize),
		                        requestListRVSpacing)

		self.appSize = self.configMgr.appSize
		self.defaultAppPosAndSize = self.configMgr.appSize
		self.appSizeHalfProportion = float(self.configMgr.appSizeHalfProportion)
		self.applyAppPosAndSize()
		self.movedRequestNewIndex = -1
		self.movingRequest = False
		
		self.downloadVideoInfoDic = None
		self.playlistOrSingleVideoUrl = None
	
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
			popupSize = None

			if platform == 'android':
				popupSize = (980, 450)
			elif platform == 'win':
				popupSize = (500, 150)

			popup = Popup(title='CryptoPricer WARNING', content=Label(
				text=message),
						  auto_dismiss=True, size_hint=(None, None),
						  size=popupSize)
			popup.open()

			return False
		else:
			return True

	def ensureDataPathFileNameExist(self, dataPathFileName, message):
		'''
		Display a warning in a popup if the passed data path file name
		does not exist and return False. If dataPathFileName ok, returns True.
		This prevents exceptions at load or save or settings save time.
		:return:
		'''
		if not (os.path.isfile(dataPathFileName)):
			popupSize = None

			if platform == 'android':
				popupSize = (980, 450)
			elif platform == 'win':
				popupSize = (300, 150)

			popup = Popup(title='CryptoPricer WARNING', content=Label(
				text=message),
						  auto_dismiss=True, size_hint=(None, None),
						  size=popupSize)
			popup.open()

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
			# list items specific buttons remain active !
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
		# Get the request from the TextInput
		requestStr = self.requestInput.text

		# purpose of the informations obtained from the business layer:
		#   outputResultStr - for the output text zone
		#   fullRequestStr - for the request history list
		#   fullRequestStrWithOptions - for the status bar
		#   fullRequestStrWithSaveModeOptions - for the request history list
		outputResultStr, fullRequestStr, fullRequestStrWithOptions, fullRequestStrWithSaveModeOptions, fullCommandStrForStatusBar = self.audioController.getPrintableResultForInput(
			requestStr)

		self.outputResult(outputResultStr)

		fullRequestListEntry = {'text': fullRequestStr, 'selectable': True}

		if fullRequestStrWithSaveModeOptions != None:
			if fullRequestListEntry in self.requestListRV.data:
				# if the full request string corresponding to the full request string with options is already
				# in the history list, it is removed before the full request string with options is added
				# to the list. Otherwise, this would engender a duplicate !
				self.requestListRV.data.remove(fullRequestListEntry)

			fullRequestStrWithSaveModeOptionsListEntry = {'text': fullRequestStrWithSaveModeOptions, 'selectable': True}

			if not fullRequestStrWithSaveModeOptionsListEntry in self.requestListRV.data:
				self.requestListRV.data.append(fullRequestStrWithSaveModeOptionsListEntry)

			# Reset the ListView
			self.resetListViewScrollToEnd()
		elif fullRequestStr != '' and not fullRequestListEntry in self.requestListRV.data:
			# Add the full request to the ListView if not already in

			# if an identical full request string with options is in the history, it is not
			# removed automatically. If the user wants to get rid of it, he must do it exolicitely
			# using the delete button !
			self.requestListRV.data.append(fullRequestListEntry)

			# Reset the ListView
			self.resetListViewScrollToEnd()

		if self.showRequestList:
			self.adjustRequestListSize()

		self.manageStateOfGlobalRequestListButtons()
		self.requestInput.text = ''

		# displaying request in status bar

		if 'ERROR' in outputResultStr:
			self.updateStatusBar(requestStr + ' --> ' + 'ERROR ...')
		else:
			if fullRequestStrWithSaveModeOptions:
				if requestStr != fullRequestStrWithSaveModeOptions:
					self.updateStatusBar(requestStr + ' --> ' + fullCommandStrForStatusBar)
				else:
					self.updateStatusBar(fullCommandStrForStatusBar)
			else:
				if not fullRequestStrWithOptions:
					fullCommandStrForStatusBar = fullRequestStr

				if requestStr != fullRequestStrWithOptions:
					self.updateStatusBar(requestStr + ' --> ' + fullCommandStrForStatusBar)
				else:
					self.updateStatusBar(fullCommandStrForStatusBar)

		self.refocusOnRequestInput()

	def ensureLowercase(self):
		'''
		Ensure the input text control only contains lower cases.
		'''
		# Get the request from the TextInput
		requestStr = self.requestInput.text
		self.requestInput.text = requestStr.lower()

	def recycleViewSelectItem(self, index, isSelected):
		if self.recycleViewCurrentSelIndex != -1 and \
			index != self.recycleViewCurrentSelIndex:
			
			return
		
		if isSelected:
			# fixing crash when deleting last item of history list
			itemNumber = len(self.requestListRV.data)
			
			if index == itemNumber:
				index -= 1
			# fixing crash when deleting last item of history list

			requestStr = self.requestListRV.data[index]['text']
			self.requestInput.text = requestStr
			self.enableRequestListItemButtons()
			self.refocusOnRequestInput()
		else:
			self.requestInput.text = ''
			self.disableRequestListItemButtons()

	def clearOutput(self):
		self.resultOutput.text = ''
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
					self.manageStateOfRequestListButtons()
	
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
	
	def outputResult(self, resultStr):
		if len(self.resultOutput.text) == 0:
			self.resultOutput.text = resultStr
		else:
			self.resultOutput.text = self.resultOutput.text + '\n' + resultStr
			# self.outputResultScrollView.scroll_to(100000)
			# self.resultOutput.cursor = (10000,0)

		self.clearResultOutputButton.disabled = False

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
		self.replayAllButton.disabled = True

		t = threading.Thread(target=self.replayAllRequestsOnNewThread, args=())
		t.daemon = True
		t.start()

	def replayAllRequestsOnNewThread(self):
		# output blank line
		self.outputResult('')

		for listEntry in self.requestListRV.data:
			outputResultStr, fullRequestStr, fullRequestStrWithOptions, fullRequestStrWithSaveModeOptions, fullCommandStrForStatusBar = \
				self.audioController.getPrintableResultForInput(listEntry['text'], copyResultToClipboard=False)
			self.outputResult(outputResultStr)

		self.replayAllButton.disabled = False

		# self.resultOutput.do_cursor_movement('cursor_pgdown')
		self.refocusOnRequestInput()

	def openDropDownMenu(self, widget):
		self.dropDownMenu.open(widget)

	def displayHelp(self):
		self.dropDownMenu.dismiss()

		popupSize = None

		if platform == 'android':
			popupSize = (980, 1200)
			width = 45
		elif platform == 'win':
			popupSize = (400, 450)
			width = 54

		popup = ScrollablePopup(title=AUDIODOWNLOADER_VERSION, size_hint=(None, None), size=popupSize)

		with open('help.txt') as helpFile:
			formatedHelpTextPageList = GuiUtil.sizeParagraphsForKivyLabelFromFile(helpFile, width)

		popup.setContentPageList(formatedHelpTextPageList)
		popup.open()

	def updateStatusBar(self, messageStr):
		self.statusBarTextInput.text = messageStr

	# --- file chooser code ---
	def getStartPath(self):
		return "D:\\Users\\Jean-Pierre"

	def dismissPopup(self):
		'''
		Act as a call back function for the cancel button of the load and save dialog
		:return: nothing
		'''
		self.updateStatusBar('')
		self.popup.dismiss()

	def openLoadHistoryFileChooser(self):
		fileChooserDialog = LoadDialog(load=self.load, cancel=self.dismissPopup)
		fileChooserDialog.fileChooser.rootpath = self.dataPath
		self.popup = Popup(title="Load file", content=fileChooserDialog,
						   size_hint=(0.9, 0.6), pos_hint={'center': 1, 'top': 1})
		self.popup.open()
		self.dropDownMenu.dismiss()

	def openSaveHistoryFileChooser(self):
		fileChooserDialog = SaveDialog(save=self.saveHistoryToFile, cancel=self.dismissPopup)
		fileChooserDialog.owner = self
		fileChooserDialog.fileChooser.rootpath = self.dataPath
		self.popup = Popup(title="Save file", content=fileChooserDialog,
						   size_hint=(0.9, 0.6), pos_hint={'center': 1, 'top': 1})
		self.popup.open()
		self.dropDownMenu.dismiss()

	def load(self, path, filename):
		if not filename:
			# no file selected. Load dialog remains open ..
			return

		pathFilename = os.path.join(path, filename[0])
		self.loadHistoryFromPathFilename(pathFilename)
		self.dismissPopup()

	def loadHistoryFromPathFilename(self, pathFilename):
		dataFileNotFoundMessage = 'Data file\n' + pathFilename + 'not found. No history loaded.'

		if not self.ensureDataPathFileNameExist(pathFilename, dataFileNotFoundMessage):
			return

		with open(pathFilename) as stream:
			lines = stream.readlines()

		lines = list(map(lambda line: line.strip('\n'), lines))
		histoLines = [{'text' : val, 'selectable': True} for val in lines]
		self.requestListRV.data = histoLines
		self.requestListRVSelBoxLayout.clear_selection()

		# Reset the ListView
		self.resetListViewScrollToEnd()

		self.manageStateOfGlobalRequestListButtons()
		self.refocusOnRequestInput()

	def saveHistoryToFile(self, path, filename, isLoadAtStart):
		dataPathNotExistMessage = self.buildDataPathNotExistMessage(path)
		pathFileName = os.path.join(path, filename)

		if not filename or not self.ensureDataPathExist(path, dataPathNotExistMessage):
			# no file selected. Save dialog remains open ..
			return

		with open(pathFileName, 'w') as stream:
			for listEntry in self.requestListRV.data:
				line = listEntry['text']
				line = line + '\n'
				stream.write(line)

		# saving in config file if the saved file
		# is to be loaded at application start
		if isLoadAtStart:
			self.configMgr.loadAtStartPathFilename = pathFileName
		else:
			if self.configMgr.loadAtStartPathFilename == pathFileName:
				self.configMgr.loadAtStartPathFilename = ''

		self.configMgr.storeConfig()

		self.dismissPopup()
		self.refocusOnRequestInput()

	# --- end file chooser code ---

	def buildDataPathNotExistMessage(self, path):
		return 'Data path ' + path + '\nas defined in the settings does not exist !\nEither create the directory or change the\ndata path value using the Settings menu.'

	def isLoadAtStart(self, filePathName):
		return self.configMgr.loadAtStartPathFilename == filePathName

	def buildFileNotFoundMessage(self, filePathFilename):
		return 'Data file\n' + filePathFilename + '\nnot found. No history loaded.'

	def statusBarTextChanged(self):
		width_calc = self.statusBarScrollView.width
		for line_label in self.statusBarTextInput._lines_labels:
			width_calc = max(width_calc, line_label.width + 20)   # add 20 to avoid automatically creating a new line
		self.statusBarTextInput.width = width_calc

	def displayFileActionOnStatusBar(self, pathFileName, actionType, isLoadAtStart=None):
		if actionType == FILE_LOADED:
			self.updateStatusBar('History file loaded:\n{}'.format(pathFileName))
		else:
			if isLoadAtStart:
				self.updateStatusBar('History saved to file: {}.\nLoad at start activated.'.format(pathFileName))
			else:
				self.updateStatusBar('History saved to file: {}'.format(pathFileName))

	# --- start AudioDownloaderGUI new code ---
	
	def getDownloadVideoInfoDicOrSingleVideoTitleFortUrl(self, url):
		"""
		As the passed URL points either to a playlist or to a single video, the
		method returns either a DownloadVideoInfoDic in case of playlist URL or
		None and a video title in case of single video URL.
		
		:param url: playlist or single video url
		:return: downloadVideoInfoDic, videoTitle
		"""
		self.downloadVideoInfoDic, videoTitle = self.audioController.getDownloadVideoInfoDicOrSingleVideoTitleFortUrl(url)
	
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
		self.audioController.downloadVideosReferencedInPlaylistOrSingleVideo(self.playlistOrSingleVideoUrl, self.downloadVideoInfoDic, self.singleVideoTitle)
	
	def setMessage(self, msgText):
		pass
	
	def getConfirmation(self, title, msgText):
		self.popup = self.createConfirmPopup(title, msgText, self.onPopupAnswer)
		self.popup.open()
	
	def onPopupAnswer(self, instance, answer):
		answer = answer == 'yes'
		self.popup.dismiss()
		
		return answer
	
	def createConfirmPopup(self,
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

class ConfirmPopup(GridLayout):
	text = StringProperty()
	
	def __init__(self, **kwargs):
		self.register_event_type('on_answer')
		super(ConfirmPopup, self).__init__(**kwargs)
	
	def on_answer(self, *args):
		pass

# --- end AudioDownloaderGUI new code ---

class AudioDownloaderGUIApp(App):
	settings_cls = SettingsWithTabbedPanel
	audioDownloaderGUI = None

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.playlistOrSingleVideoUrl = None
		self.singleVideoTitle = None

	def build(self): # implicitely looks for a kv file of name audiodownloadergui.kv which is
					 # class name without App, in lowercases
		global fromAppBuilt
		fromAppBuilt = True

		if os.name != 'posix':
			# running app om Windows
			Config.set('graphics', 'width', '600')
			Config.set('graphics', 'height', '500')
			Config.write()

		self.title = 'AudioDownloader GUI'
		self.audioDownloaderGUI = AudioDownloaderGUI()

		return self.audioDownloaderGUI

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
		config.setdefaults(ConfigManager.CONFIG_SECTION_GENERAL,
						   {ConfigManager.CONFIG_KEY_TIME_ZONE: ConfigManager.DEFAULT_TIME_ZONE})
		config.setdefaults(ConfigManager.CONFIG_SECTION_GENERAL,
						   {ConfigManager.CONFIG_KEY_DATE_TIME_FORMAT: ConfigManager.DEFAULT_DATE_TIME_FORMAT})

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
		TIME_ZONE_LIST = """["Europe/Amsterdam", "Europe/Andorra", "Europe/Astrakhan", "Europe/Athens", "Europe/Belfast", "Europe/Belgrade", "Europe/Berlin", "Europe/Bratislava", "Europe/Brussels", "Europe/Bucharest", "Europe/Budapest", "Europe/Busingen", "Europe/Chisinau", "Europe/Copenhagen", "Europe/Dublin", "Europe/Gibraltar", "Europe/Guernsey", "Europe/Helsinki", "Europe/Isle_of_Man", "Europe/Istanbul", "Europe/Jersey", "Europe/Kaliningrad", "Europe/Kiev", "Europe/Kirov", "Europe/Lisbon", "Europe/Ljubljana", "Europe/London", "Europe/Luxembourg", "Europe/Madrid", "Europe/Malta", "Europe/Mariehamn", "Europe/Minsk", "Europe/Monaco", "Europe/Moscow", "Europe/Nicosia", "Europe/Oslo", "Europe/Paris", "Europe/Podgorica", "Europe/Prague", "Europe/Riga", "Europe/Rome", "Europe/Samara", "Europe/San_Marino", "Europe/Sarajevo", "Europe/Saratov", "Europe/Simferopol", "Europe/Skopje", "Europe/Sofia", "Europe/Stockholm", "Europe/Tallinn", "Europe/Tirane", "Europe/Tiraspol", "Europe/Ulyanovsk", "Europe/Uzhgorod", "Europe/Vaduz", "Europe/Vatican", "Europe/Vienna", "Europe/Vilnius", "Europe/Volgograd", "Europe/Warsaw", "Europe/Zagreb", "Europe/Zaporozhye", "Europe/Zurich", "GMT", "GMT+1", "GMT+2", "GMT+3", "GMT+4", "GMT+5", "GMT+6", "GMT+7", "GMT+8", "GMT+9", "GMT+10", "GMT+11", "GMT+12", "GMT+13", "GMT+14", "GMT+15", "GMT+16", "GMT+17", "GMT+18", "GMT+19", "GMT+20", "GMT+21", "GMT+22", "GMT+23", "GMT-1", "GMT-2", "GMT-3", "GMT-4", "GMT-5", "GMT-6", "GMT-7", "GMT-8", "GMT-9", "GMT-10", "GMT-11", "GMT-12", "GMT-13", "GMT-14", "GMT-15", "GMT-16", "GMT-17", "GMT-18", "GMT-19", "GMT-20", "GMT-21", "GMT-22", "GMT-23"]"""
		settings.add_json_panel("General", self.config, data=("""
			[
				{"type": "scrolloptions",
					"title": "Time zone",
					"desc": "Set the local time zone",
					"section": "General",
					"key": "timezone",
					"options": %s
				},
				{"type": "options",
					"title": "Date/time format",
					"desc": "Set the full date/time format",
					"section": "General",
					"key": "datetimeformat",
					"options": ["dd/mm/yy hh:mm"]
				},
				{"type": "path",
					"title": "Audiobook files root location",
					"desc": "Set the directory where the downloaded playlists are stored",
					"section": "General",
					"key": "dataPath"
				}
			]""" % TIME_ZONE_LIST)  # "key": "dataPath" above is the key in the app config file.
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
			elif key == ConfigManager.CONFIG_KEY_TIME_ZONE:
				self.root.configMgr.localTimeZone = config.getdefault(ConfigManager.CONFIG_SECTION_GENERAL, ConfigManager.CONFIG_KEY_TIME_ZONE, ConfigManager.DEFAULT_TIME_ZONE)
				self.root.configMgr.storeConfig()
			elif key == ConfigManager.CONFIG_KEY_DATE_TIME_FORMAT:
				self.root.configMgr.dateTimeFormat = config.getdefault(ConfigManager.CONFIG_SECTION_GENERAL, ConfigManager.CONFIG_KEY_DATE_TIME_FORMAT, ConfigManager.DEFAULT_DATE_TIME_FORMAT)
				self.root.configMgr.storeConfig()

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

	def on_start(self):
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
		
		downloadVideoInfoDic, videoTitle = self.audioDownloaderGUI.getDownloadVideoInfoDicOrSingleVideoTitleFortUrl(self.playlistOrSingleVideoUrl)
		self.singleVideoTitle = videoTitle
		
		if downloadVideoInfoDic is not None:
			downloadObjectTitle = downloadVideoInfoDic.getPlaylistTitle()
			confirmPopupTitle = "Go on with processing playlist ..."
		elif videoTitle is not None:
			downloadObjectTitle = videoTitle
			confirmPopupTitle = "Go on with downloading audio for video ... "
		else:
			# the case if the url is neither pointing to a playlist nor to a
			# single video. Here, an error message was displayed in the UI !
			return
			
		confirmPopupCallbackFunction = self.onPopupAnswer
		
		self.popup = self.audioDownloaderGUI.createConfirmPopup(confirmPopupTitle, downloadObjectTitle, confirmPopupCallbackFunction)
		self.popup.open()
	
	def onPopupAnswer(self, instance, answer):
		if answer == 'yes':
			self.audioDownloaderGUI.downloadPlaylistOrSingleVideoAudio(self.playlistOrSingleVideoUrl, self.singleVideoTitle)

		self.popup.dismiss()
		
	def loadHistoryDataIfSet(self):
		'''
		Testing at app start if data path defined in settings does exist
		and if history file loaded at start app does exist. Since a warning popup
		is displayed in case of invalid data, this must be performed here and
		not in audioDownloaderGUI.__init__ where no popup could be displayed.
		:return:
		'''
		dataPathNotExistMessage = self.audioDownloaderGUI.buildDataPathNotExistMessage(self.audioDownloaderGUI.dataPath)

		if self.audioDownloaderGUI.ensureDataPathExist(self.audioDownloaderGUI.dataPath, dataPathNotExistMessage):
			# loading the load at start history file if defined
			historyFilePathFilename = self.audioDownloaderGUI.configMgr.loadAtStartPathFilename
			dataFileNotFoundMessage = self.audioDownloaderGUI.buildFileNotFoundMessage(historyFilePathFilename)

			if historyFilePathFilename != '' and self.audioDownloaderGUI.ensureDataPathFileNameExist(historyFilePathFilename, dataFileNotFoundMessage):
				self.audioDownloaderGUI.loadHistoryFromPathFilename(historyFilePathFilename)
				self.audioDownloaderGUI.displayFileActionOnStatusBar(historyFilePathFilename, FILE_LOADED)

if __name__ == '__main__':
	dbApp = AudioDownloaderGUIApp()

	dbApp.run()
