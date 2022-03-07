from os.path import sep

from configmanager import ConfigManager
from dirutil import DirUtil

class ConfigManagerStub(ConfigManager):
	@property
	def dataPath(self):
		return DirUtil.getTestAudioRootPath()
	
	@property
	def singleVideoDataPath(self):
		return DirUtil.getTestAudioRootPath() + sep + 'Various'
