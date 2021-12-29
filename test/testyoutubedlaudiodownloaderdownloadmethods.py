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

class TestYoutubeDlAudioDownloaderDownloadMethods(unittest.TestCase):
	"""
	Since testing download consume band width, it is placed in a specific test class.
	"""
	def testDownloadPlaylistVideosForUrl_targetFolder_exist(self):
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
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess = YoutubeDlAudioDownloader(audioController, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS"
		
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

		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()

		sys.stdout = stdout

		self.assertIsNone(accessError)
		self.assertEqual(['downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
 '',
 'video download complete.',
 '',
 '"test_audio_downloader_one_file" playlist audio(s) download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))

		self.assertEqual(validPlaylistDirName, targetAudioDir)
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.', downloadVideoInfoDic.getVideoTitleForVideoIndex(1))
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk', downloadVideoInfoDic.getVideoUrlForVideoIndex(1))
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk', downloadVideoInfoDic.getVideoUrlForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3', downloadVideoInfoDic.getVideoAudioFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3', downloadVideoInfoDic.getVideoAudioFileNameForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))
		self.assertEqual(['1'], downloadVideoInfoDic.getVideoIndexStrings())

		if os.name == 'posix':
			self.assertEqual('/storage/emulated/0/Download/Audiobooks/test_audio_downloader_one_file',
			                 downloadDir)
		else:
			self.assertEqual('{}test_audio_downloader_one_file'.format(DirUtil.getTestAudioRootPath() + sep), downloadDir)

		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Wear a mask. Help slow the spread of Covid-19..mp3',
								 'test_audio_downloader_one_file_dic.txt']), sorted(fileNameLst))

	def testDownloadPlaylistVideosForUrl_targetFolder_not_exist(self):
		playlistName = 'test_audio_downloader_one_file'
		downloadDir = DirUtil.getTestAudioRootPath() + sep + DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistName)

		# deleting downloadDir (dir and content)
		if os.path.exists(downloadDir):
			shutil.rmtree(downloadDir)
		
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess = YoutubeDlAudioDownloader(audioController, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS"
		
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
 'video download complete.',
 '',
 '"test_audio_downloader_one_file" playlist audio(s) download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))

		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Wear a mask. Help slow the spread of Covid-19..mp3',
								 'test_audio_downloader_one_file_dic.txt']), sorted(fileNameLst))

	def testDownloadPlaylistVideosForUrlMultipleVideo(self):
		playlistName = 'test_audio_downloader_two_files'
		subTestDirName = '1'
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
			youtubeAccess.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)

		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			playlistUrl, youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)

		youtubeAccess.downloadPlaylistVideosForUrl(playlistUrl=playlistUrl,
		                                           downloadVideoInfoDic=downloadVideoInfoDic,
		                                           isUploadDateSuffixAddedToPlaylistVideo=False,
		                                           isDownloadDatePrefixAddedToPlaylistVideo=False)

		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()
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

		self.assertEqual(validPlaylistDirName, targetAudioDir)
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.', downloadVideoInfoDic.getVideoTitleForVideoIndex(1))
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk', downloadVideoInfoDic.getVideoUrlForVideoIndex(1))
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk', downloadVideoInfoDic.getVideoUrlForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3', downloadVideoInfoDic.getVideoAudioFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3', downloadVideoInfoDic.getVideoAudioFileNameForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))

		self.assertEqual('Here to help: Give him what he wants', downloadVideoInfoDic.getVideoTitleForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw', downloadVideoInfoDic.getVideoUrlForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw', downloadVideoInfoDic.getVideoUrlForVideoTitle('Here to help: Give him what he wants'))
		self.assertEqual('Here to help - Give him what he wants.mp3', downloadVideoInfoDic.getVideoAudioFileNameForVideoIndex(2))
		self.assertEqual('Here to help - Give him what he wants.mp3', downloadVideoInfoDic.getVideoAudioFileNameForVideoTitle('Here to help: Give him what he wants'))

		self.assertEqual(['1', '2'], downloadVideoInfoDic.getVideoIndexStrings())

		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Here to help - Give him what he wants.mp3',
								 'Wear a mask. Help slow the spread of Covid-19..mp3',
								 'test_audio_downloader_two_files_dic.txt']), sorted(fileNameLst))
	
	def testDownloadPlaylistVideosForUrlMultipleVideo_withTimeFrames(self):
		# playlist title: test_audio_downloader_two_files_with_time_frames (e0:0:2-0:0:8) (s0:0:2-0:0:5 s0:0:7-0:0:10)
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
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess = YoutubeDlAudioDownloader(audioController, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMSFWGrRGKOypqN29MlyuQvn"
		
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
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3', downloadVideoInfoDic.getVideoAudioFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3', downloadVideoInfoDic.getVideoAudioFileNameForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))

		self.assertEqual('Here to help: Give him what he wants', downloadVideoInfoDic.getVideoTitleForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw', downloadVideoInfoDic.getVideoUrlForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw', downloadVideoInfoDic.getVideoUrlForVideoTitle('Here to help: Give him what he wants'))
		self.assertEqual('Here to help - Give him what he wants.mp3', downloadVideoInfoDic.getVideoAudioFileNameForVideoIndex(2))
		self.assertEqual('Here to help - Give him what he wants.mp3', downloadVideoInfoDic.getVideoAudioFileNameForVideoTitle('Here to help: Give him what he wants'))

		self.assertEqual(['1', '2'], downloadVideoInfoDic.getVideoIndexStrings())

		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(
			sorted(['Here to help - Give him what he wants.mp3',
					'Wear a mask. Help slow the spread of Covid-19..mp3',
					'test_audio_downloader_two_files_with_time_frames_dic.txt']), sorted(fileNameLst))

	@unittest.skip # this test takes too much time
	def testDownloadPlaylistVideosForUrl_invalid_url(self):
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess = YoutubeDlAudioDownloader(audioController, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://www.youtube.com/playlist?list=invalid"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			playlistUrl, youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistUrl)
		downloadVideoInfoDic, accessError = youtubeAccess.downloadPlaylistVideosForUrl(
			playlistUrl=playlistUrl,
			downloadVideoInfoDic=downloadVideoInfoDic,
			isUploadDateSuffixAddedToPlaylistVideo=False,
			isDownloadDatePrefixAddedToPlaylistVideo=False)

		
		sys.stdout = stdout
		
		self.assertEqual("trying to get the video title for the URL obtained from clipboard did not succeed.\nfailing URL: https://www.youtube.com/playlist?list=invalid\nerror info: 'title'\nnothing to download.", accessError.errorMsg)
	
	def testDownloadPlaylistVideosForUrl_empty_url(self):
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess = YoutubeDlAudioDownloader(audioController, DirUtil.getTestAudioRootPath())
		playlistUrl = ""
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)

		sys.stdout = stdout
		
		self.assertEqual('the URL obtained from clipboard is empty.\nnothing to download.', accessError.errorMsg)
	
	def testDownloadPlaylistVideosForUrl_with_timeFrame(self):
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
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess = YoutubeDlAudioDownloader(audioController, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMTB7GasAttwVnPPk3-WTMNJ"
		
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

		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()

		sys.stdout = stdout

		self.assertIsNone(accessError)
		self.assertEqual(['downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
 '',
 'video download complete.',
 '',
 '"Test_title_one_time_frame_extract" playlist audio(s) download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))

		self.assertEqual([[5, 10]], downloadVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1))
		self.assertEqual(validPlaylistDirName, targetAudioDir)
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.', downloadVideoInfoDic.getVideoTitleForVideoIndex(1))
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk', downloadVideoInfoDic.getVideoUrlForVideoIndex(1))
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk', downloadVideoInfoDic.getVideoUrlForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3', downloadVideoInfoDic.getVideoAudioFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3', downloadVideoInfoDic.getVideoAudioFileNameForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))

		self.assertEqual(['1'], downloadVideoInfoDic.getVideoIndexStrings())

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
			youtubeAccess.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)

		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			playlistUrl, youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)

		youtubeAccess.downloadPlaylistVideosForUrl(playlistUrl=playlistUrl,
		                                           downloadVideoInfoDic=downloadVideoInfoDic,
		                                           isUploadDateSuffixAddedToPlaylistVideo=False,
		                                           isDownloadDatePrefixAddedToPlaylistVideo=False)

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
		                 downloadVideoInfoDic.getVideoAudioFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3',
		                 downloadVideoInfoDic.getVideoAudioFileNameForVideoTitle(
			                 'Wear a mask. Help slow the spread of Covid-19.'))
		
		self.assertEqual('Here to help: Give him what he wants',
		                 downloadVideoInfoDic.getVideoTitleForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                 downloadVideoInfoDic.getVideoUrlForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                 downloadVideoInfoDic.getVideoUrlForVideoTitle('Here to help: Give him what he wants'))
		self.assertEqual('Here to help - Give him what he wants.mp3',
		                 downloadVideoInfoDic.getVideoAudioFileNameForVideoIndex(2))
		self.assertEqual('Here to help - Give him what he wants.mp3',
		                 downloadVideoInfoDic.getVideoAudioFileNameForVideoTitle(
			                 'Here to help: Give him what he wants'))
		
		self.assertEqual(['1', '2'], downloadVideoInfoDic.getVideoIndexStrings())
		
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
			youtubeAccess_redownload.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)

		redownloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			playlistUrl, youtubeAccess_redownload.audioDirRoot, youtubeAccess_redownload.audioDirRoot, playlistTitle)

		youtubeAccess_redownload.downloadPlaylistVideosForUrl(playlistUrl=playlistUrl,
		                                                      downloadVideoInfoDic=redownloadVideoInfoDic,
		                                                      isUploadDateSuffixAddedToPlaylistVideo=False,
		                                                      isDownloadDatePrefixAddedToPlaylistVideo=False)

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
		                 redownloadVideoInfoDic.getVideoAudioFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3',
		                 redownloadVideoInfoDic.getVideoAudioFileNameForVideoTitle(
			                 'Wear a mask. Help slow the spread of Covid-19.'))
		
		self.assertEqual('Here to help: Give him what he wants',
		                 redownloadVideoInfoDic.getVideoTitleForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                 redownloadVideoInfoDic.getVideoUrlForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                 redownloadVideoInfoDic.getVideoUrlForVideoTitle('Here to help: Give him what he wants'))
		self.assertEqual('Here to help - Give him what he wants.mp3',
		                 redownloadVideoInfoDic.getVideoAudioFileNameForVideoIndex(2))
		self.assertEqual('Here to help - Give him what he wants.mp3',
		                 redownloadVideoInfoDic.getVideoAudioFileNameForVideoTitle(
			                 'Here to help: Give him what he wants'))
		
		self.assertEqual(['1', '2'], redownloadVideoInfoDic.getVideoIndexStrings())
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Here to help - Give him what he wants.mp3',
		                         'Wear a mask. Help slow the spread of Covid-19..mp3',
		                         'test_audio_downloader_two_files_dic.txt']), sorted(fileNameLst))
		
	def testDownloadPlaylistVideosForUrlOneVideo_with_title_ending_with_question_mark_redownloading_the_playlist(self):
		playlistName = "Test playlist with one video whose title ends with ? char"
		validPlaylistDirName = DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistName)
		downloadDir = DirUtil.getTestAudioRootPath() + sep + validPlaylistDirName

		guiOutput = GuiOutputStub()
		playlistUrl = "https://youtube.com/playlist?list=PLzwWSJNcZTMTA4XDsubBsSfTCVLxqy1jG"

		# re-downloading the playlist
		
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess_redownload = YoutubeDlAudioDownloader(audioController, DirUtil.getTestAudioRootPath())
		
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
			self.assertEqual(['"Comment Etudier Un Cours En Miracles .mp3" audio already downloaded in '
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
	
	def testDownloadPlaylistVideosForUrlMultipleVideo_withTimeFrames_redownloading_the_playlist(self):
		# playlist title: test_audio_downloader_two_files_with_time_frames (e0:0:2-0:0:8) (s0:0:2-0:0:5 s0:0:7-0:0:10)
		originalPlaylistName = 'test_audio_downloader_two_files_with_time_frames'
		modifiedPlaylistName = 'test_audio_downloader_two_files_with_time_frames_redownloading'
		downloadDir = DirUtil.getTestAudioRootPath()
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting files in downloadDir
		targetAudioPath = downloadDir + sep + modifiedPlaylistName
		
		files = glob.glob(targetAudioPath + sep + '*.*')
		
		for f in files:
			os.remove(f)

		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess = YoutubeDlAudioDownloader(audioController, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMSFWGrRGKOypqN29MlyuQvn"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, originalPlaylistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)
		
		modifiedPlaylistTitle = originalPlaylistTitle.replace(originalPlaylistName, modifiedPlaylistName)

		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			playlistUrl=playlistUrl,
			audioRootDir=youtubeAccess.audioDirRoot,
			playlistDownloadRootPath=downloadDir,
			originalPlaylistTitle=originalPlaylistTitle,
			modifiedPlaylistTitle=modifiedPlaylistTitle)

		youtubeAccess.downloadPlaylistVideosForUrl(playlistUrl=playlistUrl,
		                                           downloadVideoInfoDic=downloadVideoInfoDic,
		                                           isUploadDateSuffixAddedToPlaylistVideo=False,
		                                           isDownloadDatePrefixAddedToPlaylistVideo=False)

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
		                 downloadVideoInfoDic.getVideoAudioFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3',
		                 downloadVideoInfoDic.getVideoAudioFileNameForVideoTitle(
			                 'Wear a mask. Help slow the spread of Covid-19.'))
		
		self.assertEqual('Here to help: Give him what he wants',
		                 downloadVideoInfoDic.getVideoTitleForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                 downloadVideoInfoDic.getVideoUrlForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                 downloadVideoInfoDic.getVideoUrlForVideoTitle('Here to help: Give him what he wants'))
		self.assertEqual('Here to help - Give him what he wants.mp3',
		                 downloadVideoInfoDic.getVideoAudioFileNameForVideoIndex(2))
		self.assertEqual('Here to help - Give him what he wants.mp3',
		                 downloadVideoInfoDic.getVideoAudioFileNameForVideoTitle(
			                 'Here to help: Give him what he wants'))
		
		self.assertEqual(['1', '2'], downloadVideoInfoDic.getVideoIndexStrings())
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(targetAudioPath + sep + '*.*')]
		self.assertEqual(
			sorted(['Here to help - Give him what he wants.mp3',
			        'Wear a mask. Help slow the spread of Covid-19..mp3',
			        'test_audio_downloader_two_files_with_time_frames_redownloading_dic.txt']), sorted(fileNameLst))

		# re-downloading the playlist
		
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess_redownload = YoutubeDlAudioDownloader(audioController, DirUtil.getTestAudioRootPath())
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, originalPlaylistTitle, videoTitle, accessError = \
			youtubeAccess_redownload.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)

		redownloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			playlistUrl, youtubeAccess_redownload.audioDirRoot, youtubeAccess_redownload.audioDirRoot, originalPlaylistTitle)

		youtubeAccess_redownload.downloadPlaylistVideosForUrl(playlistUrl=playlistUrl,
		                                                      downloadVideoInfoDic=redownloadVideoInfoDic,
		                                                      isUploadDateSuffixAddedToPlaylistVideo=False,
		                                                      isDownloadDatePrefixAddedToPlaylistVideo=False)

		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(['"Wear a mask. Help slow the spread of Covid-19..mp3" audio already '
 'downloaded in "test\\test_audio_downloader_two_files_with_time_frames" dir. '
 'Video skipped.',
 '',
 '"Here to help - Give him what he wants.mp3" audio already downloaded in '
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
		                 redownloadVideoInfoDic.getVideoAudioFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3',
		                 redownloadVideoInfoDic.getVideoAudioFileNameForVideoTitle(
			                 'Wear a mask. Help slow the spread of Covid-19.'))
		
		self.assertEqual('Here to help: Give him what he wants',
		                 redownloadVideoInfoDic.getVideoTitleForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                 redownloadVideoInfoDic.getVideoUrlForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                 redownloadVideoInfoDic.getVideoUrlForVideoTitle('Here to help: Give him what he wants'))
		self.assertEqual('Here to help - Give him what he wants.mp3',
		                 redownloadVideoInfoDic.getVideoAudioFileNameForVideoIndex(2))
		self.assertEqual('Here to help - Give him what he wants.mp3',
		                 redownloadVideoInfoDic.getVideoAudioFileNameForVideoTitle(
			                 'Here to help: Give him what he wants'))
		
		self.assertEqual(['1', '2'], redownloadVideoInfoDic.getVideoIndexStrings())
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(targetAudioPath + sep + '*.*')]
		self.assertEqual(
			sorted(['Here to help - Give him what he wants.mp3',
			        'Wear a mask. Help slow the spread of Covid-19..mp3',
			        'test_audio_downloader_two_files_with_time_frames_redownloading_dic.txt']), sorted(fileNameLst))

	def testDownloadPlaylistVideosForUrlMultipleVideo_withTimeFrames_redownloading_the_playlist_after_adding_a_new_video(self):
		# re-downloading playlist with clearing all files but one in the destination dir
		# playlist title: test_audio_downloader_two_files_with_time_frames (e0:0:2-0:0:8) (s0:0:2-0:0:5 s0:0:7-0:0:10)
		playlistName = 'Test download three short videos'
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
		playlistUrl = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRlLR6cTkwSBjduI5HOh71R'
		
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
		self.assertEqual(
			['downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
			 '',
			 'video download complete.',
			 '',
			 'downloading "Here to help: Give him what he wants" audio ...',
			 '',
			 'video download complete.',
			 '',
			 'downloading "Funny suspicious looking dog" audio ...',
			 '',
			 'video download complete.',
			 '',
			 '"Test download three short videos" playlist audio(s) download terminated.',
			 '',
			 ''], outputCapturingString.getvalue().split('\n'))
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(
			sorted(['Funny suspicious looking dog.mp3',
 'Here to help - Give him what he wants.mp3',
 'Test download three short videos_dic.txt',
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
			playlistUrl, youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)
		redownloadVideoInfoDic.removeVideoInfoForVideoTitle('Funny suspicious looking dog')
		
		redownloadVideoInfoDic, accessError = youtubeAccess.downloadPlaylistVideosForUrl(
			playlistUrl=playlistUrl,
			downloadVideoInfoDic=redownloadVideoInfoDic,
			isUploadDateSuffixAddedToPlaylistVideo=False,
			isDownloadDatePrefixAddedToPlaylistVideo=False)
		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(['"Wear a mask. Help slow the spread of Covid-19..mp3" audio already '
 'downloaded in "test\\Test download three short videos" dir. Video skipped.',
 '',
 '"Here to help - Give him what he wants.mp3" audio already downloaded in '
 '"test\\Test download three short videos" dir. Video skipped.',
 '',
 'downloading "Funny suspicious looking dog" audio ...',
 '',
 'video download complete.',
 '',
 '"Test download three short videos" playlist audio(s) download terminated.',
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
		                 redownloadVideoInfoDic.getVideoAudioFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3',
		                 redownloadVideoInfoDic.getVideoAudioFileNameForVideoTitle(
			                 'Wear a mask. Help slow the spread of Covid-19.'))
		
		self.assertEqual('Here to help: Give him what he wants',
		                 redownloadVideoInfoDic.getVideoTitleForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                 redownloadVideoInfoDic.getVideoUrlForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                 redownloadVideoInfoDic.getVideoUrlForVideoTitle('Here to help: Give him what he wants'))
		self.assertEqual('Here to help - Give him what he wants.mp3',
		                 redownloadVideoInfoDic.getVideoAudioFileNameForVideoIndex(2))
		self.assertEqual('Here to help - Give him what he wants.mp3',
		                 redownloadVideoInfoDic.getVideoAudioFileNameForVideoTitle(
			                 'Here to help: Give him what he wants'))
		
		self.assertEqual('Funny suspicious looking dog',
		                 redownloadVideoInfoDic.getVideoTitleForVideoIndex(4))
		self.assertEqual('https://www.youtube.com/watch?v=vU1NEZ9sTOM',
		                 redownloadVideoInfoDic.getVideoUrlForVideoIndex(4))
		self.assertEqual('https://www.youtube.com/watch?v=vU1NEZ9sTOM',
		                 redownloadVideoInfoDic.getVideoUrlForVideoTitle('Funny suspicious looking dog'))
		self.assertEqual('Funny suspicious looking dog.mp3',
		                 redownloadVideoInfoDic.getVideoAudioFileNameForVideoIndex(4))
		self.assertEqual('Funny suspicious looking dog.mp3',
		                 redownloadVideoInfoDic.getVideoAudioFileNameForVideoTitle(
			                 'Funny suspicious looking dog'))
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(
			sorted(['Funny suspicious looking dog.mp3',
 'Here to help - Give him what he wants.mp3',
 'Test download three short videos_dic.txt',
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
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess = YoutubeDlAudioDownloader(audioController, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://youtube.com/playlist?list=PLzwWSJNcZTMRTPgK-xIKcbu5JbKpN49Tn"
		
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
 'file:D:/Users/Jean-Pierre/Downloads/Audio/test/Je commence à être '
 'fatigué de ce problème impossible à analyser Je commence à être fatigué de '
 'ce problème impossible à analyser/Les imaginaires effondristes sont les '
 'seuls qui tiennent la route - Arthur Keller.temp.mp3: No such file or '
 'directory. Playlist target dir '
 '"D:/Users/Jean-Pierre/Downloads/Audio/test/Je commence à être fatigué '
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
 'file:D:\\Users\\Jean-Pierre\\Downloads\\Audio\\test\\Je commence à être '
 'fatigué de ce problème impossible à analyser Je commence à être fatigué de '
 'ce problème impossible à analyser\\Les imaginaires effondristes sont les '
 'seuls qui tiennent la route - Arthur Keller.temp.mp3: No such file or '
 'directory.',
 '',
 'retry downloading the playlist later to download the failed audio only ...',
 '',
 '"Je commence à être fatigué de ce problème impossible à analyser Je commence '
 'à être fatigué de ce problème impossible à analyser" playlist audio(s) '
 'download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Les imaginaires effondristes sont les seuls qui tiennent la route - Arthur '
 'Keller.mp3']), sorted(fileNameLst))
	
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
		playlistNameWindowsAcceptable = 'Il commence à être fatigué de ce problème impossible à analyser. Je commence à être fatigué de ce problème impossible à analyser'
		downloadDir = DirUtil.getTestAudioRootPath() + sep + DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistNameWindowsAcceptable)
		
		# deleting downloadDir (dir and content)
		if os.path.exists(downloadDir):
			shutil.rmtree(downloadDir)
		
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess = YoutubeDlAudioDownloader(audioController, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://youtube.com/playlist?list=PLzwWSJNcZTMSqBPP5sFHilrgG6dbNr6ei"
		
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
 'file:D:/Users/Jean-Pierre/Downloads/Audio/test/Il commence à être '
 'fatigué de ce problème impossible à analyser Je commence à être fatigué de '
 'ce problème impossible à analyser/Les imaginaires effondristes sont les '
 'seuls qui tiennent la route - Arthur Keller.temp.mp3: No such file or '
 'directory. Playlist target dir '
 '"D:/Users/Jean-Pierre/Downloads/Audio/test/Il commence à être fatigué '
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
 'test\\Il commence à être fatigué de ce problème impossible à analyser. Je '
 'commence à être fatigué de ce problème impossible à analyser',
 'was created.',
 '',
 'downloading "Les imaginaires effondristes sont les seuls qui tiennent la '
 'route - Arthur Keller" audio ...',
 '',
 'downloading video "Les imaginaires effondristes sont les seuls qui tiennent '
 'la route - Arthur Keller" caused this DownloadError exception: ERROR: '
 'file:D:\\Users\\Jean-Pierre\\Downloads\\Audio\\test\\Il commence à être '
 'fatigué de ce problème impossible à analyser. Je commence à être fatigué de '
 'ce problème impossible à analyser\\Les imaginaires effondristes sont les '
 'seuls qui tiennent la route - Arthur Keller.temp.mp3: No such file or '
 'directory.',
 '',
 'retry downloading the playlist later to download the failed audio only ...',
 '',
 '"Il commence à être fatigué de ce problème impossible à analyser. Je '
 'commence à être fatigué de ce problème impossible à analyser" playlist '
 'audio(s) download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Les imaginaires effondristes sont les seuls qui tiennent la route - Arthur '
		                         'Keller.mp3']), sorted(fileNameLst))

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
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess = YoutubeDlAudioDownloader(audioController, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://youtube.com/playlist?list=PLzwWSJNcZTMQRlpXCFMkrgSnJXNRNAgn8"
		
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
			                  'video download complete.',
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
		longPlaylistNameMinusOneChar = 'Gcommence à être fatigué de ce problème impossible à analyser. Je commence à être fatigué de ce problème impossible à analyser'
		longPlaylistNameMinusOneCharWindowsAcceptable = 'Gcommence à être fatigué de ce problème impossible à analyser. Je commence à être fatigué de ce problème impossible à analyser'
		downloadDir = DirUtil.getTestAudioRootPath() + sep + DirUtil.replaceUnauthorizedDirOrFileNameChars(longPlaylistNameMinusOneCharWindowsAcceptable)
		
		# deleting downloadDir (dir and content)
		if os.path.exists(downloadDir):
			shutil.rmtree(downloadDir)
		
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess = YoutubeDlAudioDownloader(audioController, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMSkA0--6AhpekQXmAZXbAmz"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)

		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			playlistUrl=playlistUrl,
			audioRootDir=youtubeAccess.audioDirRoot,
			playlistDownloadRootPath=youtubeAccess.audioDirRoot,
			originalPlaylistTitle=playlistTitle)

		youtubeAccess.downloadPlaylistVideosForUrl(playlistUrl=playlistUrl,
		                                           downloadVideoInfoDic=downloadVideoInfoDic,
		                                           isUploadDateSuffixAddedToPlaylistVideo=False,
		                                           isDownloadDatePrefixAddedToPlaylistVideo=False)
		
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
 'test\\Gcommence à être fatigué de ce problème impossible à analyser. Je '
 'commence à être fatigué de ce problème impossible à analyser',
 'was created.',
 '',
 'downloading "Les imaginaires effondristes sont les seuls qui tiennent la '
 'route - Arthur Keller" audio ...',
 '',
 'video download complete.',
 '',
 '"Gcommence à être fatigué de ce problème impossible à analyser. Je commence '
 'à être fatigué de ce problème impossible à analyser" playlist audio(s) '
 'download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Gcommence à être fatigué de ce problème impossible à analyser. Je commence à '
 'être fatigué de ce problème impossible à analyser_dic.txt',
 'Les imaginaires effondristes sont les seuls qui tiennent la route - Arthur '
 'Keller.mp3']), sorted(fileNameLst))

		self.assertEqual(longPlaylistNameMinusOneChar, downloadVideoInfoDic.getPlaylistNameOriginal())

	def testDownloaTooLongNamePlaylist_127_char_oneShortVideo_targetFolder_not_exist(self):
		playlistName = '127 char_____playlist name is very long and will cause a problem if the target dir name exceeds a maximum possible too big name.'
		downloadDir = DirUtil.getTestAudioRootPath() + sep + DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistName)
		
		# deleting downloadDir (dir and content)
		if os.path.exists(downloadDir):
			shutil.rmtree(downloadDir)
		
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess = YoutubeDlAudioDownloader(audioController, DirUtil.getTestAudioRootPath())
		playlistUrl = 'https://youtube.com/playlist?list=PLzwWSJNcZTMQou0yHh8npCY2_ls8dwgVn'
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
 'file:D:/Users/Jean-Pierre/Downloads/Audio/test/127 char_____playlist '
 'name is very long and will cause a problem if the target dir name exceeds a '
 'maximum possible too big name/Les imaginaires effondristes sont les seuls '
 'qui tiennent la route - Arthur Keller.temp.mp3: No such file or directory. '
 'Playlist target dir "D:/Users/Jean-Pierre/Downloads/Audio/test/127 '
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
 'the target dir name exceeds a maximum possible too big name.',
 'was created.',
 '',
 'downloading "Les imaginaires effondristes sont les seuls qui tiennent la '
 'route - Arthur Keller" audio ...',
 '',
 'downloading video "Les imaginaires effondristes sont les seuls qui tiennent '
 'la route - Arthur Keller" caused this DownloadError exception: ERROR: '
 'file:D:\\Users\\Jean-Pierre\\Downloads\\Audio\\test\\127 char_____playlist '
 'name is very long and will cause a problem if the target dir name exceeds a '
 'maximum possible too big name#\\Les imaginaires effondristes sont les seuls '
 'qui tiennent la route - Arthur Keller.temp.mp3: No such file or directory.',
 '',
 'retry downloading the playlist later to download the failed audio only ...',
 '',
 '"127 char_____playlist name is very long and will cause a problem if the '
 'target dir name exceeds a maximum possible too big name." playlist audio(s) '
 'download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted([]), sorted(fileNameLst))
	
	def testDownloadPlaylistWithName_two_points(self):
		playlistName = "test short_n\'ame pl, aylist: avec deux points"
		playlistDirName = "test short_n'ame pl, aylist - avec deux points"
		downloadDir = DirUtil.getTestAudioRootPath() + sep + playlistDirName
		
		# deleting downloadDir (dir and content)
		if os.path.exists(downloadDir):
			shutil.rmtree(downloadDir)
		
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess = YoutubeDlAudioDownloader(audioController, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://youtube.com/playlist?list=PLzwWSJNcZTMSg3vAMZWqdGiEPQEuZi2Zh"
		
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
 "test\\test short_n'ame pl, aylist - avec deux points",
 'was created.',
 '',
 'downloading "Les imaginaires effondristes sont les seuls qui tiennent la '
 'route - Arthur Keller" audio ...',
 '',
 'video download complete.',
 '',
 '"test short_n\'ame pl, aylist: avec deux points" playlist audio(s) download '
 'terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*')]
		self.assertEqual(sorted(['Les imaginaires effondristes sont les seuls qui tiennent la route - Arthur '
 'Keller.mp3',
 "test short_n'ame pl, aylist - avec deux points_dic.txt"]), sorted(fileNameLst))

		self.assertEqual(playlistName, downloadVideoInfoDic.getPlaylistNameOriginal())

	def testRedownloading_the_playlist_with_deleted_audio_files(self):
		playlistName = 'test_audio_downloader_two_files'
		subTestDirName = '3'
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
			youtubeAccess.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)

		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			playlistUrl, youtubeAccess.audioDirRoot, youtubeAccess.audioDirRoot, playlistTitle)

		youtubeAccess.downloadPlaylistVideosForUrl(playlistUrl=playlistUrl,
		                                           downloadVideoInfoDic=downloadVideoInfoDic,
		                                           isUploadDateSuffixAddedToPlaylistVideo=False,
		                                           isDownloadDatePrefixAddedToPlaylistVideo=False)

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
		                 downloadVideoInfoDic.getVideoAudioFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3',
		                 downloadVideoInfoDic.getVideoAudioFileNameForVideoTitle(
			                 'Wear a mask. Help slow the spread of Covid-19.'))
		
		self.assertEqual('Here to help: Give him what he wants',
		                 downloadVideoInfoDic.getVideoTitleForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                 downloadVideoInfoDic.getVideoUrlForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                 downloadVideoInfoDic.getVideoUrlForVideoTitle('Here to help: Give him what he wants'))
		self.assertEqual('Here to help - Give him what he wants.mp3',
		                 downloadVideoInfoDic.getVideoAudioFileNameForVideoIndex(2))
		self.assertEqual('Here to help - Give him what he wants.mp3',
		                 downloadVideoInfoDic.getVideoAudioFileNameForVideoTitle(
			                 'Here to help: Give him what he wants'))
		
		self.assertEqual(['1', '2'], downloadVideoInfoDic.getVideoIndexStrings())
		
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

		targetAudioDir = redownloadVideoInfoDic.getPlaylistDownloadDir()
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(['"Wear a mask. Help slow the spread of Covid-19..mp3" audio already '
 'downloaded in "3\\test_audio_downloader_two_files" dir. Video skipped.',
 '',
 '"Here to help - Give him what he wants.mp3" audio already downloaded in '
 '"3\\test_audio_downloader_two_files" dir but was deleted. Video skipped.',
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
		                 redownloadVideoInfoDic.getVideoAudioFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3',
		                 redownloadVideoInfoDic.getVideoAudioFileNameForVideoTitle(
			                 'Wear a mask. Help slow the spread of Covid-19.'))
		
		self.assertEqual('Here to help: Give him what he wants',
		                 redownloadVideoInfoDic.getVideoTitleForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                 redownloadVideoInfoDic.getVideoUrlForVideoIndex(2))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                 redownloadVideoInfoDic.getVideoUrlForVideoTitle('Here to help: Give him what he wants'))
		self.assertEqual('Here to help - Give him what he wants.mp3',
		                 redownloadVideoInfoDic.getVideoAudioFileNameForVideoIndex(2))
		self.assertEqual('Here to help - Give him what he wants.mp3',
		                 redownloadVideoInfoDic.getVideoAudioFileNameForVideoTitle(
			                 'Here to help: Give him what he wants'))
		
		self.assertEqual(['1', '2'], redownloadVideoInfoDic.getVideoIndexStrings())
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Wear a mask. Help slow the spread of Covid-19..mp3',
 'test_audio_downloader_two_files_dic.txt']), sorted(fileNameLst))

	def testDownloadPlaylistVideosForUrl_renamedFile_already_exist(self):
		playlistName = 'test_audio_downloader_two_files'
		subTestDirName = '4'
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

		renamedFileName = 'Wear a mask. Help slow the spread of Covid-19. 20-07-31.mp3'
		
		renamedFilePathName = downloadDir + sep + renamedFileName
		
		with open(renamedFilePathName, 'w') as f:
			f.write('Hello World')
		
		self.assertTrue(os.path.isfile(renamedFilePathName))
		
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
			youtubeAccess.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)
		
		downloadVideoInfoDic, accessError = PlaylistTitleParser.createDownloadVideoInfoDicForPlaylist(
			playlistUrl=playlistUrl,
			audioRootDir=youtubeAccess.audioDirRoot,
			playlistDownloadRootPath=youtubeAccess.audioDirRoot,
			originalPlaylistTitle=playlistTitle)
		
		youtubeAccess.downloadPlaylistVideosForUrl(playlistUrl=playlistUrl,
		                                           downloadVideoInfoDic=downloadVideoInfoDic,
		                                           isUploadDateSuffixAddedToPlaylistVideo=True,
		                                           isDownloadDatePrefixAddedToPlaylistVideo=False)
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(
			['downloading "Wear a mask. Help slow the spread of Covid-19. 20-07-31.mp3" '
			 'audio ...',
			 '',
			 '[WinError 183] Impossible de créer un fichier déjà existant: '
			 "'D:\\\\Users\\\\Jean-Pierre\\\\Downloads\\\\Audio\\\\test\\\\4\\\\test_audio_downloader_two_files\\\\Wear "
			 "a mask. Help slow the spread of Covid-19..mp3' -> "
			 "'D:\\\\Users\\\\Jean-Pierre\\\\Downloads\\\\Audio\\\\test\\\\4\\\\test_audio_downloader_two_files\\\\Wear "
			 "a mask. Help slow the spread of Covid-19. 20-07-31.mp3'.",
			 '"Possible cause: a problem in '
			 'DirUtil.replaceUnauthorizedDirOrFileNameChars() method"',
			 '',
			 'downloading "Here to help - Give him what he wants 19-06-07.mp3" audio ...',
			 '',
			 'video download complete.',
			 '',
			 '"test_audio_downloader_two_files" playlist audio(s) download terminated.',
			 '',
			 ''], outputCapturingString.getvalue().split('\n'))
	
	def testDownloadPlaylistWithNameOneVideo_title_or_char(self):
		playlistDirName = "bugeco"
		playlistSaveDirName = "bugeco_save"
		downloadDir = DirUtil.getTestAudioRootPath() + sep + playlistDirName
		savedDownloadDir = DirUtil.getTestAudioRootPath() + sep + playlistSaveDirName

		# deleting downloadDir (dir and content)
		if os.path.exists(downloadDir):
			shutil.rmtree(downloadDir)

		# restoring download dir with almost fully downloaded video
		shutil.copytree(savedDownloadDir, downloadDir)
		
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		youtubeAccess = YoutubeDlAudioDownloader(audioController, DirUtil.getTestAudioRootPath())
		playlistUrl = "https://youtube.com/playlist?list=PLzwWSJNcZTMQnJYXjC9vDnWwG2pT9YNVV"
		
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
			self.assertEqual(['downloading "💥 EFFONDREMENT Imminent de l\'Euro ?! | 👉 Maintenant, La Fin de '
 'l\'Euro Approche ?!" audio ...',
 '',
 'video download complete.',
 '',
 '"bugeco" playlist audio(s) download terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*')]
		self.assertEqual(sorted(['bugeco_dic.txt',
 "💥 EFFONDREMENT Imminent de l'Euro ! _ 👉 Maintenant, La Fin de l'Euro "
 'Approche !.mp3']), sorted(fileNameLst))

		dicFileName = playlistDirName + DownloadPlaylistInfoDic.DIC_FILE_NAME_EXTENT
		dicFilePathName = downloadDir + sep + dicFileName

		dvi = DownloadPlaylistInfoDic(playlistUrl=None,
		                              audioRootDir=None,
		                              playlistDownloadRootPath=None,
		                              originalPaylistTitle=None,
		                              originalPlaylistName=None,
		                              modifiedPlaylistTitle=None,
		                              modifiedPlaylistName=None,
		                              loadDicIfDicFileExist=True,
		                              existingDicFilePathName=dicFilePathName)

		self.assertEqual("\ud83d\udca5 EFFONDREMEN Imminent de l'Euro ! _ \ud83d\udc49 Maintenant, La Fin de l'Euro Approche !.mp3",
		                 dvi.getVideoAudioFileNameForVideoIndex(1))

if __name__ == '__main__':
#	unittest.main()
	tst = TestYoutubeDlAudioDownloaderDownloadMethods()

	tst.testDownloadPlaylistWithNameOneVideo_title_or_char()
