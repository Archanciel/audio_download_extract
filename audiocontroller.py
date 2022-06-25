from os.path import sep
import traceback
import datetime
import os

from downloadplaylistinfodic import DownloadPlaylistInfoDic
from youtubedlaudiodownloader import YoutubeDlAudioDownloader
from dirutil import DirUtil

if os.name == 'posix':
	# sound file extraction is not possible on Android
	pass
else:
	from audioextractor import AudioExtractor

from playlisttitleparser import PlaylistTitleParser

class AudioController:
	SINGLE_VIDEO_DOWNLOAD_SUCCESS = 0
	SINGLE_VIDEO_DOWNLOAD_FAIL = 1
	SINGLE_VIDEO_DOWNLOAD_SKIPPED = 2

	def __init__(self, audioGUI, configMgr):
		"""
		
		:param audioGUI: used for unit testing only !
		"""
		self.configMgr = configMgr
		self.audioGUI = audioGUI
		self.audioDownloader = YoutubeDlAudioDownloader(self, audioDirRoot=configMgr.dataPath)
		
		self.stopDownloading = False
	
	def downloadSingleVideo(self,
	                        singleVideoUrl,
	                        singleVideoDownloadPath,
	                        originalSingleVideoTitle,
	                        modifiedVideoTitle=None):
		"""

		:param singleVideoUrl:              single video url
		:param singleVideoDownloadPath:     path where the playlist dir will be created
											or where the single video will be downloaded
		:param originalSingleVideoTitle:    if the playlistOrSingleVideoUrl points
											to a single video
		:param modifiedVideoTitle:          None if the video title was not modified
		"""
		self.stopDownloading = False

		self.audioDownloader.downloadSingleVideoForUrl(singleVideoUrl=singleVideoUrl,
		                                               originalVideoTitle=originalSingleVideoTitle,
		                                               modifiedVideoTitle=modifiedVideoTitle,
		                                               targetAudioDir=singleVideoDownloadPath)
	
	def downloadVideosReferencedInPlaylist(self,
	                                       downloadVideoInfoDic,
	                                       isIndexAddedToPlaylistVideo,
	                                       isUploadDateAddedToPlaylistVideo):
		"""
		In case we are downloading videos referenced in a playlist, this method first
		execute the download of the audio of the videos and then execute the extraction
		or suppression of audio parts as specified in the playlist title, this,
		provided we are on Windows (extraction/suppression are not supported on Android).

		Example of playlist title:
		playlist_title (s01:05:52-01:07:23 e01:15:52-E E01:35:52-01:37:23 S01:25:52-e) (s01:05:52-01:07:23 e01:15:52-e S01:25:52-e E01:35:52-01:37:23)
		-e or -E means "to end" !

		:param downloadVideoInfoDic:
		:param isUploadDateAddedToPlaylistVideo     parameter used for playlist only
		:param isIndexAddedToPlaylistVideo          parameter used for playlist only
		"""
		self.stopDownloading = False

		_, accessError = \
			self.audioDownloader.downloadPlaylistVideosForUrl(playlistUrl=downloadVideoInfoDic.getPlaylistUrl(),
			                                                  downloadVideoInfoDic=downloadVideoInfoDic,
			                                                  isUploadDateSuffixAddedToPlaylistVideo=isUploadDateAddedToPlaylistVideo,
			                                                  isDownloadDatePrefixAddedToPlaylistVideo=isIndexAddedToPlaylistVideo)
		
		# extracting/suppressing the audio portions for the downloaded audio tracks
		
		if accessError is None:
			if os.name == 'posix':
				msgText = 'skipping extraction/suppression on Android.\n'
				self.displayMessage(msgText)
			else:
				if not self.stopDownloading:
					# extraction/suppression possible only on Windows !
					audioDirRoot = self.configMgr.dataPath
					targetAudioDir = audioDirRoot + sep + downloadVideoInfoDic.getPlaylistDownloadSubDir()
					audioExtractor = AudioExtractor(self, targetAudioDir, downloadVideoInfoDic)
					audioExtractor.extractPlaylistAudio(downloadVideoInfoDic)
					
					# saving the content of the downloadVideoInfoDic which has been completed
					# by AudioExtractor in the directory containing the extracted audio files
					try:
						downloadVideoInfoDic.saveDic(audioDirRoot)
					except TypeError as e:
						print(e)
						traceback.print_exc()
	
	def getDownloadVideoInfoDicAndIndexDateSettingWarningMsg(self,
	                                                         playlistOrSingleVideoUrl,
	                                                         playlistOrSingleVideoDownloadPath,
	                                                         originalPlaylistTitle,
	                                                         modifiedPlaylistTitle,
	                                                         isIndexAddedToPlaylistVideo,
	                                                         isUploadDateAddedToPlaylistVideo):
		"""
		
		:param playlistOrSingleVideoUrl:
		:param playlistOrSingleVideoDownloadPath:   if the playlist is downloaded without
													modifying its download dir by clicking
													on the "Select or create dir" button,
													then the playlistDownloadRootPath is
													equal to the audioRootDir. Otherwise,
													its value is the dir selected or created
													where the playlist will be downloaded.
													In fact, audioRootDir + the selected or
													created sub-dir(s). For example:
													C:\\Users\\Jean-Pierre\\Downloads\\Audio\\
													zz\\UCEM\\Gary Renard
		:param originalPlaylistTitle:
		:param modifiedPlaylistTitle:
		:param isIndexAddedToPlaylistVideo:
		:param isUploadDateAddedToPlaylistVideo:
		:return:
		"""
		
		downloadVideoInfoDic = \
			self.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl=playlistOrSingleVideoUrl,
			                                             playlistOrSingleVideoDownloadPath=playlistOrSingleVideoDownloadPath,
			                                             originalPlaylistTitle=originalPlaylistTitle,
			                                             modifiedPlaylistTitle=modifiedPlaylistTitle)
		
		indexAndDateSettingWarningMsg = self.defineIndexAndDateSettingWarningMsg(
			downloadVideoInfoDic=downloadVideoInfoDic,
			isDownloadDatePrefixAddedToPlaylistVideo=isIndexAddedToPlaylistVideo,
			isUploadDateSuffixAddedToPlaylistVideo=isUploadDateAddedToPlaylistVideo)
		
		return downloadVideoInfoDic, indexAndDateSettingWarningMsg
	
	def clipAudioFile(self,
					  audioFilePathName,
					  clipStartHHMMSS,
					  clipEndHHMMSS,
					  floatSpeed=1.0):
		"""
		Extracts a portion of the audio file referred by the passed
		audioFilePathName.
		
		:param audioFilePathName:   the file which will be trimmed
		:param clipStartHHMMSS:     format = HH:MM:SS, 00:05:23
		:param clipEndHHMMSS:       format = HH:MM:SS, 00:07:21
		:param floatSpeed:          trimmed mp3 file speed modification
		
		:return:    the created (but not saved) DownloadVideoInfoDic which contains
					the clip information
		"""
		audioFileName = DirUtil.extractFileNameFromFilePathName(audioFilePathName)
		audioFilePath = DirUtil.extractPathFromPathFileName(audioFilePathName)
		videoTitle = audioFileName.split('.')[0]
		playlistDownloadRootPath = audioFilePath.replace(self.configMgr.dataPath + sep, '')
		playlistDownloadRootPathComponentLst = playlistDownloadRootPath.split(sep)
		playlistTitle = playlistDownloadRootPathComponentLst[-1]
		playlistDownloadRootPathWithoutPlaylistTitle = sep.join(playlistDownloadRootPathComponentLst[:-1])
		
		# initializing a partially filled DownloadVideoInfoDic with only the
		# information required by the AudioExtractor to split the audio file
		audioExtractorVideoInfoDic = DownloadPlaylistInfoDic(playlistUrl='',
		                                                     audioRootDir=self.configMgr.dataPath,
		                                                     playlistDownloadRootPath=playlistDownloadRootPathWithoutPlaylistTitle,
		                                                     modifiedPlaylistTitle=playlistTitle,
		                                                     modifiedPlaylistName=playlistTitle,
		                                                     loadDicIfDicFileExist=False)

		audioExtractorVideoInfoDic.addVideoInfoForVideoIndex(videoIndex=1,
															 videoTitle=videoTitle,
															 videoUrl='',
															 downloadedFileName=audioFileName)
		
		# getting the extract time frames specified as command line argument
		# and adding them to the DownloadVideoInfoDic
		startEndTimeFrame = clipStartHHMMSS + '-' + clipEndHHMMSS
		extractStartEndSecondsLists = [PlaylistTitleParser.convertToStartEndSeconds(startEndTimeFrame)]
		
		for extractStartEndSecondsList in extractStartEndSecondsLists:
			audioExtractorVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(1, extractStartEndSecondsList)
		
		# now trimming the audio file
		audioExtractor = AudioExtractor(audioController=self,
		                                targetAudioDir=audioFilePath,
		                                downloadVideoInfoDic=audioExtractorVideoInfoDic)
		
		audioExtractor.extractAudioPortions(videoIndex=1, downloadVideoInfoDic=audioExtractorVideoInfoDic,
		                                    floatSpeed=floatSpeed)
		
		return audioExtractorVideoInfoDic
	
	def getPlaylistTitleOrVideoTitleForUrl(self, url):
		"""
		Returns a playlistTitle or a videoTitle if the passed url points to a Youtube single
		video and an AccessError instance if the passed url does not contain a valid Youtube
		url.

		:param url: points either to a Youtube playlist or to a Youtube single video
					or is invalid since obtained from the clipboard.
		:return:    playlistTitle   if url points to a playlist or None otherwise,
					videoTitle      if url points to a single video or None otherwise,
					accessError     if the url is invalid (clipboard contained anything but
									a Youtube valid url
		"""
		playlistUrlTitleCachedDic = DownloadPlaylistInfoDic.getPlaylistUrlTitleCachedDic(self.configMgr.dataPath)

		playlistTitle = None
		videoTitle = None
		accessError = None
		
		try:
			playlistTitle = playlistUrlTitleCachedDic[url]
		except KeyError:
			pass
		
		if playlistTitle:
			return playlistTitle, videoTitle, accessError
		else:
			_, playlistTitle, videoTitle, accessError = \
				self.audioDownloader.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(url)
		
		if accessError:
			self.displayError(accessError.errorMsg)
		else:
			if playlistTitle:
				# here, the passed url points to a playlist which is not referenced
				# in the playlistUrlTitleCachedDic returned by the DownloadPlaylistInfoDic.
				# This means that DownloadPlaylistInfoDic must update the cached
				# url: playlist title dic.
				DownloadPlaylistInfoDic.updatePlaylistUrlTitleCachedDic(audioDirRoot=self.configMgr.dataPath,
				                                                        playlistUrl=url,
				                                                        playlistTitle=playlistTitle)
		
		return playlistTitle, videoTitle, accessError
	
	def getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(self, url):
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
		playlistObject, playlistTitle, videoTitle, accessError = \
			self.audioDownloader.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(url)
		
		if accessError:
			self.displayError(accessError.errorMsg)
			
		return playlistObject, playlistTitle, videoTitle, accessError
	
	def getDownloadVideoInfoDicForPlaylistTitle(self,
												playlistUrl,
												playlistOrSingleVideoDownloadPath,
												originalPlaylistTitle,
												modifiedPlaylistTitle):
		"""
		Returns a DownloadVideoInfoDic for the passed playlistTitle. The playlistTitle
		may contain extract / suppress info (ex: 'Test 3 short videos
		(e0:0:4-0:0:6 e0:0:12-e s0:0:1-0:0:3 s0:0:4-0:0:6 s0:0:9-e)$
		(s0:0:2-0:0:4 s0:0:5-0:0:7 s0:0:10-e) (e0:0:2-0:0:3 e0:0:5-e)'), info which will be
		added o the returned DownloadVideoInfoDic.

		:param playlistUrl:                         playlist url to add to the
													download video info div
		:param playlistOrSingleVideoDownloadPath:   if the playlist is downloaded without
													modifying its download dir by clicking
													on the "Select or create dir" button,
													then the playlistDownloadRootPath is
													equal to the audioRootDir. Otherwise,
													its value is the dir selected or created
													where the playlist will be downloaded.
													In fact, audioRootDir + the selected or
													created sub-dir(s). For example:
													C:\\Users\\Jean-Pierre\\Downloads\\Audio\\
													zz\\UCEM\\Gary Renard
		:param originalPlaylistTitle:
		:param modifiedPlaylistTitle:

		:return: downloadVideoInfoDic, accessError
		"""
		downloadVideoInfoDic, accessError = \
			PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(playlistUrl=playlistUrl,
																	  audioRootDir=self.configMgr.dataPath,
																	  playlistDownloadRootPath=playlistOrSingleVideoDownloadPath,
																	  originalPlaylistTitle=originalPlaylistTitle,
																	  modifiedPlaylistTitle=modifiedPlaylistTitle)
		
		if accessError:
			self.displayError(accessError.errorMsg)
			return None
		else:
			return downloadVideoInfoDic
	
	def displayVideoCurrentDownloadInfo(self, currentDownloadInfoTuple):
		"""
		Method called every n seconds by
		YoutubeDlDownloadInfoExtractor.ydlCallableHook() which is hooked in
		YoutubeDL options.
		
		:param currentDownloadInfoTuple:    3 elements tuple containing current
											download size in bytes, download size
											percent string and current download
											speed string (in KiB/s)
		"""
		self.audioGUI.displayVideoCurrentDownloadInfo(currentDownloadInfoTuple)
	
	def displayVideoEndDownloadInfo(self, endDownloadInfoLst):
		"""
		Method called when the video download is finished by
		YoutubeDlDownloadInfoExtractor.ydlCallableHook() which is hooked in
		YoutubeDL options.

		:param endDownloadInfoLst:  2 elements list containing final download
									size in bytes and total download time in
									seconds
		"""
		downloadTime = endDownloadInfoLst[1]
		
		if downloadTime is None:
			# the case for some videos on Android Maybe for videos which were
			# almost fully partially downloaded ...
			hhmmssStr = '?'
		else:
			hhmmssStr = datetime.timedelta(seconds=int(downloadTime))
	
		endDownloadInfoLst[1] = hhmmssStr
		
		self.audioGUI.displayVideoEndDownloadInfo(endDownloadInfoLst)
	
	def displayPlaylistEndDownloadInfo(self, endDownloadInfoLst):
		"""
		Method called when the playlist videos download is finished by
		YoutubeDlAudioDownloader.downloadPlaylistVideosForUrl().

		:param endDownloadInfoLst:  5 elements list containing number of
									videos successfully downloaded, number od
									video download failure, number of
									video download skipped, playlist total
									download size in bytes and playlist total
									download time in seconds
		"""
		downloadTime = endDownloadInfoLst[4]
		
		if downloadTime is None:
			# the case for some videos on Android Maybe for videos which were
			# almost fully partially downloaded ...
			hhmmssStr = '?'
		else:
			hhmmssStr = datetime.timedelta(seconds=int(downloadTime))
		
		endDownloadInfoLst[4] = hhmmssStr
		
		self.audioGUI.displayPlaylistEndDownloadInfo(endDownloadInfoLst)
	
	def displaySingleVideoEndDownloadInfo(self,
	                                      msgText,
	                                      singleVideoDownloadStatus):
		"""
		Method called when the single video download is finished by
		YoutubeDlAudioDownloader.downloadSingleVideoForUrl().

		:param msgText:                     contains the single video title and the download dir.
		:param singleVideoDownloadStatus:   SINGLE_VIDEO_DOWNLOAD_SUCCESS or
											SINGLE_VIDEO_DOWNLOAD_FAIL
											SINGLE_VIDEO_DOWNLOAD_SKIPPED

		"""
		self.audioGUI.displaySingleVideoEndDownloadInfo(msgText=msgText,
		                                                singleVideoDownloadStatus=singleVideoDownloadStatus)
	
	def displayMessage(self, msgText):
		self.audioGUI.outputResult(msgText)
	
	def displayVideoDownloadStartMessage(self, msgText):
		self.audioGUI.displayVideoDownloadStartMessage(msgText)
	
	def displayError(self, msg):
		self.audioGUI.outputResult(msg)

	def displayVideoDownloadEndMessage(self, msg):
		self.audioGUI.displayVideoDownloadEndMessage(msg)
		
	# method temporary here. Will be suppressed !
	def getPrintableResultForInput(self, inputStr, copyResultToClipboard=True):
		'''
		Return the printable request result, the full request command without any command option and
		the full request command with any specified save mode option (option which is to be saved in the
		command history list.
	
		:param inputStr:
		:param copyResultToClipboard: set to True by default. Whreplaying all requests
									  stored in history, set to False, which avoids
									  problem on Android
		:seqdiag_return printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions
	
		:return: 1/ printable request result
				 2/ full request command without any command option
				 3/ full request command with any non save command option
				 4/ full request command with any specified save mode option, None if no save mode option
					is in effect
	
				 Ex: 1/ 0.1 ETH/36 USD on Bitfinex: 21/11/17 10:00 360
					 2/ eth usd 0 bitfinex
					 3/ None (value command with save mode in effect !)
					 4/ eth usd 0 bitfinex -vs0.1eth
	
					 1/ 0.1 ETH/36 USD on Bitfinex: 21/11/17 10:00 360
					 2/ eth usd 0 bitfinex
					 3/ eth usd 0 bitfinex -v0.1eth
					 4/ None (no value command save option in effect)
	
					 1/ ETH/USD on Bitfinex: 21/11/17 10:00 360
					 2/ eth usd 0 bitfinex
					 3/ None (no value command in effect)
					 4/ None (no value command save option in effect)
		'''
		return inputStr, inputStr, inputStr, inputStr, inputStr

	def extractAudioFromVideoFile(self, videoFilePathName):
		"""
		Extract the audio from the passed video file path name.
		
		:param videoFilePathName:
		
		:return: the extracted audio mp3 file path name
		"""
		audioExtractor = AudioExtractor(audioController=self,
		                                targetAudioDir=videoFilePathName,
		                                downloadVideoInfoDic={})
		
		return audioExtractor.extractAudioFromVideoFile(videoFilePathName)

	def downloadStopped(self):
		"""
		Method called by YoutubeDlAudioDownloader.downloadVideosReferencedInPlaylistForPlaylistUrl()
		after the playlist current download has been interrupted.
		"""
		self.audioGUI.downloadStopped()
	
	def displayVideoMp3ConversionCurrentInfo(self, videoCurrentMp3ConversionInfoList):
		"""
		Method called every n seconds by a new SepThreadExec instance created
		and started once the video download is finished by
		YoutubeDlDownloadInfoExtractor.ydlCallableHook() which is hooked in
		YoutubeDL options.

		:param videoCurrentMp3ConversionInfoList:   1 element list containing current
													conversion time in seconds.
		"""
		mp3ConversionTime = videoCurrentMp3ConversionInfoList[0]
		
		if mp3ConversionTime is None:
			# the case for some videos on Android Maybe for videos which were
			# almost fully partially downloaded ...
			hhmmssStr = '?'
		else:
			hhmmssStr = datetime.timedelta(seconds=int(mp3ConversionTime))
		
		videoCurrentMp3ConversionInfoList[0] = hhmmssStr

		self.audioGUI.displayVideoMp3ConversionCurrentInfo(videoCurrentMp3ConversionInfoList)
	
	def deleteAudioFilesFromDirAndFromDic(self, filePathNameLst):
		"""
		Called by AudioDownloaderGUI.deleteAudioFilesFromDirAndFromDic().
		
		Delete the files listed in the passed filePathNameLst and remove
		their corresponding entry in the relevant playlist dic file.

		:param filePathNameLst:
		"""
		
		# deleting audio files
		
		# the first element in the list is the playlist dir path ...
		deletedFilesPath = DirUtil.extractPathFromPathFileName(filePathNameLst[-1])
		
		if deletedFilesPath == self.configMgr.dataPath:
			# the case if a playlist dir in audio root path was selected instead
			# a playlist audio file inside the playlist dir
			return
		
		DirUtil.deleteFiles(filePathNameLst)
		
		# now removing video entries in download video info dic
		
		dicFilePathNameLst = DirUtil.getFilePathNamesInDirForPattern(
			deletedFilesPath, '*' + DownloadPlaylistInfoDic.DIC_FILE_NAME_EXTENT)
		
		if len(dicFilePathNameLst) > 0:
			# the file deletion is done in a playlist dir, not in a
			# single videos dir
			downloadVideoInfoDic = DownloadPlaylistInfoDic(existingDicFilePathName=dicFilePathNameLst[0])
			
			# deleting corresponding video entries in downloadVideoInfoDic
			
			for filePathName in filePathNameLst:
				fileName = DirUtil.extractFileNameFromFilePathName(filePathName)
				downloadVideoInfoDic.deleteVideoInfoForVideoFileName(fileName)
	
			downloadVideoInfoDic.saveDic(audioDirRoot=self.configMgr.dataPath)

	def getDownloadPlaylistInfoDic(self,
	                               playlistName):
		'''
		Load the existing download video info dic for the passed playlist name.
		
		:param playlistName:
		
		:return: None if no DownloadPlaylistInfoDic exist in the passed playlistName
				 dir (currently the case for the audio\Various dir)
		'''
		dicFilePathName = self.configMgr.dataPath + sep + playlistName + sep + playlistName + DownloadPlaylistInfoDic.DIC_FILE_NAME_EXTENT
		downloadPlaylistInfoDic = DownloadPlaylistInfoDic(existingDicFilePathName=dicFilePathName)
		
		if downloadPlaylistInfoDic.dic is None:
			# currently the case if we try to load a DownloadPlaylistInfoDic located
			# in the audio\Various dir
			downloadPlaylistInfoDic = None
		
		return downloadPlaylistInfoDic
	
	def deleteAudioFilesFromDirOnly(self, delFileDic):
		"""
		Called by AudioDownloaderGUI.deleteSelectedAudioDownloadedFiles().

		Delete the files listed in the passed delFileDic without removing
		their corresponding entry from the relevant playlist dic file.

		:param  delFileDic: dictionary with key == playlist name and value == list
				of audio file to delete names contained in the playlist dir. Ex:
				{'Politique': ['220324-Nouveau document texte.mp3',
							   'Nouveau document texte.mp3'],
				 'EMI':       ['211224-Nouveau document texte jjjhmhfhmgfj zkuztuz.mp3']}
				 
		:return:    deletedFileNameLst
		"""
		
		# deleting audio files
		audioRoot = self.configMgr.dataPath
		
		deletedFileNameLst, deletedFilePathNameLst = DirUtil.deleteAudioFiles(audioRootPath=audioRoot,
		                                                                      delFileDic=delFileDic)
		
		self.audioGUI.displayDeletedAudioFiles(deletedFilePathNameLst)

		return deletedFileNameLst
	
	def defineIndexAndDateSettingWarningMsg(self,
	                                        downloadVideoInfoDic,
	                                        isDownloadDatePrefixAddedToPlaylistVideo,
	                                        isUploadDateSuffixAddedToPlaylistVideo):
		"""
		According to the value of the passed boolean params isIndexAddedToPlaylistVideo,
		isUploadDateAddedToPlaylistVideo which represent how the user set the index
		and upload date suffix checkbox on the ConfirmDownloadPopup, this method returns
		the messages listed below which will be displayed by the YesNoPopup.
		
		Returnable messages:
		
		Playlist directory does not exist. Continue with adding download date prefix and upload date suffix ?
		Playlist directory does not exist. Continue with adding index ?
		Playlist directory does not exist. Continue with adding upload date suffix ?
		
		Playlist directory is empty. Continue with with adding download date prefix and upload date suffix ?
		Playlist directory is empty. Continue with with adding index ?
		Playlist directory is empty. Continue with with adding upload date suffix ?
		
		Currently, index is not used. Continue with adding index ?
		Currently, index is used. Continue without adding index ?
		Currently, upload date suffix is not used. Continue with adding date ?
		Currently, upload date suffix is used. Continue without adding date ?
		
		:param downloadVideoInfoDic:
		:param isDownloadDatePrefixAddedToPlaylistVideo:
		:param isUploadDateSuffixAddedToPlaylistVideo:
		:return:
		"""
		warningMsg = ''
		indexAndDateUsageLst = \
			self.getIndexAndDateUsageLstForPlaylist(playlistDownloadVideoInfoDic=downloadVideoInfoDic)
		
		if indexAndDateUsageLst is None:
			# the case if the passed playlistOrSingleVideoDownloadPath does
			# not exist.
			warningMsgStart = 'Playlist directory does not exist. Continue with '

			if isDownloadDatePrefixAddedToPlaylistVideo and isUploadDateSuffixAddedToPlaylistVideo:
				warningMsg = warningMsgStart + 'adding download date prefix and upload date suffix ?'
			elif isDownloadDatePrefixAddedToPlaylistVideo:
				warningMsg = warningMsgStart + 'adding download date prefix ?'
			elif isUploadDateSuffixAddedToPlaylistVideo:
				warningMsg = warningMsgStart + 'adding upload date suffix ?'
			
			return warningMsg

		if indexAndDateUsageLst == []:
			# the case if the passed playlistOrSingleVideoDownloadPath is
			# empty.
			warningMsgStart = 'Playlist directory is empty. Continue with '
			
			if isDownloadDatePrefixAddedToPlaylistVideo and isUploadDateSuffixAddedToPlaylistVideo:
				warningMsg = warningMsgStart + 'adding download date prefix and upload date suffix ?'
			elif isDownloadDatePrefixAddedToPlaylistVideo:
				warningMsg = warningMsgStart + 'adding download date prefix ?'
			elif isUploadDateSuffixAddedToPlaylistVideo:
				warningMsg = warningMsgStart + 'adding upload date suffix ?'
			
			return warningMsg
		
		if isDownloadDatePrefixAddedToPlaylistVideo:
			if not indexAndDateUsageLst[DirUtil.DOWNLOAD_DATE_UPLOAD_DATE_POS] and \
				not indexAndDateUsageLst[DirUtil.DOWNLOAD_DATE_NO_UPLOAD_DATE_POS]:
				warningMsg += 'Currently, download date prefix is not used. Continue with adding download date prefix ?\n'
		else:
			if indexAndDateUsageLst[DirUtil.DOWNLOAD_DATE_UPLOAD_DATE_POS] or \
				indexAndDateUsageLst[DirUtil.DOWNLOAD_DATE_NO_UPLOAD_DATE_POS]:
				warningMsg += 'Currently, download date prefix is used. Continue without adding download date prefix ?\n'

		if isUploadDateSuffixAddedToPlaylistVideo:
			if not indexAndDateUsageLst[DirUtil.DOWNLOAD_DATE_UPLOAD_DATE_POS] and \
				not indexAndDateUsageLst[DirUtil.NO_DOWNLOAD_DATE_UPLOAD_DATE_POS]:
				warningMsg += 'Currently, upload date suffix is not used. Continue with adding date suffix ?'
		else:
			if indexAndDateUsageLst[DirUtil.DOWNLOAD_DATE_UPLOAD_DATE_POS] or \
				indexAndDateUsageLst[DirUtil.NO_DOWNLOAD_DATE_UPLOAD_DATE_POS]:
				warningMsg += 'Currently, upload date suffix is used. Continue without adding date suffix ?'

		return warningMsg.strip() # strip() removes last '\n' !
	
	def getIndexAndDateUsageLstForPlaylist(self, playlistDownloadVideoInfoDic):
		"""
		If the playlist audioDir is empty, then [] is returned.
		If the playlist audioDir does not exist, then None is returned.
		Else, see below.

		:param playlistDownloadVideoInfoDic:
		
		:return:indexAndDateUsageLst    four boolean elements list or
										None if the passed audioDir does not
										exist or
										[] if the passed audioDir is empty.

										four elements list:  [DOWNLOAD_DATE_UPLOAD_DATE_POS boolean,
															 DOWNLOAD_DATE_NO_UPLOAD_DATE_POS boolean,
															 NO_DOWNLOAD_DATE_UPLOAD_DATE_POS boolean,
															 NO_DOWNLOAD_DATE_NO_UPLOAD_DATE_POS boolean]
	
										the list index are defined by those DirUtil
										constants:
										
										DirUtil.DOWNLOAD_DATE_UPLOAD_DATE_POS = 0
										DirUtil.DOWNLOAD_DATE_NO_UPLOAD_DATE_POS = 1
										DirUtil.NO_DOWNLOAD_DATE_UPLOAD_DATE_POS = 2
										DirUtil.NO_DOWNLOAD_DATE_NO_UPLOAD_DATE_POS = 3
		"""
		playlistDownloadDir = self.configMgr.dataPath + sep + playlistDownloadVideoInfoDic.getPlaylistDownloadSubDir()
		indexAndDateUsageLst = DirUtil.getIndexAndDateUsageInDir(playlistDownloadDir)
		
		return indexAndDateUsageLst

	def getAudioFilesSortedByDateInfoList(self,
	                                      excludedSubDirNameLst=[]):
		"""
		Returns a list of sub-lists formatted according to this model:
		
		[
			[<audio sub-dir name 1>, [
					[<audio file name 1>, <yymmdd download date>],
					[<audio file name 2>, <yymmdd download date>]
				]
			],
			[<audio sub-dir name 2>, [
					[<audio file name 1>, <yymmdd download date>],
					[<audio file name 2>, <yymmdd download date>]
				]
			]
		]
		
		Example:
		
		[
			['JMJ', [
					['200310-exploreAudio.mp3', '220219'],
					['Here to help - Give him what he wants.mp3', '220219']
				]
			],
			['Crypto', [
					['98-Here to help - Give him what he wants.mp3', '220219'],
					['Funny suspicious looking dog.mp3', '220219']
				]
			]
		]
		
		:param excludedSubDirNameLst: [<sub-dir name 1>, <sub-dir name 1>, ...]
		
		:return: see above
		"""
		return DirUtil.getAudioFilesSortedByDateInfoList(targetDir=self.configMgr.dataPath,
		                                                 excludedSubDirNameLst=excludedSubDirNameLst)

	def deleteAudioFilesOlderThanPlaylistDicFile(self,
	                                             downloadPlaylistInfoDic):
		
		playlistDir = self.configMgr.dataPath + sep + downloadPlaylistInfoDic.getPlaylistDownloadSubDir()
		playlistDicFileName = self._getPlaylistDicFileName(playlistDir)
		
		if playlistDicFileName:
			fileNameLstBefore, filePathNameLstBefore, _, _ = DirUtil.getListOfFilesCreatedOrModifiedBeforeOrAfterRefFileDate(
				playlistDir, playlistDicFileName)
			DirUtil.deleteFiles(filePathNameLstBefore)
	
	def _getPlaylistDicFileName(self, playlistDir):
		playlistDicFileNameLst = DirUtil.getFileNamesInDirForPattern(playlistDir, '*' + DownloadPlaylistInfoDic.DIC_FILE_NAME_EXTENT)
		
		if len(playlistDicFileNameLst) == 1:
			return playlistDicFileNameLst[0]
		else:
			return None


if __name__ == "__main__":
	controller = AudioController()
