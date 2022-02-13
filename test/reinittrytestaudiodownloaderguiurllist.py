import os, sys, inspect
from io import StringIO

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from trytestaudiodownloaderguiurllist import TryTestAudioDownloaderGUIUrlList


class ReInitTryTestAudioDownloaderGUIUrlList:
	"""
	Test utility class which executes TryTestAudioDownloaderGUIUrlList after
	having entered a different letter than 'g' in stdin so that the
	TryTestAudioDownloaderGUIUrlList is executed without opening the GUI,
	but only in restoring the output dirs. So, re-download all can be redone
	without restarting TryTestAudioDownloaderGUIUrlList and loose time re-selecting
	the URL items to download.
	"""
	def doReinit(self):
		"""
		Restores the TryTestAudioDownloaderGUIUrlList output dirs
		:return:
		"""

		stdin = sys.stdin
		sys.stdin = StringIO('a')

		tryTst = TryTestAudioDownloaderGUIUrlList()
		tryTst.tryTestAudioDownloaderGUI()
		print('\n\nTryTestAudioDownloaderGUIUrlList output dirs reinitialized')
		
		sys.stdin = stdin

if __name__ == '__main__':
	reI = ReInitTryTestAudioDownloaderGUIUrlList()
	reI.doReinit()