import shutil
import unittest
import os, sys, inspect
from os.path import sep
import datetime

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from kivy.core.clipboard import Clipboard

from configmanager import ConfigManager
from dirutil import DirUtil
from gui.audiodownloadergui import AudioDownloaderGUIMainApp
from downloadUrlinfodic import DownloadUrlInfoDic

class TryTestAudioDownloaderGUIUrlList(unittest.TestCase):

	def __init__(self):
		super().__init__()
		
		self.configMgr = ConfigManager(DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini')

		self.singleVideoAudioFileNameLst = []
		self.playlistSaveDirNameLst = []
		self.playlistDirNameLst = []

		self.playlistDirName_3 = "test_small_videos_3"
		self.playlistDirNameLst.append(self.playlistDirName_3)
		self.playlistDirName_4 = "test_audio_downloader_two_files_with_time_frames"
		self.playlistDirNameLst.append(self.playlistDirName_4)
		self.playlistDirName_5 = "test warning index date files_noIndexNoDate"
		self.playlistDirNameLst.append(self.playlistDirName_5)
		self.playlistDirName_6 = "test warning index date files_indexNoDate"
		self.playlistDirNameLst.append(self.playlistDirName_6)
		self.playlistDirName_7 = "test warning index date files_noIndexDate"
		self.playlistDirNameLst.append(self.playlistDirName_7)
		self.playlistDirName_8 = "test warning index date files_IndexDate"
		self.playlistDirNameLst.append(self.playlistDirName_8)
		self.playlistDirName_9 = "test warning index date files_downloadDirNotExist"
		self.playlistDirNameLst.append(self.playlistDirName_9)
		self.playlistDirName_10 = "test warning index date files_downloadDirEmpty"
		self.playlistDirNameLst.append(self.playlistDirName_10)
		
		downloadDatePrefix = datetime.datetime.today().strftime("%y%m%d") + '-'
		
		# this video is no longer on Youtube and so will cause a download error !
		self.singleVideoFileName_1 = '{}Try Not To Laugh _ The most interesting funny short video tik tok #shorts 21-12-05.mp3'.format(downloadDatePrefix)
		self.singleVideoUrl_1 = 'https://youtu.be/t2K4uM9ktsE'
		self.singleVideoAudioFileNameLst.append(self.singleVideoFileName_1)

		self.singleVideoFileName_3 = '{}Lama Tanz 15-06-11.mp3'.format(downloadDatePrefix)
		self.singleVideoUrl_3 = 'https://youtu.be/FqC2lO3Yy_4'
		self.singleVideoAudioFileNameLst.append(self.singleVideoFileName_3)

	def tryTestAudioDownloaderGUI(self):
		urlListDicFileName = DirUtil.extractFileNameFromFilePathName(self.configMgr.loadAtStartPathFilename)

		downloadUrlInfoDic = DownloadUrlInfoDic(
			audioRootDir=self.configMgr.dataPath,
			urlListDicFileName=urlListDicFileName,
			generalTotalDownlResultTuple=(13, 4, 7),
			generalTotalDownlSuccessTuple=(3, 5, 1, 1, 2),
			generalTotalDownlFailTuple=(0, 2, 0, 0, 2),
			generalTotalDownlSkipTuple=(1, 2, 0, 0, 4),
			loadDicIfDicFileExist=False,
			existingDicFilePathName=None)

		# the three videos in the playlist have been partially downloaded
		playlistSaveDirName_3 = self.playlistDirName_3 + sep + "sav"
		self.playlistSaveDirNameLst.append(playlistSaveDirName_3)
		playlistUrl_3 = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRx16thPZ3i4u3ZJthdifqo'
		downloadUrlInfoDic.addUrlInfo(urlType=downloadUrlInfoDic.URL_TYPE_PLAYLIST, urlTitle=self.playlistDirName_3,
		                              url=playlistUrl_3, downloadDir='')
		
		# adding first single video url (this video is no longer on Youtube !)
		downloadUrlInfoDic.addUrlInfo(urlType=downloadUrlInfoDic.URL_TYPE_SINGLE_VIDEO, urlTitle='Short King Struggles',
		                              url=self.singleVideoUrl_1, downloadDir='')

		# downloading a playlist with extract and suppress portion settings
		# in playlist title
		playlistSaveDirName_4 = None # avoids playlist dir restore after it was emptied
		self.playlistSaveDirNameLst.append(playlistSaveDirName_4)
		playlistUrl_4 = 'https://youtube.com/playlist?list=PLzwWSJNcZTMSFWGrRGKOypqN29MlyuQvn'
		downloadUrlInfoDic.addUrlInfo(urlType=downloadUrlInfoDic.URL_TYPE_PLAYLIST,
		                              urlTitle='test_audio_downloader_two_files_with_time_frames (e0:0:2-0:0:8) (s0:0:2-0:0:5 s0:0:7-0:0:10)',
		                              url=playlistUrl_4, downloadDir='')
		
		# now testing the index prefix and upload date suffix automatic
		# setting for playlist url list downloading

		# playlist where only one file is to be downloaded since it was deleted
		# from the save dir. Since all the files in the playlist dir are named
		# without index and without date, the downloaded file name must also be
		# without index and without date.
		playlistSaveDirName_5 = self.playlistDirName_5 + sep + "sav"
		self.playlistSaveDirNameLst.append(playlistSaveDirName_5)
		playlistUrl_5 = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRVKblKqskAyseCgsUmhlSc'
		downloadUrlInfoDic.addUrlInfo(urlType=downloadUrlInfoDic.URL_TYPE_PLAYLIST, urlTitle=self.playlistDirName_5,
		                              url=playlistUrl_5, downloadDir='')
		
		# playlist where only one file is to be downloaded since it was deleted
		# from the save dir. No file in the playlist dir is named with upload
		# date suffix. Since one file in the playlist dir is named
		# with index prefix, the downloaded file name must also be
		# named with index prefix and without date suffix.
		playlistSaveDirName_6 = self.playlistDirName_6 + sep + "sav"
		self.playlistSaveDirNameLst.append(playlistSaveDirName_6)
		playlistUrl_6 = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRqeXBddcErPTC__A2KHjFd'
		downloadUrlInfoDic.addUrlInfo(urlType=downloadUrlInfoDic.URL_TYPE_PLAYLIST, urlTitle=self.playlistDirName_6,
		                              url=playlistUrl_6, downloadDir='')
		
		# adding second single video url
		downloadUrlInfoDic.addUrlInfo(urlType=downloadUrlInfoDic.URL_TYPE_SINGLE_VIDEO,
		                              urlTitle='Lama Tanz',
		                              url=self.singleVideoUrl_3, downloadDir='')
		
		# playlist where only one file is to be downloaded since it was deleted
		# from the save dir. No file in the playlist dir is named with index
		# prefix. Since one file in the playlist dir is named with upload date
		# suffix, the downloaded file name must also be named without index prefix
		# and with upload date suffix.
		playlistSaveDirName_7 = self.playlistDirName_7 + sep + "sav"
		self.playlistSaveDirNameLst.append(playlistSaveDirName_7)
		playlistUrl_7 = 'https://www.youtube.com/playlist?list=PLzwWSJNcZTMT_P0bftfIjKbKdaVaxem4D'
		downloadUrlInfoDic.addUrlInfo(urlType=downloadUrlInfoDic.URL_TYPE_PLAYLIST, urlTitle=self.playlistDirName_7,
		                              url=playlistUrl_7, downloadDir='')

		# playlist where only one file is to be downloaded since it was deleted
		# from the save dir. One file in the playlist dir is named with index
		# prefix and upload date suffix. For this reason, the downloaded file name
		# must also be named with index prefix and with upload date suffix.
		playlistSaveDirName_8 = self.playlistDirName_8 + sep + "sav"
		self.playlistSaveDirNameLst.append(playlistSaveDirName_8)
		playlistUrl_8 = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRMhkp5nzUm_h02fKsiy1se'
		downloadUrlInfoDic.addUrlInfo(urlType=downloadUrlInfoDic.URL_TYPE_PLAYLIST, urlTitle=self.playlistDirName_8,
		                              url=playlistUrl_8, downloadDir='')

		# playlist whose download dir does not exist. The downloaded file
		# will be named with index prefix and with upload date suffix.
		playlistUrl_9 = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRXamI-VlOly97Prt4_Jj2W'
		downloadUrlInfoDic.addUrlInfo(urlType=downloadUrlInfoDic.URL_TYPE_PLAYLIST, urlTitle=self.playlistDirName_9,
		                              url=playlistUrl_9, downloadDir='')

		downloadDir = self.configMgr.dataPath + sep + self.playlistDirName_9
		
		if os.path.isdir(downloadDir):
			shutil.rmtree(downloadDir)
		
		# playlist whose download dir is empty. The downloaded file
		# will be named with index prefix and with upload date suffix.
		playlistUrl_10 = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRUSEsR1zccRxrBeCl3Nmc_'
		downloadUrlInfoDic.addUrlInfo(urlType=downloadUrlInfoDic.URL_TYPE_PLAYLIST, urlTitle=self.playlistDirName_10,
		                              url=playlistUrl_10, downloadDir='')

		downloadDir = self.configMgr.dataPath + sep + self.playlistDirName_10
		
		DirUtil.deleteFilesInDirForPattern(downloadDir, '*')
		
		singleVideoSaveDirName = 'single80%'
		
		self.restorePlaylistDownloadDirs(self.playlistDirNameLst,
		                                 self.playlistSaveDirNameLst,
		                                 singleVideoSaveDirName,
		                                 self.singleVideoAudioFileNameLst)
		
		downloadUrlInfoDic.saveDic(audioDirRoot=self.configMgr.dataPath,
		                           dicFilePathName=self.configMgr.loadAtStartPathFilename)

		Clipboard.copy('  ')

		if input('Type g to open the GUI (you can run reinittrytestaudiodownloaderguiurllist.py to reinitialize the test data ...) : ') == 'g':
			dbApp = AudioDownloaderGUIMainApp()
			dbApp.run()
	
	def restorePlaylistDownloadDirs(self,
	                                playlistDirNameLst,
	                                playlistSaveDirNameLst,
	                                singleVideoSaveDirName,
	                                singleVideoAudioFileNameLst):
		downloadDirLst = []
		
		for playlistDirName, playlistSaveDirName in zip(playlistDirNameLst, playlistSaveDirNameLst):
			downloadDir = self.configMgr.dataPath + sep + playlistDirName
			DirUtil.deleteFilesInDirForPattern(downloadDir, '*')
			
			if playlistSaveDirName:
				savedDownloadDir = self.configMgr.dataPath + sep + playlistSaveDirName
				DirUtil.copyFilesInDirToDirForPattern(sourceDir=savedDownloadDir,
				                                      targetDir=downloadDir,
				                                      fileNamePattern='*')
			downloadDirLst.append(downloadDir)

		for singleVideoAudioFileName in singleVideoAudioFileNameLst:
			DirUtil.deleteFileIfExist(self.configMgr.singleVideoDataPath + sep + singleVideoAudioFileName)
			
		DirUtil.copyFilesInDirToDirForPattern(sourceDir=self.configMgr.singleVideoDataPath + sep + singleVideoSaveDirName,
		                                      targetDir=self.configMgr.singleVideoDataPath,
		                                      fileNamePattern='*')

		return downloadDirLst


if __name__ == '__main__':
#	unittest.main()
	tst = TryTestAudioDownloaderGUIUrlList()
	tst.tryTestAudioDownloaderGUI()
