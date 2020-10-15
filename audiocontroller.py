import os
from tkinter import Tk

from configmanager import ConfigManager
from guioutput import GuiOutput
from youtubeaccess import YoutubeAccess
from audioextractor import AudioExtractor

class AudioController:
	def __init__(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/audiodownload/audiodownload.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\audiodownload\\audiodownload.ini'

		self.configMgr = ConfigManager(configFilePathName)
		
		# Tk must be instanciated in AudioController: class, not in
		# GuyOutput class !
		self.guiOutput = GuiOutput(Tk())
		
	def downloadAudio(self):
		'''
		# Example of playlist title:
		playlist_title (s01:05:52-01:07:23 e01:15:52-E E01:35:52-01:37:23 S01:25:52-e) (s01:05:52-01:07:23 e01:15:52-e S01:25:52-e E01:35:52-01:37:23)
		-e or -E means "to end" !

		:return:
		'''
		playlistUrl = self.guiOutput.getPlaylistUrlFromClipboard()
		
		if playlistUrl == None:
			self.guiOutput.displayError('Playlist URL not in clipboard. Program closed.')

			return
			
		audioDownloader = YoutubeAccess(self.guiOutput)
		targetAudioDir, downloadedVideoInfoDictionary = audioDownloader.downloadVideosReferencedInPlaylist(playlistUrl)
		
		audioExtractor = AudioExtractor(self.guiOutput, targetAudioDir, downloadedVideoInfoDictionary)
		audioExtractor.extractPlaylistAudio(downloadedVideoInfoDictionary)
		
		downloadedVideoInfoDictionary.saveDic()
		
if __name__ == "__main__":
	downloader = AudioController()
	downloader.downloadAudio()
