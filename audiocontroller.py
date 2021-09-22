import traceback

from constants import *
from downloadvideoinfodic import DownloadVideoInfoDic
from youtubedlaudiodownloader import YoutubeDlAudioDownloader

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
		self.audioDownloader = YoutubeDlAudioDownloader(self, configMgr.dataPath)
		
	def downloadVideosReferencedInPlaylistOrSingleVideo(self, url, downloadVideoInfoDic, singleVideoTitle):
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
		if downloadVideoInfoDic:
			# downloading a playlist
			_, accessError = self.audioDownloader.downloadVideosReferencedInPlaylistForPlaylistUrl(url, downloadVideoInfoDic)
			
			# extracting/suppressing the audio portions for the downloaded audio tracks
	
			if accessError is None:
				if os.name == 'posix':
					msgText = 'skipping extraction/suppression on Android.\n'
					self.displayMessage(msgText)
				else:
					# extraction/suppression possible only on Windows !
					targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()
					audioExtractor = AudioExtractor(self, targetAudioDir, downloadVideoInfoDic)
					audioExtractor.extractPlaylistAudio(downloadVideoInfoDic)
				
					# saving the content of the downloadVideoInfoDic which has been completed
					# by AudioExtractor in the directory containing the extracted audio files
					try:
						downloadVideoInfoDic.saveDic()
					except TypeError as e:
						print(e)
						traceback.print_exc()
		else:
			# downloading a single video in the single video default dir
			self.audioDownloader.downloadSingleVideoForUrl(url, singleVideoTitle, self.configMgr.singleVideoDataPath)
	
	def trimAudioFile(self,
	                  audioFilePathName,
	                  trimStartHHMMSS,
	                  trimEndHHMMSS,
	                  floatSpeed=1.0):
		"""
		
		:param audioFilePathName: the file which will be trimmed
		:param trimStartHHMMSS:
		:param trimEndHHMMSS:
		:param floatSpeed: trimmed mp3 file speed modification
		
		:return: the trimmed file pathname
		"""
		audioFileName = audioFilePathName.split(DIR_SEP)[-1]
		audioFileDir = audioFilePathName.replace(DIR_SEP + audioFileName, '')
		
		# initializing a partially filled DownloadVideoInfoDic with only the informations
		# required to trim the audio file
		downloadVideoInfoDic = DownloadVideoInfoDic(audioFileDir)
		downloadVideoInfoDic.addVideoInfoForVideoIndex(1, audioFileName.split('.')[0],
		                                               '', audioFileName)
		
		# getting the extract time frames specified as command line argument
		# and adding them to the DownloadVideoInfoDic
		startEndTimeFrame = trimStartHHMMSS + '-' + trimEndHHMMSS
		extractStartEndSecondsLists = [PlaylistTitleParser.convertToStartEndSeconds(startEndTimeFrame)]
		
		for extractStartEndSecondsList in extractStartEndSecondsLists:
			downloadVideoInfoDic.addExtractStartEndSecondsListForVideoIndex(1, extractStartEndSecondsList)
		
		# now trimming the audio file
		audioExtractor = AudioExtractor(self, audioFileDir, downloadVideoInfoDic)
		audioExtractor.extractAudioPortions(videoIndex=1,
		                                    videoFileName=audioFileName,
		                                    downloadVideoInfoDic=downloadVideoInfoDic,
		                                    floatSpeed=floatSpeed)
		
		return downloadVideoInfoDic
	
	def getDownloadVideoInfoDicOrSingleVideoTitleFortUrl(self, url):
		"""
		As the passed URL points either to a playlist or to a single video, the
		method returns either a DownloadVideoInfoDic in case of playlist URL or
		None and a video title in case of single video URL.
		
		:param url: playlist or single video url
		
		:return: downloadVideoInfoDic, videoTitle, accessError
		"""
		downloadVideoInfoDic, videoTitle, accessError = self.audioDownloader.getDownloadVideoInfoDicOrSingleVideoTitleFortUrl(url)
		
		if accessError:
			self.displayMessage(accessError.errorMsg)
			return None, None, accessError
		
		return downloadVideoInfoDic, videoTitle, accessError
	
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
