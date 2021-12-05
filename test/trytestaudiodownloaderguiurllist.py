import unittest
import os, sys, inspect, shutil, glob, time
from io import StringIO
from os.path import sep

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)
#sys.path.insert(1, parentDir + sep + 'gui')

from constants import *
from guioutputstub import GuiOutputStub
from audiocontroller import AudioController
from configmanager import ConfigManager
from dirutil import DirUtil
from downloadvideoinfodic import DownloadVideoInfoDic
from kivy.core.clipboard import Clipboard

from gui.filechooserpopup import LoadFileChooserPopup
from gui.filechooserpopup import SaveFileChooserPopup
from gui.filechooserpopup import DeleteFileChooserPopup
from gui.filechooserpopup import SelectOrCreateDirFileChooserPopup
from gui.filechooserpopup import FileToClipLoadFileChooserPopup
from gui.filechooserpopup import FileToShareLoadFileChooserPopup
from gui.confirmdownloadpopup import ConfirmDownloadPopup
from gui.yesnopopup import YesNoPopup
from gui.helputil import HelpUtil
from gui.helppopup import HelpPopup
from gui.focustextinput import FocusTextInput
from gui.audioclippergui import AudioClipperGUI
from gui.audiosharegui import AudioShareGUI
from gui.audiopositiongui import AudioPositionGUI

from gui.audiogui import AudioGUI
from gui.audiogui import FILE_ACTION_LOAD
from constants import *
from configmanager import ConfigManager
from audiocontroller import AudioController
from gui.guiutil import GuiUtil
from gui.selectablerecycleboxlayout import SelectableRecycleBoxLayout
from dirutil import DirUtil
from septhreadexec import SepThreadExec


from gui.audiodownloadergui import AudioDownloaderGUIMainApp
from gui.audiodownloadergui import AudioDownloaderGUI

class TryTestAudioDownloaderGUIUrlList(unittest.TestCase):

	def tryTestAudioDownloaderGUI(self):
		configMgr = ConfigManager(
			DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini')

		playlistDirNameLst = []
		playlistSaveDirNameLst = []

		playlistDirName_0 = "test_small_videos"
		playlistSaveDirName_0 = "test_small_videos" + sep + '80%'
		playlistDirNameLst.append(playlistDirName_0)
		playlistSaveDirNameLst.append(playlistSaveDirName_0)

		playlistDirName_1 = "test_small_videos_1"
		playlistSaveDirName_1 = "test_small_videos_1" + sep + '80%'
		playlistDirNameLst.append(playlistDirName_1)
		playlistSaveDirNameLst.append(playlistSaveDirName_1)

		playlistDirName_2 = "test_small_videos_2"
		playlistSaveDirName_2 = "test_small_videos_2" + sep + '80%'
		playlistDirNameLst.append(playlistDirName_2)
		playlistSaveDirNameLst.append(playlistSaveDirName_2)

		playlistDirName_3 = "test_small_videos_3"
		playlistSaveDirName_3 = "test_small_videos_3" + sep + '80%'
		playlistDirNameLst.append(playlistDirName_3)
		playlistSaveDirNameLst.append(playlistSaveDirName_3)

		self.restorePlaylistDownloadDirs(configMgr, playlistDirNameLst, playlistSaveDirNameLst)
		
		Clipboard.copy('https://youtube.com/playlist?list=PLzwWSJNcZTMRx16thPZ3i4u3ZJthdifqo')
		dbApp = AudioDownloaderGUIMainApp()
		dbApp.run()
		audioDownloaderGUI = dbApp.audioDownloaderGUI
		
		audioDownloaderGUI.addDownloadUrl()
		
		self.assertTrue(True)
	
	def restorePlaylistDownloadDirs(self,
	                                configMgr,
	                                playlistDirNameLst,
	                                playlistSaveDirNameLst):
		downloadDirLst = []
		
		for playlistDirName, playlistSaveDirName in zip(playlistDirNameLst, playlistSaveDirNameLst):
			downloadDir = configMgr.dataPath + sep + playlistDirName
			savedDownloadDir = configMgr.dataPath + sep + playlistSaveDirName
			DirUtil.deleteFilesInDirForPattern(downloadDir, '*')
			DirUtil.copyFilesInDirToDirForPattern(sourceDir=savedDownloadDir,
			                                      targetDir=downloadDir,
			                                      fileNamePattern='*')
			downloadDirLst.append(downloadDir)
			
		return downloadDirLst


if __name__ == '__main__':
#	unittest.main()
	tst = TryTestAudioDownloaderGUIUrlList()
	tst.tryTestAudioDownloaderGUI()
