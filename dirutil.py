import os
from os import listdir
from os.path import isfile, join, sep

class DirUtil:
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