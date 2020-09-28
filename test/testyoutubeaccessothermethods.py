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

if __name__ == '__main__':
	unittest.main()
	# tst = TestYoutubeAccessDownloadMethods()
	# tst.testDownloadAudioFromPlaylistMultipleVideo()
