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
		playlistUrl = self.guiOutput.getPlaylistUrlFromClipboard()
		
		if playlistUrl == None:
			self.guiOutput.displayError('Playlist URL not in clipboard. Program closed.')

			return
			
		audioDownloader = YoutubeAccess(self.guiOutput)
		playlistTimeFrameData, targetAudioDir, downloadedVideoInfoDictionary = audioDownloader.downloadAudioFromPlaylist(playlistUrl)
		
		if playlistTimeFrameData:
			audioExtractor = AudioExtractor(self.guiOutput, targetAudioDir, downloadedVideoInfoDictionary)
			audioExtractor.extractAudioPortion(playlistTimeFrameData)
		
		downloadedVideoInfoDictionary.save()
		
if __name__ == "__main__":
	downloader = AudioController()
	downloader.downloadAudio()
