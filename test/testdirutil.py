import unittest
import os, sys, inspect, glob

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from constants import  *
from dirutil import DirUtil

class TestDirUtil(unittest.TestCase):

	def testReplaceUnauthorizedDirNameChars(self):
		playlistTitle = "Audio: - ET L'UNIVERS DISPARAÎTRA/La \\nature * illusoire de notre réalité et le pouvoir transcendant du |véritable \"pardon\" + commentaires de <Gary> Renard ?"
		expectedFileName = "Audio - ET L'UNIVERS DISPARAÎTRA La nature   illusoire de notre réalité et le pouvoir transcendant du véritable pardon + commentaires de Gary Renard"
		
		downloadDir = AUDIO_DIR_TEST + DIR_SEP + expectedFileName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.txt')
		
		for f in files:
			os.remove(f)
		
		actualFileName = DirUtil.replaceUnauthorizedDirNameChars(playlistTitle)
		
		self.assertEqual(expectedFileName, actualFileName)


if __name__ == '__main__':
	#unittest.main()
	tst = TestDirUtil()
	tst.testReplaceUnauthorizedDirNameChars()
