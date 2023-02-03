import unittest
import os, sys, inspect, shutil, glob
from os.path import sep
from io import StringIO

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from constants import *
from guioutputstub import GuiOutputStub
from youtubedlaudiodownloader import YoutubeDlAudioDownloader
from dirutil import DirUtil
from playlisttitleparser import PlaylistTitleParser
from audiocontroller import AudioController
from configmanager import ConfigManager
from downloadplaylistinfodic import DownloadPlaylistInfoDic

class TestYoutubeDlAudioDownloaderException(unittest.TestCase):
	
	def testRedownloadingTwoVideosPlaylist_after_first_video_download_exception(self):
		playlistName = 'test_audio_downloader_two_files'
		subTestDirName = '5'
		validPlaylistDirName = DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistName)
		testAudioRootPath = DirUtil.getTestAudioRootPath()
		testAudioRootSubDirPath = testAudioRootPath + sep + subTestDirName
		downloadDir = testAudioRootSubDirPath + sep + validPlaylistDirName
		
		DirUtil.createTargetDirIfNotExist(rootDir=testAudioRootPath,
		                                  targetAudioDir=downloadDir)
		
		# deleting files in downloadDir
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()

		# downloading the playlist for the first time

		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess = YoutubeDlAudioDownloader(audioController, testAudioRootSubDirPath)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRGA1T1vOn500RuLFo_lGJv"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)
		
		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			playlistUrl, youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)
		
		youtubeAccess.downloadPlaylistVideosForUrl(playlistUrl=playlistUrl,
		                                           downloadVideoInfoDic=downloadVideoInfoDic,
		                                           isUploadDateSuffixAddedToPlaylistVideo=False,
		                                           isDownloadDatePrefixAddedToPlaylistVideo=False)
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(['downloading Here to help: Give him what he wants audio ...',
 '',
 'video download complete.',
 '',
 'test_audio_downloader_two_files playlist audio(s) download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertEqual('Here to help: Give him what he wants',
		                 downloadVideoInfoDic.getVideoTitleForVideoIndex(1))
		
		self.assertEqual(['1'], downloadVideoInfoDic.getVideoIndexStrings())
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Here to help - Give him what he wants.mp3',
		                         'test_audio_downloader_two_files_dic.txt']), sorted(fileNameLst))
		
		# setting download success to False for
		# 'Wear a mask. Help slow the spread of Covid-19.'. This video will
		# be redownloaded
		downloadVideoInfoDic.setVideoDownloadExceptionForVideoTitle(videoTitle='Wear a mask. Help slow the spread of Covid-19.',
		                                                            isDownloadSuccess=False)
		downloadVideoInfoDic.saveDic(youtubeAccess.audioDirRoot)

		# re-downloading the playlist
		
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess_redownload = YoutubeDlAudioDownloader(audioController, testAudioRootSubDirPath)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess_redownload.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)
		
		redownloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			playlistUrl, youtubeAccess_redownload.audioDirRoot, youtubeAccess_redownload.audioDirRoot, playlistTitle)
		
		youtubeAccess_redownload.downloadPlaylistVideosForUrl(playlistUrl=playlistUrl,
		                                                      downloadVideoInfoDic=redownloadVideoInfoDic,
		                                                      isUploadDateSuffixAddedToPlaylistVideo=False,
		                                                      isDownloadDatePrefixAddedToPlaylistVideo=False)

		targetAudioDir = redownloadVideoInfoDic.getPlaylistDownloadSubDir()
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(['Here to help - Give him what he wants.mp3 audio already downloaded in '
 '5\\test_audio_downloader_two_files dir. Video skipped.',
 '',
 'test_audio_downloader_two_files playlist audio(s) download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertEqual(validPlaylistDirName, targetAudioDir)
		self.assertEqual(None,
		                 redownloadVideoInfoDic.getVideoTitleForVideoIndex(3))
		
		self.assertIsNone(redownloadVideoInfoDic.getVideoTitleForVideoIndex(2))
		
		self.assertEqual(['1'], redownloadVideoInfoDic.getVideoIndexStrings())
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Here to help - Give him what he wants.mp3',
		                         'test_audio_downloader_two_files_dic.txt']), sorted(fileNameLst))
	
		# deleting files in downloadDir to avoid loading them on GitHub
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
	
	def testRedownloadingTwoVideosPlaylist_after_2_videos_download_exception(self):
		playlistName = 'test_audio_downloader_two_files'
		subTestDirName = '5'
		validPlaylistDirName = DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistName)
		testAudioRootPath = DirUtil.getTestAudioRootPath()
		testAudioRootSubDirPath = testAudioRootPath + sep + subTestDirName
		downloadDir = testAudioRootSubDirPath + sep + validPlaylistDirName
		
		DirUtil.createTargetDirIfNotExist(rootDir=testAudioRootPath,
		                                  targetAudioDir=downloadDir)
		
		# deleting files in downloadDir
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		
		# downloading the playlist for the first time
		
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess = YoutubeDlAudioDownloader(audioController, testAudioRootSubDirPath)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRGA1T1vOn500RuLFo_lGJv"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)
		
		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			playlistUrl, youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)
		
		youtubeAccess.downloadPlaylistVideosForUrl(playlistUrl=playlistUrl,
		                                           downloadVideoInfoDic=downloadVideoInfoDic,
		                                           isUploadDateSuffixAddedToPlaylistVideo=False,
		                                           isDownloadDatePrefixAddedToPlaylistVideo=False)
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(['downloading Here to help: Give him what he wants audio ...',
 '',
 'video download complete.',
 '',
 'test_audio_downloader_two_files playlist audio(s) download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertEqual('Here to help: Give him what he wants',
		                 downloadVideoInfoDic.getVideoTitleForVideoIndex(1))
		
		self.assertEqual(['1'], downloadVideoInfoDic.getVideoIndexStrings())
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Here to help - Give him what he wants.mp3',
		                         'test_audio_downloader_two_files_dic.txt']), sorted(fileNameLst))
		
		# setting download success to False for
		# 'Wear a mask. Help slow the spread of Covid-19.'. This video will
		# be redownloaded
		downloadVideoInfoDic.setVideoDownloadExceptionForVideoTitle(
			videoTitle='Here to help: Give him what he wants',
			isDownloadSuccess=False)
		downloadVideoInfoDic.saveDic(youtubeAccess.audioDirRoot)
		
		# re-downloading the playlist
		
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess_redownload = YoutubeDlAudioDownloader(audioController, testAudioRootSubDirPath)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess_redownload.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)
		
		redownloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			playlistUrl, youtubeAccess_redownload.audioDirRoot, youtubeAccess_redownload.audioDirRoot, playlistTitle)
		
		youtubeAccess_redownload.downloadPlaylistVideosForUrl(playlistUrl=playlistUrl,
		                                                      downloadVideoInfoDic=redownloadVideoInfoDic,
		                                                      isUploadDateSuffixAddedToPlaylistVideo=False,
		                                                      isDownloadDatePrefixAddedToPlaylistVideo=False)
		
		targetAudioDir = redownloadVideoInfoDic.getPlaylistDownloadSubDir()
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(['Here to help - Give him what he wants.mp3 audio download done previously in '
 '5\\test_audio_downloader_two_files dir FAILED. Try re-downloading it on pc. '
 'Video skipped.',
 '',
 'test_audio_downloader_two_files playlist audio(s) download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertEqual(validPlaylistDirName, targetAudioDir)
		self.assertEqual(None,
		                 redownloadVideoInfoDic.getVideoTitleForVideoIndex(3))
		
		self.assertEqual(None,
		                 redownloadVideoInfoDic.getVideoTitleForVideoIndex(4))
		
		self.assertEqual(['1'], redownloadVideoInfoDic.getVideoIndexStrings())
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Here to help - Give him what he wants.mp3',
		                         'test_audio_downloader_two_files_dic.txt']), sorted(fileNameLst))
		
		# deleting files in downloadDir to avoid loading them on GitHub
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
	
	def testRedownloadingTwoVideosPlaylist_after_second_video_download_exception(self):
		playlistName = 'test_audio_downloader_two_files'
		subTestDirName = '5'
		validPlaylistDirName = DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistName)
		testAudioRootPath = DirUtil.getTestAudioRootPath()
		testAudioRootSubDirPath = testAudioRootPath + sep + subTestDirName
		downloadDir = testAudioRootSubDirPath + sep + validPlaylistDirName
		
		DirUtil.createTargetDirIfNotExist(rootDir=testAudioRootPath,
		                                  targetAudioDir=downloadDir)
		
		# deleting files in downloadDir
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		
		# downloading the playlist for the first time
		
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess = YoutubeDlAudioDownloader(audioController, testAudioRootSubDirPath)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRGA1T1vOn500RuLFo_lGJv"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)
		
		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			playlistUrl, youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)
		
		youtubeAccess.downloadPlaylistVideosForUrl(playlistUrl=playlistUrl,
		                                           downloadVideoInfoDic=downloadVideoInfoDic,
		                                           isUploadDateSuffixAddedToPlaylistVideo=False,
		                                           isDownloadDatePrefixAddedToPlaylistVideo=False)
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(['downloading Here to help: Give him what he wants audio ...',
 '',
 'video download complete.',
 '',
 'test_audio_downloader_two_files playlist audio(s) download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertEqual('Here to help: Give him what he wants',
		                 downloadVideoInfoDic.getVideoTitleForVideoIndex(1))
		
		self.assertEqual(['1'], downloadVideoInfoDic.getVideoIndexStrings())
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Here to help - Give him what he wants.mp3',
		                         'test_audio_downloader_two_files_dic.txt']), sorted(fileNameLst))
		
		# setting download success to False for
		# 'Wear a mask. Help slow the spread of Covid-19.'. This video will
		# be redownloaded
		downloadVideoInfoDic.setVideoDownloadExceptionForVideoTitle(
			videoTitle='Here to help: Give him what he wants',
			isDownloadSuccess=False)
		downloadVideoInfoDic.saveDic(youtubeAccess.audioDirRoot)
		
		# re-downloading the playlist
		
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess_redownload = YoutubeDlAudioDownloader(audioController, testAudioRootSubDirPath)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess_redownload.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)
		
		redownloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			playlistUrl, youtubeAccess_redownload.audioDirRoot, youtubeAccess_redownload.audioDirRoot, playlistTitle)
		
		youtubeAccess_redownload.downloadPlaylistVideosForUrl(playlistUrl=playlistUrl,
		                                                      downloadVideoInfoDic=redownloadVideoInfoDic,
		                                                      isUploadDateSuffixAddedToPlaylistVideo=False,
		                                                      isDownloadDatePrefixAddedToPlaylistVideo=False)
		
		targetAudioDir = redownloadVideoInfoDic.getPlaylistDownloadSubDir()
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(['Here to help - Give him what he wants.mp3 audio download done previously in '
 '5\\test_audio_downloader_two_files dir FAILED. Try re-downloading it on pc. '
 'Video skipped.',
 '',
 'test_audio_downloader_two_files playlist audio(s) download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertEqual(validPlaylistDirName, targetAudioDir)
		self.assertEqual(None,
		                 redownloadVideoInfoDic.getVideoTitleForVideoIndex(2))
		
		self.assertEqual(['1'], redownloadVideoInfoDic.getVideoIndexStrings())
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Here to help - Give him what he wants.mp3',
		                         'test_audio_downloader_two_files_dic.txt']), sorted(fileNameLst))
		
		# deleting files in downloadDir to avoid loading them on GitHub
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)


if __name__ == '__main__':
#	unittest.main()
	tst = TestYoutubeDlAudioDownloaderException()

	tst.testRedownloadingTwoVideosPlaylist_after_2_videos_download_exception()
