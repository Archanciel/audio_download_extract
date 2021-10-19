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

class TestYoutubeDlAudioDownloaderDownloadMethods(unittest.TestCase):
	"""
	Since testing download consume band width, it is placed in a specific test class.
	"""


	def testRedownloading_the_playlist_with_deleted_audio_files(self):
		playlistName = 'test_audio_downloader_two_files'
		validPlaylistDirName = DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistName)
		downloadDir = DirUtil.getTestAudioRootPath() + sep + validPlaylistDirName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting files in downloadDir
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess = YoutubeDlAudioDownloader(audioController, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRGA1T1vOn500RuLFo_lGJv"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndTitlesFortUrl(playlistUrl)

		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			playlistUrl, youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)

		youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)

		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(
			['downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
			 '',
			 'addVideoInfoForVideoIndex(videoIndex=1, videoTitle=Wear a mask. Help slow '
			 'the spread of Covid-19., downloadedFileName=Wear a mask. Help slow the '
			 'spread of Covid-19..mp3)',
			 'video download complete.',
			 '',
			 'downloading "Here to help: Give him what he wants" audio ...',
			 '',
			 'addVideoInfoForVideoIndex(videoIndex=2, videoTitle=Here to help: Give him '
			 'what he wants, downloadedFileName=Here to help - Give him what he wants.mp3)',
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
		
		# re-downloading the playlist after deleting one audio file
		
		deletedAudioFileName = 'Here to help - Give him what he wants.mp3'
		os.remove(downloadDir + sep + deletedAudioFileName)
		
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess_redownload = YoutubeDlAudioDownloader(audioController, DirUtil.getTestAudioRootPath())
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess_redownload.getPlaylistObjectAndTitlesFortUrl(playlistUrl)

		redownloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			playlistUrl, youtubeAccess_redownload.audioDirRoot, youtubeAccess_redownload.audioDirRoot, playlistTitle)

		youtubeAccess_redownload.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, redownloadVideoInfoDic)

		targetAudioDir = redownloadVideoInfoDic.getPlaylistDownloadDir()
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(['"Wear a mask. Help slow the spread of Covid-19." audio already downloaded in '
 '"test\\test_audio_downloader_two_files" dir. Video skipped.',
 '',
 '"Here to help: Give him what he wants" audio already downloaded in '
 '"test\\test_audio_downloader_two_files" dir but was deleted. Video skipped.',
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
		self.assertEqual(sorted(['Wear a mask. Help slow the spread of Covid-19..mp3',
 'test_audio_downloader_two_files_dic.txt']), sorted(fileNameLst))


if __name__ == '__main__':
#	unittest.main()
	tst = TestYoutubeDlAudioDownloaderDownloadMethods()
	tst.testRedownloading_the_playlist_with_deleted_audio_files()
