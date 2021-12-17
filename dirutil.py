import glob
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
from os.path import sep
import shutil
import re


INDEX_PATTERN = r'(^[\d-]*)(.*).mp3'
DATE_PATTERN = r'(.*) ([\d-]*).mp3'

class DirUtil:
	INDEX_DATE_POS = 0
	INDEX_NO_DATE_POS = 1
	NO_INDEX_DATE_POS = 2
	NO_INDEX_NO_DATE_POS = 3
	
	@staticmethod
	def getDefaultAudioRootPath():
		"""
		Essentially used by ConfigManager to initialize the default audio
		root path. Since this information can be modified with the settings
		dialog which updates the audiodownload.ini file, obtaining the
		real audiobook root path must be done using the ConfigManager.
		
		:return:
		"""
		if os.name == 'posix':
			audioRootPath = '/sdcard/'
		else:
			# Path.home() returns C:\users\my name\ even if my OneDrive folder is
			# on D:\users\my name\ !!!
			audioRootPath = str(Path.home() / "Downloads" / 'Audio')

		return audioRootPath
	
	@staticmethod
	def getTestAudioRootPath():
		audioRootPath = DirUtil.getDefaultAudioRootPath()
		
		return audioRootPath + sep + 'test'
	
	@staticmethod
	def getTestDataPath():
		"""
		Returns the test data path containing the unit test test data. Those
		data are commited to the GitHub project space.
		
		:return example: 'D:\\Development\\Python\\audiodownload\\test\\testData'
		"""
		currentDirPath = os.path.dirname(os.path.realpath(__file__))
		
		return currentDirPath + sep + 'test' + sep + 'testData'
	
	@staticmethod
	def extractPathFromPathFileName(pathFileName):
		pathElemLst = pathFileName.split(sep)

		return sep.join(pathElemLst[:-1])
	
	@staticmethod
	def extractFileNameFromFilePathName(pathFileName):
		pathElemLst = pathFileName.split(sep)
		
		return pathElemLst[-1]
	
	@staticmethod
	def getConfigFilePathName():
		
		configFileName = 'audiodownloader.ini'
		
		if os.name == 'posix':
			configFilePath = '/sdcard/'
			configFilePathName = '%s%s' % (configFilePath, configFileName)
		else:
			configFilePath = str(Path.home() / "Downloads" / 'Audio')
			configFilePathName = configFilePath + sep + configFileName
		
		return configFilePathName
	
	@staticmethod
	def createTargetDirIfNotExist(rootDir,
								  targetAudioDir):
		targetAudioDirShort = DirUtil.getFullFilePathNameMinusRootDir(rootDir=rootDir,
																	  fullFilePathName=targetAudioDir,
																	  eliminatedRootLastSubDirsNumber=1)
		dirCreationMessage = None
		
		if not os.path.isdir(targetAudioDir):
			os.makedirs(targetAudioDir)
			dirCreationMessage = "directory\n{}\nwas created.\n".format(targetAudioDirShort)
		
		return targetAudioDirShort, dirCreationMessage

	@staticmethod
	def getLastSubDirs(fullDir, subDirsNumber):
		fullDirComponentList = fullDir.split(sep)
		targetAudioDirShort = sep.join(fullDirComponentList[-subDirsNumber:])
		
		return targetAudioDirShort

	@staticmethod
	def getFullFilePathNameMinusRootDir(rootDir,
										fullFilePathName,
										eliminatedRootLastSubDirsNumber=None):
		"""
		Return the passed fullFilePathName minus the passed rootDir. Note that
		the passed fullFilePathName may contain only a path.
		
		:param rootDir:
		:param fullFilePathName:
		:param eliminatedRootLastSubDirsNumber: if defined, the passed root dir
												which will be removed from the
												passed fullFilePathName will have
												its eliminatedRootLastSubDirsNumber
												last sub dirs removed.
												
					Example: rootDir = 'C:\\Users\\Jean-Pierre\\Downloads\\Audio'
							 eliminatedRootLastSubDirsNumber = 1
							 root dir removed from fullFilePathName =
							 'C:\\Users\\Jean-Pierre\\Downloads'
							 
							 So, if the passed fullFilePathName =
							 'C:\\Users\\Jean-Pierre\\Downloads\\Audio\\UCEM\\chap 1.mp3',
							 the returned filePathName will be
							 'Audio\\UCEM\\chap 1.mp3'
							 
							 If eliminatedRootLastSubDirsNumber = None,
							 the returned filePathName will be
							 'UCEM\\chap 1.mp3'
		:return:
		"""
		if eliminatedRootLastSubDirsNumber is None or eliminatedRootLastSubDirsNumber == 0:
			return fullFilePathName.replace(rootDir + sep, '')
		
		rootDirElementLst = rootDir.split(sep)
		remainingRootDir = sep.join(rootDirElementLst[:-eliminatedRootLastSubDirsNumber])
		targetAudioDirShort = fullFilePathName.replace(remainingRootDir + sep, '')
		
		return targetAudioDirShort
	
	@staticmethod
	def getFileNamesInDir(targetDir):
		return [f for f in listdir(targetDir) if isfile(join(targetDir, f))]
	
	@staticmethod
	def getFilePathNamesInDirForPattern(targetDir, fileNamePattern, inSubDirs=False):
		if not os.path.isdir(targetDir):
			return None

		return glob.glob(targetDir + sep + fileNamePattern, recursive=inSubDirs)
	
	@staticmethod
	def getFileNamesInDirForPattern(targetDir, fileNamePattern):
		if not os.path.isdir(targetDir):
			return None
		
		filePathNameLst = glob.glob(targetDir + sep + fileNamePattern)
		
		return [DirUtil.extractFileNameFromFilePathName(f) for f in filePathNameLst]
	
	@staticmethod
	def replaceUnauthorizedDirOrFileNameChars(rawFileName):
		"""
		This method replaces chars in the passed raw file name which are
		unauthorized on Windows. The replacements are conform to how
		youtube_dl names the downloaded audio file.
		
		:param rawFileName:
		:return:
		"""
		if rawFileName[-1] == '|':
			rawFileName = rawFileName[:-1]  # since YoutubeDL replaces '|' by '
											# if '|' is located at end of file name !
			
		charToReplace = {
						 '\\': '',
						 '/': '_', # since YoutubeDL replaces '/' by '_'
						 ':': ' -', # since YoutubeDL replaces ':' by ' -'
						 '*': ' ',
						 #'.': '', point is not illegal in file name
						 '?': '',
						 '"': "'", # since YoutubeDL replaces " by '
						 '<': '',
						 '>': '',
						 '|': '_'  # since YoutubeDL replaces '|' by '_'
						 #"'": '_' apostrophe is not illegal in file name
						 }
		
		# Replace all multiple characters in a string
		# based on translation table created by dictionary
		validFileName = rawFileName.translate(str.maketrans(charToReplace))

		# Since YoutubeDL replaces '?' by ' ', determining if a video whose title
		# ends with '?' has already been downloaded using
		# replaceUnauthorizedDirOrFileNameChars(videoTitle) + '.mp3' can be executed
		# if validFileName.strip() is NOT done.
		return validFileName
	
	@staticmethod
	def removeSubDirsContainedInDir(dirsToRemoveContainingDir):
		"""
		Removes recursively the sub dirs contained in the passed
		dirsToRemoveContainingDir. Any file contained in the sub dirs are
		deleted as well.
		
		:param dirsToRemoveContainingDir:
		"""
		if os.path.isdir(dirsToRemoveContainingDir):
			shutil.rmtree(dirsToRemoveContainingDir)
			
	@staticmethod
	def renameFile(originalFilePathName, newFileName):
		newFilePathName = DirUtil.extractPathFromPathFileName(originalFilePathName) + sep + newFileName

		try:
			os.rename(originalFilePathName, newFilePathName)
		except (FileNotFoundError, FileExistsError, OSError) as e:
			return str(e)
		
	@staticmethod
	def deleteFiles(filePathNameLst):
		for filePathName in filePathNameLst:
			DirUtil.deleteFileIfExist(filePathName)
	
	@staticmethod
	def deleteFilesInDirForPattern(targetDir, fileNamePattern):
		filePathNameLst = DirUtil.getFilePathNamesInDirForPattern(targetDir, fileNamePattern)

		if filePathNameLst:
			for filePathName in filePathNameLst:
				DirUtil.deleteFileIfExist(filePathName)
	
	@staticmethod
	def copyFilesInDirToDirForPattern(sourceDir, targetDir, fileNamePattern):
		filePathNameLst = DirUtil.getFilePathNamesInDirForPattern(sourceDir, fileNamePattern)
		
		if filePathNameLst:
			for filePathName in filePathNameLst:
				shutil.copy(filePathName, targetDir)
	
	@staticmethod
	def deleteFileIfExist(filePathName):
		if isfile(filePathName):
			os.remove(filePathName)
	
	@staticmethod
	def getIndexAndDateUsageInDir(audioDir):
		"""
		Returns a four boolean list which corresponds to the usage in the passed
		audioDir of the index and the video upload date.
		
		If one of the audio file name located in the passed audioDir starts
		with an index and ends with a date (for example
		93-Here to help - Give him what he wants 2019-06-07.mp3, then the
		first element of the returned audioFileNameLst is True.
		
		If one of the audio file name located in the passed audioDir starts
		with an index and does not end with a date (for example
		93-Here to help - Give him what he wants.mp3,then the second element
		of the returned audioFileNameLst is True.
		
		If one of the audio file name located in the passed audioDir does not
		start with an index and	does end with a date (for example
		Here to help - Give him what he wants 2019-06-07.mp3, then the
		third element of the returned audioFileNameLst is True.
		
		If one of the audio file name located in the passed audioDir does not
		start with an index and	does not end with a date (for example
		Here to help - Give him what he wants.mp3, then the
		fourth element of the returned audioFileNameLst is True.

		If the passed audioDir is empty, then [] is returned.
		If the passed audioDir does not exist, then None is returned.
		
		:param audioDir:
		
		:return:indexAndDateUsageLst    four boolean elements list or
										None if the passed audioDir does not
										exist or
										[] if the passed audioDir is empty.

										four elements list:  [INDEX_DATE boolean,
															 INDEX_NO_DATE boolean,
															 NO_INDEX_DATE boolean,
															 NO_INDEX_NO_DATE boolean]
	
										the list index are defined by those DirUtil
										constants:
										
										DirUtil.INDEX_DATE_POS = 0
										DirUtil.INDEX_NO_DATE_POS = 1
										DirUtil.NO_INDEX_DATE_POS = 2
										DirUtil.NO_INDEX_NO_DATE_POS = 3

		"""
		audioFileNameLst = DirUtil.getFileNamesInDirForPattern(audioDir, '*.mp3')

		if audioFileNameLst is None or audioFileNameLst == []:
			return audioFileNameLst
		else:
			return DirUtil.getIndexAndDateUsageInFileNameLst(audioFileNameLst)
	
	@staticmethod
	def getIndexAndDateUsageInFileNameLst(audioFileNameLst):
		"""
		Returns a four boolean list which corresponds to the usage in the passed
		audioFileNameLst of the index and the video upload date.
		
		If one of the passed audio file name starts with an index and ends
		with a date (for example
		93-Here to help - Give him what he wants 2019-06-07.mp3, then the
		first element of the returned audioFileNameLst is True.
		
		If one of the passed audio file name starts with an index and does not
		end	with a date (for example 93-Here to help - Give him what he wants.mp3,
		then the second element of the returned audioFileNameLst is True.
		
		If one of the passed audio file name does not start with an index and
		does end with a date (for example
		Here to help - Give him what he wants 2019-06-07.mp3, then the
		third element of the returned audioFileNameLst is True.
		
		If one of the passed audio file name does not start with an index and
		does not end with a date (for example
		Here to help - Give him what he wants.mp3, then the
		fourth element of the returned audioFileNameLst is True.

		If the passed audioFileNameLst was empty, then the returned
		indexAndDateUsageLst would contain four False elements. But this case
		does not happen since this method is called only if the audioFileNameLst
		is not empty.
		
		:param audioFileNameLst:
		
		:return:indexAndDateUsageLst  four elements list:    [INDEX_DATE boolean,
															 INDEX_NO_DATE boolean,
															 NO_INDEX_DATE boolean,
															 NO_INDEX_NO_DATE boolean]

									  the list index are defined by those DirUtil
									  constants:
									  
									  DirUtil.INDEX_DATE_POS = 0
									  DirUtil.INDEX_NO_DATE_POS = 1
									  DirUtil.NO_INDEX_DATE_POS = 2
									  DirUtil.NO_INDEX_NO_DATE_POS = 3

		"""
		indexAndDateUsageLst = [False,  # INDEX_DATE
		                        False,  # INDEX_NO_DATE
		                        False,  # NO_INDEX_DATE
		                        False]  # NO_INDEX_NO_DATE

		for fileName in audioFileNameLst:
			match = re.search(INDEX_PATTERN, fileName)
			
			if match.group(1) != '':
				match = re.search(DATE_PATTERN, fileName)
				if match is not None:
					indexAndDateUsageLst[DirUtil.INDEX_DATE_POS] = True
				else:
					indexAndDateUsageLst[DirUtil.INDEX_NO_DATE_POS] = True
			else:
				match = re.search(DATE_PATTERN, fileName)
				if match is not None:
					indexAndDateUsageLst[DirUtil.NO_INDEX_DATE_POS] = True
				else:
					indexAndDateUsageLst[DirUtil.NO_INDEX_NO_DATE_POS] = True
			
		return indexAndDateUsageLst


