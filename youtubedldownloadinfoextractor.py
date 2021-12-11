import time
from septhreadexec import SepThreadExec

DISPLAY_VIDEO_DOWNLOAD_TIME_EVERY_N_SECONDS = 1
DISPLAY_VIDEO_MP3_CONVERSION_TIME_EVERY_N_SECONDS = 1


class YoutubeDlDownloadInfoExtractor:
	"""
	This class does display every n seconds the current status of downloading
	the video and of its conversion to mp3 file.
	
	Since the youtube_dl options on Windows are now the same as on Android, the
	mp3 conversion which took time on Windows does no longer happens and so
	displaying the conversion to mp3 file status no longer executed on Windows.
	"""
	def __init__(self, audioDownloader, audioController):
		self.audioDownloader = audioDownloader
		self.audioController = audioController
		self.videoDownloadStartTime = None
		self.lstDisplayedVideoDownloadTime = None
		self.playlistTotalDownloadSize = 0

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
		"""
		Method called by a new SepThreadExec instance created and started once
		the video download is finished by
		YoutubeDlDownloadInfoExtractor.ydlCallableHook() which is hooked in
		YoutubeDL options.
		"""
		conversionSeconds = 0
		
		while self.audioDownloader.convertingVideoToMp3:
			if conversionSeconds > 0:
				self.audioController.displayVideoMp3ConversionCurrentInfo([conversionSeconds, ])

			time.sleep(DISPLAY_VIDEO_MP3_CONVERSION_TIME_EVERY_N_SECONDS)
			conversionSeconds += DISPLAY_VIDEO_MP3_CONVERSION_TIME_EVERY_N_SECONDS
