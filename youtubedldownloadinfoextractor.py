import time
from septhreadexec import SepThreadExec

DISPLAY_VIDEO_DOWNLOAD_TIME_EVERY_N_SECONDS = 1
DISPLAY_VIDEO_MP3_CONVERSION_TIME_EVERY_N_SECONDS = 1


class YoutubeDlDownloadInfoExtractor:
	def __init__(self, audioDownloader, audioController):
		self.audioDownloader = audioDownloader
		self.audioController = audioController
		self.videoDownloadStartTime = None
		self.lstDisplayedVideoDownloadTime = None
		self.playlistTotalDownloadSize = 0
		self.videoMp3ConversionStartTime = None
		self.lstDisplayedVideoMp3ConversionTime = None

	def ydlCallableHook(self, response):
		isVideoDownloadFinished = False
		
		if response['status'] == 'downloading':
			now = time.time()
			if self.videoDownloadStartTime is None:
				# new playlist video starts downloading
				self.videoDownloadStartTime = now
				self.lstDisplayedVideoDownloadTime = now
			if now - self.lstDisplayedVideoDownloadTime >= DISPLAY_VIDEO_DOWNLOAD_TIME_EVERY_N_SECONDS:
				self.audioController.displayVideoCurrentDownloadInfo((response["downloaded_bytes"],
				                                                      response["_percent_str"],
				                                                      response["_speed_str"]))
				self.lstDisplayedVideoDownloadTime = now
		elif response['status'] == 'finished':
			if self.videoDownloadStartTime is None:
				# happens for some videos on Android. Maybe for videos which were
				# almost fully partially downloaded ...
				videoTotalDownloadTime = None
			else:
				videoTotalDownloadTime = time.time() - self.videoDownloadStartTime
			
			videoTotalDownloadSize = response["total_bytes"]
			self.playlistTotalDownloadSize += videoTotalDownloadSize
			self.audioController.displayVideoEndDownloadInfo([videoTotalDownloadSize,
			                                                  videoTotalDownloadTime
			                                                  ])
			self.videoDownloadStartTime = None
			isVideoDownloadFinished = True
			
		if isVideoDownloadFinished:
			self.audioDownloader.convertingVideoToMp3 = True
			sepThreadExec = SepThreadExec(callerGUI=self,
			                              func=self.displayVideoMp3ConversionInfo)
			sepThreadExec.start()
			
	def initPlaylistDownloadInfo(self):
		self.playlistTotalDownloadSize = 0

	def getPlaylistDownloadInfo(self):
		return (self.playlistTotalDownloadSize,)
	
	def displayVideoMp3ConversionInfo(self):
		while self.audioDownloader.convertingVideoToMp3:
			now = time.time()
			
			if self.videoMp3ConversionStartTime is None:
				# new video to mp3 conversion starts
				self.videoMp3ConversionStartTime = now
				self.lstDisplayedVideoMp3ConversionTime = now
			
			if now - self.lstDisplayedVideoMp3ConversionTime >= DISPLAY_VIDEO_MP3_CONVERSION_TIME_EVERY_N_SECONDS:
				self.audioController.displayVideoMp3ConversionInfo((now - self.videoMp3ConversionStartTime,))
				self.lstDisplayedVideoMp3ConversionTime = now
		
		self.videoMp3ConversionStartTime = None