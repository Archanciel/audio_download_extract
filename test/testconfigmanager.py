import unittest
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from configmanager import ConfigManager


class TestConfigManager(unittest.TestCase):
	def setUp(self):
		configFileName = 'audiodownloader_test.ini'
	
		if os.name == 'posix':
			self.configFilePath = '/sdcard/'
			self.configFilePathName = '%s%s' % (self.configFilePath, configFileName)
		else:
			self.configFilePath = 'c:\\temp\\'
			self.configFilePathName = '%s%s' % (self.configFilePath, configFileName)


	def testConfigManagerInstanciationWithNoConfigFile(self):
		os.remove(self.configFilePathName)
		configMgr, defaultDataPath = self.instanciateConfigManager()
		
		self.verifyConfigFileDefaultValues(configMgr, defaultDataPath)
	
	
	def verifyConfigFileDefaultValues(self, configMgr, defaultDataPath):
		self.assertEqual(configMgr.dataPath, defaultDataPath)
		
		if os.name == 'posix':
			self.assertEqual('Half', configMgr.appSize)
			self.assertEqual('90', configMgr.histoListItemHeight)
		else:
			self.assertEqual('Full', configMgr.appSize)
			self.assertEqual('35', configMgr.histoListItemHeight)

		self.assertEqual('', configMgr.loadAtStartPathFilename)
		self.assertEqual('3', configMgr.histoListVisibleSize)
		self.assertEqual('0.62', configMgr.appSizeHalfProportion)
	
	def instanciateConfigManager(self):
		if os.name == 'posix':
			defaultDataPath = '/storage/emulated/0/audiodownload_data'
		else:
			defaultDataPath = r'c:\temp\audiodownload_data'

		configMgr = ConfigManager(self.configFilePathName)

		return configMgr, defaultDataPath
	
	def testConfigManagerInstanciationEmptyConfigFile(self):
		# emptying config file so that the recreated config file has default
		# values
		open(self.configFilePathName, 'w').close()
		configMgr, defaultDataPath = self.instanciateConfigManager()
		
		self.verifyConfigFileDefaultValues(configMgr, defaultDataPath)
	
	def testConfigManagerInstanciationOneMissingKey(self):
		#removing second line in config file
		with open(self.configFilePathName, 'r') as configFile:
			lines = configFile.readlines()

		with open(self.configFilePathName, 'w') as configFile:
			# first line contains [General] section name !
			configFile.write(''.join(lines[0:1] + lines[2:]))
		
		with self.assertRaises(KeyError):
			configMgr = ConfigManager(self.configFilePathName)


	def testChangingDefaultValue(self):
		# deleting config file so that the recreated config file has default
		# values
		os.remove(self.configFilePathName)
		configMgr, defaultDataPath = self.instanciateConfigManager()
		
		self.verifyConfigFileDefaultValues(configMgr, defaultDataPath)

		newDataPath = 'new path'
		configMgr.dataPath = newDataPath
		configMgr.saveConfig()

		updatedConfigMgr, _ = self.instanciateConfigManager()

		self.assertEqual(newDataPath, updatedConfigMgr.dataPath)

if __name__ == '__main__':
	#unittest.main()
	tst = TestConfigManager()
	tst.setUp()
	tst.testConfigManagerInstanciationWithNoConfigFile()
	tst.testConfigManagerInstanciationEmptyConfigFile()