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
	
	def displayVideoCurrentDownloadInfo(self, currentDownloadInfoTuple):
		"""
		Method called every n seconds by AudioController.displayVideoCurrentDownloadInfo().

		:param currentDownloadInfoTuple:    3 elements tuple containing current
											download size in bytes, download size
											percent string and current download
											speed string (in KiB/s)
		"""
		pass # avoid printing variable info values when running unit tests
	
	def displayVideoEndDownloadInfo(self, endDownloadInfoLst):
		"""
		Method called when the video download is finished by
		AudioController.displayVideoEndDownloadInfo().

		:param endDownloadInfoLst:  2 elements tuple containing final download
									size in bytes and total download time in
									seconds
		"""
		pass # avoid printing variable info values when running unit tests

	def displayPlaylistEndDownloadInfo(self, endDownloadInfoLst):
		"""
		Method called when the playlist videos download is finished by
		AudioController.displayPlaylistEndDownloadInfo().

		:param endDownloadInfoLst:  2 elements tuple containing final download
									size in bytes and total download time in
									seconds
		"""
		pass # avoid printing variable info values when running unit tests

	def displayVideoMp3ConversionCurrentInfo(self, videoCurrentMp3ConversionInfoList):
		"""
		Method called every n seconds by
		AudioController.displayVideoMp3ConversionCurrentInfo().

		:param videoCurrentMp3ConversionInfoList:   1 element list containing current
													conversion time hh:mm:ss string..
		"""
		pass # avoid printing variable info values when running unit tests
	
	def confirmDownloadDespiteIndexDateCompatibilityWarning(self,
	                                                        indexAndDateSettingWarningMsg):
		print(indexAndDateSettingWarningMsg)
		return True