import os
from tkinter import TclError, Message
import tkinter.messagebox as msgb

if os.name == 'posix':
	WIN_WIDTH_RATIO = 1
	WIN_HEIGHT = 800	
else:
	WIN_WIDTH_RATIO = 0.8
	WIN_HEIGHT = 500	

class GuiOutput:
	def __init__(self, tkRoot):
		self.root = tkRoot
		winWidth = int(self.root.winfo_screenwidth() * WIN_WIDTH_RATIO)
		self.root.geometry("{}x{}".format(winWidth, WIN_HEIGHT)) 
		self.msg = Message(self.root, aspect=winWidth - 10)
		self.msg.grid(row=2, column=0, columnspan=2, padx=2) 
		self.msgText = ''  
		self.msg = Message(self.root, aspect=winWidth - 10)

	def getPlaylistUrlFromClipboard(self):
		playlistUrl = None

		try:
			playlistUrl = self.root.clipboard_get()
		except TclError:
			# playlistUrl remains None
			pass

		return playlistUrl
	
	def setMessage(self, msgText):
		self.msg.configure(text=msgText)
		self.root.update()
			
	def displayError(self, msg):
		return msgb.showerror(message=msg)
		
	def getConfirmation(self, msg):
		return msgb.askquestion(message=msg) == 'yes'
	
	def clearClipboard(self):
		self.root.clipboard_clear()
		