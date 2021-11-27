from abc import ABCMeta, abstractmethod


class AudioDownloader(metaclass=ABCMeta):
	MAX_VIDEO_TITLES_DEFAULT_NUMBER = 4
	
	def __init__(self, audioController, audioDirRoot):
		"""
		Ctor.
		
		:param audioController:
		:param audioDirRoot: audio dir as defined in the GUI settings.
		"""
		self.audioController = audioController
		self.audioDirRoot = audioDirRoot
	
	@abstractmethod
	def downloadPlaylistVideosForUrl(self,
	                                 playlistUrl,
	                                 downloadVideoInfoDic,
	                                 isUploadDateAddedToPlaylistVideo,
	                                 isIndexAddedToPlaylistVideo):
		"""
		
		:param playlistUrl:
		:param downloadVideoInfoDic:
		:param isUploadDateAddedToPlaylistVideo if True, the name of the video
												audio files referenced in the
												playlist will be terminated by
												the video upload date.
		:param isIndexAddedToPlaylistVideo      if True, the name of the video
												audio files referenced in the
												playlist will be started by
												100 minus the video index.
		
		:return: downloadVideoInfoDic, accessError
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
