import unittest
import os, sys, inspect, datetime, shutil, glob
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from constants import *
from guioutputstub import GuiOutputStub
from audiodownloader import AudioDownloader
			
class TestAudioDownloader(unittest.TestCase):
	def testDownloadAudioFromPlaylist_targetFolder_exist(self):
		downloadDir = AUDIO_DIR + DIR_SEP + 'test_audio_downloader'

		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)

		guiOutput = GuiOutputStub()
		audioDownloader = AudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioDownloader.downloadAudioFromPlaylist(playlistUrl)

		sys.stdout = stdout

		if os.name == 'posix':
			self.assertEqual(['downloading Wear a mask. Help slow the spread of Covid-19.',
							  '',
							  ''], outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual(['downloading Wear a mask. Help slow the spread of Covid-19.',
							  '',
							  ''], outputCapturingString.getvalue().split('\n'))

		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Wear a mask Help slow the spread of Covid-19.mp4']), sorted(fileNameLst))

	def testDownloadAudioFromPlaylist_targetFolder_not_exist(self):
		downloadDir = AUDIO_DIR + DIR_SEP + 'test_audio_downloader'

		# deleting downloadDir (dir and content)
		if os.path.exists(downloadDir):
			shutil.rmtree(downloadDir)
		
		guiOutput = GuiOutputStub()
		audioDownloader = AudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioDownloader.downloadAudioFromPlaylist(playlistUrl)

		sys.stdout = stdout

		if os.name == 'posix':
			self.assertEqual(['Directory',
							  'Audiobooks/test_audio_downloader',
							  'will be created.',
							  '',
							  'Continue with download ?',
							  'downloading Wear a mask. Help slow the spread of Covid-19.',
							  '',
							  ''], outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual(['Directory',
							  'Audiobooks\\test_audio_downloader',
							  'will be created.',
							  '',
							  'Continue with download ?',
							  'downloading Wear a mask. Help slow the spread of Covid-19.',
							  '',
							  ''], outputCapturingString.getvalue().split('\n'))

		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Wear a mask Help slow the spread of Covid-19.mp4']), sorted(fileNameLst))

if __name__ == '__main__':
#	unittest.main()
	tst = TestAudioDownloader()
	tst.testDownloadAudioFromPlaylist_targetFolder_not_exist()
