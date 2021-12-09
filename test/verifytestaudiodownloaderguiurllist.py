import unittest
import os, sys, inspect, shutil, glob, time
from io import StringIO
from os.path import sep

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from dirutil import DirUtil
from trytestaudiodownloaderguiurllist import TryTestAudioDownloaderGUIUrlList

class VerifyTestAudioDownloaderGUIUrlList(TryTestAudioDownloaderGUIUrlList):
	
	def __init__(self):
		super().__init__()

	def verifyTestAudioDownloaderGUI(self):
		playlistDirExpectedFileNameLstDic = {}
		singleVideoExpectedFileNameLst = []
		
		downloadDir = self.configMgr.dataPath + sep + self.playlistDirName_3
		playlistDir_expectedFileNameLst = DirUtil.getFileNamesInDir(downloadDir)
		
		# the two videos in the playlist have been partially downloaded
		playlistDir_0_expectedFileNameLst = ['97-Product - 30 seconds animated short film 2020-08-14.mp3',
		                                     '98-Creative short film - Wonderful little world 2017-01-24.mp3',
		                                     'test_small_videos_dic.txt']
		playlistDirExpectedFileNameLstDic[self.playlistDirName_0] = playlistDir_0_expectedFileNameLst
		
		# the three videos in the playlist have been partially downloaded
		playlistDir_3_expectedFileNameLst = ['96-SLS DRIFT TAXI. Arina. #shorts 2021-08-12.mp3',
		                                     '97-Indian 🇮🇳_American🇺🇸_ Japanese🇯🇵_Students #youtubeshorts #shorts _Samayra Narula_ Subscribe  2021-09-17.mp3',
		                                     '98-Innovation (Short Film) 2020-01-07.mp3',
		                                     'test_small_videos_3_dic.txt']
		playlistDirExpectedFileNameLstDic[self.playlistDirName_3] = playlistDir_3_expectedFileNameLst
		
		# verifying a playlist with extract and suppress portion settings
		# in playlist title
		playlistDir_4_expectedFileNameLst = ['98-Here to help - Give him what he wants 2019-06-07.mp3',
		                                     '98-Here to help - Give him what he wants 2019-06-07_s.mp3',
		                                     '99-Wear a mask. Help slow the spread of Covid-19. 2020-07-31.mp3',
		                                     '99-Wear a mask. Help slow the spread of Covid-19. 2020-07-31_1.mp3',
		                                     'test_audio_downloader_two_files_with_time_frames_dic.txt']
		playlistDirExpectedFileNameLstDic[self.playlistDirName_4] = playlistDir_4_expectedFileNameLst

		# now verifying the index prefix and upload date suffix automatic
		# setting for playlist url list downloading

		playlistDir_5_expectedFileNameLst = ['Funny suspicious looking dog.mp3',
		                                     'Here to help - Give him what he wants.mp3',
		                                     'Shmeksss Short Video.mp3',
		                                     'test warning index date files_noIndexNoDate_dic.txt',
		                                     'Wear a mask. Help slow the spread of Covid-19..mp3']
		playlistDirExpectedFileNameLstDic[self.playlistDirName_5] = playlistDir_5_expectedFileNameLst
		
		playlistDir_6_expectedFileNameLst = ['92-Shmeksss Short Video.mp3',
		                                     '98-Here to help - Give him what he wants.mp3',
		                                     'Funny suspicious looking dog.mp3',
		                                     'test warning index date files_indexNoDate_dic.txt',
		                                     'Wear a mask. Help slow the spread of Covid-19..mp3']
		playlistDirExpectedFileNameLstDic[self.playlistDirName_6] = playlistDir_6_expectedFileNameLst

		playlistDir_7_expectedFileNameLst = ['Funny suspicious looking dog 2013-11-05.mp3',
		                                     'Here to help - Give him what he wants.mp3',
		                                     'Shmeksss Short Video 2021-01-26.mp3',
		                                     'test warning index date files_noIndexDate_dic.txt',
		                                     'Wear a mask. Help slow the spread of Covid-19..mp3']
		playlistDirExpectedFileNameLstDic[self.playlistDirName_7] = playlistDir_7_expectedFileNameLst

		playlistDir_8_expectedFileNameLst = ['92-Shmeksss Short Video 2021-01-26.mp3',
		                                     '99-Wear a mask. Help slow the spread of Covid-19. 2020-07-31.mp3',
		                                     'Funny suspicious looking dog.mp3',
		                                     'Here to help - Give him what he wants.mp3',
		                                     'test warning index date files_IndexDate_dic.txt']
		playlistDirExpectedFileNameLstDic[self.playlistDirName_8] = playlistDir_8_expectedFileNameLst

		playlistDir_9_expectedFileNameLst = ['99-Shmeksss Short Video 2021-01-26.mp3',
		                                     'test warning index date files_downloadDirNotExist_dic.txt']
		playlistDirExpectedFileNameLstDic[self.playlistDirName_9] = playlistDir_9_expectedFileNameLst

		playlistDir_10_expectedFileNameLst = ['99-Shmeksss Short Video 2021-01-26.mp3',
		                                     'test warning index date files_downloadDirEmpty_dic.txt']
		playlistDirExpectedFileNameLstDic[self.playlistDirName_10] = playlistDir_10_expectedFileNameLst

		self.verifyPlaylistDownloadDirs(self.playlistDirNameLst,
		                                playlistDirExpectedFileNameLstDic,
		                                singleVideoExpectedFileNameLst)
	
	def verifyPlaylistDownloadDirs(self,
	                               playlistDirNameLst,
	                               playlistDirExpectedFileNameLstDic,
	                               singleVideoExpectedFileNameLst):
		for playlistDirName in playlistDirNameLst:
			print('verifying ' + playlistDirName)
			playlistDirExpectedFileNameLst = playlistDirExpectedFileNameLstDic[playlistDirName]
			downloadDir = self.configMgr.dataPath + sep + playlistDirName
			playlistDirActualFileNameLst = DirUtil.getFileNamesInDir(downloadDir)
			self.assertEqual(playlistDirExpectedFileNameLst, playlistDirActualFileNameLst)

		singleVideoActualFileNameLst = DirUtil.getFileNamesInDir(self.configMgr.singleVideoDataPath)

		for singleVideoAudioFileName in singleVideoExpectedFileNameLst:
			print('verifying ' + singleVideoAudioFileName)
			self.assertTrue(singleVideoAudioFileName in singleVideoActualFileNameLst)


if __name__ == '__main__':
#	unittest.main()
	tst = VerifyTestAudioDownloaderGUIUrlList()
	tst.verifyTestAudioDownloaderGUI()
