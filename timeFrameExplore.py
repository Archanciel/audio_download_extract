import re

class TimeFrameParser:
	def splitPlayListTitle(self, playlistTitle):
		playlistNamePattern = r'([a-zaA-Z_]+) ([\(se\d:\- \)]*)'
		
		match = re.match(playlistNamePattern, playlistTitle)
		playlistName = match.group(1)
		videoTimeFramesInfo = match.group(2)
		
		videoTimeFramesDic = self.extractTimeInfo(videoTimeFramesInfo)
		
		return videoTimeFramesDic


	def extractTimeInfo(self, playlistName):
		videoTimeFramesPattern = r'(\([se\d:\- ]*\) ?)'
		startEndTimeFramePattern = r'([\dsSeE:-]*)'
		videoTimeFramesDic = {}
		videoIndex = 1
		
		for videoTimeFrameGroup in re.finditer(videoTimeFramesPattern, playlistName):			
			for startEndTimeFrame in videoTimeFrameGroup.groups():
				videoTimeFramesList = []
				videoTimeFramesDic[videoIndex] = videoTimeFramesList
				print('video {} timeFrames'.format(videoIndex), startEndTimeFrame)
				for startEndTimeFrame in re.finditer(startEndTimeFramePattern, startEndTimeFrame):
					for subGro in startEndTimeFrame.groups():
						videoTimeFramesList.append(subGro)
						print(subGro)
			videoIndex += 1
			
		return videoTimeFramesDic			

playlistTitle = 'The_playlist (s01:05:52-01:07:23 e01:15:52-01:17:23 e01:15:52-01:17:23) (s1:05:52-1:07:23)'

tp = TimeFrameParser()
videoTimeFramesDic = tp.splitPlayListTitle(playlistTitle)
print(videoTimeFramesDic)