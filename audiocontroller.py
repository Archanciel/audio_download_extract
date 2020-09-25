import os
from tkinter import Tk
from configmanager import ConfigManager
from guyoutput import GuyOutput

YOUTUBE_STREAM_AUDIO = '140'

if os.name == 'posix':
	CONVERT = False
	AUDIO_DIR = '/storage/emulated/0/Download/Audiobooks'
	DIR_SEP = '/'
	WIN_WIDTH_RATIO = 1
	WIN_HEIGHT = 800	
else:
	CONVERT = False # can be set to True on Windows only
	AUDIO_DIR = 'D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks'
	DIR_SEP = '\\'
	WIN_WIDTH_RATIO = 0.8
	WIN_HEIGHT = 500	

class AudioController:
	def __init__(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/audiodownload/audiodownload.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\audiodownload\\audiodownload.ini'

		self.configMgr = ConfigManager(configFilePathName)
		
		# Tk must be instanciated in AudioController: class, not in
		# GuyOutput class !
		self.guyOutput = GuyOutput(Tk())
		
	def downloadAudio(self):
		playlistUrl = self.guyOutput.getPlaylistUrlFromClipboard()
		
		if playlistUrl == None:
			self.guyOutput.displayError('Playlist URL not in clipboard. Program closed.')

			return

	def downloadAudioFromPlaylist(self, playlistUrl):

		playlist = None
		
		try:
			playlist = Playlist(playlistUrl)
			playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
		except KeyError as e:
			self.displayError('Playlist URL not in clipboard. Program closed.')			
			return
		except http.client.InvalidURL as e:
			self.displayError(str(e))
			return
		
		playlistTitle = playlist.title()

		if 'Oops' in playlistTitle:
			self.displayError('The URL obtained from clipboard is not pointing to a playlist. Program closed.')
			return
			
		playlistName, timeInfo = self.splitPlayListTitle(playlistTitle)
		targetAudioDir = AUDIO_DIR + DIR_SEP + playlistName
		
		if not os.path.isdir(targetAudioDir):
			targetAudioDirList = targetAudioDir.split(DIR_SEP)
			targetAudioDirShort = DIR_SEP.join(targetAudioDirList[-2:])
			
			if self.getConfirmation("Directory\n{}\nwill be created.\n\nContinue with download ?".format(targetAudioDirShort)) != 'yes':
				return
				
			os.makedirs(targetAudioDir)
				
		for video in playlist.videos:
			audioStream = video.streams.get_by_itag(YOUTUBE_STREAM_AUDIO)
			videoTitle = video.title
			self.msgText = self.msgText + 'downloading ' + videoTitle + '\n'
			self.msg.configure(text=self.msgText)
			self.root.update()
			audioStream.download(output_path=targetAudioDir)

if __name__ == "__main__":
	downloader = AudioController()
	downloader.downloadAudio()
