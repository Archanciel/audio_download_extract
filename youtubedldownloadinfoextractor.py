import time

PRINT_SECONDS = 1


class YoutubeDlDownloadInfoExtractor:
	def __init__(self, audioController):
		self.audioController = audioController
		self.downloadStartTime = None
		self.lstExtractTime = None
	
	def ydlCallableHook(self, response):
		if response['status'] == 'downloading':
			now = time.time()
			if self.downloadStartTime is None:
				self.downloadStartTime = now
				self.lstExtractTime = now
			if now - self.lstExtractTime >= PRINT_SECONDS:
				self.audioController.displayCurrentDownloadInfo((response["downloaded_bytes"],
				                                                 response["_percent_str"],
				                                                 response["_speed_str"]))
				self.lstExtractTime = now
		elif response['status'] == 'finished':
			self.audioController.displayEndDownloadInfo([response["total_bytes"],
			                                             time.time() - self.downloadStartTime])
			self.downloadStartTime = None
			
