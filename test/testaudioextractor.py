import unittest
import os, sys, inspect, shutil, glob, time
from io import StringIO

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from constants import *
from guioutputstub import GuiOutputStub
from audioextractor import AudioExtractor
from downloadedvideoinfodic import DownloadedVideoInfoDic
			
class TestAudioExtractor(unittest.TestCase):
	def testConvertSecondsTo_HHMMSS(self):
		audioExtractor = AudioExtractor(None, None, None)

		self.assertEqual('0:0:56', audioExtractor.convertSecondsTo_HHMMSS(56))
		self.assertEqual('0:1:56', audioExtractor.convertSecondsTo_HHMMSS(116))
		self.assertEqual('2:10:56', audioExtractor.convertSecondsTo_HHMMSS(7856))

	def testConvertStartEndSecondsListTo_HHMMSS_TimeFrameList(self):
		audioExtractor = AudioExtractor(None, None, None)

		self.assertEqual(['0:0:56', '2:10:56'], audioExtractor.convertStartEndSecondsListTo_HHMMSS_TimeFrameList([56, 7856]))
	
	def testExtractAudioPortion_one_video_with_no_extract_timeframe(self):
		playListName = 'test_audio_downloader_one_file_for_extract_with_one_extract_timeframe'
		targetAudioDir = AUDIO_DIR + DIR_SEP + playListName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		downloadedVideoInfoDic = DownloadedVideoInfoDic(targetAudioDir, playListName)
		videoFileName = 'Wear a mask Help slow the spread of Covid-19.mp4'
		downloadedVideoInfoDic.addVideoInfoForVideoIndex(1, 'Wear a mask. Help slow the spread of Covid-19.',
		                                                 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName)
		
		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)
		
		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName,
		            targetAudioDir + '\\' + videoFileName)
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadedVideoInfoDic)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtractor.extractAudioPortion(downloadedVideoInfoDic)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = os.listdir(targetAudioDir)
		self.assertEqual(
			sorted(['Wear a mask Help slow the spread of Covid-19.mp4', 'Wear a mask Help slow the spread of Covid-19.mp3']),
			sorted(videoAndAudioFileList))
		
		from mutagen.mp3 import MP3
		extractedMp3FileName = videoAndAudioFileList[0]
		
		self.assertIsNone(downloadedVideoInfoDic.getStartEndTimeFrame(1, extractedMp3FileName))
	
	# import json
	# print(json.dumps(downloadedVideoInfoDic.dic, sort_keys=False, indent=4))
	
	def testExtractAudioPortion_one_video_with_one_extract_timeframe(self):
		playListName = 'test_audio_downloader_one_file_for_extract_with_one_extract_timeframe'
		targetAudioDir = AUDIO_DIR + DIR_SEP + playListName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		startEndSecondsList = [5, 10]
		expectedExtractedFileDuration = startEndSecondsList[1] - startEndSecondsList[0]
		downloadedVideoInfoDic = DownloadedVideoInfoDic(targetAudioDir, playListName)
		videoFileName = 'Wear a mask Help slow the spread of Covid-19.mp4'
		downloadedVideoInfoDic.addVideoInfoForVideoIndex(1, 'Wear a mask. Help slow the spread of Covid-19.',
		                                    'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName)
		downloadedVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList)

		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)

		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName,
		            targetAudioDir + '\\' + videoFileName)
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadedVideoInfoDic)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtractor.extractAudioPortion(downloadedVideoInfoDic)

		sys.stdout = stdout

		videoAndAudioFileList = os.listdir(targetAudioDir)
		self.assertEqual(['Wear a mask Help slow the spread of Covid-19.mp4', 'Wear a mask Help slow the spread of Covid-19_1.mp3'], videoAndAudioFileList)

		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = videoAndAudioFileList[1]
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_1)
		self.assertAlmostEquals(expectedExtractedFileDuration, audio.info.length, delta=0.1)

		self.assertEqual(["0:0:5", "0:0:10"], downloadedVideoInfoDic.getStartEndTimeFrame(1, extractedMp3FileName_1))

		# import json
		# print(json.dumps(downloadedVideoInfoDic.dic, sort_keys=False, indent=4))
	
	def testExtractAudioPortion_one_video_with_two_extract_timeframe(self):
		playListName = 'test_audio_downloader_one_file_for_extract_with_one_extract_timeframe'
		targetAudioDir = AUDIO_DIR + DIR_SEP + playListName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		startEndSecondsList_1 = [5, 10]
		expectedExtractedFileDuration_1 = startEndSecondsList_1[1] - startEndSecondsList_1[0]

		startEndSecondsList_2 = [11, 13]
		expectedExtractedFileDuration_2 = startEndSecondsList_2[1] - startEndSecondsList_2[0]

		downloadedVideoInfoDic = DownloadedVideoInfoDic(targetAudioDir, playListName)
		videoFileName = 'Wear a mask Help slow the spread of Covid-19.mp4'
		downloadedVideoInfoDic.addVideoInfoForVideoIndex(1, 'Wear a mask. Help slow the spread of Covid-19.',
		                                                 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName)
		downloadedVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList_1)
		downloadedVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList_2)

		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)
		
		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName,
		            targetAudioDir + '\\' + videoFileName)
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadedVideoInfoDic)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtractor.extractAudioPortion(downloadedVideoInfoDic)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = os.listdir(targetAudioDir)
		self.assertEqual(
			['Wear a mask Help slow the spread of Covid-19.mp4',
			 'Wear a mask Help slow the spread of Covid-19_1.mp3',
			 'Wear a mask Help slow the spread of Covid-19_2.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = videoAndAudioFileList[1]
		extractedMp3FileName_2 = videoAndAudioFileList[2]
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_1)
		self.assertAlmostEquals(expectedExtractedFileDuration_1, audio.info.length, delta=0.1)
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_2)
		self.assertAlmostEquals(expectedExtractedFileDuration_2, audio.info.length, delta=0.1)

		self.assertEqual(["0:0:5", "0:0:10"], downloadedVideoInfoDic.getStartEndTimeFrame(1, extractedMp3FileName_1))
		self.assertEqual(["0:0:11", "0:0:13"], downloadedVideoInfoDic.getStartEndTimeFrame(1, extractedMp3FileName_2))


if __name__ == '__main__':
#	unittest.main()
	tst = TestAudioExtractor()
	ts = time.time()
	tst.testExtractAudioPortionAlt_dir_contains_one_file_with_one_extract_timeframe()
	print(time.time() - ts)
