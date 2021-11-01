import time

DISPLAY_VIDEO_DOWNLOAD_TIME_EVERY_N_SECONDS = 1


class YoutubeDlDownloadInfoExtractor:
	def __init__(self, audioController):
		self.audioController = audioController
		self.videoDownloadStartTime = None
		self.lstDisplayedVideoDownloadTime = None
	
	def ydlCallableHook(self, response):
		if response['status'] == 'downloading':
			now = time.time()
			if self.videoDownloadStartTime is None:
				# new playlist video starts downloading
				self.videoDownloadStartTime = now
				self.lstDisplayedVideoDownloadTime = now
			if now - self.lstDisplayedVideoDownloadTime >= DISPLAY_VIDEO_DOWNLOAD_TIME_EVERY_N_SECONDS:
				self.audioController.displayCurrentDownloadInfo((response["downloaded_bytes"],
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
			
			self.audioController.displayEndDownloadInfo([response["total_bytes"],
			                                             videoTotalDownloadTime
			                                             ])
			self.videoDownloadStartTime = None
			
