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
from downloadvideoinfodic import DownloadVideoInfoDic

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
		                                           isUploadDateAddedToPlaylistVideo=False,
		                                           isIndexAddedToPlaylistVideo=False)
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(['downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
 '',
 'video download complete.',
 '',
 'downloading "Here to help: Give him what he wants" audio ...',
 '',
 'video download complete.',
 '',
 '"test_audio_downloader_two_files" playlist audio(s) download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.',
		                 downloadVideoInfoDic.getVideoTitleForVideoIndex(1))
		
		self.assertEqual('Here to help: Give him what he wants',
		                 downloadVideoInfoDic.getVideoTitleForVideoIndex(2))
		
		self.assertEqual(['1', '2'], downloadVideoInfoDic.getVideoIndexes())
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Here to help - Give him what he wants.mp3',
		                         'Wear a mask. Help slow the spread of Covid-19..mp3',
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
		                                                      isUploadDateAddedToPlaylistVideo=False,
		                                                      isIndexAddedToPlaylistVideo=False)

		targetAudioDir = redownloadVideoInfoDic.getPlaylistDownloadDir()
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(['re-downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
 '',
 'video download complete.',
 '',
 '"Here to help - Give him what he wants.mp3" audio already downloaded in '
 '"5\\test_audio_downloader_two_files" dir. Video skipped.',
 '',
 '"test_audio_downloader_two_files" playlist audio(s) download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertEqual(validPlaylistDirName, targetAudioDir)
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.',
		                 redownloadVideoInfoDic.getVideoTitleForVideoIndex(3))
		
		self.assertEqual('Here to help: Give him what he wants',
		                 redownloadVideoInfoDic.getVideoTitleForVideoIndex(2))
		
		self.assertEqual(['2', '3'], redownloadVideoInfoDic.getVideoIndexes())
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Here to help - Give him what he wants.mp3',
		                         'Wear a mask. Help slow the spread of Covid-19..mp3',
		                         'test_audio_downloader_two_files_dic.txt']), sorted(fileNameLst))
	
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
		                                           isUploadDateAddedToPlaylistVideo=False,
		                                           isIndexAddedToPlaylistVideo=False)
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(['downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
		                  '',
		                  'video download complete.',
		                  '',
		                  'downloading "Here to help: Give him what he wants" audio ...',
		                  '',
		                  'video download complete.',
		                  '',
		                  '"test_audio_downloader_two_files" playlist audio(s) download terminated.',
		                  '',
		                  ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.',
		                 downloadVideoInfoDic.getVideoTitleForVideoIndex(1))
		
		self.assertEqual('Here to help: Give him what he wants',
		                 downloadVideoInfoDic.getVideoTitleForVideoIndex(2))
		
		self.assertEqual(['1', '2'], downloadVideoInfoDic.getVideoIndexes())
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Here to help - Give him what he wants.mp3',
		                         'Wear a mask. Help slow the spread of Covid-19..mp3',
		                         'test_audio_downloader_two_files_dic.txt']), sorted(fileNameLst))
		
		# setting download success to False for
		# 'Wear a mask. Help slow the spread of Covid-19.'. This video will
		# be redownloaded
		downloadVideoInfoDic.setVideoDownloadExceptionForVideoTitle(
			videoTitle='Wear a mask. Help slow the spread of Covid-19.',
			isDownloadSuccess=False)
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
		                                                      isUploadDateAddedToPlaylistVideo=False,
		                                                      isIndexAddedToPlaylistVideo=False)
		
		targetAudioDir = redownloadVideoInfoDic.getPlaylistDownloadDir()
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(['re-downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
 '',
 'video download complete.',
 '',
 're-downloading "Here to help: Give him what he wants" audio ...',
 '',
 'video download complete.',
 '',
 '"test_audio_downloader_two_files" playlist audio(s) download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertEqual(validPlaylistDirName, targetAudioDir)
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.',
		                 redownloadVideoInfoDic.getVideoTitleForVideoIndex(3))
		
		self.assertEqual('Here to help: Give him what he wants',
		                 redownloadVideoInfoDic.getVideoTitleForVideoIndex(4))
		
		self.assertEqual(['3', '4'], redownloadVideoInfoDic.getVideoIndexes())
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Here to help - Give him what he wants.mp3',
		                         'Wear a mask. Help slow the spread of Covid-19..mp3',
		                         'test_audio_downloader_two_files_dic.txt']), sorted(fileNameLst))
	
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
		                                           isUploadDateAddedToPlaylistVideo=False,
		                                           isIndexAddedToPlaylistVideo=False)
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(['downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
		                  '',
		                  'video download complete.',
		                  '',
		                  'downloading "Here to help: Give him what he wants" audio ...',
		                  '',
		                  'video download complete.',
		                  '',
		                  '"test_audio_downloader_two_files" playlist audio(s) download terminated.',
		                  '',
		                  ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.',
		                 downloadVideoInfoDic.getVideoTitleForVideoIndex(1))
		
		self.assertEqual('Here to help: Give him what he wants',
		                 downloadVideoInfoDic.getVideoTitleForVideoIndex(2))
		
		self.assertEqual(['1', '2'], downloadVideoInfoDic.getVideoIndexes())
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Here to help - Give him what he wants.mp3',
		                         'Wear a mask. Help slow the spread of Covid-19..mp3',
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
		                                                      isUploadDateAddedToPlaylistVideo=False,
		                                                      isIndexAddedToPlaylistVideo=False)
		
		targetAudioDir = redownloadVideoInfoDic.getPlaylistDownloadDir()
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(['"Wear a mask. Help slow the spread of Covid-19..mp3" audio already '
 'downloaded in "5\\test_audio_downloader_two_files" dir. Video skipped.',
 '',
 're-downloading "Here to help: Give him what he wants" audio ...',
 '',
 'video download complete.',
 '',
 '"test_audio_downloader_two_files" playlist audio(s) download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertEqual(validPlaylistDirName, targetAudioDir)
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.',
		                 redownloadVideoInfoDic.getVideoTitleForVideoIndex(1))
		
		self.assertEqual('Here to help: Give him what he wants',
		                 redownloadVideoInfoDic.getVideoTitleForVideoIndex(3))
		
		self.assertEqual(['1', '3'], redownloadVideoInfoDic.getVideoIndexes())
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Here to help - Give him what he wants.mp3',
		                         'Wear a mask. Help slow the spread of Covid-19..mp3',
		                         'test_audio_downloader_two_files_dic.txt']), sorted(fileNameLst))
	
	def testRedownloadFailedVideosInDownloadVideoInfoDic(self):
		playlistName = 'test_audio_downloader_two_files'
		subTestDirName = 'two_files_6'
		validPlaylistDirName = DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistName)
		testAudioRootPath = DirUtil.getTestDataPath()
		testAudioRootSubDirPath = testAudioRootPath + sep + subTestDirName
		downloadDir = testAudioRootSubDirPath + sep + validPlaylistDirName
		downloadDirSaved = downloadDir + '_saved'
		
		# restoring downloadDir
		
		if os.path.exists(downloadDir):
			shutil.rmtree(downloadDir)

		shutil.copytree(downloadDirSaved, downloadDir)

		guiOutput = GuiOutputStub()
		
		# re-downloading the failed videos
		
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess = YoutubeDlAudioDownloader(audioController,
		                                         testAudioRootSubDirPath)
		
		# loading the download video info dic in which the failed videos
		# are contained
		
		dicFilePathNameLst = DirUtil.getFilePathNamesInDirForPattern(
			downloadDir, '*' + DownloadVideoInfoDic.DIC_FILE_NAME_EXTENT)
		
		downloadVideoInfoDic = None
		
		if len(dicFilePathNameLst) > 0:
			# the file deletion is done in a playlist dir, not in a
			# single videos dir
			downloadVideoInfoDic = DownloadVideoInfoDic(playlistUrl=None,
			                                            audioRootDir=None,
			                                            playlistDownloadRootPath=None,
			                                            originalPaylistTitle=None,
			                                            originalPlaylistName=None,
			                                            modifiedPlaylistTitle=None,
			                                            modifiedPlaylistName=None,
			                                            loadDicIfDicFileExist=True,
			                                            existingDicFilePathName=dicFilePathNameLst[0])
		

		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		youtubeAccess.redownloadFailedVideosInDownloadVideoInfoDic(downloadVideoInfoDic=downloadVideoInfoDic)
		
		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()
		
		sys.stdout = stdout
		
#		self.assertIsNone(accessError)
		self.assertEqual(['re-downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
		                  '',
		                  'video download complete.',
		                  '',
		                  '"Here to help - Give him what he wants.mp3" audio already downloaded in '
		                  '"5\\test_audio_downloader_two_files" dir. Video skipped.',
		                  '',
		                  '"test_audio_downloader_two_files" playlist audio(s) download terminated.',
		                  '',
		                  ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertEqual(validPlaylistDirName, targetAudioDir)
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.',
		                 downloadVideoInfoDic.getVideoTitleForVideoIndex(3))
		
		self.assertEqual('Here to help: Give him what he wants',
		                 downloadVideoInfoDic.getVideoTitleForVideoIndex(2))
		
		self.assertEqual(['2', '3'], downloadVideoInfoDic.getVideoIndexes())
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Here to help - Give him what he wants.mp3',
		                         'Wear a mask. Help slow the spread of Covid-19..mp3',
		                         'test_audio_downloader_two_files_dic.txt']), sorted(fileNameLst))


if __name__ == '__main__':
#	unittest.main()
	tst = TestYoutubeDlAudioDownloaderException()

	tst.testRedownloadFailedVideosInDownloadVideoInfoDic()
