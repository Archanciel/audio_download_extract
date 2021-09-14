import os
from os import listdir
from os.path import isfile, join, sep

from constants import RV_LIST_ITEM_SPACING_WINDOWS
from pathlib import Path
from os.path import sep

class DirUtil:
	@staticmethod
	def getAudioRootPath():
		if os.name == 'posix':
			audioRootPath = '/sdcard/'
		else:
			audioRootPath = str(Path.home() / "Downloads" / 'Audio')

		return audioRootPath
	
	@staticmethod
	def getTestAudioRootPath():
		audioRootPath = DirUtil.getAudioRootPath()
		
		return audioRootPath + sep + 'test'
	
	@staticmethod
	def extractPathFromPathFileName(pathFileName):
		pathElemLst = pathFileName.split(sep)

		return sep.join(pathElemLst[:-1])

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
	def createTargetDirIfNotExist(targetAudioDir):
		targetAudioDirList = targetAudioDir.split(sep)
		targetAudioDirShort = sep.join(targetAudioDirList[-2:])
		dirCreationMessage = None
		
		if not os.path.isdir(targetAudioDir):
			os.makedirs(targetAudioDir)
			dirCreationMessage = "directory\n{}\nwas created.\n".format(targetAudioDirShort)
		
		return targetAudioDirShort, dirCreationMessage
	
	@staticmethod
	def purgeIllegalWinFileNameChar(videoTitle):
		"""
		This method eliminates the characters which are not accepted in file names
		on Windows.

		:param videoTitle:
		:return:
		"""
		return videoTitle.replace('/', '_').replace(':', '_').replace('?', '')
	
	@staticmethod
	def getFileNamesInDir(targetAudioDir):
		return [f for f in listdir(targetAudioDir) if isfile(join(targetAudioDir, f))]
	
	@staticmethod
	def replaceUnauthorizedDirNameChars(rawFileName):
		"""
		This method replaces chars in the passed raw file name which are unauthorized on
		Windows.

		:param rawFileName:
		:return:
		"""
		charToReplace = {'\\': '',
		                 '/': ' ',
		                 ':': '',
		                 '*': ' ',
		                 '?': '',
		                 '"': '',
		                 '<': '',
		                 '>': '',
		                 '|': ''}
		
		# Replace all multiple characters in a string
		# based on translation table created by dictionary
		validFileName = rawFileName.translate(str.maketrans(charToReplace))
		
		return validFileName.strip()
