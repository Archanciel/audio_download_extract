import os
from datetime import datetime
from os.path import sep

from constants import *
from baseinfodic import BaseInfoDic
from urldownloaddata import UrlDownloadData

KEY_GENERAL = 'general'
# key for a 4 elements tuple value.
#
# element 0: total number of downloaded playlists
# element 1: total number of successfully downloaded videos (in playlist or single)
# element 2: total number of failed downloaded videos (in playlist or single)
# element 3: total number of skipped videos (in playlist or single)
KEY_GENERAL_TOTAL_DOWNLOAD_RESULT = 'totalDownlResult'

# key for tuple value containing the indexes of the downloaded playlists which
# had no downloaded video failure, i.e. only video successfully downloaded or
# skipped.
#
# The tuple value also contains the indexes of the successfully downloaded
# single videos.
KEY_GENERAL_URL_IDX_DOWNL_OK = 'urlIdxDownlOk'

# key for tuple value containing the indexes of the downloaded playlists which
# had at least 1 downloaded video failure.
#
# The tuple value also contains the indexes of the failed downloaded
# single videos.
KEY_GENERAL_URL_IDX_DOWNL_FAIL = 'urlIdxDownlFail'

# key for tuple value containing the indexes of the downloaded playlists which
# had at least 1 download skipped video.
#
# The tuple value also contains the indexes of the skipped downloaded single
# videos.
KEY_GENERAL_URL_IDX_DOWNL_SKIP = 'urlIdxDownlSkip'

KEY_GENERAL_URL_LIST_FILE_NAME = 'urlListFileName'

KEY_GENERAL_NEXT_URL_INDEX = 'nextUrlIndex'

KEY_URL = 'urls'
KEY_URL_TYPE = 'type'
KEY_URL_TITLE = 'title'
KEY_URL_URL = 'url'
KEY_URL_DOWNLOAD_TIME = 'downlTime'

# key for a 3 elements tuple value.
#
# element 0: total number of successfully downloaded videos for playlist type
# or 1 or 0 for single video
# element 1: total number of failed downloaded videos for playlist type
# or 1 or 0 for single video
# element 2: total number of skipped videos for playlist type or 1 or 0 for
# single video
KEY_URL_DOWNLOAD_RESULT = 'downlResult'

KEY_URL_DOWNLOAD_DIR = 'downlDir'


