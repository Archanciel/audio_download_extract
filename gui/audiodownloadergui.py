import logging
import os, sys, inspect
import time
from configparser import NoOptionError

TOGGLE_DOWNLOAD_ALL_BUTTON_DOWN_ALL = 'Down All'
TOGGLE_DOWNLOAD_ALL_BUTTON_DOWN_DEL = 'Del All'

TOGGLE_HISTO_BUTTON_URL = "Url's"
TOGGLE_HISTO_BUTTON_DOWN_HIST = 'Dl Hist'

TOGGLE_DELETE_BUTTON_DELETE = "Delete"
TOGGLE_DELETE_BUTTON_BROWSER = 'Browser'

TIME_SLEEP_SECONDS = 1

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from os.path import sep

from kivy.app import App
from kivy.config import Config
from kivy.metrics import dp
from kivy.properties import BooleanProperty
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
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

import webbrowser

from gui.filechooserpopup import LoadFileChooserPopup
from gui.filechooserpopup import SaveFileChooserPopup
from gui.filechooserpopup import DeleteFileChooserPopup
from gui.filechooserpopup import SelectOrCreateDirFileChooserPopup
from gui.filechooserpopup import FileToClipLoadFileChooserPopup
from gui.filechooserpopup import FileToShareLoadFileChooserPopup
from gui.confirmdownloadpopup import ConfirmDownloadPopup
from gui.yesnopopup import YesNoPopup

from gui.audiogui import AudioGUI
from gui.audiogui import FILE_ACTION_LOAD
from constants import *
from configmanager import ConfigManager
from audiocontroller import AudioController
from gui.guiutil import GuiUtil
from gui.selectablerecycleboxlayout import SelectableRecycleBoxLayout
from dirutil import DirUtil
from septhreadexec import SepThreadExec
from downloadplaylistinfodic import DownloadPlaylistInfoDic
from downloadUrlinfodic import DownloadUrlInfoDic
from urldownloaddata import UrlDownloadData
from downloadhistorydata import *

STATUS_BAR_ERROR_SUFFIX = ' --> ERROR ...'
FILE_ACTION_SAVE = 1
FILE_ACTION_SELECT_OR_CREATE_DIR = 2
FILE_ACTION_SELECT_FILE_TO_SPLIT = 3
FILE_ACTION_SELECT_FILE_TO_SHARE = 4
FILE_ACTION_DELETE = 5

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
				movedItemToDownloadValue = self.parent.data[movedItemSelIndex]['toDownload']
				movedUrlDownloadData = self.parent.data.pop(movedItemSelIndex)['data']
				self.parent.data.insert(0, {'text': movedValue, 'data': movedUrlDownloadData,
				                            'toDownload': movedItemToDownloadValue, 'selectable': True})
			else:
				replacedValue = self.parent.data[movedItemNewSeIndex]['text']
				replaceUrlDownloadData = self.parent.data[movedItemNewSeIndex]['data']
				replacedItemToDownloadValue = self.parent.data[movedItemNewSeIndex]['toDownload']
				movedItemToDownloadValue = self.parent.data[movedItemSelIndex]['toDownload']
				movedUrlDownloadData = self.parent.data.pop(movedItemSelIndex)['data']
				self.parent.data.insert(movedItemSelIndex, {'text': replacedValue, 'data': replaceUrlDownloadData,
				                                            'toDownload': replacedItemToDownloadValue,
				                                            'selectable': True})
				
				self.parent.data.pop(movedItemNewSeIndex)
				self.parent.data.insert(movedItemNewSeIndex, {'text': movedValue, 'data': movedUrlDownloadData,
				                                              'toDownload': movedItemToDownloadValue,
				                                              'selectable': True})
		else:
			# handling moving up
			if movedItemSelIndex == 0:
				# we are moving up the first item. The first item will be appended to the
				# end of the list
				movedItemToDownloadValue = self.parent.data[movedItemSelIndex]['toDownload']
				movedUrlDownloadData = self.parent.data.pop(movedItemSelIndex)['data']
				self.parent.data.append(
					{'text': movedValue, 'data': movedUrlDownloadData, 'toDownload': movedItemToDownloadValue,
					 'selectable': True})
			else:
				replacedValue = self.parent.data[movedItemNewSeIndex]['text']
				replaceUrlDownloadData = self.parent.data[movedItemNewSeIndex]['data']
				replacedItemToDownloadValue = self.parent.data[movedItemNewSeIndex]['toDownload']
				movedItemToDownloadValue = self.parent.data[movedItemSelIndex]['toDownload']
				movedUrlDownloadData = self.parent.data.pop(movedItemSelIndex)['data']
				self.parent.data.insert(movedItemSelIndex, {'text': replacedValue, 'data': replaceUrlDownloadData,
				                                            'toDownload': replacedItemToDownloadValue,
				                                            'selectable': True})
				
				self.parent.data.pop(movedItemNewSeIndex)
				self.parent.data.insert(movedItemNewSeIndex, {'text': movedValue, 'data': movedUrlDownloadData,
				                                              'toDownload': movedItemToDownloadValue,
				                                              'selectable': True})
		
		# appGUI.recycleViewCurrentSelIndex is used by the
		# deleteOrBrowseItem() and updateRequest() appGUI methods
		self.appGUI.recycleViewCurrentSelIndex = movedItemNewSeIndex


class SelectableMultiFieldsItem(RecycleDataViewBehavior, GridLayout):
	''' Add selection support to the Label '''
	index = None
	selected = BooleanProperty(False)
	selectable = BooleanProperty(True)
	
	def __init__(self):
		
		super().__init__()
		self.rv = None
	
	def refresh_view_attrs(self, rv, index, data):
		''' Catch and handle the view changes '''
		
		# storing reference on the recycle view
		
		self.rv = rv
		self.audioDownloaderGUI = rv.rootGUI
		self.index = index
		
		return super(SelectableMultiFieldsItem, self).refresh_view_attrs(
			rv, index, data)
	
	def on_touch_down(self, touch):
		''' Add selection on touch down '''
		if len(self.audioDownloaderGUI.requestListRVSelBoxLayout.selected_nodes) == 1:
			# here, the user manually deselects the selected item. When
			# on_touch_down is called, if the item is selected, the
			# requestListRVSelBoxLayout.selected_nodes list has one element !
			self.audioDownloaderGUI.requestInput.text = ''
			
			# appGUI.recycleViewCurrentSelIndex is used by the
			# deleteOrBrowseItem() and updateRequest() appGUI methods
			self.audioDownloaderGUI.recycleViewCurrentSelIndex = -1
		
		if super(SelectableMultiFieldsItem, self).on_touch_down(touch):
			return True
		if self.collide_point(*touch.pos) and self.selectable:
			return self.parent.select_with_touch(self.index, touch)
	
	def apply_selection(self, rv, index, is_selected):
		# instance variable used in .kv file to change the selected item
		# color !
		self.selected = is_selected
		
		if is_selected:
			selItemUrlTitle = rv.data[index]['text']
			selItemDownloadData = rv.data[index]['data']
			if isinstance(selItemDownloadData, DownloadHistoryData):
				# here, the list contains download history information
				self.audioDownloaderGUI.isDownloadHistoDisplayed = True
				if selItemDownloadData.type == DHD_TYPE_AUDIO_FILE:
					self.audioDownloaderGUI.displayDownloadedFileName(selItemDownloadData)
			elif isinstance(selItemDownloadData, UrlDownloadData):
				# here, selItemDownloadData is an instance of UrlDownLoadData
				self.audioDownloaderGUI.isDownloadHistoDisplayed = False
				selItemUrl = selItemDownloadData.url
				Clipboard.copy(selItemUrl)
				self.audioDownloaderGUI.requestInput.text = selItemUrlTitle
			
			# appGUI.recycleViewCurrentSelIndex is used by the
			# deleteOrBrowseItem() and updateRequest() appGUI methods
			self.audioDownloaderGUI.recycleViewCurrentSelIndex = index
			
			self.audioDownloaderGUI.clearStatusBar()
		
		# next instruction fixes incomprehensible problem of setting chkbox
		# to active on other items when moving an item where the chkbox is
		# active !
		if index <= len(rv.data) - 1:
			# avoids IndexError exception happening sometimes
			self.ids.download_chkbox.active = rv.data[index]['toDownload']
		
		self.audioDownloaderGUI.refocusOnFirstRequestInput()
		self.audioDownloaderGUI.enableStateOfRequestListSingleItemButtons()
	
	def toggleCheckbox(self, chkbox, isChecked):
		selectableMultiFieldsItem = chkbox.parent
		recycleView = selectableMultiFieldsItem.parent.parent
		
		# problem: after deleting a file, the playlist item chkbox is selected !!!
		#
		# if not recycleView.data[selectableMultiFieldsItem.index]['selectable']:
		# 	# useful when the request list contains downloaded files histo.
		# 	# The playlist list items 'selectable' element is set to False (True again
		#   in order to enable opening browser !)	.
		# 	# So, checking the checkbox for a playlist name does not set
		# 	# the chkbox to active.
		# 	chkbox.active = False
		
		recycleView.data[selectableMultiFieldsItem.index]['toDownload'] = isChecked


