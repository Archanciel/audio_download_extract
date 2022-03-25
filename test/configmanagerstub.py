from os.path import sep

from configmanager import ConfigManager
from dirutil import DirUtil

class ConfigManagerStub(ConfigManager):
	'''
	Class used by unit tests so that the audio data path returned by the
	ConfigManager are located in the project test data dir.
	'''
	@property
	def dataPath(self):
		return DirUtil.getTestAudioRootPath()
	
	@property
	def singleVideoDataPath(self):
		return DirUtil.getTestAudioRootPath() + sep + 'Various'
