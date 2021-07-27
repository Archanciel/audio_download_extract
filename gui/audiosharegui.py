from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.properties import BooleanProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout

import threading

from audiopositiongui import AudioPositionGUI
from asynchsliderupdater import AsynchSliderUpdater
from focustextinput import FocusTextInput # required for loading the audiosplittergui.kv file
from configmanager import ConfigManager
from constants import *
from customdropdown import CustomDropDown
from selectablerecycleboxlayout import SelectableRecycleBoxLayout


NAME_LABEL_KEY = 'nameLabel'
EMAIL_LABEL_KEY = 'emailLabel'
PHONE_NUMBER_LABEL_KEY = 'phoneNumberLabel'

CONTACT_NAME_KEY = 'name'
CONTACT_EMAIL_KEY = 'email'
CONTACT_PHONE_NUMBER_KEY = 'phoneNumber'

class AudioShareSelectableRecycleBoxLayout(SelectableRecycleBoxLayout):
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
		
		self.updateLineValues(AudioShareSelectableRecycleBoxLayout.MOVE_DIRECTION_UP, currentSelIdx, newSelIdx)
		self.select_node(nodes[newSelIdx])
		self.appGUI.refocusOnNameTextInputField()
	
	def moveItemDown(self):
		currentSelIdx, nodes = self.get_nodes()
		
		if not nodes:
			return
		
		if currentSelIdx == len(nodes) - 1:
			# moving down last item puts it at first item position
			newSelIdx = 0
		else:
			newSelIdx = currentSelIdx + 1
		
		self.updateLineValues(AudioShareSelectableRecycleBoxLayout.MOVE_DIRECTION_DOWN, currentSelIdx, newSelIdx)
		self.select_node(nodes[newSelIdx])
		self.appGUI.refocusOnNameTextInputField()
	
	def updateLineValues(self, moveDirection, movedItemSelIndex, movedItemNewSeIndex):
		movedName, movedEmail, movedPhoneNumber = self.getSelectedContactValues(movedItemSelIndex)
		
		if moveDirection == AudioShareSelectableRecycleBoxLayout.MOVE_DIRECTION_DOWN:
			if movedItemSelIndex > movedItemNewSeIndex:
				# we are moving down the last list item. The item will be inserted at top
				# of the list
				self.parent.data.pop(movedItemSelIndex)
				self.parent.data.insert(0, {NAME_LABEL_KEY: movedName, EMAIL_LABEL_KEY: movedEmail, PHONE_NUMBER_LABEL_KEY: movedPhoneNumber, 'selectable': True})
			else:
				replacedName, replacedEmail, replacedPhoneNumber = self.getSelectedContactValues(movedItemNewSeIndex)
				self.parent.data.pop(movedItemSelIndex)
				self.parent.data.insert(movedItemSelIndex, {NAME_LABEL_KEY: replacedName, EMAIL_LABEL_KEY: replacedEmail, PHONE_NUMBER_LABEL_KEY: replacedPhoneNumber, 'selectable': True})

				self.parent.data.pop(movedItemNewSeIndex)
				self.parent.data.insert(movedItemNewSeIndex, {NAME_LABEL_KEY: movedName, EMAIL_LABEL_KEY: movedEmail, PHONE_NUMBER_LABEL_KEY: movedPhoneNumber, 'selectable': True})
		else:
			# handling moving up
			if movedItemSelIndex == 0:
				# we are moving up the first item. The first item will be appended to the
				# end of the list
				self.parent.data.pop(movedItemSelIndex)
				self.parent.data.append({NAME_LABEL_KEY: movedName, EMAIL_LABEL_KEY: movedEmail, PHONE_NUMBER_LABEL_KEY: movedPhoneNumber, 'selectable': True})
			else:
				replacedName, replacedEmail, replacedPhoneNumber = self.getSelectedContactValues(movedItemNewSeIndex)
				self.parent.data.pop(movedItemSelIndex)
				self.parent.data.insert(movedItemSelIndex, {NAME_LABEL_KEY: replacedName, EMAIL_LABEL_KEY: replacedEmail, PHONE_NUMBER_LABEL_KEY: replacedPhoneNumber, 'selectable': True})

				self.parent.data.pop(movedItemNewSeIndex)
				self.parent.data.insert(movedItemNewSeIndex, {NAME_LABEL_KEY: movedName, EMAIL_LABEL_KEY: movedEmail, PHONE_NUMBER_LABEL_KEY: movedPhoneNumber, 'selectable': True})
		
		# appGUI.recycleViewCurrentSelIndex is used by the
		# deleteRequest() and updateRequest() appGUI methods
		self.appGUI.recycleViewCurrentSelIndex = movedItemNewSeIndex
		
	def getSelectedContactValues(self, movedItemSelIndex):
		'''
		Returns values of the selected line in the contact list.

		:return: name, email, phoneNumber
		'''
		name = self.parent.data[movedItemSelIndex][NAME_LABEL_KEY]
		email = self.parent.data[movedItemSelIndex][EMAIL_LABEL_KEY]
		phoneNumber =  self.parent.data[movedItemSelIndex][PHONE_NUMBER_LABEL_KEY]
		
		return name, email, phoneNumber
	
	def getLoadedContactValues(self, movedItemSelIndex):
		'''
		Returns values of the selected contact list item.

		:return: name, email, phoneNumber
		'''
		name = self.parent.data[movedItemSelIndex][CONTACT_NAME_KEY]
		email = self.parent.data[movedItemSelIndex][CONTACT_EMAIL_KEY]
		phoneNumber = self.parent.data[movedItemSelIndex][CONTACT_PHONE_NUMBER_KEY]
		
		return name, email, phoneNumber


