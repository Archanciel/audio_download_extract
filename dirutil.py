import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
from os.path import sep
import shutil

class DirUtil:
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
		                 '|': ''
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
