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
		expectedFileName = "Audio - - ET L'UNIVERS DISPARAÎTRA_La nature   illusoire de notre réalité et le pouvoir transcendant du véritable 'pardon' + commentaires de Gary Renard "
		
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
	
	def testGetFullFilePathNameMinusRootDir_several_sub_dirs(self):
		fullDir = 'C:\\Users\\Jean-Pierre\\Downloads\\Audio\\UCEM\\Gary Rennard\\Aimer sans peur'
		audioRootDir = 'C:\\Users\\Jean-Pierre\\Downloads\\Audio'
		expectedShortDir = 'Audio\\UCEM\\Gary Rennard\\Aimer sans peur'
		expectedShorterDir = 'UCEM\\Gary Rennard\\Aimer sans peur'
		
		self.assertEqual(expectedShortDir, DirUtil.getFullFilePathNameMinusRootDir(rootDir=audioRootDir,
		                                                                           fullFilePathName=fullDir,
		                                                                           eliminatedRootLastSubDirsNumber=1))
		self.assertEqual(expectedShorterDir, DirUtil.getFullFilePathNameMinusRootDir(rootDir=audioRootDir,
		                                                                             fullFilePathName=fullDir))
	
	def testGetFullFilePathNameMinusRootDir_one_sub_dir(self):
		fullDir = 'C:\\Users\\Jean-Pierre\\Downloads\\Audio\\Aimer sans peur'
		audioRootDir = 'C:\\Users\\Jean-Pierre\\Downloads\\Audio'
		expectedShortDir = 'Audio\\Aimer sans peur'
		expectedShorterDir = 'Aimer sans peur'
		
		self.assertEqual(expectedShortDir, DirUtil.getFullFilePathNameMinusRootDir(rootDir=audioRootDir,
		                                                                           fullFilePathName=fullDir,
		                                                                           eliminatedRootLastSubDirsNumber=1))
		self.assertEqual(expectedShorterDir, DirUtil.getFullFilePathNameMinusRootDir(rootDir=audioRootDir,
		                                                                             fullFilePathName=fullDir))
	
	def testGetFullFilePathNameMinusRootDir_several_sub_dirs_mp3_fileName_1(self):
		fullDir = 'C:\\Users\\Jean-Pierre\\Downloads\\Audio\\UCEM\\Gary Rennard\\Aimer sans peur\\chapter 1.mp3'
		audioRootDir = 'C:\\Users\\Jean-Pierre\\Downloads\\Audio'
		expectedShortDir = 'Audio\\UCEM\\Gary Rennard\\Aimer sans peur\\chapter 1.mp3'
		expectedShorterDir = 'UCEM\\Gary Rennard\\Aimer sans peur\\chapter 1.mp3'
		
		self.assertEqual(expectedShortDir, DirUtil.getFullFilePathNameMinusRootDir(rootDir=audioRootDir,
		                                                                           fullFilePathName=fullDir,
		                                                                           eliminatedRootLastSubDirsNumber=1))
		self.assertEqual(expectedShorterDir, DirUtil.getFullFilePathNameMinusRootDir(rootDir=audioRootDir,
		                                                                             fullFilePathName=fullDir))
	
	def testGetFullFilePathNameMinusRootDir_several_sub_dirs_mp3_fileName_None(self):
		fullDir = 'C:\\Users\\Jean-Pierre\\Downloads\\Audio\\UCEM\\Gary Rennard\\Aimer sans peur\\chapter 1.mp3'
		audioRootDir = 'C:\\Users\\Jean-Pierre\\Downloads\\Audio'
		expectedShortDir = 'UCEM\\Gary Rennard\\Aimer sans peur\\chapter 1.mp3'
		expectedShorterDir = 'UCEM\\Gary Rennard\\Aimer sans peur\\chapter 1.mp3'
		
		self.assertEqual(expectedShortDir, DirUtil.getFullFilePathNameMinusRootDir(rootDir=audioRootDir,
		                                                                           fullFilePathName=fullDir,
		                                                                           eliminatedRootLastSubDirsNumber=None))
		self.assertEqual(expectedShorterDir, DirUtil.getFullFilePathNameMinusRootDir(rootDir=audioRootDir,
		                                                                             fullFilePathName=fullDir))
	
	def testGetFullFilePathNameMinusRootDir_several_sub_dirs_mp3_fileName_0(self):
		fullDir = 'C:\\Users\\Jean-Pierre\\Downloads\\Audio\\UCEM\\Gary Rennard\\Aimer sans peur\\chapter 1.mp3'
		audioRootDir = 'C:\\Users\\Jean-Pierre\\Downloads\\Audio'
		expectedShortDir = 'UCEM\\Gary Rennard\\Aimer sans peur\\chapter 1.mp3'
		expectedShorterDir = 'UCEM\\Gary Rennard\\Aimer sans peur\\chapter 1.mp3'
		
		self.assertEqual(expectedShortDir, DirUtil.getFullFilePathNameMinusRootDir(rootDir=audioRootDir,
		                                                                           fullFilePathName=fullDir,
		                                                                           eliminatedRootLastSubDirsNumber=0))
		self.assertEqual(expectedShorterDir, DirUtil.getFullFilePathNameMinusRootDir(rootDir=audioRootDir,
		                                                                             fullFilePathName=fullDir))
	
	def testRemoveSubDirsContainedInDir(self):
		createdFileName = 'temp.txt'
		
		testBaseRootDir = 'test dir util'
		testBaseRootPath = DirUtil.getTestAudioRootPath() + sep + testBaseRootDir
		createdSubdirs = 'new dir' + sep + 'new sub dir'
		createdSubdirsPath = testBaseRootPath + sep + createdSubdirs
		
		DirUtil.createTargetDirIfNotExist(rootDir=testBaseRootPath,
		                                  targetAudioDir=createdSubdirsPath)
		
		createdFilePathName = createdSubdirsPath + sep + createdFileName
		
		with open(createdFilePathName, 'w') as f:
			f.write('Hello World')
		
		self.assertTrue(os.path.isfile(createdFilePathName))
		filePathNameComponents = createdFilePathName.split(sep)
		self.assertTrue(os.path.isdir(sep.join(filePathNameComponents[:-1])))
		self.assertTrue(os.path.isdir(sep.join(filePathNameComponents[:-2])))
		
		# removing test dir and sub dirs and its files
		DirUtil.removeSubDirsContainedInDir(testBaseRootPath)
		
		self.assertFalse(os.path.isfile(createdFilePathName))
		self.assertFalse(os.path.isdir(sep.join(filePathNameComponents[:-1])))
		self.assertFalse(os.path.isdir(sep.join(filePathNameComponents[:-2])))
	
	def testRenameFile(self):
		createdFileName = 'temp.txt'
		renamedFileName = 'renamed_temp.txt'
		
		testBaseRootDir = 'test dir util'
		testBaseRootPath = DirUtil.getTestAudioRootPath() + sep + testBaseRootDir
		
		DirUtil.createTargetDirIfNotExist(rootDir=testBaseRootPath,
		                                  targetAudioDir=testBaseRootPath)
		
		createdFilePathName = testBaseRootPath + sep + createdFileName
		
		with open(createdFilePathName, 'w') as f:
			f.write('Hello World')
		
		self.assertTrue(os.path.isfile(createdFilePathName))
		
		DirUtil.renameFile(createdFilePathName, renamedFileName)
		
		renamedFilePathName = testBaseRootPath + sep + renamedFileName
		
		self.assertTrue(os.path.isfile(renamedFilePathName))
		
		# removing test dir and its file
		DirUtil.removeSubDirsContainedInDir(testBaseRootPath)
	
	def testRenameFile_with_invalid_file_name(self):
		createdFileName = 'temp.txt'
		invalidCreatedFileName = 'temp ?.txt'
		renamedFileName = 'renamed_temp.txt'
		
		testBaseRootDir = 'test dir util'
		testBaseRootPath = DirUtil.getTestAudioRootPath() + sep + testBaseRootDir
		
		DirUtil.createTargetDirIfNotExist(rootDir=testBaseRootPath,
		                                  targetAudioDir=testBaseRootPath)
		
		createdFilePathName = testBaseRootPath + sep + createdFileName
		
		with open(createdFilePathName, 'w') as f:
			f.write('Hello World')
		
		self.assertTrue(os.path.isfile(createdFilePathName))
		
		errorInfo = DirUtil.renameFile(invalidCreatedFileName, renamedFileName)
		
		self.assertEqual(
			"[WinError 123] La syntaxe du nom de fichier, de répertoire ou de volume est incorrecte: 'temp ?.txt' -> '\\\\renamed_temp.txt'",
			errorInfo)
		
		# removing test dir
		DirUtil.removeSubDirsContainedInDir(testBaseRootPath)
	
	def testRenameFile_file_to_rename_not_exist(self):
		createdFileName = 'temp.txt'
		renamedFileName = 'renamed_temp.txt'
		
		testBaseRootDir = 'test dir util'
		testBaseRootPath = DirUtil.getTestAudioRootPath() + sep + testBaseRootDir
		
		DirUtil.createTargetDirIfNotExist(rootDir=testBaseRootPath,
		                                  targetAudioDir=testBaseRootPath)
		
		createdFilePathName = testBaseRootPath + sep + createdFileName
		
		self.assertFalse(os.path.isfile(createdFilePathName))
		
		errorInfo = DirUtil.renameFile(createdFilePathName, renamedFileName)
		
		self.assertEqual(
			"[WinError 2] Le fichier spécifié est introuvable: 'C:\\\\Users\\\\Jean-Pierre\\\\Downloads\\\\Audio\\\\test\\\\test dir util\\\\temp.txt' -> 'C:\\\\Users\\\\Jean-Pierre\\\\Downloads\\\\Audio\\\\test\\\\test dir util\\\\renamed_temp.txt'",
			errorInfo)
		
		# removing test dir
		DirUtil.removeSubDirsContainedInDir(testBaseRootPath)
	
	def testRenameFile_file_with_new_name_already_exist(self):
		createdFileName = 'temp.txt'
		renamedFileName = 'renamed_temp.txt'
		
		testBaseRootDir = 'test dir util'
		testBaseRootPath = DirUtil.getTestAudioRootPath() + sep + testBaseRootDir
		
		DirUtil.createTargetDirIfNotExist(rootDir=testBaseRootPath,
		                                  targetAudioDir=testBaseRootPath)
		
		createdFilePathName = testBaseRootPath + sep + createdFileName
		
		with open(createdFilePathName, 'w') as f:
			f.write('Hello World')
		
		self.assertTrue(os.path.isfile(createdFilePathName))
		
		renamedFilePathName = testBaseRootPath + sep + renamedFileName
		
		with open(renamedFilePathName, 'w') as f:
			f.write('Hello World')
		
		self.assertTrue(os.path.isfile(renamedFilePathName))
		
		errorInfo = DirUtil.renameFile(createdFilePathName, renamedFileName)
		
		self.assertEqual(
			"[WinError 183] Impossible de créer un fichier déjà existant: 'C:\\\\Users\\\\Jean-Pierre\\\\Downloads\\\\Audio\\\\test\\\\test dir util\\\\temp.txt' -> 'C:\\\\Users\\\\Jean-Pierre\\\\Downloads\\\\Audio\\\\test\\\\test dir util\\\\renamed_temp.txt'",
			errorInfo)
		
		# removing test dir
		DirUtil.removeSubDirsContainedInDir(testBaseRootPath)
	
	def testCreateTargetDirIfNotExist_singleVideo(self):
		testBaseRootDir = 'Audio' + sep + 'Various'
		testBaseRootPath = DirUtil.getTestAudioRootPath() + sep + testBaseRootDir
		createdSubdirs = 'France' + sep + 'politique'
		createdSubdirsPath = testBaseRootPath + sep + createdSubdirs
		
		# removing test dir and sub dirs and its files
		DirUtil.removeSubDirsContainedInDir(testBaseRootPath)
		
		subdirs = createdSubdirsPath.split(sep)
		
		self.assertFalse(os.path.isdir(sep.join(subdirs[:-1])))
		self.assertFalse(os.path.isdir(sep.join(subdirs[:-2])))
		
		targetAudioDirShort, dirCreationMessage = \
			DirUtil.createTargetDirIfNotExist(rootDir=DirUtil.getTestAudioRootPath() + sep + 'Audio',
			                                  targetAudioDir=createdSubdirsPath)
		
		self.assertTrue(os.path.isdir(sep.join(subdirs[:-1])))
		self.assertTrue(os.path.isdir(sep.join(subdirs[:-2])))
		self.assertEqual('Audio' + sep + 'Various' + sep + 'France' + sep + 'politique', targetAudioDirShort)
		self.assertEqual("directory\nAudio" + sep + 'Various' + sep + 'France' + sep + "politique\nwas created.\n",
		                 dirCreationMessage)
	
	def testCreateTargetDirIfNotExist_playlist(self):
		testBaseRootDir = 'Audio'
		testBaseRootPath = DirUtil.getTestAudioRootPath() + sep + testBaseRootDir
		createdSubdirs = 'France' + sep + 'politique'
		createdSubdirsPath = testBaseRootPath + sep + createdSubdirs
		
		# removing test dir and sub dirs and its files
		DirUtil.removeSubDirsContainedInDir(testBaseRootPath)
		
		subdirs = createdSubdirsPath.split(sep)
		
		self.assertFalse(os.path.isdir(sep.join(subdirs[:-1])))
		self.assertFalse(os.path.isdir(sep.join(subdirs[:-2])))
		
		targetAudioDirShort, dirCreationMessage = \
			DirUtil.createTargetDirIfNotExist(rootDir=testBaseRootPath,
			                                  targetAudioDir=createdSubdirsPath)
		
		self.assertTrue(os.path.isdir(sep.join(subdirs[:-1])))
		self.assertTrue(os.path.isdir(sep.join(subdirs[:-2])))
		self.assertEqual('Audio' + sep + 'France' + sep + 'politique', targetAudioDirShort)
		self.assertEqual("directory\nAudio" + sep + 'France' + sep + "politique\nwas created.\n", dirCreationMessage)

	def testGetFilePathNamesInDirForPattern(self):
		fileName_1 = 'file_one.mp3'
		fileName_2 = 'file_two.mp3'
		
		testBaseRootDir = 'test dir util'
		testBaseRootPath = DirUtil.getTestAudioRootPath() + sep + testBaseRootDir
		
		DirUtil.createTargetDirIfNotExist(rootDir=testBaseRootPath,
		                                  targetAudioDir=testBaseRootPath)
		
		filePathName_1 = testBaseRootPath + sep + fileName_1
		filePathName_2 = testBaseRootPath + sep + fileName_2
		filePathNameLst = [filePathName_1, filePathName_2]
		
		# creating the files which will be listed
		
		for filePathName in filePathNameLst:
			with open(filePathName, 'w') as f:
				f.write('Hello World')
		
		self.assertTrue(os.path.isfile(filePathName_1))
		self.assertTrue(os.path.isfile(filePathName_2))
		
		# now getting the files
		
		filePathNameLst = DirUtil.getFilePathNamesInDirForPattern(testBaseRootPath, '*.mp3')
		
		self.assertEqual(filePathName_1, filePathNameLst[0])
		self.assertEqual(filePathName_2, filePathNameLst[1])
		
		# removing test dir and its file
		DirUtil.removeSubDirsContainedInDir(testBaseRootPath)
	
	def testGetFileNamesInDirForPattern(self):
		fileName_1 = 'file_one.mp3'
		fileName_2 = 'file_two.mp3'
		
		testBaseRootDir = 'test dir util'
		testBaseRootPath = DirUtil.getTestAudioRootPath() + sep + testBaseRootDir
		
		DirUtil.createTargetDirIfNotExist(rootDir=testBaseRootPath,
		                                  targetAudioDir=testBaseRootPath)
		
		filePathName_1 = testBaseRootPath + sep + fileName_1
		filePathName_2 = testBaseRootPath + sep + fileName_2
		fileNameLst = [filePathName_1, filePathName_2]
		
		# creating the files which will be listed
		
		for filePathName in fileNameLst:
			with open(filePathName, 'w') as f:
				f.write('Hello World')
		
		self.assertTrue(os.path.isfile(filePathName_1))
		self.assertTrue(os.path.isfile(filePathName_2))
		
		# now getting the files
		
		fileNameLst = DirUtil.getFileNamesInDirForPattern(testBaseRootPath, '*.mp3')
		
		self.assertEqual(fileName_1, fileNameLst[0])
		self.assertEqual(fileName_2, fileNameLst[1])
		
		# removing test dir and its file
		DirUtil.removeSubDirsContainedInDir(testBaseRootPath)
	
	def testDeleteFiles(self):
		deletedFileName_1 = 'file_one.mp3'
		deletedFileName_2 = 'file_two.mp3'
		
		testBaseRootDir = 'test dir util'
		testBaseRootPath = DirUtil.getTestAudioRootPath() + sep + testBaseRootDir
		
		DirUtil.createTargetDirIfNotExist(rootDir=testBaseRootPath,
		                                  targetAudioDir=testBaseRootPath)
		
		deletedFilePathName_1 = testBaseRootPath + sep + deletedFileName_1
		deletedFilePathName_2 = testBaseRootPath + sep + deletedFileName_2
		deletedFilePathNameLst = [deletedFilePathName_1, deletedFilePathName_2]
		
		# creating the files which will be deleted
		
		for deletedFilePathName in deletedFilePathNameLst:
			with open(deletedFilePathName, 'w') as f:
				f.write('Hello World')
		
		self.assertTrue(os.path.isfile(deletedFilePathName_1))
		self.assertTrue(os.path.isfile(deletedFilePathName_2))
		
		# now deleting the files
		
		DirUtil.deleteFiles(filePathNameLst=deletedFilePathNameLst)
		
		self.assertFalse(os.path.isfile(deletedFilePathName_1))
		self.assertFalse(os.path.isfile(deletedFilePathName_2))
		
		# removing test dir and its file
		DirUtil.removeSubDirsContainedInDir(testBaseRootPath)
	
	def testDeleteFiles_emptyDeleteFileLst(self):
		deletedFileName_1 = 'file_one.mp3'
		deletedFileName_2 = 'file_two.mp3'
		
		testBaseRootDir = 'test dir util'
		testBaseRootPath = DirUtil.getTestAudioRootPath() + sep + testBaseRootDir
		
		DirUtil.createTargetDirIfNotExist(rootDir=testBaseRootPath,
		                                  targetAudioDir=testBaseRootPath)
		
		deletedFilePathName_1 = testBaseRootPath + sep + deletedFileName_1
		deletedFilePathName_2 = testBaseRootPath + sep + deletedFileName_2
		deletedFilePathNameLst = [deletedFilePathName_1, deletedFilePathName_2]
		
		# creating the files which will be deleted
		
		for deletedFilePathName in deletedFilePathNameLst:
			with open(deletedFilePathName, 'w') as f:
				f.write('Hello World')
		
		self.assertTrue(os.path.isfile(deletedFilePathName_1))
		self.assertTrue(os.path.isfile(deletedFilePathName_2))
		
		# now deleting the files
		
		DirUtil.deleteFiles(filePathNameLst=[])
		
		self.assertTrue(os.path.isfile(deletedFilePathName_1))
		self.assertTrue(os.path.isfile(deletedFilePathName_2))
		
		# removing test dir and its file
		DirUtil.removeSubDirsContainedInDir(testBaseRootPath)


if __name__ == '__main__':
	# unittest.main()
	tst = TestDirUtil()
	tst.testCreateTargetDirIfNotExist_singleVideo()