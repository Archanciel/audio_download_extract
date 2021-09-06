import os
from configobj import ConfigObj


class ConfigManager:
	# those constants are used outside of ConfigurationManager. For this reason,
	# they are declared inside the class
	CONFIG_SECTION_GENERAL = 'General'
	CONFIG_SECTION_LAYOUT = 'Layout'
	CONFIG_SECTION_MAILTO = 'mailTo'
	
	CONFIG_KEY_DATA_PATH = 'datapath'
	DEFAULT_DATA_PATH_ANDROID = '/storage/emulated/0/audiodownload_data'
	DEFAULT_DATA_PATH_IOS = '~/Documents'
	DEFAULT_DATA_PATH_WINDOWS = 'c:\\temp\\audiodownload_data'
	
	CONFIG_KEY_SINGLE_VIDEO_DATA_PATH = 'singlevideodatapath'
	DEFAULT_SINGLE_VIDEO_DATA_PATH_ANDROID = '/storage/emulated/0/audiodownload_data/various'
	DEFAULT_SINGLE_VIDEO_DATA_PATH_IOS = '~/Documents'
	DEFAULT_SINGLE_VIDEO_DATA_PATH_WINDOWS = 'c:\\temp\\audiodownload_data\\various'
	
	CONFIG_KEY_LOAD_AT_START_PATH_FILENAME = 'loadatstartpathfilename'
	DEFAULT_LOAD_AT_START_PATH_FILENAME = ''
	
	CONFIG_KEY_LOAD_AT_START_SHARE_CONTACTS_PATH_FILENAME = 'loadatstartsharecontactspathfilename'
	DEFAULT_LOAD_AT_START_SHARE_CONTACTS_PATH_FILENAME = ''
	
	CONFIG_KEY_APP_SIZE = 'defaultappsize'
	DEFAULT_CONFIG_KEY_APP_SIZE_HALF_PROPORTION = '0.62'
	
	CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT = 'histolistitemheight'
	DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_ANDROID = '90'
	DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_WINDOWS = '35'
	
	CONFIG_KEY_HISTO_LIST_VISIBLE_SIZE = 'histolistvisiblesize'
	DEFAULT_CONFIG_HISTO_LIST_VISIBLE_SIZE = '3'
	
	CONFIG_KEY_APP_SIZE_HALF_PROPORTION = 'appsizehalfproportion'
	APP_SIZE_HALF = 'Half'
	APP_SIZE_FULL = 'Full'
	
	def __init__(self, configFilePathName):
		self.config = ConfigObj(configFilePathName)
		self._updated = False
		
		if len(self.config) == 0:
			self._setAndStoreDefaultConf()
		
		try:
			self.__dataPath = self.config[self.CONFIG_SECTION_GENERAL][self.CONFIG_KEY_DATA_PATH]
		except KeyError:
			if os.name == 'posix':
				self.__dataPath = self.DEFAULT_DATA_PATH_ANDROID
			else:
				self.__dataPath = self.DEFAULT_DATA_PATH_WINDOWS
			
			self._updated = True
		
		try:
			self.__singleVideoDataPath = self.config[self.CONFIG_SECTION_GENERAL][self.CONFIG_KEY_SINGLE_VIDEO_DATA_PATH]
		except KeyError:
			if os.name == 'posix':
				self.__singleVideoDataPath = self.DEFAULT_SINGLE_VIDEO_DATA_PATH_ANDROID
			else:
				self.__singleVideoDataPath = self.DEFAULT_SINGLE_VIDEO_DATA_PATH_WINDOWS
			
			self._updated = True
		
		try:
			self.__loadAtStartPathFilename = self.config[self.CONFIG_SECTION_GENERAL][
				self.CONFIG_KEY_LOAD_AT_START_PATH_FILENAME]
		except KeyError:
			self.__loadAtStartPathFilename = self.DEFAULT_LOAD_AT_START_PATH_FILENAME
			self._updated = True
		
		try:
			self.__loadAtStartShareContactsPathFilename = self.config[self.CONFIG_SECTION_GENERAL][
				self.CONFIG_KEY_LOAD_AT_START_SHARE_CONTACTS_PATH_FILENAME]
		except KeyError:
			self.__loadAtStartShareContactsPathFilename = self.DEFAULT_LOAD_AT_START_SHARE_CONTACTS_PATH_FILENAME
			self._updated = True
		
		try:
			self.__histoListVisibleSize = self.config[self.CONFIG_SECTION_LAYOUT][
				self.CONFIG_KEY_HISTO_LIST_VISIBLE_SIZE]
		except KeyError:
			self.__histoListVisibleSize = self.DEFAULT_CONFIG_HISTO_LIST_VISIBLE_SIZE
			self._updated = True
		
		try:
			self.__histoListItemHeight = self.config[self.CONFIG_SECTION_LAYOUT][self.CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT]
		except KeyError:
			if os.name == 'posix':
				self.__histoListItemHeight = self.DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_ANDROID
			else:
				self.__histoListItemHeight = self.DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_WINDOWS
			self._updated = True
		
		try:
			self.__appSize = self.config[self.CONFIG_SECTION_LAYOUT][self.CONFIG_KEY_APP_SIZE]
		except KeyError:
			self.__appSize = self.APP_SIZE_HALF
			self._updated = True
		
		try:
			self.__appSizeHalfProportion = self.config[self.CONFIG_SECTION_LAYOUT][
				self.CONFIG_KEY_APP_SIZE_HALF_PROPORTION]
		except KeyError:
			self.__appSizeHalfProportion = self.DEFAULT_CONFIG_KEY_APP_SIZE_HALF_PROPORTION
			self._updated = True
		
		self.saveConfig()  # will save config file in case one config key raised an exception
	
	def getEmailDic(self):
		return self.config[self.CONFIG_SECTION_MAILTO]
	
	def getEmailLst(self):
		emailDic = self.getEmailDic()
		emailNb = len(emailDic.keys())
		emailLst = []
		
		for i in range(1, emailNb + 1):
			key = str(i)
			email = emailDic[key]
			email = [key, email[0], email[1]]
			emailLst.append(email)
		
		return emailLst
	
	def _setAndStoreDefaultConf(self):
		"""
		In case no config file exists or if config file is empty,
		defines default values for config properties. Then creates
		or updates the config file.
		:return: nothing
		"""
		self.config[self.CONFIG_SECTION_GENERAL] = {}
		self.config.comments[self.CONFIG_SECTION_GENERAL] = ["Contains app general parameters"]
		self.config[self.CONFIG_SECTION_LAYOUT] = {}
		self.config.comments[self.CONFIG_SECTION_LAYOUT] = ["Contains GUI layout parameters"]
		self.config[self.CONFIG_SECTION_MAILTO] = {}
		self.config.comments[self.CONFIG_SECTION_MAILTO] = ["Emails to which the audio file can be sent. Format: key = Field order, value list = person name, person email. Example: 1 = Joe Bidden, jbd@gmail.com"]
		
		if os.name == 'posix':
			self.dataPath = self.DEFAULT_DATA_PATH_ANDROID
			self.singleVideoDataPath = self.DEFAULT_SINGLE_VIDEO_DATA_PATH_ANDROID
			self.histoListItemHeight = self.DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_ANDROID
			self.appSize = self.APP_SIZE_HALF
		else:
			self.dataPath = self.DEFAULT_DATA_PATH_WINDOWS
			self.singleVideoDataPath = self.DEFAULT_SINGLE_VIDEO_DATA_PATH_WINDOWS
			self.histoListItemHeight = self.DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_WINDOWS
			self.appSize = self.APP_SIZE_FULL
		
		self.loadAtStartPathFilename = self.DEFAULT_LOAD_AT_START_PATH_FILENAME
		self.loadAtStartShareContactsPathFilename = self.DEFAULT_LOAD_AT_START_SHARE_CONTACTS_PATH_FILENAME
		self.histoListVisibleSize = self.DEFAULT_CONFIG_HISTO_LIST_VISIBLE_SIZE
		self.appSizeHalfProportion = self.DEFAULT_CONFIG_KEY_APP_SIZE_HALF_PROPORTION
		self._updated = True
		
		self.saveConfig()
	
	@property
	def dataPath(self):
		return self.__dataPath
	
	@dataPath.setter
	def dataPath(self, dataPathStr):
		self.__dataPath = dataPathStr
		self._updated = True
	
	@property
	def singleVideoDataPath(self):
		return self.__singleVideoDataPath
	
	@singleVideoDataPath.setter
	def singleVideoDataPath(self, singleVideoDataPathStr):
		self.__singleVideoDataPath = singleVideoDataPathStr
		self._updated = True
	
	@property
	def loadAtStartPathFilename(self):
		return self.__loadAtStartPathFilename
	
	@loadAtStartPathFilename.setter
	def loadAtStartPathFilename(self, loadAtStartPathFilenameStr):
		self.__loadAtStartPathFilename = loadAtStartPathFilenameStr
		self._updated = True
	
	@property
	def loadAtStartShareContactsPathFilename(self):
		return self.__loadAtStartShareContactsPathFilename
	
	@loadAtStartShareContactsPathFilename.setter
	def loadAtStartShareContactsPathFilename(self, loadAtStartShareContactsPathFilenameStr):
		self.__loadAtStartShareContactsPathFilename = loadAtStartShareContactsPathFilenameStr
		self._updated = True
	
	@property
	def histoListVisibleSize(self):
		return self.__histoListVisibleSize
	
	@histoListVisibleSize.setter
	def histoListVisibleSize(self, histoListVisibleSizeStr):
		self.__histoListVisibleSize = histoListVisibleSizeStr
		self._updated = True
	
	@property
	def histoListItemHeight(self):
		return self.__histoListItemHeight
	
	@histoListItemHeight.setter
	def histoListItemHeight(self, histoListItemHeightStr):
		self.__histoListItemHeight = histoListItemHeightStr
		self._updated = True
	
	@property
	def appSize(self):
		return self.__appSize
	
	@appSize.setter
	def appSize(self, appSizeStr):
		self.__appSize = appSizeStr
		self._updated = True
	
	@property
	def appSizeHalfProportion(self):
		return self.__appSizeHalfProportion
	
	@appSizeHalfProportion.setter
	def appSizeHalfProportion(self, appSizeHalfProportionStr):
		self.__appSizeHalfProportion = appSizeHalfProportionStr
		self._updated = True
	
	def saveConfig(self):
		if not self._updated:
			return
		
		self.config[self.CONFIG_SECTION_GENERAL][self.CONFIG_KEY_DATA_PATH] = self.dataPath
		self.config[self.CONFIG_SECTION_GENERAL][self.CONFIG_KEY_SINGLE_VIDEO_DATA_PATH] = self.singleVideoDataPath
		self.config[self.CONFIG_SECTION_GENERAL][
			self.CONFIG_KEY_LOAD_AT_START_PATH_FILENAME] = self.loadAtStartPathFilename
		self.config[self.CONFIG_SECTION_GENERAL][
			self.CONFIG_KEY_LOAD_AT_START_SHARE_CONTACTS_PATH_FILENAME] = self.loadAtStartShareContactsPathFilename
		self.config[self.CONFIG_SECTION_LAYOUT][self.CONFIG_KEY_HISTO_LIST_VISIBLE_SIZE] = self.histoListVisibleSize
		self.config[self.CONFIG_SECTION_LAYOUT][self.CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT] = self.histoListItemHeight
		self.config[self.CONFIG_SECTION_LAYOUT][self.CONFIG_KEY_APP_SIZE] = self.appSize
		self.config[self.CONFIG_SECTION_LAYOUT][self.CONFIG_KEY_APP_SIZE_HALF_PROPORTION] = self.appSizeHalfProportion
		
		self.config.write()
		
		self._updated = False


if __name__ == '__main__':
	if os.name == 'posix':
		FILE_PATH = '/storage/emulated/0/audiodownloader.ini'
	else:
		FILE_PATH = 'c:\\temp\\audiodownloader.ini'
	
	cm = ConfigManager(FILE_PATH)
	
	for mail_address in cm.getEmailLst():
		print(mail_address)
