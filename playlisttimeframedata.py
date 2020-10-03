class PlaylistTimeFrameData:
	def __init__(self):
		self.videoTimeFramesDic = {}
		
	def addTimeFrameDataForVideo(self, videoIndex):
		videoTimeFramesAllList = []
		videoTimeFramesExtractList = []
		videoTimeFramesSuppressList = []
		videoTimeFramesAllList.append(videoTimeFramesExtractList)
		videoTimeFramesAllList.append(videoTimeFramesSuppressList)			
		self.videoTimeFramesDic[videoIndex] = videoTimeFramesAllList
		
	def addExtractStartEndSecondsList(self, videoIndex, startEndSecondsList):
		if not videoIndex in self.videoTimeFramesDic.keys():
			self.addTimeFrameDataForVideo(videoIndex)
			
		self.videoTimeFramesDic[videoIndex][0].append(startEndSecondsList)
		
	def addSuppressStartEndSecondsList(self, videoIndex, startEndSecondsList):
		if not videoIndex in self.videoTimeFramesDic.keys():
			self.addTimeFrameDataForVideo(videoIndex)
		
		self.videoTimeFramesDic[videoIndex][1].append(startEndSecondsList)
		
	def getExtractStartEndSecondsLists(self, videoIndex):
		return self.videoTimeFramesDic[videoIndex][0]
		
	def getSuppressStartEndSecondsLists(self, videoIndex):
		return self.videoTimeFramesDic[videoIndex][1]