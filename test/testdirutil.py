import unittest
import os, sys, inspect, glob
from os.path import sep

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from constants import *
from dirutil import DirUtil

class TestDirUtil(unittest.TestCase):

	def testReplaceUnauthorizedDirNameChars(self):
		playlistTitle = "Audio: - ET L'UNIVERS DISPARAÎTRA/La \\nature * illusoire de notre réalité et le pouvoir transcendant du |véritable \"pardon\" + commentaires de <Gary> Renard ?"
		expectedFileName = "Audio - ET L_UNIVERS DISPARAÎTRA_La nature   illusoire de notre réalité et le pouvoir transcendant du véritable 'pardon' + commentaires de Gary Renard "
		
		downloadDir = DirUtil.getTestAudioRootPath() + sep + expectedFileName
		
		# deleting dic file in downloadDir
		files = glob.glob(downloadDir + sep + '*.txt')
		
		for f in files:
			os.remove(f)
		
		actualFileName = DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistTitle)
		
		self.assertEqual(expectedFileName, actualFileName)

	def testExtractPathFromPathFileName(self):
		expectedPath = 'c:' + sep + 'users' + sep + 'jean-pierre'
		pathFileName = expectedPath + sep + 'file.mp3'
		
		self.assertEqual(expectedPath, DirUtil.extractPathFromPathFileName(pathFileName))
	
	def testExtractFileNameFromPathFileName(self):
		expectedFileName = 'file.mp3'
		pathFileName = 'c:' + sep + 'users' + sep + 'jean-pierre' + sep + expectedFileName
		
		self.assertEqual(expectedFileName, DirUtil.extractFileNameFromPathFileName(pathFileName))
	
	def testGetLastSubDirs(self):
		fullDir = 'C:\\Users\\Jean-Pierre\\Downloads\\Audio\\Test 3 short videos'
		expectedShortDir = 'Audio\\Test 3 short videos'
		
		self.assertEqual(expectedShortDir, DirUtil.getLastSubDirs(fullDir,
		                                                          subDirsNumber=2))
	
	def testGetFullDirMinusRootDir_several_sub_dirs(self):
		fullDir = 'C:\\Users\\Jean-Pierre\\Downloads\\Audio\\UCEM\\Gary Rennard\\Aimer sans peur'
		audioRootDir = 'C:\\Users\\Jean-Pierre\\Downloads\\Audio'
		expectedShortDir = 'Audio\\UCEM\\Gary Rennard\\Aimer sans peur'
		expectedShorterDir = 'UCEM\\Gary Rennard\\Aimer sans peur'

		self.assertEqual(expectedShortDir, DirUtil.getFullDirMinusRootDir(rootDir=audioRootDir,
		                                                                  fullDir=fullDir,
		                                                                  remainingRootSubDirNumber=1))
		self.assertEqual(expectedShorterDir, DirUtil.getFullDirMinusRootDir(rootDir=audioRootDir,
		                                                                    fullDir=fullDir))

	def testGetFullDirMinusRootDir_one_sub_dir(self):
		fullDir = 'C:\\Users\\Jean-Pierre\\Downloads\\Audio\\Aimer sans peur'
		audioRootDir = 'C:\\Users\\Jean-Pierre\\Downloads\\Audio'
		expectedShortDir = 'Audio\\Aimer sans peur'
		expectedShorterDir = 'Aimer sans peur'
		
		self.assertEqual(expectedShortDir, DirUtil.getFullDirMinusRootDir(rootDir=audioRootDir,
		                                                                  fullDir=fullDir,
		                                                                  remainingRootSubDirNumber=1))
		self.assertEqual(expectedShorterDir, DirUtil.getFullDirMinusRootDir(rootDir=audioRootDir,
		                                                                    fullDir=fullDir))

	def testRemoveDirectoryTree(self):
		createdFileName = 'temp.txt'
		
		testBaseRootDir = 'test dir util'
		testBaseRootPath = DirUtil.getTestAudioRootPath() + sep + testBaseRootDir
		createdSubdirs = 'new dir' + sep + 'new sub dir'
		createdSubdirsPath = testBaseRootPath + sep + createdSubdirs
		
		DirUtil.createTargetDirIfNotExist(createdSubdirsPath)
		
		createdFilePathName = createdSubdirsPath + sep + createdFileName

		with open(createdFilePathName, 'w') as f:
			f.write('Hello World')
		
		self.assertTrue(os.path.isfile(createdFilePathName))
		filePathNameComponents = createdFilePathName.split(sep)
		self.assertTrue(os.path.isdir(sep.join(filePathNameComponents[:-1])))
		self.assertTrue(os.path.isdir(sep.join(filePathNameComponents[:-2])))

		# removing test dir and sub dirs and its files
		DirUtil.removeDirectoryTree(testBaseRootPath)

		self.assertFalse(os.path.isfile(createdFilePathName))
		self.assertFalse(os.path.isdir(sep.join(filePathNameComponents[:-1])))
		self.assertFalse(os.path.isdir(sep.join(filePathNameComponents[:-2])))

	def testRenameFile(self):
		createdFileName = 'temp.txt'
		renamedFileName = 'renamed_temp.txt'
		
		testBaseRootDir = 'test dir util'
		testBaseRootPath = DirUtil.getTestAudioRootPath() + sep + testBaseRootDir
		
		DirUtil.createTargetDirIfNotExist(testBaseRootPath)
		
		createdFilePathName = testBaseRootPath + sep + createdFileName
		
		with open(createdFilePathName, 'w') as f:
			f.write('Hello World')
		
		self.assertTrue(os.path.isfile(createdFilePathName))

		DirUtil.renameFile(createdFilePathName, renamedFileName)

		renamedFilePathName = testBaseRootPath + sep + renamedFileName

		self.assertTrue(os.path.isfile(renamedFilePathName))

		# removing test dir and its file
		DirUtil.removeDirectoryTree(testBaseRootPath)


if __name__ == '__main__':
	#unittest.main()
	tst = TestDirUtil()
	tst.testReplaceUnauthorizedDirNameChars()
