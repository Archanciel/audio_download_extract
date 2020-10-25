from abc import ABCMeta, abstractmethod


class AudioDownloader(metaclass=ABCMeta):
	def __init__(self, audioController):
		self.audioController = audioController
	
	@abstractmethod
	def downloadVideosReferencedInPlaylistForPlaylistUrl(self, playlistUrl):
		'''
	
		:param playlistUrl:
	
		:return: targetAudioDir, downloadVideoInfoDic
		'''
		pass
