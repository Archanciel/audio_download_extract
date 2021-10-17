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
		targetAudioDirShort = DirUtil.getLastSubDirs(targetAudioDir, subDirsNumber=2)
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
	def getFullDirMinusRootDir(rootDir,
	                           fullDir,
	                           remainingRootSubDirNumber=None):
		if remainingRootSubDirNumber is None:
			return fullDir.replace(rootDir + sep, '')
		
		rootDirElementLst = rootDir.split(sep)
		remainingRootDir = sep.join(rootDirElementLst[:-remainingRootSubDirNumber])
		targetAudioDirShort = fullDir.replace(remainingRootDir + sep, '')
		
		return targetAudioDirShort
	
	@staticmethod
	def getFileNamesInDir(targetAudioDir):
		return [f for f in listdir(targetAudioDir) if isfile(join(targetAudioDir, f))]
	
	@staticmethod
	def replaceUnauthorizedDirOrFileNameChars(rawFileName):
		"""
		This method replaces chars in the passed raw file name which are unauthorized on
		Windows.
		
		:param rawFileName:
		:return:
		"""
		charToReplace = {'\\': '',
		                 '/': '_', # since YoutubeDL replaces / by _
		                 ':': '',
		                 '*': ' ',
		                 '.': '',
		                 '?': '',
		                 '"': "'", # since YoutubeDL replaces " by '
		                 '<': '',
		                 '>': '',
		                 '|': '',
		                 "'": '_'}
		
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
		os.rename(originalFilePathName, newFilePathName)
