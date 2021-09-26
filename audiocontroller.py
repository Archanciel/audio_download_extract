from os.path import sep
import traceback

from constants import *
from downloadvideoinfodic import DownloadVideoInfoDic
from youtubedlaudiodownloader import YoutubeDlAudioDownloader
from dirutil import DirUtil

if os.name == 'posix':
	# sound file extraction is not possible on Android
	pass
else:
	from audioextractor import AudioExtractor

from playlisttitleparser import PlaylistTitleParser

class AudioController:
	def __init__(self, audioGUI, configMgr):
		"""
		
		:param audioGUI: used for unit testing only !
		"""
		self.configMgr = configMgr
		self.audioGUI = audioGUI
		self.audioDownloader = YoutubeDlAudioDownloader(self, audioDirRoot=configMgr.dataPath)
		
	def downloadVideosReferencedInPlaylistOrSingleVideo(self, url, playlistTitle, singleVideoTitle):
		'''
		In case we are downloading videos referenced in a playlist, this method first
		execute the download of the audio of the videos and then execute the extraction
		or suppression of audio parts as specified in the playlist title, this,
		provided we are on Windows (extraction/suppression are not supported on Android).
		
		Example of playlist title:
		playlist_title (s01:05:52-01:07:23 e01:15:52-E E01:35:52-01:37:23 S01:25:52-e) (s01:05:52-01:07:23 e01:15:52-e S01:25:52-e E01:35:52-01:37:23)
		-e or -E means "to end" !

		If we are downloading a single video audio, no extraction/suppression will
		be performed.

		:param url: playlist or single video url
		:param downloadVideoInfoDic: if url points to a playlist
		:param singleVideoTitle: if the url points to a single video
		'''
		if playlistTitle is not None:
			# downloading a playlist
			downloadVideoInfoDic = \
				self.getDownloadVideoInfoDicForPlaylistTitle(playlistTitle)

			_, accessError = self.audioDownloader.downloadVideosReferencedInPlaylistForPlaylistUrl(url, downloadVideoInfoDic)
			
			# extracting/suppressing the audio portions for the downloaded audio tracks
	
			if accessError is None:
				if os.name == 'posix':
					msgText = 'skipping extraction/suppression on Android.\n'
					self.displayMessage(msgText)
				else:
					# extraction/suppression possible only on Windows !
					audioDirRoot = self.configMgr.dataPath
					targetAudioDir = audioDirRoot + sep + downloadVideoInfoDic.getPlaylistDownloadDir()
					audioExtractor = AudioExtractor(self, targetAudioDir, downloadVideoInfoDic)
					audioExtractor.extractPlaylistAudio(downloadVideoInfoDic)
				
					# saving the content of the downloadVideoInfoDic which has been completed
					# by AudioExtractor in the directory containing the extracted audio files
					try:
						downloadVideoInfoDic.saveDic(audioDirRoot)
					except TypeError as e:
						print(e)
						traceback.print_exc()
		else:
			# downloading a single video in the single video default dir
			self.audioDownloader.downloadSingleVideoForUrl(url, singleVideoTitle, self.configMgr.singleVideoDataPath)
	
	def clipAudioFile(self,
	                  audioFilePathName,
	                  clipStartHHMMSS,
	                  clipEndHHMMSS,
	                  floatSpeed=1.0):
		"""
		Extracts a portion of the audio file referred by the passed audioFilePathName.
		
		:param audioFilePathName:   the file which will be trimmed
		:param clipStartHHMMSS:     format = HH:MM:SS, 00:05:23
		:param clipEndHHMMSS:       format = HH:MM:SS, 00:07:21
		:param floatSpeed:          trimmed mp3 file speed modification
		
		:return:    the created (but not saved) DownloadVideoInfoDic which contains
					the clip information
		"""
		audioFileName = DirUtil.extractFileNameFromPathFileName(audioFilePathName)
		audioFileFullDir = DirUtil.extractPathFromPathFileName(audioFilePathName)
		videoTitle = audioFileName.split('.')[0]
		playlistTitleAndName = audioFileFullDir.replace(self.configMgr.dataPath + sep, '')
		
		# initializing a partially filled DownloadVideoInfoDic with only the
		# information required by the AudioExtractor to split the audio file
		audioExtractorVideoInfoDic = DownloadVideoInfoDic(audioDirRoot=self.configMgr.dataPath,
		                                                  playlistTitle=playlistTitleAndName,
		                                                  playlistName=playlistTitleAndName,
		                                                  loadDicIfExist=False)

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
		                                targetAudioDir=audioFileFullDir,
		                                downloadVideoInfoDictionary=audioExtractorVideoInfoDic)
		
		audioExtractor.extractAudioPortions(videoIndex=1,
											videoFileName=audioFileName,
											downloadVideoInfoDic=audioExtractorVideoInfoDic,
											floatSpeed=floatSpeed)
		
		return audioExtractorVideoInfoDic
	
	def getPlaylistObjectAndTitlesForUrl(self, url):
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
		playlistObject, playlistTitle, videoTitle, accessError = self.audioDownloader.getPlaylistObjectAndTitlesFortUrl(url)
		
		if accessError:
			self.displayError(accessError.errorMsg)
			
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
		downloadVideoInfoDic, accessError = self.audioDownloader.getDownloadVideoInfoDicForPlaylistTitle(playlistTitle)
		
		if accessError:
			self.displayError(accessError.errorMsg)
			return None
		
		return downloadVideoInfoDic
	
	def displayMessage(self, msgText):
		self.audioGUI.outputResult(msgText)
	
	def displayError(self, msg):
		self.audioGUI.outputResult(msg)

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
		audioExtractor = AudioExtractor(self, videoFilePathName, {})
		
		return audioExtractor.extractAudioFromVideoFile(videoFilePathName)


if __name__ == "__main__":
	downloader = AudioController()
	downloader.downloadPlaylistAudio()
