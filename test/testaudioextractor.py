import unittest
import os, sys, inspect, shutil, glob
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from constants import *
from guioutputstub import GuiOutputStub
from audioextractor import AudioExtractor
from playlisttimeframedata import PlaylistTimeFrameData
			
class TestAudioExtractor(unittest.TestCase):
	def testExtractAudioPortion_dir_contains_one_file_with_one_extract_timeframe(self):
		extractAudioDir = 'test_audio_downloader_one_file_for_extract_with_one_extract_timeframe'
		targetAudioDir = AUDIO_DIR + DIR_SEP + extractAudioDir
		
		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		playlistTimeFrameData = PlaylistTimeFrameData()
		videoIndex = 1
		startEndSecondsList = [5, 10]
		expectedExtractedFileDuration = startEndSecondsList[1] - startEndSecondsList[0]
		playlistTimeFrameData.addExtractStartEndSecondsList(videoIndex, startEndSecondsList)

		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)

		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData' + '\\Wear a mask Help slow the spread of Covid-19.mp4' , targetAudioDir + '\\Wear a mask Help slow the spread of Covid-19.mp4')
		guiOutput = GuiOutputStub()
		audioExtractor = AudioExtractor(guiOutput, targetAudioDir)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtractor.extractAudioPortion(playlistTimeFrameData)

		sys.stdout = stdout

#		if os.name == 'posix':
#			self.assertEqual(['downloading Wear a mask. Help slow the spread of Covid-19.',
#							  '',
#							  ''], outputCapturingString.getvalue().split('\n'))
#		else:
#			self.assertEqual(['downloading Wear a mask. Help slow the spread of Covid-19.',
#							  '',
#							  ''], outputCapturingString.getvalue().split('\n'))

#		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
#		self.assertEqual(sorted(['Wear a mask Help slow the spread of Covid-19.mp4']), sorted(fileNameLst))
		extractedFileList = os.listdir(targetAudioDir)
		self.assertEqual(['Wear a mask Help slow the spread of Covid-19.mp3'], extractedFileList)

		from mutagen.mp3 import MP3
		audio = MP3(targetAudioDir + DIR_SEP + extractedFileList[0])
		self.assertAlmostEquals(expectedExtractedFileDuration, audio.info.length, delta=0.1)

if __name__ == '__main__':
#	unittest.main()
	tst = TestAudioExtractor()
	tst.testExtractAudioPortion_dir_contains_one_file_with_one_extract_timeframe()
