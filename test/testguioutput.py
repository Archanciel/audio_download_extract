import unittest
import os, sys, inspect, datetime, shutil
from distutils import dir_util
from io import StringIO
from tkinter import Tk

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)
		
from guioutput import GuiOutput
			
class TestGuiOutput(unittest.TestCase):
	def testGetPlaylistUrlFromClipboard(self):
		tk = Tk()
		guiOutput = GuiOutput(tk)
		url = "http://anurl.com"
		tk.clipboard_clear()
		tk.clipboard_append(url)

		self.assertEqual(url, guiOutput.getPlaylistUrlFromClipboard())
		
	def testGetPlaylistUrlFromClipboard_empty(self):
		tk = Tk()
		guiOutput = GuiOutput(tk)
		tk.clipboard_clear()

		self.assertIsNone(guiOutput.getPlaylistUrlFromClipboard())
	
if __name__ == '__main__':
	unittest.main()
#	tst = TestTransferFiles()
#	tst.testPathUploadToCloud_invalid_fileName()
