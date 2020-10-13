import re
from pytube import YouTube, Playlist

from constants import *
from downloadedvideoinfodic import DownloadedVideoInfoDic

class PlaylistTitleInterpreter:
	
	@staticmethod
	def splitPlayListTitle(playlistTitle):
		'''
		Returns the playlist name and a dictionary whose key is the video index
		and value is a list of two lists, one containing the start and
		end extract positions in seconds, the second list containing the start
		and end suppress positions in seconds.

		@:return playlistName, targetAudioDir, downloadedVideoInfoDic
		'''
		playlistNamePattern = r'([a-zaA-Z_\d]+)(?: ([\(sSeE\d:\- \)]*))?'
		
		match = re.match(playlistNamePattern, playlistTitle)
		playlistName = match.group(1)
		videoTimeFramesInfo = match.group(2)
		targetAudioDir = AUDIO_DIR + DIR_SEP + playlistName
		
		downloadedVideoInfoDic = DownloadedVideoInfoDic(targetAudioDir, playlistName)
		
		if videoTimeFramesInfo != None:
			PlaylistTitleInterpreter.extractTimeInfo(downloadedVideoInfoDic, videoTimeFramesInfo)
		
		return playlistName, targetAudioDir, downloadedVideoInfoDic
	
	@staticmethod
	def extractTimeInfo(downloadedVideoInfoDic, videoTimeFramesInfo):
		videoTimeFramesPattern = r'(\([sSeE\d:\- ]*\) ?)'
		startEndTimeFramePattern = r'([\dsSeE:\-]+)'
		videoIndex = 1
		
		for videoTimeFramesGroup in re.finditer(videoTimeFramesPattern, videoTimeFramesInfo):
			# print('video {} timeFrames'.format(videoIndex), videoTimeFramesGroup.group(0))
			
			for startEndTimeFrameGroup in re.finditer(startEndTimeFramePattern, videoTimeFramesGroup.group(0)):
				startEndTimeFrame = startEndTimeFrameGroup.group(0)
				startEndSecondsList = PlaylistTitleInterpreter.convertToStartEndSeconds(startEndTimeFrame[1:])
				if startEndTimeFrame[0].upper() == 'E':
					downloadedVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList)
				elif startEndTimeFrame[0].upper() == 'S':
					downloadedVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList)
			# print(startEndTimeFrame)
			videoIndex += 1
		
		return downloadedVideoInfoDic
	
	@staticmethod
	def convertToStartEndSeconds(startEndTimeFrame):
		'''
		Returns a 2 element list containing the start end time frame in seconds.

		:param startEndTimeFrame: example: 2:23:41-2:24:01 or 2:23:41-e (means to end !)
		:return: example: [8621, 8641]
		'''
		timeLst = startEndTimeFrame.split('-')
		timeStartHHMMSS = timeLst[0].split(':')
		timeEndHHMMSS = timeLst[1].split(':')
		
		timeStartSec = int(timeStartHHMMSS[0]) * 3600 + int(timeStartHHMMSS[1]) * 60 + int(timeStartHHMMSS[2])
		
		if timeEndHHMMSS[0].upper() == 'E':
			timeEndSec = 'end'
		else:
			timeEndSec = int(timeEndHHMMSS[0]) * 3600 + int(timeEndHHMMSS[1]) * 60 + int(timeEndHHMMSS[2])
		
		return [timeStartSec, timeEndSec]
