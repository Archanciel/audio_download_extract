import unittest
import os, sys, inspect, shutil, glob
from io import StringIO

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from playlisttitleinterpreter import PlaylistTitleInterpreter

class TestPlaylistTitleInterpreter(unittest.TestCase):
		
	def testSplitPlayListTitle_one_time_frame_extract(self):
		expectedPlayListName = 'Test_title_one_time_frame_extract'
		timeInfo = '(e01:05:52-01:07:23)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideoExtractTimeFramesList = [[3952, 4043]]
		expectedVideoSuppressTimeFramesList = []

		playlistName, targetAudioDir, downloadedVideoInfoDic = PlaylistTitleInterpreter.splitPlaylistTitle(playlistTitle)

		self.assertEqual(expectedPlayListName, playlistName)
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1), expectedVideoExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1), expectedVideoSuppressTimeFramesList)
	
	def testSplitPlayListTitle_one_time_frame_extract_to_end(self):
		expectedPlayListName = 'Test_title_one_time_frame_extract'
		timeInfo = '(e01:05:52-e)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideoExtractTimeFramesList = [[3952, 'end']]
		expectedVideoSuppressTimeFramesList = []
		
		playlistName, targetAudioDir, downloadedVideoInfoDic = PlaylistTitleInterpreter.splitPlaylistTitle(playlistTitle)
		
		self.assertEqual(expectedPlayListName, playlistName)
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoSuppressTimeFramesList)
	
	def testSplitPlayListTitle_two_time_frame_extract_last_to_end(self):
		expectedPlayListName = 'Test_title_one_time_frame_extract'
		timeInfo = '(e01:05:02-01:05:05 e01:05:52-e)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideoExtractTimeFramesList = [[3902, 3905], [3952, 'end']]
		expectedVideoSuppressTimeFramesList = []
		
		playlistName, targetAudioDir, downloadedVideoInfoDic = PlaylistTitleInterpreter.splitPlaylistTitle(playlistTitle)
		
		self.assertEqual(expectedPlayListName, playlistName)
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoSuppressTimeFramesList)
	
	def testSplitPlayListTitle_one_time_frame_extract_upper(self):
		expectedPlayListName = 'Test_title_one_time_frame_extract'
		timeInfo = '(E01:05:52-01:07:23)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideoExtractTimeFramesList = [[3952, 4043]]
		expectedVideoSuppressTimeFramesList = []
		
		playlistName, targetAudioDir, downloadedVideoInfoDic = PlaylistTitleInterpreter.splitPlaylistTitle(playlistTitle)
		
		self.assertEqual(expectedPlayListName, playlistName)
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoSuppressTimeFramesList)
	
	def testSplitPlayListTitle_one_time_frame_suppress(self):
		expectedPlayListName = 'Test_title_one_time_frame_suppress'
		timeInfo = '(s0:05:52-0:07:23)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideoExtractTimeFramesList = []
		expectedVideoSuppressTimeFramesList = [[352, 443]]

		playlistName, targetAudioDir, downloadedVideoInfoDic = PlaylistTitleInterpreter.splitPlaylistTitle(playlistTitle)

		self.assertEqual(expectedPlayListName, playlistName)
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1), expectedVideoExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1), expectedVideoSuppressTimeFramesList)
	
	def testSplitPlayListTitle_one_time_frame_suppress_to_end(self):
		expectedPlayListName = 'Test_title_one_time_frame_suppress'
		timeInfo = '(s0:05:52-e)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideoExtractTimeFramesList = []
		expectedVideoSuppressTimeFramesList = [[352, 'end']]
		
		playlistName, targetAudioDir, downloadedVideoInfoDic = PlaylistTitleInterpreter.splitPlaylistTitle(playlistTitle)
		
		self.assertEqual(expectedPlayListName, playlistName)
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoSuppressTimeFramesList)
	
	def testSplitPlayListTitle_one_time_frame_suppress_upper(self):
		expectedPlayListName = 'Test_title_one_time_frame_suppress'
		timeInfo = '(S0:05:52-0:07:23)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideoExtractTimeFramesList = []
		expectedVideoSuppressTimeFramesList = [[352, 443]]
		
		playlistName, targetAudioDir, downloadedVideoInfoDic = PlaylistTitleInterpreter.splitPlaylistTitle(playlistTitle)
		
		self.assertEqual(expectedPlayListName, playlistName)
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoSuppressTimeFramesList)
	
	def testSplitPlayListTitle_no_time_frame(self):
		expectedPlayListName = 'Test_title_no_time_frame'
		playlistTitle = expectedPlayListName
		
		playlistName, targetAudioDir, downloadedVideoInfoDic = PlaylistTitleInterpreter.splitPlaylistTitle(playlistTitle)

		self.assertEqual(expectedPlayListName, playlistName)
		
	def testSplitPlayListTitle_two_time_frames_suppress(self):
		expectedPlayListName = 'Test_title_two_time_frame_suppress'
		timeInfo = '(s0:05:52-0:07:23 s0:10:52-0:10:53)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideoExtractTimeFramesList = []
		expectedVideoSuppressTimeFramesList = [[352, 443], [652, 653]]

		playlistName, targetAudioDir, downloadedVideoInfoDic = PlaylistTitleInterpreter.splitPlaylistTitle(playlistTitle)

		self.assertEqual(expectedPlayListName, playlistName)
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1), expectedVideoExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1), expectedVideoSuppressTimeFramesList)
	
	def testSplitPlayListTitle_two_time_frames_suppress_last_to_end(self):
		expectedPlayListName = 'Test_title_two_time_frame_suppress'
		timeInfo = '(s0:05:52-0:07:23 s0:10:52-e)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideoExtractTimeFramesList = []
		expectedVideoSuppressTimeFramesList = [[352, 443], [652, 'end']]
		
		playlistName, targetAudioDir, downloadedVideoInfoDic = PlaylistTitleInterpreter.splitPlaylistTitle(playlistTitle)
		
		self.assertEqual(expectedPlayListName, playlistName)
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1),
		                 expectedVideoSuppressTimeFramesList)
	
	def testSplitPlayListTitle_two_time_frames_one_extract_one_suppress(self):
		expectedPlayListName = 'Test_title_two_time_frame_one_extract_one_suppress'
		timeInfo = '(e0:05:52-0:07:23 s0:10:52-0:10:53)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideoExtractTimeFramesList = [[352, 443]]
		expectedVideoSuppressTimeFramesList = [[652, 653]]

		playlistName, targetAudioDir, downloadedVideoInfoDic = PlaylistTitleInterpreter.splitPlaylistTitle(playlistTitle)

		self.assertEqual(expectedPlayListName, playlistName)
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1), expectedVideoExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1), expectedVideoSuppressTimeFramesList)
		
	def testSplitPlayListTitle_two_time_frames_one_extract_one_suppress_two_videos(self):
		# Example of playlist title: playlist_title (s01:05:52-01:07:23 e01:15:52-e  E01:35:52-01:37:23 S01:25:52-e) (s01:05:52-01:07:23 e01:15:52-e S01:25:52-e E01:35:52-01:37:23)
		expectedPlayListName = 'Test_title_two_time_frame_one_extract_one_suppress_two_videos'
		timeInfo = '(E0:05:52-0:07:23 S0:10:52-0:10:53) (e1:05:52-1:07:23 s1:10:52-1:10:53)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideo1ExtractTimeFramesList = [[352, 443]]
		expectedVideo1SuppressTimeFramesList = [[652, 653]]

		expectedVideo2ExtractTimeFramesList = [[3952, 4043]]
		expectedVideo2SuppressTimeFramesList = [[4252, 4253]]

		playlistName, targetAudioDir, downloadedVideoInfoDic = PlaylistTitleInterpreter.splitPlaylistTitle(playlistTitle)

		self.assertEqual(expectedPlayListName, playlistName)
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1), expectedVideo1ExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1), expectedVideo1SuppressTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(2), expectedVideo2ExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(2), expectedVideo2SuppressTimeFramesList)
	
	def testSplitPlayListTitle_two_time_frames_one_extract_one_suppress_two_videos_timeFrames_to_end(self):
		# Example of playlist title: playlist_title (s01:05:52-01:07:23 e01:15:52-e  E01:35:52-01:37:23 S01:25:52-e) (s01:05:52-01:07:23 e01:15:52-e S01:25:52-e E01:35:52-01:37:23)
		expectedPlayListName = 'Test_title_two_time_frame_one_extract_one_suppress_two_videos'
		timeInfo = '(E0:05:52-0:07:23 S0:10:52-e) (e1:05:52-E s1:10:52-1:10:53)'
		playlistTitle = expectedPlayListName + ' ' + timeInfo
		
		expectedVideo1ExtractTimeFramesList = [[352, 443]]
		expectedVideo1SuppressTimeFramesList = [[652, 'end']]
		
		expectedVideo2ExtractTimeFramesList = [[3952, 'end']]
		expectedVideo2SuppressTimeFramesList = [[4252, 4253]]
		
		playlistName, targetAudioDir, downloadedVideoInfoDic = PlaylistTitleInterpreter.splitPlaylistTitle(playlistTitle)
		
		self.assertEqual(expectedPlayListName, playlistName)
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1),
		                 expectedVideo1ExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1),
		                 expectedVideo1SuppressTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(2),
		                 expectedVideo2ExtractTimeFramesList)
		self.assertEqual(downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(2),
		                 expectedVideo2SuppressTimeFramesList)


if __name__ == '__main__':
	unittest.main()
	# tst = TestYoutubeAccessOtherMethods()
	# tst.testSplitPlayListTitle_one_time_frame_extract()
