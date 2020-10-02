import unittest
import os, sys, inspect, shutil, glob
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from constants import *
from guioutputstub import GuiOutputStub
from youtubeaccess import YoutubeAccess
			
class TestYoutubeAccessDownloadMethods(unittest.TestCase):
	'''
	Since testing download consume band width, it is placed in a specific test class.
	'''

	def testDownloadAudioFromPlaylistOneVideo_targetFolder_exist(self):
		playlistName = 'test_audio_downloader_one_file'
		downloadDir = AUDIO_DIR + DIR_SEP + playlistName

		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)

		# deleting files in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)
			
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAccess(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistTimeFrameData, targetAudioDir = youtubeAccess.downloadAudioFromPlaylist(playlistUrl)

		sys.stdout = stdout

		if os.name == 'posix':
			self.assertEqual(['downloading Wear a mask. Help slow the spread of Covid-19.',
							  '',
							  ''], outputCapturingString.getvalue().split('\n'))
			self.assertEqual('/storage/emulated/0/Download/Audiobooks/test_audio_downloader_one_file',
			                 downloadDir)
		else:
			self.assertEqual(['downloading Wear a mask. Help slow the spread of Covid-19.',
							  '',
							  ''], outputCapturingString.getvalue().split('\n'))
			self.assertEqual('D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks\\test_audio_downloader_one_file', downloadDir)

		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Wear a mask Help slow the spread of Covid-19.mp4']), sorted(fileNameLst))
		self.assertIsNone(playlistTimeFrameData)

	def testDownloadAudioFromPlaylistOneVideo_targetFolder_not_exist(self):
		playlistName = 'test_audio_downloader_one_file'
		downloadDir = AUDIO_DIR + DIR_SEP + playlistName

		# deleting downloadDir (dir and content)
		if os.path.exists(downloadDir):
			shutil.rmtree(downloadDir)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAccess(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		youtubeAccess.downloadAudioFromPlaylist(playlistUrl)

		sys.stdout = stdout

		if os.name == 'posix':
			self.assertEqual(['Directory',
							  'Audiobooks/test_audio_downloader_one_file',
							  'will be created.',
							  '',
							  'Continue with download ?',
							  'downloading Wear a mask. Help slow the spread of Covid-19.',
							  '',
							  ''], outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual(['Directory',
							  'Audiobooks\\test_audio_downloader_one_file',
							  'will be created.',
							  '',
							  'Continue with download ?',
							  'downloading Wear a mask. Help slow the spread of Covid-19.',
							  '',
							  ''], outputCapturingString.getvalue().split('\n'))

		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Wear a mask Help slow the spread of Covid-19.mp4']), sorted(fileNameLst))

	def testDownloadAudioFromPlaylistMultipleVideo(self):
		playlistName = 'test_audio_downloader_two_files'
		downloadDir = AUDIO_DIR + DIR_SEP + playlistName

		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting files in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAccess(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRGA1T1vOn500RuLFo_lGJv"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		youtubeAccess.downloadAudioFromPlaylist(playlistUrl)

		sys.stdout = stdout

		if os.name == 'posix':
			self.assertEqual(['downloading Wear a mask. Help slow the spread of Covid-19.',
			                  '',
			                  'downloading Wear a mask. Help slow the spread of Covid-19.',
			                  'downloading Here to help: Give him what he wants',
							  '',
							  ''], outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual(['downloading Wear a mask. Help slow the spread of Covid-19.',
			                  '',
			                  'downloading Wear a mask. Help slow the spread of Covid-19.',
			                  'downloading Here to help: Give him what he wants',
							  '',
							  ''], outputCapturingString.getvalue().split('\n'))

		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Wear a mask Help slow the spread of Covid-19.mp4', 'Here to help Give him what he wants.mp4',]), sorted(fileNameLst))
	
	def testDownloadAudioFromPlaylistOneVideo_invalid_url(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAccess(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=invalid"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		youtubeAccess.downloadAudioFromPlaylist(playlistUrl)
		
		sys.stdout = stdout
		
		if os.name == 'posix':
			self.assertEqual(['The URL obtained from clipboard is not pointing to a playlist. Program closed.',
			                  ''], outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual(['The URL obtained from clipboard is not pointing to a playlist. Program closed.',
			                  ''], outputCapturingString.getvalue().split('\n'))
	
	def testDownloadAudioFromPlaylistOneVideo_empty_url(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAccess(guiOutput)
		playlistUrl = ""
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		youtubeAccess.downloadAudioFromPlaylist(playlistUrl)
		
		sys.stdout = stdout
		
		if os.name == 'posix':
			self.assertEqual(['The URL obtained from clipboard is not pointing to a playlist. Program closed.',
			                  ''], outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual(['The URL obtained from clipboard is not pointing to a playlist. Program closed.',
			                  ''], outputCapturingString.getvalue().split('\n'))
	
	def testDownloadAudioFromPlaylistOneVideo_with_timeFrame(self):
		playlistName = 'Test_title_one_time_frame_extract'
		downloadDir = AUDIO_DIR + DIR_SEP + playlistName
		# timeInfo = '(e0:0:5-0:0:10)'

		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting files in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAccess(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMTB7GasAttwVnPPk3-WTMNJ"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistTimeFrameData, targetAudioDir = youtubeAccess.downloadAudioFromPlaylist(playlistUrl)
		
		sys.stdout = stdout
		
		if os.name == 'posix':
			self.assertEqual(['downloading Wear a mask. Help slow the spread of Covid-19.',
			                  '',
			                  ''], outputCapturingString.getvalue().split('\n'))
			self.assertEqual('/storage/emulated/0/Download/Audiobooks/'+ playlistName,
			                 downloadDir)
		else:
			self.assertEqual(['downloading Wear a mask. Help slow the spread of Covid-19.',
			                  '',
			                  ''], outputCapturingString.getvalue().split('\n'))
			self.assertEqual('D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks\\' + playlistName,
			                 downloadDir)
		
		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Wear a mask Help slow the spread of Covid-19.mp4']), sorted(fileNameLst))
		self.assertEqual([[5, 10]], playlistTimeFrameData.getExtractStartEndSecondsLists(videoIndex=1))

if __name__ == '__main__':
#	unittest.main()
	tst = TestYoutubeAccessDownloadMethods()
	tst.testDownloadAudioFromPlaylistOneVideo_with_timeFrame()
