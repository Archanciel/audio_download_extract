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
		playListName = 'essai_vid_info'
		downloadDir = AUDIO_DIR + DIR_SEP + playListName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting video info dic file
		files = glob.glob(downloadDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)
		
		dvi = DownloadedVideoInfoDic(downloadDir, playListName)
		additionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_VIDEO_INFO_FILE)

		dvi.addVideoInfo(1, 'title 1', 'https://youtube.com/watch?v=9iPvLx7gotk')
		dvi.addVideoInfo(2, 'title 2', 'https://youtube.com/watch?v=9iPvL8880999')
		
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', dvi.getVideoInfoForVideoTitle('title 1')['url'])
		self.assertEqual('https://youtube.com/watch?v=9iPvL8880999', dvi.getVideoInfoForVideoTitle('title 2')['url'])

		self.assertEqual(additionTimeStr, dvi.getVideoInfoForVideoTitle('title 1')['downloadTime'])
		self.assertEqual(additionTimeStr, dvi.getVideoInfoForVideoTitle('title 2')['downloadTime'])

	def testSaveDic_new_info_dic_file(self):
		playListName = 'essai_vid_info'
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
		dvi.addVideoInfo(1, 'title 1', 'https://youtube.com/watch?v=9iPvLx7gotk')
		dvi.addVideoInfo(2, 'title 2', 'https://youtube.com/watch?v=9iPvL8880999')
		
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', dvi.getVideoInfoForVideoTitle('title 1')['url'])
		self.assertEqual('https://youtube.com/watch?v=9iPvL8880999', dvi.getVideoInfoForVideoTitle('title 2')['url'])

		self.assertEqual(additionTimeStr, dvi.getVideoInfoForVideoTitle('title 1')['downloadTime'])
		self.assertEqual(additionTimeStr, dvi.getVideoInfoForVideoTitle('title 2')['downloadTime'])

		dvi.saveDic()
		
		# creating new video info dic, reloading newly created video info dic file
		newDvi = DownloadedVideoInfoDic(downloadDir, playListName)
		newDvi.loadDic()
		
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', newDvi.getVideoInfoForVideoTitle('title 1')['url'])
		self.assertEqual('https://youtube.com/watch?v=9iPvL8880999', newDvi.getVideoInfoForVideoTitle('title 2')['url'])

		self.assertEqual(additionTimeStr, newDvi.getVideoInfoForVideoTitle('title 1')['downloadTime'])
		self.assertEqual(additionTimeStr, newDvi.getVideoInfoForVideoTitle('title 2')['downloadTime'])

	def testAddVideoInfo_existing_info_dic_file(self):
		playListName = 'essai_vid_info'
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
		dvi.addVideoInfo(1, 'title 1', 'https://youtube.com/watch?v=9iPvLx7gotk')
		dvi.addVideoInfo(2, 'title 2', 'https://youtube.com/watch?v=9iPvL8880999')
		
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', dvi.getVideoInfoForVideoTitle('title 1')['url'])
		self.assertEqual('https://youtube.com/watch?v=9iPvL8880999', dvi.getVideoInfoForVideoTitle('title 2')['url'])

		self.assertEqual(additionTimeStr, dvi.getVideoInfoForVideoTitle('title 1')['downloadTime'])
		self.assertEqual(additionTimeStr, dvi.getVideoInfoForVideoTitle('title 2')['downloadTime'])

		dvi.saveDic()
		
		# creating new video info dic, reloading newly created video info dic file
		newDvi = DownloadedVideoInfoDic(downloadDir, playListName)
		newDvi.loadDic()
		time.sleep(1)
		newAdditionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_VIDEO_INFO_FILE)

		# adding supplementary video info entry
		newDvi.addVideoInfo(3, 'title 3', 'https://youtube.com/watch?v=9iPvL1111')

		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', newDvi.getVideoInfoForVideoTitle('title 1')['url'])
		self.assertEqual('https://youtube.com/watch?v=9iPvL8880999', newDvi.getVideoInfoForVideoTitle('title 2')['url'])
		self.assertEqual('https://youtube.com/watch?v=9iPvL1111', newDvi.getVideoInfoForVideoTitle('title 3')['url'])

		self.assertEqual(additionTimeStr, newDvi.getVideoInfoForVideoTitle('title 1')['downloadTime'])
		self.assertEqual(additionTimeStr, newDvi.getVideoInfoForVideoTitle('title 2')['downloadTime'])
		self.assertEqual(newAdditionTimeStr, newDvi.getVideoInfoForVideoTitle('title 3')['downloadTime'])

		newDvi.saveDic()

		# creating new extended video info dic, reloading newly created video info dic file
		newExtendedDvi = DownloadedVideoInfoDic(downloadDir, playListName)
		newExtendedDvi.loadDic()

		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', newExtendedDvi.getVideoInfoForVideoTitle('title 1')['url'])
		self.assertEqual('https://youtube.com/watch?v=9iPvL8880999', newExtendedDvi.getVideoInfoForVideoTitle('title 2')['url'])
		self.assertEqual('https://youtube.com/watch?v=9iPvL1111', newExtendedDvi.getVideoInfoForVideoTitle('title 3')['url'])

		self.assertEqual(additionTimeStr, newExtendedDvi.getVideoInfoForVideoTitle('title 1')['downloadTime'])
		self.assertEqual(additionTimeStr, newExtendedDvi.getVideoInfoForVideoTitle('title 2')['downloadTime'])
		self.assertEqual(newAdditionTimeStr, newExtendedDvi.getVideoInfoForVideoTitle('title 3')['downloadTime'])

if __name__ == '__main__':
	unittest.main()
#	tst = TestTransferFiles()
#	tst.testPathUploadToCloud_invalid_fileName()
