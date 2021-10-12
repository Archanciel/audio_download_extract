class AccessError:
	ERROR_TYPE_PLAYLIST_URL_INVALID = 1
	ERROR_TYPE_NO_INTERNET = 2
	ERROR_TYPE_NOT_PLAYLIST_URL = 3
	ERROR_TYPE_VIDEO_DOWNLOAD_FAILURE = 5
	ERROR_TYPE_PLAYLIST_DOWNLOAD_FAILURE = 6
	ERROR_TYPE_PLAYLIST_DOWNLOAD_DIRECTORY_NOT_EXIST = 7
	ERROR_TYPE_PLAYLIST_TIME_FRAME_SYNTAX_ERROR = 8
	ERROR_TYPE_SINGLE_VIDEO_URL_PROBLEM = 9
	ERROR_TYPE_LOADING_DOWNLOAD_DIC = 10

	def __init__(self, errorType, errorMsg):
		self.errorType = errorType
		
		if errorType == AccessError.ERROR_TYPE_NOT_PLAYLIST_URL:
			if errorMsg == '':
				self.errorMsg = "the URL obtained from clipboard is empty.\nnothing to download."
			else:
				self.errorMsg = "the URL obtained from clipboard is not pointing to a playlist.\nwrong URL: {}\nnothing to download.".format(errorMsg)
		elif errorType == AccessError.ERROR_TYPE_NO_INTERNET:
			self.errorMsg = "{}\nprogram will be closed.".format(errorMsg)
		elif errorType == AccessError.ERROR_TYPE_VIDEO_DOWNLOAD_FAILURE:
			self.errorMsg = errorMsg + ' download failed.\ndownloading playlist interrupted.\nretry downloading the playlist to download the remaining videos !'
		elif errorType == AccessError.ERROR_TYPE_PLAYLIST_DOWNLOAD_FAILURE:
			self.errorMsg = errorMsg + ' download failed.\ndownloading playlist interrupted.\nretry downloading the playlist to download the remaining videos !'
		elif errorType == AccessError.ERROR_TYPE_PLAYLIST_DOWNLOAD_DIRECTORY_NOT_EXIST:
			self.errorMsg = errorMsg + '\ndownloading playlist interrupted.'
		elif errorType == AccessError.ERROR_TYPE_PLAYLIST_TIME_FRAME_SYNTAX_ERROR:
			self.errorMsg = errorMsg + '\ndownloading playlist interrupted.'
		elif errorType == AccessError.ERROR_TYPE_SINGLE_VIDEO_URL_PROBLEM:
			self.errorMsg = "trying to get the video title for the URL obtained from clipboard did not succeed.\n{}\nnothing to download.".format(errorMsg)
		elif errorType == AccessError.ERROR_TYPE_LOADING_DOWNLOAD_DIC:
			self.errorMsg = "trying to load the existing download dictionary failed.\n{}\ndownload interrupted.".format(
				errorMsg)
		else:
			if errorMsg == '':
				self.errorMsg = "the URL obtained from clipboard is empty.\nnothing to download."
			else:
				self.errorMsg = "the URL obtained from clipboard is not pointing to a playlist.\nerror msg: {}\nnothing to download.".format(errorMsg)
