import unittest
import os, sys, inspect, shutil, glob, time
from io import StringIO
from os.path import sep

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from configmanager import ConfigManager
from dirutil import DirUtil
from trytestaudiodownloaderguiurllist import TryTestAudioDownloaderGUIUrlList

class VerifyTestAudioDownloaderGUIUrlList(TryTestAudioDownloaderGUIUrlList):
	
	def __init__(self):
		super().__init__()

	def verifyTestAudioDownloaderGUI(self):
		playlistDirExpectedFileNameLstDic = {}
		singleVideoExpectedFileNameLst = []
		
		# playlist where only one file is to be downloaded since it was deleted
		# from the save dir. Since all the files in the playlist dir are named
		# without index and without date, the downloaded file name must also be
		# without index and without date
		downloadDir = self.configMgr.dataPath + sep + self.playlistDirName_5
		playlistDir_5_expectedFileNameLst = DirUtil.getFileNamesInDir(downloadDir)
		
		playlistDir_5_expectedFileNameLst = ['Funny suspicious looking dog.mp3',
		                                     'Here to help - Give him what he wants.mp3',
		                                     'Shmeksss Short Video.mp3',
		                                     'test warning index date files_noIndexNoDate_dic.txt',
		                                     'Wear a mask. Help slow the spread of Covid-19..mp3']
		playlistDirExpectedFileNameLstDic[self.playlistDirName_5] = playlistDir_5_expectedFileNameLst
		
		self.verifyPlaylistDownloadDirs(self.playlistDirNameLst,
		                                playlistDirExpectedFileNameLstDic,
		                                singleVideoExpectedFileNameLst)
	
	def verifyPlaylistDownloadDirs(self,
	                               playlistDirNameLst,
	                               playlistDirExpectedFileNameLstDic,
	                               singleVideoExpectedFileNameLst):
		for playlistDirName in playlistDirNameLst:
			playlistDirExpectedFileNameLst = playlistDirExpectedFileNameLstDic[playlistDirName]
			downloadDir = self.configMgr.dataPath + sep + playlistDirName
			playlistDirActualFileNameLst = DirUtil.getFileNamesInDir(downloadDir)
			self.assertEqual(playlistDirExpectedFileNameLst, playlistDirActualFileNameLst)

		singleVideoActualFileNameLst = DirUtil.getFileNamesInDir(self.configMgr.singleVideoDataPath)

		for singleVideoAudioFileName in singleVideoExpectedFileNameLst:
			self.assertTrue(singleVideoAudioFileName in singleVideoActualFileNameLst)


if __name__ == '__main__':
#	unittest.main()
	tst = VerifyTestAudioDownloaderGUIUrlList()
	tst.verifyTestAudioDownloaderGUI()
