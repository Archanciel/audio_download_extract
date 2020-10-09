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
		playListName = 'test_audio_extractor'
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
		
		self.assertIsNone(downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(1, extractedMp3FileName))
	
	def testExtractAudioPortion_one_video_with_one_extract_and_no_suppress_timeframe(self):
		playListName = 'test_audio_extractor'
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

		self.assertEqual(["0:0:5", "0:0:10"], downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(1, extractedMp3FileName_1))
	
	def testExtractAudioPortion_one_video_with_two_extract_timeframe(self):
		playListName = 'test_audio_extractor'
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

		self.assertEqual(["0:0:5", "0:0:10"], downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(1, extractedMp3FileName_1))
		self.assertEqual(["0:0:11", "0:0:13"], downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(1, extractedMp3FileName_2))
	
	def testExtractAudioPortion_two_video_with_two_extract_timeframe_each(self):
		playListName = 'test_audio_extractor'
		targetAudioDir = AUDIO_DIR + DIR_SEP + playListName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)

		# first video		
		videoIndex = 1
		startEndSecondsList_1_1 = [5, 10]
		expectedExtractedFileDuration_1_1 = startEndSecondsList_1_1[1] - startEndSecondsList_1_1[0]
		
		startEndSecondsList_1_2 = [11, 13]
		expectedExtractedFileDuration_1_2 = startEndSecondsList_1_2[1] - startEndSecondsList_1_2[0]
		
		downloadedVideoInfoDic = DownloadedVideoInfoDic(targetAudioDir, playListName)
		videoFileName_1 = 'Wear a mask Help slow the spread of Covid-19.mp4'
		downloadedVideoInfoDic.addVideoInfoForVideoIndex(1, 'Wear a mask. Help slow the spread of Covid-19.',
		                                                 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName_1)
		downloadedVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList_1_1)
		downloadedVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList_1_2)
		
		# second video		
		videoIndex = 2
		startEndSecondsList_2_1 = [3, 8]
		expectedExtractedFileDuration_2_1 = startEndSecondsList_2_1[1] - startEndSecondsList_2_1[0]
		
		startEndSecondsList_2_2 = [10, 13]
		expectedExtractedFileDuration_2_2 = startEndSecondsList_2_2[1] - startEndSecondsList_2_2[0]
		
		videoFileName_2 = 'Here to help Give him what he wants.mp4'
		downloadedVideoInfoDic.addVideoInfoForVideoIndex(2, 'Here to help: Give him what he wants downloaded.',
		                                                 'https://youtube.com/watch?v=Eqy6M6qLWGw', videoFileName_2)
		downloadedVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList_2_1)
		downloadedVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList_2_2)
		
		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)
		
		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName_1,
		            targetAudioDir + '\\' + videoFileName_1)
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName_2,
		            targetAudioDir + '\\' + videoFileName_2)
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadedVideoInfoDic)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtractor.extractAudioPortion(downloadedVideoInfoDic)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = sorted(os.listdir(targetAudioDir))
		self.assertEqual(
			['Here to help Give him what he wants.mp4',
			 'Here to help Give him what he wants_1.mp3',
			 'Here to help Give him what he wants_2.mp3',
			 'Wear a mask Help slow the spread of Covid-19.mp4',
			 'Wear a mask Help slow the spread of Covid-19_1.mp3',
			 'Wear a mask Help slow the spread of Covid-19_2.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1_1 = videoAndAudioFileList[4]
		extractedMp3FileName_1_2 = videoAndAudioFileList[5]
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_1_1)
		self.assertAlmostEquals(expectedExtractedFileDuration_1_1, audio.info.length, delta=0.1)
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_1_2)
		self.assertAlmostEquals(expectedExtractedFileDuration_1_2, audio.info.length, delta=0.1)
		
		self.assertEqual(["0:0:5", "0:0:10"], downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(1, extractedMp3FileName_1_1))
		self.assertEqual(["0:0:11", "0:0:13"], downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(1, extractedMp3FileName_1_2))

		extractedMp3FileName_2_1 = videoAndAudioFileList[1]
		extractedMp3FileName_2_2 = videoAndAudioFileList[2]
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_2_1)
		self.assertAlmostEquals(expectedExtractedFileDuration_2_1, audio.info.length, delta=0.1)
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_2_2)
		self.assertAlmostEquals(expectedExtractedFileDuration_2_2, audio.info.length, delta=0.1)
		
		self.assertEqual(["0:0:3", "0:0:8"], downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(2, extractedMp3FileName_2_1))
		self.assertEqual(["0:0:10", "0:0:13"], downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(2, extractedMp3FileName_2_2))
	
	def testSuppressAudioPortion_one_video_with_no_extract_and_one_suppress_timeframe(self):
		playListName = 'test_audio_extractor'
		targetAudioDir = AUDIO_DIR + DIR_SEP + playListName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		suppressStartEndSecondsList = [[0, 2], [4, 8], [11, 13], [15, 17]]
		expectedExtractedFileDuration = 10
		downloadedVideoInfoDic = DownloadedVideoInfoDic(targetAudioDir, playListName)
		videoFileName = 'test_suppress_audio_file.mp4'
		downloadedVideoInfoDic.addVideoInfoForVideoIndex(1, 'test_suppress_audio_file.',
		                                                 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName)
		downloadedVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList)
		
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
		
		audioExtractor.suppressAudioPortion(downloadedVideoInfoDic)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = os.listdir(targetAudioDir)

		self.assertEqual(
			['test_suppress_audio_file.mp4', 'test_suppress_audio_file_s.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = videoAndAudioFileList[1]
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_1)
		self.assertAlmostEquals(expectedExtractedFileDuration, audio.info.length, delta=0.5)
		
		self.assertEqual([["0:0:0", "0:0:2"], ["0:0:4", "0:0:8"], ["0:0:11", "0:0:13"], ["0:0:15", "0:0:17"]], downloadedVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(1))

if __name__ == '__main__':
#	unittest.main()
	tst = TestAudioExtractor()
	ts = time.time()
	tst.testExtractAudioPortion_one_video_with_two_extract_timeframe()
	print(time.time() - ts)
