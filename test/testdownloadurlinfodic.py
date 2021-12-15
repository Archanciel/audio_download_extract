import shutil
import unittest
import os, sys, inspect, glob
from os.path import sep
from datetime import datetime

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)
		
from downloadUrlinfodic import DownloadUrlInfoDic
from constants import *
from dirutil import DirUtil
			
class TestDownloadUrlInfoDic(unittest.TestCase):
	def testAddVideoInfoForVideoIndex_new_info_dic_file(self):
		audioDirRoot = DirUtil.getTestAudioRootPath()
		downloadDir = audioDirRoot + sep + 'tst_url_info_dic_1'
		urlDicFileName = 'urlListDic'

		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting url info dic file
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		dui = DownloadUrlInfoDic(
			audioRootDir=audioDirRoot,
			urlListDicFileName=urlDicFileName,
			generalTotalDownlResultTuple=(13, 4, 7),
			generalTotalDownlSuccessTuple=(3, 5, 1, 1, 2),
			generalTotalDownlFailTuple=(0, 2, 0, 0, 2),
			generalTotalDownlSkipTuple=(1, 2, 0, 0, 4),
			loadDicIfDicFileExist=True,
			existingDicFilePathName=None)
		urlTitle_1 = 'test warning index date files_noIndexNoDate'
		url_1 = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRVKblKqskAyseCgsUmhlSc'
		dui.addUrlInfo(urlType=DownloadUrlInfoDic.URL_TYPE_PLAYLIST, urlTitle=urlTitle_1, url=url_1, downloadDir='')
		urlTitle_2 = 'Here to help: Give him what he wants'
		url_2 = 'https://www.youtube.com/watch?v=Eqy6M6qLWGw'
		dui.addUrlInfo(urlType=DownloadUrlInfoDic.URL_TYPE_SINGLE_VIDEO, urlTitle=urlTitle_2, url=url_2, downloadDir='')
		dui.saveDic(downloadDir)
		additionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_DOWNLOAD_DIC_FILE)

		
		self.assertEqual(url_1, dui.getUrlForUrlTitle(urlTitle_1))
		self.assertEqual(url_1, dui.getUrlForUrlIndex(1))
		self.assertEqual(url_1, dui.getUrlForUrlKey('1'))
		self.assertEqual(url_2, dui.getUrlForUrlTitle(urlTitle_2))
		self.assertEqual(url_2, dui.getUrlForUrlIndex(2))
		self.assertEqual(url_2, dui.getUrlForUrlKey('2'))

		self.assertEqual(additionTimeStr, dui.getVideoDownloadTimeForVideoTitle(urlTitle_1))
		self.assertEqual(additionTimeStr, dui.getVideoDownloadTimeForVideoTitle(urlTitle_2))

		self.assertEqual(urlTitle_1, dui.getUrlTitleForUrlIndex(1))

		self.assertEqual('', dui.getUrlDownloadDirForUrlIndex(1))
		self.assertEqual('', dui.getUrlDownloadDirForUrlTitle(urlTitle_1))
		self.assertEqual('', dui.getUrlDownloadDirForUrlIndex(2))
		self.assertEqual('', dui.getUrlDownloadDirForUrlTitle(urlTitle_2))
		
		self.assertEqual(3, dui.getNextUrlIndex())

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
		
		dvi = DownloadUrlInfoDic(playlistUrl, audioDirRoot, audioDirRoot, playlistTitle, playListName, playlistTitle, playListName)
		
		videoIndex = dvi.getNextUrlIndex()
		title_1 = 'title 1'
		url_1 = 'https://youtube.com/watch?v=9iPvLx7gotk'
		videoFileName_1 = 'title 1.mp4'
		dvi.addUrlInfo(urlType='', urlTitle=title_1, url=url_1, downloadDir=videoFileName_1)
		videoIndex += 1
		title_2 = 'title 2'
		url_2 = 'https://youtube.com/watch?v=9iPvL8880999'
		videoFileName_2 = 'title 2.mp4'
		dvi.addUrlInfo(urlType='', urlTitle=title_2, url=url_2, downloadDir=videoFileName_2)
		
		self.assertEqual(url_1, dvi.getUrlForUrlTitle(title_1))
		self.assertEqual(url_1, dvi.getUrlForUrlIndex(1))
		self.assertEqual(url_2, dvi.getUrlForUrlTitle(title_2))
		self.assertEqual(url_2, dvi.getUrlForUrlIndex(2))
		
		dvi.removeVideoInfoForVideoTitle(title_1)
		
		# print('dvi after removing first video info')
		# print(dvi)
		
		self.assertEqual({}, dvi._getUrlInfoForUrlIndex(1))
		self.assertEqual(3, dvi.getNextUrlIndex())
		self.assertEqual(playlistUrl, dvi.getTotalDownloadResultTuple())

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
		
		dvi = DownloadUrlInfoDic(playlistUrl, audioDirRoot, audioDirRoot, playlistTitle, playListName, playlistTitle, playListName)
		
		videoIndex = dvi.getNextUrlIndex()
		title_1 = 'title 1'
		url_1 = 'https://youtube.com/watch?v=9iPvLx7gotk'
		videoFileName_1 = 'title 1.mp4'
		dvi.addUrlInfo(urlType='', urlTitle=title_1, url=url_1, downloadDir=videoFileName_1)
		videoIndex += 1
		title_2 = 'title 2'
		url_2 = 'https://youtube.com/watch?v=9iPvL8880999'
		videoFileName_2 = 'title 2.mp4'
		dvi.addUrlInfo(urlType='', urlTitle=title_2, url=url_2, downloadDir=videoFileName_2)
		
		self.assertEqual(url_1, dvi.getUrlForUrlTitle(title_1))
		self.assertEqual(url_1, dvi.getUrlForUrlIndex(1))
		self.assertEqual(url_2, dvi.getUrlForUrlTitle(title_2))
		self.assertEqual(url_2, dvi.getUrlForUrlIndex(2))
		
		dvi.removeVideoInfoForVideoTitle(title_2)
		
		# print('dvi after removing second video info')
		# print(dvi)
		
		self.assertEqual({}, dvi._getUrlInfoForUrlIndex(2))
		self.assertEqual(3, dvi.getNextUrlIndex())
		self.assertEqual(playlistUrl, dvi.getTotalDownloadResultTuple())

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
		
		dvi = DownloadUrlInfoDic(playlistUrl, audioDirRoot, audioDirRoot, playlistTitle, playListName, playlistTitle, playListName)
		
		title_1 = 'title 1'
		
		dvi.removeVideoInfoForVideoTitle(title_1)
		
		# print('dvi after removing video info in empty dic')
		# print(dvi)
		
		self.assertEqual({}, dvi._getUrlInfoForUrlIndex(1))
		self.assertEqual(1, dvi.getNextUrlIndex())
		self.assertEqual(playlistUrl, dvi.getTotalDownloadResultTuple())

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
		
		dvi = DownloadUrlInfoDic(playlistUrl, audioDirRoot, audioDirRoot, playlistTitle, playListName, playlistTitle, playListName)
		
		videoIndex = dvi.getNextUrlIndex()
		title_1 = 'title 1'
		url_1 = 'https://youtube.com/watch?v=9iPvLx7gotk'
		videoFileName_1 = 'title 1.mp4'
		dvi.addUrlInfo(urlType='', urlTitle=title_1, url=url_1, downloadDir=videoFileName_1)
		videoIndex += 1
		title_2 = 'title 2'
		url_2 = 'https://youtube.com/watch?v=9iPvL8880999'
		videoFileName_2 = 'title 2.mp4'
		dvi.addUrlInfo(urlType='', urlTitle=title_2, url=url_2, downloadDir=videoFileName_2)
		
		self.assertEqual(url_1, dvi.getUrlForUrlTitle(title_1))
		self.assertEqual(url_1, dvi.getUrlForUrlIndex(1))
		self.assertEqual(url_2, dvi.getUrlForUrlTitle(title_2))
		self.assertEqual(url_2, dvi.getUrlForUrlIndex(2))
		
		dvi.removeVideoInfoForVideoTitle('bad title')
		
		# print('dvi after removing bad title video info')
		# print(dvi)
		
		self.assertEqual(url_1, dvi.getUrlForUrlTitle(title_1))
		self.assertEqual(url_1, dvi.getUrlForUrlIndex(1))
		self.assertEqual(url_2, dvi.getUrlForUrlTitle(title_2))
		self.assertEqual(url_2, dvi.getUrlForUrlIndex(2))
		self.assertEqual(3, dvi.getNextUrlIndex())
		self.assertEqual(playlistUrl, dvi.getTotalDownloadResultTuple())

	def testRemoveVideoInfoForVideoIndex_first_added_video(self):
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
		
		dvi = DownloadUrlInfoDic(playlistUrl, audioDirRoot, audioDirRoot, playlistTitle, playListName, playlistTitle, playListName)
		
		videoIndex = dvi.getNextUrlIndex()
		title_1 = 'title 1'
		url_1 = 'https://youtube.com/watch?v=9iPvLx7gotk'
		videoFileName_1 = 'title 1.mp4'
		dvi.addUrlInfo(urlType='', urlTitle=title_1, url=url_1, downloadDir=videoFileName_1)
		videoIndex += 1
		title_2 = 'title 2'
		url_2 = 'https://youtube.com/watch?v=9iPvL8880999'
		videoFileName_2 = 'title 2.mp4'
		dvi.addUrlInfo(urlType='', urlTitle=title_2, url=url_2, downloadDir=videoFileName_2)
		
		self.assertEqual(url_1, dvi.getUrlForUrlTitle(title_1))
		self.assertEqual(url_1, dvi.getUrlForUrlIndex(1))
		self.assertEqual(url_2, dvi.getUrlForUrlTitle(title_2))
		self.assertEqual(url_2, dvi.getUrlForUrlIndex(2))
		
		dvi.removeVideoInfoForVideoIndex(1)
		
		self.assertEqual({}, dvi._getUrlInfoForUrlIndex(1))
		self.assertEqual(3, dvi.getNextUrlIndex())
		self.assertEqual(playlistUrl, dvi.getTotalDownloadResultTuple())

	def testRemoveVideoInfoForVideoIndex_second_added_video(self):
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
		
		dvi = DownloadUrlInfoDic(playlistUrl, audioDirRoot, audioDirRoot, playlistTitle, playListName, playlistTitle, playListName)
		
		videoIndex = dvi.getNextUrlIndex()
		title_1 = 'title 1'
		url_1 = 'https://youtube.com/watch?v=9iPvLx7gotk'
		videoFileName_1 = 'title 1.mp4'
		dvi.addUrlInfo(urlType='', urlTitle=title_1, url=url_1, downloadDir=videoFileName_1)
		videoIndex += 1
		title_2 = 'title 2'
		url_2 = 'https://youtube.com/watch?v=9iPvL8880999'
		videoFileName_2 = 'title 2.mp4'
		dvi.addUrlInfo(urlType='', urlTitle=title_2, url=url_2, downloadDir=videoFileName_2)
		
		self.assertEqual(url_1, dvi.getUrlForUrlTitle(title_1))
		self.assertEqual(url_1, dvi.getUrlForUrlIndex(1))
		self.assertEqual(url_2, dvi.getUrlForUrlTitle(title_2))
		self.assertEqual(url_2, dvi.getUrlForUrlIndex(2))
		
		dvi.removeVideoInfoForVideoIndex(2)
		
		# print('dvi after removing second video info')
		# print(dvi)
		
		self.assertEqual({}, dvi._getUrlInfoForUrlIndex(2))
		self.assertEqual(3, dvi.getNextUrlIndex())
		self.assertEqual(playlistUrl, dvi.getTotalDownloadResultTuple())

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
		
		dvi = DownloadUrlInfoDic(playlistUrl, audioDirRoot, audioDirRoot, playlistTitle, playListName, playlistTitle, playListName)
		
		videoIndex = dvi.getNextUrlIndex()
		title_1 = 'title 1'
		url_1 = 'https://youtube.com/watch?v=9iPvLx7gotk'
		videoFileName_1 = 'title 1.mp4'
		dvi.addUrlInfo(urlType='', urlTitle=title_1, url=url_1, downloadDir=videoFileName_1)
		videoIndex += 1
		title_2 = 'title 2'
		url_2 = 'https://youtube.com/watch?v=9iPvL8880999'
		videoFileName_2 = 'title 2.mp4'
		dvi.addUrlInfo(urlType='', urlTitle=title_2, url=url_2, downloadDir=videoFileName_2)
		
		self.assertEqual(url_1, dvi.getUrlForUrlTitle(title_1))
		self.assertEqual(url_1, dvi.getUrlForUrlIndex(1))
		self.assertEqual(url_2, dvi.getUrlForUrlTitle(title_2))
		self.assertEqual(url_2, dvi.getUrlForUrlIndex(2))
		
		dvi.removeVideoInfoForVideoIndex(100)
		
		# print('dvi after removing bad title video info')
		# print(dvi)
		
		self.assertEqual(url_1, dvi.getUrlForUrlTitle(title_1))
		self.assertEqual(url_1, dvi.getUrlForUrlIndex(1))
		self.assertEqual(url_2, dvi.getUrlForUrlTitle(title_2))
		self.assertEqual(url_2, dvi.getUrlForUrlIndex(2))
		self.assertEqual(3, dvi.getNextUrlIndex())
		self.assertEqual(playlistUrl, dvi.getTotalDownloadResultTuple())
	
	def testLoadExistingDownloadUrlInfoDic_specifying_only_info_dic_filePathName(self):
		audioDirRoot = DirUtil.getTestAudioRootPath()
		downloadDir = audioDirRoot + sep + 'tst_url_info_dic_2'
		testDirNameSaved = downloadDir + sep + 'save'
		urlDicFileName = 'urlListDic'

		# deleting files in downloadDir
		
		DirUtil.deleteFilesInDirForPattern(downloadDir, '*')
		
		# restoring dic file
		
		DirUtil.copyFilesInDirToDirForPattern(sourceDir=testDirNameSaved,
		                                      targetDir=downloadDir,
		                                      fileNamePattern='*')

		urlTitle_1 = 'test warning index date files_noIndexNoDate'
		url_1 = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRVKblKqskAyseCgsUmhlSc'
		urlTitle_2 = 'Here to help: Give him what he wants'
		url_2 = 'https://www.youtube.com/watch?v=Eqy6M6qLWGw'
		
		dicFilePathNameLst = DirUtil.getFilePathNamesInDirForPattern(downloadDir, '*' + DownloadUrlInfoDic.DIC_FILE_NAME_EXTENT)
		dui = DownloadUrlInfoDic(existingDicFilePathName=dicFilePathNameLst[0])
		
		self.assertEqual(url_1, dui.getUrlForUrlTitle(urlTitle_1))
		self.assertEqual(url_1, dui.getUrlForUrlIndex(1))
		self.assertEqual(url_1, dui.getUrlForUrlKey('1'))
		self.assertEqual(url_2, dui.getUrlForUrlTitle(urlTitle_2))
		self.assertEqual(url_2, dui.getUrlForUrlIndex(2))
		self.assertEqual(url_2, dui.getUrlForUrlKey('2'))

		additionTimeStr = '14/12/2021 18:30:55'
		self.assertEqual(additionTimeStr, dui.getVideoDownloadTimeForVideoTitle(urlTitle_1))
		self.assertEqual(additionTimeStr, dui.getVideoDownloadTimeForVideoTitle(urlTitle_2))
		
		self.assertEqual(urlTitle_1, dui.getUrlTitleForUrlIndex(1))
		
		self.assertEqual('', dui.getUrlDownloadDirForUrlIndex(1))
		self.assertEqual('', dui.getUrlDownloadDirForUrlTitle(urlTitle_1))
		self.assertEqual('', dui.getUrlDownloadDirForUrlIndex(2))
		self.assertEqual('', dui.getUrlDownloadDirForUrlTitle(urlTitle_2))
		
		self.assertEqual(3, dui.getNextUrlIndex())
	
	def testDeleteVideoInfoForVideoFileName(self):
		testDirName = 'test delete files'
		testDirNameSaved = 'test delete files save dir'
		
		videoTitle_1 = 'Wear a mask. Help slow the spread of Covid-19.'
		videoTitle_2 = 'Here to help: Give him what he wants'
		videoTitle_3 = 'Funny suspicious looking dog'
		
		videoFileName_1 = '99-Wear a mask. Help slow the spread of Covid-19. 2020-07-31.mp3'
		videoFileName_2 = '98-Here to help - Give him what he wants 2019-06-07.mp3'
		videoFileName_3 = '97-Funny suspicious looking dog 2013-11-05.mp3'
		videoFileName_not_exist = 'Wear a mask. Help slow the spread of Covid-19 not exist.mp3'

		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		testPath = testAudioDirRoot + sep + testDirName
		testPathSaved = testAudioDirRoot + sep + testDirNameSaved
		
		# restoring test dir
		
		if os.path.exists(testPath):
			shutil.rmtree(testPath)
		
		shutil.copytree(testPathSaved, testPath)
		
		# obtaining the download video info dic file path name
		dicFileNameLst = DirUtil.getFilePathNamesInDirForPattern(testPath, '*' + DownloadUrlInfoDic.DIC_FILE_NAME_EXTENT)
		dicFilePathName = dicFileNameLst[0]

		dvi = DownloadUrlInfoDic(existingDicFilePathName=dicFilePathName)
		
		self.assertIsNotNone(dvi)
		
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk',
		                 dvi.getUrlForUrlTitle(videoTitle_1))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                 dvi.getUrlForUrlTitle(videoTitle_2))
		self.assertEqual('https://www.youtube.com/watch?v=vU1NEZ9sTOM',
		                 dvi.getUrlForUrlTitle(videoTitle_3))

		dvi.deleteVideoInfoForVideoFileName(videoFileName_not_exist)
		
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk',
		                 dvi.getUrlForUrlTitle(videoTitle_1))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                 dvi.getUrlForUrlTitle(videoTitle_2))
		self.assertEqual('https://www.youtube.com/watch?v=vU1NEZ9sTOM',
		                 dvi.getUrlForUrlTitle(videoTitle_3))
		
		dvi.deleteVideoInfoForVideoFileName(videoFileName_2)

		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk',
		                 dvi.getUrlForUrlTitle(videoTitle_1))
		self.assertEqual(None,
		                 dvi.getUrlForUrlTitle(videoTitle_2))
		self.assertEqual('https://www.youtube.com/watch?v=vU1NEZ9sTOM',
		                 dvi.getUrlForUrlTitle(videoTitle_3))

		dvi.deleteVideoInfoForVideoFileName(videoFileName_3)

		self.assertEqual(videoFileName_1,
		                 dvi.getUrlDownloadDirForUrlTitle(videoTitle_1))
		self.assertEqual(None,
		                 dvi.getUrlDownloadDirForUrlTitle(videoTitle_2))
		self.assertEqual(None,
		                 dvi.getUrlDownloadDirForUrlTitle(videoTitle_3))

if __name__ == '__main__':
#	unittest.main()
	tst = TestDownloadUrlInfoDic()
	tst.testLoadExistingDownloadUrlInfoDic_specifying_only_info_dic_filePathName()