class MultiFieldSelectableBoxLayout(RecycleDataViewBehavior, BoxLayout):
	''' Add selection support to the Label '''
	index = None
	selected = BooleanProperty(False)
	selectable = BooleanProperty(True)
	
	def refresh_view_attrs(self, rv, index, data):
		''' Catch and handle the view changes '''
		self.rv = rv
		self.audioShareGUI = rv.rootGUI
		self.index = index
		
		return super(MultiFieldSelectableBoxLayout, self).refresh_view_attrs(
			rv, index, data)
	
	def on_touch_down(self, touch):
		''' Add selection on touch down '''
		if len(self.audioShareGUI.requestListRVSelBoxLayout.selected_nodes) == 1:
			# here, the user manually deselects the selected item. When
			# on_touch_down is called, if the item is selected, the
			# requestListRVSelBoxLayout.selected_nodes list has one element !
			self.audioShareGUI.nameTextInputField.text = ''
			self.audioShareGUI.emailTextInputField.text = ''
			self.audioShareGUI.phoneNumberTextInputField.text = ''

			# appGUI.recycleViewCurrentSelIndex is used by the
			# deleteRequest() and updateRequest() appGUI methods
			self.audioShareGUI.recycleViewCurrentSelIndex = -1
		
		if super(MultiFieldSelectableBoxLayout, self).on_touch_down(touch):
			return True
		if self.collide_point(*touch.pos) and self.selectable:
			return self.parent.select_with_touch(self.index, touch)
	
	def apply_selection(self, rv, index, is_selected):
		# instance variable used in .kv file to change the selected item
		# color !
		self.selected = is_selected
		
		if is_selected:
			selName = rv.data[index][NAME_LABEL_KEY]
			selEmail = rv.data[index][EMAIL_LABEL_KEY]
			selPhoneNumber = rv.data[index][PHONE_NUMBER_LABEL_KEY]

			# appGUI.recycleViewCurrentSelIndex is used by the
			# deleteRequest() and updateRequest() appGUI methods
			self.audioShareGUI.recycleViewCurrentSelIndex = index
			self.audioShareGUI.nameTextInputField.text = selName
			self.audioShareGUI.emailTextInputField.text = selEmail
			self.audioShareGUI.phoneNumberTextInputField.text = selPhoneNumber

		self.audioShareGUI.refocusOnNameTextInputField()
		self.audioShareGUI.enableStateOfRequestListSingleItemButtons()


