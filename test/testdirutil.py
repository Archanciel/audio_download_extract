import unittest
import os, sys, inspect, glob
from os.path import sep

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from constants import  *
from dirutil import DirUtil

class TestDirUtil(unittest.TestCase):

	def testReplaceUnauthorizedDirNameChars(self):
		playlistTitle = "Audio: - ET L'UNIVERS DISPARAÎTRA/La \\nature * illusoire de notre réalité et le pouvoir transcendant du |véritable \"pardon\" + commentaires de <Gary> Renard ?"
		expectedFileName = "Audio - ET L'UNIVERS DISPARAÎTRA La nature   illusoire de notre réalité et le pouvoir transcendant du véritable pardon + commentaires de Gary Renard"
		
		downloadDir = DirUtil.getTestAudioRootPath() + sep + expectedFileName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		actualFileName = DirUtil.replaceUnauthorizedDirNameChars(playlistTitle)
		
		self.assertEqual(expectedFileName, actualFileName)

	def testExtractPathFromPathFileName(self):
		expectedPath = 'c:' + sep + 'users' + sep + 'jean-pierre'
		pathFileName = expectedPath + sep + 'file.mp3'
		
		self.assertEqual(expectedPath, DirUtil.extractPathFromPathFileName(pathFileName))


if __name__ == '__main__':
	#unittest.main()
	tst = TestDirUtil()
	tst.testReplaceUnauthorizedDirNameChars()
