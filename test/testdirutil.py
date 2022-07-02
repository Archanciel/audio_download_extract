import time
import unittest
import os, sys, inspect, shutil, datetime
from os.path import sep

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from dirutil import DirUtil
from downloadplaylistinfodic import DownloadPlaylistInfoDic


class TestDirUtil(unittest.TestCase):
	
	def testReplaceUnauthorizedDirOrFileNameChars(self):
		playlistTitle = "Audio: - ET L'UNIVERS DISPARAÎTRA/La \\nature * illusoire de notre réalité et le pouvoir transcendant du |véritable \"pardon\" + commentaires de <Gary> Renard ?"
		expectedFileName = "Audio - - ET L'UNIVERS DISPARAÎTRA_La nature   illusoire de notre réalité et le pouvoir transcendant du _véritable 'pardon' + commentaires de Gary Renard "
		
		actualFileName = DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistTitle)
		
		self.assertEqual(expectedFileName, actualFileName)
	
	def testReplaceUnauthorizedDirOrFileNameChars_or_char(self):
		playlistTitle = "💥 EFFONDREMENT Imminent de l'Euro ?! | 👉 Maintenant, La Fin de l'Euro Approche ?!"
		expectedFileName = "💥 EFFONDREMENT Imminent de l'Euro ! _ 👉 Maintenant, La Fin de l'Euro Approche !"
		
		actualFileName = DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistTitle)
		
		self.assertEqual(expectedFileName, actualFileName)
	
	def testReplaceUnauthorizedDirOrFileNameChars_or_char_at_end_fileName(self):
		playlistTitle = 'Indian 🇮🇳|American🇺🇸| Japanese🇯🇵|Students #youtubeshorts #shorts |Samayra Narula| Subscribe |'
		expectedFileName = 'Indian 🇮🇳_American🇺🇸_ Japanese🇯🇵_Students #youtubeshorts #shorts _Samayra Narula_ Subscribe '
		
		actualFileName = DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistTitle)
		
		self.assertEqual(expectedFileName, actualFileName)
	
	def testReplaceUnauthorizedDirOrFileNameChars_double_or_char(self):
		playlistTitle = 'Lambda Expressions & Anonymous Functions ||  Python Tutorial  ||  Learn Python Programming'
		expectedFileName = 'Lambda Expressions & Anonymous Functions _  Python Tutorial  _  Learn Python Programming'
		
		actualFileName = DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistTitle)
		
		self.assertEqual(expectedFileName, actualFileName)
	
	def testReplaceUnauthorizedDirOrFileNameChars_double_slash_char(self):
		videoTitle = '9 Dart concepts to know before you jump into Flutter // for super beginners in Flutter'
		expectedFileName = '9 Dart concepts to know before you jump into Flutter _ for super beginners in Flutter'
		
		actualFileName = DirUtil.replaceUnauthorizedDirOrFileNameChars(videoTitle)
		
		self.assertEqual(expectedFileName, actualFileName)
	
	def testExtractPathFromPathFileName(self):
		expectedPath = 'c:' + sep + 'users' + sep + 'jean-pierre'
		pathFileName = expectedPath + sep + 'file.mp3'
		
		self.assertEqual(expectedPath, DirUtil.extractPathFromPathFileName(pathFileName))
	
	def testExtractFileNameFromPathFileName(self):
		expectedFileName = 'file.mp3'
		pathFileName = 'c:' + sep + 'users' + sep + 'jean-pierre' + sep + expectedFileName
		
		self.assertEqual(expectedFileName, DirUtil.extractFileNameFromFilePathName(pathFileName))
	
	def testGetLastSubDirs(self):
		fullDir = 'D:\\Users\\Jean-Pierre\\Downloads\\Audio\\Test 3 short videos'
		expectedShortDir = 'Audio\\Test 3 short videos'
		
		self.assertEqual(expectedShortDir, DirUtil.getLastSubDirs(fullDir,
																  subDirsNumber=2))
	
	def testGetFullFilePathNameMinusRootDir_several_sub_dirs(self):
		fullDir = 'D:\\Users\\Jean-Pierre\\Downloads\\Audio\\UCEM\\Gary Rennard\\Aimer sans peur'
		audioRootDir = 'D:\\Users\\Jean-Pierre\\Downloads\\Audio'
		expectedShortDir = 'Audio\\UCEM\\Gary Rennard\\Aimer sans peur'
		expectedShorterDir = 'UCEM\\Gary Rennard\\Aimer sans peur'
		
		self.assertEqual(expectedShortDir, DirUtil.getFullFilePathNameMinusRootDir(rootDir=audioRootDir,
																				   fullFilePathName=fullDir,
																				   eliminatedRootLastSubDirsNumber=1))
		self.assertEqual(expectedShorterDir, DirUtil.getFullFilePathNameMinusRootDir(rootDir=audioRootDir,
																					 fullFilePathName=fullDir))
	
	def testGetFullFilePathNameMinusRootDir_one_sub_dir(self):
		fullDir = 'D:\\Users\\Jean-Pierre\\Downloads\\Audio\\Aimer sans peur'
		audioRootDir = 'D:\\Users\\Jean-Pierre\\Downloads\\Audio'
		expectedShortDir = 'Audio\\Aimer sans peur'
		expectedShorterDir = 'Aimer sans peur'
		
		self.assertEqual(expectedShortDir, DirUtil.getFullFilePathNameMinusRootDir(rootDir=audioRootDir,
																				   fullFilePathName=fullDir,
																				   eliminatedRootLastSubDirsNumber=1))
		self.assertEqual(expectedShorterDir, DirUtil.getFullFilePathNameMinusRootDir(rootDir=audioRootDir,
																					 fullFilePathName=fullDir))
	
	def testGetFullFilePathNameMinusRootDir_several_sub_dirs_mp3_fileName_1(self):
		fullDir = 'D:\\Users\\Jean-Pierre\\Downloads\\Audio\\UCEM\\Gary Rennard\\Aimer sans peur\\chapter 1.mp3'
		audioRootDir = 'D:\\Users\\Jean-Pierre\\Downloads\\Audio'
		expectedShortDir = 'Audio\\UCEM\\Gary Rennard\\Aimer sans peur\\chapter 1.mp3'
		expectedShorterDir = 'UCEM\\Gary Rennard\\Aimer sans peur\\chapter 1.mp3'
		
		self.assertEqual(expectedShortDir, DirUtil.getFullFilePathNameMinusRootDir(rootDir=audioRootDir,
																				   fullFilePathName=fullDir,
																				   eliminatedRootLastSubDirsNumber=1))
		self.assertEqual(expectedShorterDir, DirUtil.getFullFilePathNameMinusRootDir(rootDir=audioRootDir,
																					 fullFilePathName=fullDir))
	
	def testGetFullFilePathNameMinusRootDir_several_sub_dirs_mp3_fileName_None(self):
		fullDir = 'D:\\Users\\Jean-Pierre\\Downloads\\Audio\\UCEM\\Gary Rennard\\Aimer sans peur\\chapter 1.mp3'
		audioRootDir = 'D:\\Users\\Jean-Pierre\\Downloads\\Audio'
		expectedShortDir = 'UCEM\\Gary Rennard\\Aimer sans peur\\chapter 1.mp3'
		expectedShorterDir = 'UCEM\\Gary Rennard\\Aimer sans peur\\chapter 1.mp3'
		
		self.assertEqual(expectedShortDir, DirUtil.getFullFilePathNameMinusRootDir(rootDir=audioRootDir,
																				   fullFilePathName=fullDir,
																				   eliminatedRootLastSubDirsNumber=None))
		self.assertEqual(expectedShorterDir, DirUtil.getFullFilePathNameMinusRootDir(rootDir=audioRootDir,
																					 fullFilePathName=fullDir))
	
	def testGetFullFilePathNameMinusRootDir_several_sub_dirs_mp3_fileName_0(self):
		fullDir = 'D:\\Users\\Jean-Pierre\\Downloads\\Audio\\UCEM\\Gary Rennard\\Aimer sans peur\\chapter 1.mp3'
		audioRootDir = 'D:\\Users\\Jean-Pierre\\Downloads\\Audio'
		expectedShortDir = 'UCEM\\Gary Rennard\\Aimer sans peur\\chapter 1.mp3'
		expectedShorterDir = 'UCEM\\Gary Rennard\\Aimer sans peur\\chapter 1.mp3'
		
		self.assertEqual(expectedShortDir, DirUtil.getFullFilePathNameMinusRootDir(rootDir=audioRootDir,
																				   fullFilePathName=fullDir,
																				   eliminatedRootLastSubDirsNumber=0))
		self.assertEqual(expectedShorterDir, DirUtil.getFullFilePathNameMinusRootDir(rootDir=audioRootDir,
																					 fullFilePathName=fullDir))
	
	def testDeleteDirAndItsSubDirs(self):
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
		DirUtil.deleteDirAndItsSubDirs(testBaseRootPath)
		
		self.assertFalse(os.path.isdir(testBaseRootPath))
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
		
		# removing test dir and its file so that they are not uploaded on GitHub
		DirUtil.deleteDirAndItsSubDirs(testBaseRootPath)
	
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
		
		# removing test dir and its file so that they are not uploaded on GitHub
		DirUtil.deleteDirAndItsSubDirs(testBaseRootPath)
	
	def testRenameFile_file_to_rename_not_exist(self):
		testAudioRootPath = DirUtil.getTestAudioRootPath()
		createdFileName = 'temp.txt'
		renamedFileName = 'renamed_temp.txt'
		
		testBaseRootDir = 'test dir util'
		testBaseRootPath = DirUtil.getTestAudioRootPath() + sep + testBaseRootDir
		
		# removing test dir and recreating it

		DirUtil.deleteDirAndItsSubDirs(testBaseRootPath)
		DirUtil.createTargetDirIfNotExist(rootDir=testAudioRootPath,
										  targetAudioDir=testBaseRootPath)
		
		createdFilePathName = testBaseRootPath + sep + createdFileName
		
		self.assertFalse(os.path.isfile(createdFilePathName))
		
		errorInfo = DirUtil.renameFile(createdFilePathName, renamedFileName)
		
		testAudioRootPathDoubleBackSlash = testAudioRootPath.replace('\\', '\\\\')
		expectedErrorMsg = "[WinError 2] Le fichier spécifié est introuvable: '{}\\\\test dir util\\\\temp.txt' -> '{}\\\\test dir util\\\\renamed_temp.txt'".format(testAudioRootPathDoubleBackSlash, testAudioRootPathDoubleBackSlash)
		self.assertEqual(
			expectedErrorMsg,
			errorInfo)

		# removing test dir and its file so that they are not uploaded on GitHub
		DirUtil.deleteDirAndItsSubDirs(testBaseRootPath)

	def testRenameFile_file_with_new_name_already_exist(self):
		createdFileName = 'temp.txt'
		renamedFileName = 'renamed_temp.txt'
		
		testBaseRootDir = 'test dir util'
		testAudioRootPath = DirUtil.getTestAudioRootPath()
		testBaseRootPath = testAudioRootPath + sep + testBaseRootDir
		
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
		
		testAudioRootPathDoubleBackSlash = testAudioRootPath.replace('\\', '\\\\')

		self.assertEqual(
			"[WinError 183] Impossible de créer un fichier déjà existant: '{}\\\\test dir util\\\\temp.txt' -> '{}\\\\test dir util\\\\renamed_temp.txt'".format(testAudioRootPathDoubleBackSlash, testAudioRootPathDoubleBackSlash),
			errorInfo)
		
		# removing test dir so that it is not uploaded on GitHub
		DirUtil.deleteDirAndItsSubDirs(testBaseRootPath)
	
	def testCreateTargetDirIfNotExist_singleVideo(self):
		testBaseRootDir = 'Audio' + sep + 'Various'
		testBaseRootPath = DirUtil.getTestAudioRootPath() + sep + testBaseRootDir
		createdSubdirs = 'France' + sep + 'politique'
		createdSubdirsPath = testBaseRootPath + sep + createdSubdirs
		
		# removing test dir and sub dirs and its files
		DirUtil.deleteDirAndItsSubDirs(testBaseRootPath)
		
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
		
		# removing test dir so that it is not uploaded on GitHub
		DirUtil.deleteDirAndItsSubDirs(testBaseRootPath)
	
	def testCreateTargetDirIfNotExist_playlist(self):
		testBaseRootDir = 'Audio'
		testBaseRootPath = DirUtil.getTestAudioRootPath() + sep + testBaseRootDir
		createdSubdirs = 'France' + sep + 'politique'
		createdSubdirsPath = testBaseRootPath + sep + createdSubdirs
		
		# removing test dir and sub dirs and its files
		DirUtil.deleteDirAndItsSubDirs(testBaseRootPath)
		
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
		
		# removing test dir so that it is not uploaded on GitHub
		DirUtil.deleteDirAndItsSubDirs(testBaseRootPath)
	
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
		
		# removing test dir so that it is not uploaded on GitHub
		DirUtil.deleteDirAndItsSubDirs(testBaseRootPath)
	
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
		
		# removing test dir so that it is not uploaded on GitHub
		DirUtil.deleteDirAndItsSubDirs(testBaseRootPath)
	
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
		
		# removing test dir so that it is not uploaded on GitHub
		DirUtil.deleteDirAndItsSubDirs(testBaseRootPath)
	
	def testDeleteFiles_file_list_empty(self):
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
		
		# removing test dir so that it is not uploaded on GitHub
		DirUtil.deleteDirAndItsSubDirs(testBaseRootPath)

	def testGetIndexAndDateUsageInFileNameLst(self):
		fileNameLst_index_date_1 = ['97-Funny suspicious looking dog 2013-11-05.mp3',
									'Funny suspicious looking dog 2013-11-05.mp3',
									'97-Funny suspicious looking dog.mp3',
									'Funny suspicious looking dog.mp3']
		fileNameLst_index_date_2 = ['Funny suspicious looking dog 2013-11-05.mp3',
									'97-Funny suspicious looking dog.mp3',
									'Funny suspicious looking dog.mp3']
		fileNameLst_index_no_date = ['97-Funny suspicious looking dog.mp3',
									 'Funny suspicious looking dog.mp3']
		fileNameLst_no_index_no_date = ['Funny new suspicious looking dog.mp3',
										'Funny suspicious looking dog.mp3']
		fileNameLst_no_index_date = ['Funny suspicious looking dog 2013-11-05.mp3',
									 'Funny new suspicious looking dog.mp3',
									 'Funny suspicious looking dog.mp3']
		emptyFileNameLst = []

		self.assertEqual([True, True, True, True], DirUtil.getIndexAndDateUsageInFileNameLst(fileNameLst_index_date_1))
		self.assertEqual([False, True, True, True], DirUtil.getIndexAndDateUsageInFileNameLst(fileNameLst_index_date_2))
		self.assertEqual([False, True, False, True], DirUtil.getIndexAndDateUsageInFileNameLst(fileNameLst_index_no_date))
		self.assertEqual([False, False, False, True], DirUtil.getIndexAndDateUsageInFileNameLst(fileNameLst_no_index_no_date))
		self.assertEqual([False, False, True, True], DirUtil.getIndexAndDateUsageInFileNameLst(fileNameLst_no_index_date))
		self.assertEqual([False, False, False, False], DirUtil.getIndexAndDateUsageInFileNameLst(emptyFileNameLst))

	def testGetIndexAndDateUsageInDir(self):
		"""
		DOWNLOAD_DATE_UPLOAD_DATE_POS = 0
		DOWNLOAD_DATE_NO_UPLOAD_DATE_POS = 1
		NO_DOWNLOAD_DATE_UPLOAD_DATE_POS = 2
		NO_DOWNLOAD_DATE_NO_UPLOAD_DATE_POS = 3
		"""
		testDirName = 'test warning index date files'
		testDirNameSaved = 'test warning index date files save dir'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		testPath = testAudioDirRoot + sep + testDirName
		testPathSaved = testAudioDirRoot + sep + testDirNameSaved
		
		# restoring test dir
		
		if os.path.exists(testPath):
			shutil.rmtree(testPath)
		
		shutil.copytree(testPathSaved, testPath)

		self.assertEqual([True, True, True, True], DirUtil.getIndexAndDateUsageInDir(testPath))
		
		# removing test dir so that it is not uploaded on GitHub
		DirUtil.deleteDirAndItsSubDirs(testPath)
	
	def testGetIndexAndDateUsageInDir_noPrefix_suffix(self):
		"""
		DOWNLOAD_DATE_UPLOAD_DATE_POS = 0
		DOWNLOAD_DATE_NO_UPLOAD_DATE_POS = 1
		NO_DOWNLOAD_DATE_UPLOAD_DATE_POS = 2
		NO_DOWNLOAD_DATE_NO_UPLOAD_DATE_POS = 3
		"""
		testDirName = 'test warning index date files_noIndexDate'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		testPath = testAudioDirRoot + sep + testDirName
		
		self.assertEqual([False, False, True, True], DirUtil.getIndexAndDateUsageInDir(testPath))
	
	def testGetIndexAndDateUsageInDir_prefix_noSuffix_and_noPrefixNoSuffix(self):
		"""
		DOWNLOAD_DATE_UPLOAD_DATE_POS = 0
		DOWNLOAD_DATE_NO_UPLOAD_DATE_POS = 1
		NO_DOWNLOAD_DATE_UPLOAD_DATE_POS = 2
		NO_DOWNLOAD_DATE_NO_UPLOAD_DATE_POS = 3
		"""
		testDirName = 'test warning index date files_indexNoDate'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		testPath = testAudioDirRoot + sep + testDirName
		
		self.assertEqual([False, True, False, True], DirUtil.getIndexAndDateUsageInDir(testPath))
	
	def testGetIndexAndDateUsageInDir_prefix_noSuffix_only(self):
		"""
		DOWNLOAD_DATE_UPLOAD_DATE_POS = 0
		DOWNLOAD_DATE_NO_UPLOAD_DATE_POS = 1
		NO_DOWNLOAD_DATE_UPLOAD_DATE_POS = 2
		NO_DOWNLOAD_DATE_NO_UPLOAD_DATE_POS = 3
		"""
		testDirName = 'test warning index date files_indexNoDate_only'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		testPath = testAudioDirRoot + sep + testDirName
		
		self.assertEqual([False, True, False, False], DirUtil.getIndexAndDateUsageInDir(testPath))
	
	def testGetIndexAndDateUsageInDir_noPrefix_noSuffix(self):
		"""
		DOWNLOAD_DATE_UPLOAD_DATE_POS = 0
		DOWNLOAD_DATE_NO_UPLOAD_DATE_POS = 1
		NO_DOWNLOAD_DATE_UPLOAD_DATE_POS = 2
		NO_DOWNLOAD_DATE_NO_UPLOAD_DATE_POS = 3
		"""
		testDirName = 'test warning index date files_noIndexNoDate'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		testPath = testAudioDirRoot + sep + testDirName
		
		self.assertEqual([False, False, False, True], DirUtil.getIndexAndDateUsageInDir(testPath))
	
	def testGetIndexAndDateUsageInEmptyDir(self):
		"""
		DOWNLOAD_DATE_UPLOAD_DATE_POS = 0
		DOWNLOAD_DATE_NO_UPLOAD_DATE_POS = 1
		NO_DOWNLOAD_DATE_UPLOAD_DATE_POS = 2
		NO_DOWNLOAD_DATE_NO_UPLOAD_DATE_POS = 3
		"""
		testDirName = 'test warning index date files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		testPath = testAudioDirRoot + sep + testDirName
		
		# emptying test dir
		
		if os.path.exists(testPath):
			shutil.rmtree(testPath)
			
		DirUtil.createTargetDirIfNotExist(rootDir=testAudioDirRoot,
										  targetAudioDir=testPath)
		
		self.assertEqual([], DirUtil.getIndexAndDateUsageInDir(testPath))
		
		# removing test dir so that it is not uploaded on GitHub
		DirUtil.deleteDirAndItsSubDirs(testPath)
	
	def testGetIndexAndDateUsageInDirNotExist(self):
		testDirName = 'test warning index date files not exist'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		testPath = testAudioDirRoot + sep + testDirName
		
		self.assertIsNone(DirUtil.getIndexAndDateUsageInDir(testPath))

	def testReplaceStringsInFiles(self):
		testAudioRootPath = DirUtil.getTestAudioRootPath()
		searchRootDir = testAudioRootPath + sep + "test_DirUtil_replace"  # Windows audio dir
		searchRootDirSaved = searchRootDir + '_saved'
		#	searchRootDir = '/storage/9016-4EF8/Audio'  # smartphone audio dir
		#	searchRootDir = '/storage/emulated/0/Music' # tablet audio dir
		fileNamePattern = '*_dic.txt'
		inSubDirs = True
		text_to_searchLst = ['pl_downloadSubDir', 'downl', 'vd_downlFileName']
		replacement_textLst = ['pl_downlSubDirAAA', 'downlAAA', 'vd_downlFileNameAAA']

		# restoring dic text files
		
		if os.path.exists(searchRootDir):
			shutil.rmtree(searchRootDir)

		shutil.copytree(searchRootDirSaved, searchRootDir)
		
		modifiedPlaylistName_1 = 'test warning index date files'
		downloadplaylistinfodicFilePathName_1 = searchRootDir + sep + 'test warning index false date false files' + sep + modifiedPlaylistName_1 + DownloadPlaylistInfoDic.DIC_FILE_NAME_EXTENT
		modifiedPlaylistName_2 = 'test warning index date files'
		downloadplaylistinfodicFilePathName_2 = searchRootDir + sep + 'test warning index false date true files' + sep + modifiedPlaylistName_2 + DownloadPlaylistInfoDic.DIC_FILE_NAME_EXTENT
		
		downloadPlaylistInfoDic_1 = DownloadPlaylistInfoDic(modifiedPlaylistName=modifiedPlaylistName_1,
		                                                    existingDicFilePathName=downloadplaylistinfodicFilePathName_1)


		self.assertEqual(modifiedPlaylistName_1, downloadPlaylistInfoDic_1.getDicDirSubDir())
		
		downloadPlaylistInfoDic_2 = DownloadPlaylistInfoDic(modifiedPlaylistName=modifiedPlaylistName_2,
		                                                    existingDicFilePathName=downloadplaylistinfodicFilePathName_2)


		self.assertEqual(modifiedPlaylistName_2, downloadPlaylistInfoDic_2.getDicDirSubDir())

		DirUtil.replaceStringsInFiles(searchRootDir,
									  fileNamePattern,
									  inSubDirs,
									  text_to_searchLst,
									  replacement_textLst)
		
		downloadPlaylistInfoDic_reloaded_2 = DownloadPlaylistInfoDic(modifiedPlaylistName=modifiedPlaylistName_2,
		                                                             existingDicFilePathName=downloadplaylistinfodicFilePathName_2)

		self.assertRaises(KeyError, downloadPlaylistInfoDic_reloaded_2.getDicDirSubDir)
		
		# removing test dir so that it is not uploaded on GitHub
		DirUtil.deleteDirAndItsSubDirs(searchRootDir)
	
	def testDeleteFilesInDirForPattern(self):
		testAudioRootPath = DirUtil.getTestAudioRootPath()
		searchRootDir = testAudioRootPath + sep + "test_DirUtil_replace"  # Windows audio dir
		searchRootDirSaved = searchRootDir + '_saved'
		#	searchRootDir = '/storage/9016-4EF8/Audio'  # smartphone audio dir
		#	searchRootDir = '/storage/emulated/0/Music' # tablet audio dir
		fileNamePattern = '*_dic.txt'
		inSubDirs = True
		
		# restoring dic text files
		
		if os.path.exists(searchRootDir):
			shutil.rmtree(searchRootDir)
		
		shutil.copytree(searchRootDirSaved, searchRootDir)
		
		self.assertEqual(['{}\\test_DirUtil_replace\\test '
		                  'warning index date files save dir\\test warning index date files_dic.txt'.format(testAudioRootPath),
		                  '{}\\test_DirUtil_replace\\test '
		                  'warning index false date false files\\test warning index date files_dic.txt'.format(testAudioRootPath),
		                  '{}\\test_DirUtil_replace\\test '
		                  'warning index false date true files\\test warning index date files_dic.txt'.format(testAudioRootPath)],
		                 DirUtil.getFilePathNamesInDirForPattern(targetDir=searchRootDir,
		                                                         fileNamePattern=fileNamePattern,
		                                                         inSubDirs=inSubDirs))
		
		DirUtil.deleteFilesInDirForPattern(searchRootDir,
		                                   fileNamePattern,
		                                   inSubDirs)

		self.assertEqual([], DirUtil.getFilePathNamesInDirForPattern(targetDir=searchRootDir,
		                                                             fileNamePattern=fileNamePattern,
		                                                             inSubDirs=inSubDirs))
		
		# removing test dir so that it is not uploaded on GitHub
		DirUtil.deleteDirAndItsSubDirs(searchRootDir)
	
	def testGetAudioFilesSortedByDateInfoList(self):
		testDirName = 'testDownloadFilesHisto'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		testPath = testAudioDirRoot + sep + testDirName
		
		audioFileHistoryLst = DirUtil.getAudioFilesSortedByDateInfoList(targetDir=testPath,
		                                                                excludedSubDirNameLst=['Excluded dir'])
		self.assertEqual([['JMJ',  [['Here to help - Give him what he wants.mp3', '220222'],   ['200310-exploreAudio.mp3', '220222']]], ['Crypto',  [['Funny suspicious looking dog.mp3', '220222'],   ['98-Here to help - Give him what he wants.mp3', '220222']]]],
		                 audioFileHistoryLst)

		'''
		for audioSubDirLst in audioFileHistoryLst:
			print(audioSubDirLst[0])
			for audioFileNameSubList in audioSubDirLst[1]:
				print('\t', audioFileNameSubList)
		'''
		
	def testDeleteAudioFiles(self):
		testRootDir = DirUtil.getTestAudioRootPath() + sep + "test_DirUtil_deletePartialNameAudioFiles"  # Windows audio dir
		testRootDirSaved = testRootDir + '_saved'
		
		# restoring dic text files
		
		if os.path.exists(testRootDir):
			shutil.rmtree(testRootDir)
		
		shutil.copytree(testRootDirSaved, testRootDir)
		
		self.assertEqual(['D:\\Development\\Python\\audiodownload\\test\\testData\\test_DirUtil_deletePartialNameAudioFiles\\EMI\\211224-Nouveau '
 'document texte jjjhmhfhmgfj zkuztuz.mp3',
 'D:\\Development\\Python\\audiodownload\\test\\testData\\test_DirUtil_deletePartialNameAudioFiles\\EMI\\211224-Nouveau '
 'document texte.mp3',
 'D:\\Development\\Python\\audiodownload\\test\\testData\\test_DirUtil_deletePartialNameAudioFiles\\EMI\\Nouveau '
 'document text_dic.txt',
 'D:\\Development\\Python\\audiodownload\\test\\testData\\test_DirUtil_deletePartialNameAudioFiles\\Politique\\220324-Nouveau '
 'document texte.mp3',
 'D:\\Development\\Python\\audiodownload\\test\\testData\\test_DirUtil_deletePartialNameAudioFiles\\Politique\\Nouveau '
 'document texte.mp3'],
		                 DirUtil.getFilePathNamesInDirForPattern(targetDir=testRootDir,
		                                                         fileNamePattern='*.*',
				                                                 inSubDirs=True))
		delFileDic = {}
		delFileDic['Politique'] = ['220324-Nouveau document texte.mp3', 'Nouveau document texte.mp3']
		delFileDic['EMI'] = ['211224-Nouveau document texte jjjhmhfhmgfj zkuztuz.mp3']

		deletedFileNameLst, deletedFilePathNameLst = DirUtil.deleteAudioFiles(testRootDir, delFileDic)
		
		self.assertEqual(['220324-Nouveau document texte.mp3',
 'Nouveau document texte.mp3',
 '211224-Nouveau document texte jjjhmhfhmgfj zkuztuz.mp3'], deletedFileNameLst)
		self.assertEqual(['Politique\\220324-Nouveau document texte.mp3',
 'Politique\\Nouveau document texte.mp3',
 'EMI\\211224-Nouveau document texte jjjhmhfhmgfj zkuztuz.mp3'], deletedFilePathNameLst)
		self.assertEqual(['D:\\Development\\Python\\audiodownload\\test\\testData\\test_DirUtil_deletePartialNameAudioFiles\\EMI\\211224-Nouveau '
 'document texte.mp3',
 'D:\\Development\\Python\\audiodownload\\test\\testData\\test_DirUtil_deletePartialNameAudioFiles\\EMI\\Nouveau '
 'document text_dic.txt'],
		                 DirUtil.getFilePathNamesInDirForPattern(targetDir=testRootDir,
		                                                         fileNamePattern='*.*',
				                                                 inSubDirs=True))
		
		# removing test dir so that it is not uploaded on GitHub
		DirUtil.deleteDirAndItsSubDirs(testRootDir)
	
	def testDeleteAudioFiles_playlist_dir_not_exist(self):
		testRootDir = DirUtil.getTestAudioRootPath() + sep + "test_DirUtil_deletePartialNameAudioFiles"  # Windows audio dir
		testRootDirSaved = testRootDir + '_saved'
		
		# restoring dic text files
		
		if os.path.exists(testRootDir):
			shutil.rmtree(testRootDir)
		
		shutil.copytree(testRootDirSaved, testRootDir)
		
		self.assertEqual([
			                 'D:\\Development\\Python\\audiodownload\\test\\testData\\test_DirUtil_deletePartialNameAudioFiles\\EMI\\211224-Nouveau '
			                 'document texte jjjhmhfhmgfj zkuztuz.mp3',
			                 'D:\\Development\\Python\\audiodownload\\test\\testData\\test_DirUtil_deletePartialNameAudioFiles\\EMI\\211224-Nouveau '
			                 'document texte.mp3',
			                 'D:\\Development\\Python\\audiodownload\\test\\testData\\test_DirUtil_deletePartialNameAudioFiles\\EMI\\Nouveau '
			                 'document text_dic.txt',
			                 'D:\\Development\\Python\\audiodownload\\test\\testData\\test_DirUtil_deletePartialNameAudioFiles\\Politique\\220324-Nouveau '
			                 'document texte.mp3',
			                 'D:\\Development\\Python\\audiodownload\\test\\testData\\test_DirUtil_deletePartialNameAudioFiles\\Politique\\Nouveau '
			                 'document texte.mp3'],
		                 DirUtil.getFilePathNamesInDirForPattern(targetDir=testRootDir,
		                                                         fileNamePattern='*.*',
		                                                         inSubDirs=True))
		delFileDic = {}
		delFileDic['Politique'] = ['220324-Nouveau document texte.mp3', 'Nouveau document texte.mp3']
		delFileDic['Playlist not exist'] = ['211226-Nouveau document texte jjjhmhfhmgfj']
		delFileDic['EMI'] = ['211224-Nouveau document texte jjjhmhfhmgfj zkuztuz.mp3']

		deletedFileNameLst, deletedFilePathNameLst = DirUtil.deleteAudioFiles(testRootDir, delFileDic)
		
		self.assertEqual(['220324-Nouveau document texte.mp3',
 'Nouveau document texte.mp3',
 '211224-Nouveau document texte jjjhmhfhmgfj zkuztuz.mp3'], deletedFileNameLst)
		self.assertEqual(['Politique\\220324-Nouveau document texte.mp3',
		                  'Politique\\Nouveau document texte.mp3',
		                  'EMI\\211224-Nouveau document texte jjjhmhfhmgfj zkuztuz.mp3'], deletedFilePathNameLst)
		self.assertEqual([
			                 'D:\\Development\\Python\\audiodownload\\test\\testData\\test_DirUtil_deletePartialNameAudioFiles\\EMI\\211224-Nouveau '
			                 'document texte.mp3',
			                 'D:\\Development\\Python\\audiodownload\\test\\testData\\test_DirUtil_deletePartialNameAudioFiles\\EMI\\Nouveau '
			                 'document text_dic.txt'],
		                 DirUtil.getFilePathNamesInDirForPattern(targetDir=testRootDir,
		                                                         fileNamePattern='*.*',
		                                                         inSubDirs=True))
		
		# removing test dir so that it is not uploaded on GitHub
		DirUtil.deleteDirAndItsSubDirs(testRootDir)
	
	def testGetListOfFilesCreatedOrModifiedBeforeOrAfterRefFileDate(self):
		playlistDir = 'C:\\Users\\Jean-Pierre\\Downloads\\Audio\\test_DirUtil_getListOfFilesCreatedOrModifiedBeforeDate'

		testRootDir = DirUtil.getTestAudioRootPath() + sep + "test_DirUtil_getListOfFilesCreatedOrModifiedBeforeDate"  # Windows audio dir
		testRootDirSaved = testRootDir + '_saved'
		
		# restoring dic text files
		
		if os.path.exists(playlistDir):
			shutil.rmtree(playlistDir)
		
		shutil.copytree(testRootDirSaved, playlistDir)
		
		time.sleep(1.0)
		
		playlistDicFileName = 'test_small_videos_3_dic.txt'
		
		with open(playlistDir + sep + playlistDicFileName, 'a') as f:
			f.write('\n')

		time.sleep(1.0)

		shutil.copy2('C:\\Users\\Jean-Pierre\\Downloads\\Audio\\test_DirUtil_getListOfFilesCreatedOrModifiedBeforeDate\\220625-Lama Tanz 15-06-11.mp3',
		             'C:\\Users\\Jean-Pierre\\Downloads\\Audio\\test_DirUtil_getListOfFilesCreatedOrModifiedBeforeDate\\220625-Lama Tanz 15-06-11_copy.mp3')
		
		expectedAllFileNameLstBefore = [
			'220625-Indian 🇮🇳_American🇺🇸_ Japanese🇯🇵_Students #youtubeshorts #shorts _Samayra Narula_ Subscribe  21-09-17.mp3',
			'220625-Innovation (Short Film) 20-01-07.mp3',
			'220625-Lama Tanz 15-06-11.mp3']

		expectedAllFilePathNameLstBefore = [
			'C:\\Users\\Jean-Pierre\\Downloads\\Audio\\test_DirUtil_getListOfFilesCreatedOrModifiedBeforeDate\\220625-Indian 🇮🇳_American🇺🇸_ Japanese🇯🇵_Students #youtubeshorts #shorts _Samayra Narula_ Subscribe  21-09-17.mp3',
			'C:\\Users\\Jean-Pierre\\Downloads\\Audio\\test_DirUtil_getListOfFilesCreatedOrModifiedBeforeDate\\220625-Innovation (Short Film) 20-01-07.mp3',
			'C:\\Users\\Jean-Pierre\\Downloads\\Audio\\test_DirUtil_getListOfFilesCreatedOrModifiedBeforeDate\\220625-Lama Tanz 15-06-11.mp3']
		
		expectedAllFileNameLstAfter = ['220625-Lama Tanz 15-06-11_copy.mp3']

		expectedAllFilePathNameLstAfter = [
			'C:\\Users\\Jean-Pierre\\Downloads\\Audio\\test_DirUtil_getListOfFilesCreatedOrModifiedBeforeDate\\220625-Lama Tanz 15-06-11_copy.mp3']

		fileNameLstBefore, filePathNameLstBefore, fileNameLstAfter, filePathNameLstAfter = DirUtil.getListOfFilesCreatedOrModifiedBeforeOrAfterRefFileDate(playlistDir, playlistDicFileName)
		self.assertEqual(sorted(expectedAllFileNameLstBefore), sorted(fileNameLstBefore))
		self.assertEqual(sorted(expectedAllFilePathNameLstBefore), sorted(filePathNameLstBefore))
		self.assertEqual(sorted(expectedAllFileNameLstAfter), sorted(fileNameLstAfter))
		self.assertEqual(sorted(expectedAllFilePathNameLstAfter), sorted(filePathNameLstAfter))

if __name__ == '__main__':
	# unittest.main()
	tst = TestDirUtil()
	tst.testGetListOfFilesCreatedOrModifiedBeforeOrAfterRefFileDate()