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

		dvi.addVideoInfo('title 1', 'https://youtube.com/watch?v=9iPvLx7gotk')
		dvi.addVideoInfo('title 2', 'https://youtube.com/watch?v=9iPvL8880999')
		
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', dvi.getVideoInfo('title 1')[0])
		self.assertEqual('https://youtube.com/watch?v=9iPvL8880999', dvi.getVideoInfo('title 2')[0])

		self.assertEqual(additionTimeStr, dvi.getVideoInfo('title 1')[1])
		self.assertEqual(additionTimeStr, dvi.getVideoInfo('title 2')[1])

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
		dvi.addVideoInfo('title 1', 'https://youtube.com/watch?v=9iPvLx7gotk')
		dvi.addVideoInfo('title 2', 'https://youtube.com/watch?v=9iPvL8880999')
		
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', dvi.getVideoInfo('title 1')[0])
		self.assertEqual('https://youtube.com/watch?v=9iPvL8880999', dvi.getVideoInfo('title 2')[0])

		self.assertEqual(additionTimeStr, dvi.getVideoInfo('title 1')[1])
		self.assertEqual(additionTimeStr, dvi.getVideoInfo('title 2')[1])

		dvi.saveDic()
		
		# creating new video info dic, reloading newly created video info dic file
		newDvi = DownloadedVideoInfoDic(downloadDir, playListName)
		
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', newDvi.getVideoInfo('title 1')[0])
		self.assertEqual('https://youtube.com/watch?v=9iPvL8880999', newDvi.getVideoInfo('title 2')[0])

		self.assertEqual(additionTimeStr, newDvi.getVideoInfo('title 1')[1])
		self.assertEqual(additionTimeStr, newDvi.getVideoInfo('title 2')[1])

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
		dvi.addVideoInfo('title 1', 'https://youtube.com/watch?v=9iPvLx7gotk')
		dvi.addVideoInfo('title 2', 'https://youtube.com/watch?v=9iPvL8880999')
		
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', dvi.getVideoInfo('title 1')[0])
		self.assertEqual('https://youtube.com/watch?v=9iPvL8880999', dvi.getVideoInfo('title 2')[0])

		self.assertEqual(additionTimeStr, dvi.getVideoInfo('title 1')[1])
		self.assertEqual(additionTimeStr, dvi.getVideoInfo('title 2')[1])

		dvi.saveDic()
		
		# creating new video info dic, reloading newly created video info dic file
		newDvi = DownloadedVideoInfoDic(downloadDir, playListName)
		time.sleep(1)
		newAdditionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_VIDEO_INFO_FILE)

		# adding supplementary video info entry
		newDvi.addVideoInfo('title 3', 'https://youtube.com/watch?v=9iPvL1111')

		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', newDvi.getVideoInfo('title 1')[0])
		self.assertEqual('https://youtube.com/watch?v=9iPvL8880999', newDvi.getVideoInfo('title 2')[0])
		self.assertEqual('https://youtube.com/watch?v=9iPvL1111', newDvi.getVideoInfo('title 3')[0])

		self.assertEqual(additionTimeStr, newDvi.getVideoInfo('title 1')[1])
		self.assertEqual(additionTimeStr, newDvi.getVideoInfo('title 2')[1])
		self.assertEqual(newAdditionTimeStr, newDvi.getVideoInfo('title 3')[1])

		newDvi.saveDic()

		# creating new extended video info dic, reloading newly created video info dic file
		newExtendedDvi = DownloadedVideoInfoDic(downloadDir, playListName)

		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', newExtendedDvi.getVideoInfo('title 1')[0])
		self.assertEqual('https://youtube.com/watch?v=9iPvL8880999', newExtendedDvi.getVideoInfo('title 2')[0])
		self.assertEqual('https://youtube.com/watch?v=9iPvL1111', newExtendedDvi.getVideoInfo('title 3')[0])

		self.assertEqual(additionTimeStr, newExtendedDvi.getVideoInfo('title 1')[1])
		self.assertEqual(additionTimeStr, newExtendedDvi.getVideoInfo('title 2')[1])
		self.assertEqual(newAdditionTimeStr, newExtendedDvi.getVideoInfo('title 3')[1])

if __name__ == '__main__':
	unittest.main()
#	tst = TestTransferFiles()
#	tst.testPathUploadToCloud_invalid_fileName()
