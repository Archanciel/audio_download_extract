import unittest
import os, sys, inspect, shutil, glob
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from constants import *
from guioutputstub import GuiOutputStub
from audioextracter import AudioExtracter
			
class TestAudioExtracter(unittest.TestCase):
	def testExtractAudioPortion(self):
		extractAudioDir = 'test_audio_downloader_one_file_for_extract'
		targetAudioDir = AUDIO_DIR + DIR_SEP + extractAudioDir
		timeInfo = '0.0.5/0.0.10'

		# deleting files in downloadDir
		files = glob.glob(targetAudioDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)

		# restoring mp4 file
		
		shutil.copy('D:\\Development\\Python\\audiodownload\\test\\testData' + '\\Wear a mask Help slow the spread of Covid-19.mp4' , targetAudioDir + '\\Wear a mask Help slow the spread of Covid-19.mp4')
		guiOutput = GuiOutputStub()
		audioExtracter = AudioExtracter(guiOutput, targetAudioDir)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioExtracter.extractAudioPortion(timeInfo)

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

if __name__ == '__main__':
#	unittest.main()
	tst = TestAudioDownloader()
	tst.testDownloadAudioFromPlaylistMultipleVideo()
