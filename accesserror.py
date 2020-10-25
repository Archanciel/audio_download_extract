class AccessError:
	ERROR_TYPE_PLAYLIST_URL_INVALID = 1
	ERROR_TYPE_NO_INTERNET = 2
	ERROR_TYPE_NOT_PLAYLIST_URL = 3
	ERROR_TYPE_VIDEO_DOWNLOAD_FAILURE = 5
	ERROR_TYPE_PLAYLIST_DOWNLOAD_FAILURE = 6
	ERROR_TYPE_PLAYLIST_DOWNLOAD_DIRECTORY_NOT_EXIST = 7

	def __init__(self, errorType, errorMsg):
		self.errorType = errorType
		
		if errorType == AccessError.ERROR_TYPE_NOT_PLAYLIST_URL:
			if errorMsg == '':
				self.errorMsg = "the URL obtained from clipboard is empty.\nprogram will be closed."
			else:
				self.errorMsg = "the URL obtained from clipboard is not pointing to a playlist.\nwrong URL: {}\nprogram will be closed.".format(errorMsg)
		elif errorType == AccessError.ERROR_TYPE_NO_INTERNET:
			self.errorMsg = "{}\nprogram will be closed.".format(errorMsg)
		elif errorType == AccessError.ERROR_TYPE_VIDEO_DOWNLOAD_FAILURE:
			self.errorMsg = errorMsg + ' download failed.\ndownloading playlist interrupted.\nretry downloading the playlist to download the remaining videos !'
		elif errorType == AccessError.ERROR_TYPE_PLAYLIST_DOWNLOAD_FAILURE:
			self.errorMsg = errorMsg + ' download failed.\ndownloading playlist interrupted.\nretry downloading the playlist to download the remaining videos !'
		elif errorType == AccessError.ERROR_TYPE_PLAYLIST_DOWNLOAD_DIRECTORY_NOT_EXIST:
			self.errorMsg = errorMsg + '\ndownloading playlist interrupted.'

		else:
			if errorMsg == '':
				self.errorMsg = "the URL obtained from clipboard is empty.\nprogram will be closed."
			else:
				self.errorMsg = "the URL obtained from clipboard is not pointing to a playlist.\nerror msg: {}\nprogram will be closed.".format(errorMsg)
