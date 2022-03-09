class DownloadHistoryData():
	def __init__(self,
	             playlistName,
	             audioFileName,
	             audioFileDownladDate):
		"""
		
		:param playlistName: name of playlist containing the audio file
		:param audioFileName: name of the audio file
		:param audioFileDownladDate: string date in format yymmdd. Ex 220310
		"""
		self.playlistName = playlistName
		self.audioFileName = audioFileName
		self.audioFileDownladDate = audioFileDownladDate
		
	def __str__(self):
		return self.playlistName + ', ' + self.audioFileName + ', ' + self.audioFileDownladDate
	
	def getAudioFileNameShortened(self, length):
		return self.audioFileName[0:length]