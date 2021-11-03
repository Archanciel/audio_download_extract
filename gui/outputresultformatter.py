from constants import *

class OutputResultFormatter:
	def buildOutputResultStr(self, msgType, msgArgTuple):
		resultStr = ''
		
		if msgType == MSG_TYPE_STOP_DOWNLOADING:
			resultStr = '[b]{}[/b] playlist audio(s) download interrupted.\n'.format(msgArgTuple[0])
		elif msgType == MSG_TYPE_ATTRIBUTE_ERROR_VIDEO_TITLE:
			resultStr = 'obtaining video title failed with error {}.\n'.format(msgArgTuple[0])
		elif msgType == MSG_TYPE_DISPLAY_RETRY_DOWNLOAD:
			resultStr = 'retry downloading the playlist later to download the failed audio only ...\n'
		elif msgType == MSG_TYPE_AUDIO_ALREADY_DOWNLOADED_SAME_FILE_NAME:
			resultStr = '[b]{}[/b] audio already downloaded in [b]{}[/b] dir. Video skipped.\n'.format(
				msgArgTuple[0],
				msgArgTuple[1])
		elif msgType == MSG_TYPE_AUDIO_ALREADY_DOWNLOADED_DIFF_FILE_NAME:
			resultStr = '[b]{}[/b] audio already downloaded in [b]{}[/b] dir as [b]{}[/b]. Video skipped.\n'.format(
				msgArgTuple[0],
				msgArgTuple[1],
				msgArgTuple[2])
		elif msgType == MSG_TYPE_ATTRIBUTE_ERROR_VIDEO_TITLE:
			resultStr = 'obtaining video title failed with error {}.\n'.format(msgArgTuple[0])
		elif msgType == MSG_TYPE_ATTRIBUTE_ERROR_VIDEO_TITLE:
			resultStr = 'obtaining video title failed with error {}.\n'.format(msgArgTuple[0])

		return resultStr
