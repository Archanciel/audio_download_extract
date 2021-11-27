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
	def extractPathFromPathFileName(pathFileName):
		pathElemLst = pathFileName.split(sep)

		return sep.join(pathElemLst[:-1])
	
	@staticmethod
	def extractFileNameFromPathFileName(pathFileName):
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
	def getFileNamesInDir(targetAudioDir):
		return [f for f in listdir(targetAudioDir) if isfile(join(targetAudioDir, f))]
	
	@staticmethod
	def getFilePathNamesInDirForPattern(targetAudioDir, pattern):
		return glob.glob(targetAudioDir + sep + pattern)
	
	@staticmethod
	def getFileNamesInDirForPattern(targetAudioDir, pattern):
		if not os.path.isdir(targetAudioDir):
			return None
		
		filePathNameLst = glob.glob(targetAudioDir + sep + pattern)
		
		return [DirUtil.extractFileNameFromPathFileName(f) for f in filePathNameLst]
	
	@staticmethod
	def replaceUnauthorizedDirOrFileNameChars(rawFileName):
		"""
		This method replaces chars in the passed raw file name which are
		unauthorized on Windows. The replacements are conform to how
		youtube_dl names the downloaded audio file.
		
		:param rawFileName:
		:return:
		"""
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

		If the passed audioDir is empty, then None is returned
		
		:param audioDir:
		
		:return:indexAndDateUsageLst    four boolean elements list or
										None if the passed audioDir does not
										exist or
										[] if the passed audioDir is empty.
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

		If the passed audioFileNameLst is empty, then the returned
		indexAndDateUsageLst contains four False elements.
		
		:param audioFileNameLst:
		
		:return:indexAndDateUsageLst four boolean elements list
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
