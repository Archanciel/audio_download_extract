class DownloadHistoryData():
	# playlistName, audioFileName, audioFileDownladDate_yymmdd
	def __init__(self,
	             playlistName,
	             title,
	             url):
		self.type = playlistName
		self.title = title
		self.url = url
		self.downloadDir = '' # not really useful for now
		
	def __str__(self):
		return self.type + ', ' + self.title + ', ' + self.url