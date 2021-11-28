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

class TestYoutubeDlAudioDownloaderDownloadMethodsSingleVideo(unittest.TestCase):
	
	def testDownloadSingleVideoForUrl_targetFolder_exist(self):
		expectedVideoTitle = 'Funny suspicious looking dog'
		audioSubDirName = 'Various_test'
		downloadDir = DirUtil.getTestAudioRootPath() + sep + audioSubDirName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting files in downloadDir
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		videoUrl = "https://youtu.be/vU1NEZ9sTOM"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(videoUrl)
		
		self.assertIsNone(accessError)
		self.assertEqual(expectedVideoTitle, videoTitle)
		
		youtubeAccess.downloadSingleVideoForUrl(singleVideoUrl=videoUrl,
		                                        originalVideoTitle=videoTitle,
		                                        modifiedVideoTitle=None,
		                                        targetAudioDir=downloadDir)
		
		sys.stdout = stdout
		
		
		if os.name == 'posix':
			self.assertEqual(['downloading "Funny suspicious looking dog" audio ...',
 							'',
							 '"Funny suspicious looking dog" audio downloaded in "test/Various_test" '
							 'dir.',
							 '',
							 ''], outputCapturingString.getvalue().split('\n'))
			self.assertEqual('/storage/emulated/0/Download/Audiobooks/test/' + audioSubDirName,
			                 downloadDir)
		else:
			self.assertEqual(['downloading "Funny suspicious looking dog 2013-11-05.mp3" audio ...',
 '',
 '"Funny suspicious looking dog 2013-11-05.mp3" audio downloaded in '
 '"test\\Various_test" directory.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
			self.assertEqual(DirUtil.getTestAudioRootPath() + sep + audioSubDirName,
			                 downloadDir)
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Funny suspicious looking dog 2013-11-05.mp3']), sorted(fileNameLst))
	
	def testDownloadSingleVideoForUrl_targetFolder_not_exist(self):
		expectedVideoTitle = 'Funny suspicious looking dog'
		audioSubDirName = 'Various_test_new'
		downloadDir = DirUtil.getTestAudioRootPath() + sep + audioSubDirName
		
		# deleting downloadDir (dir and content)
		if os.path.exists(downloadDir):
			shutil.rmtree(downloadDir)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		videoUrl = "https://youtu.be/vU1NEZ9sTOM"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(videoUrl)
		
		self.assertIsNone(accessError)
		self.assertEqual(expectedVideoTitle, videoTitle)
		
		youtubeAccess.downloadSingleVideoForUrl(singleVideoUrl=videoUrl,
		                                        originalVideoTitle=videoTitle,
		                                        modifiedVideoTitle=None,
		                                        targetAudioDir=downloadDir)
		
		sys.stdout = stdout
		
		
		if os.name == 'posix':
			self.assertEqual(['directory',
 							'Audiobooks/Various_test_new',
 							'was created.',
							 '',
							 'downloading "Funny suspicious looking dog" audio ...',
							 '',
							 '"Funny suspicious looking dog" audio downloaded in '
							 '"test/Various_test_new" dir.',
							 '',
							 ''], outputCapturingString.getvalue().split('\n'))
			self.assertEqual('/storage/emulated/0/Download/Audiobooks/test/' + audioSubDirName,
			                 downloadDir)
		else:
			self.assertEqual(['directory',
 'test\\Various_test_new',
 'was created.',
 '',
 'downloading "Funny suspicious looking dog 2013-11-05.mp3" audio ...',
 '',
 '"Funny suspicious looking dog 2013-11-05.mp3" audio downloaded in '
 '"test\\Various_test_new" directory.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
			self.assertEqual(DirUtil.getTestAudioRootPath() + sep + audioSubDirName,
			                 downloadDir)
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Funny suspicious looking dog 2013-11-05.mp3']), sorted(fileNameLst))
	
	def testDownloadSingleVideoForUrl_redownloading_video(self):
		expectedVideoTitle = 'Funny suspicious looking dog'
		audioSubDirName = 'Various_test'
		downloadDir = DirUtil.getTestAudioRootPath() + sep + audioSubDirName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting files in downloadDir
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		videoUrl = 'https://youtu.be/vU1NEZ9sTOM'
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(videoUrl)
		
		self.assertIsNone(accessError)
		self.assertEqual(expectedVideoTitle, videoTitle)

		youtubeAccess.downloadSingleVideoForUrl(singleVideoUrl=videoUrl,
		                                        originalVideoTitle=videoTitle,
		                                        modifiedVideoTitle=None,
		                                        targetAudioDir=downloadDir)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString

		youtubeAccess.downloadSingleVideoForUrl(singleVideoUrl=videoUrl,
		                                        originalVideoTitle=videoTitle,
		                                        modifiedVideoTitle=None,
		                                        targetAudioDir=downloadDir)

		sys.stdout = stdout
		
		self.assertEqual(['"Funny suspicious looking dog 2013-11-05.mp3" audio already downloaded in '
 '"test\\Various_test" dir. Video skipped.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
	
	def testDownloadSingleVideoForUrl_redownloading_video_title_ending_with_question_mark(self):
		expectedVideoTitle = 'Comment Etudier Un Cours En Miracles ?'
		audioSubDirName = 'Various_test_not_emptied'
		downloadDir = DirUtil.getTestAudioRootPath() + sep + audioSubDirName
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, downloadDir)
		videoUrl = 'https://youtu.be/tT032M6mSGQ'
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(videoUrl)
		
		self.assertIsNone(accessError)
		self.assertEqual(expectedVideoTitle, videoTitle)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		youtubeAccess.downloadSingleVideoForUrl(singleVideoUrl=videoUrl,
		                                        originalVideoTitle=videoTitle,
		                                        modifiedVideoTitle=None,
		                                        targetAudioDir=downloadDir)
		
		sys.stdout = stdout

		self.assertEqual(['"Comment Etudier Un Cours En Miracles  2018-12-16.mp3" audio already '
 'downloaded in "Various_test_not_emptied" dir. Video skipped.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
	
	def testDownloadSingleVideoForUrl_redownloading_video_title_containing_slash(self):
		expectedVideoTitle = 'Aimer sans peur 3/9 - Gary Renard'
		audioSubDirName = 'Various_test_not_emptied'
		downloadDir = DirUtil.getTestAudioRootPath() + sep + audioSubDirName
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, downloadDir)
		videoUrl = 'https://youtu.be/EHsi_KPKFqU'
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(videoUrl)
		
		self.assertIsNone(accessError)
		self.assertEqual(expectedVideoTitle, videoTitle)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		youtubeAccess.downloadSingleVideoForUrl(singleVideoUrl=videoUrl,
		                                        originalVideoTitle=videoTitle,
		                                        modifiedVideoTitle=None,
		                                        targetAudioDir=downloadDir)
		
		sys.stdout = stdout
		
		self.assertEqual(['"Aimer sans peur 3_9 - Gary Renard 2013-03-26.mp3" audio already downloaded '
 'in "Various_test_not_emptied" dir. Video skipped.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
	
	def testDownloadSingleVideoForUrl_succeed_on_Windows_only(self):
		"""
		As unit test, works on Android although the downloaded file is not fully valid:
		can be played, but without setting position.
		"""
		expectedVideoTitle = 'Is NEO Worth Buying? - Price Prediction 2020/2021 🚀🚀🚀'
		audioSubDirName = 'Various_test'
		downloadDir = DirUtil.getTestAudioRootPath() + sep + audioSubDirName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting files in downloadDir
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		videoUrl = "https://youtu.be/LhH9uX3kgTI"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			youtubeAccess.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(videoUrl)
		
		self.assertIsNone(accessError)
		self.assertEqual(expectedVideoTitle, videoTitle)
		
		youtubeAccess.downloadSingleVideoForUrl(singleVideoUrl=videoUrl,
		                                        originalVideoTitle=videoTitle,
		                                        modifiedVideoTitle=None,
		                                        targetAudioDir=downloadDir)
		
		sys.stdout = stdout
		
		if os.name == 'posix':
			self.assertEqual(['downloading "Is NEO Worth Buying? - Price Prediction 2020/2021 🚀🚀🚀" audio '
							 '...',
							 '',
							 '"Is NEO Worth Buying? - Price Prediction 2020/2021 🚀🚀🚀" audio downloaded in '
							 '"test/Various_test" dir.',
							 '',
							 ''], outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual(['downloading "Is NEO Worth Buying - Price Prediction 2020_2021 🚀🚀🚀 '
 '2020-09-26.mp3" audio ...',
 '',
 '"Is NEO Worth Buying - Price Prediction 2020_2021 🚀🚀🚀 2020-09-26.mp3" audio '
 'downloaded in "test\\Various_test" directory.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		if os.name == 'posix':
			self.assertEqual('/storage/emulated/0/Download/Audiobooks/test/' + audioSubDirName,
			                 downloadDir)
		else:
			self.assertEqual(DirUtil.getTestAudioRootPath() + sep + audioSubDirName,
			                 downloadDir)
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['Is NEO Worth Buying - Price Prediction 2020_2021 🚀🚀🚀 2020-09-26.mp3']), sorted(fileNameLst))
	
	def testDownloadPlaylistWithNameOneVideo_title_or_char(self):
		singleVideoDirName = "bug_or_char_single_video"
		singleVideoSaveDirName = "bug_or_char_single_video_save"
		downloadDir = DirUtil.getTestAudioRootPath() + sep + singleVideoDirName
		savedDownloadDir = DirUtil.getTestAudioRootPath() + sep + singleVideoSaveDirName
		
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
		                                           isUploadDateAddedToPlaylistVideo=False,
		                                           isIndexAddedToPlaylistVideo=False)
		
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
		
		dicFileName = singleVideoDirName + DownloadVideoInfoDic.DIC_FILE_NAME_EXTENT
		dicFilePathName = downloadDir + sep + dicFileName
		
		dvi = DownloadVideoInfoDic(playlistUrl=None,
		                           audioRootDir=None,
		                           playlistDownloadRootPath=None,
		                           originalPaylistTitle=None,
		                           originalPlaylistName=None,
		                           modifiedPlaylistTitle=None,
		                           modifiedPlaylistName=None,
		                           loadDicIfDicFileExist=True,
		                           existingDicFilePathName=dicFilePathName)
		
		self.assertEqual(
			"\ud83d\udca5 EFFONDREMEN Imminent de l'Euro ! _ \ud83d\udc49 Maintenant, La Fin de l'Euro Approche !.mp3",
			dvi.getVideoFileNameForVideoIndex(1))


if __name__ == '__main__':
	# unittest.main()
	tst = TestYoutubeDlAudioDownloaderDownloadMethodsSingleVideo()
	tst.setUp()
	tst.testDownloadSingleVideoForUrl_redownloading_video_title_ending_with_question_mark()