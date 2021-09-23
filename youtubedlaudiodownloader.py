import glob, re, logging
from urllib.error import URLError, HTTPError
from urllib.error import HTTPError
from pytube import Playlist, YouTube
from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable
from pytube.exceptions import VideoUnavailable
import http.client
import youtube_dl
from youtube_dl import DownloadError

from constants import *
from audiodownloader import AudioDownloader
from playlisttitleparser import PlaylistTitleParser
from dirutil import DirUtil
from accesserror import AccessError

YOUTUBE_DL_QUIET = True

class YoutubeDlAudioDownloader(AudioDownloader):
	def __init__(self, audioController, audioDir):
		super().__init__(audioController, audioDir)
	
		if os.name == 'posix':
			# on AndroidAndroid, FFmpegExtractAudio not available !
			self.ydlOutTmplFormat = '/%(title)s.mp3'

			self.ydl_opts = {
				#'format': 'bestaudio/best', # for unknown reason, not working on
											 # Android when used by AudioDownloaderGUI !
				'format': 'worstaudio/worst',# this fixes the error AttributeError:
											 # 'str' object has no attribute 'write'
				'quiet': YOUTUBE_DL_QUIET
			}
			
			self.tempYdlFileExtension = 'mp3.ytdl'
		else:
			self.ydlOutTmplFormat = '\\%(title)s.%(ext)s'
			
			self.ydl_opts = {
				'format': 'worstaudio/worst',
				'postprocessors': [{
					'key': 'FFmpegExtractAudio',
					'preferredcodec': 'mp3',
					'preferredquality': '64',
				}],
				'quiet': YOUTUBE_DL_QUIET
			}

			self.tempYdlFileExtension = 'm4a.ytdl'

	def downloadVideosReferencedInPlaylistForPlaylistUrl(self, playlistUrl, downloadVideoInfoDic):
		"""
		Downloads the video(s) of the play list referenced in the passed playlistUrl and add to
		the passed downloadVideoInfoDic the downloaded videos information as well as the
		playlist download dir.

		:param playlistUrl:
		:param downloadVideoInfoDic:
		
		:return: downloadVideoInfoDic, accessError
		"""
		playlistObject, _, _, accessError = self.getPlaylistObjectAndTitlesFortUrl(playlistUrl)

		if accessError:
			return None, accessError

		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()
		targetAudioDirShort = DirUtil.getLastSubDirs(targetAudioDir, subDirsNumber=2)
		_, dirCreationMessage = DirUtil.createTargetDirIfNotExist(targetAudioDir)
		
		if dirCreationMessage:
			self.audioController.displayMessage(dirCreationMessage)
		
		targetAudioDirFileNameList = DirUtil.getFileNamesInDir(targetAudioDir)
		self.ydl_opts['outtmpl'] = targetAudioDir + self.ydlOutTmplFormat

		videoIndex = downloadVideoInfoDic.getNextVideoIndex()
			
		with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
			for videoUrl in playlistObject.video_urls:
				videoTitle = ''
				
				try:
					meta = ydl.extract_info(videoUrl, download=False)
					videoTitle = meta['title']
				except AttributeError as e:
					msgText = 'Obtaining video title failed with error {}.\n'.format(e)
					self.audioController.displayMessage(msgText)
				
				if downloadVideoInfoDic.existVideoInfoForVideoTitle(videoTitle):
					if downloadVideoInfoDic.getVideoFileNameForVideoTitle(videoTitle) in targetAudioDirFileNameList:
						# the video was already downloaded and converted to audio file
						msgText = '[b]{}[/b] audio already downloaded in [b]{}[/b] dir. Video skipped.\n'.format(videoTitle, targetAudioDirShort)
					else:
						# the video audio file was already downloaded and was deleted
						msgText = '[b]{}[/b] audio already downloaded in [b]{}[/b] dir but was deleted. Video skipped.\n'.format(videoTitle, targetAudioDirShort)

					self.audioController.displayMessage(msgText)
					continue

				msgText = 'downloading [b]{}[/b] audio ...\n'.format(videoTitle)
				self.audioController.displayMessage(msgText)

				try:
					ydl.download([videoUrl])
				except AttributeError as e:
					# typically 'str' object has no attribute 'write'. This error
					# is no longer a problem
					self.audioController.displayError("Downloading video [b]{}[/b] caused this Attribute exception: {}. Playlist target dir [b]{}[/b] length is {} chars which exceeds the max acceptable length of 168 chars !".format(videoTitle, e, targetAudioDir, len(targetAudioDir)))
				except DownloadError as e:
					self.audioController.displayError("Downloading video [b]{}[/b] caused this DownloadError exception: {}. Playlist target dir [b]{}[/b] length is {} chars which exceeds the max acceptable length of 168 chars !".format(videoTitle, e, targetAudioDir, len(targetAudioDir)))
					continue
					
				downloadedAudioFileName = self.getLastCreatedMp3FileName(targetAudioDir)
				
				if videoTitle == '':
					# the case if ydl.extract_info() raised an AttributeError
					videoTitle = downloadedAudioFileName.replace('.mp3', '')
				
				if self.isAudioFileDownloadOk(targetAudioDir, downloadedAudioFileName):
					# updating and saving the downloadVideoInfoDic only if the audio file
					# was downloaded successfully enables to retry downloading the playlist.
					# The failed video download will be retried.
					downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex, videoTitle, videoUrl, downloadedAudioFileName)
					downloadVideoInfoDic.saveDic()
					
					msgText = '[b]{}[/b] audio downloaded.\n'.format(videoTitle)
				else:
					msgText = '[b]{}[/b] audio download failed. Please retry downloading the playlist later.\n'.format(videoTitle)

				self.audioController.displayMessage(msgText)

				videoIndex += 1
		
			msgText = '[b]{}[/b] playlist audio(s) download terminated.\n'.format(downloadVideoInfoDic.getPlaylistName())
			self.audioController.displayMessage(msgText)
		
		return downloadVideoInfoDic, None

	def isAudioFileDownloadOk(self, targetAudioDir, downloadedAudioFileName):
		"""
		Return True if no ytdl file version for the passed downloadedAudioFileName
		exist. Otherwise, this means that the mp3 extraction from the downloaded
		video failed.
		
		:param targetAudioDir:
		:param downloadedAudioFileName:
		:return:
		"""
		ytdlFileName = downloadedAudioFileName.replace('mp3', self.tempYdlFileExtension)
		ytdlFilePathName = targetAudioDir + DIR_SEP + ytdlFileName
		
		# logging.info('isAudioFileDownloadOk. ytdlFileName = {}, ytdlFilePathName = {}'.format(ytdlFileName, ytdlFilePathName))
		# logging.info('isAudioFileDownloadOk. doesYtdlFileExist = {}'.format(os.path.isfile(ytdlFilePathName)))
		
		return not os.path.isfile(ytdlFilePathName)
		
	def getLastCreatedMp3FileName(self, dir):
		files = glob.glob(dir + DIR_SEP + '*.mp3')
		files.sort(key=os.path.getctime, reverse=True)
		
		return files[0].split(DIR_SEP)[-1]

	def getPlaylistObjectAndTitlesFortUrl(self, url):
		"""
		Returns a pytube.Playlist instance if the passed url points to a Youtube
		playlist, None otherwise, as well as a playlistTitle or a videoTitle if
		the passed url points to a Youtube single video and an AccessError instance
		if the passed url does not contain a valid Youtube url.
		
		:param url: points either to a Youtube playlist or to a Youtube single video
					or is invalid sinc obtained from the clipboard.
		:return:    playlistObject  if url points to a playlist or None otherwise,
					playlistTitle   if url points to a playlist or None otherwise,
					videoTitle      if url points to a single video or None otherwise,
					accessError     if the url is invalid (clipboard contained anything but
									a Youtube valid url
		"""
		playlistObject = None
		playlistTitle = None
		videoTitle = None
		accessError = None

		try:
			playlistObject = Playlist(url)
			playlistObject._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
			playlistTitle = playlistObject.title
		except http.client.InvalidURL as e:
			accessError = AccessError(AccessError.ERROR_TYPE_PLAYLIST_URL_INVALID, str(e))
		except AttributeError as e:
			accessError = AccessError(AccessError.ERROR_TYPE_PLAYLIST_URL_INVALID, str(e))
		except URLError:
			accessError = AccessError(AccessError.ERROR_TYPE_NO_INTERNET, 'No internet access. Fix the problem and retry !')
		except KeyError:
			# this happens if the url in the clipboard points to a single video !
			pass

		if url != '' and accessError is None and playlistTitle is None:
			# the case if the url points to a single video instead of a playlist
			# or if the URL obtained from the clipboard is invalid.
			try:
				youtube = YouTube(url)
				video = youtube.streams.first()
				videoTitle = video.title
			except (RegexMatchError, VideoUnavailable, KeyError, HTTPError) as e:
				errorInfoStr = 'failing URL: {}\nerror info: {}'.format(url, str(e))
				accessError = AccessError(AccessError.ERROR_TYPE_SINGLE_VIDEO_URL_PROBLEM, errorInfoStr)

		if accessError is None and playlistTitle is None and videoTitle is None:
			accessError = AccessError(AccessError.ERROR_TYPE_NOT_PLAYLIST_URL, url)

		if accessError is None and playlistTitle is not None and ('Oops' in playlistTitle or 'Hoppla' in playlistTitle):
			accessError = AccessError(AccessError.ERROR_TYPE_NOT_PLAYLIST_URL, url)

		return playlistObject, playlistTitle, videoTitle, accessError
	
	def getDownloadVideoInfoDicForPlaylistTitle(self, playlistTitle):
		"""
		Returns a DownloadVideoInfoDic for the passed playlistTitle. The playlistTitle
		may contain extract / suppress info (ex: 'Test 3 short videos
		(e0:0:4-0:0:6 e0:0:12-e s0:0:1-0:0:3 s0:0:4-0:0:6 s0:0:9-e)$
		(s0:0:2-0:0:4 s0:0:5-0:0:7 s0:0:10-e) (e0:0:2-0:0:3 e0:0:5-e)'), info which will be
		added o the returned DownloadVideoInfoDic.
		
		:param playlistTitle:
		
		:return: downloadVideoInfoDic, accessError
		"""
		return PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistTitle, self.audioDir)
	
	def getPlaylistObjectOrVideoTitleFortUrl(self, url):
		"""
		The passed url can either point to a Youtube playlist or to a Youtube
		single video.
		
		In case of playlist url, the method returns the pytube.Playlist object
		corresponding to the passed url, the playlist title, None for the video
		title and None for the access error if no problem happened.
		
		In case of video url, the method returns an invalid playlist object,
		None for the playlist title, the video title and None for the access error
		if no problem happened.
		
		:param url: playlist or single video url
		:return: playlistObject - Playlist object or None
				 playlistTitle - playlist title or None
				 videoTitle - video title or None
				 accessError in case of problem, None otherwise
		"""
		playlistObject = None
		playlistTitle = None
		videoTitle = None
		accessError = None
		
		try:
			playlistObject = Playlist(url)
			playlistObject._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
			playlistTitle = playlistObject.title
		except http.client.InvalidURL as e:
			accessError = AccessError(AccessError.ERROR_TYPE_PLAYLIST_URL_INVALID, str(e))
		except AttributeError as e:
			accessError = AccessError(AccessError.ERROR_TYPE_PLAYLIST_URL_INVALID, str(e))
		except URLError:
			accessError = AccessError(AccessError.ERROR_TYPE_NO_INTERNET, 'No internet access. Fix the problem and retry !')
		except KeyError:
			# this happens if the url in the clipboard points to a single video !
			pass

		if url != '' and accessError is None and playlistTitle is None:
			# the case if the url points to a single video instead of a playlist
			# or if the URL obtained from the clipboard is invalid.
			try:
				youtube = YouTube(url)
				video = youtube.streams.first()
				videoTitle = video.title
			except (RegexMatchError, VideoUnavailable, KeyError, HTTPError) as e:
				errorInfoStr = 'failing URL: {}\nerror info: {}'.format(url, str(e))
				accessError = AccessError(AccessError.ERROR_TYPE_SINGLE_VIDEO_URL_PROBLEM, errorInfoStr)
		
		if accessError is None and playlistTitle is None and videoTitle is None:
			accessError = AccessError(AccessError.ERROR_TYPE_NOT_PLAYLIST_URL, url)

		if accessError is None and playlistTitle is not None and ('Oops' in playlistTitle or 'Hoppla' in playlistTitle):
			accessError = AccessError(AccessError.ERROR_TYPE_NOT_PLAYLIST_URL, url)

		return playlistObject, playlistTitle, videoTitle, accessError

	def downloadSingleVideoForUrl(self, singleVideoUrl, videoTitle, targetAudioDir):
		"""
		Downloads in the passed targetAudioDir the single video referenced in the passed
		singleVideoUrl.
		
		:param singleVideoUrl:
		:param videoTitle:
		:param targetAudioDir:
		"""
		targetAudioDirShort, dirCreationMessage = DirUtil.createTargetDirIfNotExist(targetAudioDir)
		targetAudioDirFileNameList = []
		
		if dirCreationMessage:
			# target dir was created
			self.audioController.displayMessage(dirCreationMessage)
		else:
			# target dir already existed which means that the single video
			# may already be downloaded
			targetAudioDirFileNameList = DirUtil.getFileNamesInDir(targetAudioDir)

		purgedVideoTitle = DirUtil.replaceUnauthorizedDirOrFileNameChars(videoTitle)
		
		if purgedVideoTitle + '.mp3' in targetAudioDirFileNameList:
			msgText = '[b]{}[/b] audio already downloaded in [b]{}[/b] dir. Video skipped.\n'.format(videoTitle, targetAudioDirShort)
			self.audioController.displayMessage(msgText)
			return
		
		self.ydl_opts['outtmpl'] = targetAudioDir + self.ydlOutTmplFormat
		
		with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
			msgText = 'downloading [b]{}[/b] audio ...\n'.format(videoTitle)
			self.audioController.displayMessage(msgText)

			try:
				ydl.download([singleVideoUrl])
			except AttributeError as e:
				# typically 'str' object has no attribute 'write'. This error
				# is no longer a problem
				logging.info("Downloading video {} caused this Attribute exception: {}".format(videoTitle, e))
			
			msgText = '[b]{}[/b] audio downloaded in [b]{}[/b] directory.\n'.format(videoTitle, targetAudioDirShort)
			self.audioController.displayMessage(msgText)
