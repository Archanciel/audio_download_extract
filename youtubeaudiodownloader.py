import re
from urllib.error import URLError
from pytube import Playlist
import http.client

from constants import *
from audiodownloader import AudioDownloader
from playlisttitleparser import PlaylistTitleParser
from accesserror import AccessError

class YoutubeAudioDownloader(AudioDownloader):
	def __init__(self, guiOutput):
		super().__init__(guiOutput)

	def downloadVideosReferencedInPlaylistForPlaylistUrl(self, playlistUrl):
		'''
		
		:param playlistUrl:
		
		:return: downloadVideoInfoDic, accessError
		'''
		playlistObject, downloadVideoInfoDic = self.getDownloadVideoInfoDicForPlaylistUrl(playlistUrl)
		targetAudioDir = downloadVideoInfoDic.downloadDir
		
		if not os.path.isdir(targetAudioDir):
			targetAudioDirList = targetAudioDir.split(DIR_SEP)
			targetAudioDirShort = DIR_SEP.join(targetAudioDirList[-2:])
			
			if not self.guiOutput.getConfirmation("Directory\n{}\nwill be created.\n\nContinue with download ?".format(targetAudioDirShort)):
				return targetAudioDir, downloadVideoInfoDic
			
			os.makedirs(targetAudioDir)
		
		try:
			videoIndex = 1
			
			for video in playlistObject.videos:
				videoTitle = video.title

				if downloadVideoInfoDic.existVideoInfoForVideoTitle(videoTitle):
					# the video was already downloaded
					self.msgText = self.msgText + videoTitle + ' already downloaded. Video skipped.\n'
					self.guiOutput.setMessage(self.msgText)
					videoIndex += 1
					continue
					
				try:
					audioStream = video.streams.get_by_itag(YOUTUBE_STREAM_AUDIO)
					videoUrl = video.watch_url
					self.msgText = self.msgText + 'downloading ' + videoTitle + '\n'
					self.guiOutput.setMessage(self.msgText)
					audioStream.download(output_path=targetAudioDir)
					downloadedVideoFileName = audioStream.default_filename
				except:
					accessError = AccessError(AccessError.ERROR_TYPE_VIDEO_DOWNLOAD_FAILURE, videoTitle)
					self.msgText = self.msgText + accessError.errorMsg
					self.guiOutput.setMessage(self.msgText)
					return targetAudioDir, downloadVideoInfoDic, accessError
				else:
					self.msgText = self.msgText + videoTitle + ' downloaded.\n'
					self.guiOutput.setMessage(self.msgText)
					downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, videoTitle, videoUrl, downloadedVideoFileName)
					downloadVideoInfoDic.saveDic()
				videoIndex += 1
		except:
			accessError = AccessError(AccessError.ERROR_TYPE_PLAYLIST_DOWNLOAD_FAILURE, downloadVideoInfoDic.playlistName)
			self.msgText = self.msgText + accessError.errorMsg
			self.guiOutput.setMessage(self.msgText)
			return targetAudioDir, downloadVideoInfoDic, accessError
		
		return downloadVideoInfoDic, None

	def getDownloadVideoInfoDicForPlaylistUrl(self, playlistUrl):
		playlistObject, playlistTitle, accessError = self.getPlaylistObjectForPlaylistUrl(playlistUrl)
		
		if accessError:
			self.guiOutput.displayError(accessError.errorMsg)
			return None, None
		
		downloadVideoInfoDic = PlaylistTitleParser.createDownloadVideoInfoDic(playlistTitle)
		
		return playlistObject, downloadVideoInfoDic
	
	def downloadVideosReferencedInPlaylist(self, playlistObject, playlistTitle):
		'''

		:param playlistObject:
		:param playlistUrl:

		:return: targetAudioDir, downloadVideoInfoDic
		'''
		playlistName, targetAudioDir, downloadVideoInfoDic = PlaylistTitleParser.createDownloadVideoInfoDic(playlistTitle)
		
		if not os.path.isdir(targetAudioDir):
			targetAudioDirList = targetAudioDir.split(DIR_SEP)
			targetAudioDirShort = DIR_SEP.join(targetAudioDirList[-2:])
			
			if not self.guiOutput.getConfirmation(
					"Directory\n{}\nwill be created.\n\nContinue with download ?".format(targetAudioDirShort)):
				return targetAudioDir, downloadVideoInfoDic
			
			os.makedirs(targetAudioDir)
		
		try:
			videoIndex = 1
			
			for video in playlistObject.videos:
				videoTitle = video.title
				
				if downloadVideoInfoDic.existVideoInfoForVideoTitle(videoTitle):
					# the video was already downloaded
					self.msgText = self.msgText + videoTitle + ' already downloaded. Video skipped.\n'
					self.guiOutput.setMessage(self.msgText)
					videoIndex += 1
					continue
				
				try:
					audioStream = video.streams.get_by_itag(YOUTUBE_STREAM_AUDIO)
					videoUrl = video.watch_url
					self.msgText = self.msgText + 'downloading ' + videoTitle + '\n'
					self.guiOutput.setMessage(self.msgText)
					audioStream.download(output_path=targetAudioDir)
					downloadedVideoFileName = audioStream.default_filename
				except:
					accessError = AccessError(AccessError.ERROR_TYPE_VIDEO_DOWNLOAD_FAILURE, videoTitle)
					self.msgText = self.msgText + accessError.errorMsg
					self.guiOutput.setMessage(self.msgText)
					return targetAudioDir, downloadVideoInfoDic, accessError
				else:
					self.msgText = self.msgText + videoTitle + ' downloaded.\n'
					self.guiOutput.setMessage(self.msgText)
					downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, videoTitle, videoUrl,
					                                                 downloadedVideoFileName)
					downloadVideoInfoDic.saveDic()
				videoIndex += 1
		except:
			accessError = AccessError(AccessError.ERROR_TYPE_PLAYLIST_DOWNLOAD_FAILURE, playlistName)
			self.msgText = self.msgText + accessError.errorMsg
			self.guiOutput.setMessage(self.msgText)
			return targetAudioDir, downloadVideoInfoDic, accessError
		
		return targetAudioDir, downloadVideoInfoDic, None
	
	def getPlaylistObjectForPlaylistUrl(self, playlistUrl):
		"""
		Returns the pytube.Playlist object corresponding to the passed playlistUrl the
		playlistObject title and None if no problem happened.
		
		:param playlistUrl:
		:return: playlistObject - Playlist object
				 playlistTitle
				 accessError in case of problem, None otherwise
		"""
		playlistObject = None
		playlistTitle = None
		accessError = None
		
		try:
			playlistObject = Playlist(playlistUrl)
			playlistObject._video_regex = re.compile(r"\"playlistUrl\":\"(/watch\?v=[\w-]*)")
			playlistTitle = playlistObject.title()
		except http.client.InvalidURL as e:
			accessError = AccessError(AccessError.ERROR_TYPE_PLAYLIST_URL_INVALID, str(e))
		except AttributeError as e:
			accessError = AccessError(AccessError.ERROR_TYPE_PLAYLIST_URL_INVALID, str(e))
		except URLError:
			accessError = AccessError(AccessError.ERROR_TYPE_NO_INTERNET, 'No internet access. Fix the problem and retry !')

		if accessError is None and (playlistTitle is None or 'Oops' in playlistTitle):
			accessError = AccessError(AccessError.ERROR_TYPE_NOT_PLAYLIST_URL, playlistUrl)

		return playlistObject, playlistTitle, accessError
