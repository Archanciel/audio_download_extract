from abc import ABCMeta, abstractmethod

import json
import os
from os.path import sep

from dirutil import DirUtil

KEY_PLAYLIST = 'playlist'
KEY_PLAYLIST_NAME_MODIFIED = 'pl_name_modified'

# playlist download dir name. This name DOES NOT contain the
# audio dir root dir (defined in uthe GUI settings)
KEY_PLAYLIST_DOWNLOAD_DIR = 'pl_downloadDir'


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
	
	def saveDic(self, audioDirRoot):
		"""
		
		:param audioDirRoot: audio dir as defined in the GUI settings.
		:return:
		"""
		validPlaylistDirName = DirUtil.replaceUnauthorizedDirOrFileNameChars(self.getDicDirName())
		playlistDownloadDir = self.getPlaylistDownloadDir()
		
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
	
	def getPlaylistNameModified(self):
		"""
		Return the modified play list name, which is the modified playlist title
		without the optional extract or suppress time frames definitions.

		:return:
		"""
		if KEY_PLAYLIST in self.dic.keys():
			return self.dic[KEY_PLAYLIST][KEY_PLAYLIST_NAME_MODIFIED]
		else:
			return None
	
	def getPlaylistDownloadDir(self):
		"""
		Returns the playlist download dir name. This name does not contain the
		audio dir root dir (defined in the GUI settings).
		
		:return: playlist download dir name
		"""
		if KEY_PLAYLIST in self.dic.keys():
			return self.dic[KEY_PLAYLIST][KEY_PLAYLIST_DOWNLOAD_DIR]
		else:
			return None
	
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
