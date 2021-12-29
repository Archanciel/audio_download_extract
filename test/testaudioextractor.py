import unittest
import os, sys, inspect, shutil, glob
from os.path import sep
from io import StringIO

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from constants import *
from guioutputstub import GuiOutputStub
from audioextractor import AudioExtractor
from downloadplaylistinfodic import DownloadPlaylistInfoDic
from dirutil import DirUtil

class TestAudioExtractor(unittest.TestCase):
	def testConvertSecondsTo_HHMMSS(self):
		audioExtractor = AudioExtractor(None, None, None)

		self.assertEqual('0:0:00', audioExtractor.convertSecondsTo_HHMMSS(0))
		self.assertEqual('0:0:06', audioExtractor.convertSecondsTo_HHMMSS(6))
		self.assertEqual('0:0:56', audioExtractor.convertSecondsTo_HHMMSS(56))
		self.assertEqual('0:1:56', audioExtractor.convertSecondsTo_HHMMSS(116))
		self.assertEqual('2:10:56', audioExtractor.convertSecondsTo_HHMMSS(7856))

	def testConvertStartEndSecondsListTo_HHMMSS_TimeFrameList(self):
		audioExtractor = AudioExtractor(None, None, None)

		self.assertEqual(['0:0:56', '2:10:56'], audioExtractor.convertStartEndSecondsListTo_HHMMSS_TimeFrameList([56, 7856]))
	
	def testExtractAudioPortions_one_video_with_no_extract_no_suppress_timeframe(self):
		playlistTitle = 'test_audio_extractor'
		playlistName = playlistTitle
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + playlistName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		downloadVideoInfoDic = DownloadPlaylistInfoDic('', targetAudioDir, targetAudioDir, playlistTitle, playlistName, playlistTitle, playlistName)
		videoFileName = 'Wear a mask Help slow the spread of Covid-19.mp4'
		downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'Wear a mask. Help slow the spread of Covid-19.',
														 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName)
		
		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName,
					targetAudioDir + '\\' + videoFileName)
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadVideoInfoDic)
		
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
		
		self.assertIsNone(downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex, extractedMp3FileName))
		
		self.assertIsNone(downloadVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertIsNone(downloadVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
	
	def testExtractAudioPortions_one_video_with_one_extract_no_suppress_timeframe(self):
		playlistTitle = 'test_audio_extractor'
		playlistName = playlistTitle
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + playlistName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		startEndSecondsList = [5, 10]
		expectedExtractedFileDuration = startEndSecondsList[1] - startEndSecondsList[0]
		downloadVideoInfoDic = DownloadPlaylistInfoDic('', targetAudioDir, targetAudioDir, playlistTitle, playlistName, playlistTitle, playlistName)
		videoFileName = 'Wear a mask Help slow the spread of Covid-19.mp4'
		downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'Wear a mask. Help slow the spread of Covid-19.',
											'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName)
		downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList)

		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + sep + '*')
		
		for f in files:
			os.remove(f)

		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName,
					targetAudioDir + '\\' + videoFileName)
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadVideoInfoDic)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtractor.extractAudioPortions(videoIndex, downloadVideoInfoDic)

		sys.stdout = stdout

		videoAndAudioFileList = os.listdir(targetAudioDir)
		self.assertEqual(['Wear a mask Help slow the spread of Covid-19.mp4', 'Wear a mask Help slow the spread of Covid-19_1.mp3'], videoAndAudioFileList)

		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = videoAndAudioFileList[1]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_1)
		self.assertAlmostEqual(expectedExtractedFileDuration, audio.info.length, delta=0.1)

		self.assertEqual(["0:0:05", "0:0:10"], downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex, extractedMp3FileName_1))
		
		self.assertIsNone(downloadVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertIsNone(downloadVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))

	def testExtractAudioPortions_one_video_with_one_extract_no_suppress_timeframe_endTimeTooBig(self):
		playlistTitle = 'test_audio_extractor_extractEndTimeTooBig'
		playlistName = playlistTitle
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + playlistName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		startEndSecondsList = [5, 20]
		expectedExtractedFileDuration = startEndSecondsList[1] - startEndSecondsList[0]
		downloadVideoInfoDic = DownloadPlaylistInfoDic('', targetAudioDir, targetAudioDir, playlistTitle, playlistName,
		                                               playlistTitle, playlistName)
		videoFileName = 'Wear a mask Help slow the spread of Covid-19.mp4'
		downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'Wear a mask. Help slow the spread of Covid-19.',
		                                               'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName)
		downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList)
		
		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName,
		            targetAudioDir + '\\' + videoFileName)
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadVideoInfoDic)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtractor.extractAudioPortions(videoIndex, downloadVideoInfoDic)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = os.listdir(targetAudioDir)
		self.assertEqual(
			['Wear a mask Help slow the spread of Covid-19.mp4', 'Wear a mask Help slow the spread of Covid-19_1.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = videoAndAudioFileList[1]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_1)
		self.assertAlmostEqual(expectedExtractedFileDuration, audio.info.length, delta=0.1)
		
		self.assertEqual(["0:0:05", "0:0:10"],
		                 downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex,
		                                                                                      extractedMp3FileName_1))
		
		self.assertIsNone(downloadVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertIsNone(downloadVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
	
	def testExtractAudioPortions_one_video_with_one_extract_no_suppress_timeframe_startAfterEnd(self):
		playlistTitle = 'test_audio_extractor_extractStartAfterEnd'
		playlistName = playlistTitle
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + playlistName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		startEndSecondsList = [12, 10]
		expectedExtractedFileDuration = startEndSecondsList[1] - startEndSecondsList[0]
		downloadVideoInfoDic = DownloadPlaylistInfoDic('', targetAudioDir, targetAudioDir, playlistTitle, playlistName,
		                                               playlistTitle, playlistName)
		videoFileName = 'Wear a mask Help slow the spread of Covid-19.mp4'
		downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'Wear a mask. Help slow the spread of Covid-19.',
		                                               'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName)
		downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList)
		
		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName,
		            targetAudioDir + '\\' + videoFileName)
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadVideoInfoDic)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtractor.extractAudioPortions(videoIndex, downloadVideoInfoDic)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = os.listdir(targetAudioDir)
		self.assertEqual(
			['Wear a mask Help slow the spread of Covid-19.mp4', 'Wear a mask Help slow the spread of Covid-19_1.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = videoAndAudioFileList[1]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_1)
		self.assertAlmostEqual(expectedExtractedFileDuration, audio.info.length, delta=0.1)
		
		self.assertEqual(["0:0:05", "0:0:10"],
		                 downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex,
		                                                                                      extractedMp3FileName_1))
		
		self.assertIsNone(downloadVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertIsNone(downloadVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
	
	def testExtractAudioPortions_one_video_with_one_extract_no_suppress_timeframe_doubleSpeed(self):
		playlistTitle = 'test_audio_extractor'
		playlistName = playlistTitle
		
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + playlistName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		startEndSecondsList = [5, 10]
		expectedExtractedFileDuration = 2.56 # speed is doubled
		downloadVideoInfoDic = DownloadPlaylistInfoDic('', targetAudioDir, targetAudioDir, playlistTitle, playlistName, playlistTitle, playlistName)
		videoFileName = 'Wear a mask Help slow the spread of Covid-19.mp4'
		downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'Wear a mask. Help slow the spread of Covid-19.',
													   'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName)
		downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList)
		
		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName,
					targetAudioDir + '\\' + videoFileName)
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadVideoInfoDic)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtractor.extractAudioPortions(videoIndex, downloadVideoInfoDic, floatSpeed=2.0)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = os.listdir(targetAudioDir)
		self.assertEqual(
			['Wear a mask Help slow the spread of Covid-19.mp4', 'Wear a mask Help slow the spread of Covid-19_1.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = videoAndAudioFileList[1]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_1)
		self.assertAlmostEqual(expectedExtractedFileDuration, audio.info.length, delta=0.1)
		
		self.assertEqual(["0:0:05", "0:0:10"],
						 downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex,
																							  extractedMp3FileName_1))
		
		self.assertIsNone(downloadVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertIsNone(downloadVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
	
	def testExtractAudioPortions_one_video_with_one_extract_no_suppress_timeframe_extract_from_0(self):
		playlistTitle = 'test_audio_extractor'
		playlistName = playlistTitle
		
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + playlistName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		startEndSecondsList = [0, 5]
		expectedExtractedFileDuration = startEndSecondsList[1] - startEndSecondsList[0]
		downloadVideoInfoDic = DownloadPlaylistInfoDic('', targetAudioDir, targetAudioDir, playlistTitle, playlistName, playlistTitle, playlistName)
		videoFileName = 'Wear a mask Help slow the spread of Covid-19.mp4'
		downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'Wear a mask. Help slow the spread of Covid-19.',
														 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName)
		downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList)
		
		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName,
					targetAudioDir + '\\' + videoFileName)
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadVideoInfoDic)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtractor.extractAudioPortions(videoIndex, downloadVideoInfoDic)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = os.listdir(targetAudioDir)
		self.assertEqual(
			['Wear a mask Help slow the spread of Covid-19.mp4', 'Wear a mask Help slow the spread of Covid-19_1.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = videoAndAudioFileList[1]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_1)
		self.assertAlmostEqual(expectedExtractedFileDuration, audio.info.length, delta=0.1)
		
		self.assertEqual(["0:0:00", "0:0:05"],
						 downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex,
																								extractedMp3FileName_1))
		
		self.assertIsNone(downloadVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertIsNone(downloadVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))

	def testExtractAudioPortions_one_video_with_one_extract_no_suppress_timeframe_extract_from_n_to_end(self):
		playlistTitle = 'test_audio_extractor'
		playlistName = playlistTitle
		
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + playlistName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		startEndSecondsList = [10, 'end']
		expectedExtractedFileDuration = 4.7
		downloadVideoInfoDic = DownloadPlaylistInfoDic('', targetAudioDir, targetAudioDir, playlistTitle, playlistName, playlistTitle, playlistName)
		videoFileName = 'Wear a mask Help slow the spread of Covid-19.mp4'
		downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'Wear a mask. Help slow the spread of Covid-19.',
														 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName)
		downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList)
		
		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName,
					targetAudioDir + '\\' + videoFileName)
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadVideoInfoDic)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtractor.extractAudioPortions(videoIndex, downloadVideoInfoDic)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = os.listdir(targetAudioDir)
		self.assertEqual(
			['Wear a mask Help slow the spread of Covid-19.mp4', 'Wear a mask Help slow the spread of Covid-19_1.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = videoAndAudioFileList[1]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_1)
		self.assertAlmostEqual(expectedExtractedFileDuration, audio.info.length, delta=0.1)
		
		self.assertEqual(['0:0:10', '0:0:15'],
						 downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex,
																								extractedMp3FileName_1))
		
		self.assertIsNone(downloadVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertIsNone(downloadVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
	
	def testExtractAudioPortions_one_video_with_two_extract_no_suppress_timeframe(self):
		playlistTitle = 'test_audio_extractor'
		playlistName = playlistTitle
		
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + playlistName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		startEndSecondsList_extract_1 = [5, 10]
		expectedExtractedFileDuration_1 = startEndSecondsList_extract_1[1] - startEndSecondsList_extract_1[0]

		startEndSecondsList_extract_2 = [11, 13]
		expectedExtractedFileDuration_2 = startEndSecondsList_extract_2[1] - startEndSecondsList_extract_2[0]

		downloadVideoInfoDic = DownloadPlaylistInfoDic('', targetAudioDir, targetAudioDir, playlistTitle, playlistName, playlistTitle, playlistName)
		videoFileName = 'Wear a mask Help slow the spread of Covid-19.mp4'
		downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'Wear a mask. Help slow the spread of Covid-19.',
														 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName)
		downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList_extract_1)
		downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList_extract_2)

		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName,
					targetAudioDir + '\\' + videoFileName)

		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadVideoInfoDic)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtractor.extractAudioPortions(videoIndex, downloadVideoInfoDic)
		
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
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_1)
		self.assertAlmostEqual(expectedExtractedFileDuration_1, audio.info.length, delta=0.1)
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_2)
		self.assertAlmostEqual(expectedExtractedFileDuration_2, audio.info.length, delta=0.1)

		self.assertEqual(["0:0:05", "0:0:10"], downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex, extractedMp3FileName_1))
		self.assertEqual(["0:0:11", "0:0:13"], downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex, extractedMp3FileName_2))
		
		self.assertIsNone(downloadVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertIsNone(downloadVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
	
	def testExtractAudioPortions_one_mp3_with_two_superposed_extract_no_suppress_timeframe(self):
		playlistTitle = 'test_audio_extractor'
		playlistName = playlistTitle
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + playlistName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		startEndSecondsList_extract_1 = [2, 'end']
		expectedExtractedFileDuration_1 = 63
		
		startEndSecondsList_extract_2 = [3, 'end']
		expectedExtractedFileDuration_2 = 62
		
		downloadVideoInfoDic = DownloadPlaylistInfoDic('', targetAudioDir, targetAudioDir, playlistTitle, playlistName, playlistTitle, playlistName)
		audioFileName = 'LExpérience de Mort Imminente de Madame Mirjana Uzoh.mp3'
		downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, "L'Expérience de Mort Imminente de Madame Mirjana Uzoh",
														 'https://youtube.com/watch?v=9iPvLx7gotk', audioFileName)
		downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList_extract_1)
		downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList_extract_2)
		
		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + audioFileName,
					targetAudioDir + '\\' + audioFileName)
		
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadVideoInfoDic)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtractor.extractAudioPortions(videoIndex, downloadVideoInfoDic)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = os.listdir(targetAudioDir)
		self.assertEqual(
			['LExpérience de Mort Imminente de Madame Mirjana Uzoh.mp3',
			 'LExpérience de Mort Imminente de Madame Mirjana Uzoh_1.mp3',
			 'LExpérience de Mort Imminente de Madame Mirjana Uzoh_2.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = videoAndAudioFileList[1]
		extractedMp3FileName_2 = videoAndAudioFileList[2]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_1)
		self.assertAlmostEqual(expectedExtractedFileDuration_1, audio.info.length, delta=0.1)
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_2)
		self.assertAlmostEqual(expectedExtractedFileDuration_2, audio.info.length, delta=0.1)
		
		self.assertEqual(["0:0:02", "0:1:05"],
						 downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex,
																								extractedMp3FileName_1))
		self.assertEqual(["0:0:03", "0:1:05"],
						 downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex,
																								extractedMp3FileName_2))
		
		self.assertIsNone(downloadVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertIsNone(downloadVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
	
	def testExtractAudioPortions_one_video_with_two_extract_no_suppress_timeframe_last_extract_to_end(self):
		playlistTitle = 'test_audio_extractor'
		playlistName = playlistTitle
		
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + playlistName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		startEndSecondsList_1 = [5, 10]
		expectedExtractedFileDuration_1 = startEndSecondsList_1[1] - startEndSecondsList_1[0]
		
		startEndSecondsList_2 = [11, 'end']
		expectedExtractedFileDuration_2 = 3.7
		
		downloadVideoInfoDic = DownloadPlaylistInfoDic('', targetAudioDir, targetAudioDir, playlistTitle, playlistName, playlistTitle, playlistName)
		videoFileName = 'Wear a mask Help slow the spread of Covid-19.mp4'
		downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'Wear a mask. Help slow the spread of Covid-19.',
														 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName)
		downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList_1)
		downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList_2)
		
		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName,
					targetAudioDir + '\\' + videoFileName)
		
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadVideoInfoDic)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtractor.extractAudioPortions(videoIndex, downloadVideoInfoDic)
		
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
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_1)
		self.assertAlmostEqual(expectedExtractedFileDuration_1, audio.info.length, delta=0.1)
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_2)
		self.assertAlmostEqual(expectedExtractedFileDuration_2, audio.info.length, delta=0.1)
		
		self.assertEqual(["0:0:05", "0:0:10"],
						 downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex,
																								extractedMp3FileName_1))
		self.assertEqual(["0:0:11", "0:0:15"],
						 downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex,
																								extractedMp3FileName_2))
		
		self.assertIsNone(downloadVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertIsNone(downloadVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
	
	def testExtractAudioPortions_two_video_with_two_extract_no_suppress_timeframe_each(self):
		playlistTitle = 'test_audio_extractor'
		playlistName = playlistTitle
		
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + playlistName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)

		# first video		
		videoIndexOne = 1
		startEndSecondsList_1_1 = [5, 10]
		expectedExtractedFileDuration_1_1 = startEndSecondsList_1_1[1] - startEndSecondsList_1_1[0]
		
		startEndSecondsList_1_2 = [11, 13]
		expectedExtractedFileDuration_1_2 = startEndSecondsList_1_2[1] - startEndSecondsList_1_2[0]
		
		downloadVideoInfoDic = DownloadPlaylistInfoDic('', targetAudioDir, targetAudioDir, playlistTitle, playlistName, playlistTitle, playlistName)
		videoFileName_1 = 'Wear a mask Help slow the spread of Covid-19.mp4'
		downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndexOne, 'Wear a mask. Help slow the spread of Covid-19.',
														 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName_1)
		downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndexOne, startEndSecondsList_1_1)
		downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndexOne, startEndSecondsList_1_2)
		
		# second video		
		videoIndexTwo = 2
		startEndSecondsList_2_1 = [3, 8]
		expectedExtractedFileDuration_2_1 = startEndSecondsList_2_1[1] - startEndSecondsList_2_1[0]
		
		startEndSecondsList_2_2 = [10, 13]
		expectedExtractedFileDuration_2_2 = startEndSecondsList_2_2[1] - startEndSecondsList_2_2[0]
		
		videoFileName_2 = 'Here to help Give him what he wants.mp4'
		downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndexTwo, 'Here to help: Give him what he wants downloaded.',
														 'https://youtube.com/watch?v=Eqy6M6qLWGw', videoFileName_2)
		downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndexTwo, startEndSecondsList_2_1)
		downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndexTwo, startEndSecondsList_2_2)
		
		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName_1,
					targetAudioDir + '\\' + videoFileName_1)
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName_2,
					targetAudioDir + '\\' + videoFileName_2)
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadVideoInfoDic)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtractor.extractPlaylistAudio(downloadVideoInfoDic)
		
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
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_1_1)
		self.assertAlmostEqual(expectedExtractedFileDuration_1_1, audio.info.length, delta=0.1)
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_1_2)
		self.assertAlmostEqual(expectedExtractedFileDuration_1_2, audio.info.length, delta=0.1)
		
		extractedMp3FileName_2_1 = videoAndAudioFileList[1]
		extractedMp3FileName_2_2 = videoAndAudioFileList[2]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_2_1)
		self.assertAlmostEqual(expectedExtractedFileDuration_2_1, audio.info.length, delta=0.1)
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_2_2)
		self.assertAlmostEqual(expectedExtractedFileDuration_2_2, audio.info.length, delta=0.1)

		self.assertEqual(["0:0:05", "0:0:10"], downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndexOne, extractedMp3FileName_1_1))
		self.assertEqual(["0:0:11", "0:0:13"], downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndexOne, extractedMp3FileName_1_2))
		
		self.assertIsNone(downloadVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndexOne))
		self.assertIsNone(downloadVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndexOne))
		
		extractedMp3FileName_2_1 = videoAndAudioFileList[1]
		extractedMp3FileName_2_2 = videoAndAudioFileList[2]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_2_1)
		self.assertAlmostEqual(expectedExtractedFileDuration_2_1, audio.info.length, delta=0.1)
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_2_2)
		self.assertAlmostEqual(expectedExtractedFileDuration_2_2, audio.info.length, delta=0.1)
		
		self.assertEqual(["0:0:03", "0:0:08"], downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndexTwo, extractedMp3FileName_2_1))
		self.assertEqual(["0:0:10", "0:0:13"], downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndexTwo, extractedMp3FileName_2_2))
		
		self.assertIsNone(downloadVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndexTwo))
		self.assertIsNone(downloadVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndexTwo))
	
	def testSuppressAudioPortions_one_video_with_no_extract_and_three_suppress_timeframe(self):
		playlistTitle = 'test_audio_extractor'
		playlistName = playlistTitle
		
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + playlistName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		suppressStartEndSecondsList_1 = [4, 8]
		suppressStartEndSecondsList_2 = [11, 13]
		suppressStartEndSecondsList_3 = [15, 17]
		expectedExtractedFileDuration = 12.5
		downloadVideoInfoDic = DownloadPlaylistInfoDic('', targetAudioDir, targetAudioDir, playlistTitle, playlistName, playlistTitle, playlistName)
		videoFileName = 'test_suppress_audio_file.mp4'
		downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'test_suppress_audio_file.',
														 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_1)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_2)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_3)
		
		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName,
					targetAudioDir + '\\' + videoFileName)
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadVideoInfoDic)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtractor.suppressAudioPortions(videoIndex, videoFileName, downloadVideoInfoDic)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = os.listdir(targetAudioDir)

		self.assertEqual(
			['test_suppress_audio_file.mp4', 'test_suppress_audio_file_s.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = videoAndAudioFileList[1]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_1)
		self.assertAlmostEqual(expectedExtractedFileDuration, audio.info.length, delta=0.1)

		self.assertIsNone(downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex, extractedMp3FileName_1))

		self.assertEqual([["0:0:04", "0:0:08"], ["0:0:11", "0:0:13"], ["0:0:15", "0:0:17"]], downloadVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertEqual([['0:0:00', '0:0:04'], ['0:0:08', '0:0:11'], ['0:0:13', '0:0:15'], ['0:0:17', '0:0:20']], downloadVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
	
	def testSuppressAudioPortions_one_video_with_no_extract_and_three_suppress_timeframe_last_suppress_to_end(self):
		playlistTitle = 'test_audio_extractor'
		playlistName = playlistTitle
		
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + playlistName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		suppressStartEndSecondsList_1 = [4, 8]
		suppressStartEndSecondsList_2 = [11, 13]
		suppressStartEndSecondsList_3 = [15, 'end']
		expectedExtractedFileDuration = 9.03
		downloadVideoInfoDic = DownloadPlaylistInfoDic('', targetAudioDir, targetAudioDir, playlistTitle, playlistName, playlistTitle, playlistName)
		videoFileName = 'test_suppress_audio_file.mp4'
		downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'test_suppress_audio_file.',
														 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_1)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_2)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_3)
		
		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName,
					targetAudioDir + '\\' + videoFileName)
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadVideoInfoDic)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtractor.suppressAudioPortions(videoIndex, videoFileName, downloadVideoInfoDic)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = os.listdir(targetAudioDir)
		
		self.assertEqual(
			['test_suppress_audio_file.mp4', 'test_suppress_audio_file_s.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = videoAndAudioFileList[1]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_1)
		self.assertAlmostEqual(expectedExtractedFileDuration, audio.info.length, delta=0.1)
		
		self.assertIsNone(
			downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex, extractedMp3FileName_1))
		
		self.assertEqual([["0:0:04", "0:0:08"], ["0:0:11", "0:0:13"], ["0:0:15", '0:0:20']],
						 downloadVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertEqual([['0:0:00', '0:0:04'], ['0:0:08', '0:0:11'], ['0:0:13', '0:0:15']],
						 downloadVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))

	def testSuppressAudioPortions_one_video_with_no_extract_and_one_suppress_timeframe_starting_at_zero_endTimeTooBig(self):
		playlistTitle = 'test_audio_extractor_suppressEndTimeTooBig'
		playlistName = playlistTitle
		
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + playlistName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		suppressStartEndSecondsList_1 = [0, 60]
		expectedSuppressedFileDuration = 0.4
		downloadVideoInfoDic = DownloadPlaylistInfoDic('', targetAudioDir, targetAudioDir, playlistTitle, playlistName,
		                                               playlistTitle, playlistName)
		videoFileName = 'test_suppress_audio_file.mp4'
		downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'test_suppress_audio_file.',
		                                               'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_1)
		
		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName,
		            targetAudioDir + '\\' + videoFileName)
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadVideoInfoDic)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		audioExtractor.suppressAudioPortions(videoIndex, videoFileName, downloadVideoInfoDic)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = os.listdir(targetAudioDir)
		
		self.assertEqual(
			['test_suppress_audio_file.mp4', 'test_suppress_audio_file_s.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = videoAndAudioFileList[1]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_1)
		self.assertAlmostEqual(expectedSuppressedFileDuration, audio.info.length, delta=0.1)
		
		self.assertIsNone(
			downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex, extractedMp3FileName_1))
		
		self.assertEqual([['0:0:00', '0:0:02']],
		                 downloadVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertEqual([['0:0:02', '0:0:20']],
		                 downloadVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
	
	def testSuppressAudioPortions_one_video_with_no_extract_and_one_suppress_timeframe_starting_at_zero_startAfterEndTime(
			self):
		playlistTitle = 'test_audio_extractor'
		playlistName = playlistTitle
		
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + playlistName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		suppressStartEndSecondsList_1 = [65, 2]
		expectedSuppressedFileDuration = 18.4
		downloadVideoInfoDic = DownloadPlaylistInfoDic('', targetAudioDir, targetAudioDir, playlistTitle, playlistName,
		                                               playlistTitle, playlistName)
		videoFileName = 'test_suppress_audio_file.mp4'
		downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'test_suppress_audio_file.',
		                                               'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_1)
		
		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName,
		            targetAudioDir + '\\' + videoFileName)
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadVideoInfoDic)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		audioExtractor.suppressAudioPortions(videoIndex, videoFileName, downloadVideoInfoDic)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = os.listdir(targetAudioDir)
		
		self.assertEqual(
			['test_suppress_audio_file.mp4', 'test_suppress_audio_file_s.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = videoAndAudioFileList[1]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_1)
		self.assertAlmostEqual(expectedSuppressedFileDuration, audio.info.length, delta=0.1)
		
		self.assertIsNone(
			downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex, extractedMp3FileName_1))
		
		self.assertEqual([['0:0:00', '0:0:02']],
		                 downloadVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertEqual([['0:0:02', '0:0:20']],
		                 downloadVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
	
	def testSuppressAudioPortions_one_video_with_no_extract_and_four_suppress_timeframe_one_starting_at_zero(self):
		playlistTitle = 'test_audio_extractor'
		playlistName = playlistTitle
		
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + playlistName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1
		suppressStartEndSecondsList_1 = [0, 2]
		suppressStartEndSecondsList_2 = [4, 8]
		suppressStartEndSecondsList_3 = [11, 13]
		suppressStartEndSecondsList_4 = [15, 17]
		expectedSuppressedFileDuration = 10.4
		downloadVideoInfoDic = DownloadPlaylistInfoDic('', targetAudioDir, targetAudioDir, playlistTitle, playlistName, playlistTitle, playlistName)
		videoFileName = 'test_suppress_audio_file.mp4'
		downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'test_suppress_audio_file.',
														 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_1)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_2)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_3)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_4)

		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName,
					targetAudioDir + '\\' + videoFileName)
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadVideoInfoDic)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		audioExtractor.suppressAudioPortions(videoIndex, videoFileName, downloadVideoInfoDic)

		sys.stdout = stdout
		
		videoAndAudioFileList = os.listdir(targetAudioDir)
		
		self.assertEqual(
			['test_suppress_audio_file.mp4', 'test_suppress_audio_file_s.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = videoAndAudioFileList[1]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_1)
		self.assertAlmostEqual(expectedSuppressedFileDuration, audio.info.length, delta=0.1)

		self.assertIsNone(downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex, extractedMp3FileName_1))

		self.assertEqual([['0:0:00', '0:0:02'], ['0:0:04', '0:0:08'], ['0:0:11', '0:0:13'], ['0:0:15', '0:0:17']], downloadVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertEqual([['0:0:02', '0:0:04'], ['0:0:08', '0:0:11'], ['0:0:13', '0:0:15'], ['0:0:17', '0:0:20']], downloadVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
	
	def testSuppressAudioPortions_two_video_with_two_suppress_no_extract_timeframe_each(self):
		playlistTitle = 'test_audio_extractor'
		playlistName = playlistTitle
		
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + playlistName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		# first video
		videoIndexOne = 1
		suppressStartEndSecondsList_1_1 = [0, 2]
		suppressStartEndSecondsList_1_2 = [4, 8]
		suppressStartEndSecondsList_1_3 = [11, 13]
		suppressStartEndSecondsList_1_4 = [15, 17]
		expectedSuppressedFileDuration_1 = 10.4
		downloadVideoInfoDic = DownloadPlaylistInfoDic('', targetAudioDir, targetAudioDir, playlistTitle, playlistName, playlistTitle, playlistName)
		videoFileName_1 = 'test_suppress_audio_file.mp4'
		downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndexOne, 'test_suppress_audio_file.',
														 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName_1)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndexOne, suppressStartEndSecondsList_1_1)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndexOne, suppressStartEndSecondsList_1_2)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndexOne, suppressStartEndSecondsList_1_3)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndexOne, suppressStartEndSecondsList_1_4)
		
		# second video
		videoIndexTwo = 2
		suppressStartEndSecondsList_2_1 = [4, 8]
		suppressStartEndSecondsList_2_2 = [11, 13]
		suppressStartEndSecondsList_2_3 = [15, 17]
		expectedSuppressedFileDuration_2 = 12.5
		videoFileName_2 = 'test_suppress_audio_file_second.mp4'
		downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndexTwo, 'test_suppress_audio_file_second',
														 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName_2)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndexTwo, suppressStartEndSecondsList_2_1)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndexTwo, suppressStartEndSecondsList_2_2)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndexTwo, suppressStartEndSecondsList_2_3)
		
		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName_1,
					targetAudioDir + '\\' + videoFileName_1)
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName_2,
					targetAudioDir + '\\' + videoFileName_2)
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadVideoInfoDic)
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtractor.extractPlaylistAudio(downloadVideoInfoDic)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = sorted(os.listdir(targetAudioDir))
		self.assertEqual(
			['test_suppress_audio_file.mp4',
			 'test_suppress_audio_file_s.mp3',
			 'test_suppress_audio_file_second.mp4',
			 'test_suppress_audio_file_second_s.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1_1 = videoAndAudioFileList[3]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_1_1)
		self.assertAlmostEqual(expectedSuppressedFileDuration_2, audio.info.length, delta=0.1)

		self.assertIsNone(downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndexOne, extractedMp3FileName_1_1))

		self.assertEqual([['0:0:00', '0:0:02'], ['0:0:04', '0:0:08'], ['0:0:11', '0:0:13'], ['0:0:15', '0:0:17']], downloadVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndexOne))
		self.assertEqual([['0:0:02', '0:0:04'], ['0:0:08', '0:0:11'], ['0:0:13', '0:0:15'], ['0:0:17', '0:0:20']], downloadVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndexOne))

		extractedMp3FileName_2_1 = videoAndAudioFileList[1]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_2_1)
		self.assertAlmostEqual(expectedSuppressedFileDuration_1, audio.info.length, delta=0.1)

		self.assertIsNone(downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndexTwo, extractedMp3FileName_2_1))

		self.assertEqual([["0:0:04", "0:0:08"], ["0:0:11", "0:0:13"], ["0:0:15", "0:0:17"]], downloadVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndexTwo))
		self.assertEqual([['0:0:00', '0:0:04'], ['0:0:08', '0:0:11'], ['0:0:13', '0:0:15'], ['0:0:17', '0:0:20']], downloadVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndexTwo))
	
	def testSuppressAudioPortions_one_video_with_two_extract_and_three_suppress_timeframe(self):
		playlistTitle = 'test_audio_extractor'
		playlistName = playlistTitle
		
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + playlistName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		videoIndex = 1

		# setting extract time frames
		startEndSecondsList_extract_1 = [5, 10]
		expectedExtractedFileDuration_1 = startEndSecondsList_extract_1[1] - startEndSecondsList_extract_1[0]

		startEndSecondsList_extract_2 = [11, 13]
		expectedExtractedFileDuration_2 = startEndSecondsList_extract_2[1] - startEndSecondsList_extract_2[0]

		downloadVideoInfoDic = DownloadPlaylistInfoDic('', targetAudioDir, targetAudioDir, playlistTitle, playlistName, playlistTitle, playlistName)
		videoFileName = 'test_extract_suppress_audio_file_one.mp4'
		downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, 'test_suppress_audio_file_one.',
														 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileName)
		downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList_extract_1)
		downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList_extract_2)

		# setting suppress time frames
		suppressStartEndSecondsList_suppress_1 = [4, 8]
		suppressStartEndSecondsList_suppress_2 = [11, 13]
		suppressStartEndSecondsList_suppress_3 = [15, 17]
		expectedSuppressedFileDuration = 12.5

		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_suppress_1)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_suppress_2)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, suppressStartEndSecondsList_suppress_3)
		
		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileName,
					targetAudioDir + '\\' + videoFileName)
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadVideoInfoDic)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtractor.extractPlaylistAudio(downloadVideoInfoDic)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = os.listdir(targetAudioDir)
		
		self.assertEqual(
			['test_extract_suppress_audio_file_one.mp4',
			 'test_extract_suppress_audio_file_one_1.mp3',
			 'test_extract_suppress_audio_file_one_2.mp3',
			 'test_extract_suppress_audio_file_one_s.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3

		# testing extract time frames
		extractedMp3FileName_1 = videoAndAudioFileList[1]
		extractedMp3FileName_2 = videoAndAudioFileList[2]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_1)
		self.assertAlmostEqual(expectedExtractedFileDuration_1, audio.info.length, delta=0.1)
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_2)
		self.assertAlmostEqual(expectedExtractedFileDuration_2, audio.info.length, delta=0.1)

		self.assertEqual(["0:0:05", "0:0:10"], downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex, extractedMp3FileName_1))
		self.assertEqual(["0:0:11", "0:0:13"], downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex, extractedMp3FileName_2))
		
		# testing suppress time frame
		extractedMp3FileName_3 = videoAndAudioFileList[3]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_3)
		self.assertAlmostEqual(expectedSuppressedFileDuration, audio.info.length, delta=0.1)
		
		self.assertIsNone(
			downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndex, extractedMp3FileName_3))
		
		self.assertEqual([["0:0:04", "0:0:08"], ["0:0:11", "0:0:13"], ["0:0:15", "0:0:17"]],
						 downloadVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
		self.assertEqual([['0:0:00', '0:0:04'], ['0:0:08', '0:0:11'], ['0:0:13', '0:0:15'], ['0:0:17', '0:0:20']],
						 downloadVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndex))
	
	def testSuppressAudioPortions_two_videos_with_two_extract_and_three_suppress_timeframe(self):
		playlistTitle = 'test_audio_extractor'
		playlistName = playlistTitle
		
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + playlistName
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		# setting video one

		videoIndexOne = 1
		
		# setting extract time frames
		startEndSecondsList_extract_1_1 = [5, 10]
		expectedExtractedFileDuration_1_1 = startEndSecondsList_extract_1_1[1] - startEndSecondsList_extract_1_1[0]
		
		startEndSecondsList_extract_1_2 = [11, 13]
		expectedExtractedFileDuration_1_2 = startEndSecondsList_extract_1_2[1] - startEndSecondsList_extract_1_2[0]
		
		downloadVideoInfoDic = DownloadPlaylistInfoDic('', targetAudioDir, targetAudioDir, playlistTitle, playlistName, playlistTitle, playlistName)
		videoFileNameOne = 'test_extract_suppress_audio_file_one.mp4'
		downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndexOne, 'test_suppress_audio_file_one.',
														 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileNameOne)
		downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndexOne, startEndSecondsList_extract_1_1)
		downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndexOne, startEndSecondsList_extract_1_2)
		
		# setting suppress time frames
		suppressStartEndSecondsList_suppress_1_1 = [4, 8]
		suppressStartEndSecondsList_suppress_1_2 = [11, 13]
		suppressStartEndSecondsList_suppress_1_3 = [15, 17]
		expectedSuppressedFileDuration = 12.5
		
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndexOne,
																		   suppressStartEndSecondsList_suppress_1_1)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndexOne,
																		   suppressStartEndSecondsList_suppress_1_2)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndexOne,
																		   suppressStartEndSecondsList_suppress_1_3)
		
		# setting video two
		
		videoIndexTwo = 2
		
		# setting extract time frames
		startEndSecondsList_extract_2_1 = [5, 9]
		expectedExtractedFileDuration_2_1 = startEndSecondsList_extract_2_1[1] - startEndSecondsList_extract_2_1[0]
		
		startEndSecondsList_extract_2_2 = [11, 14]
		expectedExtractedFileDuration_2_2 = startEndSecondsList_extract_2_2[1] - startEndSecondsList_extract_2_2[0]
		
		videoFileNameTwo = 'test_extract_suppress_audio_file_two.mp4'
		downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndexTwo, 'test_extract_suppress_audio_file_two.',
														 'https://youtube.com/watch?v=9iPvLx7gotk', videoFileNameTwo)
		downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndexTwo,
																		  startEndSecondsList_extract_2_1)
		downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndexTwo,
																		  startEndSecondsList_extract_2_2)
		
		# setting suppress time frames
		suppressStartEndSecondsList_suppress_2_1 = [4, 8]
		suppressStartEndSecondsList_suppress_2_2 = [11, 13]
		suppressStartEndSecondsList_suppress_2_3 = [15, 'end']
		expectedExtractedFileDuration_2 = 9.03
		
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndexTwo,
																		   suppressStartEndSecondsList_suppress_2_1)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndexTwo,
																		   suppressStartEndSecondsList_suppress_2_2)
		downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndexTwo,
																		   suppressStartEndSecondsList_suppress_2_3)
		
		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileNameOne,
					targetAudioDir + '\\' + videoFileNameOne)
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + videoFileNameTwo,
					targetAudioDir + '\\' + videoFileNameTwo)
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, downloadVideoInfoDic)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtractor.extractPlaylistAudio(downloadVideoInfoDic)
		
		sys.stdout = stdout
		
		videoAndAudioFileList = os.listdir(targetAudioDir)
		
		self.assertEqual(
			['test_extract_suppress_audio_file_one.mp4',
			 'test_extract_suppress_audio_file_one_1.mp3',
			 'test_extract_suppress_audio_file_one_2.mp3',
			 'test_extract_suppress_audio_file_one_s.mp3',
			 'test_extract_suppress_audio_file_two.mp4',
			 'test_extract_suppress_audio_file_two_1.mp3',
			 'test_extract_suppress_audio_file_two_2.mp3',
			 'test_extract_suppress_audio_file_two_s.mp3'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		
		# testing video one

		# testing extract time frames
		extractedMp3FileName_1_1 = videoAndAudioFileList[1]
		extractedMp3FileName_1_2 = videoAndAudioFileList[2]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_1_1)
		self.assertAlmostEqual(expectedExtractedFileDuration_1_1, audio.info.length, delta=0.1)
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_1_2)
		self.assertAlmostEqual(expectedExtractedFileDuration_1_2, audio.info.length, delta=0.1)
		
		self.assertEqual(["0:0:05", "0:0:10"],
						 downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndexOne,
																								extractedMp3FileName_1_1))
		self.assertEqual(["0:0:11", "0:0:13"],
						 downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndexOne,
																								extractedMp3FileName_1_2))
		
		# testing suppress time frame
		extractedMp3FileName_1_3 = videoAndAudioFileList[3]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_1_3)
		self.assertAlmostEqual(expectedSuppressedFileDuration, audio.info.length, delta=0.1)
		
		self.assertIsNone(
			downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndexOne, extractedMp3FileName_1_3))
		
		self.assertEqual([["0:0:04", "0:0:08"], ["0:0:11", "0:0:13"], ["0:0:15", "0:0:17"]],
						 downloadVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndexOne))
		self.assertEqual([['0:0:00', '0:0:04'], ['0:0:08', '0:0:11'], ['0:0:13', '0:0:15'], ['0:0:17', '0:0:20']],
						 downloadVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndexOne))
		
		# testing video two
		
		# testing extract time frames
		extractedMp3FileName_2_1 = videoAndAudioFileList[5]
		extractedMp3FileName_2_2 = videoAndAudioFileList[6]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_2_1)
		self.assertAlmostEqual(expectedExtractedFileDuration_2_1, audio.info.length, delta=0.1)
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_2_2)
		self.assertAlmostEqual(expectedExtractedFileDuration_2_2, audio.info.length, delta=0.1)
		
		self.assertEqual(["0:0:05", "0:0:09"],
						 downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndexTwo,
																								extractedMp3FileName_2_1))
		self.assertEqual(["0:0:11", "0:0:14"],
						 downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndexTwo,
																								extractedMp3FileName_2_2))
		
		# testing suppress time frame
		extractedMp3FileName_2_3 = videoAndAudioFileList[7]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_2_3)
		self.assertAlmostEqual(expectedExtractedFileDuration_2, audio.info.length, delta=0.1)
		
		self.assertIsNone(
			downloadVideoInfoDic.getStartEndHHMMSS_TimeFrameForExtractedFileName(videoIndexOne,
																				   extractedMp3FileName_2_3))
		
		self.assertEqual([["0:0:04", "0:0:08"], ["0:0:11", "0:0:13"], ["0:0:15", '0:0:20']],
						 downloadVideoInfoDic.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(videoIndexTwo))
		self.assertEqual([['0:0:00', '0:0:04'], ['0:0:08', '0:0:11'], ['0:0:13', '0:0:15']],
						 downloadVideoInfoDic.getKeptStartEndHHMMSS_TimeFramesForVideoIndex(videoIndexTwo))
	
	def testExtractAudioFromVideoFile(self):
		testDirName = 'test_audible_mobizen'
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + testDirName
		videoFileName = 'Short low video quality'
		videoFilePathName = targetAudioDir + sep + videoFileName + '.mp4'
		
		expectedExtractedAudioFileDuration = 964.661
		
		# deleting mp3 files in test dir
		files = glob.glob(targetAudioDir + sep + '*.mp3')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, {})
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtractor.extractAudioFromVideoFile(videoFilePathName)
		
		sys.stdout = stdout
		
		self.assertTrue(r'extracted audio file "{}Short low video quality.mp3" from video file "{}Short low video quality.mp4"'.format(targetAudioDir + sep, targetAudioDir + sep) in outputCapturingString.getvalue())

		videoAndAudioFileList = os.listdir(targetAudioDir)
		
		self.assertEqual(
			['Short low video quality.mp3',
			 'Short low video quality.mp4'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName = videoAndAudioFileList[1]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName)
		self.assertAlmostEqual(expectedExtractedAudioFileDuration, audio.info.length, delta=0.1)

	def testConcatenateAudioFiles(self):
		testDirName = "test_audio_extractor_concatenate"
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + testDirName
		audioFileName_1 = "Les vies où Jésus et Bouddha se connaissaient  1_22 L'histoire d'une noble amitié.mp3"
		audioFileName_2 = "Les vies où Jésus et Bouddha se connaissaient  2_22 L'histoire d'une noble amitié.mp3"
		sourceFileNameLst = [audioFileName_1, audioFileName_2]
		targetAudioFileName = 'concatenatedAudio.mp3'
		targetAudioFilePathName = targetAudioDir + sep + targetAudioFileName
		expectedTargetAudioFileDuration = 96.13
		
		try:
			os.remove(targetAudioFilePathName)
		except Exception:
			pass
		
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir, {})
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtractor.concatenateAudioFiles(audioSourcePath=targetAudioDir,
											 sourceFileNameLst=sourceFileNameLst,
											 targetFileName=targetAudioFileName)
		
		sys.stdout = stdout
		
		self.assertEqual(['',
 'Concatenating "Les vies où Jésus et Bouddha se connaissaient  1_22 '
 "L'histoire d'une noble amitié.mp3,",
 "Les vies où Jésus et Bouddha se connaissaient  2_22 L'histoire d'une noble "
 'amitié.mp3" ...',
 '',
 'MoviePy - Writing audio in '
 'D:\\Users\\Jean-Pierre\\Downloads\\Audio\\test\\test_audio_extractor_concatenate\\concatenatedAudio.mp3',
 'MoviePy - Done.',
 '',
 '"Les vies où Jésus et Bouddha se connaissaient  1_22 L\'histoire d\'une '
 'noble amitié.mp3,',
 "Les vies où Jésus et Bouddha se connaissaient  2_22 L'histoire d'une noble "
 'amitié.mp3 concatenated into "concatenatedAudio.mp3"',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		audioFileList = os.listdir(targetAudioDir)
		
		self.assertEqual(['concatenatedAudio.mp3',
 "Les vies où Jésus et Bouddha se connaissaient  1_22 L'histoire d'une noble "
 'amitié.mp3',
 "Les vies où Jésus et Bouddha se connaissaient  2_22 L'histoire d'une noble "
 'amitié.mp3'],
			audioFileList)
		
		from mutagen.mp3 import MP3
		audio = MP3(targetAudioFilePathName)
		self.assertAlmostEqual(expectedTargetAudioFileDuration, audio.info.length, delta=0.1)


if __name__ == '__main__':
#	unittest.main()
	tst = TestAudioExtractor()
	tst.testExtractAudioPortions_one_mp3_with_two_superposed_extract_no_suppress_timeframe()