class DownloadUrlInfoDic(BaseInfoDic):
	"""
	Stores the playlists or videos information which were added to the URL's
	AudioDownloaderGUI URL's to download list.
	"""
	URL_TYPE_PLAYLIST = 'playlist'
	URL_TYPE_SINGLE_VIDEO = 'video'
	
	def __init__(self,
	             audioRootDir=None,
	             urlListDicFileName=None,
	             generalTotalDownlResultTuple=None,
	             generalTotalDownlSuccessTuple=None,
	             generalTotalDownlFailTuple=None,
	             generalTotalDownlSkipTuple=None,
	             loadDicIfDicFileExist=True,
	             existingDicFilePathName=None):
		"""
		Constructor.
		
		If a file containing the dictionary data for the corresponding playlist
		exist in the passed playlistVideoDownloadDir + playlistValidDirName, it is
		loaded and set into the self.dic instance variable. Otherwise, the self
		dic is initialized with the passed information.
		
		If the passed existingDicFilePathName is not None, which is the case in
		the situation of deleting audio files, the instantiated
		DownloadVideoInfoDic is created with the data contained in the
		DownloadVideoInfoDic file located in the existingDicFilePathName dir.
		
		:param generalTotalDownlResultTuple:                 playlist url to add to the
											download video info div
		:param urlListDicFileName:    base dir set in the GUI settings containing
											the extracted audio files
		:param generalTotalDownlSuccessTuple:        may contain extract and/or suppress information.
											Ex: E_Klein - le temps {(s01:05:52-01:07:23) (s01:05:52-01:07:23)}
		:param originalPlaylistName:        contains only the playlist title part without extract
											and/or suppress information. May contain chars which
											would be unacceptable for Windows dir or file names.
		:param loadDicIfDicFileExist:       set to False if the DownloadVideoInfoDic is created
											in order to pass extraction info to the AudioExtractor.
											Typically when executing
											AudioClipperGUI.createClipFileOnNewThread()
		:param existingDicFilePathName      used only if the DownloadVideoInfoDic
											is instantiated based on this parameter
											only (in the case of processing audio files deletion9
		"""
		super().__init__()

		if existingDicFilePathName is not None:
			# we are in the situation of deleting audio files and so removing
			# their corresponding video entry from the loaded download video
			# info dic
			self.dic = self._loadDicIfExist(existingDicFilePathName)
			
			return  # skipping the rest of the __init__ method in this case

		if loadDicIfDicFileExist:
			# is always True, except when AudioController creates a download info
			# dic in order to set in it clip audio start and end times. In this
			# case, the dic must not be loaded from a file
			playlistVideoDownloadDir = audioRootDir + sep + urlListDicFileName
			self.dic = self._loadDicIfExist(playlistVideoDownloadDir)

		if self.dic is None:
			self.dic = {}
			self.dic[KEY_GENERAL] = {}
			
			self.dic[KEY_GENERAL][KEY_GENERAL_TOTAL_DOWNLOAD_RESULT] = generalTotalDownlResultTuple
			self.dic[KEY_GENERAL][KEY_GENERAL_URL_IDX_DOWNL_OK] = generalTotalDownlSuccessTuple
			self.dic[KEY_GENERAL][KEY_GENERAL_URL_IDX_DOWNL_SKIP] = generalTotalDownlSkipTuple
			self.dic[KEY_GENERAL][KEY_GENERAL_URL_IDX_DOWNL_FAIL] = generalTotalDownlFailTuple
			self.dic[KEY_GENERAL][KEY_GENERAL_NEXT_URL_INDEX] = 1
			self.dic[KEY_GENERAL][KEY_GENERAL_URL_LIST_FILE_NAME] = urlListDicFileName
			self.dic[KEY_URL] = {}

	def getNextUrlIndex(self):
		if KEY_GENERAL in self.dic.keys():
			return self.dic[KEY_GENERAL][KEY_GENERAL_NEXT_URL_INDEX]
		else:
			return None

	def getPlaylistTitleOriginal(self):
		"""
		Return the original play list title, which is the original playlist name +
		the optional extract or suppress time frames definitions.
	
		:return:
		"""
		return self.getUrlListDicFileName()
	
	def getUrlListDicFileName(self):
		"""
		Return the download url dic file name..

		:return:
		"""
		if KEY_GENERAL in self.dic.keys():
			return self.dic[KEY_GENERAL][KEY_GENERAL_URL_LIST_FILE_NAME]
		else:
			return None
	
	def getFailedUrlIndexTuple(self):
		"""
		Returns a tuple containing the indexes of the downloaded playlists which
		had at least 1 failed downloaded video.

		The returned tuple also contains the indexes of the failed downloaded
		single videos.

		:return: failed url index tuple
		"""
		# TODO: add method usage and test or delete the method
		if KEY_GENERAL in self.dic.keys():
			return self.dic[KEY_GENERAL][KEY_GENERAL_URL_IDX_DOWNL_FAIL]
		else:
			return None
	
	def getSkippedUrlIndexTuple(self):
		"""
		Returns a tuple containing the indexes of the downloaded playlists which
		had at least 1 download skipped video.

		The returned tuple also contains the indexes of the skipped downloaded
		single videos.
		
		:return: skipped url index tuple
		"""
		# TODO: add method usage and test or delete the method
		if KEY_GENERAL in self.dic.keys():
			return self.dic[KEY_GENERAL][KEY_GENERAL_URL_IDX_DOWNL_SKIP]
		else:
			return None
	
	def getPlaylistDownloadDir(self):
		"""
		Returns the playlist download dir name. This name does not contain the
		audio dir root dir (defined in the GUI settings).
		
		:return: playlist download dir name
		"""
		# TODO: add method usage and test or delete the method
		if KEY_GENERAL in self.dic.keys():
			return self.dic[KEY_GENERAL][KEY_GENERAL_URL_LIST_FILE_NAME]
		else:
			return None
	
	def getTotalDownloadResultTuple(self):
		"""
		Returns a 4 elements tuple containing:

		at pos 0: total number of downloaded playlists
		at pos 1: total number of successfully downloaded videos (in playlist or single)
		at pos 2: total number of failed downloaded videos (in playlist or single)
		at pos 3: total number of skipped videos (in playlist or single)

		:return: total download result tuple
		"""
		# TODO: add method usage and test or delete the method
		if KEY_GENERAL in self.dic.keys():
			return self.dic[KEY_GENERAL][KEY_GENERAL_TOTAL_DOWNLOAD_RESULT]
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
		return playlistDownloadBaseDir + sep + validPlaylistDirName + DownloadUrlInfoDic.DIC_FILE_NAME_EXTENT
	
	def getUrlTitleForUrlIndex(self, urlIndex):
		urlInfoDic = self._getUrlInfoForUrlIndex(urlIndex)
		
		if KEY_URL_TITLE in urlInfoDic.keys():
			return urlInfoDic[KEY_URL_TITLE]
		else:
			return None
	
	def getUrlTypeForUrlIndex(self, urlIndex):
		urlInfoDic = self._getUrlInfoForUrlIndex(urlIndex)
		
		if KEY_URL_TYPE in urlInfoDic.keys():
			return urlInfoDic[KEY_URL_TYPE]
		else:
			return None
	
	def getUrlForUrlIndex(self, urlIndex):
		urlInfoDic = self._getUrlInfoForUrlIndex(urlIndex)
		
		if KEY_URL_URL in urlInfoDic.keys():
			return urlInfoDic[KEY_URL_URL]
		else:
			return None
	
	def getUrlForUrlTitle(self, urlTitle):
		urlIndex = self.getUrlIndexForUrlTitle(urlTitle)
		
		if urlIndex:
			return self._getUrlInfoForUrlIndex(urlIndex)[KEY_URL_URL]
		else:
			return None
	
	def getUrlDownloadDirForUrlIndex(self, urlIndex):
		videoInfoDic = self._getUrlInfoForUrlIndex(urlIndex)
		
		if KEY_URL_DOWNLOAD_DIR in videoInfoDic.keys():
			return videoInfoDic[KEY_URL_DOWNLOAD_DIR]
		else:
			return None
	
	def getUrlDownloadDirForUrlTitle(self, urlTitle):
		videoIndex = self.getUrlIndexForUrlTitle(urlTitle)

		if videoIndex:
			return self._getUrlInfoForUrlIndex(videoIndex)[KEY_URL_DOWNLOAD_DIR]
		else:
			return None
	
	def getUrlDownloadResultTupleForUrlTitle(self, urlTitle):
		"""
		Returns a 3 elements tuple.
		
			element 0: total number of successfully downloaded videos for playlist type
			or 1 or 0 for single video
			element 1: total number of failed downloaded videos for playlist type
			or 1 or 0 for single video
			element 2: total number of skipped videos for playlist type or 1 or 0 for
			single video
		
		:param urlTitle:
		
		:return:    download result 3 elements tuple or None
		"""
		# TODO: add method usage and test or delete the method
		urlIndex = self.getUrlIndexForUrlTitle(urlTitle)

		if urlIndex:
			videoInfoDic = self._getUrlInfoForUrlIndex(urlIndex)
			if KEY_URL_DOWNLOAD_RESULT in videoInfoDic.keys():
				return videoInfoDic[KEY_URL_DOWNLOAD_RESULT]

		return None
	
	def setUrlDownloadResultTupleForUrlIndex(self,
	                                         urlIndex,
	                                         downloadResultTuple):
		"""
		Sets the video download exception value for the passed video
		index to True if the passed isDownloadSuccess is False, and to
		False otherwise.

		:param urlIndex:
		"""
		# TODO: add method usage and test or delete the method
		self._getUrlInfoForUrlIndex(urlIndex)[KEY_URL_DOWNLOAD_RESULT] = downloadResultTuple

	def getVideoDownloadTimeForVideoTitle(self, videoTitle):
		videoIndex = self.getUrlIndexForUrlTitle(videoTitle)
		
		if videoIndex:
			return self._getUrlInfoForUrlIndex(videoIndex)[KEY_URL_DOWNLOAD_TIME]
		else:
			return None

	def addUrlDownloadData(self,
	                       urlDownloadData):
		"""
		Creates the url info sub-dic for next url index using data contained
		in the passed UrlDownloadData instance.
		:param urlDownloadData:
		"""
		#		logging.info('DownloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex={}, videoTitle={}, downloadedFileName={})'.format(videoIndex, videoTitle, downloadedFileName))
		#		print('addVideoInfoForVideoIndex(videoIndex={}, videoTitle={}, downloadedFileName={})'.format(videoIndex, videoTitle, downloadedFileName))

		if not KEY_URL in self.dic.keys():
			self.dic[KEY_URL] = {}

		urlIndex = self.getNextUrlIndex()
		urlIndexKey = str(urlIndex)

		if not urlIndexKey in self.dic[KEY_URL].keys():
			urlIndexDic = {}
			self.dic[KEY_URL][urlIndexKey] = urlIndexDic
		else:
			urlIndexDic = self.dic[KEY_URL][urlIndexKey]

		additionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_DOWNLOAD_DIC_FILE)

		urlIndexDic[KEY_URL_TYPE] = urlDownloadData.type
		urlIndexDic[KEY_URL_TITLE] = urlDownloadData.title
		urlIndexDic[KEY_URL_URL] = urlDownloadData.url
		urlIndexDic[KEY_URL_DOWNLOAD_DIR] = urlDownloadData.downloadDir
		urlIndexDic[KEY_URL_DOWNLOAD_TIME] = additionTimeStr

		self.dic[KEY_GENERAL][KEY_GENERAL_NEXT_URL_INDEX] = urlIndex + 1

	def addUrlInfo(self,
	               urlType,
	               urlTitle,
	               url,
	               downloadDir):
		"""
		Creates the url info sub-dic for the url index if necessary.
		
		Then, adds to the sub-dic the url title, the url url and the url downloaded
		file name.

		:param urlType:
		:param urlTitle:
		:param url:
		:param downloadDir:
		"""
