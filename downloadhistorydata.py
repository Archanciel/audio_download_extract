DHD_TYPE_PLAYLIST = 1
DHD_TYPE_AUDIO_FILE = 2

class DownloadHistoryData():
	'''
	Class storing the data of the download history UI list. Its instances are placed
	in the 'data' value of the requestListRV.data dic list.
	'''
	def __init__(self,
	             type,
	             playlistName,
	             audioFileName='',
	             audioFileDownloadDate=''):
		"""
		:param type: DHD_TYPE_PLAYLIST or DHD_TYPE_AUDIO_FILE
		:param playlistName: name of playlist containing the audio file
		:param audioFileName: set for DHD_TYPE_AUDIO_FILE only. Name of the audio
							  file
		:param audioFileDownloadDate: set for DHD_TYPE_AUDIO_FILE only. String date
									 in format yymmdd. Ex 220310
		"""
		self.type = type
		self.playlistName = playlistName
		self.audioFileName = audioFileName
		self.audioFileDownloadDate = audioFileDownloadDate
		
	def __str__(self):
		return self.type + ', ' + self.playlistName + ', ' + self.audioFileName + ', ' + self.audioFileDownloadDate
	
	def getAudioFileNameShortened(self, length):
		return self.audioFileName[0:length]