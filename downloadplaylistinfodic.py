import os
import posixpath
import re
from datetime import datetime
from os.path import sep
import logging

from constants import *
from dirutil import DirUtil
from baseinfodic import BaseInfoDic
from playlistvideoindexinfo import PlaylistVideoIndexInfo

METHOD_FAILED_VIDEO_INDEX = 0
METHOD_REDOWNLOADED_VIDEO_INDEX = 1

DATE_PREFIX_PATTERN = r'(^[\d]{6})-.+.mp3'

KEY_PLAYLIST = 'playlist'
KEY_PLAYLIST_URL = 'pl_url'
KEY_PLAYLIST_TITLE_ORIGINAL = 'pl_title_original'
KEY_PLAYLIST_TITLE_MODIFIED = 'pl_title_modified'
KEY_PLAYLIST_NAME_ORIGINAL = 'pl_name_original'
KEY_PLAYLIST_NAME_MODIFIED = 'pl_name_modified'

# playlist download dir name. This name DOES NOT contain the
# audio dir root dir (defined in the GUI settings).
#
# Example:

# if the playlistDownloadRootPath ___init__() parm equals
# C:\\Users\\Jean-Pierre\\Downloads\\Audio\\zz\\UCEM\\Gary Renard
# then the playlist download sub dir will be
# zz\\UCEM\\Gary Renard\\<playlist valid name>
#
# if the playlistDownloadRootPath ___init__() parm equals
# C:\\Users\\Jean-Pierre\\Downloads\\Audio, i.e the audio
# root path, then the playlist download sub dir will be
# <playlist valid name> only.
KEY_PLAYLIST_DOWNLOAD_SUB_DIR = 'pl_downlSubDir'

KEY_PLAYLIST_NEXT_VIDEO_INDEX = 'pl_nextVideoIndex'

KEY_VIDEOS = 'videos'
KEY_VIDEO_TITLE = 'vd_title'
KEY_VIDEO_URL = 'vd_url'
KEY_VIDEO_DOWNLOAD_FILENAME = 'vd_downlFileName'
KEY_VIDEO_DOWNLOAD_TIME = 'vd_downlTime'
KEY_VIDEO_TIME_FRAMES_IN_SECONDS = 'vd_startEndTimeFramesInSeconds'
KEY_VIDEO_DOWNLOAD_EXCEPTION = 'vd_downlException'

KEY_TIMEFRAME_EXTRACT = 'vd_extract'
KEY_VIDEO_EXTRACTED_FILES = 'vd_extractedFiles'
KEY_FILENAME = 'ex_fileName'
KEY_FILE_TIMEFRAME_HHMMSS = 'ex_startEndTimeFrameHHMMSS'

KEY_TIMEFRAME_SUPPRESS = 'vd_suppress'
KEY_VIDEO_SUPPRESS_FILE = 'sp_fileName'
KEY_TIMEFRAMES_HHMMSS_SUPPRESSED = 'sp_startEndTimeFramesHHMMSS_suppressed'
KEY_TIMEFRAMES_HHMMSS_KEPT = 'sp_startEndTimeFramesHHMMSS_kept'

