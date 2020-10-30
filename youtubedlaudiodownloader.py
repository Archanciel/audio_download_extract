import os, glob, re
from urllib.error import URLError
from pytube import Playlist
import http.client
import youtube_dl

from constants import *
from audiodownloader import AudioDownloader
from playlisttitleparser import PlaylistTitleParser
from accesserror import AccessError

YOUTUBE_DL_QUIET = True

class YoutubeDlAudioDownloader(AudioDownloader):
	def __init__(self, audioController):
		super().__init__(audioController)
	
		if os.name == 'posix':

			self.ydl_opts = {
				'format': 'bestaudio/best',
				'quiet': YOUTUBE_DL_QUIET
			}
		else:
			self.ydl_opts = {
				'format': 'bestaudio/best',
				'postprocessors': [{
					'key': 'FFmpegExtractAudio',
					'preferredcodec': 'mp3',
					'preferredquality': '128',
				}],
				'quiet': YOUTUBE_DL_QUIET
			}
	
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
			self.audioController.setMessage("directory\n{}\nwas created.".format(targetAudioDirShort))

		self.ydl_opts['outtmpl'] = targetAudioDir + DIR_SEP + '%(title)s.' + YOUTUBE_DL_FILE_EXT

		videoIndex = 1
			
		with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
			for videoUrl in playlistObject.video_urls:
				videoTitle = ''
				try:
					meta = ydl.extract_info(videoUrl, download=False)
					videoTitle = meta['title']
				except AttributeError as e:
					print(e)

				if downloadVideoInfoDic.existVideoInfoForVideoTitle(videoTitle):
					# the video was already downloaded
					msgText = videoTitle + ' already downloaded. Video skipped.\n'
					self.audioController.setMessage(msgText)
					videoIndex += 1
					continue

				msgText = 'downloading ' + videoTitle + '\n'
				self.audioController.setMessage(msgText)

				try:
					ydl.download([videoUrl])
				except AttributeError as e:
					print(e)				

				msgText = videoTitle + ' downloaded.\n'
				self.audioController.setMessage(msgText)
				
				downloadedVideoFileName = self.getLastCreatedFileName(targetAudioDir)
				
				if videoTitle == '':
					# the case if ydl.extract_info() raised an AttributeError
					videoTitle = downloadedVideoFileName.replace('.mp3', '')
					
				downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, videoTitle, videoUrl, downloadedVideoFileName)
				downloadVideoInfoDic.saveDic()

				videoIndex += 1
		
		return downloadVideoInfoDic, None

	def getLastCreatedFileName(self, dir):
		files = glob.glob(dir + DIR_SEP + '*.mp3')
		files.sort(key=os.path.getctime, reverse=True)
		
		return files[0].split(DIR_SEP)[-1]
		
	def getDownloadVideoInfoDicForPlaylistUrl(self, playlistUrl):
		playlistObject, playlistTitle, accessError = self.getPlaylistObjectForPlaylistUrl(playlistUrl)
		
		if accessError:
			self.audioController.displayError(accessError.errorMsg)
			return None, None
		
		downloadVideoInfoDic = PlaylistTitleParser.createDownloadVideoInfoDic(playlistTitle)
		
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

		if accessError is None and (playlistTitle is None or 'Oops' in playlistTitle or 'Hoppla' in playlistTitle):
			accessError = AccessError(AccessError.ERROR_TYPE_NOT_PLAYLIST_URL, playlistUrl)

		return playlistObject, playlistTitle, accessError
