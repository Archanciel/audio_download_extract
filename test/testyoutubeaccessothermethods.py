import unittest
import os, sys, inspect, shutil, glob
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from constants import *
from guioutputstub import GuiOutputStub
from youtubeaccess import YoutubeAccess
			
class TestYoutubeAccessOtherMethods(unittest.TestCase):
	'''
	Since testing download consume band width, it is placed in a specific test class.
	'''

	def testGetPlaylistObject(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAccess(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS"
		playlistName = 'test_audio_downloader_one_file'

		youtubePlaylist = youtubeAccess.getPlaylistObject(playlistUrl)

		self.assertEqual(playlistName, youtubePlaylist.title())
	
	def testGetPlaylistObjectInvalidURL(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAccess(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=invalid"
		
		youtubePlaylist = youtubeAccess.getPlaylistObject(playlistUrl)
		
		self.assertTrue('Oops' in youtubePlaylist.title())
	
	def testGetPlaylistObjectEmptyURL(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAccess(guiOutput)
		playlistUrl = ''
		
		youtubePlaylist = youtubeAccess.getPlaylistObject(playlistUrl)
		
		self.assertTrue('Oops' in youtubePlaylist.title())
	
	def testGetPlaylistObjectNoneURL(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAccess(guiOutput)
		playlistUrl = None
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		youtubePlaylist = youtubeAccess.getPlaylistObject(playlistUrl)
		
		sys.stdout = stdout
		
		if os.name == 'posix':
			self.assertEqual(['playlist URL == None',
			                  ''], outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual(['playlist URL == None',
			                  ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertIsNone(youtubePlaylist)
		
	def testGetPlaylistObject_one_time_frame_extract(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAccess(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMSRkN1v6xt75mWsjewlqfL3"
		playlistName = 'Test_title_one_time_frame_extract (e01:05:52-01:07:23)'

		youtubePlaylist = youtubeAccess.getPlaylistObject(playlistUrl)

		self.assertEqual(playlistName, youtubePlaylist.title())	
		
	def testGetPlaylistObject_one_time_frame_suppress(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAccess(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMTE_E56D5obclOxWSIbcqNL"
		playlistName = 'Test_title_one_time_frame_suppress (s01:05:52-01:07:23)'

		youtubePlaylist = youtubeAccess.getPlaylistObject(playlistUrl)

		self.assertEqual(playlistName, youtubePlaylist.title())	
		
	def testGetPlaylistObject_one_time_frame_extract_suppress(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAccess(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMQglE3cl-cJyYQKrdsMvsfO"
		playlistName = 'Test_title_one_time_frame_extract_suppress (e01:05:52-01:07:23 s01:15:52-01:17:23)'

		youtubePlaylist = youtubeAccess.getPlaylistObject(playlistUrl)

		self.assertEqual(playlistName, youtubePlaylist.title())	
		
	def testGetPlaylistObject_one_time_frame_suppress_extract(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAccess(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMQCd5zf-V9H0ePbDqw3nfbR"
		playlistName = 'Test_title_one_time_frame_suppress_extract (s01:05:52-01:07:23 e01:15:52-01:17:23)'

		youtubePlaylist = youtubeAccess.getPlaylistObject(playlistUrl)

		self.assertEqual(playlistName, youtubePlaylist.title())	
		
	def testGetPlaylistObject_multiple_time_frame_extract_suppress(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAccess(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMQv-CxkvJ0NCti5L9AwLGUr"
		playlistName = 'Test_title_multiple_time_frame_suppress_extract (s01:05:52-01:07:23 e01:15:52-01:17:23 s01:25:52-01:27:23 e01:35:52-01:37:23)'

		youtubePlaylist = youtubeAccess.getPlaylistObject(playlistUrl)

		self.assertEqual(playlistName, youtubePlaylist.title())	

if __name__ == '__main__':
	unittest.main()
	# tst = TestYoutubeAccessDownloadMethods()
	# tst.testDownloadAudioFromPlaylistMultipleVideo()