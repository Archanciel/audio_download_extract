from os.path import sep

class UrlDownloadData():
	def __init__(self,
	             type,
	             title,
	             url,
	             downloadDir=''):
		"""
		:param type:    DownloadUrlInfoDic.URL_TYPE_PLAYLIST = 'playlist' or
						DownloadUrlInfoDic.URL_TYPE_SINGLE_VIDEO = 'video'

		:param title:
		:param url:
		:param downloadDir:
		"""
		self.type = type
		self.title = title
		self.url = url
		self.downloadDir = downloadDir
		
	def __str__(self):
		if self.downloadDir == '':
			return self.type + ', ' + self.title + ', ' + self.url
		else:
			return self.type + ', ' + self.downloadDir + sep + self.title + ', ' + self.url