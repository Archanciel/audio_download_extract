import os
from datetime import datetime
from os.path import sep

from constants import *
from dirutil import DirUtil
from baseinfodic import BaseInfoDic

KEY_GENERAL = 'general'
KEY_GENERAL_TOTAL_DOWNLOAD_RESULT = 'totalDownlResult'
KEY_GENERAL_URL_IDX_DOWNL_SUCCESS = 'urlIdxDownlSuccess'
KEY_GENERAL_URL_IDX_DOWNL_FAIL = 'urlIdxDownlFail'
KEY_GENERAL_URL_IDX_DOWNL_SKIP = 'urlIdxDownlSkip'

# playlist download dir name. This name DOES NOT contain the
# audio dir root dir (defined in uthe GUI settings)
KEY_PLAYLIST_DOWNLOAD_DIR = 'pl_downloadDir'

KEY_PLAYLIST_NEXT_VIDEO_INDEX = 'pl_nextVideoIndex'

KEY_URL = 'urls'
KEY_URL_TYPE = 'type'
KEY_URL_TITLE = 'title'
KEY_URL_URL = 'url'
KEY_URL_DOWNLOAD_TIME = 'downlTime'
KEY_URL_DOWNLOAD_RESULT = 'downlResult'
KEY_URL_DOWNLOAD_DIR = 'downlDir'

