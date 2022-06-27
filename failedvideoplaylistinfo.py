class FailedVideoPlaylistInfo:
	def __init__(self,
	             playlistInfoDic,
	             failedVideoIndexLst):
		"""
		:param playlistInfoDic:     playlistInfoDic containing at least one failed video
		:param failedVideoIndexLst: list of failed video indexes contained in the
									playlistInfoDic
		"""
		self.playlistInfoDic = playlistInfoDic
		self.failedVideoIndexLst = failedVideoIndexLst
	