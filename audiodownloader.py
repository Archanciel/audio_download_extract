import re, os
from pytube import YouTube, Playlist 
import http.client

from constants import *

class AudioDownloader:
	def __init__(self, guiOutput):
		self.guiOutput = guiOutput
		self.msgText = ''
		
	def downloadAudioFromPlaylist(self, playlistUrl):

		playlist = None
		
		try:
			playlist = Playlist(playlistUrl)
			playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
		except KeyError as e:
			self.guiOutput.displayError('Playlist URL not in clipboard. Program closed.')			
			return
		except http.client.InvalidURL as e:
			self.guiOutput.displayError(str(e))
			return
		
		playlistTitle = playlist.title()

		if 'Oops' in playlistTitle:
			self.guiOutput.displayError('The URL obtained from clipboard is not pointing to a playlist. Program closed.')
			return
			
		playlistName, timeInfo = self.splitPlayListTitle(playlistTitle)
		targetAudioDir = AUDIO_DIR + DIR_SEP + playlistName
		
		if not os.path.isdir(targetAudioDir):
			targetAudioDirList = targetAudioDir.split(DIR_SEP)
			targetAudioDirShort = DIR_SEP.join(targetAudioDirList[-2:])
			
			if not self.guiOutput.getConfirmation("Directory\n{}\nwill be created.\n\nContinue with download ?".format(targetAudioDirShort)):
				return
				
			os.makedirs(targetAudioDir)
				
		for video in playlist.videos:
			audioStream = video.streams.get_by_itag(YOUTUBE_STREAM_AUDIO)
			videoTitle = video.title
			self.msgText = self.msgText + 'downloading ' + videoTitle + '\n'
			self.guiOutput.setMessage(self.msgText)
			audioStream.download(output_path=targetAudioDir)
		
		return timeInfo, targetAudioDir
	
	def splitPlayListTitle(self, playlistTitle):
		pattern = r"(.+) ([\d\./]+)"
		playlistName = None
		timeInfo = None

		match = re.match(pattern, playlistTitle)
		
		if match:
			playlistName = match.group(1)
			timeInfo = match.group(2)
		else:
			# no time info provided in the play list title
			playlistName = playlistTitle

		return playlistName, timeInfo
		