class DownloadUrlInfoDic(BaseInfoDic):
	"""
	Stores the playlists or videos information which were added to the URL's
	AudioDownloaderGUI URL's to download list.
	"""
	wasDicUpdated = False
	cachedRateAccessNumber = 0

	def __init__(self,
	             playlistOrSingleVideoUrl=None,
	             audioRootDir=None,
	             playlistOrSingleVideoDownloadRootPath=None,
	             playlistOrSingleVideoTitle=None,
	             playlistOrSingleVideoName=None,
	             playlistOrSingleVideoLastDownloadDate=None,
	             playlistOrSingleVideoDownloadResultTuple=None,
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
		
		:param playlistOrSingleVideoUrl:                 playlist url to add to the
											download video info div
		:param playlistOrSingleVideoDownloadRootPath:    base dir set in the GUI settings containing
											the extracted audio files
		:param playlistOrSingleVideoTitle:        may contain extract and/or suppress information.
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

		playlistValidDirName = DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistOrSingleVideoName)
		playlistVideoDownloadDir = playlistOrSingleVideoDownloadRootPath + sep + playlistValidDirName

		if loadDicIfDicFileExist:
			# is always True, except when AudioController creates a download info
			# dic in order to set in it clip audio start and end times. In this
			# case, the dic must not be loaded from a file
			infoDicFilePathName = self.buildInfoDicFilePathName(playlistVideoDownloadDir, playlistValidDirName)
			self.dic = self._loadDicIfExist(infoDicFilePathName)

		if self.dic is None:
			self.dic = {}
			self.dic[KEY_GENERAL] = {}
			
			self.dic[KEY_GENERAL][KEY_GENERAL_TOTAL_DOWNLOAD_RESULT] = playlistOrSingleVideoUrl
			self.dic[KEY_GENERAL][KEY_GENERAL_URL_IDX_DOWNL_SUCCESS] = playlistOrSingleVideoTitle
			self.dic[KEY_GENERAL][KEY_GENERAL_URL_IDX_DOWNL_SKIP] = playlistOrSingleVideoName
			self.dic[KEY_GENERAL][KEY_PLAYLIST_DOWNLOAD_DIR] = DirUtil.getFullFilePathNameMinusRootDir(rootDir=audioRootDir,
			                                                                                           fullFilePathName=playlistVideoDownloadDir)
			self.dic[KEY_GENERAL][KEY_PLAYLIST_NEXT_VIDEO_INDEX] = 1
			self.dic[KEY_URL] = {}
	
	def updatePlaylistTitle(self, playlistTitle):
		self.dic[KEY_GENERAL][KEY_GENERAL_URL_IDX_DOWNL_SUCCESS] = playlistTitle

	def buildDownloadDirValue(self, playlistTitle):
		# must be changed !!!
		return playlistTitle

	def getNextVideoIndex(self):
		if KEY_GENERAL in self.dic.keys():
			return self.dic[KEY_GENERAL][KEY_PLAYLIST_NEXT_VIDEO_INDEX]
		else:
			return None
		
	def getPlaylistTitleOriginal(self):
		"""
		Return the original play list title, which is the original playlist name +
		the optional extract or suppress time frames definitions.
	
		:return:
		"""
		if KEY_GENERAL in self.dic.keys():
			return self.dic[KEY_GENERAL][KEY_GENERAL_URL_IDX_DOWNL_SUCCESS]
		else:
			return None
	
	def getPlaylistTitleModified(self):
		"""
		Return the modified play list title, which is the modified playlist name +
		the optional extract or suppress time frames definitions.

		:return:
		"""
		if KEY_GENERAL in self.dic.keys():
			return self.dic[KEY_GENERAL][KEY_GENERAL_URL_IDX_DOWNL_FAIL]
		else:
			return None
	
	def getPlaylistNameOriginal(self):
		"""
		Return the original play list name, which is the original playlist title
		without the optional extract or suppress time frames definitions.
	
		:return:
		"""
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
		if KEY_GENERAL in self.dic.keys():
			return self.dic[KEY_GENERAL][KEY_PLAYLIST_DOWNLOAD_DIR]
		else:
			return None
	
	def getPlaylistUrl(self):
		"""
		Returns the playlist url.

		:return: playlist url
		"""
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
	
	def getVideoIndexStrings(self):
		'''
		Returns a list of video indexes as string.
		
		:return: example: ['1', '2']
		'''
		return list(self.dic[KEY_URL].keys())
	
	def existVideoInfoForVideoTitle(self, videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)
		
		return videoIndex is not None
	
	def getVideoTitleForVideoIndex(self, videoIndex):
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if KEY_URL_TITLE in videoInfoDic.keys():
			return videoInfoDic[KEY_URL_TITLE]
		else:
			return None

	def getVideoUrlForVideoIndex(self, videoIndex):
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if KEY_URL_URL in videoInfoDic.keys():
			return videoInfoDic[KEY_URL_URL]
		else:
			return None
	
	def getVideoUrlForVideoTitle(self, videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)
		
		if videoIndex:
			return self._getVideoInfoForVideoIndex(videoIndex)[KEY_URL_URL]
		else:
			return None
	
	def getVideoAudioFileNameForVideoIndex(self, videoIndex):
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if KEY_URL_DOWNLOAD_DIR in videoInfoDic.keys():
			return videoInfoDic[KEY_URL_DOWNLOAD_DIR]
		else:
			return None
	
	def getVideoAudioFileNameForVideoTitle(self, videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)

		if videoIndex:
			return self._getVideoInfoForVideoIndex(videoIndex)[KEY_URL_DOWNLOAD_DIR]
		else:
			return None
	
	def getVideoDownloadExceptionForVideoTitle(self, videoTitle):
		"""
		Returns True if the video download caused an exception, False
		otherwise
		
		:param videoTitle:
		
		:return:    True if the video download caused an exception,
					False otherwise
		"""
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)
		
		if videoIndex:
			videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
			if KEY_URL_DOWNLOAD_RESULT in videoInfoDic.keys():
				return videoInfoDic[KEY_URL_DOWNLOAD_RESULT]
			else:
				# the case if the DownloadVideoInfoDic is old and does not
				# contain this information
				return False
		else:
			return None
	
	def setVideoDownloadExceptionForVideoTitle(self,
	                                           videoTitle,
	                                           isDownloadSuccess):
		"""
		Sets the video download exception value for the passed video
		title to True if the passed isDownloadSuccess is False, and to
		False otherwise.

		:param videoTitle:
		"""
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)
		
		if videoIndex:
			self.setVideoDownloadExceptionForVideoIndex(videoIndex,
			                                            isDownloadSuccess)
	
	def setVideoDownloadExceptionForVideoIndex(self,
	                                           videoIndex,
	                                           isDownloadSuccess):
		"""
		Sets the video download exception value for the passed video
		index to True if the passed isDownloadSuccess is False, and to
		False otherwise.

		:param videoIndex:
		"""
		self._getVideoInfoForVideoIndex(videoIndex)[KEY_URL_DOWNLOAD_RESULT] = not isDownloadSuccess
	
	def getVideoDownloadTimeForVideoIndex(self, videoIndex):
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if KEY_URL_DOWNLOAD_TIME in videoInfoDic.keys():
			return videoInfoDic[KEY_URL_DOWNLOAD_TIME]
		else:
			return None

	def getVideoDownloadTimeForVideoTitle(self, videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)
		
		if videoIndex:
			return self._getVideoInfoForVideoIndex(videoIndex)[KEY_URL_DOWNLOAD_TIME]
		else:
			return None

	def addVideoInfoForVideoIndex(self,
								  videoIndex,
								  videoTitle,
								  videoUrl,
								  downloadedFileName,
	                              isDownloadSuccess=True):
		"""
		Creates the video info sub-dic for the video index if necessary.
		
		Then, adds to the sub-dic the video title, the video url and the video downloaded
		file name.

		:param videoIndex:
		:param videoTitle:
		:param videoUrl:
		:param downloadedFileName:
		:param isDownloadSuccess
		"""
