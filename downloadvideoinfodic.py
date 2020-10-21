import json
from datetime import datetime

from constants import *

KEY_VIDEO_TITLE = 'title'
KEY_VIDEO_URL = 'playlistUrl'
KEY_VIDEO_DOWNLOAD_FILENAME = 'downloadedFileName'
KEY_VIDEO_DOWNLOAD_TIME = 'downloadTime'
KEY_VIDEO_TIME_FRAMES_IN_SECONDS = 'startEndTimeFramesInSeconds'
KEY_TIMEFRAME_EXTRACT = 'extract'
KEY_TIMEFRAME_SUPPRESS = 'suppress'
KEY_VIDEO_EXTRACTED_FILES = 'extracted files'
KEY_FILENAME = 'fileName'
KEY_FILE_TIMEFRAME_HHMMSS = 'startEndTimeFrameHHMMSS'
KEY_VIDEO_SUPPRESS_FILE = 'suppressed file'
KEY_TIMEFRAMES_HHMMSS_SUPPRESSED = 'startEndTimeFramesHHMMSS_suppressed'
KEY_TIMEFRAMES_HHMMSS_KEPT = 'startEndTimeFramesHHMMSS_kept'


class DownloadVideoInfoDic:
	wasDicUpdated = False
	cachedRateAccessNumber = 0
	
	def __init__(self, downloadDir, playlistName=''):
		self.downloadDir = downloadDir
		self.playlistName = playlistName
		self._loadDicIfExist()
	
	def __str__(self):
		mainStr = 'playlistName: ' + self.playlistName + '\n' + 'downloadDir: ' + self.downloadDir
		dicStr = json.dumps(self.dic, sort_keys=False, indent=4)
		
		return mainStr + '\n' + dicStr
	
	def _loadDicIfExist(self):
		"""
		If a file containing the dictionary data for the corresponding playlist,
		it is loaded into the self.dic instance variable. Otherwise, the dic variable
		is initialized to an empty dic.
		
		:return:
		"""
		infoDicFilePathName = self.getInfoDicFilePathName()
		
		if os.path.isfile(infoDicFilePathName):
			with open(infoDicFilePathName, 'r') as f:
				self.dic = json.load(f)
		else:
			self.dic = {}
	
	def saveDic(self):
		with open(self.getInfoDicFilePathName(), 'w') as f:
			json.dump(self.dic,
			          f,
			          indent=4,
			          sort_keys=True)
	
	def getInfoDicFilePathName(self):
		return self.downloadDir + DIR_SEP + self.playlistName + '_dic.txt'
	
	def getVideoIndexes(self):
		"""
		Returns a list of video indexes as string.
		
		:return: example: ['1', '2']
		"""
		return list(self.dic.keys())
	
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
		
		return self._getVideoInfoForVideoIndex(videoIndex)[KEY_VIDEO_URL]
	
	def getVideoFileNameForVideoIndex(self, videoIndex):
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if KEY_VIDEO_DOWNLOAD_FILENAME in videoInfoDic.keys():
			return videoInfoDic[KEY_VIDEO_DOWNLOAD_FILENAME]
		else:
			return None
	
	def getVideoFileNameForVideoTitle(self, videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)
		
		return self._getVideoInfoForVideoIndex(videoIndex)[KEY_VIDEO_DOWNLOAD_FILENAME]
	
	def getVideoDownloadTimeForVideoIndex(self, videoIndex):
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if KEY_VIDEO_DOWNLOAD_TIME in videoInfoDic.keys():
			return videoInfoDic[KEY_VIDEO_DOWNLOAD_TIME]
		else:
			return None
	
	def getVideoDownloadTimeForVideoTitle(self, videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)
		
		return self._getVideoInfoForVideoIndex(videoIndex)[KEY_VIDEO_DOWNLOAD_TIME]
	
	def isExtractTimeFrameDataAvailableForVideoIndex(self, videoIndex):
		if KEY_VIDEO_TIME_FRAMES_IN_SECONDS in self.dic[videoIndex].keys():
			if KEY_TIMEFRAME_EXTRACT in self.dic[videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS]:
				return self.dic[videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS][KEY_TIMEFRAME_EXTRACT] != []
		
		return False
	
	def isSuppressTimeFrameDataAvailableForVideoIndex(self, videoIndex):
		if KEY_VIDEO_TIME_FRAMES_IN_SECONDS in self.dic[videoIndex].keys():
			if KEY_TIMEFRAME_SUPPRESS in self.dic[videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS]:
				return self.dic[videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS][KEY_TIMEFRAME_SUPPRESS] != []
		
		return False
	
	def _addTimeFrameDataForVideo(self, videoIndex):
		"""
		Protected method used internally only.
		
		:param videoIndex:
		:return:
		"""
		videoTimeFramesDic = {KEY_TIMEFRAME_EXTRACT: [], KEY_TIMEFRAME_SUPPRESS: []}
		
		self.dic[videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS] = videoTimeFramesDic
	
	def removeTimeFrameInSecondsDataIfExistForVideoIndex(self, videoIndex):
		videoIndex = str(videoIndex)
		
		if videoIndex not in self.dic.keys():
			return
		
		if KEY_VIDEO_TIME_FRAMES_IN_SECONDS not in self.dic[videoIndex].keys():
			return
		else:
			del self.dic[videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS]
	
	def addExtractStartEndSecondsListForVideoIndex(self, videoIndex, startEndSecondsList):
		videoIndex = str(videoIndex)
		
		if videoIndex not in self.dic.keys():
			self.dic[videoIndex] = {}
		
		if KEY_VIDEO_TIME_FRAMES_IN_SECONDS not in self.dic[videoIndex].keys():
			self._addTimeFrameDataForVideo(videoIndex)
		
		self.dic[videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS][KEY_TIMEFRAME_EXTRACT].append(startEndSecondsList)
	
	def addSuppressStartEndSecondsListForVideoIndex(self, videoIndex, startEndSecondsList):
		videoIndex = str(videoIndex)
		
		if videoIndex not in self.dic.keys():
			self.dic[videoIndex] = {}
		
		if KEY_VIDEO_TIME_FRAMES_IN_SECONDS not in self.dic[videoIndex].keys():
			self._addTimeFrameDataForVideo(videoIndex)
		
		self.dic[videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS][KEY_TIMEFRAME_SUPPRESS].append(startEndSecondsList)
	
	def getExtractStartEndSecondsListsForVideoIndex(self, videoIndex):
		videoIndex = str(videoIndex)
		
		if KEY_VIDEO_TIME_FRAMES_IN_SECONDS in self.dic[videoIndex].keys():
			return self.dic[videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS][KEY_TIMEFRAME_EXTRACT]
		else:
			return None
	
	def getSuppressStartEndSecondsListsForVideoIndex(self, videoIndex):
		videoIndex = str(videoIndex)
		
		if KEY_VIDEO_TIME_FRAMES_IN_SECONDS in self.dic[videoIndex].keys():
			return self.dic[videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS][KEY_TIMEFRAME_SUPPRESS]
		else:
			return None
	
	def addVideoInfoForVideoIndex(self,
	                              videoIndex,
	                              videoTitle,
	                              videoUrl,
	                              downloadedFileName):
		"""
		Creates the video info sub-dic for the video index if necessary.
		
		Then, adds to the sub-dic the video title, the video playlistUrl and the video downloaded
		file name.

		:param videoIndex:
		:param videoTitle:
		:param videoUrl:
		:param downloadedFileName:
		"""
		videoIndex = str(videoIndex)
		
		if videoIndex not in self.dic.keys():
			self.dic[videoIndex] = {}
		
		additionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_VIDEO_INFO_FILE)
		
		self.dic[videoIndex][KEY_VIDEO_TITLE] = videoTitle
		self.dic[videoIndex][KEY_VIDEO_URL] = videoUrl
		self.dic[videoIndex][KEY_VIDEO_DOWNLOAD_FILENAME] = downloadedFileName
		self.dic[videoIndex][KEY_VIDEO_DOWNLOAD_TIME] = additionTimeStr
	
	def _getVideoInfoForVideoIndex(self, videoIndex):
		"""
		Returns the video info dic associated to the passed key videoIndex.
		Protected method used internally only.

		:param videoIndex:
		:return: dictionary containing video information
		"""
		videoIndex = str(videoIndex)
		
		videoInfoDic = None
		
		try:
			videoInfoDic = self.dic[videoIndex]
		except KeyError:
			pass
		
		if videoInfoDic is None:
			videoInfoDic = {}
		
		return videoInfoDic
	
	def getVideoIndexForVideoTitle(self, videoTitle):
		for key in self.dic.keys():
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
		:param startEndHHMMSS_TimeFramesList: Example: ['0:23:45', '0:24:54']
		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		extractedFilesSubDic = {}
		
		if KEY_VIDEO_EXTRACTED_FILES not in videoInfoDic.keys():
			videoInfoDic[KEY_VIDEO_EXTRACTED_FILES] = extractedFilesSubDic
		else:
			extractedFilesSubDic = videoInfoDic[KEY_VIDEO_EXTRACTED_FILES]
		
		extractedFilesSubDic[timeFrameIndex] = {KEY_FILENAME: extractedFileName,
		                                        KEY_FILE_TIMEFRAME_HHMMSS: startEndHHMMSS_TimeFramesList}
	
	def getStartEndHHMMSS_TimeFrameForExtractedFileName(self, videoIndex, extractedFileName):
		"""
		Returns the time frame in HH:MM:SS format for the passed extracted file name
		extracted from the video videoIndex.

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
		audioDir = '/storage/emulated/0/Download/Audiobooks'
	else:
		audioDir = 'D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks'
	
	dvi = DownloadVideoInfoDic(audioDir, 'trial_vid_info')
	dvi.addVideoInfoForVideoIndex(1, 'Title_vid_1', 'https://youtube.com/watch?v=9iPvLx7gotk', 'Title_vid_1.mp4')
	dvi.addVideoInfoForVideoIndex(2, 'title_vid_2', 'https://youtube.com/watch?v=9iPvL8880999', 'Title_vid_2.mp4')
	dvi.addExtractStartEndSecondsListForVideoIndex(1, [34, 56])
	dvi.addExtractStartEndSecondsListForVideoIndex(1, [34, 65])
	dvi.addSuppressStartEndSecondsListForVideoIndex(1, [[340, 560], [840, 960]])
	dvi.addSuppressStartEndSecondsListForVideoIndex(3, [3400, 5600])
	dvi.addExtractedFileInfoForVideoIndexTimeFrameIndex(1, 1, 'title_1_1.mp3', ['0:2:3', '0:4:56'])
	dvi.addExtractedFileInfoForVideoIndexTimeFrameIndex(1, 2, 'title_1_2.mp3', ['0:20:3', '0:40:56'])
	dvi.addExtractedFileInfoForVideoIndexTimeFrameIndex(2, 1, 'title_2_1.mp3', ['0:2:3', '0:4:56'])
	dvi.addSuppressedFileInfoForVideoIndex(1, 'title_1_s.mp3', ['0:23:45-0:24:54', '1:03:45-1:24:54'],
	                                       ['0:0:0-0:23:45', '0:24:54-1:03:45', '1:24:54-1:55:12'])
	
	print(dvi)
	
	print(dvi.getSuppressStartEndSecondsListsForVideoIndex(1))
	print(dvi.getSuppressedFileNameForVideoIndex(1))
	print(dvi.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(1))
