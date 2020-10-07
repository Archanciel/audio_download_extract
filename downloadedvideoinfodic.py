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
		return self.dic.keys()
	
	def getVideoTitleForVideoIndex(self, videoIndex):
		return self._getVideoInfoForVideoIndex(videoIndex)['title']

	def getVideoUrlForVideoIndex(self, videoIndex):
		return self._getVideoInfoForVideoIndex(videoIndex)['url']
	
	def getVideoUrlForVideoTitle(self, videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)
		
		return self._getVideoInfoForVideoIndex(videoIndex)['url']
	
	def getVideoFileNameForVideoIndex(self, videoIndex):
		return self._getVideoInfoForVideoIndex(videoIndex)['downloadedVideoFileName']
	
	def getVideoFileNameForVideoTitle(self, videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)
		
		return self._getVideoInfoForVideoIndex(videoIndex)['downloadedVideoFileName']
	
	def getVideoDownloadTimeForVideoIndex(self, videoIndex):
		return self._getVideoInfoForVideoIndex(videoIndex)['downloadTime']

	def getVideoDownloadTimeForVideoTitle(self, videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)
		
		return self._getVideoInfoForVideoIndex(videoIndex)['downloadTime']

	def isTimeFrameDataAvailableForVideoIndex(self, videoIndex):
		return 'timeFrames' in self.dic[videoIndex].keys()
		
	def _addTimeFrameDataForVideo(self, videoIndex):
		'''
		Protected method used internally only.
		
		:param videoIndex:
		:return:
		'''
		videoTimeFramesDic = {'extract': [], 'suppress': []}
		
		self.dic[videoIndex]['timeFrames'] = videoTimeFramesDic
	
	def addExtractStartEndSecondsListForVideoIndex(self, videoIndex, startEndSecondsList):
		videoIndex = str(videoIndex)
		
		if not videoIndex in self.dic.keys():
			self.dic[videoIndex] = {}

		if not 'timeFrames' in self.dic[videoIndex].keys():
			self._addTimeFrameDataForVideo(videoIndex)
		
		self.dic[videoIndex]['timeFrames']['extract'].append(startEndSecondsList)
	
	def addSuppressStartEndSecondsListForVideoIndex(self, videoIndex, startEndSecondsList):
		videoIndex = str(videoIndex)

		if not videoIndex in self.dic.keys():
			self.dic[videoIndex] = {}
		
		if not 'timeFrames' in self.dic[videoIndex].keys():
			self._addTimeFrameDataForVideo(videoIndex)
		
		self.dic[videoIndex]['timeFrames']['suppress'].append(startEndSecondsList)
	
	def getExtractStartEndSecondsListsForVideoIndex(self, videoIndex):
		videoIndex = str(videoIndex)

		if 'timeFrames' in self.dic[videoIndex].keys():
			return self.dic[videoIndex]['timeFrames']['extract']
		else:
			return None
	
	def getSuppressStartEndSecondsListsForVideoIndex(self, videoIndex):
		videoIndex = str(videoIndex)

		if 'timeFrames' in self.dic[videoIndex].keys():
			return self.dic[videoIndex]['timeFrames']['suppress']
		else:
			return None

	def addVideoInfoForVideoIndex(self, videoIndex, videoTitle, videoUrl, downloadedVideoFileName):
		videoIndex = str(videoIndex)

		if not videoIndex in self.dic.keys():
			self.dic[videoIndex] = {}
			
		additionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_VIDEO_INFO_FILE)

		self.dic[videoIndex]['title'] = videoTitle
		self.dic[videoIndex]['url'] = videoUrl
		self.dic[videoIndex]['downloadedVideoFileName'] = downloadedVideoFileName
		self.dic[videoIndex]['downloadTime'] = additionTimeStr
	
	def _getVideoInfoForVideoIndex(self, videoIndex):
		videoIndex = str(videoIndex)
		
		videoInfo = None
		
		try:
			videoInfo = self.dic[videoIndex]
		except KeyError:
			pass
		
		return videoInfo
	
	def getVideoIndexForVideoTitle(self, videoTitle):
		for key in self.dic.keys():
			if self.getVideoTitleForVideoIndex(key) == videoTitle:
				return key
		
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
