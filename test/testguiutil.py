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
		
		self.assertEqual("c:\\temp\\\ntesting\\\naudiobooks\\\nEt \nl\'Univers \ndisparaîtra-\nt-il: avec \nmes \ncommentaires", formattedMessage)
	
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
			"c:\\temp\\\ntesting\\\naudiobooks\Et \nl'Univers \ndisparaîtra-t-\nil: avec mes \ncommentaires",
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
		
		self.assertEqual(
			"c:\\temp\\testing\\\naudiobooks\Et \nl'Univers disparaîtra-\nt-il: avec mes \ncommentaires",
			formattedMessage)


if __name__ == '__main__':
#	unittest.main()
	tst = TestGuiUtil()
	tst.testReformatString()
