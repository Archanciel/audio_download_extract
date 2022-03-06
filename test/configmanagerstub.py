from configmanager import ConfigManager
from dirutil import DirUtil

class ConfigManagerStub(ConfigManager):
	@property
	def dataPath(self):
		return DirUtil.getTestAudioRootPath()