class DownloadPlaylistInfoDic(BaseInfoDic):
	"""
	Stores the downloaded playlist information as well as the playlist videos
	information.
	"""
	
	def __init__(self,
	             playlistUrl=None,
	             audioRootDir=None,
	             playlistDownloadRootPath=None,
	             originalPaylistTitle=None,
	             originalPlaylistName=None,
	             modifiedPlaylistTitle=None,
	             modifiedPlaylistName=None,
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
		
		:param playlistUrl:                 playlist url to add to the
											download video info div
		:param audioRootDir:                base dir set in the GUI settings containing
											the extracted audio files
		:param playlistDownloadRootPath:    if the playlist is downloaded without
											modifying its download dir by clicking
											on the "Select or create dir" button,
											then the playlistDownloadRootPath is
											equal to the audioRootDir. Otherwise,
											its value is the dir selected or created
											where the playlist will be downloaded.
											In fact, audioRootDir + the selected or
											created sub-dir(s). For example:
											C:\\Users\\Jean-Pierre\\Downloads\\Audio\\
											zz\\UCEM\\Gary Renard
		:param originalPaylistTitle:        may contain extract and/or suppress information.
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
											only (in the case of processing audio files deletion)
		"""
		super().__init__()
		self.dic = None

		if existingDicFilePathName is not None:
			# we are in the situation of deleting audio files and so removing
			# their corresponding video entry from the loaded download video
			# info dic
			self.dic = self._loadDicIfExist(existingDicFilePathName)
			
			return  # skipping the rest of the __init__ method in this case

		playlistValidDirName = DirUtil.replaceUnauthorizedDirOrFileNameChars(modifiedPlaylistName)
		playlistVideoDownloadDir = playlistDownloadRootPath + sep + playlistValidDirName
		
		if loadDicIfDicFileExist:
			# is always True, except when AudioController creates a download info
			# dic in order to set in it clip audio start and end times. In this
			# case, the dic must not be loaded from a file
			infoDicFilePathName = self.buildInfoDicFilePathName(playlistVideoDownloadDir, playlistValidDirName)
			self.dic = self._loadDicIfExist(infoDicFilePathName)
		
		if self.dic is None:
			self.dic = {}
			self.dic[KEY_PLAYLIST] = {}
			
			if modifiedPlaylistTitle is None:
				modifiedPlaylistTitle = originalPaylistTitle
				
			if modifiedPlaylistName is None:
				modifiedPlaylistName = originalPlaylistName
				
			self.dic[KEY_PLAYLIST][KEY_PLAYLIST_URL] = playlistUrl
			self.dic[KEY_PLAYLIST][KEY_PLAYLIST_TITLE_ORIGINAL] = originalPaylistTitle
			self.dic[KEY_PLAYLIST][KEY_PLAYLIST_TITLE_MODIFIED] = modifiedPlaylistTitle
			self.dic[KEY_PLAYLIST][KEY_PLAYLIST_NAME_ORIGINAL] = originalPlaylistName
			self.dic[KEY_PLAYLIST][KEY_PLAYLIST_NAME_MODIFIED] = modifiedPlaylistName
			self.dic[KEY_PLAYLIST][KEY_PLAYLIST_DOWNLOAD_SUB_DIR] = DirUtil.getFullFilePathNameMinusRootDir(rootDir=audioRootDir,
			                                                                                                fullFilePathName=playlistVideoDownloadDir)
			self.dic[KEY_PLAYLIST][KEY_PLAYLIST_NEXT_VIDEO_INDEX] = 1
			self.dic[KEY_VIDEOS] = {}
	
	def updatePlaylistTitle(self, playlistTitle):
		self.dic[KEY_PLAYLIST][KEY_PLAYLIST_TITLE_ORIGINAL] = playlistTitle

	def updateOriginalPlaylistName(self, originalPlaylistName):
		self.dic[KEY_PLAYLIST][KEY_PLAYLIST_NAME_ORIGINAL] = originalPlaylistName

	def updateModifiedPlaylistName(self, modifiedPlaylistName):
		self.dic[KEY_PLAYLIST][KEY_PLAYLIST_NAME_MODIFIED] = modifiedPlaylistName

	def buildDownloadDirValue(self, playlistTitle):
		# must be changed !!!
		return playlistTitle
	
	def getNextVideoIndex(self):
		if KEY_PLAYLIST in self.dic.keys():
			return self.dic[KEY_PLAYLIST][KEY_PLAYLIST_NEXT_VIDEO_INDEX]
		else:
			return None
		
	def getPlaylistTitleOriginal(self):
		"""
		Return the original play list title, which is the original playlist name +
		the optional extract or suppress time frames definitions.
	
		:return:
		"""
		if KEY_PLAYLIST in self.dic.keys():
			return self.dic[KEY_PLAYLIST][KEY_PLAYLIST_TITLE_ORIGINAL]
		else:
			return None
	
	def getPlaylistTitleModified(self):
		"""
		Return the modified play list title, which is the modified playlist name +
		the optional extract or suppress time frames definitions. Note that
		if the original playlist name or title were not modified, the modified playlist
		name or title value are set to the original name or title value !
		Ex:
		original playlist name = test_audio_downloader_two_files_with_time_frames
		modified playlist name = test_audio_downloader_two_files_with_time_frames
		original playlist title = test_audio_downloader_two_files_with_time_frames (e0:0:2-0:0:8) (s0:0:2-0:0:5 s0:0:7-0:0:10)
		modified playlist title = test_audio_downloader_two_files_with_time_frames (e0:0:2-0:0:8) (s0:0:2-0:0:5 s0:0:7-0:0:10)

		:return:
		"""
		if KEY_PLAYLIST in self.dic.keys():
			return self.dic[KEY_PLAYLIST][KEY_PLAYLIST_TITLE_MODIFIED]
		else:
			return None
	
	def getPlaylistNameOriginal(self):
		"""
		Return the original play list name, which is the original playlist title
		without the optional extract or suppress time frames definitions.
	
		:return:
		"""
		if KEY_PLAYLIST in self.dic.keys():
			return self.dic[KEY_PLAYLIST][KEY_PLAYLIST_NAME_ORIGINAL]
		else:
			return None
	
	def getPlaylistUrl(self):
		"""
		Returns the playlist url.

		:return: playlist url
		"""
		if KEY_PLAYLIST in self.dic.keys():
			if KEY_PLAYLIST_URL in self.dic[KEY_PLAYLIST].keys():
				return self.dic[KEY_PLAYLIST][KEY_PLAYLIST_URL]
			else:
				logging.info('key {} not found in {} dic file located in {}!'.format(KEY_PLAYLIST_URL, self.getPlaylistNameModified(), self.getPlaylistDownloadSubDir()))
				return None
		else:
			return None
	
	def getVideoIndexStrings(self):
		'''
		Returns a list of video indexes as string.
		
		:return: example: ['1', '2']
		'''
		return list(self.dic[KEY_VIDEOS].keys())
	
	def existVideoInfoForVideoTitle(self, videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)
		
		return videoIndex is not None
	
	def getVideoTitleForVideoIndex(self, videoIndex):
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if KEY_VIDEO_TITLE in videoInfoDic.keys():
			return videoInfoDic[KEY_VIDEO_TITLE]
		else:
			return None

	def getVideoUrlForVideoIndex(self, videoIndex):
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if KEY_VIDEO_URL in videoInfoDic.keys():
			return videoInfoDic[KEY_VIDEO_URL]
		else:
			return None
	
	def getVideoUrlForVideoTitle(self, videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)
		
		if videoIndex:
			return self._getVideoInfoForVideoIndex(videoIndex)[KEY_VIDEO_URL]
		else:
			return None
	
	def getVideoUrlForVideoFileName(self, videoFileName):
		videoIndex = self.getVideoIndexForVideoFileName(videoFileName)
		
		if videoIndex:
			return self._getVideoInfoForVideoIndex(videoIndex)[KEY_VIDEO_URL]
		else:
			return None
	
	def getVideoAudioFileNameForVideoIndex(self, videoIndex):
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if KEY_VIDEO_DOWNLOAD_FILENAME in videoInfoDic.keys():
			return videoInfoDic[KEY_VIDEO_DOWNLOAD_FILENAME]
		else:
			return None
	
	def getVideoAudioFileNameForVideoTitle(self, videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)

		if videoIndex:
			return self._getVideoInfoForVideoIndex(videoIndex)[KEY_VIDEO_DOWNLOAD_FILENAME]
		else:
			return None

	def getVideoDownloadExceptionForVideoFileName(self, videoFileName):
		"""
		Returns True if the video download caused an exception, False
		otherwise

		:param videoFileName:

		:return:    True if the video download caused an exception,
					False otherwise
		"""
		videoIndex = self.getVideoIndexForVideoFileName(videoFileName)
		
		if videoIndex:
			videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
			if KEY_VIDEO_DOWNLOAD_EXCEPTION in videoInfoDic.keys():
				return videoInfoDic[KEY_VIDEO_DOWNLOAD_EXCEPTION]
			else:
				# the case if the DownloadVideoInfoDic is old and does not
				# contain this information
				return False
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
			if KEY_VIDEO_DOWNLOAD_EXCEPTION in videoInfoDic.keys():
				return videoInfoDic[KEY_VIDEO_DOWNLOAD_EXCEPTION]
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
		self._getVideoInfoForVideoIndex(videoIndex)[KEY_VIDEO_DOWNLOAD_EXCEPTION] = not isDownloadSuccess
	
	def setVideoAudioFileNameForVideoIndex(self,
	                                       videoIndex,
	                                       audioFileName):
		"""
		Sets the video download exception value for the passed video
		index to True if the passed isDownloadSuccess is False, and to
		False otherwise.

		:param videoIndex:
		"""
		self._getVideoInfoForVideoIndex(videoIndex)[KEY_VIDEO_DOWNLOAD_FILENAME] = audioFileName
	
	def setVideoDownloadTimeForVideoIndex(self, videoIndex, videoDownloadTimeStr):
		self._getVideoInfoForVideoIndex(videoIndex)[KEY_VIDEO_DOWNLOAD_TIME] = videoDownloadTimeStr
	
	def getVideoDownloadTimeForVideoIndex(self, videoIndex):
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if KEY_VIDEO_DOWNLOAD_TIME in videoInfoDic.keys():
			return videoInfoDic[KEY_VIDEO_DOWNLOAD_TIME]
		else:
			return None

	def getVideoDownloadTimeForVideoTitle(self, videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)
		
		if videoIndex:
			return self._getVideoInfoForVideoIndex(videoIndex)[KEY_VIDEO_DOWNLOAD_TIME]
		else:
			return None

	def isExtractTimeFrameDataAvailableForVideoIndex(self, videoIndex):
		if KEY_VIDEO_TIME_FRAMES_IN_SECONDS in self.dic[KEY_VIDEOS][videoIndex].keys():
			if KEY_TIMEFRAME_EXTRACT in self.dic[KEY_VIDEOS][videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS]:
				return self.dic[KEY_VIDEOS][videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS][KEY_TIMEFRAME_EXTRACT] != []
		
		return False
	
	def isSuppressTimeFrameDataAvailableForVideoIndex(self, videoIndex):
		if KEY_VIDEO_TIME_FRAMES_IN_SECONDS in self.dic[KEY_VIDEOS][videoIndex].keys():
			if KEY_TIMEFRAME_SUPPRESS in self.dic[KEY_VIDEOS][videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS]:
				return self.dic[KEY_VIDEOS][videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS][KEY_TIMEFRAME_SUPPRESS] != []
		
		return False
	
	def _addTimeFrameDataForVideo(self, videoIndex):
		'''
		Protected method used internally only.
		
		:param videoIndex:
		:return:
		'''
		videoTimeFramesDic = {KEY_TIMEFRAME_EXTRACT: [], KEY_TIMEFRAME_SUPPRESS: []}
		
		self.dic[KEY_VIDEOS][videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS] = videoTimeFramesDic

	def removeTimeFrameInSecondsDataIfExistForVideoIndex(self, videoIndex):
		videoIndex = str(videoIndex)
		
		if not videoIndex in self.dic[KEY_VIDEOS].keys():
			return

		if not KEY_VIDEO_TIME_FRAMES_IN_SECONDS in self.dic[KEY_VIDEOS][videoIndex].keys():
			return
		else:
			del self.dic[KEY_VIDEOS][videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS]

	def addExtractStartEndSecondsListForVideoIndex(self, videoIndex, startEndSecondsList):
		videoIndex = str(videoIndex)
		
		if not videoIndex in self.dic[KEY_VIDEOS].keys():
			self.dic[KEY_VIDEOS][videoIndex] = {}

		if not KEY_VIDEO_TIME_FRAMES_IN_SECONDS in self.dic[KEY_VIDEOS][videoIndex].keys():
			self._addTimeFrameDataForVideo(videoIndex)
		
		self.dic[KEY_VIDEOS][videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS][KEY_TIMEFRAME_EXTRACT].append(startEndSecondsList)
	
	def addSuppressStartEndSecondsListForVideoIndex(self, videoIndex, startEndSecondsList):
		videoIndex = str(videoIndex)

		if not videoIndex in self.dic[KEY_VIDEOS].keys():
			self.dic[KEY_VIDEOS][videoIndex] = {}
		
		if not KEY_VIDEO_TIME_FRAMES_IN_SECONDS in self.dic[KEY_VIDEOS][videoIndex].keys():
			self._addTimeFrameDataForVideo(videoIndex)
		
		self.dic[KEY_VIDEOS][videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS][KEY_TIMEFRAME_SUPPRESS].append(startEndSecondsList)

	def getExtractStartEndSecondsListsForVideoIndex(self, videoIndex):
		videoIndex = str(videoIndex)

		if not videoIndex in self.dic[KEY_VIDEOS].keys():
			return None

		if KEY_VIDEO_TIME_FRAMES_IN_SECONDS in self.dic[KEY_VIDEOS][videoIndex].keys():
			return self.dic[KEY_VIDEOS][videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS][KEY_TIMEFRAME_EXTRACT]
		else:
			return None
	
	def getSuppressStartEndSecondsListsForVideoIndex(self, videoIndex):
		videoIndex = str(videoIndex)

		if not videoIndex in self.dic[KEY_VIDEOS].keys():
			return None

		if KEY_VIDEO_TIME_FRAMES_IN_SECONDS in self.dic[KEY_VIDEOS][videoIndex].keys():
			return self.dic[KEY_VIDEOS][videoIndex][KEY_VIDEO_TIME_FRAMES_IN_SECONDS][KEY_TIMEFRAME_SUPPRESS]
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

		if not KEY_VIDEOS in self.dic.keys():
			self.dic[KEY_VIDEOS] = {}
			
		videoIndexKey = str(videoIndex)
		
		if not videoIndexKey in self.dic[KEY_VIDEOS].keys():
			videoIndexDic = {}
			self.dic[KEY_VIDEOS][videoIndexKey] = videoIndexDic
			
			# if we are re-downloading a video whose previous download
			# was unsuccessful, it is necessary to remove its video info
			# dic since it will be replaced by the newly created dic.
			self.removeVideoDicForVideoTitleIfExist(videoTitle)
		else:
			videoIndexDic = self.dic[KEY_VIDEOS][videoIndexKey]
			
		additionTimeStr = DownloadPlaylistInfoDic.getNowDownloadDateTimeStr()

		videoIndexDic[KEY_VIDEO_TITLE] = videoTitle
		videoIndexDic[KEY_VIDEO_URL] = videoUrl
		videoIndexDic[KEY_VIDEO_DOWNLOAD_FILENAME] = downloadedFileName
		videoIndexDic[KEY_VIDEO_DOWNLOAD_TIME] = additionTimeStr
		videoIndexDic[KEY_VIDEO_DOWNLOAD_EXCEPTION] = not isDownloadSuccess

		self.dic[KEY_PLAYLIST][KEY_PLAYLIST_NEXT_VIDEO_INDEX] = videoIndex + 1
	
	@staticmethod
	def getNowDownloadDateTimeStr():
		return datetime.now().strftime(DATE_TIME_FORMAT_DOWNLOAD_DIC_FILE)
	
	def removeVideoDicForVideoTitleIfExist(self, videoTitle):
		"""
		If we are re-downloading a video whose previous download
		was unsuccessful, it is necessary to remove its video info
		dic since it will be replaced by the newly created dic.
		
		:param videoTitle:
		"""
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)
		
		if videoIndex:
			del self.dic[KEY_VIDEOS][videoIndex]
		
	def removeVideoInfoForVideoTitle(self,
									 videoTitle):
		videoIndex = self.getVideoIndexForVideoTitle(videoTitle)

		if videoIndex:
			del self.dic[KEY_VIDEOS][videoIndex]
	
	def removeVideoInfoForVideoIndex(self,
									 videoIndex):
		videoIndexStr = str(videoIndex)
		
		if videoIndexStr in self.dic[KEY_VIDEOS].keys():
			del self.dic[KEY_VIDEOS][videoIndexStr]
	
	def _getVideoInfoForVideoIndex(self, videoIndex):
		'''
		Returns the video info dic associated to the passed video index.
		Protected method used internally only.

		:param videoIndex: int index
		:return: dictionary containing video information or empty dictionary
				 if no video info for the passed video index exist.
		'''
		videoIndex = str(videoIndex)
		
		videoInfoDic = None
		
		try:
			videoInfoDic = self.dic[KEY_VIDEOS][videoIndex]
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

		for indexKey, videoDic in self.dic[KEY_VIDEOS].items():
			try:
				if videoDic[KEY_VIDEO_DOWNLOAD_EXCEPTION] is True:
					failedVideoIndexLst.append(int(indexKey))
			except KeyError:
				# old playlist entries have no KEY_VIDEO_DOWNLOAD_EXCEPTION field.
				# So, trying to redownload them due to download failure has no sense !
				pass
				
		return failedVideoIndexLst
	
	def getVideoIndexForVideoTitle(self, videoTitle):
		for key in self.dic[KEY_VIDEOS].keys():
			if self.getVideoTitleForVideoIndex(key) == videoTitle:
				return key
		
		return None
	
	def getVideoIndexForVideoFileName(self, videoFileName):
		videoFileNameNoExt = videoFileName.replace('.mp3', '')

		for key in self.dic[KEY_VIDEOS].keys():
			videoFileNameForVideoIndex = self.getVideoAudioFileNameForVideoIndex(key)
			if videoFileNameNoExt in videoFileNameForVideoIndex:
				return key
		
		return None
	
	def addExtractedFileInfoForVideoIndexTimeFrameIndex(self,
														videoIndex,
														timeFrameIndex,
														extractedFileName,
														startEndHHMMSS_TimeFramesList):
		"""
		Creates the extracted files info dic if necessary.
		
		Then, adds to the sub-dic the extracted file name and its corresponding
		time frame in HH:MM:SS format.
		
		:param videoIndex:
		:param timeFrameIndex:
		:param extractedFileName:
		:param HHMMSS_timeFramesList. Example ['0:23:45', '0:24:54']
		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		extractedFilesSubDic = {}
		timeFrameIndex = str(timeFrameIndex)
		
		if KEY_VIDEO_EXTRACTED_FILES not in videoInfoDic.keys():
			videoInfoDic[KEY_VIDEO_EXTRACTED_FILES] = extractedFilesSubDic
		else:
			extractedFilesSubDic = videoInfoDic[KEY_VIDEO_EXTRACTED_FILES]
			
		extractedFilesSubDic[timeFrameIndex] = {KEY_FILENAME: extractedFileName,
												KEY_FILE_TIMEFRAME_HHMMSS: startEndHHMMSS_TimeFramesList}
	
	def isExtractedFileInfoAvailableForVideoIndex(self, videoIndex):
		"""
		Returns True if extract info for the passed video index exist. This means
		that the audio portions for the concerned video were already extracted.

		:param videoIndex:
		
		:return True or False
		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		return KEY_VIDEO_EXTRACTED_FILES in videoInfoDic.keys()
	
	def getStartEndHHMMSS_TimeFrameForExtractedFileName(self, videoIndex, extractedFileName):
		"""
		Returns the time frame in HH:MM:SS format for the passed extracted file name
		extracted from the video videoIndexKey.

		Unlike suppressing audio portions which produces only one mp3 file per
		video, extracting audio portions produces potentially more than one
		mp3 file per video. So, obtaining a start end HHMMSS time frame list
		for a video index is nonsensical !
		
		:param videoIndex:
		:param extractedFileName:

		:return: startEndHHMMSS time frame list. Example: ['0:23:45', '0:24:54']
		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)

		if KEY_VIDEO_EXTRACTED_FILES not in videoInfoDic.keys():
			return None
		else:
			extractedFilesSubDic = videoInfoDic[KEY_VIDEO_EXTRACTED_FILES]
			
			for key in extractedFilesSubDic.keys():
				if extractedFileName == extractedFilesSubDic[key][KEY_FILENAME]:
					return extractedFilesSubDic[key][KEY_FILE_TIMEFRAME_HHMMSS]
	
	def getExtractedFilePathNameForVideoIndexTimeFrameIndex(self,
															videoIndex,
															timeFrameIndex):
		"""
		Returns the extracted file path name for the passed video index and
		time frame index.

		:param videoIndex:
		:param timeFrameIndex:

		:return: file path name. Example:
				 D:\\\\Users\\\\Jean-Pierre\\\\Downloads\\\\Audiobooks\\\\Various\\\\Wear a mask. Help slow the spread of Covid-19._1.mp3
		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if KEY_VIDEO_EXTRACTED_FILES not in videoInfoDic.keys():
			return None
		else:
			extractedFilesSubDic = videoInfoDic[KEY_VIDEO_EXTRACTED_FILES]
			timeFrameIndexExtractedFileInfo = extractedFilesSubDic[str(timeFrameIndex)]
			
			return self.getPlaylistDownloadSubDir() + sep + timeFrameIndexExtractedFileInfo[KEY_FILENAME]
	
	def addSuppressedFileInfoForVideoIndex(self,
										   videoIndex,
										   suppressedFileName,
										   HHMMSS_suppressedTimeFramesList,
										   HHMMSS_keptTimeFramesList):
		"""
		Creates the extracted files info dic if necessary.

		Then, adds to the sub-dic the extracted file name and its corresponding
		time frame in HH:MM:SS format.

		:param videoIndex:
		:param suppressedFileName:
		:param HHMMSS_suppressedTimeFramesList list of suppressed time frames.
											 Example: ['0:23:45-0:24:54', '1:03:45-1:24:54']
		:param HHMMSS_keptTimeFramesList     list of kept time frames.
											 Example: ['0:0:0-0:23:45', '0:24:54-1:03:45', '1:24:54-1:55:12']

		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		suppressedFileSubDic = {}
		
		if KEY_VIDEO_SUPPRESS_FILE not in videoInfoDic.keys():
			videoInfoDic[KEY_VIDEO_SUPPRESS_FILE] = suppressedFileSubDic
		else:
			suppressedFileSubDic = videoInfoDic[KEY_VIDEO_SUPPRESS_FILE]
		
		suppressedFileSubDic[KEY_FILENAME] = suppressedFileName
		suppressedFileSubDic[KEY_TIMEFRAMES_HHMMSS_SUPPRESSED] = HHMMSS_suppressedTimeFramesList
		suppressedFileSubDic[KEY_TIMEFRAMES_HHMMSS_KEPT] = HHMMSS_keptTimeFramesList
	
	def isSuppressedFileInfoAvailableForVideoIndex(self, videoIndex):
		"""
		Returns True if suppress info for the passed video index exist. This means
		that the audio without the suppressed portions for the concerned video
		was already created.

		:param videoIndex:

		:return True or False
		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		return KEY_VIDEO_SUPPRESS_FILE in videoInfoDic.keys()
	
	def getSuppressedFileNameForVideoIndex(self, videoIndex):
		"""
		Returns the suppressed time frames in HH:MM:SS format for the passed video
		index.

		:param videoIndex:

		:return: suppressed file name
		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if KEY_VIDEO_SUPPRESS_FILE not in videoInfoDic.keys():
			return None
		else:
			return videoInfoDic[KEY_VIDEO_SUPPRESS_FILE][KEY_FILENAME]
	
	def getSuppressedStartEndHHMMSS_TimeFramesForVideoIndex(self, videoIndex):
		"""
		Returns the suppressed time frames in HH:MM:SS format for the passed video
		index.
		
		Unlike extracting audio portions which produces potentially more than one
		mp3 file per video, suppressing audio portions produces only one mp3 file
		per video. So, obtaining a start end HHMMSS time frame list	for a
		specific file name is nonsensical since only one mp3 file is produced
		when suppressing time frames !

		:param videoIndex:

		:return: startEndHHMMSS time frame list. Example: ['0:23:45', '0:24:54']
		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if KEY_VIDEO_SUPPRESS_FILE not in videoInfoDic.keys():
			return None
		else:
			return videoInfoDic[KEY_VIDEO_SUPPRESS_FILE][KEY_TIMEFRAMES_HHMMSS_SUPPRESSED]
	
	def getKeptStartEndHHMMSS_TimeFramesForVideoIndex(self, videoIndex):
		"""
		Returns the suppressed time frames in HH:MM:SS format for the passed video
		index.

		:param videoIndex:

		:return: startEndHHMMSS time frame list. Example: ['0:23:45', '0:24:54']
		"""
		videoInfoDic = self._getVideoInfoForVideoIndex(videoIndex)
		
		if KEY_VIDEO_SUPPRESS_FILE not in videoInfoDic.keys():
			return None
		else:
			return videoInfoDic[KEY_VIDEO_SUPPRESS_FILE][KEY_TIMEFRAMES_HHMMSS_KEPT]

	def deleteVideoInfoForVideoFileName(self, videoFileName):
		videoIndex = self.getVideoIndexForVideoFileName(videoFileName)
		self.removeVideoInfoForVideoIndex(videoIndex)
		
	def getDicDirName(self):
		"""
		For
		:return:
		"""
		return self.getPlaylistNameModified()

	def getDicDirSubDir(self):
		return self.getPlaylistDownloadSubDir()

	def getPlaylistNameModified(self):
		"""
		Return the modified play list name, which is the modified playlist title
		without the optional extract or suppress time frames definitions. Note that
		if the original playlist name or title were not modified, the modified
		playlist name or title value are set to the original name or title value !
		
		Ex:
		original playlist name = test_audio_downloader_two_files_with_time_frames
		modified playlist name = test_audio_downloader_two_files_with_time_frames
		original playlist title = test_audio_downloader_two_files_with_time_frames (e0:0:2-0:0:8) (s0:0:2-0:0:5 s0:0:7-0:0:10)
		modified playlist title = test_audio_downloader_two_files_with_time_frames (e0:0:2-0:0:8) (s0:0:2-0:0:5 s0:0:7-0:0:10)

		:return:
		"""
		if KEY_PLAYLIST in self.dic.keys():
			if KEY_PLAYLIST_NAME_MODIFIED in self.dic[KEY_PLAYLIST].keys():
				return self.dic[KEY_PLAYLIST][KEY_PLAYLIST_NAME_MODIFIED]
			else:
				logging.info('key {} not found in {} dic file located in {}!'.format(KEY_PLAYLIST_NAME_MODIFIED, self.dic[KEY_PLAYLIST], self.getPlaylistDownloadBaseSubDir()))
				return None
		else:
			return None
	
	def getPlaylistDownloadBaseSubDir(self):
		"""
		Returns the playlist download base sub dir name. This name does not contain
		the	audio dir root dir (defined in the GUI settings) and does not contain
		the playlist name.
		
		Ex: if you did download a playlist with original name 'Analyse économique'
		and modified name 'Analyse économique moified' specifying its dir as
		'Crypto\essai', then the playlist videos are downloaded in audio dir root +
		sep + 'Crypto\essai\Analyse économique moified.
		
		getPlaylistDownloadBaseSubDir() returns Crypto\essai\ and

		:return: playlist download sub dir name
		"""
		playlistDownloadSubDir = self.getPlaylistDownloadSubDir()
		
		if playlistDownloadSubDir is not None:
			if sep in playlistDownloadSubDir:
				return sep.join(playlistDownloadSubDir.split(sep)[0:-1])
			elif posixpath.sep in playlistDownloadSubDir:
				# the case if the playlist _dic.txt file was created on Android and
				# is used on Windows, when downloading failed videos for example
				return posixpath.sep.join(playlistDownloadSubDir.split(posixpath.sep)[0:-1])
			else:
				return ''

	def getPlaylistDownloadSubDir(self):
		"""
		Returns the playlist download dir name. This name does not contain the
		audio dir root dir (defined in the GUI settings).

		:return: playlist download sub dir path
		"""
		if KEY_PLAYLIST in self.dic.keys():
			return self.dic[KEY_PLAYLIST][KEY_PLAYLIST_DOWNLOAD_SUB_DIR]
		else:
			return None

	def renameRedownloadedFailedVideos(self):
		"""
		This method updates the video audio file date prefix in case the date prefix
		is smaller than the video download date. This is the case if downloading the
		video audio on the smartphone failed and that the video audio was re-downloaded
		on the PC and then manually copied on the smartphone.
		"""
		pass
	
	def getRedownloadedFailedVideoIndexes(self):
		"""
		Returns a list of re-download failed video int indexes. Those videos
		were re-downloaded on the PC and are manually copied on the smartphone. As
		they have been re-downloaded, their download date time is after their
		audio filename date prefix. The method returns a list of int video indexes
		whose download date is after their audio file name date prefix.

		:return: list of re-download failed video int indexes
		"""
		failedVideoIndexLst = []
		
		for videoIndexStr, videoDic in self.dic[KEY_VIDEOS].items():
			videoAudioFileName = videoDic[KEY_VIDEO_DOWNLOAD_FILENAME]
			prefixDate, downloadDate, _ = DownloadPlaylistInfoDic.getDownloadDatePrefixDatePrefixStr(videoDic=videoDic,
			                                                                                         videoAudioFileName=videoAudioFileName)
			if prefixDate is None:
				continue
				
			if downloadDate > prefixDate:
				failedVideoIndexLst.append(int(videoIndexStr))

		return failedVideoIndexLst
	
	@staticmethod
	def getPlaylistUrlTitleCachedDic(audioDirRoot):
		"""
		Returns a {<urlStr>: <playlistTitleStr} dictionary containing
		<urlStr>: <playlistTitleStr> entries for all the download playlist info dic
		located in the passed audioDirRoot dir and sub dirs. This cached information dic is
		stored in a json file located in the audio\settings dir. It avoids requesting
		the playlist title via youtube_dl each time a playlist is re-downloaded.
		
		If the cached dic file does not exist in the settings dir, it is created and
		saved into the settings dir.
		
		:param audioDirRoot:    audio dir root path
		
		:return:    {<urlStr>: <playlistTitleStr}. Example:
					{'https://youtube.com/playlist?list=PLzwWSJNcZTMSfeJzsR9st86uW590blzRp': 'Crypto'}
		"""
		settingsDir = audioDirRoot + sep + 'settings'
		
		DirUtil.createTargetDirIfNotExist(audioDirRoot, settingsDir)
		
		dicFilePathName = settingsDir + sep + 'cachedPlaylistUrlTitleDic' + DownloadPlaylistInfoDic.DIC_FILE_NAME_EXTENT
		urlTitleDic = DownloadPlaylistInfoDic._loadDicIfExist(dicFilePathName)
		
		if urlTitleDic is not None:
			return urlTitleDic

		urlTitleDic = {}
		
		for playlistFilePathName in DirUtil.getFilePathNamesInDirForPattern(targetDir=audioDirRoot,
		                                                                    fileNamePattern='*' + DownloadPlaylistInfoDic.DIC_FILE_NAME_EXTENT,
		                                                                    inSubDirs=True):
			try:
				downloadPlaylistInfoDic = DownloadPlaylistInfoDic(existingDicFilePathName=playlistFilePathName)
				
				if downloadPlaylistInfoDic.getPlaylistUrl() == None:
					# the case for download url info dic
					continue
				
				urlTitleDic[downloadPlaylistInfoDic.getPlaylistUrl()] = downloadPlaylistInfoDic.getPlaylistTitleOriginal()
			except Exception as e:
				# if the download playlist info dic has no KEY_PLAYLIST_URL key,
				# we simply do not add this <urlStr>: <playlistTitleStr> entry to
				# the dic.
				pass
				# print(playlistFilePathName)
				# print(e)

			DownloadPlaylistInfoDic.jsonSaveDic(urlTitleDic, dicFilePathName)
			
		return urlTitleDic

	@staticmethod
	def updatePlaylistUrlTitleCachedDic(audioDirRoot,
	                                    playlistUrl,
	                                    playlistTitle):
		"""
		This method adds the passed playListUrl/playlistTitle entry to the cached
		urlTitleDic and then saves the updated dic in the settings dir.
		
		If no cached dic exist in the settings dir, the method does nothing.
		
		:param audioDirRoot:
		:param playlistUrl:
		:param playlistTitle:
		"""
		dicFilePathName = audioDirRoot + sep + 'settings' + sep + 'cachedPlaylistUrlTitleDic' + DownloadPlaylistInfoDic.DIC_FILE_NAME_EXTENT
		urlTitleDic = DownloadPlaylistInfoDic._loadDicIfExist(dicFilePathName)
		
		if urlTitleDic is not None:
			urlTitleDic[playlistUrl] = playlistTitle
			DownloadPlaylistInfoDic.jsonSaveDic(urlTitleDic, dicFilePathName)

	@staticmethod
	def getFailedVideoDownloadedOnSmartphonePlaylistInfoLst(audioDirRoot):
		"""
		Returns playlist's which contains at least one video with vd_downlException
		= True, i.e. video whose audio download on smartphone failed.
		
		More precisely, returns a list of PlaylistVideoIndexInfo. The
		PlaylistVideoIndexInfo's are instantiated only for playlist info dic
		containing at least one failed video downloaded on smartphone.
		
		:return: PlaylistVideoIndexInfoLst
		"""
		return DownloadPlaylistInfoDic.getPlaylistInfoList(audioDirRoot=audioDirRoot,
		                                                   videoIndexMethodType=METHOD_FAILED_VIDEO_INDEX)
	
	@staticmethod
	def getFailedVideoRedownloadedOnPcPlaylistInfoLst(audioDirRoot):
		"""
		Returns playlist's which contains at least one video which was re-downloaded
		on PC, i.e. a video whose download date is after the audio file name date
		prefix.

		More precisely, returns a list of PlaylistVideoIndexInfo. The
		PlaylistVideoIndexInfo's are instantiated only for playlist info dic
		containing at least one video re-downloaded on PC.

		:return: PlaylistVideoIndexInfoLst
		"""
		return DownloadPlaylistInfoDic.getPlaylistInfoList(audioDirRoot=audioDirRoot,
		                                                   videoIndexMethodType=METHOD_REDOWNLOADED_VIDEO_INDEX)
	
	@staticmethod
	def getPlaylistInfoList(audioDirRoot,
	                        videoIndexMethodType):
		videoPlaylistInfoLst = []
		
		for playlistFilePathName in DirUtil.getFilePathNamesInDirForPattern(targetDir=audioDirRoot,
		                                                                    fileNamePattern='*' + DownloadPlaylistInfoDic.DIC_FILE_NAME_EXTENT,
		                                                                    inSubDirs=True):
			downloadPlaylistInfoDic = DownloadPlaylistInfoDic(existingDicFilePathName=playlistFilePathName)
			
			if downloadPlaylistInfoDic.getPlaylistUrl() == None:
				# the case for the download url info dic used to fill the
				# AudioDownloaderGUI URL's list
				continue
			
			if videoIndexMethodType == METHOD_FAILED_VIDEO_INDEX:
				videoIndexList = downloadPlaylistInfoDic.getFailedVideoIndexes()
			elif videoIndexMethodType == METHOD_REDOWNLOADED_VIDEO_INDEX:
				videoIndexList = downloadPlaylistInfoDic.getRedownloadedFailedVideoIndexes()
			else:
				raise TypeError('Invalid  videoIndexMethodType {}'.format(videoIndexMethodType))
			
			if videoIndexList != []:
				videoPlaylistInfoLst.append(PlaylistVideoIndexInfo(playlistInfoDic=downloadPlaylistInfoDic,
				                                                   videoIndexLst=videoIndexList))
		return videoPlaylistInfoLst
	
	@staticmethod
	def renameFailedVideosUpdatedFromPC(audioDirRoot):
		playlistInfoLst = DownloadPlaylistInfoDic.getFailedVideoRedownloadedOnPcPlaylistInfoLst(
			audioDirRoot=audioDirRoot)
		renamedVideoAudioFileDic = {}
		
		for playlistInfo in playlistInfoLst:
			downloadPlaylistInfoDic = playlistInfo.playlistInfoDic
			redownloadedVideoIndexLst = playlistInfo.videoIndexLst
			playlistDownloadSubDir = downloadPlaylistInfoDic.getPlaylistDownloadSubDir()
			renamedVideoAudioFileDic[playlistDownloadSubDir] = []
			playlistDirectory = audioDirRoot + sep + playlistDownloadSubDir
			
			for redownloadedVideoIndex in redownloadedVideoIndexLst:
				videoAudioFileName = downloadPlaylistInfoDic.getVideoAudioFileNameForVideoIndex(redownloadedVideoIndex)
				currentPrefixDate, downloadDate, currentPrefixStr = DownloadPlaylistInfoDic.getDownloadDatePrefixDatePrefixStr(
					videoDic=downloadPlaylistInfoDic._getVideoInfoForVideoIndex(redownloadedVideoIndex),
					videoAudioFileName=videoAudioFileName)
				newPrefixStr = downloadDate.strftime("%y%m%d")
				newVideoAudioFileName = videoAudioFileName.replace(currentPrefixStr, newPrefixStr)
				renamedVideoAudioFileDic[playlistDownloadSubDir].append(newVideoAudioFileName)
				videoAudioFilePathName = playlistDirectory + sep + videoAudioFileName
				DirUtil.renameFile(originalFilePathName=videoAudioFilePathName,
				                   newFileName=newVideoAudioFileName)
				downloadPlaylistInfoDic.setVideoAudioFileNameForVideoIndex(videoIndex=redownloadedVideoIndex,
				                                                           audioFileName=newVideoAudioFileName)
				downloadPlaylistInfoDic.saveDic(audioDirRoot=audioDirRoot)
				
		return renamedVideoAudioFileDic
				
	@staticmethod
	def getDownloadDatePrefixDatePrefixStr(videoDic,
	                                       videoAudioFileName):
		match = DownloadPlaylistInfoDic.isAudioFileNamePrefixedWithDate(videoAudioFileName)
		
		if match is None:
			# the case if the video audio file name prefix is an old 2 digits prefix
			return None, None, None
		else:
			datePrefixStr = match.group(1)
			downloadDateTimeStr = videoDic[KEY_VIDEO_DOWNLOAD_TIME]
			prefixDate = datetime.strptime(datePrefixStr, "%y%m%d")
			downloadDate = datetime.strptime(downloadDateTimeStr.split(' ')[0], "%d/%m/%Y")
			
			return prefixDate, downloadDate, datePrefixStr
	
	@staticmethod
	def isAudioFileNamePrefixedWithDate(videoAudioFileName):
		"""
		Returns None if the passed videoAudioFileName does not start with a 6 digit
		date, match otherwise.
		
		:param videoAudioFileName:
		:return:
		"""
		match = re.search(DATE_PREFIX_PATTERN, videoAudioFileName)
		return match


if __name__ == "__main__":
	if os.name == 'posix':
		audioDir = '/storage/emulated/0/Download/Audio'
	else:
		audioDir = 'C:\\Users\\Jean-Pierre\\Downloads\\Audio'
	
	unitTestDataDir = 'Crypto' + sep + 'essai'
	playlistWithFailedVideoIndexListDic = DownloadPlaylistInfoDic(audioRootDir=audioDir,
	                                                              playlistDownloadRootPath=unitTestDataDir,
	                                                              originalPlaylistName='Analyse économique',
	                                                              modifiedPlaylistName='Analyse économique modified')
	
	print(playlistWithFailedVideoIndexListDic.getPlaylistDownloadSubDir())
	print(playlistWithFailedVideoIndexListDic.getPlaylistDownloadBaseSubDir())
