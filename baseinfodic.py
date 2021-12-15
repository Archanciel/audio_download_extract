from abc import ABCMeta, abstractmethod

import json
import os
from os.path import sep

from dirutil import DirUtil


class BaseInfoDic(metaclass=ABCMeta):
	"""
	This base class contains code used in its sub-classes.
	"""
	DIC_FILE_NAME_EXTENT = '_dic.txt'
	
	def __init__(self):
		self.dic = None
	
	def _loadDicIfExist(self, dicFilePathName):
		"""
		If a file containing the dictionary data for the corresponding playlist
		exists, it is loaded using json.
		
		:param dicFilePathName:
		
		:return None or loaded dictionary
		"""
		dic = None

		if os.path.isfile(dicFilePathName):
			with open(dicFilePathName, 'r') as f:
				dic = json.load(f)

		return dic
	
	def __str__(self):
		try:
			return json.dumps(self.dic, sort_keys=False, indent=4)
		except Exception as e:
			print(e)
	
	def saveDic(self, audioDirRoot, dicFilePathName=None):
		"""
		
		:param audioDirRoot: audio dir as defined in the GUI settings.
		:param dicFilePathName: not None in case of DownloadUrlInfoDic.
		"""
		if dicFilePathName is None:
			validPlaylistDirName = DirUtil.replaceUnauthorizedDirOrFileNameChars(self.getDicDirName())
			playlistDownloadDir = self.getDicDirSubDir()
			
			dicFilePathName = self.buildInfoDicFilePathName(playlistDownloadBaseDir=audioDirRoot + sep + playlistDownloadDir,
			                                                validPlaylistDirName=validPlaylistDirName)

		with open(dicFilePathName, 'w') as f:
			try:
				json.dump(self.dic,
						  f,
						  indent=4,
						  sort_keys=True)
			except Exception as e:
				print(self)
				print(e)

	@abstractmethod
	def getDicDirName(self):
		pass

	@abstractmethod
	def getDicDirSubDir(self):
		pass
	
	def buildInfoDicFilePathName(self, playlistDownloadBaseDir, validPlaylistDirName):
		"""
		Builds the playlist DownloadVideoInfoDic file path name.
		
		:param playlistDownloadBaseDir: base playlist download dir as defined in the
										SelectOrCreateDirFileChooserPopup dir field or
										audio root dir by default.
		:param validPlaylistDirName:    contains the playlistName purged from any invalid
										Windows dir or file names chars.

		:return: playlist DownloadVideoInfoDic file path name
		"""
		return playlistDownloadBaseDir + sep + validPlaylistDirName + BaseInfoDic.DIC_FILE_NAME_EXTENT
