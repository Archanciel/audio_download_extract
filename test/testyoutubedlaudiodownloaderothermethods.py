import unittest
import os, sys, inspect, shutil, glob
from io import StringIO

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from guioutputstub import GuiOutputStub
from youtubedlaudiodownloader import YoutubeDlAudioDownloader
from accesserror import AccessError
from dirutil import DirUtil

class TestYoutubeDlAudioDownloaderOtherMethods(unittest.TestCase):
	'''
	Since testing download consume band width, it is placed in a specific test class.
	'''

	def testGetPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS"
		expectedPlaylistTitle = 'test_audio_downloader_one_file'

		youtubePlaylist, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)

		self.assertIsNone(accessError)
		self.assertEqual(expectedPlaylistTitle, playlistTitle,)
		self.assertIsNone(videoTitle)
	
	def testGetPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl_InvalidURL_GeeksForGeeks(self):
		"""
		When starting AudioDownloader after having copied a geeksforgeeks url, the
		exception raised was pytube.exceptions.VideoUnavailable instead of
		pytube.exceptions.RegexMatchError !
		"""
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://www.geeksforgeeks.org/python-how-to-use-multiple-kv-files-in-kivy/"
		
		youtubePlaylist, playlistTitle, videoTitle, accessError = youtubeAccess.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(
			playlistUrl)
		
		self.assertIsNotNone(accessError)
		self.assertEqual(AccessError.ERROR_TYPE_SINGLE_VIDEO_URL_PROBLEM, accessError.errorType)
		self.assertEqual(
			"trying to get the video title for the URL obtained from clipboard did not succeed.\nfailing URL: https://www.geeksforgeeks.org/python-how-to-use-multiple-kv-files-in-kivy/\nerror info: ERROR: Unsupported URL: https://www.geeksforgeeks.org/python-how-to-use-multiple-kv-files-in-kivy/\nnothing to download.".format(playlistUrl),
			accessError.errorMsg)
		self.assertIsNone(videoTitle)
	
	def testGetPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl_one_time_frame_extract(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMSRkN1v6xt75mWsjewlqfL3"
		expectedPlaylistTitle = 'Test_title_one_time_frame_extract (e01:05:52-01:07:23)'

		youtubePlaylist, playlistTitle, videoTitle, accessError = youtubeAccess.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)

		self.assertIsNone(accessError)
		self.assertEqual(expectedPlaylistTitle, playlistTitle,)	
		self.assertIsNone(videoTitle)

	def testGetPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl_one_time_frame_suppress(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMTE_E56D5obclOxWSIbcqNL"
		expectedPlaylistTitle = 'Test_title_one_time_frame_suppress (s01:05:52-01:07:23)'

		youtubePlaylist, playlistTitle, videoTitle, accessError = youtubeAccess.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)

		self.assertIsNone(accessError)
		self.assertEqual(expectedPlaylistTitle, playlistTitle,)
		self.assertIsNone(videoTitle)

	def testGetPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl_one_time_frame_extract_suppress(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMQglE3cl-cJyYQKrdsMvsfO"
		expectedPlaylistTitle = 'Test_title_one_time_frame_extract_suppress (e01:05:52-01:07:23 s01:15:52-01:17:23)'

		youtubePlaylist, playlistTitle, videoTitle, accessError = youtubeAccess.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)

		self.assertIsNone(accessError)
		self.assertEqual(expectedPlaylistTitle, playlistTitle,)
		self.assertIsNone(videoTitle)

	def testGetPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl_one_time_frame_suppress_extract(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMQCd5zf-V9H0ePbDqw3nfbR"
		expectedPlaylistTitle = 'Test_title_one_time_frame_suppress_extract (s01:05:52-01:07:23 e01:15:52-01:17:23)'

		youtubePlaylist, playlistTitle, videoTitle, accessError = youtubeAccess.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)

		self.assertIsNone(accessError)
		self.assertEqual(expectedPlaylistTitle, playlistTitle,)
		self.assertIsNone(videoTitle)

	def testGetPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl_multiple_time_frame_extract_suppress(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMQv-CxkvJ0NCti5L9AwLGUr"
		expectedPlaylistTitle = 'Test_title_multiple_time_frame_suppress_extract (s01:05:52-01:07:23 e01:15:52-01:17:23 S01:25:52-01:27:23 E01:35:52-01:37:23)'

		youtubePlaylist, playlistTitle, videoTitle, accessError = youtubeAccess.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)

		self.assertIsNone(accessError)
		self.assertEqual(expectedPlaylistTitle, playlistTitle,)
		self.assertIsNone(videoTitle)

	def testGetPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl_default_titles_nb(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://youtube.com/playlist?list=PLc0WZrTnM_WCpWKANamscrjFV01m4lXW1"

		videoTitleLst, accessError = youtubeAccess.getVideoTitlesInPlaylistForUrl(playlistUrl)

		self.assertIsNone(accessError)
		self.assertEqual(YoutubeDlAudioDownloader.MAX_VIDEO_TITLES_DEFAULT_NUMBER, len(videoTitleLst))

	def testGetPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl_specified_titles_nb(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://youtube.com/playlist?list=PLc0WZrTnM_WCpWKANamscrjFV01m4lXW1"

		videoTitleLst, accessError = youtubeAccess.getVideoTitlesInPlaylistForUrl(playlistUrl,
		                                                                          maxTitlesNumber=2)

		self.assertIsNone(accessError)
		self.assertEqual(2, len(videoTitleLst))

	def testGetPlaylistVideoTitlesForVideoUrl(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://youtu.be/mere5xyUe6A"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		videoTitleLst, accessError = youtubeAccess.getVideoTitlesInPlaylistForUrl(playlistUrl)
		
		sys.stdout = stdout
		
		self.assertEqual(['trying to obtain playlist video titles on an invalid url or a url pointing '
 'to a single video.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertIsNone(accessError)
		self.assertEqual([], videoTitleLst)
	
	def testGetPlaylistVideoTitlesForInvalidUrl(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://youtu.be/mere5xyUe6Ajjjj"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		videoTitleLst, accessError = youtubeAccess.getVideoTitlesInPlaylistForUrl(playlistUrl)
		
		sys.stdout = stdout
		
		self.assertEqual(['trying to obtain playlist video titles on an invalid url or a url pointing to a single video.',
		                  '',
		                  ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertIsNone(accessError)
		self.assertEqual([], videoTitleLst)


if __name__ == '__main__':
	#unittest.main()
	tst = TestYoutubeDlAudioDownloaderOtherMethods()
	tst.testGetPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl()
