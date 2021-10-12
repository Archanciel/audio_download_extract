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

class TestYoutubeDlAudioDownloaderDownloadMethods(unittest.TestCase):
	"""
	Since testing download consume band width, it is placed in a specific test class.
	"""

	def testDownloadVideosReferencedInPlaylistForPlaylistUrl_targetFolder_exist(self):
		playlistName = 'test_audio_downloader_one_file'
		validPlaylistDirName = DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistName)
		downloadDir = DirUtil.getTestAudioRootPath() + sep + validPlaylistDirName

		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)

		# deleting files in downloadDir
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
			
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndTitlesFortUrl(playlistUrl)

		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)

		youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)

		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()

		sys.stdout = stdout

		self.assertIsNone(accessError)
		self.assertEqual(['downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
 '',
 'download complete.',
 '',
 '"test_audio_downloader_one_file" playlist audio(s) download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))

		self.assertEqual(validPlaylistDirName, targetAudioDir)
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.', downloadVideoInfoDic.getVideoTitleForVideoIndex(1))
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk', downloadVideoInfoDic.getVideoUrlForVideoIndex(1))
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk', downloadVideoInfoDic.getVideoUrlForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3', downloadVideoInfoDic.getVideoFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3', downloadVideoInfoDic.getVideoFileNameForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))
		self.assertEqual(['1'], downloadVideoInfoDic.getVideoIndexes())

		if os.name == 'posix':
			self.assertEqual('/storage/emulated/0/Download/Audiobooks/test_audio_downloader_one_file',
			                 downloadDir)
		else:
			self.assertEqual('{}test_audio_downloader_one_file'.format(DirUtil.getTestAudioRootPath() + sep), downloadDir)

		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Wear a mask. Help slow the spread of Covid-19..mp3',
								 'test_audio_downloader_one_file_dic.txt']), sorted(fileNameLst))

	def testDownloadVideosReferencedInPlaylistForPlaylistUrl_targetFolder_not_exist(self):
		playlistName = 'test_audio_downloader_one_file'
		downloadDir = DirUtil.getTestAudioRootPath() + sep + DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistName)

		# deleting downloadDir (dir and content)
		if os.path.exists(downloadDir):
			shutil.rmtree(downloadDir)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndTitlesFortUrl(playlistUrl)

		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)

		youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)

		sys.stdout = stdout

		if os.name == 'posix':
			self.assertEqual(['directory',
 'test/test_audio_downloader_one_file',
 'was created.',
 '',
 'downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
 '',
 '"Wear a mask. Help slow the spread of Covid-19." audio downloaded.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual(['directory',
 'test\\test_audio_downloader_one_file',
 'was created.',
 '',
 'downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
 '',
 'download complete.',
 '',
 '"test_audio_downloader_one_file" playlist audio(s) download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))

		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Wear a mask. Help slow the spread of Covid-19..mp3',
								 'test_audio_downloader_one_file_dic.txt']), sorted(fileNameLst))

	def testDownloadVideosReferencedInPlaylistForPlaylistUrlMultipleVideo(self):
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
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRGA1T1vOn500RuLFo_lGJv"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString

		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndTitlesFortUrl(playlistUrl)

		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)

		youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)

		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()
		sys.stdout = stdout

		self.assertIsNone(accessError)
		self.assertEqual(['downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
 '',
 'download complete.',
 '',
 'downloading "Here to help: Give him what he wants" audio ...',
 '',
 'download complete.',
 '',
 '"test_audio_downloader_two_files" playlist audio(s) download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))

		self.assertEqual(validPlaylistDirName, targetAudioDir)
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.', downloadVideoInfoDic.getVideoTitleForVideoIndex(1))
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk', downloadVideoInfoDic.getVideoUrlForVideoIndex(1))
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk', downloadVideoInfoDic.getVideoUrlForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3', downloadVideoInfoDic.getVideoFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3', downloadVideoInfoDic.getVideoFileNameForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))

		self.assertEqual('Here to help: Give him what he wants', downloadVideoInfoDic.getVideoTitleForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw', downloadVideoInfoDic.getVideoUrlForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw', downloadVideoInfoDic.getVideoUrlForVideoTitle('Here to help: Give him what he wants'))
		self.assertEqual('Here to help - Give him what he wants.mp3', downloadVideoInfoDic.getVideoFileNameForVideoIndex(2))
		self.assertEqual('Here to help - Give him what he wants.mp3', downloadVideoInfoDic.getVideoFileNameForVideoTitle('Here to help: Give him what he wants'))

		self.assertEqual(['1', '2'], downloadVideoInfoDic.getVideoIndexes())

		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Here to help - Give him what he wants.mp3',
								 'Wear a mask. Help slow the spread of Covid-19..mp3',
								 'test_audio_downloader_two_files_dic.txt']), sorted(fileNameLst))
	
	def testDownloadVideosReferencedInPlaylistForPlaylistUrlMultipleVideo_withTimeFrames(self):
		# playlist title: test_audio_downloader_two_files_with_time_frames (e0:0:2-0:0:8) (s0:0:2-0:0:5 s0:0:7-0:0:10)
		time.sleep(1)   # required to avoid uncomprehensible test failure when executing all unit tsts
		playlistName = 'test_audio_downloader_two_files_with_time_frames'
		validPlaylistDirName = DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistName)
		downloadDir = DirUtil.getTestAudioRootPath() + sep + validPlaylistDirName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting files in downloadDir
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMSFWGrRGKOypqN29MlyuQvn"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndTitlesFortUrl(playlistUrl)

		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)

		youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)

		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()

		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(
			['downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
			 '',
			 'download complete.',
			 '',
			 'downloading "Here to help: Give him what he wants" audio ...',
			 '',
			 'download complete.',
			 '',
			 '"test_audio_downloader_two_files_with_time_frames" playlist audio(s) download terminated.',
			 '',
			 ''], outputCapturingString.getvalue().split('\n'))
		
		# playlist title: test_audio_downloader_two_files_with_time_frames
		# (e0:0:2-0:0:8) (s0:0:2-0:0:5 s0:0:7-0:0:10)
		startEndSecondsList_extract_firstVideo_firstTimeFrame = [2, 8]

		startEndSecondsList_suppress_secondVideo_firstTimeFrame = [2, 5]
		startEndSecondsList_suppress_secondVideo_secondTimeFrame = [7, 10]
		
		self.assertEqual([startEndSecondsList_extract_firstVideo_firstTimeFrame],
		                 downloadVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1))
		self.assertEqual([],
		                 downloadVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1))
		
		self.assertEqual([],
		                 downloadVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(2))
		self.assertEqual([startEndSecondsList_suppress_secondVideo_firstTimeFrame,
		                  startEndSecondsList_suppress_secondVideo_secondTimeFrame],
		                 downloadVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(2))

		self.assertEqual(validPlaylistDirName, targetAudioDir)
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.', downloadVideoInfoDic.getVideoTitleForVideoIndex(1))
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk', downloadVideoInfoDic.getVideoUrlForVideoIndex(1))
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk', downloadVideoInfoDic.getVideoUrlForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3', downloadVideoInfoDic.getVideoFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3', downloadVideoInfoDic.getVideoFileNameForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))

		self.assertEqual('Here to help: Give him what he wants', downloadVideoInfoDic.getVideoTitleForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw', downloadVideoInfoDic.getVideoUrlForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw', downloadVideoInfoDic.getVideoUrlForVideoTitle('Here to help: Give him what he wants'))
		self.assertEqual('Here to help - Give him what he wants.mp3', downloadVideoInfoDic.getVideoFileNameForVideoIndex(2))
		self.assertEqual('Here to help - Give him what he wants.mp3', downloadVideoInfoDic.getVideoFileNameForVideoTitle('Here to help: Give him what he wants'))

		self.assertEqual(['1', '2'], downloadVideoInfoDic.getVideoIndexes())

		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(
			sorted(['Here to help - Give him what he wants.mp3',
					'Wear a mask. Help slow the spread of Covid-19..mp3',
					'test_audio_downloader_two_files_with_time_frames_dic.txt']), sorted(fileNameLst))
	
	def testDownloadVideosReferencedInPlaylistForPlaylistUrl_invalid_url(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath() + sep)
		playlistUrl = "https://www.youtube.com/playlist?list=invalid"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistUrl)
		downloadVideoInfoDic, accessError = youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)
		
		sys.stdout = stdout
		
		self.assertEqual('trying to get the video title for the URL obtained from clipboard did not succeed.\nfailing URL: https://www.youtube.com/playlist?list=invalid\nerror info: regex_search: could not find match for (?:v=|\/)([0-9A-Za-z_-]{11}).*\nnothing to download.', accessError.errorMsg)
	
	def testDownloadVideosReferencedInPlaylistForPlaylistUrl_empty_url(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath() + sep)
		playlistUrl = ""
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndTitlesFortUrl(playlistUrl)

		sys.stdout = stdout
		
		self.assertEqual('the URL obtained from clipboard is empty.\nnothing to download.', accessError.errorMsg)
	
	def testDownloadVideosReferencedInPlaylistForPlaylistUrl_with_timeFrame(self):
		playlistName = 'Test_title_one_time_frame_extract'
		validPlaylistDirName = DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistName)
		downloadDir = DirUtil.getTestAudioRootPath() + sep + validPlaylistDirName

		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting files in downloadDir
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMTB7GasAttwVnPPk3-WTMNJ"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndTitlesFortUrl(playlistUrl)

		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)

		youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)

		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()

		sys.stdout = stdout

		self.assertIsNone(accessError)
		self.assertEqual(['downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
 '',
 'download complete.',
 '',
 '"Test_title_one_time_frame_extract" playlist audio(s) download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))

		self.assertEqual([[5, 10]], downloadVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1))
		self.assertEqual(validPlaylistDirName, targetAudioDir)
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.', downloadVideoInfoDic.getVideoTitleForVideoIndex(1))
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk', downloadVideoInfoDic.getVideoUrlForVideoIndex(1))
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk', downloadVideoInfoDic.getVideoUrlForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3', downloadVideoInfoDic.getVideoFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3', downloadVideoInfoDic.getVideoFileNameForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))

		self.assertEqual(['1'], downloadVideoInfoDic.getVideoIndexes())

		if os.name == 'posix':
			self.assertEqual('/storage/emulated/0/Download/Audiobooks/test/' + playlistName,
			                 downloadDir)
		else:
			self.assertEqual(DirUtil.getTestAudioRootPath() + sep + playlistName,
			                 downloadDir)

		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Test_title_one_time_frame_extract_dic.txt',
								 'Wear a mask. Help slow the spread of Covid-19..mp3']), sorted(fileNameLst))
		self.assertEqual([[5, 10]], downloadVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1))
	
	def testDownloadVideosReferencedInPlaylistForPlaylistUrlMultipleVideo_redownloading_the_playlist(self):
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
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRGA1T1vOn500RuLFo_lGJv"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString


		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndTitlesFortUrl(playlistUrl)

		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)

		youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)

		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()

		sys.stdout = stdout

		self.assertIsNone(accessError)
		self.assertEqual(
			['downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
			 '',
			 'download complete.',
			 '',
			 'downloading "Here to help: Give him what he wants" audio ...',
			 '',
			 'download complete.',
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
	
		youtubeAccess_redownload = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString

		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess_redownload.getPlaylistObjectAndTitlesFortUrl(playlistUrl)

		redownloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			youtubeAccess_redownload.audioDirRoot, youtubeAccess_redownload.audioDirRoot, playlistTitle)

		youtubeAccess_redownload.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, redownloadVideoInfoDic)

		targetAudioDir = redownloadVideoInfoDic.getPlaylistDownloadDir()

		sys.stdout = stdout

		self.assertIsNone(accessError)
		self.assertEqual(['"Wear a mask. Help slow the spread of Covid-19." audio already downloaded in '
 '"test\\test_audio_downloader_two_files" dir. Video skipped.',
 '',
 '"Here to help: Give him what he wants" audio already downloaded in '
 '"test\\test_audio_downloader_two_files" dir. Video skipped.',
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
		
	def testDownloadVideosReferencedInPlaylistForPlaylistUrlOneVideo_with_title_ending_with_question_mark_redownloading_the_playlist(self):
		playlistName = "Test playlist with one video whose title ends with ? char"
		validPlaylistDirName = DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistName)
		downloadDir = DirUtil.getTestAudioRootPath() + sep + validPlaylistDirName

		guiOutput = GuiOutputStub()
		playlistUrl = "https://youtube.com/playlist?list=PLzwWSJNcZTMTA4XDsubBsSfTCVLxqy1jG"

		# re-downloading the playlist
		
		youtubeAccess_redownload = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess_redownload.getPlaylistObjectAndTitlesFortUrl(playlistUrl)

		redownloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			youtubeAccess_redownload.audioDirRoot, youtubeAccess_redownload.audioDirRoot, playlistTitle)

		youtubeAccess_redownload.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, redownloadVideoInfoDic)

		targetAudioDir = redownloadVideoInfoDic.getPlaylistDownloadDir()
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)

		if os.name == 'posix':
			self.assertEqual(['"Comment Etudier Un Cours En Miracles ?" audio already downloaded in '
			                  '"test/Test playlist with one video whose title ends with \'\' char" dir. '
			                  'Video skipped.',
			                  '',
			                  '"Test playlist with one video whose title ends with \'?\' char" playlist '
			                  'audio(s) download terminated.',
			                  '',
			                  ''], outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual(['"Comment Etudier Un Cours En Miracles ?" audio already downloaded in '
 '"test\\Test playlist with one video whose title ends with  char" dir. Video '
 'skipped.',
 '',
 '"Test playlist with one video whose title ends with ? char" playlist '
 'audio(s) download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertEqual(validPlaylistDirName, targetAudioDir)
		self.assertEqual('Comment Etudier Un Cours En Miracles ?',
		                 redownloadVideoInfoDic.getVideoTitleForVideoIndex(1))
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Comment Etudier Un Cours En Miracles .mp3',
 "Test playlist with one video whose title ends with  char_dic.txt"]), sorted(fileNameLst))
	
	def testDownloadVideosReferencedInPlaylistForPlaylistUrlMultipleVideo_withTimeFrames_redownloading_the_playlist(self):
		# playlist title: test_audio_downloader_two_files_with_time_frames (e0:0:2-0:0:8) (s0:0:2-0:0:5 s0:0:7-0:0:10)
		time.sleep(1)   # required to avoid uncomprehensible test failure when executing all unit tsts
		originalPlaylistName = 'test_audio_downloader_two_files_with_time_frames'
		modifiedPlaylistName = 'test_audio_downloader_two_files_with_time_frames_redownloading'
		downloadDir = DirUtil.getTestAudioRootPath() + sep + modifiedPlaylistName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting files in downloadDir
		targerAudioPath = downloadDir + sep + modifiedPlaylistName
		
		files = glob.glob(targerAudioPath + sep + '*.*')
		
		for f in files:
			os.remove(f)

		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMSFWGrRGKOypqN29MlyuQvn"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, originalPlaylistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndTitlesFortUrl(playlistUrl)
		
		modifiedPlaylistTitle = originalPlaylistTitle.replace(originalPlaylistName, modifiedPlaylistName)

		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			audioRootDir=youtubeAccess.audioDirRoot,
			playlistDownloadRootPath=downloadDir,
			originalPlaylistTitle=originalPlaylistTitle,
			modifiedPlaylistTitle=modifiedPlaylistTitle)

		youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)

		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(
			['downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
			 '',
			 'download complete.',
			 '',
			 'downloading "Here to help: Give him what he wants" audio ...',
			 '',
			 'download complete.',
			 '',
			 '"test_audio_downloader_two_files_with_time_frames" playlist audio(s) download terminated.',
			 '',
			 ''], outputCapturingString.getvalue().split('\n'))
		
		# playlist title: test_audio_downloader_two_files_with_time_frames
		# (e0:0:2-0:0:8) (s0:0:2-0:0:5 s0:0:7-0:0:10)
		startEndSecondsList_extract_firstVideo_firstTimeFrame = [2, 8]
		
		startEndSecondsList_suppress_secondVideo_firstTimeFrame = [2, 5]
		startEndSecondsList_suppress_secondVideo_secondTimeFrame = [7, 10]
		
		self.assertEqual([startEndSecondsList_extract_firstVideo_firstTimeFrame],
		                 downloadVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1))
		self.assertEqual([],
		                 downloadVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1))
		
		self.assertEqual([],
		                 downloadVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(2))
		self.assertEqual([startEndSecondsList_suppress_secondVideo_firstTimeFrame,
		                  startEndSecondsList_suppress_secondVideo_secondTimeFrame],
		                 downloadVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(2))
		
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
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(targerAudioPath + sep + '*.*')]
		self.assertEqual(
			sorted(['Here to help - Give him what he wants.mp3',
			        'Wear a mask. Help slow the spread of Covid-19..mp3',
			        'test_audio_downloader_two_files_with_time_frames_redownloading_dic.txt']), sorted(fileNameLst))

		# re-downloading the playlist
		
		youtubeAccess_redownload = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, originalPlaylistTitle, videoTitle, accessError = \
			youtubeAccess_redownload.getPlaylistObjectAndTitlesFortUrl(playlistUrl)

		redownloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			youtubeAccess_redownload.audioDirRoot, youtubeAccess_redownload.audioDirRoot, originalPlaylistTitle)

		youtubeAccess_redownload.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, redownloadVideoInfoDic)

		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(['"Wear a mask. Help slow the spread of Covid-19." audio already downloaded in '
 '"test\\test_audio_downloader_two_files_with_time_frames" dir. Video skipped.',
 '',
 '"Here to help: Give him what he wants" audio already downloaded in '
 '"test\\test_audio_downloader_two_files_with_time_frames" dir. Video skipped.',
 '',
 '"test_audio_downloader_two_files_with_time_frames" playlist audio(s) '
 'download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertEqual([startEndSecondsList_extract_firstVideo_firstTimeFrame],
		                 redownloadVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1))
		self.assertEqual([],
		                 redownloadVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(1))
		
		self.assertEqual([],
		                 redownloadVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(2))
		self.assertEqual([startEndSecondsList_suppress_secondVideo_firstTimeFrame,
		                  startEndSecondsList_suppress_secondVideo_secondTimeFrame],
		                 redownloadVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(2))
		
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
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(targerAudioPath + sep + '*.*')]
		self.assertEqual(
			sorted(['Here to help - Give him what he wants.mp3',
			        'Wear a mask. Help slow the spread of Covid-19..mp3',
			        'test_audio_downloader_two_files_with_time_frames_redownloading_dic.txt']), sorted(fileNameLst))

	def testDownloadVideosReferencedInPlaylistForPlaylistUrlMultipleVideo_withTimeFrames_redownloading_the_playlist_after_adding_a_new_video(self):
		# re-downloading playlist with clearing all files but one in the destination dir
		# playlist title: test_audio_downloader_two_files_with_time_frames (e0:0:2-0:0:8) (s0:0:2-0:0:5 s0:0:7-0:0:10)
		playlistName = 'Test 3 short videos'
		validPlaylistDirName = DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistName)
		downloadDir = DirUtil.getTestAudioRootPath() + sep + validPlaylistDirName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting files in downloadDir
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = 'https://www.youtube.com/playlist?list=PLzwWSJNcZTMShenMgwyjHC8o5bU8QUPbn'
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndTitlesFortUrl(playlistUrl)

		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)

		youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(
			['downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
			 '',
			 'download complete.',
			 '',
			 'downloading "Here to help: Give him what he wants" audio ...',
			 '',
			 'download complete.',
			 '',
			 'downloading "Funny suspicious looking dog" audio ...',
			 '',
			 'download complete.',
			 '',
			 '"Test 3 short videos" playlist audio(s) download terminated.',
			 '',
			 ''], outputCapturingString.getvalue().split('\n'))
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(
			sorted(['Funny suspicious looking dog.mp3',
 'Here to help - Give him what he wants.mp3',
 'Test 3 short videos_dic.txt',
 'Wear a mask. Help slow the spread of Covid-19..mp3']), sorted(fileNameLst))
		
		# re-downloading the playlist after suppressing the files and data for
		# the last video
		
		# the last video files in downloadDir
		files = glob.glob(downloadDir + sep + '*.mp3')
		
		for f in files:
			if 'Funny suspicious looking dog' in f:
				os.remove(f)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		redownloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)
		redownloadVideoInfoDic.removeVideoInfoForVideoTitle('Funny suspicious looking dog')
		
		redownloadVideoInfoDic, accessError = youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(
			playlistUrl, redownloadVideoInfoDic)
		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(['"Wear a mask. Help slow the spread of Covid-19." audio already downloaded in '
 '"test\\Test 3 short videos" dir. Video skipped.',
 '',
 '"Here to help: Give him what he wants" audio already downloaded in '
 '"test\\Test 3 short videos" dir. Video skipped.',
 '',
 'downloading "Funny suspicious looking dog" audio ...',
 '',
 'download complete.',
 '',
 '"Test 3 short videos" playlist audio(s) download terminated.',
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
		
		self.assertEqual('Funny suspicious looking dog',
		                 redownloadVideoInfoDic.getVideoTitleForVideoIndex(4))
		self.assertEqual('https://www.youtube.com/watch?v=vU1NEZ9sTOM',
		                 redownloadVideoInfoDic.getVideoUrlForVideoIndex(4))
		self.assertEqual('https://www.youtube.com/watch?v=vU1NEZ9sTOM',
		                 redownloadVideoInfoDic.getVideoUrlForVideoTitle('Funny suspicious looking dog'))
		self.assertEqual('Funny suspicious looking dog.mp3',
		                 redownloadVideoInfoDic.getVideoFileNameForVideoIndex(4))
		self.assertEqual('Funny suspicious looking dog.mp3',
		                 redownloadVideoInfoDic.getVideoFileNameForVideoTitle(
			                 'Funny suspicious looking dog'))
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(
			sorted(['Funny suspicious looking dog.mp3',
 'Here to help - Give him what he wants.mp3',
 'Test 3 short videos_dic.txt',
 'Wear a mask. Help slow the spread of Covid-19..mp3']), sorted(fileNameLst))

	def testDownloadMaxNamePlaylist(self):
		"""
		Verifying that downloading a playlist whose name exceeds with only one char
		the max possible playlist name raises the awaited exception, which causes
		an adequate error msg to be outputted to the GUI output text field.
		
		WARNING: the exception raised is due to the download dir + sep + playlist name
		too long length, not to the playlist name only exceeding length !
		
		BUT what is uncomprehensible is that downloading this playlist with the
		AudioDownloaderGUI succeeds !
		"""
		playlistNameWindowsAcceptable = 'Je commence à être fatigué de ce problème impossible à analyser Je commence à être fatigué de ce problème impossible à analyser'
		downloadDir = DirUtil.getTestAudioRootPath() + sep + DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistNameWindowsAcceptable)
		
		# deleting downloadDir (dir and content)
		if os.path.exists(downloadDir):
			shutil.rmtree(downloadDir)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://youtube.com/playlist?list=PLzwWSJNcZTMRTPgK-xIKcbu5JbKpN49Tn"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndTitlesFortUrl(playlistUrl)

		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)

		youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)
		
		sys.stdout = stdout
		
		if os.name == 'posix':
			self.assertEqual(['directory',
 'test/Je commence à être fatigué de ce problème impossible à analyser Je '
 'commence à être fatigué de ce problème impossible à analyser',
 'was created.',
 '',
 'downloading "Les imaginaires effondristes sont les seuls qui tiennent la '
 'route - Arthur Keller" audio ...',
 '',
 'downloading video "Les imaginaires effondristes sont les seuls qui tiennent '
 'la route - Arthur Keller" caused this DownloadError exception: ERROR: '
 'file:C:/Users/Jean-Pierre/Downloads/Audio/test/Je commence à être '
 'fatigué de ce problème impossible à analyser Je commence à être fatigué de '
 'ce problème impossible à analyser/Les imaginaires effondristes sont les '
 'seuls qui tiennent la route - Arthur Keller.temp.m4a: No such file or '
 'directory. Playlist target dir '
 '"C:/Users/Jean-Pierre/Downloads/Audio/test/Je commence à être fatigué '
 'de ce problème impossible à analyser Je commence à être fatigué de ce '
 'problème impossible à analyser" length = 169 chars (max '
 'acceptable length = 168 chars) !',
 '"Je commence à être fatigué de ce problème impossible à analyser Je commence '
 'à être fatigué de ce problème impossible à analyser" playlist audio(s) '
 'download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual(['directory',
 'test\\Je commence à être fatigué de ce problème impossible à analyser Je '
 'commence à être fatigué de ce problème impossible à analyser',
 'was created.',
 '',
 'downloading "Les imaginaires effondristes sont les seuls qui tiennent la '
 'route - Arthur Keller" audio ...',
 '',
 'downloading video "Les imaginaires effondristes sont les seuls qui tiennent '
 'la route - Arthur Keller" caused this DownloadError exception: ERROR: '
 'file:C:\\Users\\Jean-Pierre\\Downloads\\Audio\\test\\Je commence à être '
 'fatigué de ce problème impossible à analyser Je commence à être fatigué de '
 'ce problème impossible à analyser\\Les imaginaires effondristes sont les '
 'seuls qui tiennent la route - Arthur Keller.temp.m4a: No such file or '
 'directory. Playlist target dir '
 '"C:\\Users\\Jean-Pierre\\Downloads\\Audio\\test\\Je commence à être fatigué '
 'de ce problème impossible à analyser Je commence à être fatigué de ce '
 'problème impossible à analyser" length = 169 chars (max '
 'acceptable length = 168 chars) !',
 '"Je commence à être fatigué de ce problème impossible à analyser Je commence '
 'à être fatigué de ce problème impossible à analyser" playlist audio(s) '
 'download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Les imaginaires effondristes sont les seuls qui tiennent la route - Arthur '
 'Keller.m4a']), sorted(fileNameLst))
	
	def testDownloadMaxNamePlaylist_with_point(self):
		"""
		Verifying that downloading a playlist whose name exceeds with only one char
		the max possible playlist name raises the awaited exception, which causes
		an adequate error msg to be outputted to the GUI output text field.
		
		In this test, the playlist name contins a point. The point will be removed
		from the created dir name. The point does not alter the error due to the
		exceeding download dir name + playlist name.

		WARNING: the exception raised is due to the download dir + sep + playlist name
		too long length, not to the playlist name only exceeding length !
		
		BUT what is uncomprehensible is that downloading this playlist with the
		AudioDownloaderGUI succeeds !
		"""
		playlistName = 'Il commence à être fatigué de ce problème impossible à analyser. Je commence à être fatigué de ce problème impossible à analyser'
		playlistNameWindowsAcceptable = 'Il commence à être fatigué de ce problème impossible à analyser Je commence à être fatigué de ce problème impossible à analyser'
		downloadDir = DirUtil.getTestAudioRootPath() + sep + DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistNameWindowsAcceptable)
		
		# deleting downloadDir (dir and content)
		if os.path.exists(downloadDir):
			shutil.rmtree(downloadDir)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://youtube.com/playlist?list=PLzwWSJNcZTMSqBPP5sFHilrgG6dbNr6ei"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndTitlesFortUrl(playlistUrl)

		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)

		youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)
		
		sys.stdout = stdout
		
		if os.name == 'posix':
			self.assertEqual(['directory',
 'test/Il commence à être fatigué de ce problème impossible à analyser Je '
 'commence à être fatigué de ce problème impossible à analyser',
 'was created.',
 '',
 'downloading "Les imaginaires effondristes sont les seuls qui tiennent la '
 'route - Arthur Keller" audio ...',
 '',
 'downloading video "Les imaginaires effondristes sont les seuls qui tiennent '
 'la route - Arthur Keller" caused this DownloadError exception: ERROR: '
 'file:C:/Users/Jean-Pierre/Downloads/Audio/test/Il commence à être '
 'fatigué de ce problème impossible à analyser Je commence à être fatigué de '
 'ce problème impossible à analyser/Les imaginaires effondristes sont les '
 'seuls qui tiennent la route - Arthur Keller.temp.m4a: No such file or '
 'directory. Playlist target dir '
 '"C:/Users/Jean-Pierre/Downloads/Audio/test/Il commence à être fatigué '
 'de ce problème impossible à analyser Je commence à être fatigué de ce '
 'problème impossible à analyser" length = 169 chars (max '
 'acceptable length = 168 chars) !',
 '"Il commence à être fatigué de ce problème impossible à analyser. Je '
 'commence à être fatigué de ce problème impossible à analyser" playlist '
 'audio(s) download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual(['directory',
 'test\\Il commence à être fatigué de ce problème impossible à analyser Je '
 'commence à être fatigué de ce problème impossible à analyser',
 'was created.',
 '',
 'downloading "Les imaginaires effondristes sont les seuls qui tiennent la '
 'route - Arthur Keller" audio ...',
 '',
 'downloading video "Les imaginaires effondristes sont les seuls qui tiennent '
 'la route - Arthur Keller" caused this DownloadError exception: ERROR: '
 'file:C:\\Users\\Jean-Pierre\\Downloads\\Audio\\test\\Il commence à être '
 'fatigué de ce problème impossible à analyser Je commence à être fatigué de '
 'ce problème impossible à analyser\\Les imaginaires effondristes sont les '
 'seuls qui tiennent la route - Arthur Keller.temp.m4a: No such file or '
 'directory. Playlist target dir '
 '"C:\\Users\\Jean-Pierre\\Downloads\\Audio\\test\\Il commence à être fatigué '
 'de ce problème impossible à analyser Je commence à être fatigué de ce '
 'problème impossible à analyser" length = 169 chars (max '
 'acceptable length = 168 chars) !',
 '"Il commence à être fatigué de ce problème impossible à analyser. Je '
 'commence à être fatigué de ce problème impossible à analyser" playlist '
 'audio(s) download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Les imaginaires effondristes sont les seuls qui tiennent la route - Arthur '
		                         'Keller.m4a']), sorted(fileNameLst))

		self.assertEqual(playlistName, downloadVideoInfoDic.getPlaylistNameOriginal())
		
	def testDownloadMaxNamePlaylist_minus_one_char(self):
		"""
		Verifying that downloading a playlist whose name length = one char less than
		the max possible playlist name is ok.
		"""
		playlistNameWindowsAcceptable = 'Je commence à être fatigué de ce problème impossible à analyser Je commence à être fatigué de ce problème impossible à analyse'
		downloadDir = DirUtil.getTestAudioRootPath() + sep + DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistNameWindowsAcceptable)
		
		# deleting downloadDir (dir and content)
		if os.path.exists(downloadDir):
			shutil.rmtree(downloadDir)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://youtube.com/playlist?list=PLzwWSJNcZTMQRlpXCFMkrgSnJXNRNAgn8"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString

		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndTitlesFortUrl(playlistUrl)

		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)

		youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)
		
		sys.stdout = stdout
		
		if os.name == 'posix':
			self.assertEqual(['directory',
			                  'test/Je commence à être fatigué de ce problème impossible à analyser Je '
			                  'commence à être fatigué de ce problème impossible à analyse',
			                  'was created.',
			                  '',
			                  'downloading "Les imaginaires effondristes sont les seuls qui tiennent la '
			                  'route - Arthur Keller" audio ...',
			                  '',
			                  '"Les imaginaires effondristes sont les seuls qui tiennent la route - Arthur '
			                  'Keller" audio downloaded.',
			                  '',
			                  '"Je commence à être fatigué de ce problème impossible à analyser Je commence '
			                  'à être fatigué de ce problème impossible à analyse" playlist audio(s) '
			                  'download terminated.',
			                  '',
			                  ''], outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual(['directory',
			                  'test\\Je commence à être fatigué de ce problème impossible à analyser Je '
			                  'commence à être fatigué de ce problème impossible à analyse',
			                  'was created.',
			                  '',
			                  'downloading "Les imaginaires effondristes sont les seuls qui tiennent la '
			                  'route - Arthur Keller" audio ...',
			                  '',
			                  'download complete.',
'',
			                  '"Je commence à être fatigué de ce problème impossible à analyser Je commence '
			                  'à être fatigué de ce problème impossible à analyse" playlist audio(s) '
			                  'download terminated.',
			                  '',
			                  ''], outputCapturingString.getvalue().split('\n'))
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Je commence à être fatigué de ce problème impossible à analyser Je commence '
		                         'à être fatigué de ce problème impossible à analyse_dic.txt',
		                         'Les imaginaires effondristes sont les seuls qui tiennent la route - Arthur '
		                         'Keller.mp3']), sorted(fileNameLst))
	
	def testDownloadMaxNamePlaylist_minus_one_char_with_point(self):
		"""
		Verifying that downloading a playlist whose name length = one char less than
		the max possible playlist name is ok.

		In this test, the playlist name contains a point. The point will be removed
		from the created dir name. The point does not alter the fact that the playlist
		download succeeds.
		"""
		playlistName = 'G commence à être fatigué de ce problème impossible à analyser. Je commence à être fatigué de ce problème impossible à analyser'
		playlistNameWindowsAcceptable = 'G commence à être fatigué de ce problème impossible à analyser Je commence à être fatigué de ce problème impossible à analyser'
		downloadDir = DirUtil.getTestAudioRootPath() + sep + DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistNameWindowsAcceptable)
		
		# deleting downloadDir (dir and content)
		if os.path.exists(downloadDir):
			shutil.rmtree(downloadDir)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://youtube.com/playlist?list=PLzwWSJNcZTMQBqzowzbM5XlJkYw0Ovl5W"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndTitlesFortUrl(playlistUrl)

		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)

		youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)
		
		sys.stdout = stdout
		
		if os.name == 'posix':
			self.assertEqual(['directory',
 'test/G commence à être fatigué de ce problème impossible à analyser Je '
 'commence à être fatigué de ce problème impossible à analyser',
 'was created.',
 '',
 'downloading "Les imaginaires effondristes sont les seuls qui tiennent la '
 'route - Arthur Keller" audio ...',
 '',
 '"Les imaginaires effondristes sont les seuls qui tiennent la route - Arthur '
 'Keller" audio downloaded.',
 '',
 '"G commence à être fatigué de ce problème impossible à analyser. Je commence '
 'à être fatigué de ce problème impossible à analyser" playlist audio(s) '
 'download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual(['directory',
 'test\\G commence à être fatigué de ce problème impossible à analyser Je '
 'commence à être fatigué de ce problème impossible à analyser',
 'was created.',
 '',
 'downloading "Les imaginaires effondristes sont les seuls qui tiennent la '
 'route - Arthur Keller" audio ...',
 '',
 'download complete.',
 '',
 '"G commence à être fatigué de ce problème impossible à analyser. Je commence '
 'à être fatigué de ce problème impossible à analyser" playlist audio(s) '
 'download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['G commence à être fatigué de ce problème impossible à analyser Je commence à '
 'être fatigué de ce problème impossible à analyser_dic.txt',
 'Les imaginaires effondristes sont les seuls qui tiennent la route - Arthur '
 'Keller.mp3']), sorted(fileNameLst))

		self.assertEqual(playlistName, downloadVideoInfoDic.getPlaylistNameOriginal())

	def testDownloaTooLongNamePlaylist_127_char_oneShortVideo_targetFolder_not_exist(self):
		playlistName = '127 char_____playlist name is very long and will cause a problem if the target dir name exceeds a maximum possible too big name.'
		downloadDir = DirUtil.getTestAudioRootPath() + sep + DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistName)
		
		# deleting downloadDir (dir and content)
		if os.path.exists(downloadDir):
			shutil.rmtree(downloadDir)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://youtube.com/playlist?list=PLzwWSJNcZTMQou0yHh8npCY2_ls8dwgVn"
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString

		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndTitlesFortUrl(playlistUrl)

		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)

		youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)
		
		sys.stdout = stdout
		
		if os.name == 'posix':
			self.assertEqual(['directory',
 'test/127 char_____playlist name is very long and will cause a problem if '
 'the target dir name exceeds a maximum possible too big name',
 'was created.',
 '',
 'downloading "Les imaginaires effondristes sont les seuls qui tiennent la '
 'route - Arthur Keller" audio ...',
 '',
 'downloading video "Les imaginaires effondristes sont les seuls qui tiennent '
 'la route - Arthur Keller" caused this DownloadError exception: ERROR: '
 'file:C:/Users/Jean-Pierre/Downloads/Audio/test/127 char_____playlist '
 'name is very long and will cause a problem if the target dir name exceeds a '
 'maximum possible too big name/Les imaginaires effondristes sont les seuls '
 'qui tiennent la route - Arthur Keller.temp.m4a: No such file or directory. '
 'Playlist target dir "C:/Users/Jean-Pierre/Downloads/Audio/test/127 '
 'char_____playlist name is very long and will cause a problem if the target '
 'dir name exceeds a maximum possible too big name" length = 169 chars (max '
 'acceptable length = 168 chars) !',
 '"127 char_____playlist name is very long and will cause a problem if the '
 'target dir name exceeds a maximum possible too big name." playlist audio(s) '
 'download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual(['directory',
 'test\\127 char_____playlist name is very long and will cause a problem if '
 'the target dir name exceeds a maximum possible too big name',
 'was created.',
 '',
 'downloading "Les imaginaires effondristes sont les seuls qui tiennent la '
 'route - Arthur Keller" audio ...',
 '',
 'downloading video "Les imaginaires effondristes sont les seuls qui tiennent '
 'la route - Arthur Keller" caused this DownloadError exception: ERROR: '
 'file:C:\\Users\\Jean-Pierre\\Downloads\\Audio\\test\\127 char_____playlist '
 'name is very long and will cause a problem if the target dir name exceeds a '
 'maximum possible too big name\\Les imaginaires effondristes sont les seuls '
 'qui tiennent la route - Arthur Keller.temp.m4a: No such file or directory. '
 'Playlist target dir "C:\\Users\\Jean-Pierre\\Downloads\\Audio\\test\\127 '
 'char_____playlist name is very long and will cause a problem if the target '
 'dir name exceeds a maximum possible too big name" length = 169 chars (max '
 'acceptable length = 168 chars) !',
 '"127 char_____playlist name is very long and will cause a problem if the '
 'target dir name exceeds a maximum possible too big name." playlist audio(s) '
 'download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Les imaginaires effondristes sont les seuls qui tiennent la route - Arthur '
 'Keller.m4a']), sorted(fileNameLst))
	
	def testDownloadPlaylistWithName_two_points(self):
		playlistName = "test short_n\'ame pl, aylist: avec deux points"
		playlistDirName = "test short_n_ame pl, aylist avec deux points"
		downloadDir = DirUtil.getTestAudioRootPath() + sep + playlistDirName
		
		# deleting downloadDir (dir and content)
		if os.path.exists(downloadDir):
			shutil.rmtree(downloadDir)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://youtube.com/playlist?list=PLzwWSJNcZTMSg3vAMZWqdGiEPQEuZi2Zh"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndTitlesFortUrl(playlistUrl)

		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)

		youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)
		
		sys.stdout = stdout
		
		if os.name == 'posix':
			self.assertEqual(['directory',
			                  'test/test_audio_downloader_one_file',
			                  'was created.',
			                  '',
			                  'downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
			                  '',
			                  '"Wear a mask. Help slow the spread of Covid-19." audio downloaded.',
			                  '',
			                  ''], outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual(['directory',
 "test\\test short_n_ame pl, aylist avec deux points",
 'was created.',
 '',
 'downloading "Les imaginaires effondristes sont les seuls qui tiennent la '
 'route - Arthur Keller" audio ...',
 '',
 'download complete.',
 '',
 '"test short_n\'ame pl, aylist: avec deux points" playlist audio(s) download '
 'terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*')]
		self.assertEqual(sorted(['Les imaginaires effondristes sont les seuls qui tiennent la route - Arthur '
 'Keller.mp3',
 "test short_n_ame pl, aylist avec deux points_dic.txt"]), sorted(fileNameLst))

		self.assertEqual(playlistName, downloadVideoInfoDic.getPlaylistNameOriginal())

	def testRedownloading_the_playlist_with_deleted_audio_files(self):
		time.sleep(1)
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
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRGA1T1vOn500RuLFo_lGJv"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndTitlesFortUrl(playlistUrl)

		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)

		youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)

		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(
			['downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
			 '',
			 'download complete.',
			 '',
			 'downloading "Here to help: Give him what he wants" audio ...',
			 '',
			 'download complete.',
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
		
		youtubeAccess_redownload = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess_redownload.getPlaylistObjectAndTitlesFortUrl(playlistUrl)

		redownloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			youtubeAccess_redownload.audioDirRoot, youtubeAccess_redownload.audioDirRoot, playlistTitle)

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
	tst.testDownloadVideosReferencedInPlaylistForPlaylistUrlMultipleVideo_withTimeFrames()
