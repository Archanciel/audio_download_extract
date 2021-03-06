import re
from urllib.error import URLError
from pytube import Playlist
import http.client

from constants import *
from audiodownloader import AudioDownloader
from playlisttitleparser import PlaylistTitleParser
from accesserror import AccessError

class YoutubeAudioDownloader(AudioDownloader):
	def __init__(self, audioController):
		super().__init__(audioController)

	def downloadVideosReferencedInPlaylistForPlaylistUrl(self, playlistUrl, downloadVideoInfoDic):
		'''
		
		:param playlistUrl:
		
		:return: downloadVideoInfoDic, accessError
		'''
		playlistObject, _, accessError = self.getPlaylistObjectForPlaylistUrl(playlistUrl)

		if accessError:
			return None, accessError

		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()
		
		if not os.path.isdir(targetAudioDir):
			targetAudioDirList = targetAudioDir.split(DIR_SEP)
			targetAudioDirShort = DIR_SEP.join(targetAudioDirList[-2:])
			
			os.makedirs(targetAudioDir)
			self.audioController.displayMessage("directory\n{}\nwas created.".format(targetAudioDirShort))
		
		try:
			videoIndex = 1
			
			for video in playlistObject.videos:
				videoTitle = video.title

				if downloadVideoInfoDic.existVideoInfoForVideoTitle(videoTitle):
					# the video was already downloaded
					msgText = videoTitle + ' already downloaded. Video skipped.\n'
					self.audioController.displayMessage(msgText)
					videoIndex += 1
					continue
					
				try:
					audioStream = video.streams.get_by_itag(YOUTUBE_STREAM_AUDIO)
					videoUrl = video.watch_url
					msgText = 'downloading ' + videoTitle + '\n'
					self.audioController.displayMessage(msgText)
					audioStream.download(output_path=targetAudioDir)
					downloadedVideoFileName = audioStream.default_filename
				except:
					accessError = AccessError(AccessError.ERROR_TYPE_VIDEO_DOWNLOAD_FAILURE, videoTitle)
					self.audioController.displayMessage(accessError.errorMsg)
					return downloadVideoInfoDic, accessError
				else:
					msgText = videoTitle + ' downloaded.\n'
					self.audioController.displayMessage(msgText)
					downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, videoTitle, videoUrl, downloadedVideoFileName)
					downloadVideoInfoDic.saveDic()
				videoIndex += 1
		except KeyError as e:
			accessError = AccessError(AccessError.ERROR_TYPE_PLAYLIST_DOWNLOAD_FAILURE, downloadVideoInfoDic.getPlaylistName())
			self.audioController.displayMessage(accessError.errorMsg)
			return downloadVideoInfoDic, accessError
		
		return downloadVideoInfoDic, None

	def getDownloadVideoInfoDicForPlaylistUrl(self, playlistUrl):
		playlistObject, playlistTitle, accessError = self.getPlaylistObjectForPlaylistUrl(playlistUrl)
		
		if accessError:
			self.audioController.displayError(accessError.errorMsg)
			return None, None
		
		downloadVideoInfoDic = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle)
		
		return playlistObject, downloadVideoInfoDic
	
	def getPlaylistObjectForPlaylistUrl(self, playlistUrl):
		"""
		Returns the pytube.Playlist object corresponding to the passed playlistObject the
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
			playlistObject._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
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
