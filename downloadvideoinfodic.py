import json
from datetime import datetime

from constants import *

KEY_PLAYLIST = 'playlist'
KEY_PLAYLIST_TITLE = 'pl_title'
KEY_PLAYLIST_NAME = 'pl_name'
KEY_PLAYLIST_DOWNLOAD_DIR = 'pl_downloadDir'
KEY_PLAYLIST_NEXT_VIDEO_INDEX = 'pl_nextVideoIndex'

KEY_VIDEOS = 'videos'
KEY_VIDEO_TITLE = 'vd_title'
KEY_VIDEO_URL = 'vd_url'
KEY_VIDEO_DOWNLOAD_FILENAME = 'vd_downloadedFileName'
KEY_VIDEO_DOWNLOAD_TIME = 'vd_downloadTime'
KEY_VIDEO_TIME_FRAMES_IN_SECONDS = 'vd_startEndTimeFramesInSeconds'

KEY_TIMEFRAME_EXTRACT = 'vd_extract'
KEY_VIDEO_EXTRACTED_FILES = 'vd_extractedFiles'
KEY_FILENAME = 'ex_fileName'
KEY_FILE_TIMEFRAME_HHMMSS = 'ex_startEndTimeFrameHHMMSS'

KEY_TIMEFRAME_SUPPRESS = 'vd_suppress'
KEY_VIDEO_SUPPRESS_FILE = 'sp_fileName'
KEY_TIMEFRAMES_HHMMSS_SUPPRESSED = 'sp_startEndTimeFramesHHMMSS_suppressed'
KEY_TIMEFRAMES_HHMMSS_KEPT = 'sp_startEndTimeFramesHHMMSS_kept'

