import unittest
import os, sys, inspect, shutil, glob
import datetime
from os.path import sep
from io import StringIO

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

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
		
		downloadDatePrefix = datetime.datetime.today().strftime("%y%m%d") + '-'
		
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
			self.assertEqual(['downloading "{}Funny suspicious looking dog 13-11-05.mp3" audio ...'.format(downloadDatePrefix),
 '',
 '"{}Funny suspicious looking dog 13-11-05.mp3" audio downloaded in '
 '"test\\Various_test" directory.'.format(downloadDatePrefix),
 '',
 ''], outputCapturingString.getvalue().split('\n'))
			self.assertEqual(DirUtil.getTestAudioRootPath() + sep + audioSubDirName,
			                 downloadDir)
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['{}Funny suspicious looking dog 13-11-05.mp3'.format(downloadDatePrefix)]), sorted(fileNameLst))
	
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
		
		downloadDatePrefix = datetime.datetime.today().strftime("%y%m%d") + '-'
		
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
 'downloading "{}Funny suspicious looking dog 13-11-05.mp3" audio ...'.format(downloadDatePrefix),
 '',
 '"{}Funny suspicious looking dog 13-11-05.mp3" audio downloaded in '
 '"test\\Various_test_new" directory.'.format(downloadDatePrefix),
 '',
 ''], outputCapturingString.getvalue().split('\n'))
			self.assertEqual(DirUtil.getTestAudioRootPath() + sep + audioSubDirName,
			                 downloadDir)
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['{}Funny suspicious looking dog 13-11-05.mp3'.format(downloadDatePrefix)]), sorted(fileNameLst))
	
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
		
		downloadDatePrefix = datetime.datetime.today().strftime("%y%m%d") + '-'

		self.assertEqual(['"{}Funny suspicious looking dog 13-11-05.mp3" audio already downloaded in '
 '"test\\Various_test" dir. Video skipped.'.format(downloadDatePrefix),
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

		downloadDatePrefix = datetime.datetime.today().strftime("%y%m%d") + '-'

		self.assertEqual(['"{}Comment Etudier Un Cours En Miracles  18-12-16.mp3" audio already '
 'downloaded in "Various_test_not_emptied" dir. Video skipped.'.format(downloadDatePrefix),
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

		downloadDatePrefix = datetime.datetime.today().strftime("%y%m%d") + '-'

		self.assertEqual(['"{}Aimer sans peur 3_9 - Gary Renard 13-03-26.mp3" audio already downloaded '
 'in "Various_test_not_emptied" dir. Video skipped.'.format(downloadDatePrefix),
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

		downloadDatePrefix = datetime.datetime.today().strftime("%y%m%d") + '-'

		if os.name == 'posix':
			self.assertEqual(['downloading "{}Is NEO Worth Buying? - Price Prediction 2020/2021 🚀🚀🚀" audio '
							 '...'.format(downloadDatePrefix),
							 '',
							 '"{}Is NEO Worth Buying? - Price Prediction 2020/2021 🚀🚀🚀" audio downloaded in '
							 '"test/Various_test" dir.'.format(downloadDatePrefix),
							 '',
							 ''], outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual(['downloading "{}Is NEO Worth Buying - Price Prediction 2020_2021 🚀🚀🚀 '
 '20-09-26.mp3" audio ...'.format(downloadDatePrefix),
 '',
 '"{}Is NEO Worth Buying - Price Prediction 2020_2021 🚀🚀🚀 20-09-26.mp3" audio '
 'downloaded in "test\\Various_test" directory.'.format(downloadDatePrefix),
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		if os.name == 'posix':
			self.assertEqual('/storage/emulated/0/Download/Audiobooks/test/' + audioSubDirName,
			                 downloadDir)
		else:
			self.assertEqual(DirUtil.getTestAudioRootPath() + sep + audioSubDirName,
			                 downloadDir)
		
		fileNameLst = [x.split(sep)[-1] for x in glob.glob(downloadDir + sep + '*.*')]
		self.assertEqual(sorted(['{}Is NEO Worth Buying - Price Prediction 2020_2021 🚀🚀🚀 20-09-26.mp3'.format(downloadDatePrefix)]), sorted(fileNameLst))


if __name__ == '__main__':
	# unittest.main()
	tst = TestYoutubeDlAudioDownloaderDownloadMethodsSingleVideo()
	tst.setUp()
	tst.testDownloadPlaylistWithNameOneVideo_title_or_char()