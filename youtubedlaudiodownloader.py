import time, os
import datetime
from os.path import sep
import glob, re
from urllib.error import URLError
from urllib.error import HTTPError
from pytube import Playlist
from pytube.exceptions import RegexMatchError
from pytube.exceptions import VideoUnavailable
import http.client
import youtube_dl
from youtube_dl import DownloadError

from audiodownloader import AudioDownloader
from dirutil import DirUtil
from accesserror import AccessError
from youtubedldownloadinfoextractor import YoutubeDlDownloadInfoExtractor


YOUTUBE_DL_QUIET = True
MAX_VIDEO_INDEX = 100

class YoutubeDlAudioDownloader(AudioDownloader):
	
	def __init__(self, audioController, audioDirRoot):
		"""
		Ctor.

		:param audioController:
		:param audioDirRoot: audio dir as defined in the GUI settings.
		"""
		super().__init__(audioController, audioDirRoot)
		
		self.downloadInfoExtractor = YoutubeDlDownloadInfoExtractor(audioDownloader=self,
		                                                            audioController=audioController)
		
		if os.name == 'posix':
			# on AndroidAndroid, FFmpegExtractAudio not available !
			self.ydlOutTmplFormat = '/%(title)s.mp3'

			self.ydl_opts = {
				#'format': 'bestaudio/best', # for unknown reason, not working on
											 # Android when used by AudioDownloaderGUI !
				'format': 'worstaudio/worst',# this fixes the error AttributeError:
											 # 'str' object has no attribute 'write'
				'quiet': YOUTUBE_DL_QUIET,
				"progress_hooks": [self.downloadInfoExtractor.ydlCallableHook]
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
				"progress_hooks": [self.downloadInfoExtractor.ydlCallableHook]
			}

			self.tempYdlFileExtension = 'm4a.ytdl'
			self.convertingVideoToMp3 = False
	
	def downloadPlaylistVideosForUrl(self,
	                                 playlistUrl,
	                                 downloadVideoInfoDic,
	                                 isUploadDateAddedToPlaylistVideo,
	                                 isIndexAddedToPlaylistVideo):
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
		:param isIndexAddedToPlaylistVideo      if True, the name of the video
												audio files referenced in the
												playlist will be started by
												100 minus the video index.
		
		:return: downloadVideoInfoDic, accessError
		"""
		self.downloadInfoExtractor.initPlaylistDownloadInfo()
		playlistStartDownloadTime = time.time()
		playlistDownloadedVideoNb_succeed = 0
		playlistDownloadedVideoNb_failed = 0
		playlistObject, _, _, accessError = self.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)

		if accessError:
			return None, accessError

		targetAudioDir = self.audioDirRoot + sep + downloadVideoInfoDic.getPlaylistDownloadDir()
		targetAudioDirShort = DirUtil.getFullFilePathNameMinusRootDir(rootDir=self.audioDirRoot,
		                                                              fullFilePathName=targetAudioDir,
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
						formattedUploadDate = datetime.datetime.strptime(uploadDate, '%Y%m%d').strftime(' %Y-%m-%d')
				except AttributeError as e:
					msgText = 'obtaining video title and upload date failed with error {}.\n'.format(e)
					self.audioController.displayError(msgText)
					self.displayRetryPlaylistDownloadMsg(downloadVideoInfoDic)
					playlistDownloadedVideoNb_failed += 1

					continue
				
				purgedVideoTitle = DirUtil.replaceUnauthorizedDirOrFileNameChars(videoTitle)
				purgedVideoTitleMp3 = purgedVideoTitle + '.mp3'
				
				if isUploadDateAddedToPlaylistVideo:
					if isIndexAddedToPlaylistVideo:
						addedIndexStr = str(MAX_VIDEO_INDEX - videoIndex) + '-'
						finalPurgedVideoTitleMp3 = addedIndexStr + purgedVideoTitle + formattedUploadDate + '.mp3'
					else:
						if isIndexAddedToPlaylistVideo:
							addedIndexStr = str(MAX_VIDEO_INDEX - videoIndex) + '-'
							finalPurgedVideoTitleMp3 =addedIndexStr + purgedVideoTitle + formattedUploadDate + '.mp3'
						else:
							finalPurgedVideoTitleMp3 = purgedVideoTitle + formattedUploadDate + '.mp3'
				else:
					if isIndexAddedToPlaylistVideo:
						addedIndexStr = str(MAX_VIDEO_INDEX - videoIndex) + '-'
						finalPurgedVideoTitleMp3 = addedIndexStr + purgedVideoTitle + '.mp3'
					else:
						finalPurgedVideoTitleMp3 = purgedVideoTitle + formattedUploadDate + '.mp3'

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
				
				if isUploadDateAddedToPlaylistVideo or isIndexAddedToPlaylistVideo:
					msgText = 'downloading [b]{}[/b] audio ...\n'.format(finalPurgedVideoTitleMp3)
				else:
					msgText = 'downloading [b]{}[/b] audio ...\n'.format(videoTitle)

				self.audioController.displayMessage(msgText)

				try:
					ydl.download([videoUrl])
				except AttributeError as e:
					self.audioController.displayError("downloading video [b]{}[/b] caused this Attribute exception: {}. WARNING: bookmarks will be ignored !\n".format(videoTitle, e))
					self.displayRetryPlaylistDownloadMsg(downloadVideoInfoDic)
					self.convertingVideoToMp3 = False   # avoiding that the display
														# conversion info spread
														# pollutes the GUI
					
					videoIndex, playlistDownloadedVideoNb_failed, msgText  = \
						self.addVideoInfoAndSaveDic(downloadVideoInfoDic,
						                            videoIndex,
						                            videoTitle,
						                            videoUrl,
						                            downloadedFileName=finalPurgedVideoTitleMp3,
						                            playlistDownloadedVideoNb=playlistDownloadedVideoNb_failed,
						                            isDownloadSuccess=False)

					continue    # this avoids that the video is fully downloaded
								# and so facilitates the video redownload.
				except DownloadError as e:
					self.audioController.displayError("downloading video [b]{}[/b] caused this DownloadError exception: {}.\n".format(videoTitle, e))
					self.displayRetryPlaylistDownloadMsg(downloadVideoInfoDic)
					playlistDownloadedVideoNb_failed += 1
					self.convertingVideoToMp3 = False   # avoiding that the display
														# conversion info spread
														# pollutes the GUI

					continue
				
				if isUploadDateAddedToPlaylistVideo or isIndexAddedToPlaylistVideo:
					# finally, renaming the downloaded video to a name which
					# includes the video upload date.
					
					ydlDownloadedAudioFilePathName = targetAudioDir + sep + purgedVideoTitle + '.mp3'
					
					fileNotFoundErrorInfo = DirUtil.renameFile(originalFilePathName=ydlDownloadedAudioFilePathName,
					                                           newFileName=finalPurgedVideoTitleMp3)
					
					if fileNotFoundErrorInfo is not None:
						self.audioController.displayError(fileNotFoundErrorInfo + '\n')
						playlistDownloadedVideoNb_failed += 1
						self.convertingVideoToMp3 = False  # avoiding that the display
						# conversion info spread
						# pollutes the GUI
						
						continue
				
				if self.isAudioFileDownloadOk(targetAudioDir, purgedVideoTitleMp3):
					videoIndex, playlistDownloadedVideoNb_succeed, msgText  = \
						self.addVideoInfoAndSaveDic(downloadVideoInfoDic,
						                            videoIndex,
						                            videoTitle,
						                            videoUrl,
						                            downloadedFileName=finalPurgedVideoTitleMp3,
						                            playlistDownloadedVideoNb=playlistDownloadedVideoNb_succeed)
				else:
					msgText = 'audio download failed. Retry downloading the playlist later to download the failed audio only.\n'

				self.audioController.displayVideoDownloadEndMessage(msgText)
				self.convertingVideoToMp3 = False
			
			# here, all playlist videos have been downloaded
			
			if not self.audioController.stopDownloading:
				playlistTotalDownloadTime = time.time() - playlistStartDownloadTime
				playlistTotalDownloadSize = self.downloadInfoExtractor.getPlaylistDownloadInfo()[0]
				msgText = '[b]{}[/b] playlist audio(s) download terminated.\n'.format(
					downloadVideoInfoDic.getPlaylistNameOriginal())
				self.audioController.displayMessage(msgText)
				self.audioController.displayPlaylistEndDownloadInfo([playlistDownloadedVideoNb_succeed,
				                                                     playlistDownloadedVideoNb_failed,
				                                                     playlistTotalDownloadSize,
				                                                     playlistTotalDownloadTime
				                                                     ])
			else:
				msgText = '[b]{}[/b] playlist audio(s) download interrupted.\n'.format(downloadVideoInfoDic.getPlaylistNameOriginal())
				self.audioController.displayMessage(msgText)

		return downloadVideoInfoDic, None
	
	def addVideoInfoAndSaveDic(self,
	                           downloadVideoInfoDic,
	                           videoIndex,
	                           videoTitle,
	                           videoUrl,
	                           downloadedFileName,
	                           playlistDownloadedVideoNb,
	                           isDownloadSuccess=True):
		"""
		This method add the current downloading video info to the passed
		downloadVideoInfoDic and save the downloadVideoInfoDic.
		
		:param downloadVideoInfoDic:
		:param videoIndex:
		:param videoTitle:
		:param videoUrl:
		:param downloadedFileName:
		:param playlistDownloadedVideoNb:
		:return:
		"""
		# updating and saving the downloadVideoInfoDic if the audio file
		# was downloaded successfully enables to retry downloading the playlist.
		# The failed video download will be retried.
		downloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex=videoIndex,
		                                               videoTitle=videoTitle,
		                                               videoUrl=videoUrl,
		                                               downloadedFileName=downloadedFileName,
		                                               isDownloadSuccess=False)
		downloadVideoInfoDic.saveDic(self.audioDirRoot)
		videoIndex += 1
		playlistDownloadedVideoNb += 1
		msgText = 'video download complete.\n'
		
		return videoIndex, playlistDownloadedVideoNb, msgText
	
	def displayRetryPlaylistDownloadMsg(self, downloadVideoInfoDic):
		msgText = 'retry downloading the playlist later to download the failed audio only ...\n'.format(
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

	def getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(self, url):
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
				with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
					meta = ydl.extract_info(url, download=False)
					videoTitle = meta['title']
			except (RegexMatchError, VideoUnavailable, KeyError, HTTPError, AttributeError, DownloadError) as e:
				errorInfoStr = 'failing URL: {}\nerror info: {}'.format(url, str(e))
				accessError = AccessError(AccessError.ERROR_TYPE_SINGLE_VIDEO_URL_PROBLEM, errorInfoStr)

		if accessError is None and playlistTitle is None and videoTitle is None:
			accessError = AccessError(AccessError.ERROR_TYPE_NOT_PLAYLIST_URL, url)

		if accessError is None and playlistTitle is not None and ('Oops' in playlistTitle or 'Hoppla' in playlistTitle):
			accessError = AccessError(AccessError.ERROR_TYPE_NOT_PLAYLIST_URL, url)

		return playlistObject, playlistTitle, videoTitle, accessError
	
	def getVideoTitlesInPlaylistForUrl(self,
	                                   playlistUrl,
	                                   maxTitlesNumber=AudioDownloader.MAX_VIDEO_TITLES_DEFAULT_NUMBER):
		"""
		This method returns a list containing the titles of the videos
		referenced in the playlist pointed by the passed playlistUrl.
		Since obtaining the video titles referenced in a playlist is
		very time consuming, the maxTitlesNumber passed parm limits
		the number of returned titles.
		
		Currently, this method is not used, except in unit testing.

		:param playlistUrl:
		:param maxTitlesNumber:
		
		:return: video titles list
				 accessError in case of problem, None otherwise
		"""
		videoTitleLst = []
		playlistObject, _, _, accessError = self.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)
		
		if accessError:
			return None, accessError
		
		with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
			try:
				for videoUrl in playlistObject.video_urls:
					meta = ydl.extract_info(videoUrl, download=False)
					videoTitleLst.append(meta['title'])
					maxTitlesNumber -= 1
					
					if maxTitlesNumber <= 0:
						break
			except AttributeError as e:
				msgText = 'obtaining video title failed with error {}.\n'.format(e)
				self.audioController.displayError(msgText)
			except KeyError as e:
				msgText = 'trying to obtain playlist video titles on an invalid url or a url pointing to a single video.\n'
				self.audioController.displayError(msgText)

		return videoTitleLst, None
	
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
				formattedUploadDate = datetime.datetime.strptime(uploadDate, '%Y%m%d').strftime(' %Y-%m-%d')
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
		
		self.convertingVideoToMp3 = False
		
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

