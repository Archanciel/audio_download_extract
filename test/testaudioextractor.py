import unittest
import os, sys, inspect, shutil, glob, time
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from constants import *
from guioutputstub import GuiOutputStub
from audioextractor import AudioExtractor
from downloadedvideoinfodic import DownloadedVideoInfoDic
			
class TestAudioExtractor(unittest.TestCase):
	def testExtractAudioPortion_dir_contains_one_file_with_one_extract_timeframe(self):
		playListName = 'test_audio_downloader_one_file_for_extract_with_one_extract_timeframe'
		targetAudioDir = AUDIO_DIR + DIR_SEP + playListName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		downloadedVideoInfoDic = DownloadedVideoInfoDic(targetAudioDir, playListName)
		videoIndex = 1
		startEndSecondsList = [5, 10]
		expectedExtractedFileDuration = startEndSecondsList[1] - startEndSecondsList[0]
		downloadedVideoInfoDic = DownloadedVideoInfoDic(targetAudioDir, playListName)
		downloadedVideoInfoDic.addVideoInfoForVideoIndex(1, 'Wear a mask. Help slow the spread of Covid-19.',
		                                    'https://youtube.com/watch?v=9iPvLx7gotk', 'Wear a mask Help slow the spread of Covid-19.mp4')
		downloadedVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList)

		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)

		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData' + '\\Wear a mask Help slow the spread of Covid-19.mp4' , targetAudioDir + '\\Wear a mask Help slow the spread of Covid-19.mp4')
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadedVideoInfoDic)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtractor.extractAudioPortion(downloadedVideoInfoDic)

		sys.stdout = stdout

		extractedFileList = os.listdir(targetAudioDir)
		self.assertEqual(['Wear a mask Help slow the spread of Covid-19_1.mp3'], extractedFileList)

		from mutagen.mp3 import MP3
		audio = MP3(targetAudioDir + DIR_SEP + extractedFileList[0])
		self.assertAlmostEquals(expectedExtractedFileDuration, audio.info.length, delta=0.1)

if __name__ == '__main__':
#	unittest.main()
	tst = TestAudioExtractor()
	ts = time.time()
	tst.testExtractAudioPortionAlt_dir_contains_one_file_with_one_extract_timeframe()
	print(time.time() - ts)