class AudioShareGUI(AudioPositionGUI):
	showRequestList = False

	def __init__(self, **kw):
		super(AudioShareGUI, self).__init__(**kw)
		
	def _finish_init(self, dt):
		"""
		Due to using WindowManager for managing multiple screens, the content
		of this method can no longer be located in the __init__ ctor method,
		but must be called by Clock.schedule_once() (located in the base
		class).

		:param dt:
		"""
		self.soundloaderSharedMp3Obj = None
		self.dropDownMenu = CustomDropDown(owner=self)

		if os.name == 'posix':
			configPath = '/sdcard/audiodownloader.ini'
			requestListRVSpacing = RV_LIST_ITEM_SPACING_ANDROID
		else:
			configPath = 'c:\\temp\\audiodownloader.ini'
			requestListRVSpacing = RV_LIST_ITEM_SPACING_WINDOWS

		self.configMgr = ConfigManager(configPath)
		self.dataPath = self.configMgr.dataPath

		self.setRVListSizeParms(int(self.configMgr.histoListItemHeight),
								int(self.configMgr.histoListVisibleSize),
								requestListRVSpacing)

		self.loadHistoryDataIfSet()
	
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
		
		self.refocusOnNameTextInputField()
	
	def adjustRequestListSize(self):
		listItemNumber = len(self.requestListRV.data)
		self.boxLayoutContainingRV.height = min(listItemNumber * self.rvListItemHeight, self.maxRvListHeight)
		
		return listItemNumber
	
	def deleteRequest(self, *args):
		# deleting selected item from RecycleView list
		self.requestListRV.data.pop(self.recycleViewCurrentSelIndex)
		
		remainingItemNb = len(self.requestListRV.data)
		
		if remainingItemNb == 0:
			# no more item in RecycleView list
			self.disableStateOfRequestListSingleItemButtons()
			self.toggleHistoButton.disabled = True
			self.showRequestList = False
			self.nameTextInputField.text = ''
			self.emailTextInputField.text = ''
			self.phoneNumberTextInputField.text = ''
		
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
		
		self.refocusOnNameTextInputField()
	
	def clearHistoryListSelection(self):
		self.requestListRV._get_layout_manager().clear_selection()
	
	def replaceRequest(self, *args):
		# Remove the selected item
		self.requestListRV.data.pop(self.recycleViewCurrentSelIndex)
		
		# Get new values from the TextInput fields
		name, email, phoneNumber = self.getInputContactValues()
		
		# Add the updated data to the list if not already in
		requestListEntry = {NAME_LABEL_KEY: name, EMAIL_LABEL_KEY: email, PHONE_NUMBER_LABEL_KEY: phoneNumber, 'selectable': True}
		
		if not requestListEntry in self.requestListRV.data:
			self.requestListRV.data.insert(self.recycleViewCurrentSelIndex, requestListEntry)
		
		self.refocusOnNameTextInputField()

	def setInputValues(self):
		# Get new values from the TextInput fields
		name, email, phoneNumber = self.getInputContactValues()

		if name != '' and email != '' and phoneNumber != '':
			requestListEntry = {NAME_LABEL_KEY: name, EMAIL_LABEL_KEY: email, PHONE_NUMBER_LABEL_KEY: phoneNumber, 'selectable': True}

			if not requestListEntry in self.requestListRV.data:
				self.requestListRV.data.insert(self.recycleViewCurrentSelIndex, requestListEntry)
			
			self.resetListViewScrollToEnd()
			self.manageStateOfGlobalRequestListButtons()
			
			self.nameTextInputField.text = ''
			self.emailTextInputField.text = ''
			self.phoneNumberTextInputField.text = ''
			
			self.refocusOnNameTextInputField()
		elif name == '':
			self.nameTextInputField.focus = True
		elif email == '':
			self.emailTextInputField.focus = True
		else:
			self.phoneNumberTextInputField.focus = True
			
	def getInputContactValues(self):
		'''
		Returns new values from the TextInput fields.

		:return: name, email, phoneNumber
		'''
		name = self.nameTextInputField.text
		email = self.emailTextInputField.text
		phoneNumber = self.phoneNumberTextInputField.text
		
		return name, email, phoneNumber
	
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
	
	def loadHistoryFromPathFilename(self, pathFileName):
		self.currentLoadedFathFileName = pathFileName
		dataFileNotFoundMessage = self.buildFileNotFoundMessage(pathFileName)
		
		if not self.ensureDataPathFileNameExist(pathFileName, dataFileNotFoundMessage):
			return
		
		with open(pathFileName) as stream:
			lines = stream.readlines()
		
		lines = list(map(lambda line: line.strip('\n'), lines))
		#histoLines = [{'text': val, 'selectable': True} for val in lines
		
		items = [{CONTACT_NAME_KEY: 'Jean-Pierre Schnyder', CONTACT_EMAIL_KEY: 'jp.schnyder@gmail.com', CONTACT_PHONE_NUMBER_KEY: '+41768224987'},
		         {CONTACT_NAME_KEY: 'Tamara Jagne', CONTACT_EMAIL_KEY: 'tamara.jagne@gmail.com', CONTACT_PHONE_NUMBER_KEY: '+41764286884'}
		         ]
		
		histoLines = [{NAME_LABEL_KEY: str(x[CONTACT_NAME_KEY]), EMAIL_LABEL_KEY: str(x[CONTACT_EMAIL_KEY]), PHONE_NUMBER_LABEL_KEY: str(x[CONTACT_PHONE_NUMBER_KEY]), 'selectable': True} for x in items]

		self.requestListRV.data = histoLines
		self.requestListRVSelBoxLayout.clear_selection()
		
		# Reset the ListView
		self.resetListViewScrollToEnd()
		
		self.manageStateOfGlobalRequestListButtons()
		self.refocusOnNameTextInputField()
	
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
			self.boxLayoutContainingRV.height = '0dp'
			self.dropDownMenu.saveButton.disabled = True
		else:
			self.toggleHistoButton.disabled = False
			self.dropDownMenu.saveButton.disabled = False
	
	def refocusOnNameTextInputField(self):
		# defining a delay of 0.5 sec ensure the
		# refocus works in all situations, moving
		# up and down comprised (0.1 sec was not
		# sufficient for item move ...)
		Clock.schedule_once(self._refocusOnNameTextInputField, 0.5)
	
	def _refocusOnNameTextInputField(self, *args):
		'''
		This method is here to be used as callback by Clock and must not be called directly
		:param args:
		:return:
		'''
		self.nameTextInputField.focus = True

	def openDropDownMenu(self, widget):
		self.dropDownMenu.open(widget)

	def initSoundFile(self, sharedAudioFilePathName):
		if 'mp3' != sharedAudioFilePathName[-3:]:
			return
		
		self.sharedAudioFilePathNameInitValue = sharedAudioFilePathName
		self.sharedAudioFilePathName.text = sharedAudioFilePathName
		self.soundloaderSharedMp3Obj = SoundLoader.load(sharedAudioFilePathName)
		
		# setting focus on startTextInput must be done here, not in
		# the _finish_init() method !
		self.sharedAudioFilePathName.focus = True
	
	def playSharedFile(self):
		"""
		Method called when pressing the share file Play button
		"""
		self.sharedFilePlayButton.disabled = True
		self.soundloaderSharedMp3Obj.play()

	def stopSharedFile(self):
		"""
		Method called when pressing the source file Stop button
		"""
		self.soundloaderSharedMp3Obj.stop()
		self.sharedFilePlayButton.disabled = False
	
	def cancelSharedFile(self):
		"""
		Method called when Cancel button is pressed.
		"""
		self.stopSharedFile()
	
	def goToSharedFileStartPos(self):
		"""
		Method called when source file <| button is pressed.
		"""
		self.updateFileSoundPos(soundloaderMp3Obj=self.soundloaderSharedMp3Obj,
		                        newSoundPos=0,
		                        soundFilePlayButton=self.sharedFilePlayButton)
	
	def goToSharedFileEndPos(self):
		"""
		Method called when source file |> button is pressed.
		"""
		endPos = self.soundloaderSharedMp3Obj.length - 5
		self.updateFileSoundPos(soundloaderMp3Obj=self.soundloaderSharedMp3Obj,
		                        newSoundPos=endPos,
		                        soundFilePlayButton=self.sharedFilePlayButton)
	
	def forwardSharedFileTenSeconds(self):
		"""
		Method called when source file > button is pressed.
		"""
		currentPos = self.soundloaderSharedMp3Obj.get_pos()
		currentPos += 10
		self.updateFileSoundPos(soundloaderMp3Obj=self.soundloaderSharedMp3Obj,
		                        newSoundPos=currentPos,
		                        soundFilePlayButton=self.sharedFilePlayButton)
	
	def forwardSharedFileThirtySeconds(self):
		"""
		Method called when source file >> button is pressed.
		"""
		currentPos = self.soundloaderSharedMp3Obj.get_pos()
		currentPos += 30
		self.updateFileSoundPos(soundloaderMp3Obj=self.soundloaderSharedMp3Obj,
		                        newSoundPos=currentPos,
		                        soundFilePlayButton=self.sharedFilePlayButton)
	
	def backwardSharedFileTenSeconds(self):
		"""
		Method called when source file < button is pressed.
		"""
		currentPos = self.soundloaderSharedMp3Obj.get_pos()
		currentPos -= 10
		self.updateFileSoundPos(soundloaderMp3Obj=self.soundloaderSharedMp3Obj,
		                        newSoundPos=currentPos,
		                        soundFilePlayButton=self.sharedFilePlayButton)

	def backwardSharedFileThirtySeconds(self):
		"""
		Method called when source file << button is pressed.
		"""
		currentPos = self.soundloaderSharedMp3Obj.get_pos()
		currentPos -= 30
		self.updateFileSoundPos(soundloaderMp3Obj=self.soundloaderSharedMp3Obj,
		                        newSoundPos=currentPos,
		                        soundFilePlayButton=self.sharedFilePlayButton)
	
	def shareSharedFile(self):
		"""
		Method called when Share button is pressed.
		"""
		print('shareShareFile not yet implemented')
