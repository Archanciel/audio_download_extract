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
		files = glob.glob(targetAudioDir + DIR_SEP + '*.mp3')
		
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
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName)
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


if __name__ == '__main__':
#	unittest.main()
	tst = TestAudioController()
	tst.testGetPlaylistObjectAndTitlesForValidPlaylistUrl()
