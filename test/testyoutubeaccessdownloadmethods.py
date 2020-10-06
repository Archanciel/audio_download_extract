import unittest
import os, sys, inspect, shutil, glob
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from constants import *
from guioutputstub import GuiOutputStub
from youtubeaccess import YoutubeAccess
			
class TestYoutubeAccessDownloadMethods(unittest.TestCase):
	'''
	Since testing download consume band width, it is placed in a specific test class.
	'''

	def testDownloadAudioFromPlaylistOneVideo_targetFolder_exist(self):
		playlistName = 'test_audio_downloader_one_file'
		downloadDir = AUDIO_DIR + DIR_SEP + playlistName

		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)

		# deleting files in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)
			
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAccess(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		targetAudioDir, downloadedVideoInfoDictionary = youtubeAccess.downloadAudioFromPlaylist(playlistUrl)

		sys.stdout = stdout

		self.assertEqual(['downloading Wear a mask. Help slow the spread of Covid-19.',
						 '',
						 'downloading Wear a mask. Help slow the spread of Covid-19.',
						 'Wear a mask. Help slow the spread of Covid-19. downloaded.',
						 '',
						 ''], outputCapturingString.getvalue().split('\n'))

		self.assertEqual(downloadDir, targetAudioDir)
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', downloadedVideoInfoDictionary.getVideoInfoForVideoTitle('Wear a mask. Help slow the spread of Covid-19.')['url'])
		self.assertEqual('Wear a mask. Help slow the spread of Covid-19.', downloadedVideoInfoDictionary.getVideoInfoForVideoIndex(1)['title'])

		if os.name == 'posix':
			self.assertEqual('/storage/emulated/0/Download/Audiobooks/test_audio_downloader_one_file',
			                 downloadDir)
		else:
			self.assertEqual('D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks\\test_audio_downloader_one_file', downloadDir)

		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Wear a mask Help slow the spread of Covid-19.mp4']), sorted(fileNameLst))

	def testDownloadAudioFromPlaylistOneVideo_targetFolder_not_exist(self):
		playlistName = 'test_audio_downloader_one_file'
		downloadDir = AUDIO_DIR + DIR_SEP + playlistName

		# deleting downloadDir (dir and content)
		if os.path.exists(downloadDir):
			shutil.rmtree(downloadDir)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAccess(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRxj8f47BrkV9S6WoxYWYDS"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		youtubeAccess.downloadAudioFromPlaylist(playlistUrl)

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
		self.assertEqual(sorted(['Wear a mask Help slow the spread of Covid-19.mp4']), sorted(fileNameLst))

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
		youtubeAccess = YoutubeAccess(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRGA1T1vOn500RuLFo_lGJv"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		targetAudioDir, downloadedVideoInfoDictionary = youtubeAccess.downloadAudioFromPlaylist(playlistUrl)

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
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', downloadedVideoInfoDictionary.getVideoInfoForVideoTitle('Wear a mask. Help slow the spread of Covid-19.')['url'])
		self.assertEqual('https://youtube.com/watch?v=Eqy6M6qLWGw', downloadedVideoInfoDictionary.getVideoInfoForVideoTitle('Here to help: Give him what he wants')['url'])

		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Wear a mask Help slow the spread of Covid-19.mp4', 'Here to help Give him what he wants.mp4',]), sorted(fileNameLst))
	
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
		youtubeAccess = YoutubeAccess(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMSFWGrRGKOypqN29MlyuQvn"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		targetAudioDir, downloadedVideoInfoDictionary = youtubeAccess.downloadAudioFromPlaylist(
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
		                 downloadedVideoInfoDictionary.getExtractStartEndSecondsLists(videoIndex=1))
		self.assertEqual([],
		                 downloadedVideoInfoDictionary.getSuppressStartEndSecondsLists(videoIndex=1))
		
		self.assertEqual([],
		                 downloadedVideoInfoDictionary.getExtractStartEndSecondsLists(videoIndex=2))
		self.assertEqual([startEndSecondsList_suppress_secondVideo_firstTimeFrame,
		                  startEndSecondsList_suppress_secondVideo_secondTimeFrame],
		                 downloadedVideoInfoDictionary.getSuppressStartEndSecondsLists(videoIndex=2))

		self.assertEqual(downloadDir, targetAudioDir)
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk',
		                 downloadedVideoInfoDictionary.getVideoInfoForVideoTitle('Wear a mask. Help slow the spread of Covid-19.')['url'])
		self.assertEqual('https://youtube.com/watch?v=Eqy6M6qLWGw',
		                 downloadedVideoInfoDictionary.getVideoInfoForVideoTitle('Here to help: Give him what he wants')['url'])
		
		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(
			sorted(['Wear a mask Help slow the spread of Covid-19.mp4', 'Here to help Give him what he wants.mp4', ]),
			sorted(fileNameLst))
	
	def testDownloadAudioFromPlaylistOneVideo_invalid_url(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAccess(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=invalid"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		youtubeAccess.downloadAudioFromPlaylist(playlistUrl)
		
		sys.stdout = stdout
		
		if os.name == 'posix':
			self.assertEqual(['The URL obtained from clipboard is not pointing to a playlist. Program closed.',
			                  ''], outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual(['The URL obtained from clipboard is not pointing to a playlist. Program closed.',
			                  ''], outputCapturingString.getvalue().split('\n'))
	
	def testDownloadAudioFromPlaylistOneVideo_empty_url(self):
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeAccess(guiOutput)
		playlistUrl = ""
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		youtubeAccess.downloadAudioFromPlaylist(playlistUrl)
		
		sys.stdout = stdout
		
		self.assertEqual('The URL obtained from clipboard is not pointing to a playlist. Program closed.\n', outputCapturingString.getvalue())
	
	def testDownloadAudioFromPlaylistOneVideo_with_timeFrame(self):
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
		youtubeAccess = YoutubeAccess(guiOutput)
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMTB7GasAttwVnPPk3-WTMNJ"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		targetAudioDir, downloadedVideoInfoDictionary = youtubeAccess.downloadAudioFromPlaylist(playlistUrl)
		
		sys.stdout = stdout

		self.assertEqual(['downloading Wear a mask. Help slow the spread of Covid-19.',
						 '',
						 'downloading Wear a mask. Help slow the spread of Covid-19.',
						 'Wear a mask. Help slow the spread of Covid-19. downloaded.',
						 '',
						 ''], outputCapturingString.getvalue().split('\n'))

		self.assertEqual([[5, 10]], downloadedVideoInfoDictionary.getExtractStartEndSecondsLists(1))
		self.assertEqual(downloadDir, targetAudioDir)
		self.assertEqual('https://youtube.com/watch?v=9iPvLx7gotk', downloadedVideoInfoDictionary.getVideoInfoForVideoTitle('Wear a mask. Help slow the spread of Covid-19.')['url'])

		if os.name == 'posix':
			self.assertEqual('/storage/emulated/0/Download/Audiobooks/'+ playlistName,
			                 downloadDir)
		else:
			self.assertEqual('D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks\\' + playlistName,
			                 downloadDir)

		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Wear a mask Help slow the spread of Covid-19.mp4']), sorted(fileNameLst))
		self.assertEqual([[5, 10]], downloadedVideoInfoDictionary.getExtractStartEndSecondsLists(videoIndex=1))

if __name__ == '__main__':
#	unittest.main()
	tst = TestYoutubeAccessDownloadMethods()
	tst.testDownloadAudioFromPlaylistMultipleVideo_withTimeFrames()
