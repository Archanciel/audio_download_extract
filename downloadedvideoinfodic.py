import json
from datetime import datetime

from constants import *

class DownloadedVideoInfoDic:
	wasDicUpdated = False
	cachedRateAccessNumber = 0

	def __init__(self, downloadDir, playlistName):
		self.downloadDir = downloadDir
		self.playlistName = playlistName
		self.dic = {}
		
	def __str__(self):
		return 	json.dumps(self.dic, sort_keys=False, indent=4)

	def loadDic(self):
		infoDicFilePathName = self.getInfoDicFilePathName()
		if os.path.isfile(infoDicFilePathName):
			with open(infoDicFilePathName, 'r') as f:
				self.dic = json.load(f)
	
	def saveDic(self):
		with open(self.getInfoDicFilePathName(), 'w') as f:
			json.dump(self.dic,
			          f,
			          indent=4,
			          sort_keys=True)
	
	def getInfoDicFilePathName(self):
		return self.downloadDir + DIR_SEP + self.playlistName + '.txt'
	
	def getVideoIndexes(self):
		'''
		Returns a list of video indexes as string.
		
		:return: example: ['1', '2']
		'''
		return list(self.dic.keys())
	
	def getVideoTitleForVideoIndex(self, videoIndex):
		return self._getVideoInfoForVideoIndex(videoIndex)['title']

	def getVideoUrlForVideoIndex(self, videoIndex):
		return self._getVideoInfoForVideoIndex(videoIndex)['url']
	
	def getVideoUrlForVideoTitle(self, videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)
		
		return self._getVideoInfoForVideoIndex(videoIndex)['url']
	
	def getVideoFileNameForVideoIndex(self, videoIndex):
		return self._getVideoInfoForVideoIndex(videoIndex)['downloadedFileName']
	
	def getVideoFileNameForVideoTitle(self, videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)
		
		return self._getVideoInfoForVideoIndex(videoIndex)['downloadedFileName']
	
	def getVideoDownloadTimeForVideoIndex(self, videoIndex):
		return self._getVideoInfoForVideoIndex(videoIndex)['downloadTime']

	def getVideoDownloadTimeForVideoTitle(self, videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)
		
		return self._getVideoInfoForVideoIndex(videoIndex)['downloadTime']

	def isExtractTimeFrameDataAvailableForVideoIndex(self, videoIndex):
		if 'startEndTimeFramesInSeconds' in self.dic[videoIndex].keys():
			return 'extract' in self.dic[videoIndex]['startEndTimeFramesInSeconds']
		
		return False
	
	def isSuppressTimeFrameDataAvailableForVideoIndex(self, videoIndex):
		if 'startEndTimeFramesInSeconds' in self.dic[videoIndex].keys():
			return 'suppress' in self.dic[videoIndex]['startEndTimeFramesInSeconds']
		
		return False
	
	def _addTimeFrameDataForVideo(self, videoIndex):
		'''
		Protected method used internally only.
		
		:param videoIndex:
		:return:
		'''
		videoTimeFramesDic = {'extract': [], 'suppress': []}
		
		self.dic[videoIndex]['startEndTimeFramesInSeconds'] = videoTimeFramesDic
	
	def addExtractStartEndSecondsListForVideoIndex(self, videoIndex, startEndSecondsList):
		videoIndex = str(videoIndex)
		
		if not videoIndex in self.dic.keys():
			self.dic[videoIndex] = {}

		if not 'startEndTimeFramesInSeconds' in self.dic[videoIndex].keys():
			self._addTimeFrameDataForVideo(videoIndex)
		
		self.dic[videoIndex]['startEndTimeFramesInSeconds']['extract'].append(startEndSecondsList)
	
	def addSuppressStartEndSecondsListForVideoIndex(self, videoIndex, startEndSecondsList):
		videoIndex = str(videoIndex)

		if not videoIndex in self.dic.keys():
			self.dic[videoIndex] = {}
		
		if not 'startEndTimeFramesInSeconds' in self.dic[videoIndex].keys():
			self._addTimeFrameDataForVideo(videoIndex)
		
		self.dic[videoIndex]['startEndTimeFramesInSeconds']['suppress'] = startEndSecondsList
	
	def getExtractStartEndSecondsListsForVideoIndex(self, videoIndex):
		videoIndex = str(videoIndex)

		if 'startEndTimeFramesInSeconds' in self.dic[videoIndex].keys():
			return self.dic[videoIndex]['startEndTimeFramesInSeconds']['extract']
		else:
			return None
	
	def getSuppressStartEndSecondsListsForVideoIndex(self, videoIndex):
		videoIndex = str(videoIndex)

		if 'startEndTimeFramesInSeconds' in self.dic[videoIndex].keys():
			return self.dic[videoIndex]['startEndTimeFramesInSeconds']['suppress']
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
		videoIndex = str(videoIndex)

		if not videoIndex in self.dic.keys():
			self.dic[videoIndex] = {}
			
		additionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_VIDEO_INFO_FILE)

		self.dic[videoIndex]['title'] = videoTitle
		self.dic[videoIndex]['url'] = videoUrl
		self.dic[videoIndex]['downloadedFileName'] = downloadedFileName
		self.dic[videoIndex]['downloadTime'] = additionTimeStr
	
	def _getVideoInfoForVideoIndex(self, videoIndex):
		'''
		Returns the video info dic associated to the passedkey videoIndex.
		Protected method used internally only.

		:param videoIndex:
		:return: dictionary containing video information
		'''
		videoIndex = str(videoIndex)
		
		videoInfoDic = None
		
		try:
			videoInfoDic = self.dic[videoIndex]
		except KeyError:
			pass
		
		if videoInfoDic == None:
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
		:param startEndHHMMSS_TimeFramesList. Example: ['0:23:45', '0:24:54']
		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		extractedFilesSubDic = {}
		
		if 'extracted files' not in videoInfoDic.keys():
			videoInfoDic['extracted files'] = extractedFilesSubDic
		else:
			extractedFilesSubDic = videoInfoDic['extracted files']
			
		extractedFilesSubDic[timeFrameIndex] = {'fileName': extractedFileName,
		                                     'startEndTimeFrameHHMMSS': startEndHHMMSS_TimeFramesList}

	def getStartEndHHMMSS_TimeFrameForExtractedFileName(self, videoIndex, extractedFileName):
		"""
		Returns the time frame in HH:MM:SS format for the passed extracted file name
		extracted from the video videoIndex.
		
		:param videoIndex:
		:param extractedFileName:

		:return: startEndHHMMSS time frame list. Example: ['0:23:45', '0:24:54']
		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)

		if 'extracted files' not in videoInfoDic.keys():
			pass
		else:
			extractedFilesSubDic = videoInfoDic['extracted files']
			
			for key in extractedFilesSubDic.keys():
				if extractedFileName == extractedFilesSubDic[key]['fileName']:
					return extractedFilesSubDic[key]['startEndTimeFrameHHMMSS']
		
		return None
	
	def addSuppressedFileInfoForVideoIndex(self,
	                                       videoIndex,
	                                       suppressedFileName,
	                                       startEndHHMMSS_TimeFramesList):
		"""
		Creates the extracted files info dic if necessary.

		Then, adds to the sub-dic the extracted file name and its corresponding
		time frame in HH:MM:SS format.

		:param videoIndex:
		:param suppressedFileName:
		:param startEndHHMMSS_TimeFramesList list os suppressed time frames.
											 Example: ['0:23:45-0:24:54', '1:03:45-1:24:54']
		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		suppressedFileSubDic = {}
		
		if 'suppressed file' not in videoInfoDic.keys():
			videoInfoDic['suppressed file'] = suppressedFileSubDic
		else:
			suppressedFileSubDic = videoInfoDic['suppressed file']
		
		suppressedFileSubDic['fileName'] = suppressedFileName
		suppressedFileSubDic['startEndTimeSuppressedFramesHHMMSS'] = startEndHHMMSS_TimeFramesList
	
	def getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(self, videoIndex):
		"""
		Returns the suppressed time frames in HH:MM:SS format for the passed video
		index.

		:param videoIndex:

		:return: startEndHHMMSS time frame list. Example: ['0:23:45', '0:24:54']
		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if 'suppressed file' not in videoInfoDic.keys():
			pass
		else:
			return videoInfoDic['suppressed file']['startEndTimeSuppressedFramesHHMMSS']
		
		return None
	
	def getSuppressedFileNameForVideoIndex(self, videoIndex):
		"""
		Returns the suppressed time frames in HH:MM:SS format for the passed video
		index.

		:param videoIndex:

		:return: suppressed file name
		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if 'suppressed file' not in videoInfoDic.keys():
			pass
		else:
			return videoInfoDic['suppressed file']['fileName']
		
		return None


