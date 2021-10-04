import unittest
import os, sys, inspect, shutil, glob, time
from io import StringIO
from os.path import sep

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from constants import *
from guioutputstub import GuiOutputStub
from audiocontroller import AudioController
from configmanager import ConfigManager
from dirutil import DirUtil
			
class TestAudioController(unittest.TestCase):

	def testExtractAudioFromVideoFile(self):
		testDirName = 'test_audible_mobizen'
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + testDirName + sep
		videoFileName = 'Short low video quality'
		videoFilePathName = targetAudioDir + videoFileName + '.mp4'
		
		expectedExtractedAudioFileDuration = 964.661
		
		# deleting mp3 files in test dir
		files = glob.glob(targetAudioDir + sep + '*.mp3')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput, ConfigManager(DirUtil.getAudioRootPath() + sep + 'audiodownloader.ini'))
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioController.extractAudioFromVideoFile(videoFilePathName)
		
		sys.stdout = stdout

		self.assertTrue(r'extracted audio file "{}Short low video quality.mp3" from video file "{}Short low video quality.mp4"'.format(targetAudioDir, targetAudioDir) in outputCapturingString.getvalue())

		videoAndAudioFileList = os.listdir(targetAudioDir)

		self.assertEqual(
			['Short low video quality.mp3',
			 'Short low video quality.mp4'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName = videoAndAudioFileList[1]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName)
		self.assertAlmostEqual(expectedExtractedAudioFileDuration, audio.info.length, delta=0.1)

	def testGetPlaylistObjectAndTitlesForUrl_empty_url(self):
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput, ConfigManager(DirUtil.getAudioRootPath() + sep + 'audiodownloader.ini'))
		playlistUrl = ""
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			audioController.getPlaylistObjectAndTitlesForUrl(playlistUrl)
		
		sys.stdout = stdout
		
		self.assertEqual('the URL obtained from clipboard is empty.\nnothing to download.', accessError.errorMsg)
	
	def testGetPlaylistObjectAndTitlesForValidPlaylistUrl(self):
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(DirUtil.getAudioRootPath() + sep + 'audiodownloader.ini'))
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMTB7GasAttwVnPPk3-WTMNJ"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			audioController.getPlaylistObjectAndTitlesForUrl(playlistUrl)
		
		sys.stdout = stdout

		self.assertIsNone(accessError)
		self.assertIsNone(videoTitle)
		self.assertEqual('Test_title_one_time_frame_extract (e0:0:5-0:0:10)', playlistTitle)
		self.assertIsNotNone(playlistObject)
	
	def testGetPlaylistObjectAndTitlesForValidVideotUrl(self):
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(DirUtil.getAudioRootPath() + sep + 'audiodownloader.ini'))
		videoUrl = "https://youtu.be/LhH9uX3kgTI"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			audioController.getPlaylistObjectAndTitlesForUrl(videoUrl)
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertIsNone(playlistTitle)
		self.assertEqual('Is NEO Worth Buying? - Price Prediction 2020/2021 🚀🚀🚀', videoTitle)
		self.assertIsNotNone(playlistObject)

	def testClipAudioFile(self):
		playlistTitle = 'test_audio_controller_clip'
		playlistName = playlistTitle
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + playlistName
		audioFileName = 'LExpérience de Mort Imminente de Madame Mirjana Uzoh.mp3'
		audioFilePathName = targetAudioDir + sep + audioFileName
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(DirUtil.getAudioRootPath() + sep + 'audiodownloader.ini'))

		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		# deleting clipped mp3 files in test dir
		files = glob.glob(targetAudioDir + sep + '*_*.mp3')
		
		for f in files:
			os.remove(f)
		
		clipStartHHMMSS = '00:00:17'
		clipEndHHMMSS = '00:00:49'
		expectedClipFileDuration_1 = 32
		
		audioExtractorVideoInfoDic = audioController.clipAudioFile(audioFilePathName=audioFilePathName,
		                                                           clipStartHHMMSS=clipStartHHMMSS,
		                                                           clipEndHHMMSS=clipEndHHMMSS,
		                                                           floatSpeed=1.0)
		createdClipFilePathName = targetAudioDir + sep + audioExtractorVideoInfoDic.\
			getExtractedFilePathNameForVideoIndexTimeFrameIndex(videoIndex=1, timeFrameIndex=1)
		audioFileList = os.listdir(targetAudioDir)
		
		self.assertEqual('C:\\Users\\Jean-Pierre\\Downloads\\Audio\\test\\test_audio_controller_clip\\test\\test_audio_controller_clip\\LExpérience de Mort Imminente de Madame Mirjana Uzoh_1.mp3',
		                 createdClipFilePathName)
		self.assertEqual(
			['LExpérience de Mort Imminente de Madame Mirjana Uzoh.mp3',
			 'LExpérience de Mort Imminente de Madame Mirjana Uzoh_1.mp3'],
			audioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = audioFileList[1]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_1)
		self.assertAlmostEqual(expectedClipFileDuration_1, audio.info.length, delta=0.1)
	
	def testClipAudioFile_file_in_sub_dirs(self):
		playlistName = 'Test 3 short videos time frame deleted now should be ok'
		audioFileName = 'Here to help - Give him what he wants.mp3'
		playlistDownloadRootPath = 'Various\\test_to_del\\time frame supprimé\\{}'.format(playlistName)
		audioFilePath = DirUtil.getTestAudioRootPath() + sep + playlistDownloadRootPath
		audioFilePathName = audioFilePath + sep + audioFileName
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(DirUtil.getAudioRootPath() + sep + 'audiodownloader.ini'))
		
		# deleting clipped mp3 files in test dir
		files = glob.glob(audioFilePath + sep + '*_*.mp3')
		
		for f in files:
			os.remove(f)
		
		clipStartHHMMSS = '00:00:04'
		clipEndHHMMSS = '00:00:08'
		expectedClipFileDuration_1 = 4
		
		audioExtractorVideoInfoDic = audioController.clipAudioFile(audioFilePathName=audioFilePathName,
		                                                           clipStartHHMMSS=clipStartHHMMSS,
		                                                           clipEndHHMMSS=clipEndHHMMSS,
		                                                           floatSpeed=1.0)
		createdClipFilePathName = audioExtractorVideoInfoDic. \
			getExtractedFilePathNameForVideoIndexTimeFrameIndex(videoIndex=1, timeFrameIndex=1)

		self.assertEqual('test\\Various\\test_to_del\\time frame supprimé\\Test 3 short videos time frame deleted now should be ok\\Here to help - Give him what he wants_1.mp3',
		                 createdClipFilePathName)
		
		audioFileList = os.listdir(audioFilePath)
		
		self.assertEqual(
			['Funny suspicious looking dog.mp3',
			 'Here to help - Give him what he wants.mp3',
			 'Here to help - Give him what he wants_1.mp3',
			 'Test 3 short videos time frame deleted now should be ok_dic.txt',
			 'Wear a mask. Help slow the spread of Covid-19..mp3'],
			audioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = audioFileList[2]
		audio = MP3(audioFilePath + sep + extractedMp3FileName_1)
		self.assertAlmostEqual(expectedClipFileDuration_1, audio.info.length, delta=0.1)


if __name__ == '__main__':
#	unittest.main()
	tst = TestAudioController()
	tst.testClipAudioFile()
