class PlaylistVideoIndexInfo:
	def __init__(self,
	             playlistInfoDic,
	             videoIndexLst):
		"""
		:param playlistInfoDic:     playlistInfoDic containing at least one failed video
		:param videoIndexLst:       list of failed video indexes or re-downloaded on PC
									video indexes contained in the playlistInfoDic
		"""
		self.playlistInfoDic = playlistInfoDic
		self.videoIndexLst = videoIndexLst
	