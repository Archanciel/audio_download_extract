import re
from os.path import sep

from downloadplaylistinfodic import DownloadPlaylistInfoDic
from accesserror import AccessError

class PlaylistTitleParser:
	
	@staticmethod
	def createDownloadVideoInfoDicForPlaylist(playlistUrl,
											  audioRootDir,
											  playlistDownloadRootPath,
											  originalPlaylistTitle,
											  modifiedPlaylistTitle=None):
		"""
		Returns the playlist name and a dictionary whose key is the video index
		and value is a list of two lists, one containing the start and
		end extract positions in seconds, the second list containing the start
		and end suppress positions in seconds.

		Example of playlist title with extract/suppress information:
		E_Klein - le temps {(s01:05:52-01:07:23 e01:15:52-E E01:35:52-01:37:23 S01:25:52-e) (s01:05:52-01:07:23 e01:15:52-e S01:25:52-e E01:35:52-01:37:23)}
		-e or -E means "to end"
		
		:param playlistUrl:                 playlist url to add to the
											download video info div
		:param audioRootDir:                base dir set in the GUI settings containing
											the extracted audio files
		:param playlistDownloadRootPath:    if the playlist is downloaded without
											modifying its download dir by clicking
											on the "Select or create dir" button,
											then the playlistDownloadRootPath is
											equal to the audioRootDir. Otherwise,
											its value is the dir selected or created
											where the playlist will be downloaded.
											In fact, audioRootDir + the selected or
											created sub-dir(s). For example:
											C:\\Users\\Jean-Pierre\\Downloads\\Audio\\
											zz\\UCEM\\Gary Renard
		:param originalPlaylistTitle:
		:param modifiedPlaylistTitle:
		:return:
		"""
		playlistNamePattern = r"([a-zA-Z0-9ÉéÂâÊêÎîÔôÛûÀàÈèÙùËëÏïÜüŸÿçÇö/ '\\_\-:*?\"<>|+,\.]+)(\{.*\})?"
		
		match = re.match(playlistNamePattern, originalPlaylistTitle)
		originalPlaylistName = match.group(1)
		
		videoTimeFramesInfo = originalPlaylistTitle.replace(originalPlaylistName, '')
		originalPlaylistName = originalPlaylistName.strip() # removing originalPlaylistName last space if exist
		
		if modifiedPlaylistTitle is not None:
			match = re.match(playlistNamePattern, modifiedPlaylistTitle)
			modifiedPlaylistName = match.group(1)
			videoTimeFramesInfo = modifiedPlaylistTitle.replace(modifiedPlaylistName, '')
			modifiedPlaylistName = modifiedPlaylistName.strip()  # removing originalPlaylistName last space if exist
		else:
			modifiedPlaylistTitle = originalPlaylistTitle
			modifiedPlaylistName = originalPlaylistName
		
		accessError = None
		downloadVideoInfoDic = None
		
		try:
			downloadVideoInfoDic = DownloadPlaylistInfoDic(playlistUrl=playlistUrl,
			                                               audioRootDir=audioRootDir,
			                                               playlistDownloadRootPath=playlistDownloadRootPath,
			                                               originalPaylistTitle=originalPlaylistTitle,
			                                               originalPlaylistName=originalPlaylistName,
			                                               modifiedPlaylistTitle=modifiedPlaylistTitle,
			                                               modifiedPlaylistName=modifiedPlaylistName)
		except Exception as e:
			errorInfoStr = 'loading download video info dic located in {} failed\nerror info: {}'.format(playlistDownloadRootPath + sep + modifiedPlaylistTitle, str(e))
			accessError = AccessError(AccessError.ERROR_TYPE_PLAYLIST_TIME_FRAME_SYNTAX_ERROR, errorInfoStr)
		
		
		if videoTimeFramesInfo is not None and videoTimeFramesInfo != '':
			try:
				downloadVideoInfoDic, accessError = PlaylistTitleParser.extractTimeInfo(downloadVideoInfoDic,
																						videoTimeFramesInfo,
																						downloadVideoInfoDic.getPlaylistTitleModified())
			except IndexError:
				# the case for example for a playlist title containing parentheses
				# like 'Seconds Out (1977) - Genesis [Full Album]'
				originalPlaylistName = originalPlaylistTitle
				if modifiedPlaylistTitle:
					modifiedPlaylistName = modifiedPlaylistTitle
				else:
					modifiedPlaylistName = originalPlaylistName
				
				downloadVideoInfoDic.updateOriginalPlaylistName(originalPlaylistName)
				downloadVideoInfoDic.updateModifiedPlaylistName(modifiedPlaylistName)
		
		return downloadVideoInfoDic, accessError
	
	@staticmethod
	def extractTimeInfo(downloadVideoInfoDic, videoTimeFramesInfo, playlistTitle):
		"""
		Extracts the time information and add them to the passed downloadVideoInfoDic.
		
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
				except ValueError:
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
