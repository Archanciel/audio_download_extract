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
	
	def addTimeFrameDataForVideo(self, videoIndex):
		videoTimeFramesDic = {'extract': [], 'suppress': []}
		
		self.dic[videoIndex]['timeFrames'] = videoTimeFramesDic
	
	def addExtractStartEndSecondsList(self, videoIndex, startEndSecondsList):
		videoIndex = str(videoIndex)
		
		if not videoIndex in self.dic.keys():
			self.dic[videoIndex] = {}

		if not 'timeFrames' in self.dic[videoIndex].keys():
			self.addTimeFrameDataForVideo(videoIndex)
		
		self.dic[videoIndex]['timeFrames']['extract'].append(startEndSecondsList)
	
	def addSuppressStartEndSecondsList(self, videoIndex, startEndSecondsList):
		videoIndex = str(videoIndex)

		if not videoIndex in self.dic.keys():
			self.dic[videoIndex] = {}
		
		if not 'timeFrames' in self.dic[videoIndex].keys():
			self.addTimeFrameDataForVideo(videoIndex)
		
		self.dic[videoIndex]['timeFrames']['suppress'].append(startEndSecondsList)
	
	def getExtractStartEndSecondsLists(self, videoIndex):
		videoIndex = str(videoIndex)

		return self.dic[videoIndex]['timeFrames']['extract']
	
	def getSuppressStartEndSecondsLists(self, videoIndex):
		videoIndex = str(videoIndex)

		return self.dic[videoIndex]['timeFrames']['suppress']
	
	def addVideoInfo(self, videoIndex, videoTitle, videoUrl):
		videoIndex = str(videoIndex)

		if not videoIndex in self.dic.keys():
			self.dic[videoIndex] = {}
			
		additionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_VIDEO_INFO_FILE)

		self.dic[videoIndex]['title'] = videoTitle
		self.dic[videoIndex]['url'] = videoUrl
		self.dic[videoIndex]['downloadTime'] = additionTimeStr
	
	def getVideoInfoForVideoIndex(self, videoIndex):
		videoIndex = str(videoIndex)
		
		videoInfo = None
		
		try:
			videoInfo = self.dic[videoIndex]
		except KeyError:
			pass
		
		return videoInfo
	
	def getVideoInfoForVideoTitle(self, videoTitle):
		for key in self.dic.keys():
			videoInfo = self.dic[key]
			if videoInfo['title'] == videoTitle:
				return videoInfo
		
		return None


if __name__ == "__main__":
	dvi = DownloadedVideoInfoDic('D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks', 'essai_vid_info')
	dvi.addVideoInfo(1, 'Title_vid_1', 'https://youtube.com/watch?v=9iPvLx7gotk')
	dvi.addVideoInfo(2, 'title_vid_2', 'https://youtube.com/watch?v=9iPvL8880999')
	print('vidéo 1 info ', dvi.getVideoInfoForVideoIndex(1))
	print('vidéo 2 info ', dvi.getVideoInfoForVideoIndex(2))
	dvi.addExtractStartEndSecondsList(1, [34, 56])
	dvi.addExtractStartEndSecondsList(1, [34, 65])
	dvi.addSuppressStartEndSecondsList(1, [340, 560])
	dvi.addSuppressStartEndSecondsList(3, [3400, 5600])
	print('vidéo 3 info ', dvi.getVideoInfoForVideoIndex(3))
	print(dvi.getExtractStartEndSecondsLists(1))
	print(dvi.getSuppressStartEndSecondsLists(1))
	print('vidéo 1 info                           ', dvi.getVideoInfoForVideoIndex(1))
	print('vidéo 2 info                           ', dvi.getVideoInfoForVideoIndex(2))
	print('vidéo info for video title Title_vid_1 ', dvi.getVideoInfoForVideoTitle('Title_vid_1'))
	dvi.saveDic()
