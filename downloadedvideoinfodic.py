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

	def isTimeFrameDataAvailableForVideoIndex(self, videoIndex):
		return 'startEndTimeFramesInSeconds' in self.dic[videoIndex].keys()
		
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
		
		self.dic[videoIndex]['startEndTimeFramesInSeconds']['suppress'].append(startEndSecondsList)
	
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
	
	def addExtractedFilePathNameForVideoIndex(self,
	                                          videoIndex,
	                                          timeFrameIndex,
	                                          startEndSecondsList,
	                                          extractedFileName):
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		extractedFilesDic = {}
		
		if 'extracted files' not in videoInfoDic.keys():
			videoInfoDic['extracted files'] = extractedFilesDic
		else:
			extractedFilesDic = videoInfoDic['extracted files']
			
		extractedFilesDic[timeFrameIndex] = {'fileName': extractedFileName,
		                                     'startEndTimeFrameHHMMSS': startEndSecondsList}

	def getStartEndTimeFrame(self, videoIndex, extractedFileName):
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)

		if 'extracted files' not in videoInfoDic.keys():
			pass
		else:
			extractedFilesDic = videoInfoDic['extracted files']
			
			for key in extractedFilesDic.keys():
				if extractedFileName == extractedFilesDic[key]['fileName']:
					return extractedFilesDic[key]['startEndTimeFrameHHMMSS']
		
		return None

if __name__ == "__main__":
	dvi = DownloadedVideoInfoDic('D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks', 'essai_vid_info')
	dvi.addVideoInfoForVideoIndex(1, 'Title_vid_1', 'https://youtube.com/watch?v=9iPvLx7gotk')
	dvi.addVideoInfoForVideoIndex(2, 'title_vid_2', 'https://youtube.com/watch?v=9iPvL8880999')
	print('vidéo 1 info ', dvi._getVideoInfoForVideoIndex(1))
	print('vidéo 2 info ', dvi._getVideoInfoForVideoIndex(2))
	dvi.addExtractStartEndSecondsListForVideoIndex(1, [34, 56])
	dvi.addExtractStartEndSecondsListForVideoIndex(1, [34, 65])
	dvi.addSuppressStartEndSecondsListForVideoIndex(1, [340, 560])
	dvi.addSuppressStartEndSecondsListForVideoIndex(3, [3400, 5600])
	print('vidéo 3 info ', dvi._getVideoInfoForVideoIndex(3))
	print(dvi.getExtractStartEndSecondsListsForVideoIndex(1))
	print(dvi.getSuppressStartEndSecondsListsForVideoIndex(1))
	print('vidéo 1 info                           ', dvi._getVideoInfoForVideoIndex(1))
	print('vidéo 2 info                           ', dvi._getVideoInfoForVideoIndex(2))
	dvi.saveDic()
