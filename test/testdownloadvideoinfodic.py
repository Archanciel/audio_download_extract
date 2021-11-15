import shutil
import unittest
import os, sys, inspect, glob, time
from os.path import sep
from datetime import datetime

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)
		
from downloadvideoinfodic import DownloadVideoInfoDic
from constants import *
from dirutil import DirUtil
			
class TestDownloadVideoInfoDic(unittest.TestCase):
	def testAddVideoInfoForVideoIndex_new_info_dic_file(self):
		playlistUrl = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS'
		playListName = 'test_download_vid_info_dic'
		playlistTitle = playListName
		
		audioDirRoot = DirUtil.getTestAudioRootPath()
		downloadDir = audioDirRoot + sep + playListName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting video info dic files
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		dvi = DownloadVideoInfoDic(playlistUrl, audioDirRoot, audioDirRoot, playlistTitle, playListName, playlistTitle, playListName)
		additionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_VIDEO_INFO_FILE)

		videoIndex = dvi.getNextVideoIndex()
		title_1 = 'title 1'
		url_1 = 'https://youtube.com/watch?v=9iPvLx7gotk'
		videoFileName_1 = 'title 1.mp4'
		dvi.addVideoInfoForVideoIndex(videoIndex=videoIndex,
		                              videoTitle=title_1,
		                              videoUrl=url_1,
		                              downloadedFileName=videoFileName_1)
		videoIndex += 1
		title_2 = 'title 2'
		url_2 = 'https://youtube.com/watch?v=9iPvL8880999'
		videoFileName_2 = 'title 2.mp4'
		dvi.addVideoInfoForVideoIndex(videoIndex=videoIndex,
		                              videoTitle=title_2,
		                              videoUrl=url_2,
		                              downloadedFileName=videoFileName_2)
		
		self.assertEqual(url_1, dvi.getVideoUrlForVideoTitle(title_1))
		self.assertEqual(url_1, dvi.getVideoUrlForVideoIndex(1))
		self.assertEqual(url_2, dvi.getVideoUrlForVideoTitle(title_2))
		self.assertEqual(url_2, dvi.getVideoUrlForVideoIndex(2))

		self.assertEqual(additionTimeStr, dvi.getVideoDownloadTimeForVideoTitle(title_1))
		self.assertEqual(additionTimeStr, dvi.getVideoDownloadTimeForVideoTitle(title_2))

		self.assertEqual(title_1, dvi.getVideoTitleForVideoIndex(1))

		self.assertEqual(videoFileName_1, dvi.getVideoFileNameForVideoIndex(1))
		self.assertEqual(videoFileName_1, dvi.getVideoFileNameForVideoTitle(title_1))
		self.assertEqual(videoFileName_2, dvi.getVideoFileNameForVideoIndex(2))
		self.assertEqual(videoFileName_2, dvi.getVideoFileNameForVideoTitle(title_2))

		self.assertIsNone(dvi.getExtractStartEndSecondsListsForVideoIndex(videoIndex=1))
		self.assertIsNone(dvi.getSuppressStartEndSecondsListsForVideoIndex(videoIndex=1))
		self.assertIsNone(dvi.getExtractStartEndSecondsListsForVideoIndex(videoIndex=2))
		self.assertIsNone(dvi.getSuppressStartEndSecondsListsForVideoIndex(videoIndex=2))
		
		self.assertEqual(3, dvi.getNextVideoIndex())
		self.assertEqual(playlistUrl, dvi.getPlaylistUrl())

	def testAddVideoInfoForVideoIndex_existing_info_dic_file(self):
		playlistUrl = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS'
		playListName = 'test_download_vid_info_dic'
		playlistTitle = playListName
		
		audioDirRoot = DirUtil.getTestAudioRootPath()
		downloadDir = audioDirRoot + sep + playListName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting video info dic file
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		# creating new video info dic file and saving it
		
		dvi = DownloadVideoInfoDic(playlistUrl=playlistUrl,
		                           audioRootDir=audioDirRoot,
		                           playlistDownloadRootPath=audioDirRoot,
		                           originalPaylistTitle=playlistTitle,
		                           originalPlaylistName=playListName,
		                           modifiedPlaylistTitle=playlistTitle,
		                           modifiedPlaylistName=playListName)
		additionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_VIDEO_INFO_FILE)
		videoIndex = dvi.getNextVideoIndex()
		dvi.addVideoInfoForVideoIndex(videoIndex, 'title 1', 'https://youtube.com/watch?v=9iPvLx7gotk', 'title 1.mp4')
		videoIndex += 1
		dvi.addVideoInfoForVideoIndex(videoIndex, 'title 2', 'https://youtube.com/watch?v=9iPvL8880999', 'title 2.mp4')
		
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', dvi.getVideoUrlForVideoTitle('title 1'))
		self.assertEqual('https://youtube.com/watch?v=9iPvL8880999', dvi.getVideoUrlForVideoTitle('title 2'))

		self.assertEqual(additionTimeStr, dvi.getVideoDownloadTimeForVideoTitle('title 1'))
		self.assertEqual(additionTimeStr, dvi.getVideoDownloadTimeForVideoTitle('title 2'))

		self.assertEqual('title 1', dvi.getVideoTitleForVideoIndex(1))

		self.assertEqual('title 1.mp4', dvi.getVideoFileNameForVideoIndex(1))
		self.assertEqual('title 2.mp4', dvi.getVideoFileNameForVideoIndex(2))
		self.assertEqual(playlistUrl, dvi.getPlaylistUrl())

		dvi.saveDic(audioDirRoot)
		
		# creating new video info dic, reloading newly created video info dic file
		reloadedDvi = DownloadVideoInfoDic('', audioDirRoot, audioDirRoot, playlistTitle, playListName, playlistTitle, playListName)
		time.sleep(1)
		newAdditionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_VIDEO_INFO_FILE)

		# adding supplementary video info entry
		videoIndex = reloadedDvi.getNextVideoIndex()
		reloadedDvi.addVideoInfoForVideoIndex(videoIndex, 'title 3', 'https://youtube.com/watch?v=9iPvL1111', 'title 3.mp4')

		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', reloadedDvi.getVideoUrlForVideoTitle('title 1'))
		self.assertEqual('https://youtube.com/watch?v=9iPvL8880999', reloadedDvi.getVideoUrlForVideoTitle('title 2'))
		self.assertEqual('https://youtube.com/watch?v=9iPvL1111', reloadedDvi.getVideoUrlForVideoTitle('title 3'))

		self.assertEqual(additionTimeStr, reloadedDvi.getVideoDownloadTimeForVideoTitle('title 1'))
		self.assertEqual(additionTimeStr, reloadedDvi.getVideoDownloadTimeForVideoTitle('title 2'))
		self.assertEqual(newAdditionTimeStr, reloadedDvi.getVideoDownloadTimeForVideoTitle('title 3'))

		self.assertEqual('title 3', reloadedDvi.getVideoTitleForVideoIndex(3))
		self.assertEqual('title 3.mp4', reloadedDvi.getVideoFileNameForVideoIndex(3))
		self.assertEqual(4, reloadedDvi.getNextVideoIndex())
		self.assertEqual(playlistUrl, reloadedDvi.getPlaylistUrl())

		reloadedDvi.saveDic(audioDirRoot)

		# creating new extended video info dic, reloading newly created video info dic file
		newReloadedDvi = DownloadVideoInfoDic(playlistUrl, audioDirRoot, audioDirRoot, playlistTitle, playListName, playlistTitle, playListName)

		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', newReloadedDvi.getVideoUrlForVideoTitle('title 1'))
		self.assertEqual('https://youtube.com/watch?v=9iPvL8880999', newReloadedDvi.getVideoUrlForVideoTitle('title 2'))
		self.assertEqual('https://youtube.com/watch?v=9iPvL1111', newReloadedDvi.getVideoUrlForVideoTitle('title 3'))

		self.assertEqual(additionTimeStr, newReloadedDvi.getVideoDownloadTimeForVideoTitle('title 1'))
		self.assertEqual(additionTimeStr, newReloadedDvi.getVideoDownloadTimeForVideoTitle('title 2'))
		self.assertEqual(newAdditionTimeStr, newReloadedDvi.getVideoDownloadTimeForVideoTitle('title 3'))

		self.assertEqual('title 3', newReloadedDvi.getVideoTitleForVideoIndex(3))

		self.assertEqual('title 3.mp4', reloadedDvi.getVideoFileNameForVideoIndex(3))

		self.assertIsNone(newReloadedDvi.getExtractStartEndSecondsListsForVideoIndex(videoIndex=1))
		self.assertIsNone(newReloadedDvi.getSuppressStartEndSecondsListsForVideoIndex(videoIndex=1))
		self.assertIsNone(newReloadedDvi.getExtractStartEndSecondsListsForVideoIndex(videoIndex=2))
		self.assertIsNone(newReloadedDvi.getSuppressStartEndSecondsListsForVideoIndex(videoIndex=2))
		self.assertIsNone(newReloadedDvi.getExtractStartEndSecondsListsForVideoIndex(videoIndex=3))
		self.assertIsNone(newReloadedDvi.getSuppressStartEndSecondsListsForVideoIndex(videoIndex=3))

		self.assertEqual(4, newReloadedDvi.getNextVideoIndex())
		self.assertEqual(playlistUrl, newReloadedDvi.getPlaylistUrl())

	def testAddExtractAndSuppressStartEndSecondsList_existing_info_dic_file(self):
		testDirName = 'test delete files'
		testDirNameSaved = 'test delete files save dir'
		existingDownloadVideoInfoDicFileName = 'Test download three short videos_dic.txt'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		testPath = testAudioDirRoot + sep + testDirName
		testPathSaved = testAudioDirRoot + sep + testDirNameSaved
		existingDownloadVideoInfoDicFilePathName = testPath + sep + existingDownloadVideoInfoDicFileName

		# restoring test dir
		
		if os.path.exists(testPath):
			shutil.rmtree(testPath)

		shutil.copytree(testPathSaved, testPath)
		dicFileNameLst = DirUtil.getFilePathNamesInDirForPattern(testPath, '*.txt')
		
		dvi = DownloadVideoInfoDic(playlistUrl=None,
		                           audioRootDir=None,
		                           playlistDownloadRootPath=None,
		                           originalPaylistTitle=None,
		                           originalPlaylistName=None,
		                           modifiedPlaylistTitle=None,
		                           modifiedPlaylistName=None,
		                           loadDicIfDicFileExist=True,
		                           existingDicFilePathName=dicFileNameLst[0])

		self.assertIsNotNone(dvi)
		
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk',
		                 dvi.getVideoUrlForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                 dvi.getVideoUrlForVideoTitle('Here to help: Give him what he wants'))
		self.assertEqual('https://www.youtube.com/watch?v=vU1NEZ9sTOM',
		                 dvi.getVideoUrlForVideoTitle('Funny suspicious looking dog'))
		

	def testAddExtractedFileInfoForVideoIndex_existing_info_dic_file(self):
		playlistUrl = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS'
		playListName = 'test_download_vid_info_dic'
		playlistTitle = playListName
		
		audioDirRoot = DirUtil.getTestAudioRootPath()
		downloadDir = audioDirRoot + sep + playListName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting video info dic file
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		# creating new video info dic file and saving it
		
		dvi = DownloadVideoInfoDic(playlistUrl, audioDirRoot, audioDirRoot, playlistTitle, playListName, playlistTitle, playListName)
		additionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_VIDEO_INFO_FILE)
		dvi.addVideoInfoForVideoIndex(1, 'title 1', 'https://youtube.com/watch?v=9iPvLx7gotk', 'title 1.mp4')
		
		self.assertEqual('title 1.mp4', dvi.getVideoFileNameForVideoIndex(1))
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', dvi.getVideoUrlForVideoTitle('title 1'))
		self.assertEqual(additionTimeStr, dvi.getVideoDownloadTimeForVideoTitle('title 1'))
		
		startEndSecondsList_one = [1, 10]
		startEndSecondsList_two = [15, 20]
		
		dvi.addExtractStartEndSecondsListForVideoIndex(1, startEndSecondsList_one)
		dvi.addExtractStartEndSecondsListForVideoIndex(1, startEndSecondsList_two)
		dvi.addSuppressStartEndSecondsListForVideoIndex(1, startEndSecondsList_two)
		dvi.addSuppressStartEndSecondsListForVideoIndex(1, startEndSecondsList_one)
		
		self.assertEqual([startEndSecondsList_one, startEndSecondsList_two],
		                 dvi.getExtractStartEndSecondsListsForVideoIndex(1))
		self.assertEqual([startEndSecondsList_two, startEndSecondsList_one],
		                 dvi.getSuppressStartEndSecondsListsForVideoIndex(1))
		
		HHMMSS_TimeFrameList_1_1 = ['0:23:45', '0:24:54']
		extractedMp3FileName_1_1 = 'title 1_1.mp3'
		dvi.addExtractedFileInfoForVideoIndexTimeFrameIndex(1,
		                                                    1,
		                                                    extractedMp3FileName_1_1,
		                                                    HHMMSS_TimeFrameList_1_1)
		HHMMSS_TimeFrameList_1_2 = ['0:25:45', '1:24:54']
		extractedMp3FileName_1_2 = 'title 1_2.mp3'
		dvi.addExtractedFileInfoForVideoIndexTimeFrameIndex(1,
		                                                    2,
		                                                    extractedMp3FileName_1_2,
		                                                    HHMMSS_TimeFrameList_1_2)

		self.assertEqual(HHMMSS_TimeFrameList_1_1, dvi.getStartEndHHMMSS_TimeFrameForExtractedFileName(1, extractedMp3FileName_1_1))
		self.assertEqual(HHMMSS_TimeFrameList_1_2, dvi.getStartEndHHMMSS_TimeFrameForExtractedFileName(1, extractedMp3FileName_1_2))
		self.assertEqual(playlistUrl, dvi.getPlaylistUrl())

		dvi.saveDic(audioDirRoot)
		
		# creating new video info dic, reloading newly created video info dic file
		reloadedDvi = DownloadVideoInfoDic('', audioDirRoot, audioDirRoot, playlistTitle, playListName, playlistTitle, playListName)
		
		self.assertEqual('title 1.mp4', reloadedDvi.getVideoFileNameForVideoIndex(1))
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', reloadedDvi.getVideoUrlForVideoTitle('title 1'))
		self.assertEqual(additionTimeStr, reloadedDvi.getVideoDownloadTimeForVideoTitle('title 1'))
		
		self.assertEqual([startEndSecondsList_one, startEndSecondsList_two],
		                 reloadedDvi.getExtractStartEndSecondsListsForVideoIndex(1))
		self.assertEqual([startEndSecondsList_two, startEndSecondsList_one],
		                 reloadedDvi.getSuppressStartEndSecondsListsForVideoIndex(1))

		self.assertEqual(HHMMSS_TimeFrameList_1_1, reloadedDvi.getStartEndHHMMSS_TimeFrameForExtractedFileName(1, extractedMp3FileName_1_1))
		self.assertEqual(HHMMSS_TimeFrameList_1_2, reloadedDvi.getStartEndHHMMSS_TimeFrameForExtractedFileName(1, extractedMp3FileName_1_2))
		self.assertEqual(playlistUrl, reloadedDvi.getPlaylistUrl())

	def testAddSuppressedFileInfoForVideoIndex_existing_info_dic_file(self):
		playlistUrl = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS'
		playListName = 'test_download_vid_info_dic'
		playlistTitle = playListName
		
		audioDirRoot = DirUtil.getTestAudioRootPath()
		downloadDir = audioDirRoot + sep + playListName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting video info dic file
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		# creating new video info dic file and saving it
		
		dvi = DownloadVideoInfoDic(playlistUrl, audioDirRoot, audioDirRoot, playlistTitle, playListName, playlistTitle, playListName)
		additionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_VIDEO_INFO_FILE)
		dvi.addVideoInfoForVideoIndex(1, 'title 1', 'https://youtube.com/watch?v=9iPvLx7gotk', 'title 1.mp4')
		
		self.assertEqual('title 1.mp4', dvi.getVideoFileNameForVideoIndex(1))
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', dvi.getVideoUrlForVideoTitle('title 1'))
		self.assertEqual(additionTimeStr, dvi.getVideoDownloadTimeForVideoTitle('title 1'))
		
		startEndSecondsList_one = [1, 10]
		startEndSecondsList_two = [15, 20]
		
		dvi.addExtractStartEndSecondsListForVideoIndex(1, startEndSecondsList_one)
		dvi.addExtractStartEndSecondsListForVideoIndex(1, startEndSecondsList_two)
		dvi.addSuppressStartEndSecondsListForVideoIndex(1, startEndSecondsList_two)
		dvi.addSuppressStartEndSecondsListForVideoIndex(1, startEndSecondsList_one)
		
		self.assertEqual([startEndSecondsList_one, startEndSecondsList_two],
		                 dvi.getExtractStartEndSecondsListsForVideoIndex(1))
		self.assertEqual([startEndSecondsList_two, startEndSecondsList_one],
		                 dvi.getSuppressStartEndSecondsListsForVideoIndex(1))
		
		HHMMSS_TimeFrameList_1_1 = ['0:23:45', '0:24:54']
		extractedMp3FileName_1_1 = 'title 1_1.mp3'
		dvi.addExtractedFileInfoForVideoIndexTimeFrameIndex(1,
		                                                    1,
		                                                    extractedMp3FileName_1_1,
		                                                    HHMMSS_TimeFrameList_1_1)
		HHMMSS_TimeFrameList_1_2 = ['0:25:45', '1:24:54']
		extractedMp3FileName_1_2 = 'title 1_2.mp3'
		dvi.addExtractedFileInfoForVideoIndexTimeFrameIndex(1,
		                                                    2,
		                                                    extractedMp3FileName_1_2,
		                                                    HHMMSS_TimeFrameList_1_2)
		
		self.assertEqual(HHMMSS_TimeFrameList_1_1,
		                 dvi.getStartEndHHMMSS_TimeFrameForExtractedFileName(1, extractedMp3FileName_1_1))
		self.assertEqual(HHMMSS_TimeFrameList_1_2,
		                 dvi.getStartEndHHMMSS_TimeFrameForExtractedFileName(1, extractedMp3FileName_1_2))
		
		suppressFileName = 'title_1_s.mp3'
		suppressTimeFrameList = ['0:23:45-0:24:54', '1:03:45-1:24:54']
		keptTimeFrameList = ['0:0:0-0:23:45', '0:24:54-1:03:45', '1:24:54-1:55:12']
		dvi.addSuppressedFileInfoForVideoIndex(1, suppressFileName, suppressTimeFrameList, keptTimeFrameList)
		
		self.assertEqual(suppressFileName, dvi.getSuppressedFileNameForVideoIndex(1))
		self.assertEqual(suppressTimeFrameList, dvi.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(1))
		self.assertEqual(keptTimeFrameList, dvi.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(1))
		self.assertEqual(playlistUrl, dvi.getPlaylistUrl())

		dvi.saveDic(audioDirRoot)
		
		# creating new video info dic, reloading newly created video info dic file
		reloadedDvi = DownloadVideoInfoDic('', audioDirRoot, audioDirRoot, playlistTitle, playListName, playlistTitle, playListName)
		
		self.assertEqual('title 1.mp4', reloadedDvi.getVideoFileNameForVideoIndex(1))
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', reloadedDvi.getVideoUrlForVideoTitle('title 1'))
		self.assertEqual(additionTimeStr, reloadedDvi.getVideoDownloadTimeForVideoTitle('title 1'))
		
		self.assertEqual([startEndSecondsList_one, startEndSecondsList_two],
		                 reloadedDvi.getExtractStartEndSecondsListsForVideoIndex(1))
		self.assertEqual([startEndSecondsList_two, startEndSecondsList_one],
		                 reloadedDvi.getSuppressStartEndSecondsListsForVideoIndex(1))
		
		self.assertEqual(HHMMSS_TimeFrameList_1_1,
		                 reloadedDvi.getStartEndHHMMSS_TimeFrameForExtractedFileName(1, extractedMp3FileName_1_1))
		self.assertEqual(HHMMSS_TimeFrameList_1_2,
		                 reloadedDvi.getStartEndHHMMSS_TimeFrameForExtractedFileName(1, extractedMp3FileName_1_2))
		
		self.assertEqual(suppressFileName, reloadedDvi.getSuppressedFileNameForVideoIndex(1))
		self.assertEqual(suppressTimeFrameList, reloadedDvi.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(1))
		self.assertEqual(keptTimeFrameList, reloadedDvi.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(1))
		self.assertEqual(playlistUrl, reloadedDvi.getPlaylistUrl())

	def testRemoveFirstVideoInfoForVideoTitle(self):
		playlistUrl = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS'
		playListName = 'test_download_vid_info_dic'
		playlistTitle = playListName
		
		audioDirRoot = DirUtil.getTestAudioRootPath()
		downloadDir = audioDirRoot + sep + playListName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting video info dic files
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		dvi = DownloadVideoInfoDic(playlistUrl, audioDirRoot, audioDirRoot, playlistTitle, playListName, playlistTitle, playListName)
		
		videoIndex = dvi.getNextVideoIndex()
		title_1 = 'title 1'
		url_1 = 'https://youtube.com/watch?v=9iPvLx7gotk'
		videoFileName_1 = 'title 1.mp4'
		dvi.addVideoInfoForVideoIndex(videoIndex=videoIndex,
		                              videoTitle=title_1,
		                              videoUrl=url_1,
		                              downloadedFileName=videoFileName_1)
		videoIndex += 1
		title_2 = 'title 2'
		url_2 = 'https://youtube.com/watch?v=9iPvL8880999'
		videoFileName_2 = 'title 2.mp4'
		dvi.addVideoInfoForVideoIndex(videoIndex=videoIndex,
		                              videoTitle=title_2,
		                              videoUrl=url_2,
		                              downloadedFileName=videoFileName_2)
		
		self.assertEqual(url_1, dvi.getVideoUrlForVideoTitle(title_1))
		self.assertEqual(url_1, dvi.getVideoUrlForVideoIndex(1))
		self.assertEqual(url_2, dvi.getVideoUrlForVideoTitle(title_2))
		self.assertEqual(url_2, dvi.getVideoUrlForVideoIndex(2))
		
		dvi.removeVideoInfoForVideoTitle(title_1)
		
		# print('dvi after removing first video info')
		# print(dvi)
		
		self.assertEqual({}, dvi._getVideoInfoForVideoIndex(1))
		self.assertEqual(3, dvi.getNextVideoIndex())
		self.assertEqual(playlistUrl, dvi.getPlaylistUrl())

	def testRemoveSecondVideoInfoForVideoTitle(self):
		playlistUrl = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS'
		playListName = 'test_download_vid_info_dic'
		playlistTitle = playListName
		
		audioDirRoot = DirUtil.getTestAudioRootPath()
		downloadDir = audioDirRoot + sep + playListName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting video info dic files
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		dvi = DownloadVideoInfoDic(playlistUrl, audioDirRoot, audioDirRoot, playlistTitle, playListName, playlistTitle, playListName)
		
		videoIndex = dvi.getNextVideoIndex()
		title_1 = 'title 1'
		url_1 = 'https://youtube.com/watch?v=9iPvLx7gotk'
		videoFileName_1 = 'title 1.mp4'
		dvi.addVideoInfoForVideoIndex(videoIndex=videoIndex,
		                              videoTitle=title_1,
		                              videoUrl=url_1,
		                              downloadedFileName=videoFileName_1)
		videoIndex += 1
		title_2 = 'title 2'
		url_2 = 'https://youtube.com/watch?v=9iPvL8880999'
		videoFileName_2 = 'title 2.mp4'
		dvi.addVideoInfoForVideoIndex(videoIndex=videoIndex,
		                              videoTitle=title_2,
		                              videoUrl=url_2,
		                              downloadedFileName=videoFileName_2)
		
		self.assertEqual(url_1, dvi.getVideoUrlForVideoTitle(title_1))
		self.assertEqual(url_1, dvi.getVideoUrlForVideoIndex(1))
		self.assertEqual(url_2, dvi.getVideoUrlForVideoTitle(title_2))
		self.assertEqual(url_2, dvi.getVideoUrlForVideoIndex(2))
		
		dvi.removeVideoInfoForVideoTitle(title_2)
		
		# print('dvi after removing second video info')
		# print(dvi)
		
		self.assertEqual({}, dvi._getVideoInfoForVideoIndex(2))
		self.assertEqual(3, dvi.getNextVideoIndex())
		self.assertEqual(playlistUrl, dvi.getPlaylistUrl())

	def testRemoveVideoInfoForVideoTitle_in_empty_dic(self):
		playlistUrl = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS'
		playListName = 'test_download_vid_info_dic'
		playlistTitle = playListName
		
		audioDirRoot = DirUtil.getTestAudioRootPath()
		downloadDir = audioDirRoot + sep + playListName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting video info dic files
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		dvi = DownloadVideoInfoDic(playlistUrl, audioDirRoot, audioDirRoot, playlistTitle, playListName, playlistTitle, playListName)
		
		title_1 = 'title 1'
		
		dvi.removeVideoInfoForVideoTitle(title_1)
		
		# print('dvi after removing video info in empty dic')
		# print(dvi)
		
		self.assertEqual({}, dvi._getVideoInfoForVideoIndex(1))
		self.assertEqual(1, dvi.getNextVideoIndex())
		self.assertEqual(playlistUrl, dvi.getPlaylistUrl())

	def testRemoveVideoInfoForBadVideoTitle(self):
		playlistUrl = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS'
		playListName = 'test_download_vid_info_dic'
		playlistTitle = playListName
		
		audioDirRoot = DirUtil.getTestAudioRootPath()
		downloadDir = audioDirRoot + sep + playListName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting video info dic files
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		dvi = DownloadVideoInfoDic(playlistUrl, audioDirRoot, audioDirRoot, playlistTitle, playListName, playlistTitle, playListName)
		
		videoIndex = dvi.getNextVideoIndex()
		title_1 = 'title 1'
		url_1 = 'https://youtube.com/watch?v=9iPvLx7gotk'
		videoFileName_1 = 'title 1.mp4'
		dvi.addVideoInfoForVideoIndex(videoIndex=videoIndex,
		                              videoTitle=title_1,
		                              videoUrl=url_1,
		                              downloadedFileName=videoFileName_1)
		videoIndex += 1
		title_2 = 'title 2'
		url_2 = 'https://youtube.com/watch?v=9iPvL8880999'
		videoFileName_2 = 'title 2.mp4'
		dvi.addVideoInfoForVideoIndex(videoIndex=videoIndex,
		                              videoTitle=title_2,
		                              videoUrl=url_2,
		                              downloadedFileName=videoFileName_2)
		
		self.assertEqual(url_1, dvi.getVideoUrlForVideoTitle(title_1))
		self.assertEqual(url_1, dvi.getVideoUrlForVideoIndex(1))
		self.assertEqual(url_2, dvi.getVideoUrlForVideoTitle(title_2))
		self.assertEqual(url_2, dvi.getVideoUrlForVideoIndex(2))
		
		dvi.removeVideoInfoForVideoTitle('bad title')
		
		# print('dvi after removing bad title video info')
		# print(dvi)
		
		self.assertEqual(url_1, dvi.getVideoUrlForVideoTitle(title_1))
		self.assertEqual(url_1, dvi.getVideoUrlForVideoIndex(1))
		self.assertEqual(url_2, dvi.getVideoUrlForVideoTitle(title_2))
		self.assertEqual(url_2, dvi.getVideoUrlForVideoIndex(2))
		self.assertEqual(3, dvi.getNextVideoIndex())
		self.assertEqual(playlistUrl, dvi.getPlaylistUrl())

	def testRemoveFirstVideoInfoForVideoIndex(self):
		playlistUrl = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS'
		playListName = 'test_download_vid_info_dic'
		playlistTitle = playListName
		
		audioDirRoot = DirUtil.getTestAudioRootPath()
		downloadDir = audioDirRoot + sep + playListName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting video info dic files
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		dvi = DownloadVideoInfoDic(playlistUrl, audioDirRoot, audioDirRoot, playlistTitle, playListName, playlistTitle, playListName)
		
		videoIndex = dvi.getNextVideoIndex()
		title_1 = 'title 1'
		url_1 = 'https://youtube.com/watch?v=9iPvLx7gotk'
		videoFileName_1 = 'title 1.mp4'
		dvi.addVideoInfoForVideoIndex(videoIndex=videoIndex,
		                              videoTitle=title_1,
		                              videoUrl=url_1,
		                              downloadedFileName=videoFileName_1)
		videoIndex += 1
		title_2 = 'title 2'
		url_2 = 'https://youtube.com/watch?v=9iPvL8880999'
		videoFileName_2 = 'title 2.mp4'
		dvi.addVideoInfoForVideoIndex(videoIndex=videoIndex,
		                              videoTitle=title_2,
		                              videoUrl=url_2,
		                              downloadedFileName=videoFileName_2)
		
		self.assertEqual(url_1, dvi.getVideoUrlForVideoTitle(title_1))
		self.assertEqual(url_1, dvi.getVideoUrlForVideoIndex(1))
		self.assertEqual(url_2, dvi.getVideoUrlForVideoTitle(title_2))
		self.assertEqual(url_2, dvi.getVideoUrlForVideoIndex(2))
		
		dvi.removeVideoInfoForVideoIndex(1)
		
		self.assertEqual({}, dvi._getVideoInfoForVideoIndex(1))
		self.assertEqual(3, dvi.getNextVideoIndex())
		self.assertEqual(playlistUrl, dvi.getPlaylistUrl())

	def testRemoveSecondVideoInfoForVideoIndex(self):
		playlistUrl = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS'
		playListName = 'test_download_vid_info_dic'
		playlistTitle = playListName
		
		audioDirRoot = DirUtil.getTestAudioRootPath()
		downloadDir = audioDirRoot + sep + playListName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting video info dic files
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		dvi = DownloadVideoInfoDic(playlistUrl, audioDirRoot, audioDirRoot, playlistTitle, playListName, playlistTitle, playListName)
		
		videoIndex = dvi.getNextVideoIndex()
		title_1 = 'title 1'
		url_1 = 'https://youtube.com/watch?v=9iPvLx7gotk'
		videoFileName_1 = 'title 1.mp4'
		dvi.addVideoInfoForVideoIndex(videoIndex=videoIndex,
		                              videoTitle=title_1,
		                              videoUrl=url_1,
		                              downloadedFileName=videoFileName_1)
		videoIndex += 1
		title_2 = 'title 2'
		url_2 = 'https://youtube.com/watch?v=9iPvL8880999'
		videoFileName_2 = 'title 2.mp4'
		dvi.addVideoInfoForVideoIndex(videoIndex=videoIndex,
		                              videoTitle=title_2,
		                              videoUrl=url_2,
		                              downloadedFileName=videoFileName_2)
		
		self.assertEqual(url_1, dvi.getVideoUrlForVideoTitle(title_1))
		self.assertEqual(url_1, dvi.getVideoUrlForVideoIndex(1))
		self.assertEqual(url_2, dvi.getVideoUrlForVideoTitle(title_2))
		self.assertEqual(url_2, dvi.getVideoUrlForVideoIndex(2))
		
		dvi.removeVideoInfoForVideoIndex(2)
		
		# print('dvi after removing second video info')
		# print(dvi)
		
		self.assertEqual({}, dvi._getVideoInfoForVideoIndex(2))
		self.assertEqual(3, dvi.getNextVideoIndex())
		self.assertEqual(playlistUrl, dvi.getPlaylistUrl())

	def testRemoveVideoInfoForBadVideoIndex(self):
		playlistUrl = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS'
		playListName = 'test_download_vid_info_dic'
		playlistTitle = playListName
		
		audioDirRoot = DirUtil.getTestAudioRootPath()
		downloadDir = audioDirRoot + sep + playListName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting video info dic files
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		dvi = DownloadVideoInfoDic(playlistUrl, audioDirRoot, audioDirRoot, playlistTitle, playListName, playlistTitle, playListName)
		
		videoIndex = dvi.getNextVideoIndex()
		title_1 = 'title 1'
		url_1 = 'https://youtube.com/watch?v=9iPvLx7gotk'
		videoFileName_1 = 'title 1.mp4'
		dvi.addVideoInfoForVideoIndex(videoIndex=videoIndex,
		                              videoTitle=title_1,
		                              videoUrl=url_1,
		                              downloadedFileName=videoFileName_1)
		videoIndex += 1
		title_2 = 'title 2'
		url_2 = 'https://youtube.com/watch?v=9iPvL8880999'
		videoFileName_2 = 'title 2.mp4'
		dvi.addVideoInfoForVideoIndex(videoIndex=videoIndex,
		                              videoTitle=title_2,
		                              videoUrl=url_2,
		                              downloadedFileName=videoFileName_2)
		
		self.assertEqual(url_1, dvi.getVideoUrlForVideoTitle(title_1))
		self.assertEqual(url_1, dvi.getVideoUrlForVideoIndex(1))
		self.assertEqual(url_2, dvi.getVideoUrlForVideoTitle(title_2))
		self.assertEqual(url_2, dvi.getVideoUrlForVideoIndex(2))
		
		dvi.removeVideoInfoForVideoIndex(100)
		
		# print('dvi after removing bad title video info')
		# print(dvi)
		
		self.assertEqual(url_1, dvi.getVideoUrlForVideoTitle(title_1))
		self.assertEqual(url_1, dvi.getVideoUrlForVideoIndex(1))
		self.assertEqual(url_2, dvi.getVideoUrlForVideoTitle(title_2))
		self.assertEqual(url_2, dvi.getVideoUrlForVideoIndex(2))
		self.assertEqual(3, dvi.getNextVideoIndex())
		self.assertEqual(playlistUrl, dvi.getPlaylistUrl())


if __name__ == '__main__':
#	unittest.main()
	tst = TestDownloadVideoInfoDic()
	tst.testAddExtractAndSuppressStartEndSecondsList_existing_info_dic_file()