#		logging.info('DownloadVideoInfoDic.addVideoInfoForVideoIndex(videoIndex={}, videoTitle={}, downloadedFileName={})'.format(videoIndex, videoTitle, downloadedFileName))
#		print('addVideoInfoForVideoIndex(videoIndex={}, videoTitle={}, downloadedFileName={})'.format(videoIndex, videoTitle, downloadedFileName))

		if not KEY_URL in self.dic.keys():
			self.dic[KEY_URL] = {}
			
		videoIndexKey = str(videoIndex)
		
		if not videoIndexKey in self.dic[KEY_URL].keys():
			videoIndexDic = {}
			self.dic[KEY_URL][videoIndexKey] = videoIndexDic
			self.removeVideoDicForVideoTitleIfExist(videoTitle)
		else:
			videoIndexDic = self.dic[KEY_URL][videoIndexKey]
			
		additionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_VIDEO_INFO_FILE)

		videoIndexDic[KEY_URL_TITLE] = videoTitle
		videoIndexDic[KEY_URL_URL] = videoUrl
		videoIndexDic[KEY_URL_DOWNLOAD_DIR] = downloadedFileName
		videoIndexDic[KEY_URL_DOWNLOAD_TIME] = additionTimeStr
		videoIndexDic[KEY_URL_DOWNLOAD_RESULT] = not isDownloadSuccess

		self.dic[KEY_GENERAL][KEY_PLAYLIST_NEXT_VIDEO_INDEX] = videoIndex + 1

	def removeVideoDicForVideoTitleIfExist(self, videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)
		
		if videoIndex:
			del self.dic[KEY_URL][videoIndex]
		
	def removeVideoInfoForVideoTitle(self,
									 videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)

		if videoIndex:
			del self.dic[KEY_URL][videoIndex]
	
	def removeVideoInfoForVideoIndex(self,
									 videoIndex):
		videoIndexStr = str(videoIndex)
		
		if videoIndexStr in self.dic[KEY_URL].keys():
			del self.dic[KEY_URL][videoIndexStr]
	
	def _getVideoInfoForVideoIndex(self, videoIndex):
		'''
		Returns the video info dic associated to the passed video index.
		Protected method used internally only.

		:param videoIndex:
		:return: dictionary containing video information or empty dictionary
				 if no video info for the passed video index exist.
		'''
		videoIndex = str(videoIndex)
		
		videoInfoDic = None
		
		try:
			videoInfoDic = self.dic[KEY_URL][videoIndex]
		except KeyError:
			pass
		
		if videoInfoDic == None:
			videoInfoDic = {}
			
		return videoInfoDic

	def getFailedVideoIndexes(self):
		"""
		Returns a list of download failed video integer indexes.
		
		:return: list of download failed video integer indexes
		"""
		failedVideoIndexLst = []

		for indexKey, videoDic in self.dic[KEY_URL].items():
			
			if videoDic[KEY_URL_DOWNLOAD_RESULT] is True:
				failedVideoIndexLst.append(int(indexKey))
				
		return failedVideoIndexLst
	
	def getVideoIndexForVideoTitle(self, videoTitle):
		for key in self.dic[KEY_URL].keys():
			if self.getVideoTitleForVideoIndex(key) == videoTitle:
				return key
		
		return None
	
	def getVideoIndexForVideoFileName(self, videoFileName):
		for key in self.dic[KEY_URL].keys():
			if self.getVideoAudioFileNameForVideoIndex(key) == videoFileName:
				return key
		
		return None

	def deleteVideoInfoForVideoFileName(self, videoFileName):
		videoIndex = self.getVideoIndexForVideoFileName(videoFileName)
		self.removeVideoInfoForVideoIndex(videoIndex)
	
	def getDicDirName(self):
		return self.getPlaylistTitleOriginal()

	def getDicDirSubDir(self):
		return self.getPlaylistDownloadDir()

if __name__ == "__main__":
	if os.name == 'posix':
		videoAudioDir = '/storage/emulated/0/Download/Audiobooks/various'
	else:
		playlistAudioDir = 'D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks'
		videoAudioDir = 'D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks\\various'
		
	dvi = DownloadUrlInfoDic(playlistOrSingleVideoUrl='https://youtube.com/playlist?list=PLzwWSJNcZTMRx16thPZ3i4u3ZJthdifqo',
	                         audioRootDir=playlistAudioDir,
	                         playlistOrSingleVideoDownloadRootPath=playlistAudioDir,
	                         playlistOrSingleVideoTitle="test_small_videos_3",
	                         playlistOrSingleVideoName="test_small_videos_3",
	                         playlistOrSingleVideoLastDownloadDate="12/12/2021 18:36:48",
	                         playlistOrSingleVideoDownloadResultTuple=(3, 0, 0),
	                         loadDicIfDicFileExist=True,
	                         existingDicFilePathName=None)
	dvi.addVideoInfoForVideoIndex(1, 'Title_vid_1', 'https://youtube.com/watch?v=9iPvLx7gotk', 'Title_vid_1.mp4')
	dvi.addVideoInfoForVideoIndex(2, 'title_vid_2', 'https://youtube.com/watch?v=9iPvL8880999', 'Title_vid_2.mp4')
	a = 2
