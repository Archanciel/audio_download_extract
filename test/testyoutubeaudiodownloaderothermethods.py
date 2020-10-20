import unittest
import os, sys, inspect, shutil, glob
from io import StringIO

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from constants import *
from guioutputstub import GuiOutputStub
from youtubeaudiodownloader import YoutubeAudioDownloader
from accesserror import AccessError

class TestYoutubeAudioDownloaderOtherMethods(unittest.TestCase):
	'''
	Since testing download consume band width, it is placed in a specific test class.
	'''

	def testGetPlaylistObject(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS"
		expectedPlaylistTitle = 'test_audio_downloader_one_file'

		youtubePlaylist, playlistTitle, accessError = youtubeAccess.getPlaylistObject(playlistUrl)

		self.assertIsNone(accessError)
		self.assertEqual(expectedPlaylistTitle, playlistTitle,)
	
	def testGetPlaylistObjectInvalidURL(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=invalid"
		
		youtubePlaylist, playlistTitle, accessError = youtubeAccess.getPlaylistObject(playlistUrl)
		
		self.assertIsNotNone(accessError)
		self.assertEqual(AccessError.ERROR_TYPE_NOT_PLAYLIST_URL, accessError.errorType)
		self.assertEqual("The URL obtained from clipboard is not pointing to a playlist.\nWrong URL: https://www.youtube.com/playlist?list=invalid\nProgram will be closed.", accessError.errorMsg)
	
	def testGetPlaylistObject_one_time_frame_extract(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMSRkN1v6xt75mWsjewlqfL3"
		expectedPlaylistTitle = 'Test_title_one_time_frame_extract (e01:05:52-01:07:23)'

		youtubePlaylist, playlistTitle, accessError = youtubeAccess.getPlaylistObject(playlistUrl)

		self.assertIsNone(accessError)
		self.assertEqual(expectedPlaylistTitle, playlistTitle,)	
		
	def testGetPlaylistObject_one_time_frame_suppress(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMTE_E56D5obclOxWSIbcqNL"
		expectedPlaylistTitle = 'Test_title_one_time_frame_suppress (s01:05:52-01:07:23)'

		youtubePlaylist, playlistTitle, accessError = youtubeAccess.getPlaylistObject(playlistUrl)

		self.assertIsNone(accessError)
		self.assertEqual(expectedPlaylistTitle, playlistTitle,)
		
	def testGetPlaylistObject_one_time_frame_extract_suppress(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMQglE3cl-cJyYQKrdsMvsfO"
		expectedPlaylistTitle = 'Test_title_one_time_frame_extract_suppress (e01:05:52-01:07:23 s01:15:52-01:17:23)'

		youtubePlaylist, playlistTitle, accessError = youtubeAccess.getPlaylistObject(playlistUrl)

		self.assertIsNone(accessError)
		self.assertEqual(expectedPlaylistTitle, playlistTitle,)
		
	def testGetPlaylistObject_one_time_frame_suppress_extract(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMQCd5zf-V9H0ePbDqw3nfbR"
		expectedPlaylistTitle = 'Test_title_one_time_frame_suppress_extract (s01:05:52-01:07:23 e01:15:52-01:17:23)'

		youtubePlaylist, playlistTitle, accessError = youtubeAccess.getPlaylistObject(playlistUrl)

		self.assertIsNone(accessError)
		self.assertEqual(expectedPlaylistTitle, playlistTitle,)
		
	def testGetPlaylistObject_multiple_time_frame_extract_suppress(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMQv-CxkvJ0NCti5L9AwLGUr"
		expectedPlaylistTitle = 'Test_title_multiple_time_frame_suppress_extract (s01:05:52-01:07:23 e01:15:52-01:17:23 S01:25:52-01:27:23 E01:35:52-01:37:23)'

		youtubePlaylist, playlistTitle, accessError = youtubeAccess.getPlaylistObject(playlistUrl)

		self.assertIsNone(accessError)
		self.assertEqual(expectedPlaylistTitle, playlistTitle,)


if __name__ == '__main__':
	unittest.main()
	# tst = TestYoutubeAudioDownloaderOtherMethods()
	# tst.testSplitPlayListTitle_one_time_frame_extract()
