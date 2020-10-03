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
		
		infoDicFilePathName = self.getInfoDicFilePathName()
		
		if os.path.isfile(infoDicFilePathName):
			with open(infoDicFilePathName, 'r') as f:
				self.dic = json.load(f)
	
	def getVideoInfo(self, videoTitle):
		videoInfo = None

		try:
			videoInfo = self.dic[videoTitle]
		except KeyError:
			pass

		return videoInfo

	def addVideoInfo(self, videoTitle, videoUrl):
		additionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_VIDEO_INFO_FILE)

		self.dic[videoTitle] = [videoUrl, additionTimeStr]
		
	def saveDic(self):
		with open(self.getInfoDicFilePathName(), 'w') as f:
			json.dump(self.dic,
			          f,
			          indent=4,
			          sort_keys=True)
	
	def getInfoDicFilePathName(self):
		return self.downloadDir + DIR_SEP + self.playlistName + '.txt'


if __name__ == "__main__":
	dvi = DownloadedVideoInfoDic('D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks', 'essai_vid_info')
	dvi.addVideoInfo('title 1', 'https://youtube.com/watch?v=9iPvLx7gotk')
	dvi.addVideoInfo('title 2', 'https://youtube.com/watch?v=9iPvL8880999')
	print(dvi.getVideoInfo('title 1'))
	print(dvi.getVideoInfo('title 2'))
	dvi.saveDic()
