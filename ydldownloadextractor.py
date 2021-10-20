import time

PRINT_SECONDS = 1


class YdlDownloadInfoExtractor:
	def __init__(self):
		self.lstExtractTime = time.time()
	
	def ydlCallableHook(self, response):
		if response['status'] == 'downloading':
			now = time.time()
			if now - self.lstExtractTime >= PRINT_SECONDS:
				print(
					'download bytes {}: {} %. Speed: {}'.format(response["downloaded_bytes"], response["_percent_str"],
					                                            response["_speed_str"]))
				self.lstExtractTime = now
		elif response['status'] == 'finished':
			print('total download bytes {}. Now, converting to mp3 ...'.format(response["total_bytes"]))
