from abc import ABCMeta, abstractmethod


class AudioDownloader(metaclass=ABCMeta):
	def __init__(self, guiOutput):
		self.guiOutput = guiOutput
		self.msgText = ''
	
	@abstractmethod
	def downloadVideosReferencedInPlaylistForPlaylistUrl(self, playlistUrl):
		'''
	
		:param playlistUrl:
	
		:return: targetAudioDir, downloadVideoInfoDic
		'''
		pass
	
	@abstractmethod
	def downloadVideosReferencedInPlaylist(self, playlistObject):
		'''

		:param playlistUrl:

		:return: targetAudioDir, downloadVideoInfoDic
		'''
		pass