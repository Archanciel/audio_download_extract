import unittest
import os, sys, inspect
from os.path import sep

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from gui.guiutil import GuiUtil

class TestGuiUtil(unittest.TestCase):
	def testReformatString_maxLength_10(self):
		if sep == '\\':
			# on Windows
			msg = "c:\\temp\\testing\\audiobooks\\Et l'Univers disparaîtra-t-il: avec mes commentaires"
		else:
			# on Android
			msg = "c:/temp/testing/audiobooks/Et l'Univers disparaîtra: avec mes commentaires"
		
		maxLength = 10
		formattedMessage = GuiUtil.reformatString(msg, maxLength)

		
		self.assertEqual("c:\\temp\\\ntesting\\\naudiobooks\\\nEt\nl'Univers\ndisparaîtra-\nt-il:\navec mes\ncommentaires", formattedMessage)

	def testReformatString_maxLength_15(self):
		if sep == '\\':
			# on Windows
			msg = "c:\\temp\\testing\\audiobooks\\Et l'Univers disparaîtra-t-il: avec mes commentaires"
		else:
			# on Android
			msg = "c:/temp/testing/audiobooks/Et l'Univers disparaîtra: avec mes commentaires"
		
		maxLength = 15
		formattedMessage = GuiUtil.reformatString(msg, maxLength)
		
		self.assertEqual(
			"c:\\temp\\\ntesting\\\naudiobooks\Et\nl'Univers\ndisparaîtra-t-\nil: avec mes\ncommentaires",
			formattedMessage)
	
	def testReformatString_maxLength_20(self):
		if sep == '\\':
			# on Windows
			msg = "c:\\temp\\testing\\audiobooks\\Et l'Univers disparaîtra-t-il: avec mes commentaires"
		else:
			# on Android
			msg = "c:/temp/testing/audiobooks/Et l'Univers disparaîtra: avec mes commentaires"
		
		maxLength = 20
		formattedMessage = GuiUtil.reformatString(msg, maxLength)
		
		self.assertEqual("c:\\temp\\testing\\\naudiobooks\\Et\nl'Univers\ndisparaîtra-t-il:\navec mes\ncommentaires",
		                 formattedMessage)

	def testReformatString_maxLength_60(self):
		if sep == '\\':
			# on Windows
			msg = "Path C:\\Users\\Jean-Pierre\\Downloads\\Audio\\new does not exist ! Either create the directory or modify the path."
		else:
			# on Android
			msg = "Path C:/Users/Jean-Pierre/Downloads/Audio/new does not exist ! Either create the directory or modify the path."
		
		maxLength = 60
		formattedMessage = GuiUtil.reformatString(msg, maxLength)
		
		self.assertEqual("Path C:\\Users\\Jean-Pierre\\Downloads\\Audio\\new does not\nexist ! Either create the directory or modify the path.",
		                 formattedMessage)
	
	def testReformatString_maxLength_55(self):
		if sep == '\\':
			# on Windows
			msg = "Path C:\\Users\\Jean-Pierre\\Downloads\\Audio\\new does not exist ! Either create the directory or modify the path."
		else:
			# on Android
			msg = "Path C:/Users/Jean-Pierre/Downloads/Audio/new does not exist ! Either create the directory or modify the path."
		
		maxLength = 55
		formattedMessage = GuiUtil.reformatString(msg, maxLength)
		
		self.assertEqual("Path C:\\Users\\Jean-Pierre\\Downloads\\Audio\\new does\nnot exist ! Either create the directory or modify the\npath.",
		                 formattedMessage)
	
	def testReformatString_maxLength_65(self):
		msg = "Audio - LES VIES OÙ JÉSUS ET BOUDDHA SE CONNAISSAIENT L'histoire d'une noble amitié de Gary Renard"
		maxLength = 65
		formattedMessage = GuiUtil.reformatString(msg, maxLength)

		self.assertEqual("Audio - LES VIES OÙ JÉSUS ET BOUDDHA SE CONNAISSAIENT\nL'histoire d'une noble amitié de Gary Renard",
			formattedMessage)


if __name__ == '__main__':
#	unittest.main()
	tst = TestGuiUtil()
	tst.testReformatString_maxLength_55()