if __name__ == "__main__":
	if os.name == 'posix':
		audioDir = '/storage/emulated/0/Download/Audiobooks'
	else:
		audioDir = 'D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks'
		
	dvi = DownloadedVideoInfoDic(audioDir, 'essai_vid_info')
	dvi.addVideoInfoForVideoIndex(1, 'Title_vid_1', 'https://youtube.com/watch?v=9iPvLx7gotk', 'Title_vid_1.mp4')
	dvi.addVideoInfoForVideoIndex(2, 'title_vid_2', 'https://youtube.com/watch?v=9iPvL8880999', 'Title_vid_2.mp4')
	dvi.addExtractStartEndSecondsListForVideoIndex(1, [34, 56])
	dvi.addExtractStartEndSecondsListForVideoIndex(1, [34, 65])
	dvi.addSuppressStartEndSecondsListForVideoIndex(1, [[340, 560], [840, 960]])
	dvi.addSuppressStartEndSecondsListForVideoIndex(3, [3400, 5600])
	dvi.addExtractedFileInfoForVideoIndexTimeFrameIndex(1, 1, 'title_1_1.mp3', ['0:2:3', '0:4:56'])
	dvi.addExtractedFileInfoForVideoIndexTimeFrameIndex(1, 2, 'title_1_2.mp3', ['0:20:3', '0:40:56'])
	dvi.addExtractedFileInfoForVideoIndexTimeFrameIndex(2, 1, 'title_2_1.mp3', ['0:2:3', '0:4:56'])
	dvi.addSuppressedFileInfoForVideoIndex(1, 'title_1_s.mp3', ['0:23:45-0:24:54', '1:03:45-1:24:54'])

	print(dvi)
	
	print(dvi.getSuppressStartEndSecondsListsForVideoIndex(1))
	print(dvi.getSuppressedFileNameForVideoIndex(1))
	print(dvi.getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(1))
