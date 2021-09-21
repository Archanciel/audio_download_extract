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
		files = glob.glob(downloadDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		videoUrl = "https://youtu.be/vU1NEZ9sTOM"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		downloadVideoInfoDic, videoTitle, accessError = youtubeAccess.getDownloadVideoInfoDicOrSingleVideoTitleFortUrl(
			videoUrl)

		self.assertIsNone(downloadVideoInfoDic)
		self.assertIsNone(accessError)
		self.assertEqual(expectedVideoTitle, videoTitle)

		youtubeAccess.downloadSingleVideoForUrl(videoUrl, videoTitle, downloadDir)
		
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
			self.assertEqual(['downloading "Funny suspicious looking dog" audio ...',
 '',
 '"Funny suspicious looking dog" audio downloaded in "test\\Various_test" directory.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
			self.assertEqual(DirUtil.getTestAudioRootPath() + sep + audioSubDirName,
			                 downloadDir)
		
		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Funny suspicious looking dog.mp3']), sorted(fileNameLst))
	
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
		
		downloadVideoInfoDic, videoTitle, accessError = youtubeAccess.getDownloadVideoInfoDicOrSingleVideoTitleFortUrl(
			videoUrl)
		
		self.assertIsNone(downloadVideoInfoDic)
		self.assertIsNone(accessError)
		self.assertEqual(expectedVideoTitle, videoTitle)
		
		youtubeAccess.downloadSingleVideoForUrl(videoUrl, videoTitle, downloadDir)
		
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
 'downloading "Funny suspicious looking dog" audio ...',
 '',
 '"Funny suspicious looking dog" audio downloaded in "test\\Various_test_new" '
 'directory.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
			self.assertEqual(DirUtil.getTestAudioRootPath() + sep + audioSubDirName,
			                 downloadDir)
		
		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Funny suspicious looking dog.mp3']), sorted(fileNameLst))
	
	def testDownloadSingleVideoForUrl_redownloading_video(self):
		expectedVideoTitle = 'Funny suspicious looking dog'
		audioSubDirName = 'Various_test'
		downloadDir = DirUtil.getTestAudioRootPath() + sep + audioSubDirName
		
		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting files in downloadDir
		files = glob.glob(downloadDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		videoUrl = 'https://youtu.be/vU1NEZ9sTOM'
		
		downloadVideoInfoDic, videoTitle, accessError = youtubeAccess.getDownloadVideoInfoDicOrSingleVideoTitleFortUrl(
			videoUrl)
		
		self.assertIsNone(downloadVideoInfoDic)
		self.assertIsNone(accessError)
		self.assertEqual(expectedVideoTitle, videoTitle)
		
		youtubeAccess.downloadSingleVideoForUrl(videoUrl, videoTitle, downloadDir)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString

		youtubeAccess.downloadSingleVideoForUrl(videoUrl, videoTitle, downloadDir)

		sys.stdout = stdout
		
		self.assertEqual(['"Funny suspicious looking dog" audio already downloaded in '
 '"test\\Various_test" dir. Video skipped.',
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
		files = glob.glob(downloadDir + DIR_SEP + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		youtubeAccess = YoutubeDlAudioDownloader(guiOutput, DirUtil.getTestAudioRootPath())
		videoUrl = "https://youtu.be/LhH9uX3kgTI"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		downloadVideoInfoDic, videoTitle, accessError = youtubeAccess.getDownloadVideoInfoDicOrSingleVideoTitleFortUrl(
			videoUrl)
		
		self.assertIsNone(downloadVideoInfoDic)
		self.assertIsNone(accessError)
		self.assertEqual(expectedVideoTitle, videoTitle)
		
		youtubeAccess.downloadSingleVideoForUrl(videoUrl, videoTitle, downloadDir)
		
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
			self.assertEqual(['downloading "Is NEO Worth Buying? - Price Prediction 2020/2021 🚀🚀🚀" audio '
 '...',
 '',
 '"Is NEO Worth Buying? - Price Prediction 2020/2021 🚀🚀🚀" audio downloaded in '
 '"test\\Various_test" directory.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		if os.name == 'posix':
			self.assertEqual('/storage/emulated/0/Download/Audiobooks/test/' + audioSubDirName,
			                 downloadDir)
		else:
			self.assertEqual(DirUtil.getTestAudioRootPath() + sep + audioSubDirName,
			                 downloadDir)
		
		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['Is NEO Worth Buying - Price Prediction 2020_2021 🚀🚀🚀.mp3']), sorted(fileNameLst))


if __name__ == '__main__':
	# unittest.main()
	tst = TestYoutubeDlAudioDownloaderDownloadMethodsSingleVideo()
	tst.setUp()
	tst.testDownloadSingleVideoForUrl_redownloading_video()