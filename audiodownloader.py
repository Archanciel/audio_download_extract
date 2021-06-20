from abc import ABCMeta, abstractmethod


class AudioDownloader(metaclass=ABCMeta):
	def __init__(self, audioController, audioDir):
		self.audioController = audioController
		self.audioDir = audioDir
	
	@abstractmethod
	def downloadVideosReferencedInPlaylistForPlaylistUrl(self, playlistUrl, downloadVideoInfoDic):
		"""
		
		:param playlistUrl:
		:param downloadVideoInfoDic:
		:return:
		"""
		pass

	@abstractmethod
	def downloadSingleVideoForUrl(self, singleVideoUrl, videoTitle, targetAudioDir):
		"""
		
		:param singleVideoUrl:
		:param videoTitle:
		:param targetAudioDir:
		:return:
		"""
		pass
