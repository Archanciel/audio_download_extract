class DownloadHistoryData():
	def __init__(self,
	             playlistName,
	             audioFileName,
	             audioFileDownladDate):
		self.playlistName = playlistName
		self.audioFileName = audioFileName
		self.audioFileDownladDate = audioFileDownladDate
		
	def __str__(self):
		return self.playlistName + ', ' + self.audioFileName + ', ' + self.audioFileDownladDate