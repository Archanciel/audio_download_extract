import os
from tkinter import Tk

from constants import *
from configmanager import ConfigManager
from requester import Requester
from downloadedvideoinfodic import DownloadedVideoInfoDic
from guioutput import GuiOutput
from youtubeaudiodownloader import YoutubeAudioDownloader
from audioextractor import AudioExtractor
from accesserror import AccessError

class AudioController:
	def __init__(self, guiOutputStub=None):
		"""
		
		:param guiOutputStub: used for unit testing only !
		"""

		if os.name == 'posix':
			configFilePathName = '/sdcard/audiodownload.ini'
		else:
			configFilePathName = 'c:\\temp\\audiodownload.ini'

		self.configMgr = ConfigManager(configFilePathName)
		self.requester = Requester(self.configMgr)
		
		# Tk must be instanciated in AudioController: class, not in
		# GuyOutput class !
		if guiOutputStub is None:
			# we are not unit testing !
			self.guiOutput = GuiOutput(Tk())
		else:
			self.guiOutput = guiOutputStub
		
	def downloadPlaylistAudio(self):
		'''
		Example of playlist title:
		playlist_title (s01:05:52-01:07:23 e01:15:52-E E01:35:52-01:37:23 S01:25:52-e) (s01:05:52-01:07:23 e01:15:52-e S01:25:52-e E01:35:52-01:37:23)
		-e or -E means "to end" !

		:return:
		'''
		# obtaining the playlist url from the clipboard
		playlistUrl = self.guiOutput.getPlaylistUrlFromClipboard()
		
		if playlistUrl == None:
			accessError = AccessError(AccessError.ERROR_TYPE_CLIPBOARD_EMPTY, playlistUrl)
			self.guiOutput.displayError(accessError.errorMsg)

			# returning accessError is useful for unit testing only,
			# otherwise return alone is sufficient !
			return accessError
		
		# downloading the audio track of the videos referenced in the playlist
		audioDownloader = YoutubeAudioDownloader(self.guiOutput)
		targetAudioDir, downloadedVideoInfoDictionary, accessError = audioDownloader.downloadVideosReferencedInPlaylist(playlistUrl)

		if accessError:
			# playlist url invalid (error msg was displayed !) or download problem
			
			# reloading the DownloadedVideoInfoDic will enable to obtain which videos have been
			# successfully downloaded
			reloaded_downloadedVideoInfoDictionary = DownloadedVideoInfoDic(targetAudioDir)
			
			return reloaded_downloadedVideoInfoDictionary
		
		# extracting/suppressing the audio portions for the downloaded audio tracks
		audioExtractor = AudioExtractor(self.guiOutput, targetAudioDir, downloadedVideoInfoDictionary)
		audioExtractor.extractPlaylistAudio(downloadedVideoInfoDictionary)
		
		# saving the content of the downloadedVideoInfoDictionary which has been completed
		# by AudioExtractor in the directory containing the extracted audio files
		downloadedVideoInfoDictionary.saveDic()
		
		return downloadedVideoInfoDictionary
		
	def trimAudioFile(self, audioFilePathName):
		"""
		Example of command line:
		
		audiodownload.py filePathName e0:0:2-e e0:0:3-e
		audiodownload filePathName e0:0:2-0:10:55 e0:0:3-0:10:53
		
		:param audioFilePathName:
		:return:
		"""
		audioFileName = audioFilePathName.split(DIR_SEP)[-1]
		audioFileDir = audioFilePathName.replace(DIR_SEP + audioFileName, '')
		
		# initializing a partially filled DownloadedVideoInfoDic with only the informations
		# required to trim the audio file
		downloadedVideoInfoDic = DownloadedVideoInfoDic(audioFileDir)
		downloadedVideoInfoDic.addVideoInfoForVideoIndex(1, audioFileName.split('.')[0],
		                                                 '', audioFileName)
		
		# getting the extract time frames specified as command line argument
		# and adding them to the DownloadedVideoInfoDic
		extractStartEndSecondsLists = self.requester.getExtractStartEndSecondsLists()
		
		for extractStartEndSecondsList in extractStartEndSecondsLists:
			downloadedVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(1, extractStartEndSecondsList)

		# now trimming the audio file
		audioExtractor = AudioExtractor(self.guiOutput, audioFileDir, downloadedVideoInfoDic)
		audioExtractor.extractAudioPortions(1, audioFileName, downloadedVideoInfoDic)

if __name__ == "__main__":
	downloader = AudioController()
	downloader.downloadPlaylistAudio()
