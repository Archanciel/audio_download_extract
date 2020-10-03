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
		playlistTimeFrameData = PlaylistTimeFrameData()
		videoIndex = 1
		startEndSecondsList_extract_vidOne_one = [1, 10]
		startEndSecondsList_extract_vidOne_two = [15, 20]
		startEndSecondsList_suppress_vidOne_one = [100, 110]
		startEndSecondsList_suppress_vidOne_two = [115, 120]
		
		playlistTimeFrameData.addExtractStartEndSecondsList(videoIndex, startEndSecondsList_extract_vidOne_one)
		playlistTimeFrameData.addExtractStartEndSecondsList(videoIndex, startEndSecondsList_extract_vidOne_two)
		playlistTimeFrameData.addSuppressStartEndSecondsList(videoIndex, startEndSecondsList_suppress_vidOne_one)
		playlistTimeFrameData.addSuppressStartEndSecondsList(videoIndex, startEndSecondsList_suppress_vidOne_two)

		videoIndexTwo = 2

		startEndSecondsList_extract_vidTwo_one = [101, 1010]
		startEndSecondsList_extract_vidTwo_two = [1015, 1020]
		startEndSecondsList_suppress_vidTwo_one = [10100, 10110]
		startEndSecondsList_suppress_vidTwo_two = [10115, 10120]
		
		playlistTimeFrameData.addExtractStartEndSecondsList(videoIndexTwo, startEndSecondsList_extract_vidTwo_one)
		playlistTimeFrameData.addExtractStartEndSecondsList(videoIndexTwo, startEndSecondsList_extract_vidTwo_two)
		playlistTimeFrameData.addSuppressStartEndSecondsList(videoIndexTwo, startEndSecondsList_suppress_vidTwo_one)
		playlistTimeFrameData.addSuppressStartEndSecondsList(videoIndexTwo, startEndSecondsList_suppress_vidTwo_two)
		
		self.assertEqual([startEndSecondsList_extract_vidOne_one, startEndSecondsList_extract_vidOne_two],
		                 playlistTimeFrameData.getExtractStartEndSecondsLists(videoIndex))
		self.assertEqual([startEndSecondsList_suppress_vidOne_one, startEndSecondsList_suppress_vidOne_two],
		                 playlistTimeFrameData.getSuppressStartEndSecondsLists(videoIndex))
		
		self.assertEqual([startEndSecondsList_extract_vidTwo_one, startEndSecondsList_extract_vidTwo_two],
		                 playlistTimeFrameData.getExtractStartEndSecondsLists(videoIndexTwo))
		self.assertEqual([startEndSecondsList_suppress_vidTwo_one, startEndSecondsList_suppress_vidTwo_two],
		                 playlistTimeFrameData.getSuppressStartEndSecondsLists(videoIndexTwo))


if __name__ == '_main_':
	unittest.main()
#	tst = TestTransferFiles()
#	tst.testPathUploadToCloud_invalid_fileName()
