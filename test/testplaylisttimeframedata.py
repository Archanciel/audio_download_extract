import unittest
import os, sys, inspect, glob, time
from datetime import datetime

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
		
from playlisttimeframedata import PlaylistTimeFrameData
from constants import *
			
class TestPlaylistTimeFrameData(unittest.TestCase):
	def testAddTimeFrameDataForVideo(self):
		playlistTimeFrameData = PlaylistTimeFrameData()
		videoIndex = 1
		playlistTimeFrameData.addTimeFrameDataForVideo(videoIndex)
		
		self.assertEqual([], playlistTimeFrameData.getExtractStartEndSecondsLists(videoIndex))
		self.assertEqual([], playlistTimeFrameData.getSuppressStartEndSecondsLists(videoIndex))

	def testExtractTimeFrameDataForVideo_oneTimeFrame(self):
		playlistTimeFrameData = PlaylistTimeFrameData()
		videoIndex = 1
		startEndSecondsList = [1, 10]
		
		playlistTimeFrameData.addExtractStartEndSecondsList(videoIndex, startEndSecondsList)
		
		self.assertEqual([startEndSecondsList], playlistTimeFrameData.getExtractStartEndSecondsLists(videoIndex))
		self.assertEqual([], playlistTimeFrameData.getSuppressStartEndSecondsLists(videoIndex))
	
	def testSuppressTimeFrameDataForVideo_oneTimeFrame(self):
		playlistTimeFrameData = PlaylistTimeFrameData()
		videoIndex = 1
		startEndSecondsList = [10, 20]
		
		playlistTimeFrameData.addSuppressStartEndSecondsList(videoIndex, startEndSecondsList)
		
		self.assertEqual([], playlistTimeFrameData.getExtractStartEndSecondsLists(videoIndex))
		self.assertEqual([startEndSecondsList], playlistTimeFrameData.getSuppressStartEndSecondsLists(videoIndex))
	
	def testExtractTimeFrameDataForVideo_twoTimeFrames(self):
		playlistTimeFrameData = PlaylistTimeFrameData()
		videoIndex = 1
		startEndSecondsList_one = [1, 10]
		startEndSecondsList_two = [15, 20]

		playlistTimeFrameData.addExtractStartEndSecondsList(videoIndex, startEndSecondsList_one)
		playlistTimeFrameData.addExtractStartEndSecondsList(videoIndex, startEndSecondsList_two)

		self.assertEqual([startEndSecondsList_one, startEndSecondsList_two], playlistTimeFrameData.getExtractStartEndSecondsLists(videoIndex))
		self.assertEqual([], playlistTimeFrameData.getSuppressStartEndSecondsLists(videoIndex))
	
	def testSuppressTimeFrameDataForVideo_twoTimeFrames(self):
		playlistTimeFrameData = PlaylistTimeFrameData()
		videoIndex = 1
		startEndSecondsList_one = [1, 10]
		startEndSecondsList_two = [15, 20]
		
		playlistTimeFrameData.addSuppressStartEndSecondsList(videoIndex, startEndSecondsList_one)
		playlistTimeFrameData.addSuppressStartEndSecondsList(videoIndex, startEndSecondsList_two)
		
		self.assertEqual([],
		                 playlistTimeFrameData.getExtractStartEndSecondsLists(videoIndex))
		self.assertEqual([startEndSecondsList_one, startEndSecondsList_two], playlistTimeFrameData.getSuppressStartEndSecondsLists(videoIndex))
	
	def testExtractSuppressTimeFrameDataForVideo_twoTimeFrames(self):
		playlistTimeFrameData = PlaylistTimeFrameData()
		videoIndex = 1
		startEndSecondsList_extract_one = [1, 10]
		startEndSecondsList_extract_two = [15, 20]
		startEndSecondsList_suppress_one = [100, 110]
		startEndSecondsList_suppress_two = [115, 120]

		playlistTimeFrameData.addExtractStartEndSecondsList(videoIndex, startEndSecondsList_extract_one)
		playlistTimeFrameData.addExtractStartEndSecondsList(videoIndex, startEndSecondsList_extract_two)
		playlistTimeFrameData.addSuppressStartEndSecondsList(videoIndex, startEndSecondsList_suppress_one)
		playlistTimeFrameData.addSuppressStartEndSecondsList(videoIndex, startEndSecondsList_suppress_two)

		self.assertEqual([startEndSecondsList_extract_one, startEndSecondsList_extract_two],
		                 playlistTimeFrameData.getExtractStartEndSecondsLists(videoIndex))
		self.assertEqual([startEndSecondsList_suppress_one, startEndSecondsList_suppress_two],
		                 playlistTimeFrameData.getSuppressStartEndSecondsLists(videoIndex))
	
	def testExtractSuppressTimeFrameDataForTwoVideo_twoTimeFrames(self):
		# corresponding playlist title:
		# pl_title (e0:0:1-0:0:10 e0:0:15-0:0:20 s0:1:40-0:1:50 s0:1:55-0:2:0) (e0:60:41-0:16:50 e0:16:55-0:17:0 s2:48:20-s2:48:30 s2:48:35-s2:48:40)
		playlistTimeFrameData = PlaylistTimeFrameData()
		videoIndex = 1
		startEndSecondsList_extract_firstVideo_firstTimeFrame = [1, 10]
		startEndSecondsList_extract_firstVideo_secondTimeFrame = [15, 20]
		startEndSecondsList_suppress_firstVideo_firstTimeFrame = [100, 110]
		startEndSecondsList_suppress_firstVideo_secondTimeFrame = [115, 120]
		
		playlistTimeFrameData.addExtractStartEndSecondsList(videoIndex, startEndSecondsList_extract_firstVideo_firstTimeFrame)
		playlistTimeFrameData.addExtractStartEndSecondsList(videoIndex, startEndSecondsList_extract_firstVideo_secondTimeFrame)
		playlistTimeFrameData.addSuppressStartEndSecondsList(videoIndex, startEndSecondsList_suppress_firstVideo_firstTimeFrame)
		playlistTimeFrameData.addSuppressStartEndSecondsList(videoIndex, startEndSecondsList_suppress_firstVideo_secondTimeFrame)

		videoIndexTwo = 2

		startEndSecondsList_extract_secondVideo_firstTimeFrame = [101, 1010]
		startEndSecondsList_extract_secondVideo_secondTimeFrame = [1015, 1020]
		startEndSecondsList_suppress_secondVideo_firstTimeFrame = [10100, 10110]
		startEndSecondsList_suppress_secondVideo_secondTimeFrame = [10115, 10120]
		
		playlistTimeFrameData.addExtractStartEndSecondsList(videoIndexTwo, startEndSecondsList_extract_secondVideo_firstTimeFrame)
		playlistTimeFrameData.addExtractStartEndSecondsList(videoIndexTwo, startEndSecondsList_extract_secondVideo_secondTimeFrame)
		playlistTimeFrameData.addSuppressStartEndSecondsList(videoIndexTwo, startEndSecondsList_suppress_secondVideo_firstTimeFrame)
		playlistTimeFrameData.addSuppressStartEndSecondsList(videoIndexTwo, startEndSecondsList_suppress_secondVideo_secondTimeFrame)
		
		self.assertEqual([startEndSecondsList_extract_firstVideo_firstTimeFrame, startEndSecondsList_extract_firstVideo_secondTimeFrame],
		                 playlistTimeFrameData.getExtractStartEndSecondsLists(videoIndex))
		self.assertEqual([startEndSecondsList_suppress_firstVideo_firstTimeFrame, startEndSecondsList_suppress_firstVideo_secondTimeFrame],
		                 playlistTimeFrameData.getSuppressStartEndSecondsLists(videoIndex))
		
		self.assertEqual([startEndSecondsList_extract_secondVideo_firstTimeFrame, startEndSecondsList_extract_secondVideo_secondTimeFrame],
		                 playlistTimeFrameData.getExtractStartEndSecondsLists(videoIndexTwo))
		self.assertEqual([startEndSecondsList_suppress_secondVideo_firstTimeFrame, startEndSecondsList_suppress_secondVideo_secondTimeFrame],
		                 playlistTimeFrameData.getSuppressStartEndSecondsLists(videoIndexTwo))


if __name__ == '_main_':
	unittest.main()
#	tst = TestTransferFiles()
#	tst.testPathUploadToCloud_invalid_fileName()
