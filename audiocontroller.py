import os
from tkinter import Tk

from constants import *
from configmanager import ConfigManager
from requester import Requester
from downloadedvideoinfodic import DownloadedVideoInfoDic
from guioutput import GuiOutput
from youtubeaudiodownloader import YoutubeAudioDownloader
from audioextractor import AudioExtractor

class AudioController:
	def __init__(self, gui, configMgr=None):
		"""
		
		:param gui: used for unit testing only !
		"""

		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/audiodownloader.ini'
		else:
			configFilePathName = 'c:\\temp\\audiodownloader.ini'

		if configMgr == None:
			self.configMgr = ConfigManager(configFilePathName)
		else:
			self.configMgr = configMgr

		self.requester = Requester(self.configMgr)
		
		# Tk must be instanciated in AudioController: class, not in
		# GuyOutput class !
		if gui is None:
			# we are not unit testing !
			self.guiOutput = GuiOutput(Tk())
		else:
			self.guiOutput = gui

		self.audioDownloader = YoutubeAudioDownloader(self.guiOutput)
		
	def downloadPlaylistAudio(self, playlistObject, playlistTitle):
		'''
		Example of playlist title:
		playlist_title (s01:05:52-01:07:23 e01:15:52-E E01:35:52-01:37:23 S01:25:52-e) (s01:05:52-01:07:23 e01:15:52-e S01:25:52-e E01:35:52-01:37:23)
		-e or -E means "to end" !

		:param playlistObject
		
		:return: downloadedVideoInfoDictionary
		'''
		# downloading the audio track of the videos referenced in the playlist
		targetAudioDir, downloadedVideoInfoDictionary, accessError = self.audioDownloader.downloadVideosReferencedInPlaylist(playlistObject, playlistTitle)

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
	
	def getPlaylistData(self, url):
		playlistObject, playlistTitle, accessError = self.audioDownloader.getPlaylistObject(url)
		
		if accessError is None:
			return playlistObject, playlistTitle
		else:
			return None, None
		
	# method temporary here. Will be suppressed !
	def getPrintableResultForInput(self, inputStr, copyResultToClipboard=True):
		'''
		Return the printable request result, the full request command without any command option and
		the full request command with any specified save mode option (option which is to be saved in the
		command history list.
	
		:param inputStr:
		:param copyResultToClipboard: set to True by default. Whreplaying all requests
									  stored in history, set to False, which avoids
									  problem on Android
		:seqdiag_return printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions
	
		:return: 1/ printable request result
				 2/ full request command without any command option
				 3/ full request command with any non save command option
				 4/ full request command with any specified save mode option, None if no save mode option
					is in effect
	
				 Ex: 1/ 0.1 ETH/36 USD on Bitfinex: 21/11/17 10:00 360
					 2/ eth usd 0 bitfinex
					 3/ None (value command with save mode in effect !)
					 4/ eth usd 0 bitfinex -vs0.1eth
	
					 1/ 0.1 ETH/36 USD on Bitfinex: 21/11/17 10:00 360
					 2/ eth usd 0 bitfinex
					 3/ eth usd 0 bitfinex -v0.1eth
					 4/ None (no value command save option in effect)
	
					 1/ ETH/USD on Bitfinex: 21/11/17 10:00 360
					 2/ eth usd 0 bitfinex
					 3/ None (no value command in effect)
					 4/ None (no value command save option in effect)
		'''
		return 'printResult', 'fullCommandStrNoOptions', 'fullCommandStrWithOptions', 'fullCommandStrWithSaveModeOptions', 'fullCommandStrForStatusBar'


if __name__ == "__main__":
	downloader = AudioController()
	downloader.downloadPlaylistAudio()
