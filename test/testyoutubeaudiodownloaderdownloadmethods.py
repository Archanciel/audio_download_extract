import unittest
import os, sys, inspect, shutil, glob
from io import StringIO

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from constants import *
from guioutputstub import GuiOutputStub
from youtubeaudiodownloader import YoutubeAudioDownloader

class TestYoutubeAudioDownloaderDownloadMethods(unittest.TestCase):
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
		youtubeAccess = YoutubeAudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		targetAudioDir, downloadedVideoInfoDictionary = youtubeAccess.downloadVideosReferencedInPlaylist(playlistUrl)

		sys.stdout = stdout

		self.assertEqual(['downloading Wear a mask. Help slow the spread of Covid-19.',
						 '',
						 'downloading Wear a mask. Help slow the spread of Covid-19.',
						 'Wear a mask. Help slow the spread of Covid-19. downloaded.',
						 '',
						 ''], outputCapturingString.getvalue().split('\n'))

		self.assertEqual(downloadDir, targetAudioDir)
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.', downloadedVideoInfoDictionary.getVideoTitleForVideoIndex(1))
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', downloadedVideoInfoDictionary.getVideoUrlForVideoIndex(1))
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', downloadedVideoInfoDictionary.getVideoUrlForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))
		self.assertEqual('Wear a mask Help slow the spread of Covid-19.mp4', downloadedVideoInfoDictionary.getVideoFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask Help slow the spread of Covid-19.mp4', downloadedVideoInfoDictionary.getVideoFileNameForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))
		self.assertEqual(['1'], downloadedVideoInfoDictionary.getVideoIndexes())

		if os.name == 'posix':
			self.assertEqual('/storage/emulated/0/Download/Audiobooks/test_audio_downloader_one_file',
			                 downloadDir)
		else:
			self.assertEqual('D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks\\test_audio_downloader_one_file', downloadDir)

		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Wear a mask Help slow the spread of Covid-19.mp4',
								 'test_audio_downloader_one_file_dic.txt']), sorted(fileNameLst))

	def testDownloadVideoReferencedInPlaylist_targetFolder_not_exist(self):
		playlistName = 'test_audio_downloader_one_file'
		downloadDir = AUDIO_DIR + DIR_SEP + playlistName

		# deleting downloadDir (dir and content)
		if os.path.exists(downloadDir):
			shutil.rmtree(downloadDir)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		youtubeAccess.downloadVideosReferencedInPlaylist(playlistUrl)

		sys.stdout = stdout

		if os.name == 'posix':
			self.assertEqual(['Directory',
							  'Audiobooks/test_audio_downloader_one_file',
							  'will be created.',
							  '',
							  'Continue with download ?',
							  'downloading Wear a mask. Help slow the spread of Covid-19.',
			                  '',
							  'downloading Wear a mask. Help slow the spread of Covid-19.',
							  'Wear a mask. Help slow the spread of Covid-19. downloaded.',
							  '',
							  ''], outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual(['Directory',
							  'Audiobooks\\test_audio_downloader_one_file',
							  'will be created.',
							  '',
							  'Continue with download ?',
							  'downloading Wear a mask. Help slow the spread of Covid-19.',
			                  '',
							  'downloading Wear a mask. Help slow the spread of Covid-19.',
							  'Wear a mask. Help slow the spread of Covid-19. downloaded.',
							  '',
							  ''], outputCapturingString.getvalue().split('\n'))

		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Wear a mask Help slow the spread of Covid-19.mp4',
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
		youtubeAccess = YoutubeAudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRGA1T1vOn500RuLFo_lGJv"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		targetAudioDir, downloadedVideoInfoDictionary = youtubeAccess.downloadVideosReferencedInPlaylist(playlistUrl)

		sys.stdout = stdout

		self.assertEqual(['downloading Wear a mask. Help slow the spread of Covid-19.',
						 '',
						 'downloading Wear a mask. Help slow the spread of Covid-19.',
						 'Wear a mask. Help slow the spread of Covid-19. downloaded.',
						 '',
						 'downloading Wear a mask. Help slow the spread of Covid-19.',
						 'Wear a mask. Help slow the spread of Covid-19. downloaded.',
						 'downloading Here to help: Give him what he wants',
						 '',
						 'downloading Wear a mask. Help slow the spread of Covid-19.',
						 'Wear a mask. Help slow the spread of Covid-19. downloaded.',
						 'downloading Here to help: Give him what he wants',
						 'Here to help: Give him what he wants downloaded.',
						 '',
						 ''], outputCapturingString.getvalue().split('\n'))

		self.assertEqual(downloadDir, targetAudioDir)
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.', downloadedVideoInfoDictionary.getVideoTitleForVideoIndex(1))
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', downloadedVideoInfoDictionary.getVideoUrlForVideoIndex(1))
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', downloadedVideoInfoDictionary.getVideoUrlForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))
		self.assertEqual('Wear a mask Help slow the spread of Covid-19.mp4', downloadedVideoInfoDictionary.getVideoFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask Help slow the spread of Covid-19.mp4', downloadedVideoInfoDictionary.getVideoFileNameForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))

		self.assertEqual('Here to help: Give him what he wants', downloadedVideoInfoDictionary.getVideoTitleForVideoIndex(2))
		self.assertEqual('https://youtube.com/watch?v=Eqy6M6qLWGw', downloadedVideoInfoDictionary.getVideoUrlForVideoIndex(2))
		self.assertEqual('https://youtube.com/watch?v=Eqy6M6qLWGw', downloadedVideoInfoDictionary.getVideoUrlForVideoTitle('Here to help: Give him what he wants'))
		self.assertEqual('Here to help Give him what he wants.mp4', downloadedVideoInfoDictionary.getVideoFileNameForVideoIndex(2))
		self.assertEqual('Here to help Give him what he wants.mp4', downloadedVideoInfoDictionary.getVideoFileNameForVideoTitle('Here to help: Give him what he wants'))

		self.assertEqual(['1', '2'], downloadedVideoInfoDictionary.getVideoIndexes())

		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Here to help Give him what he wants.mp4',
								 'Wear a mask Help slow the spread of Covid-19.mp4',
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
		youtubeAccess = YoutubeAudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMSFWGrRGKOypqN29MlyuQvn"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		targetAudioDir, downloadedVideoInfoDictionary = youtubeAccess.downloadVideosReferencedInPlaylist(
			playlistUrl)
		
		sys.stdout = stdout
		
		self.assertEqual(['downloading Wear a mask. Help slow the spread of Covid-19.',
		                  '',
		                  'downloading Wear a mask. Help slow the spread of Covid-19.',
		                  'Wear a mask. Help slow the spread of Covid-19. downloaded.',
		                  '',
		                  'downloading Wear a mask. Help slow the spread of Covid-19.',
		                  'Wear a mask. Help slow the spread of Covid-19. downloaded.',
		                  'downloading Here to help: Give him what he wants',
		                  '',
		                  'downloading Wear a mask. Help slow the spread of Covid-19.',
		                  'Wear a mask. Help slow the spread of Covid-19. downloaded.',
		                  'downloading Here to help: Give him what he wants',
		                  'Here to help: Give him what he wants downloaded.',
		                  '',
		                  ''], outputCapturingString.getvalue().split('\n'))
		
		# playlist title: test_audio_downloader_two_files_with_time_frames
		# (e0:0:2-0:0:8) (s0:0:2-0:0:5 s0:0:7-0:0:10)
		startEndSecondsList_extract_firstVideo_firstTimeFrame = [2, 8]

		startEndSecondsList_suppress_secondVideo_firstTimeFrame = [2, 5]
		startEndSecondsList_suppress_secondVideo_secondTimeFrame = [7, 10]
		
		self.assertEqual([startEndSecondsList_extract_firstVideo_firstTimeFrame],
		                 downloadedVideoInfoDictionary.getExtractStartEndSecondsListsForVideoIndex(1))
		self.assertEqual([],
		                 downloadedVideoInfoDictionary.getSuppressStartEndSecondsListsForVideoIndex(1))
		
		self.assertEqual([],
		                 downloadedVideoInfoDictionary.getExtractStartEndSecondsListsForVideoIndex(2))
		self.assertEqual([startEndSecondsList_suppress_secondVideo_firstTimeFrame,
		                  startEndSecondsList_suppress_secondVideo_secondTimeFrame],
		                 downloadedVideoInfoDictionary.getSuppressStartEndSecondsListsForVideoIndex(2))

		self.assertEqual(downloadDir, targetAudioDir)
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.', downloadedVideoInfoDictionary.getVideoTitleForVideoIndex(1))
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', downloadedVideoInfoDictionary.getVideoUrlForVideoIndex(1))
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', downloadedVideoInfoDictionary.getVideoUrlForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))
		self.assertEqual('Wear a mask Help slow the spread of Covid-19.mp4', downloadedVideoInfoDictionary.getVideoFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask Help slow the spread of Covid-19.mp4', downloadedVideoInfoDictionary.getVideoFileNameForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))

		self.assertEqual('Here to help: Give him what he wants', downloadedVideoInfoDictionary.getVideoTitleForVideoIndex(2))
		self.assertEqual('https://youtube.com/watch?v=Eqy6M6qLWGw', downloadedVideoInfoDictionary.getVideoUrlForVideoIndex(2))
		self.assertEqual('https://youtube.com/watch?v=Eqy6M6qLWGw', downloadedVideoInfoDictionary.getVideoUrlForVideoTitle('Here to help: Give him what he wants'))
		self.assertEqual('Here to help Give him what he wants.mp4', downloadedVideoInfoDictionary.getVideoFileNameForVideoIndex(2))
		self.assertEqual('Here to help Give him what he wants.mp4', downloadedVideoInfoDictionary.getVideoFileNameForVideoTitle('Here to help: Give him what he wants'))

		self.assertEqual(['1', '2'], downloadedVideoInfoDictionary.getVideoIndexes())

		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(
			sorted(['Here to help Give him what he wants.mp4',
					'Wear a mask Help slow the spread of Covid-19.mp4',
					'test_audio_downloader_two_files_with_time_frames_dic.txt']), sorted(fileNameLst))
	
	def testDownloadVideoReferencedInPlaylist_invalid_url(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=invalid"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		youtubeAccess.downloadVideosReferencedInPlaylist(playlistUrl)
		
		sys.stdout = stdout
		
		self.assertEqual(['The URL obtained from clipboard is not pointing to a playlist.',
						 'Wrong URL: https://www.youtube.com/playlist?list=invalid',
						 'Program will be closed.',
						 ''], outputCapturingString.getvalue().split('\n'))
	
	def testDownloadVideoReferencedInPlaylist_empty_url(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAudioDownloader(guiOutput)
		playlistUrl = ""
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		youtubeAccess.downloadVideosReferencedInPlaylist(playlistUrl)
		
		sys.stdout = stdout
		
		self.assertEqual('The URL obtained from clipboard is empty.\nProgram will be closed.\n', outputCapturingString.getvalue())
	
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
		youtubeAccess = YoutubeAudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMTB7GasAttwVnPPk3-WTMNJ"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		targetAudioDir, downloadedVideoInfoDictionary = youtubeAccess.downloadVideosReferencedInPlaylist(playlistUrl)
		
		sys.stdout = stdout

		self.assertEqual(['downloading Wear a mask. Help slow the spread of Covid-19.',
						 '',
						 'downloading Wear a mask. Help slow the spread of Covid-19.',
						 'Wear a mask. Help slow the spread of Covid-19. downloaded.',
						 '',
						 ''], outputCapturingString.getvalue().split('\n'))

		self.assertEqual([[5, 10]], downloadedVideoInfoDictionary.getExtractStartEndSecondsListsForVideoIndex(1))
		self.assertEqual(downloadDir, targetAudioDir)
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.', downloadedVideoInfoDictionary.getVideoTitleForVideoIndex(1))
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', downloadedVideoInfoDictionary.getVideoUrlForVideoIndex(1))
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', downloadedVideoInfoDictionary.getVideoUrlForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))
		self.assertEqual('Wear a mask Help slow the spread of Covid-19.mp4', downloadedVideoInfoDictionary.getVideoFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask Help slow the spread of Covid-19.mp4', downloadedVideoInfoDictionary.getVideoFileNameForVideoTitle('Wear a mask. Help slow the spread of Covid-19.'))

		self.assertEqual(['1'], downloadedVideoInfoDictionary.getVideoIndexes())

		if os.name == 'posix':
			self.assertEqual('/storage/emulated/0/Download/Audiobooks/' + playlistName,
			                 downloadDir)
		else:
			self.assertEqual('D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks\\' + playlistName,
			                 downloadDir)

		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Test_title_one_time_frame_extract_dic.txt',
								 'Wear a mask Help slow the spread of Covid-19.mp4']), sorted(fileNameLst))
		self.assertEqual([[5, 10]], downloadedVideoInfoDictionary.getExtractStartEndSecondsListsForVideoIndex(1))
	
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
		youtubeAccess = YoutubeAudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRGA1T1vOn500RuLFo_lGJv"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		targetAudioDir, downloadedVideoInfoDictionary = youtubeAccess.downloadVideosReferencedInPlaylist(playlistUrl)
		
		sys.stdout = stdout
		
		self.assertEqual(['downloading Wear a mask. Help slow the spread of Covid-19.',
		                  '',
		                  'downloading Wear a mask. Help slow the spread of Covid-19.',
		                  'Wear a mask. Help slow the spread of Covid-19. downloaded.',
		                  '',
		                  'downloading Wear a mask. Help slow the spread of Covid-19.',
		                  'Wear a mask. Help slow the spread of Covid-19. downloaded.',
		                  'downloading Here to help: Give him what he wants',
		                  '',
		                  'downloading Wear a mask. Help slow the spread of Covid-19.',
		                  'Wear a mask. Help slow the spread of Covid-19. downloaded.',
		                  'downloading Here to help: Give him what he wants',
		                  'Here to help: Give him what he wants downloaded.',
		                  '',
		                  ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertEqual(downloadDir, targetAudioDir)
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.',
		                 downloadedVideoInfoDictionary.getVideoTitleForVideoIndex(1))
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk',
		                 downloadedVideoInfoDictionary.getVideoUrlForVideoIndex(1))
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk',
		                 downloadedVideoInfoDictionary.getVideoUrlForVideoTitle(
			                 'Wear a mask. Help slow the spread of Covid-19.'))
		self.assertEqual('Wear a mask Help slow the spread of Covid-19.mp4',
		                 downloadedVideoInfoDictionary.getVideoFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask Help slow the spread of Covid-19.mp4',
		                 downloadedVideoInfoDictionary.getVideoFileNameForVideoTitle(
			                 'Wear a mask. Help slow the spread of Covid-19.'))
		
		self.assertEqual('Here to help: Give him what he wants',
		                 downloadedVideoInfoDictionary.getVideoTitleForVideoIndex(2))
		self.assertEqual('https://youtube.com/watch?v=Eqy6M6qLWGw',
		                 downloadedVideoInfoDictionary.getVideoUrlForVideoIndex(2))
		self.assertEqual('https://youtube.com/watch?v=Eqy6M6qLWGw',
		                 downloadedVideoInfoDictionary.getVideoUrlForVideoTitle('Here to help: Give him what he wants'))
		self.assertEqual('Here to help Give him what he wants.mp4',
		                 downloadedVideoInfoDictionary.getVideoFileNameForVideoIndex(2))
		self.assertEqual('Here to help Give him what he wants.mp4',
		                 downloadedVideoInfoDictionary.getVideoFileNameForVideoTitle(
			                 'Here to help: Give him what he wants'))
		
		self.assertEqual(['1', '2'], downloadedVideoInfoDictionary.getVideoIndexes())
		
		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Here to help Give him what he wants.mp4',
		                         'Wear a mask Help slow the spread of Covid-19.mp4',
		                         'test_audio_downloader_two_files_dic.txt']), sorted(fileNameLst))

		# redownloading the playlist
	
		youtubeAccess_redownload = YoutubeAudioDownloader(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRGA1T1vOn500RuLFo_lGJv"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		targetAudioDir, redownloadedVideoInfoDictionary = youtubeAccess_redownload.downloadVideosReferencedInPlaylist(playlistUrl)
		
		sys.stdout = stdout

		self.assertEqual(['Wear a mask. Help slow the spread of Covid-19. already downloaded. Video skipped.',
						 '',
						 'Wear a mask. Help slow the spread of Covid-19. already downloaded. Video skipped.',
						 'Here to help: Give him what he wants already downloaded. Video skipped.',
						 '',
						 ''], outputCapturingString.getvalue().split('\n'))
		
		self.assertEqual(downloadDir, targetAudioDir)
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.',
		                 redownloadedVideoInfoDictionary.getVideoTitleForVideoIndex(1))
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk',
		                 redownloadedVideoInfoDictionary.getVideoUrlForVideoIndex(1))
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk',
		                 redownloadedVideoInfoDictionary.getVideoUrlForVideoTitle(
			                 'Wear a mask. Help slow the spread of Covid-19.'))
		self.assertEqual('Wear a mask Help slow the spread of Covid-19.mp4',
		                 redownloadedVideoInfoDictionary.getVideoFileNameForVideoIndex(1))
		self.assertEqual('Wear a mask Help slow the spread of Covid-19.mp4',
		                 redownloadedVideoInfoDictionary.getVideoFileNameForVideoTitle(
			                 'Wear a mask. Help slow the spread of Covid-19.'))
		
		self.assertEqual('Here to help: Give him what he wants',
		                 redownloadedVideoInfoDictionary.getVideoTitleForVideoIndex(2))
		self.assertEqual('https://youtube.com/watch?v=Eqy6M6qLWGw',
		                 redownloadedVideoInfoDictionary.getVideoUrlForVideoIndex(2))
		self.assertEqual('https://youtube.com/watch?v=Eqy6M6qLWGw',
		                 redownloadedVideoInfoDictionary.getVideoUrlForVideoTitle('Here to help: Give him what he wants'))
		self.assertEqual('Here to help Give him what he wants.mp4',
		                 redownloadedVideoInfoDictionary.getVideoFileNameForVideoIndex(2))
		self.assertEqual('Here to help Give him what he wants.mp4',
		                 redownloadedVideoInfoDictionary.getVideoFileNameForVideoTitle(
			                 'Here to help: Give him what he wants'))
		
		self.assertEqual(['1', '2'], redownloadedVideoInfoDictionary.getVideoIndexes())
		
		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Here to help Give him what he wants.mp4',
		                         'Wear a mask Help slow the spread of Covid-19.mp4',
		                         'test_audio_downloader_two_files_dic.txt']), sorted(fileNameLst))


if __name__ == '__main__':
#	unittest.main()
	tst = TestYoutubeAudioDownloaderDownloadMethods()
	tst.testDownloadAudioFromPlaylistMultipleVideo_redownloading_the_playlist()
