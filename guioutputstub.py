import os
from tkinter import Tk, TclError, Message
class GuiOutputStub:
	'''
	This class is used for testing only
	'''
	def getPlaylistUrlFromClipboard(self):
		pass
	
	def setMessage(self, msgText):
		print(msgText)
			
	def displayError(self, msg):
		print(msg)
		
	def getConfirmation(self, msg):
		print(msg)
		return True
		