import unittest
import os, sys, inspect, datetime, shutil

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
		
from downloadedvideoinfodic import DownloadedVideoInfoDic
from constants import *
			
class TestDownloadedVideoInfoDic(unittest.TestCase):
	def testAddVideoInfo(self):
		playListName = 'essai_vid_info'
		downloadDir = AUDIO_DIR + DIR_SEP + playListName
		dvi = DownloadedVideoInfoDic(downloadDir, playListName)
		dvi.addVideoInfo('title 1', 'https://youtube.com/watch?v=9iPvLx7gotk')
		dvi.addVideoInfo('title 2', 'https://youtube.com/watch?v=9iPvL8880999')
		
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', dvi.getVideoInfo('title 1')[0])
		self.assertEqual('https://youtube.com/watch?v=9iPvL8880999', dvi.getVideoInfo('title 2')[0])
	
if __name__ == '__main__':
	unittest.main()
#	tst = TestTransferFiles()
#	tst.testPathUploadToCloud_invalid_fileName()
