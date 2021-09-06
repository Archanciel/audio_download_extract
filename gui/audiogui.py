import logging
import os

from kivy import platform
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from constants import *
from configmanager import ConfigManager
from gui.customdropdown import CustomDropDown
from gui.guiutil import GuiUtil
from gui.helppopup import HelpPopup

AUDIODOWNLOADER_VERSION = 'AudioDownloader 2.0'
FILE_ACTION_LOAD = 0

class AudioGUI(Screen):
	"""
	Abstract base class for the audio downloader GUI classes.
	"""
	def __init__(self, **kw):
		super().__init__(**kw)
		
		self.showRequestList = False
		self.isExtractFileDropDownMenuItemDisplayed = True
		self.isShareFileDropDownMenuItemDisplayed = True
		self.isSettingsDropDownMenuItemDisplayed = True
		self.dropDownMenu = CustomDropDown(owner=self)
		self.error = False
		
		# WARNING: accessing MainWindow fields defined in kv file
		# in the __init__ ctor is no longer possible when using
		# ScreenManager. Here's the solution:
		# (https://stackoverflow.com/questions/26916262/why-cant-i-access-the-screen-ids)
		Clock.schedule_once(self._finish_init)

	def _finish_init(self, dt):
		"""
		Due to using WindowManager for managing multiple screens, the content
		of this method can no longer be located in the __init__ ctor method,
		but must be called by Clock.schedule_once().

		:param dt:
		"""
		
		configFileName = 'audiodownloader.ini'
		
		if os.name == 'posix':
			self.configFilePath = '/sdcard/'
			configFilePathName = '%s%s' % (self.configFilePath, configFileName)
			requestListRVSpacing = RV_LIST_ITEM_SPACING_ANDROID
		else:
			self.configFilePath = 'c:\\temp\\'
			configFilePathName = '%s%s' % (self.configFilePath, configFileName)
			requestListRVSpacing = RV_LIST_ITEM_SPACING_WINDOWS

		try:
			self.configMgr = ConfigManager(configFilePathName)
		except FileNotFoundError as e:
			self.configMgr = None
			msgText = 'Configuration file dir {} not found. Solve the problem and restart the application.'.format(self.configFilePath)
			self.displayPopupError(msgText)
			logging.error(e)
			self.error = True
			return
		
		self.audiobookPath = self.configMgr.dataPath
		self.audiobookSingleVideoPath = self.configMgr.singleVideoDataPath

		self.setRVListSizeParms(int(self.configMgr.histoListItemHeight),
								int(self.configMgr.histoListVisibleSize),
								requestListRVSpacing)

		self.loadHistoryDataIfSet()

	def outputResult(self, resultStr):
		markupBoldStart = '[b]'
		markupBoldEnd = '[/b]'
		
		if len(self.outputLabel.text) == 0:
			self.outputLabel.text = markupBoldStart + resultStr + markupBoldEnd
		else:
			self.outputLabel.text = self.outputLabel.text + '\n' + markupBoldStart + resultStr + markupBoldEnd

		# scrolling to end of output text
		self.outputScrollView.scroll_y = 0
	
	def displayPopupWarning(self, message):
		self.displayPopup(title='AudioDownloader WARNING',
		                  message=message)
	
	def displayPopupError(self, message):
		self.displayPopup(title='AudioDownloader ERROR',
		                  message=message)
	
	def displayPopup(self, title, message):
		popupSize = None

		if platform == 'android':
			if GuiUtil.onSmartPhone():
				popupSize = (1180, 550)
				messageMaxLength = 40
			else:
				popupSize = (1280, 300)
				messageMaxLength = 70
		elif platform == 'win':
			popupSize = (450, 150)
			messageMaxLength = 60

		# this code ensures that the popup content text does not exceeds
		# the popup borders
		
		sizingLabel = Label(text=GuiUtil.reformatString(message, messageMaxLength))

		popup = Popup(title=title, content=sizingLabel,
		              auto_dismiss=True, size_hint=(None, None),
		              size=popupSize)
		popup.open()

	def buildDataPathNotExistMessage(self, path):
		return 'Data path ' + path + '\nas defined in the settings does not exist !\nEither create the directory or change the\ndata path value using the Settings menu.'
	
	def buildFileNotFoundMessage(self, filePathFilename):
		return 'Data file\n' + filePathFilename + '\nnot found. No history loaded.'
	
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
	
	def displayHelp(self):
		self.dropDownMenu.dismiss()

		popup = HelpPopup(title=AUDIODOWNLOADER_VERSION)
		popup.open()
	
	def openDropDownMenu(self, widget):
		
		dropDownMenuItemheight = self.dropDownMenu.saveButton.height
		
		if self.isExtractFileDropDownMenuItemDisplayed:
			# set drop down menu items visible
			self.dropDownMenu.gridLayoutSplit.height = dropDownMenuItemheight
		else:
			# hide drop down menu items
			self.dropDownMenu.gridLayoutSplit.height = 0
		
		if self.isShareFileDropDownMenuItemDisplayed:
			# set drop down menu items visible
			self.dropDownMenu.gridLayoutShare.height = dropDownMenuItemheight
		else:
			# hide drop down menu items
			self.dropDownMenu.gridLayoutShare.height = 0
		
		if self.isSettingsDropDownMenuItemDisplayed:
			# set drop down menu items visible
			self.dropDownMenu.gridLayoutSettings.height = dropDownMenuItemheight
		else:
			# hide drop down menu items
			self.dropDownMenu.gridLayoutSettings.height = 0
		
		self.dropDownMenu.open(widget)
	
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
	
	def loadHistoryDataIfSet(self):
		'''
		Testing at app start if data path defined in settings does exist
		and if history file loaded at start app does exist. Since a warning popup
		is displayed in case of invalid data, this must be performed here and
		not in audioDownloaderGUI.__init__ where no popup could be displayed.
		:return:
		'''
		dataPathNotExistMessage = self.buildDataPathNotExistMessage(self.audiobookPath)
		
		if self.ensureDataPathExist(self.audiobookPath, dataPathNotExistMessage):
			# loading the load at start history file if defined
			historyFilePathFilename = self.configMgr.loadAtStartPathFilename
			dataFileNotFoundMessage = self.buildFileNotFoundMessage(historyFilePathFilename)
			
			if historyFilePathFilename != '' and self.ensureDataPathFileNameExist(
					historyFilePathFilename, dataFileNotFoundMessage):
				self.loadHistoryFromPathFilename(historyFilePathFilename)
				self.displayFileActionOnStatusBar(historyFilePathFilename, FILE_ACTION_LOAD)

	def displayFileActionOnStatusBar(self, *unused):
		pass
	
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
	
	def disableStateOfRequestListSingleItemButtons(self):
		self.deleteButton.disabled = True
		self.replaceButton.disabled = True
		self.moveUpButton.disabled = True
		self.moveDownButton.disabled = True
	
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
		
		self.refocusOnFirstRequestInput()
	
	def adjustRequestListSize(self):
		listItemNumber = len(self.requestListRV.data)
		self.boxLayoutContainingRV.height = min(listItemNumber * self.rvListItemHeight, self.maxRvListHeight)

		return listItemNumber
	
	def _refocusOnFirstTextInput(self, *args):
		'''
		This method is here to be used as callback by Clock and must not be called directly
		:param args:
		:return:
		'''
		self.requestInput.focus = True
	
	def refocusOnFirstRequestInput(self):
		# defining a delay of 0.5 sec ensure the
		# refocus works in all situations, moving
		# up and down comprised (0.1 sec was not
		# sufficient for item move ...)
		Clock.schedule_once(self._refocusOnFirstTextInput, 0.5)
	
	def deleteRequest(self, *args):
		# deleting selected item from RecycleView list
		self.requestListRV.data.pop(self.recycleViewCurrentSelIndex)
		
		remainingItemNb = len(self.requestListRV.data)
		
		if remainingItemNb == 0:
			# no more item in RecycleView list
			self.disableStateOfRequestListSingleItemButtons()
			self.toggleHistoButton.disabled = True
			self.showRequestList = False
			self.emptyRequestFields()
		
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
		self.refocusOnFirstRequestInput()
		
	def emptyRequestFields(self):
		pass