#		logging.info('DownloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex={}, videoTitle={}, downloadedFileName={})'.format(videoIndex, videoTitle, downloadedFileName))
#		print('addVideoInfoForVideoIndex(videoIndex={}, videoTitle={}, downloadedFileName={})'.format(videoIndex, videoTitle, downloadedFileName))

		if not KEY_URL in self.dic.keys():
			self.dic[KEY_URL] = {}
			
		urlIndex = self.getNextUrlIndex()
		urlIndexKey = str(urlIndex)
		
		if not urlIndexKey in self.dic[KEY_URL].keys():
			urlIndexDic = {}
			self.dic[KEY_URL][urlIndexKey] = urlIndexDic
		else:
			urlIndexDic = self.dic[KEY_URL][urlIndexKey]
			
		additionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_DOWNLOAD_DIC_FILE)

		urlIndexDic[KEY_URL_TYPE] = urlType
		urlIndexDic[KEY_URL_TITLE] = urlTitle
		urlIndexDic[KEY_URL_URL] = url
		urlIndexDic[KEY_URL_DOWNLOAD_DIR] = downloadDir
		urlIndexDic[KEY_URL_DOWNLOAD_TIME] = additionTimeStr

		self.dic[KEY_GENERAL][KEY_GENERAL_NEXT_URL_INDEX] = urlIndex + 1

	def _getUrlInfoForUrlIndex(self, urlIndex):
		'''
		Returns the url info dic associated to the passed url index.
		Protected method used internally only.

		:param urlIndex:
		
		:return: dictionary containing url information or empty dictionary
				 if no url info for the passed url index exist.
		'''
		urlIndex = str(urlIndex)
		
		return self._getUrlInfoForUrlKey(urlIndex)
	
	def _getUrlInfoForUrlKey(self, urlIndex):
		urlInfoDic = None
		try:
			urlInfoDic = self.dic[KEY_URL][urlIndex]
		except KeyError:
			pass
		if urlInfoDic == None:
			urlInfoDic = {}
		return urlInfoDic
	
	def getUrlIndexForUrlTitle(self, urlTitle):
		for key in self.dic[KEY_URL].keys():
			if self.getUrlTitleForUrlIndex(key) == urlTitle:
				return key
		
		return None
	
	def getDicDirName(self):
		return self.getPlaylistTitleOriginal()

	def getDicDirSubDir(self):
		return ''
	
	def getSortedUrlIndexLst(self):
		urlStrKeys = self.dic[KEY_URL].keys()
		intIndexLst = [int(x) for x in urlStrKeys]
		intIndexLst.sort()
		
		return intIndexLst
	
	def getUrlForUrlKey(self, urlKey):
		urlInfoDic = self._getUrlInfoForUrlKey(urlKey)
		
		if KEY_URL_URL in urlInfoDic.keys():
			return urlInfoDic[KEY_URL_URL]
		else:
			return None

	def getUrlDownloadDataForUrlIndex(self, urlIndex):
		urlInfoDic = self._getUrlInfoForUrlIndex(urlIndex)
		
		type = None
		title = None
		url = None
		
		if KEY_URL_TYPE in urlInfoDic.keys():
			type = urlInfoDic[KEY_URL_TYPE]
		
		if KEY_URL_TITLE in urlInfoDic.keys():
			title = urlInfoDic[KEY_URL_TITLE]
		
		if KEY_URL_URL in urlInfoDic.keys():
			url = urlInfoDic[KEY_URL_URL]
		
		return UrlDownloadData(type,
		                       title,
		                       url)
	
	def getAllUrlDownloadDataSortedList(self):
		sortedIndexLst = self.getSortedUrlIndexLst()
		
		return [self.getUrlDownloadDataForUrlIndex(idx) for idx in sortedIndexLst]
		

