import re
from urllib.error import URLError
from pytube import Playlist
import http.client

from constants import *
from playlisttitleparser import PlaylistTitleParser
from audiodownloader import AudioDownloader

class YoutubeAudioDownloader(AudioDownloader):
	def __init__(self, guiOutput):
		super().__init__(guiOutput)

	def downloadVideosReferencedInPlaylist(self, playlistUrl):
		'''
		
		:param playlistUrl:
		
		:return: targetAudioDir, downloadedVideoInfoDic
		'''
		targetAudioDir = None
		downloadedVideoInfoDic = None

		playlist, errorMsg = self.getPlaylistObject(playlistUrl)
		
		if errorMsg:
			self.guiOutput.displayError("The URL obtained from clipboard is not pointing to a playlist.\nError msg: {}\nProgram will be closed.".format(errorMsg))
			return targetAudioDir, downloadedVideoInfoDic
		
		playlistTitle = playlist.title()

		if playlistTitle == None or \
			'Oops' in playlistTitle:
			self.guiOutput.displayError('The URL obtained from clipboard is not pointing to a playlist. Program closed.')
			return targetAudioDir, downloadedVideoInfoDic
		
		playlistName, targetAudioDir, downloadedVideoInfoDic = PlaylistTitleParser.splitPlaylistTitle(playlistTitle)
		
		if not os.path.isdir(targetAudioDir):
			targetAudioDirList = targetAudioDir.split(DIR_SEP)
			targetAudioDirShort = DIR_SEP.join(targetAudioDirList[-2:])
			
			if not self.guiOutput.getConfirmation("Directory\n{}\nwill be created.\n\nContinue with download ?".format(targetAudioDirShort)):
				return targetAudioDir, downloadedVideoInfoDic
			
			os.makedirs(targetAudioDir)
		
		try:
			videoIndex = 1
			
			for video in playlist.videos:
				videoTitle = video.title
				try:
					audioStream = video.streams.get_by_itag(YOUTUBE_STREAM_AUDIO)
					videoUrl = video.watch_url
					self.msgText = self.msgText + 'downloading ' + videoTitle + '\n'
					self.guiOutput.setMessage(self.msgText)
					audioStream.download(output_path=targetAudioDir)
					downloadedVideoFileName = audioStream.default_filename
				except:
					self.msgText = self.msgText + videoTitle + ' download failed.\n'
					self.guiOutput.setMessage(self.msgText)
				else:
					self.msgText = self.msgText + videoTitle + ' downloaded.\n'
					self.guiOutput.setMessage(self.msgText)
					downloadedVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, videoTitle, videoUrl, downloadedVideoFileName)
				videoIndex += 1
		except:
			self.msgText = self.msgText + playlistName + ' download failed.\n'
			self.guiOutput.setMessage(self.msgText)
		
		return targetAudioDir, downloadedVideoInfoDic
	
	def getPlaylistObject(self, playlistUrl):
		playlist = None
		errorMsg = None
		
		try:
			playlist = Playlist(playlistUrl)
			playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
		except KeyError as e:
			errorMsg = 'Playlist URL not in clipboard. Program closed.'
		except http.client.InvalidURL as e:
			errorMsg = str(e)
		except AttributeError as e:
			errorMsg = 'playlist URL == None'
		except URLError:
			errorMsg = 'No internet access. Fix the problem and retry !'

		return playlist, errorMsg
