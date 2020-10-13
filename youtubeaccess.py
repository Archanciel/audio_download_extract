import re
from urllib.error import URLError
from pytube import YouTube, Playlist 
import http.client

from constants import *
from playlisttitleinterpreter import PlaylistTitleInterpreter

class YoutubeAccess:
	def __init__(self, guiOutput):
		self.guiOutput = guiOutput
		self.msgText = ''
		
	def downloadVideosReferencedInPlaylist(self, playlistUrl):
		'''
		
		:param playlistUrl:
		
		:return: targetAudioDir, downloadedVideoInfoDic
		'''
		targetAudioDir = None
		downloadedVideoInfoDic = None

		playlist = self.getPlaylistObject(playlistUrl)
		
		if playlist == None:
			return targetAudioDir, downloadedVideoInfoDic
		
		playlistTitle = playlist.title()

		if playlistTitle == None or \
			'Oops' in playlistTitle:
			self.guiOutput.displayError('The URL obtained from clipboard is not pointing to a playlist. Program closed.')
			return targetAudioDir, downloadedVideoInfoDic
		
		playlistName, targetAudioDir, downloadedVideoInfoDic = PlaylistTitleInterpreter.splitPlaylistTitle(playlistTitle)
		
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
		
		try:
			playlist = Playlist(playlistUrl)
			playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
		except KeyError as e:
			self.guiOutput.displayError('Playlist URL not in clipboard. Program closed.')
		except http.client.InvalidURL as e:
			self.guiOutput.displayError(str(e))
		except AttributeError as e:
			self.guiOutput.displayError('playlist URL == None')
		except URLError:
			self.guiOutput.displayError('No internet access. Fix the problem and retry !')

		return playlist
