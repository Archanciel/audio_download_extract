import unittest
import os, sys, inspect
from os.path import sep

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from kivy.core.clipboard import Clipboard

from configmanager import ConfigManager
from dirutil import DirUtil
from gui.audiodownloadergui import AudioDownloaderGUIMainApp

class TryTestAudioDownloaderGUIUrlList(unittest.TestCase):

	def __init__(self):
		super().__init__()

		self.configMgr = ConfigManager(DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini')

		self.singleVideoAudioFileNameLst = []
		self.urlDownloadLst = []
		self.playlistSaveDirNameLst = []
		self.playlistDirNameLst = []

		# self.playlistDirName_0 = "test_small_videos"
		# self.playlistDirNameLst.append(self.playlistDirName_0)
		# self.playlistDirName_2 = "test_small_videos_2"
		# self.playlistDirNameLst.append(self.playlistDirName_2)
		# self.playlistDirName_3 = "test_small_videos_3"
		# self.playlistDirNameLst.append(self.playlistDirName_3)
		# self.playlistDirName_4 = "test_audio_downloader_two_files_with_time_frames"
		# self.playlistDirNameLst.append(self.playlistDirName_4)
		self.playlistDirName_5 = "test warning index date files_noIndexNoDate"
		self.playlistDirNameLst.append(self.playlistDirName_5)
		self.playlistDirName_6 = "test warning index date files_indexNoDate"
		self.playlistDirNameLst.append(self.playlistDirName_6)

		self.singleVideoUrl_1 = 'https://youtu.be/t2K4uM9ktsE'
		self.singleVideoUrl_2 = 'https://youtu.be/zUEmV7ubwyc'

	def tryTestAudioDownloaderGUI(self):
		
		# playlistSaveDirName_0 = self.playlistDirName_0 + sep + '80%'
		# self.playlistSaveDirNameLst.append(playlistSaveDirName_0)
		# playlistUrl_0 = 'https://youtube.com/playlist?list=PLzwWSJNcZTMTBd1_CeKf-HnPinxiqo2zy'
		# self.urlDownloadLst.append(playlistUrl_0)
		#
		# self.urlDownloadLst.append(self.singleVideoUrl_1)
		# singleVideoFileName_1 = 'Try Not To Laugh _ The most interesting funny short video tik tok #shorts 2021-12-05.mp3'
		# self.singleVideoAudioFileNameLst.append(singleVideoFileName_1)
		#
		# playlistSaveDirName_2 = self.playlistDirName_2 + sep + '80%'
		# self.playlistSaveDirNameLst.append(playlistSaveDirName_2)
		# playlistUrl_2 = 'https://youtube.com/playlist?list=PLzwWSJNcZTMTiWvWX6IO1t9RkCpKraYfb'
		# self.urlDownloadLst.append(playlistUrl_2)
		#
		# playlistSaveDirName_3 = self.playlistDirName_3 + sep + '80%'
		# self.playlistSaveDirNameLst.append(playlistSaveDirName_3)
		# playlistUrl_3 = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRx16thPZ3i4u3ZJthdifqo'
		# self.urlDownloadLst.append(playlistUrl_3)
		#
		# self.urlDownloadLst.append(self.singleVideoUrl_2)
		# singleVideoFileName_2 = 'Short King Struggles 🥲 2021-07-28.mp3'
		# self.singleVideoAudioFileNameLst.append(singleVideoFileName_2)
		#
		# playlistSaveDirName_4 = None # avoids playlist dir restore after it was empied
		# self.playlistSaveDirNameLst.append(playlistSaveDirName_4)
		# playlistUrl_4 = 'https://youtube.com/playlist?list=PLzwWSJNcZTMSFWGrRGKOypqN29MlyuQvn'
		# self.urlDownloadLst.append(playlistUrl_4)

		# playlist where only one file is to be downloaded since it was deleted
		# from the save dir. Since all the files in the playlist dir are named
		# without index and without date, the downloaded file name must also be
		# without index and without date.
		playlistSaveDirName_5 = self.playlistDirName_5 + sep + "100%"
		self.playlistSaveDirNameLst.append(playlistSaveDirName_5)
		playlistUrl_5 = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRVKblKqskAyseCgsUmhlSc'
		self.urlDownloadLst.append(playlistUrl_5)

		# playlist where only one file is to be downloaded since it was deleted
		# from the save dir. No file in the playlist dir is named with upload
		# date suffix. Since one file in the playlist dir is named
		# with index prefix, the downloaded file name must also be
		# named with index prefix and without date suffix.
		playlistSaveDirName_6 = self.playlistDirName_6 + sep + "100%"
		self.playlistSaveDirNameLst.append(playlistSaveDirName_6)
		playlistUrl_6 = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRqeXBddcErPTC__A2KHjFd'
		self.urlDownloadLst.append(playlistUrl_6)

		singleVideoSaveDirName = 'single80%'
		
		self.restorePlaylistDownloadDirs(self.playlistDirNameLst,
		                                 self.playlistSaveDirNameLst,
		                                 singleVideoSaveDirName,
		                                 self.singleVideoAudioFileNameLst)
		self.restoreUrlDownloadFile(self.urlDownloadLst,
		                            self.configMgr.loadAtStartPathFilename)
		
		
		Clipboard.copy('  ')
#		Clipboard.copy(playlistUrl_6)   # causes the downloaded video to be prefixed
										# with index and suffixed with upload date !!

		dbApp = AudioDownloaderGUIMainApp()
		dbApp.run()
	
	def restorePlaylistDownloadDirs(self,
	                                playlistDirNameLst,
	                                playlistSaveDirNameLst,
	                                singleVideoSaveDirName,
	                                singleVideoAudioFileNameLst):
		downloadDirLst = []
		
		for playlistDirName, playlistSaveDirName in zip(playlistDirNameLst, playlistSaveDirNameLst):
			downloadDir = self.configMgr.dataPath + sep + playlistDirName
			DirUtil.deleteFilesInDirForPattern(downloadDir, '*')
			
			if playlistSaveDirName:
				savedDownloadDir = self.configMgr.dataPath + sep + playlistSaveDirName
				DirUtil.copyFilesInDirToDirForPattern(sourceDir=savedDownloadDir,
				                                      targetDir=downloadDir,
				                                      fileNamePattern='*')
			downloadDirLst.append(downloadDir)

		for singleVideoAudioFileName in singleVideoAudioFileNameLst:
			DirUtil.deleteFileIfExist(self.configMgr.singleVideoDataPath + sep + singleVideoAudioFileName)
			
		DirUtil.copyFilesInDirToDirForPattern(sourceDir=self.configMgr.singleVideoDataPath + sep + singleVideoSaveDirName,
		                                      targetDir=self.configMgr.singleVideoDataPath,
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
