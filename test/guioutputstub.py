import os
from tkinter import Tk, TclError, Message
class GuiOutputStub:
	'''
	This class is used for testing only
	'''
	def getPlaylistUrlFromClipboard(self):
		pass
	
	def displayMessage(self, msgText):
		msgText = msgText.replace('[b]', '"').replace('[/b]', '"')
		
		print(msgText)
	
	def outputResult(self, msgText):
		msgText = msgText.replace('[b]', '"').replace('[/b]', '"')
		
		print(msgText)
	
	def displayError(self, msgText):
		msgText = msgText.replace('[b]', '"').replace('[/b]', '"')
		
		print(msgText)
	
	def clearClipboard(self):
		from tkinter import Tk
		Tk().clipboard_clear()
	
	def displayCurrentDownloadInfo(self, currentDownloadInfoTuple):
		"""
		Method called every n seconds by AudioController.displayDownloadInfo().

		:param currentDownloadInfoTuple:    3 elements tuple containing current
											download size in bytes, download size
											percent string and current download
											speed string (in KiB/s)
		"""
		pass # avoid printing variable info values when running unit tests
	
	def displayEndDownloadInfo(self, endDownloadInfoLst):
		"""
		Method called when the video download is finished by
		AudioController.displayEndDownloadInfo().

		:param endDownloadInfoLst:  2 elements tuple containing final download
									size in bytes and total download time in
									seconds
		"""
		pass # avoid printing variable info values when running unit tests