import re

from constants import *
from downloadvideoinfodic import DownloadVideoInfoDic
from accesserror import AccessError

class PlaylistTitleParser:
	
	@staticmethod
	def createDownloadVideoInfoDicForPlaylist(playlistTitle, audioDir):
		"""
		Returns the playlist name and a dictionary whose key is the video index
		and value is a list of two lists, one containing the start and
		end extract positions in seconds, the second list containing the start
		and end suppress positions in seconds.

		Example of playlist title:
		The title {(s01:05:52-01:07:23 e01:15:52-E E01:35:52-01:37:23 S01:25:52-e) (s01:05:52-01:07:23 e01:15:52-e S01:25:52-e E01:35:52-01:37:23)}
		-e or -E means "to end"

		@:return downloadVideoInfoDic
				 accessError in case of problem, None otherwise
		"""
		playlistNamePattern = r'([\w_ ]+)((\([\d:\-eEsS ]*\)))?'
		playlistNamePattern = r"([a-zA-Z0-9ÉéÂâÊêÎîÔôÛûÀàÈèÙùËëÏïÜüŸÿçö :'_-]+)(\{.*\})?"
		
		match = re.match(playlistNamePattern, playlistTitle)
		playlistName = match.group(1)
		
		videoTimeFramesInfo = playlistTitle.replace(playlistName, '')
		playlistName = playlistName.strip() # removing playlistName last space if exist
		targetAudioDir = audioDir + DIR_SEP + playlistName
		
		downloadVideoInfoDic = DownloadVideoInfoDic(targetAudioDir, playlistTitle, playlistName)
		accessError = None
		
		if videoTimeFramesInfo is not None:
			downloadVideoInfoDic, accessError = PlaylistTitleParser.extractTimeInfo(downloadVideoInfoDic,
			                                                                        videoTimeFramesInfo, playlistTitle)
		
		return downloadVideoInfoDic, accessError
	
	@staticmethod
	def extractTimeInfo(downloadVideoInfoDic, videoTimeFramesInfo, playlistTitle):
		"""
		
		:param downloadVideoInfoDic:
		:param videoTimeFramesInfo:
		:param playlistTitle: used only in case of time frame syntax error

		@:return downloadVideoInfoDic
				 accessError in case of problem, None otherwise
		"""
		videoTimeFramesPattern = r'(\([sSeE\d:\- ]*\) ?)'
		startEndTimeFramePattern = r'([\dsSeE:\-]+)'
		videoIndex = 1
		accessError = None
		
		for videoTimeFramesGroup in re.finditer(videoTimeFramesPattern, videoTimeFramesInfo):
			# in case the playlist is re-downloaded, the time frame in seconds data
			# must be purged. Otherwise, the time frames in seconds will be added
			# to the existing time frames set at the first download !
			downloadVideoInfoDic.removeTimeFrameInSecondsDataIfExistForVideoIndex(videoIndex)
	
			for startEndTimeFrameGroup in re.finditer(startEndTimeFramePattern, videoTimeFramesGroup.group(0)):
				startEndTimeFrame = startEndTimeFrameGroup.group(0)
				try:
					startEndSecondsList = PlaylistTitleParser.convertToStartEndSeconds(startEndTimeFrame[1:])
				except ValueError as e:
					accessError = AccessError(AccessError.ERROR_TYPE_PLAYLIST_TIME_FRAME_SYNTAX_ERROR, 'time frame syntax error "{}" detected in playlist title: "{}".'.format(startEndTimeFrame, playlistTitle))
					
					return downloadVideoInfoDic, accessError
				
				if startEndTimeFrame[0].upper() == 'E':
					downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList)
				elif startEndTimeFrame[0].upper() == 'S':
					downloadVideoInfoDic.addSuppressStartEndSecondsListForVideoIndex(videoIndex, startEndSecondsList)

			videoIndex += 1
		
		return downloadVideoInfoDic, accessError
	
	@staticmethod
	def convertToStartEndSeconds(startEndTimeFrame):
		"""
		Returns a 2 element list containing the start end time frame in seconds.

		:param startEndTimeFrame: example: 2:23:41-2:24:01 or 2:23:41-e (means to end !)
		:return: example: [8621, 8641]
		"""
		timeLst = startEndTimeFrame.split('-')
		timeStartHHMMSS = timeLst[0].split(':')
		timeEndHHMMSS = timeLst[1].split(':')
		
		timeStartSec = int(timeStartHHMMSS[0]) * 3600 + int(timeStartHHMMSS[1]) * 60 + int(timeStartHHMMSS[2])
		
		if timeEndHHMMSS[0].upper() == 'E':
			timeEndSec = 'end'
		else:
			timeEndSec = int(timeEndHHMMSS[0]) * 3600 + int(timeEndHHMMSS[1]) * 60 + int(timeEndHHMMSS[2])
		
		return [timeStartSec, timeEndSec]