class DownloadVideoInfoDic:
	wasDicUpdated = False
	cachedRateAccessNumber = 0

	def __init__(self, downloadDir, playlistTitle='', playlistName=''):
		self._loadDicIfExist(downloadDir, playlistTitle, playlistName)
		
	def __str__(self):
		try:
			return json.dumps(self.dic, sort_keys=False, indent=4)
		except Exception as e:
			print(e)
	
	def _loadDicIfExist(self, downloadDir, playlistTitle, playlistName):
		"""
		If a file containing the dictionary data for the corresponding playlist,
		it is loaded into the self.dic instance variable. Otherwise, the dic variable
		is initialized to an empty dic.
		
		:return:
		"""
		infoDicFilePathName = self.getInfoDicFilePathName(downloadDir, playlistName)

		if os.path.isfile(infoDicFilePathName):
			try:
				with open(infoDicFilePathName, 'r') as f:
					self.dic = json.load(f)
			except Exception as e:
				print(e)
		else:
			self.dic = {}
			self.dic[KEY_PLAYLIST] = {}
			self.dic[KEY_PLAYLIST][KEY_PLAYLIST_TITLE] = playlistTitle
			self.dic[KEY_PLAYLIST][KEY_PLAYLIST_NAME] = playlistName
			self.dic[KEY_PLAYLIST][KEY_PLAYLIST_DOWNLOAD_DIR] = downloadDir
			self.dic[KEY_PLAYLIST][KEY_PLAYLIST_NEXT_VIDEO_INDEX] = 1
			self.dic[KEY_VIDEOS] = {}
	
	def saveDic(self):
		with open(self.getInfoDicFilePathName(self.getPlaylistDownloadDir(), self.getPlaylistName()), 'w') as f:
			try:
				json.dump(self.dic,
				          f,
				          indent=4,
				          sort_keys=True)
			except Exception as e:
				print(self)
				print(e)

	def getNextVideoIndex(self):
		if KEY_PLAYLIST in self.dic.keys():
			return self.dic[KEY_PLAYLIST][KEY_PLAYLIST_NEXT_VIDEO_INDEX]
		else:
			return None
		
	def getPlaylistTitle(self):
		"""
		Return the play list title, which is the playlist name + the optional extract
		or suppress time frames definitions.
	
		:return:
		"""
		if KEY_PLAYLIST in self.dic.keys():
			return self.dic[KEY_PLAYLIST][KEY_PLAYLIST_TITLE]
		else:
			return None
	
	def getPlaylistName(self):
		"""
		Return the play list name, which is the playlist title without the optional
		extract or suppress time frames definitions.
	
		:return:
		"""
		if KEY_PLAYLIST in self.dic.keys():
			return self.dic[KEY_PLAYLIST][KEY_PLAYLIST_NAME]
		else:
			return None
	
	def getPlaylistDownloadDir(self):
		if KEY_PLAYLIST in self.dic.keys():
			return self.dic[KEY_PLAYLIST][KEY_PLAYLIST_DOWNLOAD_DIR]
		else:
			return None
	
	def getInfoDicFilePathName(self, downloadDir, playlistName):
		return downloadDir + DIR_SEP + playlistName + '_dic.txt'
	
	def getVideoIndexes(self):
		'''
		Returns a list of video indexes as string.
		
		:return: example: ['1', '2']
		'''
		return list(self.dic[KEY_VIDEOS].keys())
	
	def existVideoInfoForVideoTitle(self, videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)
		
		return videoIndex is not None
	
	def getVideoTitleForVideoIndex(self, videoIndex):
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if KEY_VIDEO_TITLE in videoInfoDic.keys():
			return videoInfoDic[KEY_VIDEO_TITLE]
		else:
			return None

	def getVideoUrlForVideoIndex(self, videoIndex):
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if KEY_VIDEO_URL in videoInfoDic.keys():
			return videoInfoDic[KEY_VIDEO_URL]
		else:
			return None
	
	def getVideoUrlForVideoTitle(self, videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)
		
		if videoIndex:
			return self._getVideoInfoForVideoIndex(videoIndex)[KEY_VIDEO_URL]
		else:
			return None
	
	def getVideoFileNameForVideoIndex(self, videoIndex):
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if KEY_VIDEO_DOWNLOAD_FILENAME in videoInfoDic.keys():
			return videoInfoDic[KEY_VIDEO_DOWNLOAD_FILENAME]
		else:
			return None
	
	def getVideoFileNameForVideoTitle(self, videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)

		if videoIndex:
			return self._getVideoInfoForVideoIndex(videoIndex)[KEY_VIDEO_DOWNLOAD_FILENAME]
		else:
			return None
	
	def getVideoDownloadTimeForVideoIndex(self, videoIndex):
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if KEY_VIDEO_DOWNLOAD_TIME in videoInfoDic.keys():
			return videoInfoDic[KEY_VIDEO_DOWNLOAD_TIME]
		else:
			return None

	def getVideoDownloadTimeForVideoTitle(self, videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)
		
		if videoIndex:
			return self._getVideoInfoForVideoIndex(videoIndex)[KEY_VIDEO_DOWNLOAD_TIME]
		else:
			return None

	def isExtractTimeFrameDataAvailableForVideoIndex(self, videoIndex):
		if KEY_VIDEO_TIME_FRAMES_IN_SECONDS in self.dic[KEY_VIDEOS][videoIndex].keys():
			if KEY_TIMEFRAME_EXTRACT in self.dic[KEY_VIDEOS][videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS]:
				return self.dic[KEY_VIDEOS][videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS][KEY_TIMEFRAME_EXTRACT] != []
		
		return False
	
	def isSuppressTimeFrameDataAvailableForVideoIndex(self, videoIndex):
		if KEY_VIDEO_TIME_FRAMES_IN_SECONDS in self.dic[KEY_VIDEOS][videoIndex].keys():
			if KEY_TIMEFRAME_SUPPRESS in self.dic[KEY_VIDEOS][videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS]:
				return self.dic[KEY_VIDEOS][videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS][KEY_TIMEFRAME_SUPPRESS] != []
		
		return False
	
	def _addTimeFrameDataForVideo(self, videoIndex):
		'''
		Protected method used internally only.
		
		:param videoIndex:
		:return:
		'''
		videoTimeFramesDic = {KEY_TIMEFRAME_EXTRACT: [], KEY_TIMEFRAME_SUPPRESS: []}
		
		self.dic[KEY_VIDEOS][videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS] = videoTimeFramesDic

	def removeTimeFrameInSecondsDataIfExistForVideoIndex(self, videoIndex):
		videoIndex = str(videoIndex)
		
		if not videoIndex in self.dic[KEY_VIDEOS].keys():
			return

		if not KEY_VIDEO_TIME_FRAMES_IN_SECONDS in self.dic[KEY_VIDEOS][videoIndex].keys():
			return
		else:
			del self.dic[KEY_VIDEOS][videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS]

	def addExtractStartEndSecondsListForVideoIndex(self, videoIndex, startEndSecondsList):
		videoIndex = str(videoIndex)
		
		if not videoIndex in self.dic[KEY_VIDEOS].keys():
			self.dic[KEY_VIDEOS][videoIndex] = {}

		if not KEY_VIDEO_TIME_FRAMES_IN_SECONDS in self.dic[KEY_VIDEOS][videoIndex].keys():
			self._addTimeFrameDataForVideo(videoIndex)
		
		self.dic[KEY_VIDEOS][videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS][KEY_TIMEFRAME_EXTRACT].append(startEndSecondsList)
	
	def addSuppressStartEndSecondsListForVideoIndex(self, videoIndex, startEndSecondsList):
		videoIndex = str(videoIndex)

		if not videoIndex in self.dic[KEY_VIDEOS].keys():
			self.dic[KEY_VIDEOS][videoIndex] = {}
		
		if not KEY_VIDEO_TIME_FRAMES_IN_SECONDS in self.dic[KEY_VIDEOS][videoIndex].keys():
			self._addTimeFrameDataForVideo(videoIndex)
		
		self.dic[KEY_VIDEOS][videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS][KEY_TIMEFRAME_SUPPRESS].append(startEndSecondsList)

	def getExtractStartEndSecondsListsForVideoIndex(self, videoIndex):
		videoIndex = str(videoIndex)

		if not videoIndex in self.dic[KEY_VIDEOS].keys():
			return None

		if KEY_VIDEO_TIME_FRAMES_IN_SECONDS in self.dic[KEY_VIDEOS][videoIndex].keys():
			return self.dic[KEY_VIDEOS][videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS][KEY_TIMEFRAME_EXTRACT]
		else:
			return None
	
	def getSuppressStartEndSecondsListsForVideoIndex(self, videoIndex):
		videoIndex = str(videoIndex)

		if not videoIndex in self.dic[KEY_VIDEOS].keys():
			return None

		if KEY_VIDEO_TIME_FRAMES_IN_SECONDS in self.dic[KEY_VIDEOS][videoIndex].keys():
			return self.dic[KEY_VIDEOS][videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS][KEY_TIMEFRAME_SUPPRESS]
		else:
			return None

	def addVideoInfoForVideoIndex(self,
	                              videoIndex,
	                              videoTitle,
	                              videoUrl,
	                              downloadedFileName):
		"""
		Creates the video info sub-dic for the video index if necessary.
		
		Then, adds to the sub-dic the video title, the video url and the video downloaded
		file name.

		:param videoIndex:
		:param videoTitle:
		:param videoUrl:
		:param downloadedFileName:
		"""
		if not KEY_VIDEOS in self.dic.keys():
			self.dic[KEY_VIDEOS] = {}
			
		videoIndexKey = str(videoIndex)
		
		if not videoIndexKey in self.dic[KEY_VIDEOS].keys():
			videoIndexDic = {}
			self.dic[KEY_VIDEOS][videoIndexKey] = videoIndexDic
		else:
			videoIndexDic = self.dic[KEY_VIDEOS][videoIndexKey]
			
		additionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_VIDEO_INFO_FILE)

		videoIndexDic[KEY_VIDEO_TITLE] = videoTitle
		videoIndexDic[KEY_VIDEO_URL] = videoUrl
		videoIndexDic[KEY_VIDEO_DOWNLOAD_FILENAME] = downloadedFileName
		videoIndexDic[KEY_VIDEO_DOWNLOAD_TIME] = additionTimeStr

		self.dic[KEY_PLAYLIST][KEY_PLAYLIST_NEXT_VIDEO_INDEX] = videoIndex + 1

	def removeVideoInfoForVideoTitle(self,
	                              videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)

		if videoIndex:
			del self.dic[KEY_VIDEOS][videoIndex]
			nextVideoIndex = self.dic[KEY_PLAYLIST][KEY_PLAYLIST_NEXT_VIDEO_INDEX]
			self.dic[KEY_PLAYLIST][KEY_PLAYLIST_NEXT_VIDEO_INDEX] = nextVideoIndex - 1
	
	def _getVideoInfoForVideoIndex(self, videoIndex):
		'''
		Returns the video info dic associated to the passedkey videoIndexKey.
		Protected method used internally only.

		:param videoIndex:
		:return: dictionary containing video information
		'''
		videoIndex = str(videoIndex)
		
		videoInfoDic = None
		
		try:
			videoInfoDic = self.dic[KEY_VIDEOS][videoIndex]
		except KeyError:
			pass
		
		if videoInfoDic == None:
			videoInfoDic = {}
			
		return videoInfoDic
	
	def getVideoIndexForVideoTitle(self, videoTitle):
		for key in self.dic[KEY_VIDEOS].keys():
			if self.getVideoTitleForVideoIndex(key) == videoTitle:
				return key
		
		return None
	
	def addExtractedFileInfoForVideoIndexTimeFrameIndex(self,
	                                                    videoIndex,
	                                                    timeFrameIndex,
	                                                    extractedFileName,
	                                                    startEndHHMMSS_TimeFramesList):
		"""
		Creates the extracted files info dic if necessary.
		
		Then, adds to the sub-dic the extracted file name and its corresponding
		time frame in HH:MM:SS format.
		
		:param videoIndex:
		:param timeFrameIndex:
		:param extractedFileName:
		:param HHMMSS_timeFramesList. Example ['0:23:45', '0:24:54']
		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		extractedFilesSubDic = {}
		timeFrameIndex = str(timeFrameIndex)
		
		if KEY_VIDEO_EXTRACTED_FILES not in videoInfoDic.keys():
			videoInfoDic[KEY_VIDEO_EXTRACTED_FILES] = extractedFilesSubDic
		else:
			extractedFilesSubDic = videoInfoDic[KEY_VIDEO_EXTRACTED_FILES]
			
		extractedFilesSubDic[timeFrameIndex] = {KEY_FILENAME: extractedFileName,
		                                        KEY_FILE_TIMEFRAME_HHMMSS: startEndHHMMSS_TimeFramesList}
	
	def isExtractedFileInfoAvailableForVideoIndex(self, videoIndex):
		"""
		Returns True if extract info for the passed video index exist. This means
		that the audio portions for the concerned video were already extracted.

		:param videoIndex:
		
		:return True or False
		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		return KEY_VIDEO_EXTRACTED_FILES in videoInfoDic.keys()
	
	def getStartEndHHMMSS_TimeFrameForExtractedFileName(self, videoIndex, extractedFileName):
		"""
		Returns the time frame in HH:MM:SS format for the passed extracted file name
		extracted from the video videoIndexKey.

		Unlike suppressing audio portions which produces only one mp3 file per
		video, extracting audio portions produces potentially more than one
		mp3 file per video. So, obtaining a start end HHMMSS time frame list
		for a video index is nonsensical !
		
		:param videoIndex:
		:param extractedFileName:

		:return: startEndHHMMSS time frame list. Example: ['0:23:45', '0:24:54']
		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)

		if KEY_VIDEO_EXTRACTED_FILES not in videoInfoDic.keys():
			return None
		else:
			extractedFilesSubDic = videoInfoDic[KEY_VIDEO_EXTRACTED_FILES]
			
			for key in extractedFilesSubDic.keys():
				if extractedFileName == extractedFilesSubDic[key][KEY_FILENAME]:
					return extractedFilesSubDic[key][KEY_FILE_TIMEFRAME_HHMMSS]
	
	def getExtractedFilePathNameForVideoIndexTimeFrameIndex(self,
	                                                        videoIndex,
	                                                        timeFrameIndex):
		"""
		Returns the extracted file path name for the passed video index and
		time frame index.

		:param videoIndex:
		:param timeFrameIndex:

		:return: file path name. Example:
			     D:\\\\Users\\\\Jean-Pierre\\\\Downloads\\\\Audiobooks\\\\Various\\\\Wear a mask. Help slow the spread of Covid-19._1.mp3
		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if KEY_VIDEO_EXTRACTED_FILES not in videoInfoDic.keys():
			return None
		else:
			extractedFilesSubDic = videoInfoDic[KEY_VIDEO_EXTRACTED_FILES]
			timeFrameIndexExtractedFileInfo = extractedFilesSubDic[str(timeFrameIndex)]
			return self.getPlaylistDownloadDir() + DIR_SEP + timeFrameIndexExtractedFileInfo[KEY_FILENAME]
	
	def addSuppressedFileInfoForVideoIndex(self,
	                                       videoIndex,
	                                       suppressedFileName,
	                                       HHMMSS_suppressedTimeFramesList,
	                                       HHMMSS_keptTimeFramesList):
		"""
		Creates the extracted files info dic if necessary.

		Then, adds to the sub-dic the extracted file name and its corresponding
		time frame in HH:MM:SS format.

		:param videoIndex:
		:param suppressedFileName:
		:param HHMMSS_suppressedTimeFramesList list of suppressed time frames.
											 Example: ['0:23:45-0:24:54', '1:03:45-1:24:54']
		:param HHMMSS_keptTimeFramesList     list of kept time frames.
											 Example: ['0:0:0-0:23:45', '0:24:54-1:03:45', '1:24:54-1:55:12']

		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		suppressedFileSubDic = {}
		
		if KEY_VIDEO_SUPPRESS_FILE not in videoInfoDic.keys():
			videoInfoDic[KEY_VIDEO_SUPPRESS_FILE] = suppressedFileSubDic
		else:
			suppressedFileSubDic = videoInfoDic[KEY_VIDEO_SUPPRESS_FILE]
		
		suppressedFileSubDic[KEY_FILENAME] = suppressedFileName
		suppressedFileSubDic[KEY_TIMEFRAMES_HHMMSS_SUPPRESSED] = HHMMSS_suppressedTimeFramesList
		suppressedFileSubDic[KEY_TIMEFRAMES_HHMMSS_KEPT] = HHMMSS_keptTimeFramesList
	
	def isSuppressedFileInfoAvailableForVideoIndex(self, videoIndex):
		"""
		Returns True if suppress info for the passed video index exist. This means
		that the audio without the suppressed portions for the concerned video
		was already created.

		:param videoIndex:

		:return True or False
		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		return KEY_VIDEO_SUPPRESS_FILE in videoInfoDic.keys()
	
	def getSuppressedFileNameForVideoIndex(self, videoIndex):
		"""
		Returns the suppressed time frames in HH:MM:SS format for the passed video
		index.

		:param videoIndex:

		:return: suppressed file name
		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if KEY_VIDEO_SUPPRESS_FILE not in videoInfoDic.keys():
			return None
		else:
			return videoInfoDic[KEY_VIDEO_SUPPRESS_FILE][KEY_FILENAME]
	
	def getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(self, videoIndex):
		"""
		Returns the suppressed time frames in HH:MM:SS format for the passed video
		index.
		
		Unlike extracting audio portions which produces potentially more than one
		mp3 file per video, suppressing audio portions produces only one mp3 file
		per video. So, obtaining a start end HHMMSS time frame list	for a
		specific file name is nonsensical since only one mp3 file is produced
		when suppressing time frames !

		:param videoIndex:

		:return: startEndHHMMSS time frame list. Example: ['0:23:45', '0:24:54']
		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if KEY_VIDEO_SUPPRESS_FILE not in videoInfoDic.keys():
			return None
		else:
			return videoInfoDic[KEY_VIDEO_SUPPRESS_FILE][KEY_TIMEFRAMES_HHMMSS_SUPPRESSED]
	
	def getKeptStartEndHHMMSS_TimeFramesForVideoIndex(self, videoIndex):
		"""
		Returns the suppressed time frames in HH:MM:SS format for the passed video
		index.

		:param videoIndex:

		:return: startEndHHMMSS time frame list. Example: ['0:23:45', '0:24:54']
		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if KEY_VIDEO_SUPPRESS_FILE not in videoInfoDic.keys():
			return None
		else:
			return videoInfoDic[KEY_VIDEO_SUPPRESS_FILE][KEY_TIMEFRAMES_HHMMSS_KEPT]


if __name__ == "__main__":
	if os.name == 'posix':
		audioDir = '/storage/emulated/0/Download/Audiobooks/various'
	else:
		audioDir = 'D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks\\various'
		
	dvi = DownloadVideoInfoDic(audioDir, 'essai_vid_info (s01:05:52-01:07:23 e01:15:52-E E01:35:52-01:37:23 S01:25:52-e)', 'essai_vid_info')
	dvi.addVideoInfoForVideoIndex(1, 'Title_vid_1', 'https://youtube.com/watch?v=9iPvLx7gotk', 'Title_vid_1.mp4')
	dvi.addVideoInfoForVideoIndex(2, 'title_vid_2', 'https://youtube.com/watch?v=9iPvL8880999', 'Title_vid_2.mp4')
	dvi.addExtractStartEndSecondsListForVideoIndex(1, [34, 56])
	dvi.addExtractStartEndSecondsListForVideoIndex(1, [34, 65])
	dvi.addSuppressStartEndSecondsListForVideoIndex(1, [[340, 560], [840, 960]])
	dvi.addSuppressStartEndSecondsListForVideoIndex(3, [3400, 5600])
	dvi.addExtractedFileInfoForVideoIndexTimeFrameIndex(1, 1, 'title_1_1.mp3', ['0:2:3', '0:4:56'])
	dvi.addExtractedFileInfoForVideoIndexTimeFrameIndex(1, 2, 'title_1_2.mp3', ['0:20:3', '0:40:56'])
	dvi.addExtractedFileInfoForVideoIndexTimeFrameIndex(2, 1, 'title_2_1.mp3', ['0:2:3', '0:4:56'])
	dvi.addSuppressedFileInfoForVideoIndex(1, 'title_1_s.mp3', ['0:23:45-0:24:54', '1:03:45-1:24:54'], ['0:0:0-0:23:45', '0:24:54-1:03:45', '1:24:54-1:55:12'])

	print(dvi.getExtractedFilePathNameForVideoIndexTimeFrameIndex(videoIndex=1,timeFrameIndex=1))
	
	print(dvi.getSuppressStartEndSecondsListsForVideoIndex(1))
	print(dvi.getSuppressedFileNameForVideoIndex(1))
	print(dvi.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(1))
