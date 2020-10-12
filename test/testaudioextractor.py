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
	
	def testExtractAudioPortions_one_video_with_no_extract_no_suppress_timeframe(self):
		playListName = 'test_audio_extractor'
		targetAudioDir = AUDIO_DIR + DIR_SEP + playListName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		downloadedVideoInfoDic = DownloadedVideoInfoDic(targetAudioDir, playListName)
		videoFileName = 'Wear a mask Help slow the spread of Covid-19.mp4'
		downloadedVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'Wear a mask. Help slow the spread of Covid-19.',
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
		
		audioExtractor.convertVideoToAudio(videoFileName)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = os.listdir(targetAudioDir)
		self.assertEqual(
			sorted(['Wear a mask Help slow the spread of Covid-19.mp4', 'Wear a mask Help slow the spread of Covid-19.mp3']),
			sorted(videoAndAudioFileList))
		
		extractedMp3FileName = videoAndAudioFileList[0]
		
		self.assertIsNone(downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex, extractedMp3FileName))
		
		self.assertIsNone(downloadedVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertIsNone(downloadedVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
	
	def testExtractAudioPortions_one_video_with_one_extract_no_suppress_timeframe(self):
		playListName = 'test_audio_extractor'
		targetAudioDir = AUDIO_DIR + DIR_SEP + playListName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		startEndSecondsList = [5, 10]
		expectedExtractedFileDuration = startEndSecondsList[1] - startEndSecondsList[0]
		downloadedVideoInfoDic = DownloadedVideoInfoDic(targetAudioDir, playListName)
		videoFileName = 'Wear a mask Help slow the spread of Covid-19.mp4'
		downloadedVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'Wear a mask. Help slow the spread of Covid-19.',
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
		
		audioExtractor.extractAudioPortions(videoIndex, videoFileName, downloadedVideoInfoDic)

		sys.stdout = stdout

		videoAndAudioFileList = os.listdir(targetAudioDir)
		self.assertEqual(['Wear a mask Help slow the spread of Covid-19.mp4', 'Wear a mask Help slow the spread of Covid-19_1.mp3'], videoAndAudioFileList)

		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = videoAndAudioFileList[1]
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_1)
		self.assertAlmostEquals(expectedExtractedFileDuration, audio.info.length, delta=0.1)

		self.assertEqual(["0:0:5", "0:0:10"], downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex, extractedMp3FileName_1))
		
		self.assertIsNone(downloadedVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertIsNone(downloadedVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
	
	def testExtractAudioPortions_one_video_with_one_extract_no_suppress_timeframe_extract_from_0(self):
		playListName = 'test_audio_extractor'
		targetAudioDir = AUDIO_DIR + DIR_SEP + playListName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		startEndSecondsList = [0, 5]
		expectedExtractedFileDuration = startEndSecondsList[1] - startEndSecondsList[0]
		downloadedVideoInfoDic = DownloadedVideoInfoDic(targetAudioDir, playListName)
		videoFileName = 'Wear a mask Help slow the spread of Covid-19.mp4'
		downloadedVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'Wear a mask. Help slow the spread of Covid-19.',
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
		
		audioExtractor.extractAudioPortions(videoIndex, videoFileName, downloadedVideoInfoDic)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = os.listdir(targetAudioDir)
		self.assertEqual(
			['Wear a mask Help slow the spread of Covid-19.mp4', 'Wear a mask Help slow the spread of Covid-19_1.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = videoAndAudioFileList[1]
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_1)
		self.assertAlmostEquals(expectedExtractedFileDuration, audio.info.length, delta=0.1)
		
		self.assertEqual(["0:0:0", "0:0:5"],
		                 downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex,
		                                                                                        extractedMp3FileName_1))
		
		self.assertIsNone(downloadedVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertIsNone(downloadedVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))

	def testExtractAudioPortions_one_video_with_one_extract_no_suppress_timeframe_extract_from_n_to_end(self):
		playListName = 'test_audio_extractor'
		targetAudioDir = AUDIO_DIR + DIR_SEP + playListName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		startEndSecondsList = [10, 'end']
		expectedExtractedFileDuration = 4.7
		downloadedVideoInfoDic = DownloadedVideoInfoDic(targetAudioDir, playListName)
		videoFileName = 'Wear a mask Help slow the spread of Covid-19.mp4'
		downloadedVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'Wear a mask. Help slow the spread of Covid-19.',
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
		
		audioExtractor.extractAudioPortions(videoIndex, videoFileName, downloadedVideoInfoDic)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = os.listdir(targetAudioDir)
		self.assertEqual(
			['Wear a mask Help slow the spread of Covid-19.mp4', 'Wear a mask Help slow the spread of Covid-19_1.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = videoAndAudioFileList[1]
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_1)
		self.assertAlmostEquals(expectedExtractedFileDuration, audio.info.length, delta=0.1)
		
		self.assertEqual(['0:0:10', '0:0:14.65'],
		                 downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex,
		                                                                                        extractedMp3FileName_1))
		
		self.assertIsNone(downloadedVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertIsNone(downloadedVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
	
	def testExtractAudioPortions_one_video_with_two_extract_no_suppress_timeframe(self):
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
		downloadedVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'Wear a mask. Help slow the spread of Covid-19.',
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
		
		audioExtractor.extractAudioPortions(videoIndex, videoFileName, downloadedVideoInfoDic)
		
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

		self.assertEqual(["0:0:5", "0:0:10"], downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex, extractedMp3FileName_1))
		self.assertEqual(["0:0:11", "0:0:13"], downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex, extractedMp3FileName_2))
		
		self.assertIsNone(downloadedVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertIsNone(downloadedVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))

	def testExtractAudioPortions_one_video_with_two_extract_no_suppress_timeframe_last_extract_to_end(self):
		playListName = 'test_audio_extractor'
		targetAudioDir = AUDIO_DIR + DIR_SEP + playListName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		startEndSecondsList_1 = [5, 10]
		expectedExtractedFileDuration_1 = startEndSecondsList_1[1] - startEndSecondsList_1[0]
		
		startEndSecondsList_2 = [11, 'end']
		expectedExtractedFileDuration_2 = 3.7
		
		downloadedVideoInfoDic = DownloadedVideoInfoDic(targetAudioDir, playListName)
		videoFileName = 'Wear a mask Help slow the spread of Covid-19.mp4'
		downloadedVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'Wear a mask. Help slow the spread of Covid-19.',
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
		
		audioExtractor.extractAudioPortions(videoIndex, videoFileName, downloadedVideoInfoDic)
		
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
		
		self.assertEqual(["0:0:5", "0:0:10"],
		                 downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex,
		                                                                                        extractedMp3FileName_1))
		self.assertEqual(["0:0:11", "0:0:14.65"],
		                 downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex,
		                                                                                        extractedMp3FileName_2))
		
		self.assertIsNone(downloadedVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertIsNone(downloadedVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
	
	def testExtractAudioPortions_two_video_with_two_extract_no_suppress_timeframe_each(self):
		playListName = 'test_audio_extractor'
		targetAudioDir = AUDIO_DIR + DIR_SEP + playListName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)

		# first video		
		videoIndexOne = 1
		startEndSecondsList_1_1 = [5, 10]
		expectedExtractedFileDuration_1_1 = startEndSecondsList_1_1[1] - startEndSecondsList_1_1[0]
		
		startEndSecondsList_1_2 = [11, 13]
		expectedExtractedFileDuration_1_2 = startEndSecondsList_1_2[1] - startEndSecondsList_1_2[0]
		
		downloadedVideoInfoDic = DownloadedVideoInfoDic(targetAudioDir, playListName)
		videoFileName_1 = 'Wear a mask Help slow the spread of Covid-19.mp4'
		downloadedVideoInfoDic.addVideoInfoForVideoIndex(videoIndexOne, 'Wear a mask. Help slow the spread of Covid-19.',
		                                                 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName_1)
		downloadedVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndexOne, startEndSecondsList_1_1)
		downloadedVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndexOne, startEndSecondsList_1_2)
		
		# second video		
		videoIndexTwo = 2
		startEndSecondsList_2_1 = [3, 8]
		expectedExtractedFileDuration_2_1 = startEndSecondsList_2_1[1] - startEndSecondsList_2_1[0]
		
		startEndSecondsList_2_2 = [10, 13]
		expectedExtractedFileDuration_2_2 = startEndSecondsList_2_2[1] - startEndSecondsList_2_2[0]
		
		videoFileName_2 = 'Here to help Give him what he wants.mp4'
		downloadedVideoInfoDic.addVideoInfoForVideoIndex(videoIndexTwo, 'Here to help: Give him what he wants downloaded.',
		                                                 'https://youtube.com/watch?v=Eqy6M6qLWGw', videoFileName_2)
		downloadedVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndexTwo, startEndSecondsList_2_1)
		downloadedVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndexTwo, startEndSecondsList_2_2)
		
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
		
		audioExtractor.extractPlaylistAudio(downloadedVideoInfoDic)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = sorted(os.listdir(targetAudioDir))
		self.assertEqual(
			['Here to help Give him what he wants.mp4',
			 'Here to help Give him what he wants_1.mp3',
			 'Here to help Give him what he wants_2.mp3',
			 'Here to help Give him what he wants_full.mp3',
			 'Wear a mask Help slow the spread of Covid-19.mp4',
			 'Wear a mask Help slow the spread of Covid-19_1.mp3',
			 'Wear a mask Help slow the spread of Covid-19_2.mp3',
			 'Wear a mask Help slow the spread of Covid-19_full.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1_1 = videoAndAudioFileList[5]
		extractedMp3FileName_1_2 = videoAndAudioFileList[6]
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_1_1)
		self.assertAlmostEquals(expectedExtractedFileDuration_1_1, audio.info.length, delta=0.1)
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_1_2)
		self.assertAlmostEquals(expectedExtractedFileDuration_1_2, audio.info.length, delta=0.1)
		
		extractedMp3FileName_2_1 = videoAndAudioFileList[1]
		extractedMp3FileName_2_2 = videoAndAudioFileList[2]
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_2_1)
		self.assertAlmostEquals(expectedExtractedFileDuration_2_1, audio.info.length, delta=0.1)
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_2_2)
		self.assertAlmostEquals(expectedExtractedFileDuration_2_2, audio.info.length, delta=0.1)

		self.assertEqual(["0:0:5", "0:0:10"], downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndexOne, extractedMp3FileName_1_1))
		self.assertEqual(["0:0:11", "0:0:13"], downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndexOne, extractedMp3FileName_1_2))
		
		self.assertIsNone(downloadedVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndexOne))
		self.assertIsNone(downloadedVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndexOne))
		
		extractedMp3FileName_2_1 = videoAndAudioFileList[1]
		extractedMp3FileName_2_2 = videoAndAudioFileList[2]
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_2_1)
		self.assertAlmostEquals(expectedExtractedFileDuration_2_1, audio.info.length, delta=0.1)
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_2_2)
		self.assertAlmostEquals(expectedExtractedFileDuration_2_2, audio.info.length, delta=0.1)
		
		self.assertEqual(["0:0:3", "0:0:8"], downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndexTwo, extractedMp3FileName_2_1))
		self.assertEqual(["0:0:10", "0:0:13"], downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndexTwo, extractedMp3FileName_2_2))
		
		self.assertIsNone(downloadedVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndexTwo))
		self.assertIsNone(downloadedVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndexTwo))
	
	def testSuppressAudioPortions_one_video_with_no_extract_and_three_suppress_timeframe(self):
		playListName = 'test_audio_extractor'
		targetAudioDir = AUDIO_DIR + DIR_SEP + playListName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		suppressStartEndSecondsList_1 = [4, 8]
		suppressStartEndSecondsList_2 = [11, 13]
		suppressStartEndSecondsList_3 = [15, 17]
		expectedExtractedFileDuration = 12.5
		downloadedVideoInfoDic = DownloadedVideoInfoDic(targetAudioDir, playListName)
		videoFileName = 'test_suppress_audio_file.mp4'
		downloadedVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'test_suppress_audio_file.',
		                                                 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName)
		downloadedVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_1)
		downloadedVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_2)
		downloadedVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_3)
		
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
		
		audioExtractor.suppressAudioPortions(videoIndex, videoFileName, downloadedVideoInfoDic)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = os.listdir(targetAudioDir)

		self.assertEqual(
			['test_suppress_audio_file.mp4', 'test_suppress_audio_file_s.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = videoAndAudioFileList[1]
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_1)
		self.assertAlmostEquals(expectedExtractedFileDuration, audio.info.length, delta=0.1)

		self.assertIsNone(downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex, extractedMp3FileName_1))

		self.assertEqual([["0:0:4", "0:0:8"], ["0:0:11", "0:0:13"], ["0:0:15", "0:0:17"]], downloadedVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertEqual([['0:0:0', '0:0:4'], ['0:0:8', '0:0:11'], ['0:0:13', '0:0:15'], ['0:0:17', '0:0:20.43']], downloadedVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
	
	def testSuppressAudioPortions_one_video_with_no_extract_and_three_suppress_timeframe_last_suppress_to_end(self):
		playListName = 'test_audio_extractor'
		targetAudioDir = AUDIO_DIR + DIR_SEP + playListName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		suppressStartEndSecondsList_1 = [4, 8]
		suppressStartEndSecondsList_2 = [11, 13]
		suppressStartEndSecondsList_3 = [15, 'end']
		expectedExtractedFileDuration = 9.03
		downloadedVideoInfoDic = DownloadedVideoInfoDic(targetAudioDir, playListName)
		videoFileName = 'test_suppress_audio_file.mp4'
		downloadedVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'test_suppress_audio_file.',
		                                                 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName)
		downloadedVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_1)
		downloadedVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_2)
		downloadedVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_3)
		
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
		
		audioExtractor.suppressAudioPortions(videoIndex, videoFileName, downloadedVideoInfoDic)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = os.listdir(targetAudioDir)
		
		self.assertEqual(
			['test_suppress_audio_file.mp4', 'test_suppress_audio_file_s.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = videoAndAudioFileList[1]
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_1)
		self.assertAlmostEquals(expectedExtractedFileDuration, audio.info.length, delta=0.1)
		
		self.assertIsNone(
			downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex, extractedMp3FileName_1))
		
		self.assertEqual([["0:0:4", "0:0:8"], ["0:0:11", "0:0:13"], ["0:0:15", '0:0:20.43']],
		                 downloadedVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertEqual([['0:0:0', '0:0:4'], ['0:0:8', '0:0:11'], ['0:0:13', '0:0:15']],
		                 downloadedVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
	
	def testSuppressAudioPortions_one_video_with_no_extract_and_four_suppress_timeframe_one_starting_at_zero(self):
		playListName = 'test_audio_extractor'
		targetAudioDir = AUDIO_DIR + DIR_SEP + playListName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		suppressStartEndSecondsList_1 = [0, 2]
		suppressStartEndSecondsList_2 = [4, 8]
		suppressStartEndSecondsList_3 = [11, 13]
		suppressStartEndSecondsList_4 = [15, 17]
		expectedSuppressedFileDuration = 10.4
		downloadedVideoInfoDic = DownloadedVideoInfoDic(targetAudioDir, playListName)
		videoFileName = 'test_suppress_audio_file.mp4'
		downloadedVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'test_suppress_audio_file.',
		                                                 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName)
		downloadedVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_1)
		downloadedVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_2)
		downloadedVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_3)
		downloadedVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_4)

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
		audioExtractor.suppressAudioPortions(videoIndex, videoFileName, downloadedVideoInfoDic)

		sys.stdout = stdout
		
		videoAndAudioFileList = os.listdir(targetAudioDir)
		
		self.assertEqual(
			['test_suppress_audio_file.mp4', 'test_suppress_audio_file_s.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = videoAndAudioFileList[1]
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_1)
		self.assertAlmostEquals(expectedSuppressedFileDuration, audio.info.length, delta=0.1)

		self.assertIsNone(downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex, extractedMp3FileName_1))

		self.assertEqual([['0:0:0', '0:0:2'], ['0:0:4', '0:0:8'], ['0:0:11', '0:0:13'], ['0:0:15', '0:0:17']], downloadedVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertEqual([['0:0:2', '0:0:4'], ['0:0:8', '0:0:11'], ['0:0:13', '0:0:15'], ['0:0:17', '0:0:20.43']], downloadedVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
	
	def testSuppressAudioPortions_two_video_with_two_suppress_no_extract_timeframe_each(self):
		playListName = 'test_audio_extractor'
		targetAudioDir = AUDIO_DIR + DIR_SEP + playListName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		# first video
		videoIndexOne = 1
		suppressStartEndSecondsList_1_1 = [0, 2]
		suppressStartEndSecondsList_1_2 = [4, 8]
		suppressStartEndSecondsList_1_3 = [11, 13]
		suppressStartEndSecondsList_1_4 = [15, 17]
		expectedSuppressedFileDuration_1 = 10.4
		downloadedVideoInfoDic = DownloadedVideoInfoDic(targetAudioDir, playListName)
		videoFileName_1 = 'test_suppress_audio_file.mp4'
		downloadedVideoInfoDic.addVideoInfoForVideoIndex(videoIndexOne, 'test_suppress_audio_file.',
		                                                 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName_1)
		downloadedVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndexOne, suppressStartEndSecondsList_1_1)
		downloadedVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndexOne, suppressStartEndSecondsList_1_2)
		downloadedVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndexOne, suppressStartEndSecondsList_1_3)
		downloadedVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndexOne, suppressStartEndSecondsList_1_4)
		
		# second video
		videoIndexTwo = 2
		suppressStartEndSecondsList_2_1 = [4, 8]
		suppressStartEndSecondsList_2_2 = [11, 13]
		suppressStartEndSecondsList_2_3 = [15, 17]
		expectedSuppressedFileDuration_2 = 12.5
		videoFileName_2 = 'test_suppress_audio_file_second.mp4'
		downloadedVideoInfoDic.addVideoInfoForVideoIndex(videoIndexTwo, 'test_suppress_audio_file_second',
		                                                 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName_2)
		downloadedVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndexTwo, suppressStartEndSecondsList_2_1)
		downloadedVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndexTwo, suppressStartEndSecondsList_2_2)
		downloadedVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndexTwo, suppressStartEndSecondsList_2_3)
		
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
		
		audioExtractor.extractPlaylistAudio(downloadedVideoInfoDic)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = sorted(os.listdir(targetAudioDir))
		self.assertEqual(
			['test_suppress_audio_file.mp4',
			 'test_suppress_audio_file_full.mp3',
			 'test_suppress_audio_file_s.mp3',
			 'test_suppress_audio_file_second.mp4',
			 'test_suppress_audio_file_second_full.mp3',
			 'test_suppress_audio_file_second_s.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1_1 = videoAndAudioFileList[5]
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_1_1)
		self.assertAlmostEquals(expectedSuppressedFileDuration_2, audio.info.length, delta=0.1)

		self.assertIsNone(downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndexOne, extractedMp3FileName_1_1))

		self.assertEqual([['0:0:0', '0:0:2'], ['0:0:4', '0:0:8'], ['0:0:11', '0:0:13'], ['0:0:15', '0:0:17']], downloadedVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndexOne))
		self.assertEqual([['0:0:2', '0:0:4'], ['0:0:8', '0:0:11'], ['0:0:13', '0:0:15'], ['0:0:17', '0:0:20.43']], downloadedVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndexOne))

		extractedMp3FileName_2_1 = videoAndAudioFileList[2]
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_2_1)
		self.assertAlmostEquals(expectedSuppressedFileDuration_1, audio.info.length, delta=0.1)

		self.assertIsNone(downloadedVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndexTwo, extractedMp3FileName_2_1))

		self.assertEqual([["0:0:4", "0:0:8"], ["0:0:11", "0:0:13"], ["0:0:15", "0:0:17"]], downloadedVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndexTwo))
		self.assertEqual([['0:0:0', '0:0:4'], ['0:0:8', '0:0:11'], ['0:0:13', '0:0:15'], ['0:0:17', '0:0:20.43']], downloadedVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndexTwo))


if __name__ == '__main__':
#	unittest.main()
	tst = TestAudioExtractor()
	ts = time.time()
	tst.testSuppressAudioPortions_two_video_with_two_suppress_no_extract_timeframe_each()
	print(time.time() - ts)
