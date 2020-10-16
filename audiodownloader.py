from abc import ABCMeta, abstractmethod


class AudioDownloader(metaclass=ABCMeta):
	def __init__(self, guiOutput):
		self.guiOutput = guiOutput
		self.msgText = ''
	
	@abstractmethod
	def downloadVideosReferencedInPlaylist(self, playlistUrl):
		'''
	
		:param playlistUrl:
	
		:return: targetAudioDir, downloadedVideoInfoDic
		'''
		pass