if __name__ == '__main__':
	# PUT THAT IN UNIT TESTS !
	"""
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
	
	def printLst(lst):
		print('Index_date {}, index_no_date {}, no_index_date {}, no_index_no_date {}\n'.
		      format(lst[DirUtil.INDEX_DATE_POS],
		             lst[DirUtil.INDEX_NO_DATE_POS],
		             lst[DirUtil.NO_INDEX_DATE_POS],
		             lst[DirUtil.NO_INDEX_NO_DATE_POS]))
	
	print('fileNameLst_index_date_1')
	lst_1 = DirUtil.getIndexAndDateUsageInFileNameLst(fileNameLst_index_date_1)
	printLst(lst_1)
	print('fileNameLst_index_date_2')
	lst_2 = DirUtil.getIndexAndDateUsageInFileNameLst(fileNameLst_index_date_2)
	printLst(lst_2)
	print('fileNameLst_index_no_date')
	lst_3 = DirUtil.getIndexAndDateUsageInFileNameLst(fileNameLst_index_no_date)
	printLst(lst_3)
	print('fileNameLst_no_index_no_date')
	lst_4 = DirUtil.getIndexAndDateUsageInFileNameLst(fileNameLst_no_index_no_date)
	printLst(lst_4)
	print('fileNameLst_no_index_date')
	lst_5 = DirUtil.getIndexAndDateUsageInFileNameLst(fileNameLst_no_index_date)
	printLst(lst_5)
	"""
	#lst = DirUtil.getFilePathNamesInDirForPattern('/storage/emulated/0/Music','/**/*_dic.txt', True)
	lst = DirUtil.getFilePathNamesInDirForPattern('/storage/9016-4EF8/Audio','/**/*_dic.txt', True)
	#print(glob.glob('/storage/emulated/0/Music/**/*_dic.txt', recursive=True))
	import fileinput

	text_to_searchLst = ['pl_downloadDir', 'download', 'vd_downledFileName']
	replacement_textLst = ['pl_downlSubDir', 'downl', 'vd_downlFileName']
		
	for text_to_search, replacement_text in zip(text_to_searchLst, replacement_textLst):
		for fp in lst:
			with fileinput.FileInput(fp, inplace=True, backup='.bak') as file:
				for line in file:
					print(line.replace(text_to_search, replacement_text), end='')
	