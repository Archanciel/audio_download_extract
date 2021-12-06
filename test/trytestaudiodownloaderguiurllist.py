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
		urlDownloadLst = []
		singleVideoAudioFileNameLst = []

		playlistDirName_0 = "test_small_videos"
		playlistSaveDirName_0 = "test_small_videos" + sep + '80%'
		playlistDirNameLst.append(playlistDirName_0)
		playlistSaveDirNameLst.append(playlistSaveDirName_0)
		playlistUrl_0 = 'https://youtube.com/playlist?list=PLzwWSJNcZTMTBd1_CeKf-HnPinxiqo2zy'
		urlDownloadLst.append(playlistUrl_0)

		# playlistDirName_1 = "Test 3 short videos extr_sup"
		# playlistSaveDirName_1 = "Test 3 short videos extr_sup" + sep + '80%'
		# playlistDirNameLst.append(playlistDirName_1)
		# playlistSaveDirNameLst.append(playlistSaveDirName_1)
		# playlistUrl_1 = 'https://youtube.com/playlist?list=PLzwWSJNcZTMShenMgwyjHC8o5bU8QUPbn'
		# urlDownloadLst.append(playlistUrl_1)

		singleVideoUrl_1 = 'https://youtu.be/t2K4uM9ktsE' # Short King Struggles
		urlDownloadLst.append(singleVideoUrl_1)
		singleVideoFileName_1 = 'Try Not To Laugh _ The most interesting funny short video tik tok #shorts 2021-12-05.mp3'
		singleVideoAudioFileNameLst.append(singleVideoFileName_1)

		playlistDirName_2 = "test_small_videos_2"
		playlistSaveDirName_2 = "test_small_videos_2" + sep + '80%'
		playlistDirNameLst.append(playlistDirName_2)
		playlistSaveDirNameLst.append(playlistSaveDirName_2)
		playlistUrl_2 = 'https://youtube.com/playlist?list=PLzwWSJNcZTMTiWvWX6IO1t9RkCpKraYfb'
		urlDownloadLst.append(playlistUrl_2)

		playlistDirName_3 = "test_small_videos_3"
		playlistSaveDirName_3 = "test_small_videos_3" + sep + '80%'
		playlistDirNameLst.append(playlistDirName_3)
		playlistSaveDirNameLst.append(playlistSaveDirName_3)
		playlistUrl_3 = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRx16thPZ3i4u3ZJthdifqo'
		urlDownloadLst.append(playlistUrl_3)

		singleVideoUrl_2 = 'https://youtu.be/zUEmV7ubwyc' # Try Not To Laugh | The most interesting funny short video tik tok
		urlDownloadLst.append(singleVideoUrl_2)
		singleVideoFileName_2 = 'Short King Struggles 🥲 2021-07-28.mp3'
		singleVideoAudioFileNameLst.append(singleVideoFileName_2)

		singleVideoSaveDirName = 'single80%'
		
		self.restorePlaylistDownloadDirs(configMgr,
		                                 playlistDirNameLst,
		                                 playlistSaveDirNameLst,
		                                 singleVideoSaveDirName,
		                                 singleVideoAudioFileNameLst)
		self.restoreUrlDownloadFile(urlDownloadLst,
		                            configMgr.loadAtStartPathFilename)
		

		dbApp = AudioDownloaderGUIMainApp()
		dbApp.run()
	
	def restorePlaylistDownloadDirs(self,
	                                configMgr,
	                                playlistDirNameLst,
	                                playlistSaveDirNameLst,
	                                singleVideoSaveDirName,
	                                singleVideoAudioFileNameLst):
		downloadDirLst = []
		
		for playlistDirName, playlistSaveDirName in zip(playlistDirNameLst, playlistSaveDirNameLst):
			downloadDir = configMgr.dataPath + sep + playlistDirName
			savedDownloadDir = configMgr.dataPath + sep + playlistSaveDirName
			DirUtil.deleteFilesInDirForPattern(downloadDir, '*')
			DirUtil.copyFilesInDirToDirForPattern(sourceDir=savedDownloadDir,
			                                      targetDir=downloadDir,
			                                      fileNamePattern='*')
			downloadDirLst.append(downloadDir)

		for singleVideoAudioFileName in singleVideoAudioFileNameLst:
			DirUtil.deleteFileIfExist(configMgr.singleVideoDataPath + sep + singleVideoAudioFileName)
			
		DirUtil.copyFilesInDirToDirForPattern(sourceDir=configMgr.singleVideoDataPath + sep + singleVideoSaveDirName,
		                                      targetDir=configMgr.singleVideoDataPath,
		                                      fileNamePattern='*')

		return downloadDirLst
	
	def restoreUrlDownloadFile(self,
	                           urlDownloadLst,
	                           urlDownloadLstFilePathName):
		with open(urlDownloadLstFilePathName, 'w') as f:
			f.writelines('\n'.join(urlDownloadLst))


if __name__ == '__main__':
#	unittest.main()
	tst = TryTestAudioDownloaderGUIUrlList()
	tst.tryTestAudioDownloaderGUI()
