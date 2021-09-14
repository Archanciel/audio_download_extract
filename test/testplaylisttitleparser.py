import unittest
import os, sys, inspect, glob

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from constants import  *
from playlisttitleparser import PlaylistTitleParser
from dirutil import DirUtil

class TestPlaylistTitleParser(unittest.TestCase):
		
	def testCreateDownloadVideoInfoDic_one_time_frame_extract(self):
		expectedPlayListName = 'Test_title_one_time_frame_extract'
		timeInfo = '(e01:05:52-01:07:23)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideoExtractTimeFramesList = [[3952, 4043]]
		expectedVideoSuppressTimeFramesList = []

		downloadDir = DirUtil.getTestAudioRootPath() + expectedPlayListName

		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		downloadedVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle, DirUtil.getTestAudioRootPath())

		self.assertEqual(expectedPlayListName, downloadedVideoInfoDic.getPlaylistName())
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1), expectedVideoExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1), expectedVideoSuppressTimeFramesList)
	
	def testCreateDownloadVideoInfoDic_one_time_frame_extract_to_end(self):
		expectedPlayListName = 'Test_title_one_time_frame_extract'
		timeInfo = '(e01:05:52-e)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideoExtractTimeFramesList = [[3952, 'end']]
		expectedVideoSuppressTimeFramesList = []
		
		downloadDir = DirUtil.getTestAudioRootPath() + expectedPlayListName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)

		downloadedVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle, DirUtil.getTestAudioRootPath())
		
		self.assertEqual(expectedPlayListName, downloadedVideoInfoDic.getPlaylistName())
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoSuppressTimeFramesList)
	
	def testCreateDownloadVideoInfoDic_two_time_frame_extract_last_to_end(self):
		expectedPlayListName = 'Test_title_one_time_frame_extract'
		timeInfo = '(e01:05:02-01:05:05 e01:05:52-e)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideoExtractTimeFramesList = [[3902, 3905], [3952, 'end']]
		expectedVideoSuppressTimeFramesList = []
		
		downloadDir = DirUtil.getTestAudioRootPath() + expectedPlayListName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		downloadedVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle, DirUtil.getTestAudioRootPath())
		
		self.assertEqual(expectedPlayListName, downloadedVideoInfoDic.getPlaylistName())
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoSuppressTimeFramesList)
	
	def testCreateDownloadVideoInfoDic_one_time_frame_extract_upper(self):
		expectedPlayListName = 'Test_title_one_time_frame_extract'
		timeInfo = '(E01:05:52-01:07:23)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideoExtractTimeFramesList = [[3952, 4043]]
		expectedVideoSuppressTimeFramesList = []
		
		downloadDir = DirUtil.getTestAudioRootPath() + expectedPlayListName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		downloadedVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle, DirUtil.getTestAudioRootPath())
		
		self.assertEqual(expectedPlayListName, downloadedVideoInfoDic.getPlaylistName())
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoSuppressTimeFramesList)
	
	def testCreateDownloadVideoInfoDic_one_time_frame_suppress(self):
		expectedPlayListName = 'Test_title_one_time_frame_suppress'
		timeInfo = '(s0:05:52-0:07:23)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideoExtractTimeFramesList = []
		expectedVideoSuppressTimeFramesList = [[352, 443]]
		
		downloadDir = DirUtil.getTestAudioRootPath() + expectedPlayListName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		downloadedVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle, DirUtil.getTestAudioRootPath())

		self.assertEqual(expectedPlayListName, downloadedVideoInfoDic.getPlaylistName())
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1), expectedVideoExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1), expectedVideoSuppressTimeFramesList)
	
	def testCreateDownloadVideoInfoDic_one_time_frame_suppress_to_end(self):
		expectedPlayListName = 'Test_title_one_time_frame_suppress'
		timeInfo = '(s0:05:52-e)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideoExtractTimeFramesList = []
		expectedVideoSuppressTimeFramesList = [[352, 'end']]
		
		downloadDir = DirUtil.getTestAudioRootPath() + expectedPlayListName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		downloadedVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle, DirUtil.getTestAudioRootPath())
		
		self.assertEqual(expectedPlayListName, downloadedVideoInfoDic.getPlaylistName())
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoSuppressTimeFramesList)
	
	def testCreateDownloadVideoInfoDic_one_time_frame_suppress_upper(self):
		expectedPlayListName = 'Test_title_one_time_frame_suppress'
		timeInfo = '(S0:05:52-0:07:23)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideoExtractTimeFramesList = []
		expectedVideoSuppressTimeFramesList = [[352, 443]]
		
		downloadDir = DirUtil.getTestAudioRootPath() + expectedPlayListName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		downloadedVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle, DirUtil.getTestAudioRootPath())
		
		self.assertEqual(expectedPlayListName, downloadedVideoInfoDic.getPlaylistName())
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoSuppressTimeFramesList)
	
	def testCreateDownloadVideoInfoDic_no_time_frame(self):
		expectedPlayListName = 'Test_title_no_time_frame'
		playlistTitle = expectedPlayListName
		
		downloadDir = DirUtil.getTestAudioRootPath() + expectedPlayListName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		downloadedVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle, DirUtil.getTestAudioRootPath())

		self.assertEqual(expectedPlayListName, downloadedVideoInfoDic.getPlaylistName())
		
	def testCreateDownloadVideoInfoDic_two_time_frames_suppress(self):
		expectedPlayListName = 'Test_title_two_time_frame_suppress'
		timeInfo = '(s0:05:52-0:07:23 s0:10:52-0:10:53)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideoExtractTimeFramesList = []
		expectedVideoSuppressTimeFramesList = [[352, 443], [652, 653]]
		
		downloadDir = DirUtil.getTestAudioRootPath() + expectedPlayListName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		downloadedVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle, DirUtil.getTestAudioRootPath())

		self.assertEqual(expectedPlayListName, downloadedVideoInfoDic.getPlaylistName())
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1), expectedVideoExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1), expectedVideoSuppressTimeFramesList)
	
	def testCreateDownloadVideoInfoDic_two_time_frames_suppress_last_to_end(self):
		expectedPlayListName = 'Test_title_two_time_frame_suppress'
		timeInfo = '(s0:05:52-0:07:23 s0:10:52-e)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideoExtractTimeFramesList = []
		expectedVideoSuppressTimeFramesList = [[352, 443], [652, 'end']]
		
		downloadDir = DirUtil.getTestAudioRootPath() + expectedPlayListName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		downloadedVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle, DirUtil.getTestAudioRootPath())
		
		self.assertEqual(expectedPlayListName, downloadedVideoInfoDic.getPlaylistName())
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoSuppressTimeFramesList)
	
	def testCreateDownloadVideoInfoDic_two_time_frames_one_extract_one_suppress_no_braces(self):
		expectedPlayListName = 'Test_title_two_time_frame_one_extract_one_suppress'
		timeInfo = '(e0:05:52-0:07:23 s0:10:52-0:10:53)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideoExtractTimeFramesList = [[352, 443]]
		expectedVideoSuppressTimeFramesList = [[652, 653]]
		
		downloadDir = DirUtil.getTestAudioRootPath() + expectedPlayListName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		downloadedVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle, DirUtil.getTestAudioRootPath())

		self.assertEqual(expectedPlayListName, downloadedVideoInfoDic.getPlaylistName())
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1), expectedVideoExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1), expectedVideoSuppressTimeFramesList)
	
	def testCreateDownloadVideoInfoDic_two_time_frames_one_extract_one_suppress_with_braces(self):
		expectedPlayListName = 'Test_title_two_time_frame_one_extract_one_suppress'
		timeInfo = '{(e0:05:52-0:07:23 s0:10:52-0:10:53)}'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideoExtractTimeFramesList = [[352, 443]]
		expectedVideoSuppressTimeFramesList = [[652, 653]]
		
		downloadDir = DirUtil.getTestAudioRootPath() + expectedPlayListName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		downloadedVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle,
		                                                                                                DirUtil.getTestAudioRootPath())
		
		self.assertEqual(expectedPlayListName, downloadedVideoInfoDic.getPlaylistName())
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoSuppressTimeFramesList)
	
	def testCreateDownloadVideoInfoDic_two_time_frames_one_extract_one_suppress_two_videos(self):
		# Example of playlist title: playlist_title (s01:05:52-01:07:23 e01:15:52-e  E01:35:52-01:37:23 S01:25:52-e) (s01:05:52-01:07:23 e01:15:52-e S01:25:52-e E01:35:52-01:37:23)
		expectedPlayListName = 'Test_title_two_time_frame_one_extract_one_suppress_two_videos'
		timeInfo = '(E0:05:52-0:07:23 S0:10:52-0:10:53) (e1:05:52-1:07:23 s1:10:52-1:10:53)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideo1ExtractTimeFramesList = [[352, 443]]
		expectedVideo1SuppressTimeFramesList = [[652, 653]]

		expectedVideo2ExtractTimeFramesList = [[3952, 4043]]
		expectedVideo2SuppressTimeFramesList = [[4252, 4253]]
		
		downloadDir = DirUtil.getTestAudioRootPath() + expectedPlayListName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		downloadedVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle, DirUtil.getTestAudioRootPath())

		self.assertEqual(expectedPlayListName, downloadedVideoInfoDic.getPlaylistName())
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1), expectedVideo1ExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1), expectedVideo1SuppressTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(2), expectedVideo2ExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(2), expectedVideo2SuppressTimeFramesList)
	
	def testCreateDownloadVideoInfoDic_two_time_frames_one_extract_one_suppress_two_videos_timeFrames_to_end(self):
		# Example of playlist title: playlist_title (s01:05:52-01:07:23 e01:15:52-e  E01:35:52-01:37:23 S01:25:52-e) (s01:05:52-01:07:23 e01:15:52-e S01:25:52-e E01:35:52-01:37:23)
		expectedPlayListName = 'Test_title_two_time_frame_one_extract_one_suppress_two_videos'
		timeInfo = '(E0:05:52-0:07:23 S0:10:52-e) (e1:05:52-E s1:10:52-1:10:53)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideo1ExtractTimeFramesList = [[352, 443]]
		expectedVideo1SuppressTimeFramesList = [[652, 'end']]
		
		expectedVideo2ExtractTimeFramesList = [[3952, 'end']]
		expectedVideo2SuppressTimeFramesList = [[4252, 4253]]
		
		downloadDir = DirUtil.getTestAudioRootPath() + expectedPlayListName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		downloadedVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle, DirUtil.getTestAudioRootPath())
		
		self.assertEqual(expectedPlayListName, downloadedVideoInfoDic.getPlaylistName())
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1),
		                 expectedVideo1ExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1),
		                 expectedVideo1SuppressTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(2),
		                 expectedVideo2ExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(2),
		                 expectedVideo2SuppressTimeFramesList)
	
	def testCreateDownloadVideoInfoDic_no_time_frame_bug(self):
		expectedPlayListName = '21_leçons_pour_le_XXIe_siècle'
		playlistTitle = expectedPlayListName
		
		downloadDir = DirUtil.getTestAudioRootPath() + expectedPlayListName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		downloadedVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle, DirUtil.getTestAudioRootPath())
		
		self.assertEqual(expectedPlayListName, downloadedVideoInfoDic.getPlaylistName())
	
	def testCreateDownloadVideoInfoDic_no_time_frame_playlistTitle_with_spaces(self):
		expectedPlayListName = '21 leçons pour le XXIe siècle'
		playlistTitle = expectedPlayListName
		
		downloadDir = DirUtil.getTestAudioRootPath() + expectedPlayListName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		downloadedVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle, DirUtil.getTestAudioRootPath())
		
		self.assertEqual(expectedPlayListName, downloadedVideoInfoDic.getPlaylistName())
	
	def testCreateDownloadVideoInfoDic_two_time_frames_one_extract_one_suppress_two_videos_timeFrames_to_end_playlistTitle_with_spaces(self):
		# Example of playlist title: playlist_title (s01:05:52-01:07:23 e01:15:52-e  E01:35:52-01:37:23 S01:25:52-e) (s01:05:52-01:07:23 e01:15:52-e S01:25:52-e E01:35:52-01:37:23)
		expectedPlayListName = 'Test_title two time_frame_one extract one_suppress_two_videos'
		timeInfo = '(E0:05:52-0:07:23 S0:10:52-e) (e1:05:52-E s1:10:52-1:10:53)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideo1ExtractTimeFramesList = [[352, 443]]
		expectedVideo1SuppressTimeFramesList = [[652, 'end']]
		
		expectedVideo2ExtractTimeFramesList = [[3952, 'end']]
		expectedVideo2SuppressTimeFramesList = [[4252, 4253]]
		
		downloadDir = DirUtil.getTestAudioRootPath() + expectedPlayListName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		downloadedVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle, DirUtil.getTestAudioRootPath())
		
		self.assertEqual(expectedPlayListName, downloadedVideoInfoDic.getPlaylistName())
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1),
		                 expectedVideo1ExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1),
		                 expectedVideo1SuppressTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(2),
		                 expectedVideo2ExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(2),
		                 expectedVideo2SuppressTimeFramesList)
	
	def testCreateDownloadVideoInfoDic_timeFrameSyntax(self):
		expectedPlayListName = 'Test 3 short videos'
		timeInfoWithSyntaxError = '(e-0:0:4-0:0:6 e0:0:12-e s0:0:1-0:0:3 s0:0:4-0:0:6 s0:0:9-e) (s0:0:1-0:0:3 s0:0:4-0:0:6 s0:0:9-e) (e0:0:2-0:0:3 e0:0:5-e)'
		playlistTitle = expectedPlayListName + ' ' + timeInfoWithSyntaxError
		
		downloadDir = DirUtil.getTestAudioRootPath() + expectedPlayListName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		downloadedVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle, DirUtil.getTestAudioRootPath())
		self.assertIsNotNone(accessError)
		self.assertEqual('time frame syntax error "e-0:0:4-0:0:6" detected in playlist title: "Test 3 short videos (e-0:0:4-0:0:6 e0:0:12-e s0:0:1-0:0:3 s0:0:4-0:0:6 s0:0:9-e) (s0:0:1-0:0:3 s0:0:4-0:0:6 s0:0:9-e) (e0:0:2-0:0:3 e0:0:5-e)".\ndownloading playlist interrupted.', accessError.errorMsg)
		
		self.assertEqual(expectedPlayListName, downloadedVideoInfoDic.getPlaylistName())
		self.assertIsNone(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1))
		self.assertIsNone(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(2))
		self.assertIsNone(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(3))

		self.assertIsNone(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1))
		self.assertIsNone(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(2))
		self.assertIsNone(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(3))
	
	def testCreateDownloadVideoInfoDic_two_time_frames_one_extract_one_suppress_two_videos_timeFrames_to_end_playlistTitle_with_spaces_and_accented_letters(self):
		# Example of playlist title: playlist_title {(s01:05:52-01:07:23 e01:15:52-e  E01:35:52-01:37:23 S01:25:52-e) (s01:05:52-01:07:23 e01:15:52-e S01:25:52-e E01:35:52-01:37:23)}
		expectedPlayListName = "Audio: - ET L'UNIVERS DISPARAÎTRA La nature illusoire de notre réalité et le pouvoir transcendant du véritable pardon de Gary Renard"
		timeInfo = "{(E0:05:52-0:07:23 S0:10:52-e) (e1:05:52-E s1:10:52-1:10:53)}"
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideo1ExtractTimeFramesList = [[352, 443]]
		expectedVideo1SuppressTimeFramesList = [[652, 'end']]
		
		expectedVideo2ExtractTimeFramesList = [[3952, 'end']]
		expectedVideo2SuppressTimeFramesList = [[4252, 4253]]
		
		downloadDir = DirUtil.getTestAudioRootPath() + expectedPlayListName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		downloadedVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle,
		                                                                                                DirUtil.getTestAudioRootPath())
		
		self.assertEqual(expectedPlayListName, downloadedVideoInfoDic.getPlaylistName())
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1),
		                 expectedVideo1ExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1),
		                 expectedVideo1SuppressTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(2),
		                 expectedVideo2ExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(2),
		                 expectedVideo2SuppressTimeFramesList)
	
	def testCreateDownloadVideoInfoDic_playlistTitle_with_spaces_and_accented_letters(
			self):
		expectedPlayListName = "Audio: - ET L'UNIVERS DISPARAÎTRA La nature illusoire de notre réalité et le pouvoir transcendant du véritable pardon de Gary Renard"
		playlistTitle = expectedPlayListName
		
		downloadDir = DirUtil.getTestAudioRootPath() + expectedPlayListName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		downloadedVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle,
		                                                                                                DirUtil.getTestAudioRootPath())
		
		self.assertEqual(expectedPlayListName, downloadedVideoInfoDic.getPlaylistName())
	
	def testCreateDownloadVideoInfoDic_playlistTitle_with_unauthorized_chars(
			self):
		playlistTitle = "Audio: - ET L'UNIVERS DISPARAÎTRA/La \\nature * illusoire de notre réalité et le pouvoir transcendant du |véritable \"pardon\" + commentaires de <Gary> Renard ?"
		expectedFileName = "Audio - ET L'UNIVERS DISPARAÎTRA La nature   illusoire de notre réalité et le pouvoir transcendant du véritable pardon + commentaires de Gary Renard"
		
		epectedDownloadDir = DirUtil.getTestAudioRootPath() + expectedFileName
		
		# deleting dic file in downloadDir
		files = glob.glob(epectedDownloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		downloadedVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle,
		                                                                                                DirUtil.getTestAudioRootPathNoEndSep())
		
		self.assertEqual(epectedDownloadDir, downloadedVideoInfoDic.getPlaylistDownloadDir())
	
	def testCreateDownloadVideoInfoDic_playlistTitle_with_spaces_and_accented_letters_and_comma(
			self):
		expectedPlayListName = "Et l\'Univers disparaîtra, basé sur Un Cours en Miracles transmis par Jésus: avec mes commentaires et de nombreux extraits accompagnés de leur numéro"
		playlistTitle = expectedPlayListName
		
		downloadDir = DirUtil.getTestAudioRootPath() + expectedPlayListName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		downloadedVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle,
		                                                                                                DirUtil.getTestAudioRootPath())
		
		self.assertEqual(expectedPlayListName, downloadedVideoInfoDic.getPlaylistName())
	
	def testCreateDownloadVideoInfoDic_playlistTitle_with_spaces_and_accented_letters_and_comma_with_time_info(
			self):
		expectedPlayListName = "Et l\'Univers disparaîtra, basé sur Un Cours en Miracles transmis par Jésus: avec mes commentaires et de nombreux extraits accompagnés de leur numéro"
		timeInfo = "{(E0:05:52-0:07:23 S0:10:52-e) (e1:05:52-E s1:10:52-1:10:53)}"
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideo1ExtractTimeFramesList = [[352, 443]]
		expectedVideo1SuppressTimeFramesList = [[652, 'end']]
		
		expectedVideo2ExtractTimeFramesList = [[3952, 'end']]
		expectedVideo2SuppressTimeFramesList = [[4252, 4253]]
		
		downloadDir = DirUtil.getTestAudioRootPath() + expectedPlayListName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		downloadedVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle,
		                                                                                                DirUtil.getTestAudioRootPath())
		
		self.assertEqual(expectedPlayListName, downloadedVideoInfoDic.getPlaylistName())
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1),
		                 expectedVideo1ExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1),
		                 expectedVideo1SuppressTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(2),
		                 expectedVideo2ExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(2),
		                 expectedVideo2SuppressTimeFramesList)


if __name__ == '__main__':
	#unittest.main()
	tst = TestPlaylistTitleParser()
	tst.testCreateDownloadVideoInfoDic_playlistTitle_with_unauthorized_chars()
