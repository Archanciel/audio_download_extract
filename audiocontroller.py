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
	def __init__(self, guiOutputStub=None):
		"""
		
		:param guiOutputStub: used for unit testing only !
		"""
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/audiodownload/audiodownload.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\audiodownload\\audiodownload.ini'

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
		# obtaining th playlist url from the clipboard
		playlistUrl = self.guiOutput.getPlaylistUrlFromClipboard()
		
		if playlistUrl == None:
			self.guiOutput.displayError('Playlist URL not in clipboard. Program closed.')

			return
		
		# downloading the audio track of the videos referenced in the playlist
		audioDownloader = YoutubeAudioDownloader(self.guiOutput)
		targetAudioDir, downloadedVideoInfoDictionary = audioDownloader.downloadVideosReferencedInPlaylist(playlistUrl)

		if targetAudioDir is None:
			# playlist url invalid (error msg was displayed !)
			return
		
		# extracting/suppressing the audio portions for the downloaded audio tracks
		audioExtractor = AudioExtractor(self.guiOutput, targetAudioDir, downloadedVideoInfoDictionary)
		audioExtractor.extractPlaylistAudio(downloadedVideoInfoDictionary)
		
		# saving the content of the downloadedVideoInfoDictionary in the directory containing
		# the extracted audio files
		downloadedVideoInfoDictionary.saveDic()
		
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
