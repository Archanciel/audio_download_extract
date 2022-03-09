class UrlDownloadData():
	def __init__(self,
	             type,
	             title,
	             url):
		self.type = type
		self.title = title
		self.url = url
		self.downloadDir = '' # not really useful for now
		
	def __str__(self):
		return self.type + ', ' + self.title + ', ' + self.url