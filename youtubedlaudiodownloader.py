from os.path import sep
from datetime import datetime
import glob, re, logging
from urllib.error import URLError
from urllib.error import HTTPError
from pytube import Playlist
from pytube import YouTube
from pytube.exceptions import RegexMatchError
from pytube.exceptions import VideoUnavailable
import http.client
import youtube_dl
from youtube_dl import DownloadError

from constants import *
from audiodownloader import AudioDownloader
from dirutil import DirUtil
from accesserror import AccessError
from youtubedldownloadinfoextractor import YoutubeDlDownloadInfoExtractor

YOUTUBE_DL_QUIET = True

class YoutubeDlAudioDownloader(AudioDownloader):
	def __init__(self, audioController, audioDirRoot):
		"""
		Ctor.

		:param audioController:
		:param audioDirRoot: audio dir as defined in the GUI settings.
		"""
		super().__init__(audioController, audioDirRoot)
	
		if os.name == 'posix':
			# on AndroidAndroid, FFmpegExtractAudio not available !
			self.ydlOutTmplFormat = '/%(title)s.mp3'

			self.ydl_opts = {
				#'format': 'bestaudio/best', # for unknown reason, not working on
											 # Android when used by AudioDownloaderGUI !
				'format': 'worstaudio/worst',# this fixes the error AttributeError:
											 # 'str' object has no attribute 'write'
				'quiet': YOUTUBE_DL_QUIET,
				"progress_hooks": [YoutubeDlDownloadInfoExtractor(audioController).ydlCallableHook]
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
				'quiet': YOUTUBE_DL_QUIET,
				"progress_hooks": [YoutubeDlDownloadInfoExtractor(audioController).ydlCallableHook]
			}

			self.tempYdlFileExtension = 'm4a.ytdl'

	def downloadPlaylistVideosForUrl(self,
	                                 playlistUrl,
	                                 downloadVideoInfoDic,
	                                 isUploadDateAddedToPlaylistVideo):
		"""
		Downloads the video(s) of the play list referenced in the passed playlistUrl and add to
		the passed downloadVideoInfoDic the downloaded videos information as well as the
		playlist download dir.

		:param playlistUrl:
		:param downloadVideoInfoDic:
		:param isUploadDateAddedToPlaylistVideo if True, the name of the video
												audio files referenced in the
												playlist will be terminated by
												the video upload date.
		
		:return: downloadVideoInfoDic, accessError
		"""
		playlistObject, _, _, accessError = self.getPlaylistObjectAndTitlesFortUrl(playlistUrl)

		if accessError:
			return None, accessError

		targetAudioDir = self.audioDirRoot + sep + downloadVideoInfoDic.getPlaylistDownloadDir()
		targetAudioDirShort = DirUtil.getFullDirMinusRootDir(rootDir=self.audioDirRoot,
		                                                     fullDir=targetAudioDir,
		                                                     eliminatedRootLastSubDirsNumber=1)
		_, dirCreationMessage = DirUtil.createTargetDirIfNotExist(rootDir=self.audioDirRoot,
		                                                          targetAudioDir=targetAudioDir)
		
		if dirCreationMessage:
			self.audioController.displayMessage(dirCreationMessage)
		
		targetAudioDirFileNameList = DirUtil.getFileNamesInDir(targetAudioDir)
		self.ydl_opts['outtmpl'] = targetAudioDir + self.ydlOutTmplFormat

		videoIndex = downloadVideoInfoDic.getNextVideoIndex()
			
		with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
			for videoUrl in playlistObject.video_urls:
				if self.audioController.stopDownloading:
					msgText = '[b]{}[/b] playlist audio(s) download interrupted.\n'.format(
						downloadVideoInfoDic.getPlaylistNameOriginal())
					self.audioController.displayMessage(msgText)
					self.audioController.downloadStopped()
					
					return downloadVideoInfoDic, None
				
				formattedUploadDate = ''
				
				try:
					meta = ydl.extract_info(videoUrl, download=False)
					videoTitle = meta['title']
					
					if isUploadDateAddedToPlaylistVideo:
						uploadDate = meta['upload_date']
						formattedUploadDate = datetime.strptime(uploadDate, '%Y%m%d').strftime(' %Y-%m-%d')
				except AttributeError as e:
					msgText = 'obtaining video title failed with error {}.\n'.format(e)
					self.audioController.displayError(msgText)
					self.displayRetryPlaylistDownloadMsg(downloadVideoInfoDic)
					
					continue
				
				purgedVideoTitle = DirUtil.replaceUnauthorizedDirOrFileNameChars(videoTitle)
				purgedVideoTitleMp3 = purgedVideoTitle + '.mp3'
				
				if isUploadDateAddedToPlaylistVideo:
					finalPurgedVideoTitleMp3 = purgedVideoTitle + formattedUploadDate + '.mp3'
				else:
					finalPurgedVideoTitleMp3 = purgedVideoTitleMp3

				if downloadVideoInfoDic.existVideoInfoForVideoTitle(videoTitle):
					audioFileNameInDic = downloadVideoInfoDic.getVideoFileNameForVideoTitle(videoTitle)
					if audioFileNameInDic in targetAudioDirFileNameList:
						# the video was already downloaded and converted to audio file
						if audioFileNameInDic == finalPurgedVideoTitleMp3:
							msgText = '[b]{}[/b] audio already downloaded in [b]{}[/b] dir. Video skipped.\n'.format(finalPurgedVideoTitleMp3, targetAudioDirShort)
						else:
							msgText = '[b]{}[/b] audio already downloaded in [b]{}[/b] dir as [b]{}[/b]. Video skipped.\n'.format(
								finalPurgedVideoTitleMp3, targetAudioDirShort, audioFileNameInDic)
					else:
						# the video audio file was already downloaded and was deleted
						if audioFileNameInDic == finalPurgedVideoTitleMp3:
							msgText = '[b]{}[/b] audio already downloaded in [b]{}[/b] dir but was deleted. Video skipped.\n'.format(finalPurgedVideoTitleMp3, targetAudioDirShort)
						else:
							msgText = '[b]{}[/b] audio already downloaded in [b]{}[/b] dir as [b]{}[/b] which was deleted. Video skipped.\n'.format(
								finalPurgedVideoTitleMp3, targetAudioDirShort, audioFileNameInDic)

					self.audioController.displayMessage(msgText)
					continue
				
				if isUploadDateAddedToPlaylistVideo:
					msgText = 'downloading [b]{}[/b] audio ...\n'.format(finalPurgedVideoTitleMp3)
				else:
					msgText = 'downloading [b]{}[/b] audio ...\n'.format(videoTitle)

				self.audioController.displayMessage(msgText)

				try:
					ydl.download([videoUrl])
				except AttributeError as e:
					self.audioController.displayError("downloading video [b]{}[/b] caused this Attribute exception: {}. WARNING: bookmarks will be ignored !\n".format(videoTitle, e))
					self.displayRetryPlaylistDownloadMsg(downloadVideoInfoDic)
					
					#continue
				except DownloadError as e:
					self.audioController.displayError("downloading video [b]{}[/b] caused this DownloadError exception: {}.\n".format(videoTitle, e))
					self.displayRetryPlaylistDownloadMsg(downloadVideoInfoDic)
					
					continue
					
				if isUploadDateAddedToPlaylistVideo:
					# finally, renaming the downloaded video to a name which
					# includes the video upload date.
					
					ydlDownloadedAudioFilePathName = targetAudioDir + sep + purgedVideoTitle + '.mp3'
					
					fileNotFoundErrorInfo = DirUtil.renameFile(originalFilePathName=ydlDownloadedAudioFilePathName,
					                                           newFileName=finalPurgedVideoTitleMp3)
					
					if fileNotFoundErrorInfo is not None:
						self.audioController.displayError(fileNotFoundErrorInfo + '\n')
				
				if self.isAudioFileDownloadOk(targetAudioDir, purgedVideoTitleMp3):
					# updating and saving the downloadVideoInfoDic only if the audio file
					# was downloaded successfully enables to retry downloading the playlist.
					# The failed video download will be retried.
					downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex,
					                                               videoTitle,
					                                               videoUrl,
					                                               finalPurgedVideoTitleMp3)
					downloadVideoInfoDic.saveDic(self.audioDirRoot)
					videoIndex += 1
					
					msgText = 'video download complete.\n'
				else:
					msgText = 'audio download failed. Retry downloading the playlist later to download the failed audio only.\n'

				self.audioController.displayMessage(msgText)
			
			if not self.audioController.stopDownloading:
				msgText = '[b]{}[/b] playlist audio(s) download terminated.\n'.format(downloadVideoInfoDic.getPlaylistNameOriginal())
			else:
				msgText = '[b]{}[/b] playlist audio(s) download interrupted.\n'.format(downloadVideoInfoDic.getPlaylistNameOriginal())

			self.audioController.displayMessage(msgText)
		
		return downloadVideoInfoDic, None
	
	def displayRetryPlaylistDownloadMsg(self, downloadVideoInfoDic):
		msgText = '\nretry downloading the playlist later to download the failed audio only ...\n'.format(
			downloadVideoInfoDic.getPlaylistNameOriginal())
		self.audioController.displayMessage(msgText)
	
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
		ytdlFilePathName = targetAudioDir + sep + ytdlFileName
		
		return not os.path.isfile(ytdlFilePathName)
		
	def getLastCreatedMp3FileName(self, dir):
		files = glob.glob(dir + sep + '*.mp3')
		
		if files == []:
			# the case if a problem (an AttributeError) occurred which prevented
			# youtube-dl to convert the downloaded video to a mp3 file.
			return ''
		
		files.sort(key=os.path.getctime, reverse=True)
		
		return files[0].split(sep)[-1]

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

	def downloadSingleVideoForUrl(self,
								  singleVideoUrl,
								  originalVideoTitle,
								  modifiedVideoTitle,
								  targetAudioDir):
		"""
		Downloads in the passed targetAudioDir the single video referenced in the passed
		singleVideoUrl.
		
		:param singleVideoUrl:      single video url
		:param originalVideoTitle:  always passed
		:param modifiedVideoTitle:  None if the video title was not modified
		:param targetAudioDir:      path where the single video will be downloaded
		"""
		targetAudioDirShort, dirCreationMessage = \
			DirUtil.createTargetDirIfNotExist(rootDir=self.audioDirRoot,
			                                  targetAudioDir=targetAudioDir)
		targetAudioDirFileNameList = []
		
		if dirCreationMessage:
			# target dir was created
			self.audioController.displayMessage(dirCreationMessage)
		else:
			# target dir already existed which means that the single video
			# may be already downloaded
			targetAudioDirFileNameList = DirUtil.getFileNamesInDir(targetAudioDir)

		self.ydl_opts['outtmpl'] = targetAudioDir + self.ydlOutTmplFormat

		with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
			
			# obtaining the single video upload date. This information will
			# be added to the video mp3 audio file name so it is visible in
			# the Smart Audiobook player app.

			formattedUploadDate = ''
			
			try:
				meta = ydl.extract_info(singleVideoUrl, download=False)
				uploadDate = meta['upload_date']
				formattedUploadDate = datetime.strptime(uploadDate, '%Y%m%d').strftime(' %Y-%m-%d')
			except AttributeError as e:
				msgText = 'obtaining video upload date failed with error {}.\n'.format(e)
				self.audioController.displayError(msgText)
			
			if modifiedVideoTitle is None or originalVideoTitle == modifiedVideoTitle:
				videoTitle = originalVideoTitle
			else:
				videoTitle = modifiedVideoTitle
			
			purgedVideoTitle = DirUtil.replaceUnauthorizedDirOrFileNameChars(videoTitle)
			purgedOriginalOrModifiedVideoTitleWithDateMp3 = purgedVideoTitle + formattedUploadDate + '.mp3'
			
			# testing if the single video has already been downloaded in the
			# target audio dir. If yes, we do not re download it.
			
			if purgedOriginalOrModifiedVideoTitleWithDateMp3 in targetAudioDirFileNameList:
				msgText = '[b]{}[/b] audio already downloaded in [b]{}[/b] dir. Video skipped.\n'.format(purgedOriginalOrModifiedVideoTitleWithDateMp3, targetAudioDirShort)
				self.audioController.displayMessage(msgText)
				
				return
		
			# now downloading the single video ...
			
			msgText = 'downloading [b]{}[/b] audio ...\n'.format(purgedOriginalOrModifiedVideoTitleWithDateMp3)
			self.audioController.displayMessage(msgText)

			try:
				ydl.download([singleVideoUrl])
			except AttributeError as e:
				self.audioController.displayError(
					"downloading video [b]{}[/b] caused this Attribute exception: {}. WARNING: bookmarks will be ignored !\n".format(
						purgedOriginalOrModifiedVideoTitleWithDateMp3, e))

				#return
		
		# finally, renaming the downloaded video to a name which is either
		# the original video title or the modified video title, in both cases
		# with including the upload date
		
		ydlDownloadedAudioFilePathName = targetAudioDir + sep + purgedVideoTitle + '.mp3'

		fileNotFoundErrorInfo = DirUtil.renameFile(originalFilePathName=ydlDownloadedAudioFilePathName,
		                                           newFileName=purgedOriginalOrModifiedVideoTitleWithDateMp3)

		if fileNotFoundErrorInfo is None:
			msgText = '[b]{}[/b] audio downloaded in [b]{}[/b] directory.\n'.format(
				purgedOriginalOrModifiedVideoTitleWithDateMp3, targetAudioDirShort)
			self.audioController.displayMessage(msgText)
		else:
			self.audioController.displayError(fileNotFoundErrorInfo + '\n')

