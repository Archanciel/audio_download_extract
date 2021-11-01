import time

DISPLAY_VIDEO_DOWNLOAD_TIME_EVERY_N_SECONDS = 1


class YoutubeDlDownloadInfoExtractor:
	def __init__(self, audioController):
		self.audioController = audioController
		self.videoDownloadStartTime = None
		self.lstDisplayedVideoDownloadTime = None
		self.playlistTotalDownloadSize = 0
	
	def ydlCallableHook(self, response):
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
			
	def initPlaylistDownloadInfo(self):
		self.playlistTotalDownloadSize = 0

	def getPlaylistDownloadInfo(self):
		return (self.playlistTotalDownloadSize,)