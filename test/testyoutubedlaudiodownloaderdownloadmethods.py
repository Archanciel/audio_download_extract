import unittest
import os, sys, inspect, shutil, glob
from io import StringIO

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from constants import *
from guioutputstub import GuiOutputStub
from youtubedlaudiodownloader import YoutubeDlAudioDownloader

class TestYoutubeDlAudioDownloaderDownloadMethods(unittest.TestCase):
	"""
	Since testing download consume band width, it is placed in a specific test class.
	"""

	def testDownloadVideoReferencedInPlaylist_targetFolder_exist(self):
		playlistName = 'test_audio_downloader_one_file'
		downloadDir = AUDIO_DIR + DIR_SEP + playlistName

		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)

		# deleting files in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)
			
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		_, downloadVideoInfoDic, _, accessError = youtubeAccess.getDownloadVideoInfoDicForUrl(playlistUrl)
		downloadVideoInfoDic, accessError = youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)
		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()

		sys.stdout = stdout

		self.assertIsNone(accessError)
		self.assertEqual(['downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
 '',
 '"Wear a mask. Help slow the spread of Covid-19." audio downloaded.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))

		self.assertEqual(downloadDir, targetAudioDir)
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
			self.assertEqual('D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks\\test_audio_downloader_one_file', downloadDir)

		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Wear a mask. Help slow the spread of Covid-19..mp3',
								 'test_audio_downloader_one_file_dic.txt']), sorted(fileNameLst))

	def testDownloadVideoReferencedInPlaylist_targetFolder_not_exist(self):
		playlistName = 'test_audio_downloader_one_file'
		downloadDir = AUDIO_DIR + DIR_SEP + playlistName

		# deleting downloadDir (dir and content)
		if os.path.exists(downloadDir):
			shutil.rmtree(downloadDir)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		_, downloadVideoInfoDic, _, accessError = youtubeAccess.getDownloadVideoInfoDicForUrl(playlistUrl)
		downloadVideoInfoDic, accessError = youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)

		sys.stdout = stdout

		if os.name == 'posix':
			self.assertEqual(['directory',
 'Audiobooks/test_audio_downloader_one_file',
 'was created.',
 'downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
 '',
 '"Wear a mask. Help slow the spread of Covid-19." audio downloaded.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual(['directory',
 'Audiobooks\\test_audio_downloader_one_file',
 'was created.',
 'downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
 '',
 '"Wear a mask. Help slow the spread of Covid-19." audio downloaded.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))

		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Wear a mask. Help slow the spread of Covid-19..mp3',
								 'test_audio_downloader_one_file_dic.txt']), sorted(fileNameLst))

	def testDownloadAudioFromPlaylistMultipleVideo(self):
		playlistName = 'test_audio_downloader_two_files'
		downloadDir = AUDIO_DIR + DIR_SEP + playlistName

		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting files in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRGA1T1vOn500RuLFo_lGJv"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		_, downloadVideoInfoDic, _, accessError = youtubeAccess.getDownloadVideoInfoDicForUrl(playlistUrl)
		downloadVideoInfoDic, accessError = youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)
		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()
		sys.stdout = stdout

		self.assertIsNone(accessError)
		self.assertEqual(['downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
 '',
 '"Wear a mask. Help slow the spread of Covid-19." audio downloaded.',
 '',
 'downloading "Here to help: Give him what he wants" audio ...',
 '',
 '"Here to help: Give him what he wants" audio downloaded.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))

		self.assertEqual(downloadDir, targetAudioDir)
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

		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Here to help - Give him what he wants.mp3',
								 'Wear a mask. Help slow the spread of Covid-19..mp3',
								 'test_audio_downloader_two_files_dic.txt']), sorted(fileNameLst))
	
	def testDownloadAudioFromPlaylistMultipleVideo_withTimeFrames(self):
		# playlist title: test_audio_downloader_two_files_with_time_frames (e0:0:2-0:0:8) (s0:0:2-0:0:5 s0:0:7-0:0:10)
		playlistName = 'test_audio_downloader_two_files_with_time_frames'
		downloadDir = AUDIO_DIR + DIR_SEP + playlistName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting files in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMSFWGrRGKOypqN29MlyuQvn"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		_, downloadVideoInfoDic, _, accessError = youtubeAccess.getDownloadVideoInfoDicForUrl(playlistUrl)
		downloadVideoInfoDic, accessError = youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)
		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()

		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(
			['downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
			 '',
			 '"Wear a mask. Help slow the spread of Covid-19." audio downloaded.',
			 '',
			 'downloading "Here to help: Give him what he wants" audio ...',
			 '',
			 '"Here to help: Give him what he wants" audio downloaded.',
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

		self.assertEqual(downloadDir, targetAudioDir)
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

		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(
			sorted(['Here to help - Give him what he wants.mp3',
					'Wear a mask. Help slow the spread of Covid-19..mp3',
					'test_audio_downloader_two_files_with_time_frames_dic.txt']), sorted(fileNameLst))
	
	def testDownloadVideoReferencedInPlaylist_invalid_url(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=invalid"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		_, downloadVideoInfoDic, _, accessError = youtubeAccess.getDownloadVideoInfoDicForUrl(playlistUrl)
		downloadVideoInfoDic, accessError = youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)
		
		sys.stdout = stdout
		
		self.assertEqual('the URL obtained from clipboard is not pointing to a playlist.\nwrong URL: https://www.youtube.com/playlist?list=invalid\nnothing to download.', accessError.errorMsg)
	
	def testDownloadVideoReferencedInPlaylist_empty_url(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput)
		playlistUrl = ""
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		_, downloadVideoInfoDic, _, accessError = youtubeAccess.getDownloadVideoInfoDicForUrl(playlistUrl)
		downloadVideoInfoDic, accessError = youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)
		
		sys.stdout = stdout
		
		self.assertEqual('the URL obtained from clipboard is empty.\nnothing to download.', accessError.errorMsg)
	
	def testDownloadVideoReferencedInPlaylist_with_timeFrame(self):
		playlistName = 'Test_title_one_time_frame_extract'
		downloadDir = AUDIO_DIR + DIR_SEP + playlistName
		# timeInfo = '(e0:0:5-0:0:10)'

		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting files in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMTB7GasAttwVnPPk3-WTMNJ"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		_, downloadVideoInfoDic, _, accessError = youtubeAccess.getDownloadVideoInfoDicForUrl(playlistUrl)
		downloadVideoInfoDic, accessError = youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)
		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()

		sys.stdout = stdout

		self.assertIsNone(accessError)
		self.assertEqual(['downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
 '',
 '"Wear a mask. Help slow the spread of Covid-19." audio downloaded.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))

		self.assertEqual([[5, 10]], downloadVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1))
		self.assertEqual(downloadDir, targetAudioDir)
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.', downloadVideoInfoDic.getVideoTitleForVideoIndex(1))
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk', downloadVideoInfoDic.getVideoUrlForVideoIndex(1))
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk', downloadVideoInfoDic.getVideoUrlForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3', downloadVideoInfoDic.getVideoFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19..mp3', downloadVideoInfoDic.getVideoFileNameForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))

		self.assertEqual(['1'], downloadVideoInfoDic.getVideoIndexes())

		if os.name == 'posix':
			self.assertEqual('/storage/emulated/0/Download/Audiobooks/' + playlistName,
			                 downloadDir)
		else:
			self.assertEqual('D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks\\' + playlistName,
			                 downloadDir)

		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Test_title_one_time_frame_extract_dic.txt',
								 'Wear a mask. Help slow the spread of Covid-19..mp3']), sorted(fileNameLst))
		self.assertEqual([[5, 10]], downloadVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(1))
	
	def testDownloadAudioFromPlaylistMultipleVideo_redownloading_the_playlist(self):
		playlistName = 'test_audio_downloader_two_files'
		downloadDir = AUDIO_DIR + DIR_SEP + playlistName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting files in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRGA1T1vOn500RuLFo_lGJv"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		_, downloadVideoInfoDic, _, accessError = youtubeAccess.getDownloadVideoInfoDicForUrl(playlistUrl)
		downloadVideoInfoDic, accessError = youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)
		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()

		sys.stdout = stdout

		self.assertIsNone(accessError)
		self.assertEqual(
			['downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
			 '',
			 '"Wear a mask. Help slow the spread of Covid-19." audio downloaded.',
			 '',
			 'downloading "Here to help: Give him what he wants" audio ...',
			 '',
			 '"Here to help: Give him what he wants" audio downloaded.',
			 '',
			 ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertEqual(downloadDir, targetAudioDir)
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
		
		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Here to help - Give him what he wants.mp3',
		                         'Wear a mask. Help slow the spread of Covid-19..mp3',
		                         'test_audio_downloader_two_files_dic.txt']), sorted(fileNameLst))

		# re-downloading the playlist
	
		youtubeAccess_redownload = YoutubeDlAudioDownloader(guiOutput)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		_, downloadVideoInfoDic, _, accessError = youtubeAccess.getDownloadVideoInfoDicForUrl(playlistUrl)
		redownloadVideoInfoDic, accessError = youtubeAccess_redownload.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)
		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()

		sys.stdout = stdout

		self.assertIsNone(accessError)
		self.assertEqual(['"Wear a mask. Help slow the spread of Covid-19." audio already downloaded. '
 'Video skipped.',
 '',
 '"Here to help: Give him what he wants" audio already downloaded. Video '
 'skipped.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertEqual(downloadDir, targetAudioDir)
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
		
		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Here to help - Give him what he wants.mp3',
		                         'Wear a mask. Help slow the spread of Covid-19..mp3',
		                         'test_audio_downloader_two_files_dic.txt']), sorted(fileNameLst))
	
	def testDownloadAudioFromPlaylistMultipleVideo_withTimeFrames_redownloading_the_playlist(self):
		# playlist title: test_audio_downloader_two_files_with_time_frames (e0:0:2-0:0:8) (s0:0:2-0:0:5 s0:0:7-0:0:10)
		playlistName = 'test_audio_downloader_two_files_with_time_frames'
		downloadDir = AUDIO_DIR + DIR_SEP + playlistName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting files in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMSFWGrRGKOypqN29MlyuQvn"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		_, downloadVideoInfoDic, _, accessError = youtubeAccess.getDownloadVideoInfoDicForUrl(playlistUrl)
		downloadVideoInfoDic, accessError = youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, downloadVideoInfoDic)
		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()

		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(
			['downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
			 '',
			 '"Wear a mask. Help slow the spread of Covid-19." audio downloaded.',
			 '',
			 'downloading "Here to help: Give him what he wants" audio ...',
			 '',
			 '"Here to help: Give him what he wants" audio downloaded.',
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
		
		self.assertEqual(downloadDir, targetAudioDir)
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
		
		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(
			sorted(['Here to help - Give him what he wants.mp3',
			        'Wear a mask. Help slow the spread of Covid-19..mp3',
			        'test_audio_downloader_two_files_with_time_frames_dic.txt']), sorted(fileNameLst))

		# re-downloading the playlist
		
		youtubeAccess_redownload = YoutubeDlAudioDownloader(guiOutput)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		_, redownloadVideoInfoDic, _, accessError = youtubeAccess.getDownloadVideoInfoDicForUrl(playlistUrl)
		redownloadVideoInfoDic, accessError = youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl, redownloadVideoInfoDic)
		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()

		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(['"Wear a mask. Help slow the spread of Covid-19." audio already downloaded. '
 'Video skipped.',
 '',
 '"Here to help: Give him what he wants" audio already downloaded. Video '
 'skipped.',
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
		
		self.assertEqual(downloadDir, targetAudioDir)
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
		
		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(
			sorted(['Here to help - Give him what he wants.mp3',
			        'Wear a mask. Help slow the spread of Covid-19..mp3',
			        'test_audio_downloader_two_files_with_time_frames_dic.txt']), sorted(fileNameLst))

	def testDownloadAudioFromPlaylistMultipleVideo_withTimeFrames_redownloading_the_playlist_after_adding_a_new_video(self):
		# re-downloading playlist with clearing all files but one in the destination dir
		# playlist title: test_audio_downloader_two_files_with_time_frames (e0:0:2-0:0:8) (s0:0:2-0:0:5 s0:0:7-0:0:10)
		playlistName = 'Test 3 short videos'
		downloadDir = AUDIO_DIR + DIR_SEP + playlistName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting files in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput)
		playlistUrl = 'https://www.youtube.com/playlist?list=PLzwWSJNcZTMShenMgwyjHC8o5bU8QUPbn'
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		_, downloadVideoInfoDic, _, accessError = youtubeAccess.getDownloadVideoInfoDicForUrl(playlistUrl)
		downloadVideoInfoDic, accessError = youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(playlistUrl,
		                                                                                                   downloadVideoInfoDic)
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(
			['downloading "Wear a mask. Help slow the spread of Covid-19." audio ...',
			 '',
			 '"Wear a mask. Help slow the spread of Covid-19." audio downloaded.',
			 '',
			 'downloading "Here to help: Give him what he wants" audio ...',
			 '',
			 '"Here to help: Give him what he wants" audio downloaded.',
			 '',
			 'downloading "Funny suspicious looking dog" audio ...',
			 '',
			 '"Funny suspicious looking dog" audio downloaded.',
			 '',
			 ''], outputCapturingString.getvalue().split('\n'))
		
		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(
			sorted(['Funny suspicious looking dog.mp3',
 'Here to help - Give him what he wants.mp3',
 'Test 3 short videos_dic.txt',
 'Wear a mask. Help slow the spread of Covid-19..mp3']), sorted(fileNameLst))
		
		# re-downloading the playlist after suppressing the files and data for
		# the last video
		
		# the last video files in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*.mp3')
		
		for f in files:
			if 'Funny suspicious looking dog' in f:
				os.remove(f)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		_, redownloadVideoInfoDic, _, accessError = youtubeAccess.getDownloadVideoInfoDicForUrl(playlistUrl)
		redownloadVideoInfoDic.removeVideoInfoForVideoTitle('Funny suspicious looking dog')
		
		redownloadVideoInfoDic, accessError = youtubeAccess.downloadVideosReferencedInPlaylistForPlaylistUrl(
			playlistUrl, redownloadVideoInfoDic)
		targetAudioDir = downloadVideoInfoDic.getPlaylistDownloadDir()
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertEqual(['"Wear a mask. Help slow the spread of Covid-19." audio already downloaded. '
 'Video skipped.',
 '',
 '"Here to help: Give him what he wants" audio already downloaded. Video '
 'skipped.',
 '',
 'downloading "Funny suspicious looking dog" audio ...',
 '',
 '"Funny suspicious looking dog" audio downloaded.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertEqual(downloadDir, targetAudioDir)
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
		                 redownloadVideoInfoDic.getVideoTitleForVideoIndex(3))
		self.assertEqual('https://www.youtube.com/watch?v=vU1NEZ9sTOM',
		                 redownloadVideoInfoDic.getVideoUrlForVideoIndex(3))
		self.assertEqual('https://www.youtube.com/watch?v=vU1NEZ9sTOM',
		                 redownloadVideoInfoDic.getVideoUrlForVideoTitle('Funny suspicious looking dog'))
		self.assertEqual('Funny suspicious looking dog.mp3',
		                 redownloadVideoInfoDic.getVideoFileNameForVideoIndex(3))
		self.assertEqual('Funny suspicious looking dog.mp3',
		                 redownloadVideoInfoDic.getVideoFileNameForVideoTitle(
			                 'Funny suspicious looking dog'))
		
		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(
			sorted(['Funny suspicious looking dog.mp3',
 'Here to help - Give him what he wants.mp3',
 'Test 3 short videos_dic.txt',
 'Wear a mask. Help slow the spread of Covid-19..mp3']), sorted(fileNameLst))


if __name__ == '__main__':
#	unittest.main()
	tst = TestYoutubeDlAudioDownloaderDownloadMethods()
	tst.testDownloadAudioFromPlaylistMultipleVideo_withTimeFrames_redownloading_the_playlist_after_adding_a_new_video()
