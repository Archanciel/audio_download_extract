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
	def downloadSingleVideoForUrl(self,
	                              singleVideoUrl,
	                              originalVideoTitle,
	                              modifiedVideoTitle,
	                              targetAudioDir):
		"""
		Downloads in the passed targetAudioDir the single video referenced in the passed
		singleVideoUrl.

		:param singleVideoUrl:      single video url
		:param originalVideoTitle:  always passed
		:param modifiedVideoTitle:  None if the video title was not modified
		:param targetAudioDir:      path where the single video will be downloaded
		"""
		pass