#		logging.info('toggleCheckbox in item {}: {}'.format(selectableMultiFieldsItem.index, isChecked))


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
		popup = Popup(content=content, title=self.title, size_hint=(0.5, 0.9), auto_dismiss=False)
		
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
		
		self.partiallyDownloadedPlaylistDic = {}
	
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
				self.stopDownloadButton.width = 150
				self.downloadButton.width = 300
				self.addDownloadButton.width = 150
			else:
				self.stopDownloadButton.width = 80
				self.downloadButton.width = 190
				self.addDownloadButton.width = 80
		else:
			# self.stopDownloadButton.text = 'Half'  # correct on Windows !
			self.stopDownloadButton.width = 40
			self.downloadButton.width = 80
			self.addDownloadButton.width = 40
		
		self.audioController = AudioController(self, self.configMgr)
		self.appSize = self.configMgr.appSize
		self.defaultAppPosAndSize = self.configMgr.appSize
		self.appSizeHalfProportion = float(self.configMgr.appSizeHalfProportion)
		self.excludedSubDirNameLst = self.configMgr.excludedAudioSubdirNameLst
		self.boxLayoutContainingStatusBar.height = dp(self.configMgr.statusbarHeight)
		self.clearResultOutputButton.width = dp(self.configMgr.clearButtonWidth)
		# self.applyAppPosAndSize() # commenting it since it is currently not
		# usefull in the AudioDownload app !
		# Additionally, it avoids that the 'Stop'
		# button is set to 'Half' or 'Full'
		self.movedRequestNewIndex = -1
		self.movingRequest = False
		self.currentLoadedPathFileName = ''
		self.outputLineBold = True
		self.fileChooserPopup = None
		self.downloadVideoInfoDic = None
		self.originalPlaylistTitle = None
		self.modifiedPlaylistTitle = None
		self.modifiedSingleVideoTitle = None
		self.originalSingleVideoTitle = None
		self.downloadThreadCreated = False  # used to fix a problem on Android
		# where two download threads are
		# created after clicking on 'Yes'
		# button on the ConfirmPopup dialog
		self.downloadObjectTitleThreadCreated = False
		self.playlistOrSingleVideoDownloadPath = None
		self.accessError = None
		self.isUploadDateAddedToPlaylistVideo = False
		self.isIndexAddedToPlaylistVideo = False
		self.downloadFromUrlDownloadLstThreadCreated = False
		self.downloadUrlInfoDic = None
		
		self.totalDownloadVideoSuccessNb = 0
		self.totalDownloadVideoFailedNb = 0
		self.totalDownloadVideoSkippedNb = 0
		self.downloadUrlLst = []
		self.isDownloadHistoDisplayed = False
		self.failedVideoPlaylistDic = None
		
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
	
	def addDownloadUrlToUrlList(self,
	                            playlistOrSingleVideoModifiedTitle='',
	                            downloadSubdir='',
	                            playlistOrSingleVideoUrl=''):
		"""
		Method called
		
		1/ when pressing the add download button defined in the audiodownloadergui.kv file. In this case, the passed
		   download sub dir as well as the passed playlistOrSingleVideoUrl are empty
		2/ after setting the download dir of the playlist or single video. In this case, the download sub dir is not
		   empty
		
		:param playlistOrSingleVideoModifiedTitle: == '' if 'Add' button was pressed !
		:param downloadSubdir:
		:param playlistOrSingleVideoUrl:
		:return:
		"""
		if playlistOrSingleVideoUrl == '':
			# method called after pressing the 'Add' button
			playlistOrSingleVideoUrl = Clipboard.paste()
		
		if playlistOrSingleVideoUrl != '' and \
				playlistOrSingleVideoUrl != ' ' and \
				len(playlistOrSingleVideoUrl.split('\n')) == 1 and \
				playlistOrSingleVideoUrl.startswith('https://'):
			
			title = None
			type = None
			
			while title is None:
				self.downloadFromClipboard(onlyGetDownloadObjectTitle=True)
				time.sleep(TIME_SLEEP_SECONDS)
				
				title = self.originalPlaylistTitle
				
				if title is None:
					type = DownloadUrlInfoDic.URL_TYPE_SINGLE_VIDEO
					title = self.originalSingleVideoTitle
				else:
					type = DownloadUrlInfoDic.URL_TYPE_PLAYLIST
			
			if playlistOrSingleVideoModifiedTitle != '':
				title = playlistOrSingleVideoModifiedTitle
			
			self.enableButtons()
			
			uld = UrlDownloadData(type=type,
			                      title=title,
			                      url=playlistOrSingleVideoUrl,
			                      downloadDir=downloadSubdir)
			
			urlListEntry = {'text': title,
			                'data': uld,
			                'toDownload': False,
			                'selectable': True}
			self.requestListRV.data.append(urlListEntry)
			self.resetListViewScrollToEnd()
			self.toggleHistoButton.text = TOGGLE_HISTO_BUTTON_URL
			self.deleteBrowseButton.text = TOGGLE_DELETE_BUTTON_DELETE
			
			if self.showRequestList:
				self.adjustRequestListSize()
			
			self.clearHistoryListSelection()
			self.manageStateOfGlobalRequestListButtons()
			self.emptyRequestFields()
			Clipboard.copy(' ')  # empty clipboard. Copying '' does not work !
	
	def downloadFromClipboard(self, onlyGetDownloadObjectTitle=False):
		"""
		Method called at application start or when pressing the
		Download button or when clicking the Add button. In this last
		call type, the passed onlyGetDownloadObjectTitle is True since
		only obtaining the playlist title related to the url stored in
		the clipboard is required.
		"""
		playlistOrSingleVideoUrl = Clipboard.paste()
		
		if 'HTTP' not in playlistOrSingleVideoUrl.upper():
			return
		
		self.disableButtons()
		
		if onlyGetDownloadObjectTitle:
			# the case if method called after clicking on Add button.
			# In this case, playlist download is not performed, only
			# adding the playlist to the URL list is done.
			endFunc = None
		else:
			endFunc = self.executeDownload
		
		# obtaining the playlist or single video title using a separate thread
		# for the playlist or single video referenced by the url obtained from
		# the clipboard.
		
		if not self.downloadObjectTitleThreadCreated:
			sepThreadExec = SepThreadExec(callerGUI=self,
			                              func=self.getDownloadObjectTitleOnNewThread,
			                              funcArgs={'playlistOrSingleVideoUrl': playlistOrSingleVideoUrl},
			                              endFunc=endFunc,
			                              endFuncArgs=(playlistOrSingleVideoUrl,))
			
			self.downloadObjectTitleThreadCreated = True
			
			sepThreadExec.start()
	
	def downloadFromUrlDownloadLstOnNewThread(self):
		"""
		Called by downloadSelectedItems() method which is called by
		the downloadSelectedUrlItems() method which is executed when the
		downloadALL button is pressed.

		:return:
		"""
		for listEntry in self.downloadUrlLst:
			urlDownloadData = listEntry['data']
			playlistOrSingleVideoUrl = urlDownloadData.url
			playlistOrSingleVideoDownloadDir = urlDownloadData.downloadDir
			
			if urlDownloadData.type == DownloadUrlInfoDic.URL_TYPE_PLAYLIST:
				self.originalPlaylistTitle = urlDownloadData.title
				self.originalSingleVideoTitle = None
			else:
				self.originalPlaylistTitle = None
				self.originalSingleVideoTitle = urlDownloadData.title
			
			if self.accessError:
				# the case if the video or playlist referenced by the playlistOrSingleVideoUrl
				# no longer exist on Youtube
				self.totalDownloadVideoFailedNb += 1
				continue
			
			# correcting a bug if you first downloaded a playlist after
			# modifying the playlist name and then download a playlist
			# without setting the dir ar modifying the playlist name
			self.modifiedPlaylistTitle = urlDownloadData.title
			
			# if answer is yes, the playlist dir will be created as sub dir
			# off the audio dir or the single video will be downloaded in the
			# default single video dir as defined in the audiodownloader.ini
			# file.
			audioRootPath = self.getRootAudiobookPath()
			if playlistOrSingleVideoDownloadDir == '':
				# the case if adding the new URL to the URL's list was done by
				# clicking on the 'Add' button
				self.playlistOrSingleVideoDownloadPath = audioRootPath
			else:
				# the case if adding the new URL to the URL's list was done by
				# accepting the prefix/suffix added to the downloaded playlist
				# videos after setting a download playlist or single video dir
				if audioRootPath in playlistOrSingleVideoDownloadDir:
					self.playlistOrSingleVideoDownloadPath = playlistOrSingleVideoDownloadDir
				else:
					self.playlistOrSingleVideoDownloadPath = audioRootPath + sep + playlistOrSingleVideoDownloadDir
			
			self.downloadPlaylistOrSingleVideoAudioFromUrlLst(playlistOrSingleVideoUrl)
			
			while self.downloadThreadCreated:
				time.sleep(TIME_SLEEP_SECONDS)
		
		self.downloadFromUrlDownloadLstThreadCreated = False    # used to fix a problem on Android
																# where two download threads are
																# created after clicking on 'Yes'
																# button on the ConfirmPopup dialog
		self.displayUrlDownloadLstEndDownloadInfo()
		
		if len(self.partiallyDownloadedPlaylistDic) > 0:
			endDownloadInfoStr = '\n[b][color=0000FF]FAILED PLAYLISTS LIST {}[/color][/b]\n'.format(
				self.partiallyDownloadedPlaylistDic)
		else:
			endDownloadInfoStr = '\n[b][color=0000FF]FAILED PLAYLISTS LIST EMPTY[/color][/b]\n'

		outputLabelLineLst = self.outputLabel.text.split('\n')
		self.addToOutputLabelStr(endDownloadInfoStr, outputLabelLineLst)

		if not self.downloadThreadCreated and len(self.partiallyDownloadedPlaylistDic) > 0:
			for item in self.requestListRV.data:
				itemData = item['data']
				if itemData.title in self.partiallyDownloadedPlaylistDic:
					item['toDownload'] = True
					# since the partiallyDownloadedPlaylistDic will be updated
					# again in case the next call to downloadSelectedUrlItems()
					# causes the re-addition of the removed playlist, the
					# playlist must be suppressed here.
					# self.partiallyDownloadedPlaylistDic.pop(itemData.title)
					
					# in fact, the next instruction is be better since it
					# improves the case where more than one video in the
					# playlist were partially downloaded.
					self.decreasePlaylistVideoDownloadNumber()
				else:
					item['toDownload'] = False
					
			# calling the method linked to the Download All button
			self.downloadSelectedUrlItems()
	
	def downloadFromFailedVideoListOnNewThread(self):
		"""
		Called by downloadPlaylistFailedVideos() method which is called by
		the handleFailedVideosDownloading itself called when choosing the
		'Down failed vids' dropdown menu item

		:return:
		"""
		for failedVideoPlaylistInfo in self.failedVideoPlaylistInfoLst:
			failedVideoPlaylistDic = failedVideoPlaylistInfo.playlistInfoDic
			
			# ensuring that the playlist dirs where the failed videos will be downloaded
			# does not contain video older than the playlist dic containing failed video
			# references. The playlist dic were obtained from the smartphone using the
			# transfer file utility program.
			self.audioController.deleteAudioFilesOlderThanPlaylistDicFile(failedVideoPlaylistDic)
			
			self.failedVideoPlaylistDic = failedVideoPlaylistDic
			playListDownloadSubDir = failedVideoPlaylistDic.getPlaylistDownloadSubDir()
			failedVideoIndexLst = failedVideoPlaylistInfo.videoIndexLst
			message = "downloading {} failed video(s) of playlist [b]{}[/b] in playlist dir [b]{}[/b] ...\n".format(
				len(failedVideoIndexLst),
				failedVideoPlaylistDic.getPlaylistNameModified(),
				playListDownloadSubDir)
			self.displayFailedVideoPlaylistDownloadStartMessage(message)
			
			self.playlistOrSingleVideoDownloadPath = self.configMgr.dataPath + sep + playListDownloadSubDir
			for failedVideoIndex in failedVideoIndexLst:
				playlistOrSingleVideoUrl = failedVideoPlaylistDic.getVideoUrlForVideoIndex(failedVideoIndex)
				self.failedVideoPlaylistDic = failedVideoPlaylistDic  # must be set here and not in first for loop !
				#                                                       since it is set to None after the dic is saved
				#                                                       in downloadPlaylistOrSingleVideoAudioFromUrlLstOnNewThread()
				self.originalPlaylistTitle = None
				self.originalSingleVideoTitle = failedVideoPlaylistDic.getVideoTitleForVideoIndex(failedVideoIndex)
				
				if self.accessError:
					# the case if the video or playlist referenced by the playlistOrSingleVideoUrl
					# no longer exist on Youtube
					self.totalDownloadVideoFailedNb += 1
					continue
				
				self.downloadPlaylistOrSingleVideoAudioFromUrlLst(playlistOrSingleVideoUrl, failedVideoIndex)
				
				while self.downloadThreadCreated:
					time.sleep(TIME_SLEEP_SECONDS)
		
		self.downloadFromUrlDownloadLstThreadCreated = False    # used to fix a problem on Android
																# where two download threads are
																# created after clicking on 'Yes'
																# button on the ConfirmPopup dialog
		self.displayFailedVideoRedownloadLstEndDownloadInfo()
	
	def executeDownload(self, playlistOrSingleVideoUrl):
		self.enableButtons()
		
		if self.accessError is None:
			# self.accessError is not None if the playlistOrSingleVideoUrl is neither pointing to
			# a playlist nor to a single video. In this case, an error message was displayed in
			# the UI !
			
			if self.originalSingleVideoTitle is None:
				# url obtained from clipboard points to a playlist
				downloadObjectTitle = self.originalPlaylistTitle
				confirmPopupTitle = ConfirmDownloadPopup.POPUP_TITLE_PLAYLIST + ConfirmDownloadPopup.POPUP_TITLE_DOWNLOAD_DATE_UPLOAD_DATE
				isPlayListDownloaded = True
			else:
				# url obtained from clipboard points to a single video
				downloadObjectTitle = self.originalSingleVideoTitle
				confirmPopupTitle = ConfirmDownloadPopup.POPUP_TITLE_VIDEO
				isPlayListDownloaded = False
			
			confirmDownloadPopupCallbackFunction = self.onConfirmDownloadPopupAnswer
			
			popup = self.createDownloadConfirmPopup(confirmPopupTitle=confirmPopupTitle,
			                                        confirmPopupMsg=downloadObjectTitle,
			                                        confirmPopupCallbackFunction=confirmDownloadPopupCallbackFunction,
			                                        isPlayListDownloaded=isPlayListDownloaded,
			                                        playlistOrSingleVideoUrl=playlistOrSingleVideoUrl)
			
			popup.open()
	
	def getDownloadObjectTitleOnNewThread(self, playlistOrSingleVideoUrl):
		self.originalPlaylistTitle, self.originalSingleVideoTitle, self.accessError = \
			self.audioController.getPlaylistTitleOrVideoTitleForUrl(
				playlistOrSingleVideoUrl)
		
		self.downloadObjectTitleThreadCreated = False
	
	def enableButtons(self):
		self.downloadButton.disabled = False
		self.addDownloadButton.disabled = False
		self.clearResultOutputButton.disabled = False
	
	def disableButtons(self):
		self.downloadButton.disabled = True
		self.addDownloadButton.disabled = True
		self.stopDownloadButton.disabled = True
		self.clearResultOutputButton.disabled = True
	
	def onConfirmDownloadPopupAnswer(self, confirmPopupInstance, answer):
		"""
		Method called when one of the ConfirmPopup button is pushed. This method is
		linked to the ConfirmDownloadPopup 'on_answer' event in the
		createDownloadConfirmPopup() method called by executeDownload() method
		which is called if the clipboard contains a playlist or single video
		URL at the application start.
		
		:param confirmPopupInstance:
		:param answer:
		:return:
		"""
		self.isUploadDateAddedToPlaylistVideo = confirmPopupInstance.isUploadDateAdded()
		self.isIndexAddedToPlaylistVideo = confirmPopupInstance.isIndexAdded()
		playlistOrSingleVideoUrl = confirmPopupInstance.playlistOrSingleVideoUrl
		popup = confirmPopupInstance.parent.parent.parent
		
		if answer == 'yes':  # 'yes' is set in confirmpopup.kv file
			
			# correcting a bug if you first downloaded a playlist after
			# modifying the playlist name and then download a playlist
			# without setting the dir ar modifying the playlist name
			self.modifiedPlaylistTitle = None
			
			# if answer is yes, the playlist dir will be created as sub dir
			# off the audio dir or the single video will be downloaded in the
			# default single video dir as defined in the audiodownloader.ini
			# file.
			self.playlistOrSingleVideoDownloadPath = self.getRootAudiobookPath()
			self.downloadPlaylistOrSingleVideoAudio(playlistOrSingleVideoUrl)
		elif answer == 'setFolder':  # 'setFolder' is set in confirmdownloadpopup.kv file
			self.openSelectOrCreateDirPopup(playlistOrSingleVideoUrl)
		
		popup.dismiss()
	
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
	
	def stopDownload(self):
		"""
		Method called when clicking on the stop download button. Setting the
		AudioController stopDownloading instance variable to True will cause
		YoutubeDlAudioDownloader.downloadVideosReferencedInPlaylistForPlaylistUrl()
		to stop downloading the videos referenced in the currently downloading
		playlist.
		"""
		self.stopDownloadButton.disabled = True
		msgText = '[b]{}[/b] playlist audio(s) download stopping ....\n'.format(
			self.originalPlaylistTitle)
		self.updateStatusBar(msgText)
		self.audioController.stopDownloading = True
	
	def downloadStopped(self):
		self.stopDownloadButton.disabled = False
		self.clearStatusBar()
	
	def toggleAppPosAndSize(self):
		"""
		No longer used, but ...
		"""
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
			self.stopDownloadButton.text = 'Full'
		else:
			self.size_hint_y = 1
			self.pos_hint = {'x': 0, 'y': 0}
			self.stopDownloadButton.text = 'Half'
	
	def applyDeleteOrBrowseItem(self):
		selItemData = self.requestListRV.data[self.recycleViewCurrentSelIndex]['data']
		
		if isinstance(selItemData, DownloadHistoryData):
			# Download histo files are displayed
			playlistName = selItemData.playlistName
			downloadVideoInfoDic = self.audioController.getDownloadPlaylistInfoDic(playlistName=playlistName)
			
			if downloadVideoInfoDic is None:
				# currently the case if we try to open a browser on an audio file
				# located in the audio\Various dir in which no video info dic
				# exist
				self.updateStatusBar(
					'Not possible to open browser since {} playlist dic not exist'.format(playlistName))
				return
			
			if selItemData.type == DHD_TYPE_AUDIO_FILE:
				fullDownloadedFileName = selItemData.audioFileName
				url = downloadVideoInfoDic.getVideoUrlForVideoFileName(fullDownloadedFileName)
				if url is None:
					# possibly due ti the fact that the file download encountered
					# a problem which caused the file renaming with prefix/suffix
					# to be skipped.
					url = downloadVideoInfoDic.getVideoUrlForVideoTitle(fullDownloadedFileName.replace('.mp3', ''))
			else:
				url = downloadVideoInfoDic.getPlaylistUrl()
			
			if url is None:
				# the case if the file is not in the playlist dic
				self.updateStatusBar(
					'Not possible to open browser since the audio file is not in {} playlist dic'.format(playlistName))
				return
			
			webbrowser.open(url, new=1)
			self.clearStatusBar()
		
		elif isinstance(selItemData, UrlDownloadData):
			# URL are displayed
			self.requestListRV.data.pop(self.recycleViewCurrentSelIndex)
	
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
			
			fullRequestStrWithSaveModeOptionsListEntry = {'text': fullRequestStrWithSaveModeOptionsForHistoryList,
			                                              'selectable': True}
			
			# used to avoid replacing btc usd 20/12/20 all -vs100usd by btc usd 20/12/20 00:00 all -vs100usd !
			fullRequestStrWithSaveModeOptionsListEntryNoZeroTime = {
				'text': fullRequestStrWithSaveModeOptionsForHistoryList.replace(' 00:00', ''), 'selectable': True}
			
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
		
		self.downloadAllButton.disabled = False
		self.clearResultOutputButton.disabled = False
		
		# self.resultOutput.do_cursor_movement('cursor_pgdown')
		self.refocusOnFirstRequestInput()
	
	def clearOutput(self):
		self.outputLabel.text = ''
		
		# scrolling to top of output text. Doing that avoids that the next
		# output label text addition is done at the bottom of the label
		self.outputScrollView.scroll_y = 1
		
		self.clearStatusBar()
		
		self.clearResultOutputButton.disabled = True
		self.refocusOnFirstRequestInput()
		
		if self.toggleHistoButton.text == TOGGLE_HISTO_BUTTON_DOWN_HIST:
			# means the list contains downloaded audio files history. In this
			# case, the history list must be refilled with Url's data contained
			# in urlListDic_dic.txt
			self.toggleHistoButton.text = TOGGLE_HISTO_BUTTON_URL
			self.deleteBrowseButton.text = TOGGLE_DELETE_BUTTON_DELETE
			self.downloadAllButton.text = TOGGLE_DOWNLOAD_ALL_BUTTON_DOWN_ALL
			self.loadHistoryDataIfSet()  # reload urlListDic_dic.txt
	
	def clearStatusBar(self):
		'''
		Clear the status bar, except if it displays either the playlist	URL
		at app start loaded file or the currently downloading video.
		'''
		if 'URL' not in self.statusBarTextInput.text and 'downloading' not in self.statusBarTextInput.text:
			self.updateStatusBar('')
	
	def emptyRequestFields(self):
		self.requestInput.text = ''
	
	def clearHistoryListSelection(self):
		self.requestListRV._get_layout_manager().clear_selection()
	
	def replaceRequest(self, *args):
		# Remove the selected item
		removedItem = self.requestListRV.data.pop(self.recycleViewCurrentSelIndex)
		replaceUrlDownloadData = removedItem['data']
		replaceItemToDownloadValue = removedItem['toDownload']
		replaceUrlType = replaceUrlDownloadData.type
		replaceUrl = replaceUrlDownloadData.url
		
		# Get the request from the TextInputs
		requestStr = self.requestInput.text
		replaceUrlDownloadData.title = requestStr
		
		dataDic = {'text': requestStr, 'data': replaceUrlDownloadData, 'toDownload': replaceItemToDownloadValue,
		           'selectable': True}
		
		# Add the updated data to the list if not already in
		requestListEntry = dataDic
		
		if not requestListEntry in self.requestListRV.data:
			self.requestListRV.data.insert(self.recycleViewCurrentSelIndex, requestListEntry)
		
		self.refocusOnFirstRequestInput()
	
	def downloadSelectedUrlItems(self):
		"""
		Method linked to the Download All Or Delete ALL button in kv file.
		"""
		if self.toggleHistoButton.text == TOGGLE_HISTO_BUTTON_URL:
			# here, we are in the state where the list displays URL's.
			# The button's text is 'Down All'. Clicking on it does download
			# the selected URL's, playlist URL's for the most part.
			self.downloadSelectedItems()
		else:
			# here, we are in the state where the list displays the downloaded
			# playlists or single videos. The button's text is 'Del All'.
			# Clicking on it does delete the selected playlistsor single
			# videos.
			self.deleteSelectedAudioDownloadedFiles()
	
	def downloadSelectedItems(self):
		"""
		Method called by method downloadSelectedUrlItems itself called when
		the Download All button in kv file was pressed.
		"""
		self.totalDownloadVideoSuccessNb = 0
		self.totalDownloadVideoFailedNb = 0
		self.totalDownloadVideoSkippedNb = 0
		
		self.downloadUrlLst = [x for x in self.requestListRV.data if x['toDownload']]
		
		if len(self.downloadUrlLst) > 0:
			# the case if the Add button was pressed in order to add the
			# playlist or single video url contained in the clipboard
			# to the self.playlistOrSingleVideoUrlDownloadLst
			
			# downloading the playlists or single videos contained in
			# the self.downloadFromUrlDownloadLst using a separate thread.
			# So, the download information is displayed on the outputLabel.
			if not self.downloadFromUrlDownloadLstThreadCreated:
				sepThreadExec = SepThreadExec(callerGUI=self,
				                              func=self.downloadFromUrlDownloadLstOnNewThread)
				
				self.downloadFromUrlDownloadLstThreadCreated = True  # used to ensure that only
				#                                                      1 playlist or video is
				#                                                      downloaded at the same
				#                                                      time.
				
				sepThreadExec.start()
	
	def downloadPlaylistFailedVideos(self):
		"""
		Method called by method handleFailedVideosDownloading itself called when
		choosing the 'Down failed vids' dropdown menu item.
		"""
		self.totalDownloadVideoSuccessNb = 0
		self.totalDownloadVideoFailedNb = 0
		self.totalDownloadVideoSkippedNb = 0
		
		self.failedVideoPlaylistInfoLst = DownloadPlaylistInfoDic.getFailedVideoDownloadedOnSmartphonePlaylistInfoLst(
			self.audiobookPath)
		
		if len(self.failedVideoPlaylistInfoLst) > 0:
			# the case if the Add button was pressed in order to add the
			# playlist or single video url contained in the clipboard
			# to the self.playlistOrSingleVideoUrlDownloadLst
			
			# downloading the playlists or single videos contained in
			# the self.downloadFromUrlDownloadLst using a separate thread.
			# So, the download information is displayed on the outputLabel.
			if not self.downloadFromUrlDownloadLstThreadCreated:
				sepThreadExec = SepThreadExec(callerGUI=self,
				                              func=self.downloadFromFailedVideoListOnNewThread)
				
				self.downloadFromUrlDownloadLstThreadCreated = True  # used to ensure that only
				#                                                      1 playlist or video is
				#                                                      downloaded at the same
				#                                                      time.
				
				sepThreadExec.start()
	
	def handleFailedVideosDownloading(self):
		"""
		Method called when choosing the 'Down failed vids' dropdown menu
		item defined in the customdropdown.kv file. This menu iten is available
		on Windows only. This method obtains every video whose downloadException
		value is True in every playlist dic file and then downloads them in order
		to then replace the failed videos on the smartphone by the successfully
		downloaded videos on the pc.
		"""
		self.dropDownMenu.dismiss()
		self.downloadPlaylistFailedVideos()
	
	def renameFailedVideosUpdatedFromPC(self):
		"""
		Method called when choosing the 'Renam rdown vids' dropdown menu
		item defined in the customdropdown.kv file. This method renames the
		failed video audio files re-downloaded on Windows and manually copied
		on the smartphone. The new file name is the old file name with its
		date prefix replaced by the video download date value.
		"""
		self.dropDownMenu.dismiss()
		
		renamedVideoAudioFileDic = DownloadPlaylistInfoDic.renameFailedVideosUpdatedFromPC(
			audioDirRoot=self.audiobookPath)
		self.displayRenamedVideoAudioFiles(renamedVideoAudioFileDic)
	
	def displayRenamedVideoAudioFiles(self, renamedVideoAudioFileDic):
		"""
		Method called after renaming the video re-downloaded on PC is finished.
		"""
		outputLabelLineLst = self.outputLabel.text.split('\n')
		
		endDownloadInfoStr = self.buildEndDownloadInfoStr()
		
		if len(renamedVideoAudioFileDic) > 0:
			endDownloadInfoStr += self.formatRenamedVideoDic(renamedVideoAudioFileDic)
		
		self.addToOutputLabelStr(endDownloadInfoStr, outputLabelLineLst)
	
	def formatRenamedVideoDic(self, renamedVideoAudioFileDic):
		formattedMsgStr = '\n\n[b][color=00FF00]RENAMED REDOWNLOADED VIDEOS[/color][/b]'
		sortedDicTupleLst = sorted(renamedVideoAudioFileDic.items())
		
		for dicTuple in sortedDicTupleLst:
			playlistSubDir = dicTuple[0]
			formattedMsgStr += '\n\n[b][color=00FF00]' + playlistSubDir.replace('/', sep) + '[/color][/b]'
			newAudioFileNameLst = dicTuple[1]
			for newAudioFileName in newAudioFileNameLst:
				formattedMsgStr += '\n    [b]' + newAudioFileName + '[/b]'
		
		return formattedMsgStr
	
	def deleteSelectedAudioDownloadedFiles(self):
		selectedAudioDownloadedFileLst = [x for x in self.requestListRV.data if x['toDownload']]
		delFileDic = {}
		
		for listEntry in selectedAudioDownloadedFileLst:
			downloadHistoryData = listEntry['data']
			if downloadHistoryData.type == DHD_TYPE_AUDIO_FILE:
				playlistName = downloadHistoryData.playlistName
				audioFileName = downloadHistoryData.audioFileName
				
				if playlistName in delFileDic.keys():
					delFileDic[playlistName].append(audioFileName)
				else:
					delFileDic[playlistName] = [audioFileName]
			else:
				# list item is a playlist, not a downloaded file
				continue
		
		deletedFileNameLst = self.audioController.deleteAudioFilesFromDirOnly(delFileDic)
		
		# removing deleted files from the download histo list
		remainingAudioDownloadedFileLst = [x for x in self.requestListRV.data if
		                                   x['data'].type == DHD_TYPE_PLAYLIST or x[
			                                   'data'].audioFileName not in deletedFileNameLst]
		self.requestListRV.data = remainingAudioDownloadedFileLst
	
	def executeOnlineRequestOnNewThread(self, asyncOnlineRequestFunction, kwargs):
		"""
		This generic method first disable the buttons whose usage could disturb
		the passed asyncFunction. It then executes the asyncFunction on a new thread.
		When the asyncFunction is finished, it re-enables the disabled buttons.
		
		:param asyncOnlineRequestFunction:
		:param kwargs: keyword args dic for the asyncOnlineRequestFunction
		"""
		self.downloadAllButton.disabled = True
		self.clearResultOutputButton.disabled = True
		
		sepThreadExec = SepThreadExec(callerGUI=self,
		                              func=asyncOnlineRequestFunction)
		
		sepThreadExec.start()
	
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
		
		self.downloadAllButton.disabled = False
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
		self.fileChooserPopup.dismiss()
	
	def openFileLoadPopup(self):
		self.dropDownMenu.dismiss()
		popupTitle = self.buildFileChooserPopupTitle(FILE_ACTION_LOAD)
		self.fileChooserPopup = LoadFileChooserPopup(title=popupTitle,
		                                             rootGUI=self,
		                                             load=self.load,
		                                             cancel=self.dismissPopup)
		self.fileChooserPopup.open()
	
	def openFileSavePopup(self):
		self.dropDownMenu.dismiss()
		popupTitle = self.buildFileChooserPopupTitle(FILE_ACTION_SAVE)
		self.fileChooserPopup = SaveFileChooserPopup(title=popupTitle,
		                                             rootGUI=self,
		                                             cancel=self.dismissPopup)
		loadAtStartFilePathName = self.configMgr.loadAtStartPathFilename
		self.fileChooserPopup.setCurrentLoadAtStartFile(loadAtStartFilePathName)
		self.fileChooserPopup.open()
	
	def openFileDeletePopup(self):
		self.dropDownMenu.dismiss()
		popupTitle = self.buildFileChooserPopupTitle(FILE_ACTION_DELETE)
		self.fileChooserPopup = DeleteFileChooserPopup(title=popupTitle,
		                                               rootGUI=self,
		                                               cancel=self.dismissPopup)
		self.fileChooserPopup.open()
	
	def openSelectOrCreateDirPopup(self, playlistOrSingleVideoUrl):
		self.dropDownMenu.dismiss()
		popupTitle = self.buildFileChooserPopupTitle(FILE_ACTION_SELECT_OR_CREATE_DIR, self.originalSingleVideoTitle)
		
		self.fileChooserPopup = SelectOrCreateDirFileChooserPopup(title=popupTitle,
		                                                          rootGUI=self,
		                                                          playlistOrSingleVideoUrl=playlistOrSingleVideoUrl,
		                                                          originalPlaylistTitle=self.originalPlaylistTitle,
		                                                          originalSingleVideoTitle=self.originalSingleVideoTitle,
		                                                          load=self.load,
		                                                          cancel=self.dismissPopup)
		self.fileChooserPopup.open()
	
	def openFileToClipLoadPopup(self):
		self.dropDownMenu.dismiss()
		popupTitle = self.buildFileChooserPopupTitle(FILE_ACTION_SELECT_FILE_TO_SPLIT)
		self.fileChooserPopup = FileToClipLoadFileChooserPopup(title=popupTitle,
		                                                       rootGUI=self,
		                                                       load=self.load,
		                                                       cancel=self.dismissPopup)
		self.fileChooserPopup.open()
	
	def openShareAudioPopup(self):
		self.dropDownMenu.dismiss()
		popupTitle = self.buildFileChooserPopupTitle(FILE_ACTION_SELECT_FILE_TO_SHARE)
		self.fileChooserPopup = FileToShareLoadFileChooserPopup(title=popupTitle,
		                                                        rootGUI=self,
		                                                        load=self.load,
		                                                        cancel=self.dismissPopup)
		self.fileChooserPopup.open()
	
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
		elif fileAction == FILE_ACTION_DELETE:
			return SaveFileChooserPopup.SELECT_FILE_TO_DELETE
		else:
			# fileAction == FILE_ACTION_SELECT_FILE_TO_SHARE
			return SaveFileChooserPopup.SELECT_FILE_TO_SHARE
		
		loadAtStartFilePathName, isLoadAtStart = self.getLoadAtStartFilePathName()
		
		if loadAtStartFilePathName == self.currentLoadedPathFileName:
			loadAtStartFileName = loadAtStartFilePathName.split(sep)[-1]
			if isLoadAtStart:
				popupTitle = "{} ({} loaded at start)".format(popupTitleAction, loadAtStartFileName)
			else:
				popupTitle = "{} (no file loaded)".format(popupTitleAction)
		else:
			loadFileName = self.currentLoadedPathFileName.split(sep)[-1]
			popupTitle = "{} ({} loaded)".format(popupTitleAction, loadFileName)
		
		return popupTitle
	
	def getLoadAtStartFilePathName(self):
		"""
		Returns the load at start URL list dictionary file path name as
		well as the isLoadAtStart boolean value.
		
		:return: loadAtStartFilePathName, isLoadAtStart
		"""
		loadAtStartFilePathName = self.configMgr.loadAtStartPathFilename
		isLoadAtStart = False
		
		if loadAtStartFilePathName == self.currentLoadedPathFileName:
			loadAtStartFileName = loadAtStartFilePathName.split(sep)[-1]
			if loadAtStartFileName != '':
				isLoadAtStart = True
		
		return loadAtStartFilePathName, isLoadAtStart
	
	def load(self, path, filename):
		if not filename:
			# no file selected. Load dialog remains open ..
			return
		
		currentLoadedPathFileName = os.path.join(path, filename[0])
		self.loadHistoryFromPathFilename(currentLoadedPathFileName)
		self.dismissPopup()
		self.displayFileActionOnStatusBar(currentLoadedPathFileName, FILE_ACTION_LOAD)
	
	def displayFileActionOnStatusBar(self, pathFileName, actionType, isLoadAtStart=None):
		if actionType == FILE_ACTION_LOAD:
			self.updateStatusBar("URL's file loaded:\n{}".format(pathFileName))
		else:
			if isLoadAtStart:
				self.updateStatusBar("URL's saved to file: {}.\nLoad at start activated.".format(pathFileName))
			else:
				self.updateStatusBar("URL's saved to file: {}".format(pathFileName))
	
	def loadHistoryFromPathFilename(self, pathFileName):
		self.currentLoadedPathFileName = pathFileName
		dataFileNotFoundMessage = self.buildFileNotFoundMessage(pathFileName)
		
		if not self.ensureDataPathFileNameExist(pathFileName, dataFileNotFoundMessage):
			return
		
		self.downloadUrlInfoDic = DownloadUrlInfoDic(existingDicFilePathName=pathFileName)
		
		udlLst = self.downloadUrlInfoDic.getAllUrlDownloadDataSortedList()
		histoLines = [{'text': udl.title, 'data': udl, 'toDownload': False, 'selectable': True} for udl in udlLst]
		
		self.requestListRV.data = histoLines
		self.requestListRVSelBoxLayout.clear_selection()
		
		# Reset the ListView
		self.resetListViewScrollToEnd()
		
		self.manageStateOfGlobalRequestListButtons()
		self.refocusOnFirstRequestInput()
	
	def saveUrlListToDownloadUrlInfoDicFile(self, savingPathFileName, isLoadAtStart):
		"""
		Method called in two cases:
			1/ Save menu selected
			2/ Yes button on yesNoPopup dialog displayed to obtain user
			   confirmation on adding download date prefix or/and upload date
			   suffix to the to download playlist videos.
			   
		:param savingPathFileName: path + file name specified by the user in the
			   path file name TextInput save dialog field
		:param isLoadAtStart: value of the load at start CheckBox
		"""
		asciiOnlyPathFileName = savingPathFileName.encode("ascii", "ignore").decode()
		
		if asciiOnlyPathFileName != savingPathFileName:
			message = self.buildNonAsciiFilePathNameMessage(savingPathFileName)
			self.displayPopupWarning(message)
			return
		
		self.currentLoadedPathFileName = savingPathFileName
		pathContainedInFilePathName = DirUtil.extractPathFromPathFileName(savingPathFileName)
		savingPathNotExistMessage = self.buildDataPathContainedInFilePathNameNotExistMessage(
			pathContainedInFilePathName)
		
		if not self.ensureDataPathExist(pathContainedInFilePathName, savingPathNotExistMessage):
			# data path defined specified in saved file path name does not exist. Error popup is displayed.
			return
		
		updatedDownloadUrlInfoDic = DownloadUrlInfoDic(
			audioRootDir=None,
			urlListDicFileName=self.downloadUrlInfoDic.getUrlListDicFileName(),
			loadDicIfDicFileExist=False)
		
		for listEntry in self.requestListRV.data:
			urlDownloadData = listEntry['data']
			updatedDownloadUrlInfoDic.addUrlDownloadData(urlDownloadData)
		
		updatedDownloadUrlInfoDic.saveDic(audioDirRoot=self.configMgr.dataPath,
		                                  dicFilePathName=savingPathFileName)
		
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
	
	def deleteAudioFilesFromDirAndFromDic(self, filePathNameLst):
		"""
		Called by DeleteFileChooserPopup.delete().
		
		Delete the files listed in the passed filePathNameLst and remove
		their corresponding entry in the relevant playlist dic file.
		
		:param filePathNameLst:
		"""
		self.audioController.deleteAudioFilesFromDirAndFromDic(filePathNameLst=filePathNameLst)
	
	# --- end file chooser code ---
	
	def buildDataPathContainedInFilePathNameNotExistMessage(self, path):
		return 'Path ' + path + ' does not exist ! Either create the directory or modify the path.'
	
	def buildNonAsciiFilePathNameMessage(self, savingPathFileName):
		return 'Save path file name {}\ncontains non ascii characters. File not saved !'.format(savingPathFileName)
	
	def isLoadAtStart(self, filePathName):
		return self.configMgr.loadAtStartPathFilename == filePathName
	
	def downloadPlaylistOrSingleVideoAudio(self, playlistOrSingleVideoUrl):
		"""
		This method launch downloading audios for the videos referenced in the playlist
		URL or the audio of the single video if the URL points to a video, this in a
		new thread.
		"""
		# downloading the playlist or single video using a separate thread
		# So, the download information is displayed on the outputLabel.
		if not self.downloadThreadCreated:
			sepThreadExec = SepThreadExec(callerGUI=self,
			                              func=self.downloadPlaylistOrSingleVideoAudioOnNewThread,
			                              funcArgs={'playlistOrSingleVideoUrl': playlistOrSingleVideoUrl})
			
			self.downloadThreadCreated = True  # used to fix a problem on Android
			# where two download threads are
			# created after clicking on 'Yes'
			# button on the ConfirmPopup dialog
			
			sepThreadExec.start()
	
	def downloadPlaylistOrSingleVideoAudioFromUrlLst(self,
	                                                 playlistOrSingleVideoUrl,
	                                                 failedVideoIndex=None):
		"""
		This method launch downloading audios for the videos referenced in the playlist
		URL or the audio of the single video if the URL points to a video, this in a
		new thread. It is called in two situations:
		
		1/ downloading selected playlist or single video URL in the URL's list
		   (downloadFromUrlDownloadLstOnNewThread() method),
		2/ downloading the failed videos on Windows
		   (downloadFromFailedVideoListOnNewThread() method).
		"""
		# downloading the playlists or single videos contained in
		# the self.downloadFromUrlDownloadLst using a separate thread.
		# So, the download informations are displayed on the outputLabel.
		if not self.downloadThreadCreated:
			sepThreadExec = SepThreadExec(callerGUI=self,
			                              func=self.downloadPlaylistOrSingleVideoAudioFromUrlLstOnNewThread,
			                              funcArgs={'playlistOrSingleVideoUrl': playlistOrSingleVideoUrl,
			                                        'failedVideoIndex': failedVideoIndex})
			
			self.downloadThreadCreated = True  # used to fix a problem on Android
			# where two download threads are
			# created after clicking on 'Yes'
			# button on the ConfirmPopup dialog
			
			sepThreadExec.start()
	
	def downloadPlaylistOrSingleVideoAudioOnNewThread(self, playlistOrSingleVideoUrl):
		"""
		This method executed on a separated thread downloads audios for
		the videos referenced in a playlist or downloads the audio of a
		single video.
		"""
		self.isFirstCurrentDownloadInfo = True
		
		if self.originalPlaylistTitle is not None:
			# if a playlist is downloading, the stop download button is
			# activated
			self.stopDownloadButton.disabled = False
			
			downloadAndUploadDateSettingWarningMsg = self.getVideoTitlePrefixSuffixWarningMsg(
				playlistOrSingleVideoUrl, self.playlistOrSingleVideoDownloadPath)
			
			if downloadAndUploadDateSettingWarningMsg != '':
				self.downloadThreadCreated = False
				
				# obtaining prefix suffix setting user confirmation
				popup = self.createYesNoPopup(YesNoPopup.POPUP_TITLE_PLAYLIST,
				                              downloadAndUploadDateSettingWarningMsg,
				                              self.onPrefixSuffixFileNameConfirmYesNoPopupAnswer,
				                              True)
				popup.open()
			else:
				self.audioController.downloadVideosReferencedInPlaylist(downloadVideoInfoDic=self.downloadVideoInfoDic,
				                                                        isIndexAddedToPlaylistVideo=self.isIndexAddedToPlaylistVideo,
				                                                        isUploadDateAddedToPlaylistVideo=self.isUploadDateAddedToPlaylistVideo)
				
				self.downloadThreadCreated = False  # used to fix a problem on Android
				# where two download threads are
				# created after clicking on 'Yes'
				# button on the ConfirmPopup dialog
				
				self.stopDownloadButton.disabled = True
		else:
			# if a single video is downloading, the stop download button is
			# disabled since interrupting a single video download is not
			# possible
			self.stopDownloadButton.disabled = True
			
			self.audioController.downloadSingleVideo(
				singleVideoUrl=playlistOrSingleVideoUrl,
				singleVideoDownloadPath=self.playlistOrSingleVideoDownloadPath,
				originalSingleVideoTitle=self.originalSingleVideoTitle,
				modifiedVideoTitle=self.modifiedSingleVideoTitle)
			
			self.downloadThreadCreated = False  # used to fix a problem on Android
			# where two download threads are
			# created after clicking on 'Yes'
			# button on the ConfirmPopup dialog
			
			self.stopDownloadButton.disabled = True
	
	def getVideoTitlePrefixSuffixWarningMsg(self, playlistOrSingleVideoUrl, playlistOrSingleVideoDownloadPath):
		if self.originalPlaylistTitle is not None:
			self.downloadVideoInfoDic, indexAndDateSettingWarningMsg = self.audioController.getDownloadVideoInfoDicAndIndexDateSettingWarningMsg(
				playlistOrSingleVideoUrl=playlistOrSingleVideoUrl,
				playlistOrSingleVideoDownloadPath=playlistOrSingleVideoDownloadPath,
				originalPlaylistTitle=self.originalPlaylistTitle,
				modifiedPlaylistTitle=self.modifiedPlaylistTitle,
				isIndexAddedToPlaylistVideo=self.isIndexAddedToPlaylistVideo,
				isUploadDateAddedToPlaylistVideo=self.isUploadDateAddedToPlaylistVideo)
			return indexAndDateSettingWarningMsg
		else:
			# the case when the url points to a single video, not to a playlist ...
			return ''
	
	def downloadPlaylistOrSingleVideoAudioFromUrlLstOnNewThread(self,
	                                                            playlistOrSingleVideoUrl,
	                                                            failedVideoIndex=None):
		"""
		This method is executed on a separated thread launch downloading audios for
		the videos referenced in a playlist or the audio of a single video. The
		method is indirectly executed if the clipboard contains a playlist URL or
		a single video URL at application start.
		"""
		self.isFirstCurrentDownloadInfo = True
		
		if self.originalPlaylistTitle is not None:
			# if a playlist is downloading, the stop download button is
			# activated
			self.stopDownloadButton.disabled = False
			
			downloadVideoInfoDic = \
				self.audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl=playlistOrSingleVideoUrl,
				                                                             playlistOrSingleVideoDownloadPath=self.playlistOrSingleVideoDownloadPath,
				                                                             originalPlaylistTitle=self.originalPlaylistTitle,
				                                                             modifiedPlaylistTitle=self.modifiedPlaylistTitle)
			
			indexAndDateUsageLst = self.audioController.getIndexAndDateUsageLstForPlaylist(downloadVideoInfoDic)
			
			if indexAndDateUsageLst is None or \
					indexAndDateUsageLst == []:
				# the case if the playlist download dir does not exist or is empty.
				# In this situation, we choose to add the index prefix and the
				# video upload date suffix to the downloaded audio files.
				#
				# This means that in case of downloading an audiobook playlist,
				# you MUST first download at least one chapter without adding
				# any prefix or suffix before adding the playlist url to the url
				# list !
				#
				# A better solution would be in this situation to try to determine
				# if the new playlist is an audiobook playlist with video titles
				# starting by the same string portion. But this takes time ...
				isIndexAddedToAlreadyDownloadedPlaylistVideo = True
				isUploadDateAddedAlreadyDownloadedToPlaylistVideo = True
			else:
				isIndexAddedToAlreadyDownloadedPlaylistVideo = indexAndDateUsageLst[
					                                               DirUtil.DOWNLOAD_DATE_UPLOAD_DATE_POS] or \
				                                               indexAndDateUsageLst[
					                                               DirUtil.DOWNLOAD_DATE_NO_UPLOAD_DATE_POS]
				isUploadDateAddedAlreadyDownloadedToPlaylistVideo = indexAndDateUsageLst[
					                                                    DirUtil.DOWNLOAD_DATE_UPLOAD_DATE_POS] or \
				                                                    indexAndDateUsageLst[
					                                                    DirUtil.NO_DOWNLOAD_DATE_UPLOAD_DATE_POS]
			
			self.audioController.downloadVideosReferencedInPlaylist(originalPlaylistTitle=self.originalPlaylistTitle,
			                                                        downloadVideoInfoDic=downloadVideoInfoDic,
			                                                        isIndexAddedToPlaylistVideo=isIndexAddedToAlreadyDownloadedPlaylistVideo,
			                                                        isUploadDateAddedToPlaylistVideo=isUploadDateAddedAlreadyDownloadedToPlaylistVideo)
			
			self.downloadThreadCreated = False  # used to fix a problem on Android
			# where two download threads are
			# created after clicking on 'Yes'
			# button on the ConfirmPopup dialog
			
			self.stopDownloadButton.disabled = True
		else:
			# if a single video is downloading, the stop download button is
			# disabled since interrupting a single video download is not
			# possible
			self.stopDownloadButton.disabled = True
			failedVideoFileName = None
			if self.failedVideoPlaylistDic:
				# not None when re-downloading a failed video on pc
				failedVideoFileName = self.failedVideoPlaylistDic.getVideoAudioFileNameForVideoTitle(
					self.originalSingleVideoTitle)
			try:
				originalYdlDownloadedAudioFileName, purgedOriginalOrModifiedVideoTitleWithPrefixSuffixDatesMp3, isVideoDownloadSuccessful = self.audioController.downloadSingleVideo(
					singleVideoUrl=playlistOrSingleVideoUrl,
					singleVideoDownloadPath=self.playlistOrSingleVideoDownloadPath,
					originalSingleVideoTitle=self.originalSingleVideoTitle,
					modifiedVideoTitle=self.modifiedSingleVideoTitle,
					failedVideoFileName=failedVideoFileName)
			except TypeError as e:
				print(e)
			
			if self.failedVideoPlaylistDic is not None:
				if isVideoDownloadSuccessful:
					self.failedVideoPlaylistDic.setVideoAudioFileNameForVideoIndex(videoIndex=failedVideoIndex,
					                                                               audioFileName=purgedOriginalOrModifiedVideoTitleWithPrefixSuffixDatesMp3)
					self.failedVideoPlaylistDic.setVideoDownloadTimeForVideoIndex(videoIndex=failedVideoIndex,
					                                                              videoDownloadTimeStr=DownloadPlaylistInfoDic.getNowDownloadDateTimeStr())
				
				self.failedVideoPlaylistDic.setVideoDownloadExceptionForVideoIndex(videoIndex=failedVideoIndex,
				                                                                   isDownloadSuccess=isVideoDownloadSuccessful)
				self.failedVideoPlaylistDic.saveDic(self.configMgr.dataPath)
				self.failedVideoPlaylistDic = None
			
			self.downloadThreadCreated = False  # used to fix a problem on Android
			# where two download threads are
			# created after clicking on 'Yes'
			# button on the ConfirmPopup dialog
			
			self.stopDownloadButton.disabled = True
	
	def createDownloadConfirmPopup(self,
	                               confirmPopupTitle,
	                               confirmPopupMsg,
	                               confirmPopupCallbackFunction,
	                               isPlayListDownloaded,
	                               playlistOrSingleVideoUrl):
		"""

		:param confirmPopupTitle:
		:param confirmPopupMsg:
		:param confirmPopupCallbackFunction:    function called when the user click on
												yes or no button
		:param isPlayListDownloaded             if True, download date prefix and upload date suffix
												checkboxes will be displayed.
												if False, for downloading a
												single video, the index and
												upload date inclusion in the
												audio file name are added anyway
												and the user can not change it
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
		
		self.confirmPopup = ConfirmDownloadPopup(text=confirmPopupFormattedMsg,
		                                         isPlaylist=isPlayListDownloaded,
		                                         playlistOrSingleVideoUrl=playlistOrSingleVideoUrl)
		
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
		elif self.originalSingleVideoTitle is not None:
			# downloading single video
			return self.audiobookSingleVideoPath
		else:
			# not downloading (clip or share file ...)
			return self.audiobookPath
	
	def displayVideoDownloadStartMessage(self, msgText, originalPlaylistTitle):
		self.increasePlaylistVideoDownloadNumber(originalPlaylistTitle=originalPlaylistTitle)
		self.updateStatusBar(msgText)
		self.outputResult(msgText)
	
	def displayPlaylistReDownloadInfo(self, originalPlaylistTitle):
		msgText = 're-downloading \n[b][color=0000FF]{}[/color][/b] playlist'.format(originalPlaylistTitle)
		self.outputResult(msgText)
	
	def increasePlaylistVideoDownloadNumber(self, originalPlaylistTitle):
		if originalPlaylistTitle in self.partiallyDownloadedPlaylistDic:
			self.partiallyDownloadedPlaylistDic[originalPlaylistTitle] += 1
		else:
			self.partiallyDownloadedPlaylistDic[originalPlaylistTitle] = 1
	
	def decreasePlaylistVideoDownloadNumber(self, originalPlaylistTitle):
		if originalPlaylistTitle in self.partiallyDownloadedPlaylistDic:
			downloadingVideoNumber = self.partiallyDownloadedPlaylistDic[originalPlaylistTitle] - 1;
			if downloadingVideoNumber == 0:
				self.partiallyDownloadedPlaylistDic.pop(originalPlaylistTitle)
			else:
				self.partiallyDownloadedPlaylistDic[originalPlaylistTitle] = downloadingVideoNumber
		else:
			print('calling decreasePlaylistVideoDownloadNumber for ' + originalPlaylistTitle + ' error')
	
	def displayFailedVideoPlaylistDownloadStartMessage(self, msg):
		self.outputResult(msg)
	
	def outputResult(self, resultStr, scrollToEnd=True):
		super(AudioDownloaderGUI, self).outputResult(resultStr, scrollToEnd=scrollToEnd)
		
		self.clearResultOutputButton.disabled = False
	
	def displayVideoCurrentDownloadInfo(self, currentDownloadInfoTuple):
		"""
		Method called every n seconds by
		AudioController.displayDownloadInfo().

		:param currentDownloadInfoTuple:    3 elements tuple containing current
											download size in bytes, download size
											percent string and current download
											speed string (in KB/s)
		"""
		outputLabelLineLst = self.outputLabel.text.split('\n')
		
		currentDownloadSize = currentDownloadInfoTuple[0]
		currentDownloadSizeFormatted = (f"{currentDownloadSize:,}")
		currentDownloadInfoStr = '{} bytes, {}, {}\n'.format(currentDownloadSizeFormatted,
		                                                     currentDownloadInfoTuple[1],
		                                                     currentDownloadInfoTuple[2])
		
		if self.isFirstCurrentDownloadInfo:
			outputLabelLineLst.append(currentDownloadInfoStr)
			self.isFirstCurrentDownloadInfo = False
		else:
			outputLabelLineLst = outputLabelLineLst[:-2]
			outputLabelLineLst.append(currentDownloadInfoStr)
		
		self.outputLabel.text = outputLabelLineLst[0] + '\n' + '\n'.join(outputLabelLineLst[1:])
	
	def displayVideoMp3ConversionCurrentInfo(self, videoCurrentMp3ConversionInfoList):
		"""
		Method called every n seconds by
		AudioController.displayVideoMp3ConversionCurrentInfo().

		:param videoCurrentMp3ConversionInfoList:   1 element list containing current
													conversion time hh:mm:ss string..
		"""
		outputLabelLineLst = self.outputLabel.text.split('\n')
		currentConversionInfoStr = 'mp3 conversion {}\n'.format(videoCurrentMp3ConversionInfoList[0])
		
		if self.isFirstCurrentDownloadInfo:
			outputLabelLineLst.append(currentConversionInfoStr)
			self.isFirstCurrentDownloadInfo = False
		else:
			outputLabelLineLst = outputLabelLineLst[:-2]
			outputLabelLineLst.append(currentConversionInfoStr)
		
		self.outputLabel.text = outputLabelLineLst[0] + '\n' + '\n'.join(outputLabelLineLst[1:])
	
	def handleDownloadHistory(self):
		"""
		Called by CustomDropDown.downloadHisto() which is called by Downl histo
		menu item defined in customdropdown.kv file.
		
		Displays the download history in the output result label, i.e.
		for each playlist the file names of the files still present in the
		playlist dir ordered by date, most recent first. Fills the download
		history list so that list items can be deleted.
		"""
		self.dropDownMenu.dismiss()
		
		audioFileHistoryLst = self.audioController.getAudioFilesSortedByDateInfoList(
			excludedSubDirNameLst=self.excludedSubDirNameLst)
		
		self.fillHistoryListWithDownloadHistory(audioFileHistoryLst)
		
		if os.name == 'posix':
			if GuiUtil.onTablet():
				# on smartphone, not enough room on output result label
				self.displayDownloadedFilesHistory(audioFileHistoryLst)
			else:
				self.openDownloadHistoRequestList()
		else:
			self.displayDownloadedFilesHistory(audioFileHistoryLst)
	
	def openDownloadHistoRequestList(self):
		"""
		Method called on smartphone only. On smartphone, the download history info
		is not displayed in the output result label. Instead, the request list
		containing the downloaded file names ordered by playlist and by download
		time is opened.
		"""
		self.showRequestList = False  # forces the list to be displayed
		self.toggleRequestList()
	
	def displayDeletedAudioFiles(self, deletedFilePathNameLst):
		if len(deletedFilePathNameLst) > 0:
			self.outputResult('\naudio files deleted\n')
		else:
			return
		
		for audioFilePath in deletedFilePathNameLst:
			self.outputResult(audioFilePath + '\n')
	
	def displayDownloadedFileName(self, selectedAudioItemDownloadData):
		"""
		Called by SelectableMultiFieldsItem.apply_selection(). When selecting
		a downloaded file displayed in the download histo list, displays the
		full name of the selected file.
		
		:param selectedAudioItemDownloadData:
		"""
		downloadedFileName = selectedAudioItemDownloadData.audioFileName
		downloadedDate = selectedAudioItemDownloadData.audioFileDownloadDate
		
		if downloadedDate not in downloadedFileName:
			fullDownloadedFileName = downloadedDate + ' ' + downloadedFileName
		else:
			fullDownloadedFileName = downloadedFileName
		
		playlistName = selectedAudioItemDownloadData.playlistName
		downloadVideoInfoDic = self.audioController.getDownloadPlaylistInfoDic(playlistName=playlistName)
		
		additionalDisplayedInfo = ''
		didDownloadFail = False
		
		if downloadVideoInfoDic is None:
			# the case if the selected audio file is currently in
			# Various dir or in an audio sub sub dir
			additionalDisplayedInfo = '. {} playlist info dic [b][color=FF0000]could not be found[/color][/b]'.format(
				playlistName)
		else:
			didDownloadFail = downloadVideoInfoDic.getVideoDownloadExceptionForVideoFileName(downloadedFileName)
		
		if didDownloadFail:
			additionalDisplayedInfo = ' [b][color=FF0000]download failed[/color][/b]'
		
		self.outputResult('\n' + fullDownloadedFileName + additionalDisplayedInfo)
	
	def displayDownloadedFilesHistory(self, audioFileHistoryLst):
		"""
		Displays the download history in the output result label, i.e.
		for each playlist the file names of the files still present in the
		playlist dir ordered by date, most recent first.
		"""
		outputLines = 0
		
		for audioPlaylistDirLst in audioFileHistoryLst:
			self.outputResult('\n[b][color=00FF00]{}[/color][/b]'.format(audioPlaylistDirLst[0]),
			                  scrollToEnd=False)
			for audioFileInfoLst in audioPlaylistDirLst[1]:
				if outputLines > 85:
					break
				downloadDate = audioFileInfoLst[1]
				downloadFileFullName = audioFileInfoLst[0]
				if DownloadPlaylistInfoDic.isAudioFileNamePrefixedWithDate(downloadFileFullName):
					self.outputResult('    [b]{}[/b]'.format(downloadFileFullName),
					                  scrollToEnd=False)
				else:
					self.outputResult('    [i]{}[/i] [b]{}[/b]'.format(downloadDate, downloadFileFullName),
					                  scrollToEnd=False)
				
				outputLines += 1
	
	def fillHistoryListWithDownloadHistory(self, audioFileHistoryLst):
		"""
		Displays the download history in the main GUI selectable list, i.e.
		for each playlist the file names of the files still present in the
		playlist dir ordered by date, most recent first. Each file list item
		has a checkbox in order to set if the file must be deleted physically,
		without being removed from the playlist dictionary file.
		
		:param audioFileHistoryLst  [
										[<audio sub-dir name 1>, [
												[<audio file name 1>, <yymmdd download date>],
												[<audio file name 2>, <yymmdd download date>]
											]
										],
										[<audio sub-dir name 2>, [
												[<audio file name 1>, <yymmdd download date>],
												[<audio file name 2>, <yymmdd download date>]
											]
										]
									]

		"""
		histoLines = []
		fileNameMaxLength = 42  # value ok for Android smartphone
		
		for audioSubDirDataLst in audioFileHistoryLst:
			playlistName = audioSubDirDataLst[0]
			formattedPlaylistName = '[b]' + playlistName + '[/b]'
			playlistDownloadHistoryData = DownloadHistoryData(type=DHD_TYPE_PLAYLIST,
			                                                  playlistName=playlistName)
			histoLines.append(
				{'text': formattedPlaylistName, 'data': playlistDownloadHistoryData, 'toDownload': False,
				 'selectable': True})  # resetting 'selectable' to True so that the
			# growse button can be activated for playlist
			# items as well
			for audioFileDataLst in audioSubDirDataLst[1]:
				audioFileName = audioFileDataLst[0]
				audioFileDownladDate_yymmdd = audioFileDataLst[1]
				audioFileDownloadHistoryData = DownloadHistoryData(type=DHD_TYPE_AUDIO_FILE,
				                                                   playlistName=playlistName,
				                                                   audioFileName=audioFileName,
				                                                   audioFileDownloadDate=audioFileDownladDate_yymmdd)
				shortenedAudioFileName = audioFileDownloadHistoryData.getAudioFileNameShortened(fileNameMaxLength)
				histoLines.append(
					{'text': shortenedAudioFileName, 'data': audioFileDownloadHistoryData, 'toDownload': False,
					 'selectable': True})
		self.requestListRV.data = histoLines
		self.requestListRVSelBoxLayout.clear_selection()
		
		# Reset the ListView
		self.toggleHistoButton.text = TOGGLE_HISTO_BUTTON_DOWN_HIST
		self.deleteBrowseButton.text = TOGGLE_DELETE_BUTTON_BROWSER
		self.downloadAllButton.text = TOGGLE_DOWNLOAD_ALL_BUTTON_DOWN_DEL
		self.resetListViewScrollToEnd()
		self.manageStateOfGlobalRequestListButtons()
		self.refocusOnFirstRequestInput()
	
	def moveAudioFileToOtherPlaylist(self):
		"""
		Called by Chge playlst menu item defined in customdropdown.kv file.

		Move an audio file to another playlist and update the source and destination
		playlist dic file.
		"""
		self.dropDownMenu.dismiss()
		print('not yet used')
	
	def displayVideoEndDownloadInfo(self, endDownloadInfoLst):
		"""
		Method called when the video download is finished by
		AudioController.displayVideoEndDownloadInfo().

		:param endDownloadInfoLst:  2 elements tuple containing final download
									size in bytes and total download time in
									seconds
		"""
		outputLabelLineLst = self.outputLabel.text.split('\n')
		videoDownloadSize = endDownloadInfoLst[0]
		videoDownloadSizeFormatted = (f"{videoDownloadSize:,}")
		endDownloadInfoStr = '{} bytes, {}\n'.format(videoDownloadSizeFormatted,
		                                             endDownloadInfoLst[1])
		self.addToOutputLabelStr(endDownloadInfoStr, outputLabelLineLst)
		self.updateStatusBar('')
	
	def displayVideoDownloadEndMessage(self, msgText, playListTitle):
		"""
		This method avoids that the current downloaded video title is
		deleted by the self.displayVideoCurrentDownloadInfo() next
		execution.

		:param msgText:
		"""
		self.decreasePlaylistVideoDownloadNumber(originalPlaylistTitle=playListTitle)
		self.isFirstCurrentDownloadInfo = True
		self.outputResult(msgText)
	
	def displayPlaylistEndDownloadInfo(self, endDownloadInfoLst):
		"""
		Method called when the playlist videos download is finished by
		AudioController.displayPlaylistEndDownloadInfo().

		:param endDownloadInfoLst:  4 elements list containing number of
									videos successfully downloaded, number od
									video download failure, number of
									video download skipped, playlist total
									download size in bytes and playlist total
									download time hh:mm:ss string
		"""
		outputLabelLineLst = self.outputLabel.text.split('\n')
		videoSuccessNb = endDownloadInfoLst[0]
		videoFailedNb = endDownloadInfoLst[1]
		videoSkippedNb = endDownloadInfoLst[2]
		
		self.totalDownloadVideoSuccessNb += videoSuccessNb
		self.totalDownloadVideoFailedNb += videoFailedNb
		self.totalDownloadVideoSkippedNb += videoSkippedNb
		
		if videoSuccessNb < 2:
			videoSuccessStr = 'video downloaded'
		else:
			videoSuccessStr = 'videos downloaded'
		
		if videoFailedNb < 2:
			videoFailStr = 'video failed'
		else:
			videoFailStr = 'videos failed'
		
		if videoSkippedNb < 2:
			videoSkippedStr = 'video skipped'
		else:
			videoSkippedStr = 'videos skipped'
		
		endDownloadInfoStr = '[b][color=00FF00]{} {}, {} {}, {} {}, {} bytes, {}[/color][/b]\n'.format(videoSuccessNb,
		                                                                                               videoSuccessStr,
		                                                                                               videoFailedNb,
		                                                                                               videoFailStr,
		                                                                                               videoSkippedNb,
		                                                                                               videoSkippedStr,
		                                                                                               endDownloadInfoLst[
			                                                                                               3],
		                                                                                               endDownloadInfoLst[
			                                                                                               4])
		
		self.addToOutputLabelStr(endDownloadInfoStr, outputLabelLineLst)
	
	def displaySingleVideoEndDownloadInfo(self,
	                                      msgText,
	                                      singleVideoDownloadStatus):
		"""
		Method called when the single video download is finished by
		AudioController.displaySingleVideoEndDownloadInfo().

		:param msgText: contains the single video title and the download dir.
		:param singleVideoDownloadStatus:   SINGLE_VIDEO_DOWNLOAD_SUCCESS or
											SINGLE_VIDEO_DOWNLOAD_FAIL
											SINGLE_VIDEO_DOWNLOAD_SKIPPED
		"""
		if singleVideoDownloadStatus == AudioController.SINGLE_VIDEO_DOWNLOAD_SUCCESS:
			self.totalDownloadVideoSuccessNb += 1
		elif singleVideoDownloadStatus == AudioController.SINGLE_VIDEO_DOWNLOAD_FAIL:
			self.totalDownloadVideoFailedNb += 1
		elif singleVideoDownloadStatus == AudioController.SINGLE_VIDEO_DOWNLOAD_SKIPPED:
			self.totalDownloadVideoSkippedNb += 1
		
		self.outputResult(msgText)
		self.updateStatusBar('')
	
	def displayUrlDownloadLstEndDownloadInfo(self):
		"""
		Method called when the multi urls download is finished.
		"""
		outputLabelLineLst = self.outputLabel.text.split('\n')
		
		endDownloadInfoStr = self.buildEndDownloadInfoStr()

		self.addToOutputLabelStr(endDownloadInfoStr, outputLabelLineLst)

	def displayFailedVideoRedownloadLstEndDownloadInfo(self):
		"""
		Method called when the failed video re-download on PC is finished.
		"""
		outputLabelLineLst = self.outputLabel.text.split('\n')
		
		endDownloadInfoStr = self.buildEndDownloadInfoStr()
		redownloadedVideoMsgLst = self.audioController.createFailedVideoRedownloadedDisplayMsgLst(
			audioDirRoot=self.audiobookPath)
		
		if len(redownloadedVideoMsgLst) > 0:
			endDownloadInfoStr += self.formatRedownloadedVideoMsgLst(redownloadedVideoMsgLst)
		
		self.addToOutputLabelStr(endDownloadInfoStr, outputLabelLineLst)
	
	
	def formatRedownloadedVideoMsgLst(self, msgLineLst):
		formattedMsgStr = '\n\n[b][color=00FF00]REDOWNLOADED FAILED VIDEOS[/color][/b]'
		
		for line in msgLineLst:
			if '\t' in line:
				# video file name, not formatted
				formattedMsgStr += line.replace('\t', '\n    [b]') + '[/b]'
			else:
				# playlist dir
				formattedMsgStr += '\n\n[b][color=00FF00]' + line.replace('/', sep) + '[/color][/b]'
				playlistName = line.rsplit('/', 1)[-1]
				self.decreasePlaylistVideoDownloadNumber(playlistName)
				self.outputResult(playlistName + ' decreased ------')
		
		return formattedMsgStr
	
	
	def addToOutputLabelStr(self, endDownloadInfoStr, outputLabelLineLst):
		outputLabelLineLst = outputLabelLineLst[:-1]
		outputLabelLineLst.append(endDownloadInfoStr)
		self.outputLabel.text = outputLabelLineLst[0] + '\n' + '\n'.join(outputLabelLineLst[1:])
		self.isFirstCurrentDownloadInfo = True
	
	
	def buildEndDownloadInfoStr(self):
		if self.totalDownloadVideoSuccessNb < 2:
			videoSuccessStr = 'video downloaded'
		else:
			videoSuccessStr = 'videos downloaded'
		if self.totalDownloadVideoFailedNb < 2:
			videoFailStr = 'video failed'
		else:
			videoFailStr = 'videos failed'
		if self.totalDownloadVideoSkippedNb < 2:
			videoSkippedStr = 'video skipped'
		else:
			videoSkippedStr = 'videos skipped'
		endDownloadInfoStr = '\n[b][color=00FF00]TOTAL {} {}, {} {}, {} {}[/color][/b]\n'.format(
			self.totalDownloadVideoSuccessNb,
			videoSuccessStr,
			self.totalDownloadVideoFailedNb,
			videoFailStr,
			self.totalDownloadVideoSkippedNb,
			videoSkippedStr)
		
		return endDownloadInfoStr
	
	
	def createYesNoPopup(self,
	                     yesNoPopupTitle,
	                     yesNoPopupMsg,
	                     yesNoPopupCallbackFunction,
	                     isPlayListDownloaded):
		"""
		Called in order to obtain confirmation from user on the way the downloaded
		audio files will be renamed using the video download date prefix and/or the
		video upload date suffix.
		
		:param yesNoPopupTitle:
		:param yesNoPopupMsg:
		:param yesNoPopupCallbackFunction:  function called when the user click on
											yes or no button
		:param isPlayListDownloaded         currently not used
	
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
		
		yesNoPopupFormattedMsg = GuiUtil.reformatString(yesNoPopupMsg, msgWidth)
		
		self.yesNoPopup = YesNoPopup(text=yesNoPopupFormattedMsg,
		                             isPlaylist=isPlayListDownloaded)
		
		self.yesNoPopup.bind(on_answer=yesNoPopupCallbackFunction)
		
		popup = Popup(title=yesNoPopupTitle,
		              content=self.yesNoPopup,
		              size_hint=(None, None),
		              pos_hint={'top': 0.8},
		              size=popupSize,
		              auto_dismiss=False)
		
		return popup
	
	
	def onPrefixSuffixFileNameConfirmYesNoPopupAnswer(self, yesNoPopupInstance, answer):
		"""
		Method called when one of the YesNoPopup button is pushed. The
		YesNoPopup is displayed when it is necessary to get user
		confirmation of the way the downloaded files will be renamed
		using video download date prefix or/and video upload date suffix.
	
		:param yesNoPopupInstance:
		:param answer:
		"""
		if answer == 'yes':  # 'yes' is set in yesnopopup.kv file
			# downloading the playlist or single video using a separate
			# thread. So, the download information is displayed in real
			# time on the outputLabel.
			
			playlistDownloadSubDir = self.downloadVideoInfoDic.getPlaylistDownloadBaseSubDir()
			playlistUrl = self.downloadVideoInfoDic.getPlaylistUrl()
			playlisiTitleModified = self.downloadVideoInfoDic.getPlaylistNameModified()
			self.addDownloadUrlToUrlList(playlistOrSingleVideoModifiedTitle=playlisiTitleModified,
			                             downloadSubdir=playlistDownloadSubDir,
			                             playlistOrSingleVideoUrl=playlistUrl)
			loadAtStartFilePathName, isLoadAtStart = self.getLoadAtStartFilePathName()
			self.saveUrlListToDownloadUrlInfoDicFile(loadAtStartFilePathName, isLoadAtStart)
			
			if not self.downloadThreadCreated:
				sepThreadExec = SepThreadExec(callerGUI=self,
				                              func=self.downloadPlaylistAudioOnNewThread)
				
				self.downloadThreadCreated = True  # used to fix a problem on Android
				# where two download threads are
				# created after clicking on 'Yes'
				# button on the ConfirmPopup dialog
				
				sepThreadExec.start()
		
		popup = yesNoPopupInstance.parent.parent.parent
		popup.dismiss()
	
	
	def downloadPlaylistAudioOnNewThread(self):
		"""
		This method is called if the user did confirm the playlist download
		with or without the download date (prefix) and/or upload date (suffix)
		settings. Since specifying those settings is possible only for playlist
		download, the method is called downloadPlaylistAudioOnNewThread and not
		downloadPlaylistOrSingleVideoAudioOnNewThread !
		"""
		self.audioController.downloadVideosReferencedInPlaylist(downloadVideoInfoDic=self.downloadVideoInfoDic,
		                                                        isIndexAddedToPlaylistVideo=self.isIndexAddedToPlaylistVideo,
		                                                        isUploadDateAddedToPlaylistVideo=self.isUploadDateAddedToPlaylistVideo)
		
		self.downloadThreadCreated = False  # used to fix a problem on Android
		# where two download threads are
		# created after clicking on 'Yes'
		# button on the ConfirmPopup dialog
		
		self.stopDownloadButton.disabled = True


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
	
	def build(self):
		"""
		Implicitely looks for a kv file of name cryptopricergui.kv which is
		class name without App, in lowercases
		"""
		# Builder is a global Kivy instance used
		# in widgets that you can use to load other
		# kv files in addition to the default ones.
		from kivy.lang import Builder
		
		# Loading Multiple .kv files
		Builder.load_file('filechooser.kv')
		Builder.load_file('okpopup.kv')
		Builder.load_file('confirmdownloadpopup.kv')
		Builder.load_file('yesnopopup.kv')
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
			config.setdefaults(ConfigManager.CONFIG_SECTION_LAYOUT, {
				ConfigManager.CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT: ConfigManager.DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_ANDROID})
			config.setdefaults(ConfigManager.CONFIG_SECTION_LAYOUT, {
				ConfigManager.CONFIG_KEY_DROP_DOWN_MENU_WIDTH: ConfigManager.DEFAULT_CONFIG_KEY_DROP_DOWN_MENU_WIDTH_ANDROID})
		elif platform == 'ios':
			config.setdefaults(ConfigManager.CONFIG_SECTION_LAYOUT,
			                   {ConfigManager.CONFIG_KEY_APP_SIZE: ConfigManager.APP_SIZE_HALF})
			config.setdefaults(ConfigManager.CONFIG_SECTION_GENERAL, {
				ConfigManager.CONFIG_KEY_DATA_PATH: ConfigManager.DEFAULT_DATA_PATH_IOS})
			config.setdefaults(ConfigManager.CONFIG_SECTION_GENERAL, {
				ConfigManager.CONFIG_KEY_SINGLE_VIDEO_DATA_PATH: ConfigManager.DEFAULT_SINGLE_VIDEO_DATA_PATH_IOS})
			config.setdefaults(ConfigManager.CONFIG_SECTION_LAYOUT, {
				ConfigManager.CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT: ConfigManager.DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_ANDROID})
			config.setdefaults(ConfigManager.CONFIG_SECTION_LAYOUT, {
				ConfigManager.CONFIG_KEY_DROP_DOWN_MENU_WIDTH: ConfigManager.DEFAULT_CONFIG_KEY_DROP_DOWN_MENU_WIDTH_IOS})
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
				ConfigManager.CONFIG_KEY_DROP_DOWN_MENU_WIDTH: ConfigManager.DEFAULT_CONFIG_KEY_DROP_DOWN_MENU_WIDTH_WINDOWS})
		
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
				},
				{
					"type": "string",
					"title": "Download history excluded audio sub-dirs ",
					"desc": "List of comma separated audio sub-dirs which will not be included in the download history",
					"section": "General",
					"key": "excludedaudiosubdirnamelst"
				}
			]"""))  # "key": "dataPath" above is the key in the app config file. To use another
		# drive, simply define it as datapath value in the app config file
		
		# add 'Layout' settings panel
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
					"title": "URL list item height",
					"desc": "Set the height of each item in the URL list",
					"section": "Layout",
					"key": "histolistitemheight"
				},
				{"type": "numeric",
					"title": "URL list visible item number",
					"desc": "Set the number of items displayed in the URL list",
					"section": "Layout",
					"key": "histolistvisiblesize"
				},
				{"type": "numeric",
					"title": "Drop down menu width",
					"desc": "Set the width of the drop down menu. Effective on smartphone only !",
					"section": "Layout",
					"key": "dropdownmenuwidth"
				},
				{"type": "numeric",
					"title": "Status bar height",
					"desc": "Set the height of the status bar",
					"section": "Layout",
					"key": "statusbarheight"
				},
				{"type": "numeric",
					"title": "Clear button width",
					"desc": "Set the width of the clear button",
					"section": "Layout",
					"key": "clearbuttonwidth"
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
		"""
		Event handler fired when a configuration token has been changed by the settings
		page.
		
		:param config:
		:param section:
		:param key:
		:param value:
		:return:
		"""
		if config is self.config:
			if key == ConfigManager.CONFIG_KEY_APP_SIZE:
				appSize = config.getdefault(ConfigManager.CONFIG_SECTION_LAYOUT, ConfigManager.CONFIG_KEY_APP_SIZE,
				                            "Half").upper()
				
				if appSize == "HALF":
					self.audioDownloaderGUI.appSize = ConfigManager.APP_SIZE_HALF
				else:
					self.audioDownloaderGUI.appSize = ConfigManager.APP_SIZE_FULL
				
				self.audioDownloaderGUI.applyAppPosAndSize()
			elif key == ConfigManager.CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT:
				self.audioDownloaderGUI.rvListItemHeight = int(config.getdefault(ConfigManager.CONFIG_SECTION_LAYOUT,
				                                                                 ConfigManager.CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT,
				                                                                 ConfigManager.DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_ANDROID))
				self.audioDownloaderGUI.rvListSizeSettingsChanged()
			elif key == ConfigManager.CONFIG_KEY_HISTO_LIST_VISIBLE_SIZE:
				self.audioDownloaderGUI.rvListMaxVisibleItems = int(
					config.getdefault(ConfigManager.CONFIG_SECTION_LAYOUT,
					                  ConfigManager.CONFIG_KEY_HISTO_LIST_VISIBLE_SIZE,
					                  ConfigManager.DEFAULT_CONFIG_HISTO_LIST_VISIBLE_SIZE))
				self.audioDownloaderGUI.rvListSizeSettingsChanged()
			elif key == ConfigManager.CONFIG_KEY_DROP_DOWN_MENU_WIDTH:
				self.audioDownloaderGUI.dropDownMenu.auto_width = False
				self.audioDownloaderGUI.dropDownMenu.width = \
					dp(int(config.getdefault(ConfigManager.CONFIG_SECTION_LAYOUT,
					                         ConfigManager.CONFIG_KEY_DROP_DOWN_MENU_WIDTH,
					                         ConfigManager.DEFAULT_CONFIG_KEY_DROP_DOWN_MENU_WIDTH_ANDROID)))
			elif key == ConfigManager.CONFIG_KEY_STATUS_BAR_HEIGHT:
				self.audioDownloaderGUI.boxLayoutContainingStatusBar.height = \
					dp(int(config.getdefault(ConfigManager.CONFIG_SECTION_LAYOUT,
					                         ConfigManager.CONFIG_KEY_STATUS_BAR_HEIGHT,
					                         ConfigManager.DEFAULT_CONFIG_KEY_STATUS_BAR_HEIGHT_WINDOWS)))
			elif key == ConfigManager.CONFIG_KEY_CLEAR_BUTTON_WIDTH:
				self.audioDownloaderGUI.clearResultOutputButton.width = \
					dp(int(config.getdefault(ConfigManager.CONFIG_SECTION_LAYOUT,
					                         ConfigManager.CONFIG_KEY_CLEAR_BUTTON_WIDTH,
					                         ConfigManager.DEFAULT_CONFIG_KEY_CLEAR_BUTTON_WIDTH_WINDOWS)))
			elif key == ConfigManager.CONFIG_KEY_APP_SIZE_HALF_PROPORTION:
				self.audioDownloaderGUI.appSizeHalfProportion = float(
					config.getdefault(ConfigManager.CONFIG_SECTION_LAYOUT,
					                  ConfigManager.CONFIG_KEY_APP_SIZE_HALF_PROPORTION,
					                  ConfigManager.DEFAULT_CONFIG_KEY_APP_SIZE_HALF_PROPORTION))
				self.audioDownloaderGUI.applyAppPosAndSize()
			elif key == ConfigManager.CONFIG_KEY_EXCLUDED_AUDIO_SUBDIR_NAME_LST:
				self.audioDownloaderGUI.excludedSubDirNameLst = config.getdefault(ConfigManager.CONFIG_SECTION_GENERAL,
				                                                                  ConfigManager.CONFIG_KEY_EXCLUDED_AUDIO_SUBDIR_NAME_LST,
				                                                                  ConfigManager.DEFAULT_EXCLUDED_AUDIO_SUBDIR_NAME_LST)
	
	def get_application_config(self, **kwargs):
		'''
		Redefining super class method to control the name and location of the
		application	settings ini file. WARNING: this method is necessary for
		the app config file to be updated when a value was changed with the
		Kivy settings dialog.

		:param **kwargs:
		:return: the app config file path name
		'''
		configFilePathName = DirUtil.getConfigFilePathName()
		
		return configFilePathName
	
	def open_settings(self, *largs):
		"""
		Inherited method redefined so that the drop down menu is closed
		before opening the settings. Otherwise, the drop down menu would
		remain open after the settings screen was closed.

		:param largs:
		"""
		self.audioDownloaderGUI.dropDownMenu.dismiss()
		
		# catching NoOptionError avoids displaying the exception stack trace
		# which happens the first time the application is executed after
		# a new settings param has been added. In this case, thanks to the
		# exception catch, the app is closed and when it is started again,
		# no exception is thrown since the missing parms were added to the
		# app ini file.
		
		try:
			super().open_settings(*largs)
		except NoOptionError as e:
			logging.info(str(e) + '. Default settings values have been set in audiodownloader.ini file')
			self.stop()


if __name__ == '__main__':
	dbApp = AudioDownloaderGUIMainApp()
	
	dbApp.run()
