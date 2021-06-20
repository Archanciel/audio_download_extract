import unittest
import os, sys, inspect, shutil, glob
from io import StringIO

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from constants import *
from guioutputstub import GuiOutputStub
from youtubedlaudiodownloader import YoutubeDlAudioDownloader
from accesserror import AccessError

class TestYoutubeDlAudioDownloaderOtherMethods(unittest.TestCase):
	'''
	Since testing download consume band width, it is placed in a specific test class.
	'''

	def testGetPlaylistObjectOrVideoTitleFortUrl(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, AUDIO_DIR_TEST)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS"
		expectedPlaylistTitle = 'test_audio_downloader_one_file'

		youtubePlaylist, playlistTitle, videoTitle, accessError = youtubeAccess.getPlaylistObjectOrVideoTitleFortUrl(playlistUrl)

		self.assertIsNone(accessError)
		self.assertEqual(expectedPlaylistTitle, playlistTitle,)
		self.assertIsNone(videoTitle)
		
	def testGetPlaylistObjectOrVideoTitleFortUrlInvalidURL(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, AUDIO_DIR_TEST)
		playlistUrl = "https://www.youtube.com/playlist?list=invalid"
		
		youtubePlaylist, playlistTitle, videoTitle, accessError = youtubeAccess.getPlaylistObjectOrVideoTitleFortUrl(playlistUrl)
		
		self.assertIsNotNone(accessError)
		self.assertEqual(AccessError.ERROR_TYPE_SINGLE_VIDEO_URL_PROBLEM, accessError.errorType)
		self.assertEqual('trying to get the video title for the URL obtained from clipboard did not succeed.\nfailing URL: https://www.youtube.com/playlist?list=invalid\nerror info: regex_search: could not find match for (?:v=|\/)([0-9A-Za-z_-]{11}).*\nnothing to download.', accessError.errorMsg)
		self.assertIsNone(videoTitle)

	def testGetPlaylistObjectOrVideoTitleFortUrl_one_time_frame_extract(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, AUDIO_DIR_TEST)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMSRkN1v6xt75mWsjewlqfL3"
		expectedPlaylistTitle = 'Test_title_one_time_frame_extract (e01:05:52-01:07:23)'

		youtubePlaylist, playlistTitle, videoTitle, accessError = youtubeAccess.getPlaylistObjectOrVideoTitleFortUrl(playlistUrl)

		self.assertIsNone(accessError)
		self.assertEqual(expectedPlaylistTitle, playlistTitle,)	
		self.assertIsNone(videoTitle)

	def testGetPlaylistObjectOrVideoTitleFortUrl_one_time_frame_suppress(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, AUDIO_DIR_TEST)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMTE_E56D5obclOxWSIbcqNL"
		expectedPlaylistTitle = 'Test_title_one_time_frame_suppress (s01:05:52-01:07:23)'

		youtubePlaylist, playlistTitle, videoTitle, accessError = youtubeAccess.getPlaylistObjectOrVideoTitleFortUrl(playlistUrl)

		self.assertIsNone(accessError)
		self.assertEqual(expectedPlaylistTitle, playlistTitle,)
		self.assertIsNone(videoTitle)

	def testGetPlaylistObjectOrVideoTitleFortUrl_one_time_frame_extract_suppress(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, AUDIO_DIR_TEST)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMQglE3cl-cJyYQKrdsMvsfO"
		expectedPlaylistTitle = 'Test_title_one_time_frame_extract_suppress (e01:05:52-01:07:23 s01:15:52-01:17:23)'

		youtubePlaylist, playlistTitle, videoTitle, accessError = youtubeAccess.getPlaylistObjectOrVideoTitleFortUrl(playlistUrl)

		self.assertIsNone(accessError)
		self.assertEqual(expectedPlaylistTitle, playlistTitle,)
		self.assertIsNone(videoTitle)

	def testGetPlaylistObjectOrVideoTitleFortUrl_one_time_frame_suppress_extract(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, AUDIO_DIR_TEST)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMQCd5zf-V9H0ePbDqw3nfbR"
		expectedPlaylistTitle = 'Test_title_one_time_frame_suppress_extract (s01:05:52-01:07:23 e01:15:52-01:17:23)'

		youtubePlaylist, playlistTitle, videoTitle, accessError = youtubeAccess.getPlaylistObjectOrVideoTitleFortUrl(playlistUrl)

		self.assertIsNone(accessError)
		self.assertEqual(expectedPlaylistTitle, playlistTitle,)
		self.assertIsNone(videoTitle)

	def testGetPlaylistObjectOrVideoTitleFortUrl_multiple_time_frame_extract_suppress(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, AUDIO_DIR_TEST)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMQv-CxkvJ0NCti5L9AwLGUr"
		expectedPlaylistTitle = 'Test_title_multiple_time_frame_suppress_extract (s01:05:52-01:07:23 e01:15:52-01:17:23 S01:25:52-01:27:23 E01:35:52-01:37:23)'

		youtubePlaylist, playlistTitle, videoTitle, accessError = youtubeAccess.getPlaylistObjectOrVideoTitleFortUrl(playlistUrl)

		self.assertIsNone(accessError)
		self.assertEqual(expectedPlaylistTitle, playlistTitle,)
		self.assertIsNone(videoTitle)


if __name__ == '__main__':
	unittest.main()
	# tst = TestYoutubeDlAudioDownloaderOtherMethods()
	# tst.testSplitPlayListTitle_one_time_frame_extract()
