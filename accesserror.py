class AccessError:
	ERROR_TYPE_PLAYLIST_URL_INVALID = 1
	ERROR_TYPE_NO_INTERNET = 2
	ERROR_TYPE_NOT_PLAYLIST_URL = 3
	ERROR_TYPE_CLIPBOARD_EMPTY = 4
	ERROR_TYPE_VIDEO_DOWNLOAD_FAILURE = 5
	ERROR_TYPE_PLAYLIST_DOWNLOAD_FAILURE = 6

	def __init__(self, errorType, errorMsg):
		self.errorType = errorType
		
		if errorType == AccessError.ERROR_TYPE_NOT_PLAYLIST_URL:
			if errorMsg == '':
				self.errorMsg = "The URL obtained from clipboard is empty.\nProgram will be closed."
			else:
				self.errorMsg = "The URL obtained from clipboard is not pointing to a playlist.\nWrong URL: {}\nProgram will be closed.".format(errorMsg)
		elif errorType == AccessError.ERROR_TYPE_NO_INTERNET:
			self.errorMsg = "{}\nProgram will be closed.".format(errorMsg)
		elif errorType == AccessError.ERROR_TYPE_CLIPBOARD_EMPTY:
			self.errorMsg = "The clipboard is empty (not containing a playlist url).\nProgram will be closed."
		elif errorType == AccessError.ERROR_TYPE_VIDEO_DOWNLOAD_FAILURE:
			self.errorMsg = errorMsg + ' download failed.\nDownloading playlist interrupted.\nRetry downloading the playlist to download the remaining videos !'
		elif errorType == AccessError.ERROR_TYPE_PLAYLIST_DOWNLOAD_FAILURE:
			self.errorMsg = errorMsg + ' download failed.\nDownloading playlist interrupted.\nRetry downloading the playlist to download the remaining videos !'
		else:
			if errorMsg == '':
				self.errorMsg = "The URL obtained from clipboard is empty.\nProgram will be closed."
			else:
				self.errorMsg = "The URL obtained from clipboard is not pointing to a playlist.\nError msg: {}\nProgram will be closed.".format(errorMsg)
