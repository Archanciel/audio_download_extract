import time
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


class TestYoutubeDlAudioDownloaderDownloadMethods_2(unittest.TestCase):
	def testDownloadPlaylistVideosForUrlMultipleVideo_redownloading_the_playlist(self):
		playlistName = 'test_audio_downloader_two_files'
		subTestDirName = '2'
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
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess = YoutubeDlAudioDownloader(audioController, testAudioRootSubDirPath)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRGA1T1vOn500RuLFo_lGJv"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndTitlesFortUrl(playlistUrl)
		
		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			playlistUrl, youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)
		
		youtubeAccess.downloadPlaylistVideosForUrl(playlistUrl=playlistUrl,
		                                           downloadVideoInfoDic=downloadVideoInfoDic,
		                                           isUploadDateAddedToPlaylistVideo=False)
		
		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(
			['downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
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
		
		self.assertEqual(validPlaylistDirName, targetAudioDir)
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.',
		                 downloadVideoInfoDic.getVideoTitleForVideoIndex(1))
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk',
		                 downloadVideoInfoDic.getVideoUrlForVideoIndex(1))
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk',
		                 downloadVideoInfoDic.getVideoUrlForVideoTitle(
			                 'Wear a mask. Help slow the spread of Covid-19.'))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3',
		                 downloadVideoInfoDic.getVideoFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3',
		                 downloadVideoInfoDic.getVideoFileNameForVideoTitle(
			                 'Wear a mask. Help slow the spread of Covid-19.'))
		
		self.assertEqual('Here to help: Give him what he wants',
		                 downloadVideoInfoDic.getVideoTitleForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                 downloadVideoInfoDic.getVideoUrlForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                 downloadVideoInfoDic.getVideoUrlForVideoTitle('Here to help: Give him what he wants'))
		self.assertEqual('Here to help - Give him what he wants.mp3',
		                 downloadVideoInfoDic.getVideoFileNameForVideoIndex(2))
		self.assertEqual('Here to help - Give him what he wants.mp3',
		                 downloadVideoInfoDic.getVideoFileNameForVideoTitle(
			                 'Here to help: Give him what he wants'))
		
		self.assertEqual(['1', '2'], downloadVideoInfoDic.getVideoIndexes())
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Here to help - Give him what he wants.mp3',
		                         'Wear a mask. Help slow the spread of Covid-19..mp3',
		                         'test_audio_downloader_two_files_dic.txt']), sorted(fileNameLst))
		
		# re-downloading the playlist
		
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess_redownload = YoutubeDlAudioDownloader(audioController, testAudioRootSubDirPath)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess_redownload.getPlaylistObjectAndTitlesFortUrl(playlistUrl)
		
		redownloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			playlistUrl, youtubeAccess_redownload.audioDirRoot, youtubeAccess_redownload.audioDirRoot, playlistTitle)
		
		youtubeAccess_redownload.downloadPlaylistVideosForUrl(playlistUrl=playlistUrl,
		                                                      downloadVideoInfoDic=redownloadVideoInfoDic,
		                                                      isUploadDateAddedToPlaylistVideo=False)
		
		targetAudioDir = redownloadVideoInfoDic.getPlaylistDownloadDir()
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(['"Wear a mask. Help slow the spread of Covid-19..mp3" audio already '
		                  'downloaded in "2\\test_audio_downloader_two_files" dir. Video skipped.',
		                  '',
		                  '"Here to help - Give him what he wants.mp3" audio already downloaded in '
		                  '"2\\test_audio_downloader_two_files" dir. Video skipped.',
		                  '',
		                  '"test_audio_downloader_two_files" playlist audio(s) download terminated.',
		                  '',
		                  ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertEqual(validPlaylistDirName, targetAudioDir)
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.',
		                 redownloadVideoInfoDic.getVideoTitleForVideoIndex(1))
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk',
		                 redownloadVideoInfoDic.getVideoUrlForVideoIndex(1))
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk',
		                 redownloadVideoInfoDic.getVideoUrlForVideoTitle(
			                 'Wear a mask. Help slow the spread of Covid-19.'))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3',
		                 redownloadVideoInfoDic.getVideoFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3',
		                 redownloadVideoInfoDic.getVideoFileNameForVideoTitle(
			                 'Wear a mask. Help slow the spread of Covid-19.'))
		
		self.assertEqual('Here to help: Give him what he wants',
		                 redownloadVideoInfoDic.getVideoTitleForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                 redownloadVideoInfoDic.getVideoUrlForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                 redownloadVideoInfoDic.getVideoUrlForVideoTitle('Here to help: Give him what he wants'))
		self.assertEqual('Here to help - Give him what he wants.mp3',
		                 redownloadVideoInfoDic.getVideoFileNameForVideoIndex(2))
		self.assertEqual('Here to help - Give him what he wants.mp3',
		                 redownloadVideoInfoDic.getVideoFileNameForVideoTitle(
			                 'Here to help: Give him what he wants'))
		
		self.assertEqual(['1', '2'], redownloadVideoInfoDic.getVideoIndexes())
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Here to help - Give him what he wants.mp3',
		                         'Wear a mask. Help slow the spread of Covid-19..mp3',
		                         'test_audio_downloader_two_files_dic.txt']), sorted(fileNameLst))


if __name__ == '__main__':
	unittest.main()
