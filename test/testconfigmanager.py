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


    def testConfigManagerInstanciation(self):
        self.configMgr = ConfigManager(self.configFilePathName)
        self.assertEqual(self.configMgr.localTimeZone, 'Europe/Zurich')
        self.assertEqual(self.configMgr.dateTimeFormat, 'DD/MM/YY HH:mm')
        self.assertEqual(self.configMgr.dateOnlyFormat, 'DD/MM/YY')
        
        if os.name == 'posix':
            self.assertEqual(self.configMgr.dataPath, '/sdcard/CryptoPricerData')
            self.assertEqual(self.configMgr.appSize, 'Half')
            self.assertEqual(self.configMgr.histoListItemHeight, '90')
        else:
            self.assertEqual(self.configMgr.dataPath, 'c:\\temp')
            self.assertEqual(self.configMgr.appSize, 'Full')
            self.assertEqual(self.configMgr.histoListItemHeight, '35')

        self.assertEqual(self.configMgr.loadAtStartPathFilename, '')
        self.assertEqual(self.configMgr.histoListVisibleSize, '3')
        self.assertEqual(self.configMgr.appSizeHalfProportion, '0.62')
        self.assertEqual(self.configMgr.referenceCurrency, 'USD')


    def testConfigManagerInstanciationNoConfigFile(self):
        os.remove(self.configFilePathName)
        self.configMgr = ConfigManager(self.configFilePathName)
        self.assertEqual(self.configMgr.localTimeZone, 'Europe/Zurich')
        self.assertEqual(self.configMgr.dateTimeFormat, 'DD/MM/YY HH:mm')
        self.assertEqual(self.configMgr.dateOnlyFormat, 'DD/MM/YY')

        if os.name == 'posix':
            self.assertEqual(self.configMgr.dataPath, '/sdcard/CryptoPricerData')
            self.assertEqual(self.configMgr.appSize, 'Half')
            self.assertEqual(self.configMgr.histoListItemHeight, '90')
        else:
            self.assertEqual(self.configMgr.dataPath, 'c:\\temp')
            self.assertEqual(self.configMgr.appSize, 'Full')
            self.assertEqual(self.configMgr.histoListItemHeight, '35')

        self.assertEqual(self.configMgr.loadAtStartPathFilename, '')
        self.assertEqual(self.configMgr.histoListVisibleSize, '3')
        self.assertEqual(self.configMgr.appSizeHalfProportion, '0.62')
        self.assertEqual(self.configMgr.referenceCurrency, 'USD')


    def testConfigManagerInstanciationEmptyConfigFile(self):
        open(self.configFilePathName, 'w').close()
        self.configMgr = ConfigManager(self.configFilePathName)
        self.assertEqual(self.configMgr.localTimeZone, 'Europe/Zurich')
        self.assertEqual(self.configMgr.dateTimeFormat, 'DD/MM/YY HH:mm')
        self.assertEqual(self.configMgr.dateOnlyFormat, 'DD/MM/YY')

        if os.name == 'posix':
            self.assertEqual(self.configMgr.dataPath, '/sdcard/CryptoPricerData')
            self.assertEqual(self.configMgr.appSize, 'Half')
            self.assertEqual(self.configMgr.histoListItemHeight, '90')
        else:
            self.assertEqual(self.configMgr.dataPath, 'c:\\temp')
            self.assertEqual(self.configMgr.appSize, 'Full')
            self.assertEqual(self.configMgr.histoListItemHeight, '35')

        self.assertEqual(self.configMgr.loadAtStartPathFilename, '')
        self.assertEqual(self.configMgr.histoListVisibleSize, '3')
        self.assertEqual(self.configMgr.appSizeHalfProportion, '0.62')
        self.assertEqual(self.configMgr.referenceCurrency, 'USD')


    def testConfigManagerInstanciationOneMissingKey(self):
        #removing second line in config file
        with open(self.configFilePathName, 'r') as configFile:
            lines = configFile.readlines()

        with open(self.configFilePathName, 'w') as configFile:
            # first line contains [General] section name !
            configFile.write(''.join(lines[0:1] + lines[2:]))

        self.configMgr = ConfigManager(self.configFilePathName)
        self.assertEqual(self.configMgr.localTimeZone, 'Europe/Zurich')
        self.assertEqual(self.configMgr.dateTimeFormat, 'DD/MM/YY HH:mm')
        self.assertEqual(self.configMgr.dateOnlyFormat, 'DD/MM/YY')

        if os.name == 'posix':
            self.assertEqual(self.configMgr.dataPath, '/sdcard/CryptoPricerData')
        else:
            self.assertEqual(self.configMgr.dataPath, 'c:\\temp')

        self.assertEqual(self.configMgr.loadAtStartPathFilename, '')
        self.assertEqual(self.configMgr.histoListVisibleSize, '3')
        self.assertEqual(self.configMgr.appSizeHalfProportion, '0.62')
        self.assertEqual(self.configMgr.referenceCurrency, 'USD')


if __name__ == '__main__':
    #unittest.main()
    tst = TestConfigManager()
    tst.setUp()
    tst.testConfigManagerInstanciation()