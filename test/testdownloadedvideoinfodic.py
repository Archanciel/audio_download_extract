import unittest
import os, sys, inspect, glob, time
from datetime import datetime

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
		
from downloadedvideoinfodic import DownloadedVideoInfoDic
from constants import *
			
class TestDownloadedVideoInfoDic(unittest.TestCase):
	def testAddVideoInfo_new_info_dic_file(self):
		playListName = 'test_download_vid_info_dic'

		downloadDir = AUDIO_DIR + DIR_SEP + playListName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting video info dic file
		files = glob.glob(downloadDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)
		
		dvi = DownloadedVideoInfoDic(downloadDir, playListName)
		additionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_VIDEO_INFO_FILE)

		dvi.addVideoInfo(1, 'title 1', 'https://youtube.com/watch?v=9iPvLx7gotk', 'title 1.mp4')
		dvi.addVideoInfo(2, 'title 2', 'https://youtube.com/watch?v=9iPvL8880999', 'title 2.mp4')
		
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', dvi.getVideoInfoForVideoTitle('title 1')['url'])
		self.assertEqual('https://youtube.com/watch?v=9iPvL8880999', dvi.getVideoInfoForVideoTitle('title 2')['url'])

		self.assertEqual(additionTimeStr, dvi.getVideoInfoForVideoTitle('title 1')['downloadTime'])
		self.assertEqual(additionTimeStr, dvi.getVideoInfoForVideoTitle('title 2')['downloadTime'])

		# two ways of obtaining video title !
		self.assertEqual('title 1', dvi.getVideoInfoForVideoTitle('title 1')['title'])
		self.assertEqual('title 1', dvi.getVideoTitleForVideoIndex(1))

		self.assertEqual('title 1.mp4', dvi.getVideoFileNameForVideoIndex(1))
		self.assertEqual('title 2.mp4', dvi.getVideoFileNameForVideoIndex(2))

		self.assertIsNone(dvi.getExtractStartEndSecondsLists(videoIndex=1))
		self.assertIsNone(dvi.getSuppressStartEndSecondsLists(videoIndex=1))
		self.assertIsNone(dvi.getExtractStartEndSecondsLists(videoIndex=2))
		self.assertIsNone(dvi.getSuppressStartEndSecondsLists(videoIndex=2))

	def testAddVideoInfo_existing_info_dic_file(self):
		playListName = 'test_download_vid_info_dic'

		downloadDir = AUDIO_DIR + DIR_SEP + playListName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting video info dic file
		files = glob.glob(downloadDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)
		
		# creating new video info dic file and saving it
		
		dvi = DownloadedVideoInfoDic(downloadDir, playListName)
		additionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_VIDEO_INFO_FILE)
		dvi.addVideoInfo(1, 'title 1', 'https://youtube.com/watch?v=9iPvLx7gotk', 'title 1.mp4')
		dvi.addVideoInfo(2, 'title 2', 'https://youtube.com/watch?v=9iPvL8880999', 'title 2.mp4')
		
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', dvi.getVideoInfoForVideoTitle('title 1')['url'])
		self.assertEqual('https://youtube.com/watch?v=9iPvL8880999', dvi.getVideoInfoForVideoTitle('title 2')['url'])

		self.assertEqual(additionTimeStr, dvi.getVideoInfoForVideoTitle('title 1')['downloadTime'])
		self.assertEqual(additionTimeStr, dvi.getVideoInfoForVideoTitle('title 2')['downloadTime'])

		# two ways of obtaining video title !
		self.assertEqual('title 1', dvi.getVideoInfoForVideoTitle('title 1')['title'])
		self.assertEqual('title 1', dvi.getVideoTitleForVideoIndex(1))

		self.assertEqual('title 1.mp4', dvi.getVideoFileNameForVideoIndex(1))
		self.assertEqual('title 2.mp4', dvi.getVideoFileNameForVideoIndex(2))

		dvi.saveDic()
		
		# creating new video info dic, reloading newly created video info dic file
		reloadedDvi = DownloadedVideoInfoDic(downloadDir, playListName)
		reloadedDvi.loadDic()
		time.sleep(1)
		newAdditionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_VIDEO_INFO_FILE)

		# adding supplementary video info entry
		reloadedDvi.addVideoInfo(3, 'title 3', 'https://youtube.com/watch?v=9iPvL1111', 'title 3.mp4')

		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', reloadedDvi.getVideoInfoForVideoTitle('title 1')['url'])
		self.assertEqual('https://youtube.com/watch?v=9iPvL8880999', reloadedDvi.getVideoInfoForVideoTitle('title 2')['url'])
		self.assertEqual('https://youtube.com/watch?v=9iPvL1111', reloadedDvi.getVideoInfoForVideoTitle('title 3')['url'])

		self.assertEqual(additionTimeStr, reloadedDvi.getVideoInfoForVideoTitle('title 1')['downloadTime'])
		self.assertEqual(additionTimeStr, reloadedDvi.getVideoInfoForVideoTitle('title 2')['downloadTime'])
		self.assertEqual(newAdditionTimeStr, reloadedDvi.getVideoInfoForVideoTitle('title 3')['downloadTime'])

		# two ways of obtaining video title !
		self.assertEqual('title 3', reloadedDvi.getVideoInfoForVideoTitle('title 3')['title'])
		self.assertEqual('title 3', reloadedDvi.getVideoTitleForVideoIndex(3))

		self.assertEqual('title 3.mp4', reloadedDvi.getVideoFileNameForVideoIndex(3))

		reloadedDvi.saveDic()

		# creating new extended video info dic, reloading newly created video info dic file
		newReloadedDvi = DownloadedVideoInfoDic(downloadDir, playListName)
		newReloadedDvi.loadDic()

		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', newReloadedDvi.getVideoInfoForVideoTitle('title 1')['url'])
		self.assertEqual('https://youtube.com/watch?v=9iPvL8880999', newReloadedDvi.getVideoInfoForVideoTitle('title 2')['url'])
		self.assertEqual('https://youtube.com/watch?v=9iPvL1111', newReloadedDvi.getVideoInfoForVideoTitle('title 3')['url'])

		self.assertEqual(additionTimeStr, newReloadedDvi.getVideoInfoForVideoTitle('title 1')['downloadTime'])
		self.assertEqual(additionTimeStr, newReloadedDvi.getVideoInfoForVideoTitle('title 2')['downloadTime'])
		self.assertEqual(newAdditionTimeStr, newReloadedDvi.getVideoInfoForVideoTitle('title 3')['downloadTime'])

		# two ways of obtaining video title !
		self.assertEqual('title 3', newReloadedDvi.getVideoInfoForVideoTitle('title 3')['title'])
		self.assertEqual('title 3', newReloadedDvi.getVideoTitleForVideoIndex(3))

		self.assertEqual('title 3.mp4', reloadedDvi.getVideoFileNameForVideoIndex(3))

		self.assertIsNone(newReloadedDvi.getExtractStartEndSecondsLists(videoIndex=1))
		self.assertIsNone(newReloadedDvi.getSuppressStartEndSecondsLists(videoIndex=1))
		self.assertIsNone(newReloadedDvi.getExtractStartEndSecondsLists(videoIndex=2))
		self.assertIsNone(newReloadedDvi.getSuppressStartEndSecondsLists(videoIndex=2))
		self.assertIsNone(newReloadedDvi.getExtractStartEndSecondsLists(videoIndex=3))
		self.assertIsNone(newReloadedDvi.getSuppressStartEndSecondsLists(videoIndex=3))
	
	def testAddExtractAndSuppressStartEndSecondsList_existing_info_dic_file(self):
		playListName = 'test_download_vid_info_dic'

		downloadDir = AUDIO_DIR + DIR_SEP + playListName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting video info dic file
		files = glob.glob(downloadDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)
		
		# creating new video info dic file and saving it
		
		dvi = DownloadedVideoInfoDic(downloadDir, playListName)
		additionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_VIDEO_INFO_FILE)
		dvi.addVideoInfo(1, 'title 1', 'https://youtube.com/watch?v=9iPvLx7gotk', 'title 1.mp4')
		dvi.addVideoInfo(2, 'title 2', 'https://youtube.com/watch?v=9iPvL8880999', 'title 2.mp4')

		self.assertEqual('title 1.mp4', dvi.getVideoFileNameForVideoIndex(1))
		self.assertEqual('title 2.mp4', dvi.getVideoFileNameForVideoIndex(2))

		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', dvi.getVideoInfoForVideoTitle('title 1')['url'])
		self.assertEqual('https://youtube.com/watch?v=9iPvL8880999', dvi.getVideoInfoForVideoTitle('title 2')['url'])
		
		self.assertEqual(additionTimeStr, dvi.getVideoInfoForVideoTitle('title 1')['downloadTime'])
		self.assertEqual(additionTimeStr, dvi.getVideoInfoForVideoTitle('title 2')['downloadTime'])

		startEndSecondsList_one = [1, 10]
		startEndSecondsList_two = [15, 20]

		dvi.addExtractStartEndSecondsList(1, startEndSecondsList_one)
		dvi.addExtractStartEndSecondsList(1, startEndSecondsList_two)
		dvi.addSuppressStartEndSecondsList(1, startEndSecondsList_two)
		dvi.addSuppressStartEndSecondsList(1, startEndSecondsList_one)
		dvi.addExtractStartEndSecondsList(2, startEndSecondsList_two)

		self.assertEqual([startEndSecondsList_one, startEndSecondsList_two], dvi.getExtractStartEndSecondsLists(1))
		self.assertEqual([startEndSecondsList_two, startEndSecondsList_one], dvi.getSuppressStartEndSecondsLists(1))
		self.assertEqual([startEndSecondsList_two], dvi.getExtractStartEndSecondsLists(2))
		self.assertEqual([], dvi.getSuppressStartEndSecondsLists(2))

		dvi.saveDic()
		
		# creating new video info dic, reloading newly created video info dic file
		reloadedDvi = DownloadedVideoInfoDic(downloadDir, playListName)
		reloadedDvi.loadDic()
		time.sleep(1)
		newAdditionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_VIDEO_INFO_FILE)
		
		# adding supplementary video info entry
		reloadedDvi.addVideoInfo(3, 'title 3', 'https://youtube.com/watch?v=9iPvL1111', 'title 3.mp4')
		
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk',
		                 reloadedDvi.getVideoInfoForVideoTitle('title 1')['url'])
		self.assertEqual('https://youtube.com/watch?v=9iPvL8880999',
		                 reloadedDvi.getVideoInfoForVideoTitle('title 2')['url'])
		self.assertEqual('https://youtube.com/watch?v=9iPvL1111',
		                 reloadedDvi.getVideoInfoForVideoTitle('title 3')['url'])
		
		self.assertEqual(additionTimeStr, reloadedDvi.getVideoInfoForVideoTitle('title 1')['downloadTime'])
		self.assertEqual(additionTimeStr, reloadedDvi.getVideoInfoForVideoTitle('title 2')['downloadTime'])
		self.assertEqual(newAdditionTimeStr, reloadedDvi.getVideoInfoForVideoTitle('title 3')['downloadTime'])
		
		startEndSecondsList_one_for_3 = [12, 100]
		startEndSecondsList_two_for_3 = [115, 200]

		reloadedDvi.addExtractStartEndSecondsList(3, startEndSecondsList_one_for_3)
		reloadedDvi.addExtractStartEndSecondsList(3, startEndSecondsList_two_for_3)
		reloadedDvi.addSuppressStartEndSecondsList(3, startEndSecondsList_two_for_3)

		reloadedDvi.saveDic()
		
		# creating new extended video info dic, reloading newly created video info dic file
		newReloadedDvi = DownloadedVideoInfoDic(downloadDir, playListName)
		newReloadedDvi.loadDic()
		
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk',
		                 newReloadedDvi.getVideoInfoForVideoTitle('title 1')['url'])
		self.assertEqual('https://youtube.com/watch?v=9iPvL8880999',
		                 newReloadedDvi.getVideoInfoForVideoTitle('title 2')['url'])
		self.assertEqual('https://youtube.com/watch?v=9iPvL1111',
		                 newReloadedDvi.getVideoInfoForVideoTitle('title 3')['url'])
		
		self.assertEqual(additionTimeStr, newReloadedDvi.getVideoInfoForVideoTitle('title 1')['downloadTime'])
		self.assertEqual(additionTimeStr, newReloadedDvi.getVideoInfoForVideoTitle('title 2')['downloadTime'])
		self.assertEqual(newAdditionTimeStr, newReloadedDvi.getVideoInfoForVideoTitle('title 3')['downloadTime'])
		self.assertEqual([startEndSecondsList_one, startEndSecondsList_two], newReloadedDvi.getExtractStartEndSecondsLists(1))
		self.assertEqual([startEndSecondsList_two, startEndSecondsList_one], newReloadedDvi.getSuppressStartEndSecondsLists(1))
		self.assertEqual([startEndSecondsList_two], newReloadedDvi.getExtractStartEndSecondsLists(2))
		self.assertEqual([], newReloadedDvi.getSuppressStartEndSecondsLists(2))
		self.assertEqual([startEndSecondsList_one_for_3, startEndSecondsList_two_for_3], newReloadedDvi.getExtractStartEndSecondsLists(3))
		self.assertEqual([startEndSecondsList_two_for_3], newReloadedDvi.getSuppressStartEndSecondsLists(3))


if __name__ == '__main__':
	unittest.main()
#	tst = TestTransferFiles()
#	tst.testPathUploadToCloud_invalid_fileName()
