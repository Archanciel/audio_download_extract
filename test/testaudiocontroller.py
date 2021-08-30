import unittest
import os, sys, inspect, shutil, glob, time
from io import StringIO

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from constants import *
from guioutputstub import GuiOutputStub
from audiocontroller import AudioController
			
class TestAudioController(unittest.TestCase):
	def testTrimAudioFileCommandLine(self):
		playListName = 'test_audio_controller'
		targetAudioDir = AUDIO_DIR_TEST + DIR_SEP + playListName
		audioFileName = 'LExpérience de Mort Imminente de Madame Mirjana Uzoh.mp3'
		audioFilePathName = targetAudioDir + DIR_SEP + audioFileName

		expectedExtractedFileDuration_1 = 63
		expectedExtractedFileDuration_2 = 62
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)
		
		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + audioFileName,
		            targetAudioDir + '\\' + audioFileName)
		
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput, AUDIO_DIR_TEST)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioController.trimAudioFileCommandLine(audioFilePathName)
		
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
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_1)
		self.assertAlmostEqual(expectedExtractedFileDuration_1, audio.info.length, delta=0.1)
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_2)
		self.assertAlmostEqual(expectedExtractedFileDuration_2, audio.info.length, delta=0.1)

	def testExtractAudioFromVideoFile(self):
		playListName = 'test_audio_controller'
		targetAudioDir = AUDIO_DIR_TEST + DIR_SEP + playListName
		audioFileName = 'LExpérience de Mort Imminente de Madame Mirjana Uzoh.mp3'
		audioFilePathName = targetAudioDir + DIR_SEP + audioFileName
		
		expectedExtractedFileDuration_1 = 63
		expectedExtractedFileDuration_2 = 62
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)
		
		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData\\' + audioFileName,
		            targetAudioDir + '\\' + audioFileName)
		
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput, AUDIO_DIR_TEST)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioController.trimAudioFileCommandLine(audioFilePathName)
		
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
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_1)
		self.assertAlmostEqual(expectedExtractedFileDuration_1, audio.info.length, delta=0.1)
		audio = MP3(targetAudioDir + DIR_SEP + extractedMp3FileName_2)
		self.assertAlmostEqual(expectedExtractedFileDuration_2, audio.info.length, delta=0.1)


if __name__ == '__main__':
#	unittest.main()
	tst = TestAudioController()
	tst.testExtractAudioFromVideoFile()