if __name__ == "__main__":
	if os.name == 'posix':
		audioDir = '/storage/emulated/0/Download/Audiobooks'
	else:
		audioDir = 'C:\\Users\\Jean-Pierre\\Downloads\\Audio'
		
	dui = DownloadUrlInfoDic(
		audioRootDir=audioDir,
		urlListDicFileName='urlListDic',
		generalTotalDownlResultTuple=(13, 4, 7),
		generalTotalDownlSuccessTuple=(3, 5, 1, 1, 2),
		generalTotalDownlFailTuple=(0, 2, 0, 0, 2),
		generalTotalDownlSkipTuple=(1, 2, 0, 0, 4),
		loadDicIfDicFileExist=True,
		existingDicFilePathName=None)
	dui.addUrlInfo(urlType=DownloadUrlInfoDic.URL_TYPE_PLAYLIST,
	               urlTitle='test warning index date files_noIndexNoDate',
	               url='https://youtube.com/playlist?list=PLzwWSJNcZTMRVKblKqskAyseCgsUmhlSc', downloadDir='')
	dui.addUrlInfo(urlType=DownloadUrlInfoDic.URL_TYPE_SINGLE_VIDEO,
	               urlTitle='Here to help: Give him what he wants',
	               url='https://www.youtube.com/watch?v=Eqy6M6qLWGw', downloadDir='')
	dui.saveDic(audioDir)
	
	for udl in dui.getAllUrlDownloadDataSortedList():
		print(udl)
