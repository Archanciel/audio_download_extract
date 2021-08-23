import os
from tkinter import Tk, TclError, Message
class GuiOutputStub:
	'''
	This class is used for testing only
	'''
	def getPlaylistUrlFromClipboard(self):
		pass
	
	def displayMessage(self, msgText):
		print(msgText)
	
	def outputResult(self, msgText):
		print(msgText)
	
	def displayError(self, msg):
		print(msg)
	
	def clearClipboard(self):
		from tkinter import Tk
		Tk().clipboard_clear()
