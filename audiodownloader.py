from abc import ABCMeta, abstractmethod


class AudioDownloader(metaclass=ABCMeta):
	def __init__(self, audioController, audioDirRoot):
		"""
		Ctor.
		
		:param audioController:
		:param audioDirRoot: audio dir as defined in the GUI settings.
		"""
		self.audioController = audioController
		self.audioDirRoot = audioDirRoot
	
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
