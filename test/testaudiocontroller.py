import datetime
import unittest
import os, sys, inspect, shutil, glob, time
from io import StringIO
from os.path import sep

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from guioutputstub import GuiOutputStub
from audiocontroller import AudioController
from configmanagerstub import ConfigManagerStub
from dirutil import DirUtil
from downloadplaylistinfodic import DownloadPlaylistInfoDic
			
class TestAudioController(unittest.TestCase):

	def testExtractAudioFromVideoFile(self):
		testDirName = 'test_audible_mobizen'
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + testDirName + sep
		videoFileName = 'Short low video quality'
		videoFilePathName = targetAudioDir + videoFileName + '.mp4'
		
		expectedExtractedAudioFileDuration = 964.661
		
		# deleting mp3 files in test dir
		files = glob.glob(targetAudioDir + sep + '*.mp3')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput, ConfigManagerStub(DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioController.extractAudioFromVideoFile(videoFilePathName)
		
		sys.stdout = stdout

		self.assertTrue(r'extracted audio file "{}Short low video quality.mp3" from video file "{}Short low video quality.mp4"'.format(targetAudioDir, targetAudioDir) in outputCapturingString.getvalue())

		videoAndAudioFileList = os.listdir(targetAudioDir)

		self.assertEqual(
			['Short low video quality.mp3',
			 'Short low video quality.mp4'],
			videoAndAudioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName = videoAndAudioFileList[1]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName)
		self.assertAlmostEqual(expectedExtractedAudioFileDuration, audio.info.length, delta=0.1)

	def testGetPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl_empty_url(self):
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput, ConfigManagerStub(DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		playlistUrl = ""
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			audioController.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)
		
		sys.stdout = stdout
		
		self.assertEqual('the URL obtained from clipboard is empty.\nnothing to download.', accessError.errorMsg)
	
	def testGetPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl_playlistUrl(self):
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManagerStub(DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMTB7GasAttwVnPPk3-WTMNJ"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			audioController.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(playlistUrl)
		
		sys.stdout = stdout

		self.assertIsNone(accessError)
		self.assertIsNone(videoTitle)
		self.assertEqual('Test_title_one_time_frame_extract (e0:0:5-0:0:10)', playlistTitle)
		self.assertIsNotNone(playlistObject)
	
	def testGetPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl_validVideotUrl(self):
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManagerStub(DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		videoUrl = "https://youtu.be/LhH9uX3kgTI"
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		playlistObject, playlistTitle, videoTitle, accessError = \
			audioController.getPlaylistObjectAndPlaylistTitleOrVideoTitleForUrl(videoUrl)
		
		sys.stdout = stdout
		
		self.assertIsNone(accessError)
		self.assertIsNone(playlistTitle)
		self.assertEqual('Is NEO Worth Buying? - Price Prediction 2020/2021 🚀🚀🚀', videoTitle)
		self.assertIsNotNone(playlistObject)

	def testClipAudioFile(self):
		playlistTitle = 'test_audio_controller_clip'
		playlistName = playlistTitle
		targetAudioDir = DirUtil.getTestAudioRootPath() + sep + playlistName
		audioFileName = 'LExpérience de Mort Imminente de Madame Mirjana Uzoh.mp3'
		audioFilePathName = targetAudioDir + sep + audioFileName
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManagerStub(DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))

		if not os.path.isdir(targetAudioDir):
			os.mkdir(targetAudioDir)
		
		# deleting clipped mp3 files in test dir
		files = glob.glob(targetAudioDir + sep + '*_*.mp3')
		
		for f in files:
			os.remove(f)
		
		clipStartHHMMSS = '00:00:17'
		clipEndHHMMSS = '00:00:49'
		expectedClipFileDuration_1 = 32
		
		audioExtractorVideoInfoDic = audioController.clipAudioFile(audioFilePathName=audioFilePathName,
		                                                           clipStartHHMMSS=clipStartHHMMSS,
		                                                           clipEndHHMMSS=clipEndHHMMSS,
		                                                           floatSpeed=1.0)
		createdClipFilePathName = audioExtractorVideoInfoDic.getExtractedFilePathNameForVideoIndexTimeFrameIndex(videoIndex=1, timeFrameIndex=1)
		audioFileList = os.listdir(targetAudioDir)
		
		self.assertEqual('\\test_audio_controller_clip\\LExpérience de Mort Imminente de Madame Mirjana Uzoh_1.mp3'.format(targetAudioDir),
		                 createdClipFilePathName)
		self.assertEqual(
			['LExpérience de Mort Imminente de Madame Mirjana Uzoh.mp3',
			 'LExpérience de Mort Imminente de Madame Mirjana Uzoh_1.mp3'],
			audioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = audioFileList[1]
		audio = MP3(targetAudioDir + sep + extractedMp3FileName_1)
		self.assertAlmostEqual(expectedClipFileDuration_1, audio.info.length, delta=0.1)
		
		# deleting clipped mp3 files in test dir to avoid uploading them on GitHub
		files = glob.glob(targetAudioDir + sep + '*_*.mp3')
		
		for f in files:
			os.remove(f)
	
	def testClipAudioFile_file_in_sub_dirs(self):
		playlistName = 'Test 3 short videos time frame deleted now should be ok'
		audioFileName = 'Here to help - Give him what he wants.mp3'
		playlistDownloadRootPath = 'Various\\test_clipAudioFile\\time frame supprimé\\{}'.format(playlistName)
		tstAudioRootPath = DirUtil.getTestAudioRootPath()
		audioFilePath = tstAudioRootPath + sep + playlistDownloadRootPath
		audioFilePathName = audioFilePath + sep + audioFileName
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManagerStub(DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		# deleting clipped mp3 files in test dir
		files = glob.glob(audioFilePath + sep + '*_*.mp3')
		
		for f in files:
			os.remove(f)
		
		clipStartHHMMSS = '00:00:04'
		clipEndHHMMSS = '00:00:08'
		expectedClipFileDuration_1 = 4
		
		audioExtractorVideoInfoDic = audioController.clipAudioFile(audioFilePathName=audioFilePathName,
		                                                           clipStartHHMMSS=clipStartHHMMSS,
		                                                           clipEndHHMMSS=clipEndHHMMSS,
		                                                           floatSpeed=1.0)
		createdClipFilePathName = audioExtractorVideoInfoDic. \
			getExtractedFilePathNameForVideoIndexTimeFrameIndex(videoIndex=1, timeFrameIndex=1)

		self.assertEqual('Various\\test_clipAudioFile\\time frame supprimé\\Test 3 short videos time frame deleted now should be ok\\Here to help - Give him what he wants_1.mp3'.format(tstAudioRootPath),
		                 createdClipFilePathName)
		
		audioFileList = os.listdir(audioFilePath)
		
		self.assertEqual(
			['Funny suspicious looking dog.mp3',
			 'Here to help - Give him what he wants.mp3',
			 'Here to help - Give him what he wants_1.mp3',
			 'Test 3 short videos time frame deleted now should be ok_dic.txt',
			 'Wear a mask. Help slow the spread of Covid-19..mp3'],
			audioFileList)
		
		from mutagen.mp3 import MP3
		extractedMp3FileName_1 = audioFileList[2]
		audio = MP3(audioFilePath + sep + extractedMp3FileName_1)
		self.assertAlmostEqual(expectedClipFileDuration_1, audio.info.length, delta=0.1)
		
		# deleting clipped mp3 files in test dir to avoid uploading them on GitHub
		files = glob.glob(audioFilePath + sep + '*_*.mp3')
		
		for f in files:
			os.remove(f)
	
	def testDownloadSingleVideoTwice(self):
		playlistOrSingleVideoUrl = 'https://youtu.be/vU1NEZ9sTOM'
		singleVideoTitle = 'Funny suspicious looking dog'
		
		testBaseRootDir = 'Various' + sep + 'single_video dir'
		testBaseRootPath = DirUtil.getTestAudioRootPath() + sep + testBaseRootDir
		playlistOrSingleVideoDownloadRootSubdirs = 'new dir' + sep + 'new sub dir'
		playlistOrSingleVideoDownloadPath = testBaseRootPath + sep + playlistOrSingleVideoDownloadRootSubdirs
		
		# removing test dir and sub dirs and its files
		DirUtil.deleteDirAndItsSubDirs(testBaseRootPath)
		
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManagerStub(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		# first download
		
		audioController.downloadSingleVideo(
			singleVideoUrl=playlistOrSingleVideoUrl,
			singleVideoDownloadPath=playlistOrSingleVideoDownloadPath,
			originalSingleVideoTitle=singleVideoTitle,
			modifiedVideoTitle=None)

		# second download

		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		audioController.downloadSingleVideo(
			singleVideoUrl=playlistOrSingleVideoUrl,
			singleVideoDownloadPath=playlistOrSingleVideoDownloadPath,
			originalSingleVideoTitle=singleVideoTitle,
			modifiedVideoTitle=None)
		sys.stdout = stdout
		
		downloadDatePrefix = datetime.datetime.today().strftime('%y%m%d') + '-'
		
		if os.name == 'posix':
			self.assertEqual(['"Funny suspicious looking dog 2013-11-05.mp3" audio already downloaded in '
 '"Audio/test/Various/single_video dir/new dir/new sub dir" dir. Video '
 'skipped.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual('{}Funny suspicious looking dog 13-11-05.mp3 audio already downloaded in testData\\Various\\single_video dir\\new dir\\new sub dir dir. Single video skipped.\n\n'.format(downloadDatePrefix), outputCapturingString.getvalue())
		
		createdFileLst = os.listdir(playlistOrSingleVideoDownloadPath)
		
		self.assertEqual(
			['{}Funny suspicious looking dog 13-11-05.mp3'.format(downloadDatePrefix)],
			createdFileLst)

	def testDeleteAudioFilesFromDirAndFromDic_all(self):
		testDirName = 'test delete files'
		testDirNameSaved = 'test delete files save dir'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		testPath = testAudioDirRoot + sep + testDirName
		testPathSaved = testAudioDirRoot + sep + testDirNameSaved

		videoTitle_1 = 'Wear a mask. Help slow the spread of Covid-19.'
		videoTitle_2 = 'Here to help: Give him what he wants'
		videoTitle_3 = 'Funny suspicious looking dog'

		# restoring test dir
		
		if os.path.exists(testPath):
			shutil.rmtree(testPath)
		
		shutil.copytree(testPathSaved, testPath)
		
		# obtaining the download video info dic file path name
		dicFilePathNameLst = DirUtil.getFilePathNamesInDirForPattern(testPath, '*' + DownloadPlaylistInfoDic.DIC_FILE_NAME_EXTENT)
		dicFilePathName = dicFilePathNameLst[0]
		
		dvi = DownloadPlaylistInfoDic(playlistUrl=None,
		                              audioRootDir=None,
		                              playlistDownloadRootPath=None,
		                              originalPaylistTitle=None,
		                              originalPlaylistName=None,
		                              modifiedPlaylistTitle=None,
		                              modifiedPlaylistName=None,
		                              loadDicIfDicFileExist=True,
		                              existingDicFilePathName=dicFilePathName)
		
		self.assertIsNotNone(dvi)
		
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk',
		                 dvi.getVideoUrlForVideoTitle(videoTitle_1))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                 dvi.getVideoUrlForVideoTitle(videoTitle_2))
		self.assertEqual('https://www.youtube.com/watch?v=vU1NEZ9sTOM',
		                 dvi.getVideoUrlForVideoTitle(videoTitle_3))
		
		deletedFilePathNameLst = DirUtil.getFilePathNamesInDirForPattern(testPath, '*.mp3')
		
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManagerStub(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		audioController.deleteAudioFilesFromDirAndFromDic(deletedFilePathNameLst)
		
		dvi_after_deletion = DownloadPlaylistInfoDic(playlistUrl=None,
		                                             audioRootDir=None,
		                                             playlistDownloadRootPath=None,
		                                             originalPaylistTitle=None,
		                                             originalPlaylistName=None,
		                                             modifiedPlaylistTitle=None,
		                                             modifiedPlaylistName=None,
		                                             loadDicIfDicFileExist=True,
		                                             existingDicFilePathName=dicFilePathName)

		self.assertEqual([], DirUtil.getFilePathNamesInDirForPattern(testPath, '*.mp3'))
		self.assertIsNone(dvi_after_deletion.getVideoUrlForVideoTitle(videoTitle_1))
		self.assertIsNone(dvi_after_deletion.getVideoUrlForVideoTitle(videoTitle_2))
		self.assertIsNone(dvi_after_deletion.getVideoUrlForVideoTitle(videoTitle_3))

		#  deleting test result files in order to avoid uploading it on GitHub
		if os.path.exists(testPath):
			shutil.rmtree(testPath)

	def testDeleteAudioFilesFromDirAndFromDic_all_noDownloadInfoDicFile(self):
		testDirName = 'test delete files noDownloadInfoDic'
		testDirNameSaved = 'test delete files save dir'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		testPath = testAudioDirRoot + sep + testDirName
		testPathSaved = testAudioDirRoot + sep + testDirNameSaved
		
		videoTitle_1 = 'Wear a mask. Help slow the spread of Covid-19.'
		videoTitle_2 = 'Here to help: Give him what he wants'
		videoTitle_3 = 'Funny suspicious looking dog'
		
		# restoring test dir
		
		if os.path.exists(testPath):
			shutil.rmtree(testPath)
		
		shutil.copytree(testPathSaved, testPath)
		
		downloadvideoinfodicFilePathNameLst = DirUtil.getFilePathNamesInDirForPattern(testPath, '*.txt')
		DirUtil.deleteFiles(downloadvideoinfodicFilePathNameLst)
		
		deletedFilePathNameLst = DirUtil.getFilePathNamesInDirForPattern(testPath, '*.mp3')
		
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManagerStub(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		audioController.deleteAudioFilesFromDirAndFromDic(deletedFilePathNameLst)
	
		self.assertEqual([], DirUtil.getFilePathNamesInDirForPattern(testPath, '*.mp3'))

		#  deleting test result files in order to avoid uploading it on GitHub
		if os.path.exists(testPath):
			shutil.rmtree(testPath)

	def testDeleteAudioFilesFromDirAndFromDic_some(self):
		testDirName = 'test delete files'
		testDirNameSaved = 'test delete files save dir'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		testPath = testAudioDirRoot + sep + testDirName
		testPathSaved = testAudioDirRoot + sep + testDirNameSaved
		
		videoTitle_1 = 'Wear a mask. Help slow the spread of Covid-19.'
		videoTitle_2 = 'Here to help: Give him what he wants'
		videoTitle_3 = 'Funny suspicious looking dog'
		
		# restoring test dir
		
		if os.path.exists(testPath):
			shutil.rmtree(testPath)
		
		shutil.copytree(testPathSaved, testPath)
		
		# obtaining the download video info dic file path name
		dicFilePathNameLst = DirUtil.getFilePathNamesInDirForPattern(testPath,
		                                                         '*' + DownloadPlaylistInfoDic.DIC_FILE_NAME_EXTENT)
		dicFilePathName = dicFilePathNameLst[0]
		
		dvi = DownloadPlaylistInfoDic(playlistUrl=None,
		                              audioRootDir=None,
		                              playlistDownloadRootPath=None,
		                              originalPaylistTitle=None,
		                              originalPlaylistName=None,
		                              modifiedPlaylistTitle=None,
		                              modifiedPlaylistName=None,
		                              loadDicIfDicFileExist=True,
		                              existingDicFilePathName=dicFilePathName)
		
		self.assertIsNotNone(dvi)
		
		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk',
		                 dvi.getVideoUrlForVideoTitle(videoTitle_1))
		self.assertEqual('https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                 dvi.getVideoUrlForVideoTitle(videoTitle_2))
		self.assertEqual('https://www.youtube.com/watch?v=vU1NEZ9sTOM',
		                 dvi.getVideoUrlForVideoTitle(videoTitle_3))
		
		deletedAllFilePathNameLst = DirUtil.getFilePathNamesInDirForPattern(testPath, '*.mp3')
		deletedFilePathNameLst = deletedAllFilePathNameLst[:-1]
		
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManagerStub(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		audioController.deleteAudioFilesFromDirAndFromDic(deletedFilePathNameLst)
		
		dvi_after_deletion = DownloadPlaylistInfoDic(playlistUrl=None,
		                                             audioRootDir=None,
		                                             playlistDownloadRootPath=None,
		                                             originalPaylistTitle=None,
		                                             originalPlaylistName=None,
		                                             modifiedPlaylistTitle=None,
		                                             modifiedPlaylistName=None,
		                                             loadDicIfDicFileExist=True,
		                                             existingDicFilePathName=dicFilePathName)
		
		self.assertEqual(['{}\\test delete files\\99-Wear a mask. Help slow the spread of Covid-19. 2020-07-31.mp3'.format(testAudioDirRoot)], DirUtil.getFilePathNamesInDirForPattern(testPath, '*.mp3'))

		self.assertEqual('https://www.youtube.com/watch?v=9iPvLx7gotk',
		                 dvi.getVideoUrlForVideoTitle(videoTitle_1))
		self.assertIsNone(dvi_after_deletion.getVideoUrlForVideoTitle(videoTitle_2))
		self.assertIsNone(dvi_after_deletion.getVideoUrlForVideoTitle(videoTitle_3))

		#  deleting test result files in order to avoid uploading it on GitHub
		if os.path.exists(testPath):
			shutil.rmtree(testPath)

	def testDownloadVideosReferencedInPlaylist_noTimeFrame(self):
		playlistTitle = 'test_audio_downloader_two_files'
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRGA1T1vOn500RuLFo_lGJv"
		subTestDirName = 'ctr1'
		validPlaylistDirName = DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistTitle)
		testAudioRootPath = DirUtil.getTestAudioRootPath()
		testAudioRootSubDirPath = testAudioRootPath + sep + subTestDirName
		downloadDir = testAudioRootSubDirPath + sep + validPlaylistDirName
		isIndexAddedToPlaylistVideo = True
		isUploadDateAddedToPlaylistVideo = True
		
		DirUtil.createTargetDirIfNotExist(rootDir=testAudioRootPath,
		                                  targetAudioDir=downloadDir)
		# deleting files in downloadDir
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManagerStub(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		downloadVideoInfoDic, indexAndDateSettingWarningMsg = audioController.getDownloadVideoInfoDicAndIndexDateSettingWarningMsg(
			playlistOrSingleVideoUrl=playlistUrl,
			playlistOrSingleVideoDownloadPath=testAudioRootSubDirPath,
			originalPlaylistTitle=playlistTitle,
			modifiedPlaylistTitle=playlistTitle,
			isIndexAddedToPlaylistVideo=isIndexAddedToPlaylistVideo,
			isUploadDateAddedToPlaylistVideo=isUploadDateAddedToPlaylistVideo)
		
		audioController.downloadVideosReferencedInPlaylist(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                   isIndexAddedToPlaylistVideo=isIndexAddedToPlaylistVideo,
		                                                   isUploadDateAddedToPlaylistVideo=isUploadDateAddedToPlaylistVideo)
		
		sys.stdout = stdout

		downloadDateTodayPrefix = datetime.datetime.today().strftime("%y%m%d") + '-'

		if os.name == 'posix':
			self.assertEqual(['"Funny suspicious looking dog 2013-11-05.mp3" audio already downloaded in '
			                  '"Audio/test/Various/single_video dir/new dir/new sub dir" dir. Video '
			                  'skipped.',
			                  '',
			                  ''], outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual(['downloading "' + downloadDateTodayPrefix + 'Wear a mask. Help slow the spread of Covid-19. '
 '20-07-31.mp3" audio ...',
 '',
 'video download complete.',
 '',
 'downloading "' + downloadDateTodayPrefix + 'Here to help - Give him what he wants 19-06-07.mp3" '
 'audio ...',
 '',
 'video download complete.',
 '',
 '"test_audio_downloader_two_files" playlist audio(s) download terminated.',
 '',
 '',
 '"test_audio_downloader_two_files" playlist audio(s) extraction/suppression '
 'terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		createdFileLst = os.listdir(downloadDir)
		
		self.assertEqual(
			['' + downloadDateTodayPrefix + 'Here to help - Give him what he wants 19-06-07.mp3',
			 '' + downloadDateTodayPrefix + 'Wear a mask. Help slow the spread of Covid-19. 20-07-31.mp3',
			 'test_audio_downloader_two_files_dic.txt'],
			createdFileLst)
		
		# deleting clipped mp3 files in test dir to avoid uploading them on GitHub
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
	
	def testDownloadVideosReferencedInPlaylist_noTimeFrame_renamed(self):
		playlistTitle = 'test_audio_downloader_two_files'
		playlistTitleRenamed = 'test_audio_downloader_two_files_noTimeFrame_renamed'
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMRGA1T1vOn500RuLFo_lGJv"
		subTestDirName = 'ctr1'
		validPlaylistDirName = DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistTitleRenamed)
		testAudioRootPath = DirUtil.getTestAudioRootPath()
		testAudioRootSubDirPath = testAudioRootPath + sep + subTestDirName
		downloadDir = testAudioRootSubDirPath + sep + validPlaylistDirName
		isIndexAddedToPlaylistVideo = True
		isUploadDateAddedToPlaylistVideo = True
		
		DirUtil.createTargetDirIfNotExist(rootDir=testAudioRootPath,
		                                  targetAudioDir=downloadDir)
		# deleting files in downloadDir
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManagerStub(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		downloadVideoInfoDic, indexAndDateSettingWarningMsg = audioController.getDownloadVideoInfoDicAndIndexDateSettingWarningMsg(
			playlistOrSingleVideoUrl=playlistUrl,
			playlistOrSingleVideoDownloadPath=testAudioRootSubDirPath,
			originalPlaylistTitle=playlistTitle,
			modifiedPlaylistTitle=playlistTitleRenamed,
			isIndexAddedToPlaylistVideo=isIndexAddedToPlaylistVideo,
			isUploadDateAddedToPlaylistVideo=isUploadDateAddedToPlaylistVideo)
		
		audioController.downloadVideosReferencedInPlaylist(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                   isIndexAddedToPlaylistVideo=isIndexAddedToPlaylistVideo,
		                                                   isUploadDateAddedToPlaylistVideo=isUploadDateAddedToPlaylistVideo)
		
		sys.stdout = stdout

		downloadDateTodayPrefix = datetime.datetime.today().strftime("%y%m%d") + '-'

		if os.name == 'posix':
			self.assertEqual(['"Funny suspicious looking dog 2013-11-05.mp3" audio already downloaded in '
			                  '"Audio/test/Various/single_video dir/new dir/new sub dir" dir. Video '
			                  'skipped.',
			                  '',
			                  ''], outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual(['downloading "' + downloadDateTodayPrefix + 'Wear a mask. Help slow the spread of Covid-19. '
 '20-07-31.mp3" audio ...',
 '',
 'video download complete.',
 '',
 'downloading "' + downloadDateTodayPrefix + 'Here to help - Give him what he wants 19-06-07.mp3" '
 'audio ...',
 '',
 'video download complete.',
 '',
 '"test_audio_downloader_two_files" playlist audio(s) download terminated.',
 '',
 '',
 '"test_audio_downloader_two_files" playlist audio(s) extraction/suppression '
 'terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		createdFileLst = os.listdir(downloadDir)
		
		self.assertEqual(
			['' + downloadDateTodayPrefix + 'Here to help - Give him what he wants 19-06-07.mp3',
			 '' + downloadDateTodayPrefix + 'Wear a mask. Help slow the spread of Covid-19. 20-07-31.mp3',
			 'test_audio_downloader_two_files_noTimeFrame_renamed_dic.txt'],
			createdFileLst)
		
		# deleting clipped mp3 files in test dir to avoid uploading them on GitHub
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
	
	def testDownloadVideosReferencedInPlaylist_withTimeFrame(self):
		playlistTitle = 'test_audio_downloader_two_files_with_time_frames (e0:0:2-0:0:8) (s0:0:2-0:0:5 s0:0:7-0:0:10)'
		playlistName = 'test_audio_downloader_two_files_with_time_frames'
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMSFWGrRGKOypqN29MlyuQvn"
		subTestDirName = 'ctr1'
		validPlaylistDirName = DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistName)
		testAudioRootPath = DirUtil.getTestAudioRootPath()
		testAudioRootSubDirPath = testAudioRootPath + sep + subTestDirName
		downloadDir = testAudioRootSubDirPath + sep + validPlaylistDirName
		isIndexAddedToPlaylistVideo = True
		isUploadDateAddedToPlaylistVideo = True
		
		DirUtil.createTargetDirIfNotExist(rootDir=testAudioRootPath,
		                                  targetAudioDir=downloadDir)
		# deleting files in downloadDir
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManagerStub(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		downloadVideoInfoDic, indexAndDateSettingWarningMsg = audioController.getDownloadVideoInfoDicAndIndexDateSettingWarningMsg(
			playlistOrSingleVideoUrl=playlistUrl,
			playlistOrSingleVideoDownloadPath=testAudioRootSubDirPath,
			originalPlaylistTitle=playlistTitle,
			modifiedPlaylistTitle=playlistTitle,
			isIndexAddedToPlaylistVideo=isIndexAddedToPlaylistVideo,
			isUploadDateAddedToPlaylistVideo=isUploadDateAddedToPlaylistVideo)
		
		audioController.downloadVideosReferencedInPlaylist(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                   isIndexAddedToPlaylistVideo=isIndexAddedToPlaylistVideo,
		                                                   isUploadDateAddedToPlaylistVideo=isUploadDateAddedToPlaylistVideo)
		
		sys.stdout = stdout

		downloadDateTodayPrefix = datetime.datetime.today().strftime("%y%m%d") + '-'

		if os.name == 'posix':
			pass
		else:
			self.assertEqual(['downloading "' + downloadDateTodayPrefix + 'Wear a mask. Help slow the spread of Covid-19. '
 '20-07-31.mp3" audio ...',
 '',
 'video download complete.',
 '',
 'downloading "' + downloadDateTodayPrefix + 'Here to help - Give him what he wants 19-06-07.mp3" '
 'audio ...',
 '',
 'video download complete.',
 '',
 '"test_audio_downloader_two_files_with_time_frames" playlist audio(s) '
 'download terminated.',
 '',
 '',
 'extracting portions of "' + downloadDateTodayPrefix + 'Wear a mask. Help slow the spread of '
 'Covid-19. 20-07-31.mp3" ...',
 '',
 'MoviePy - Writing audio in '
 '{}\\ctr1\\test_audio_downloader_two_files_with_time_frames\\'.format(testAudioRootPath) + downloadDateTodayPrefix + 'Wear '
 'a mask. Help slow the spread of Covid-19. 20-07-31_1.mp3',
 'MoviePy - Done.',
 '\ttime frames extracted',
 '\t\t0:0:02-0:0:08',
 '',
 'suppressing portions of "' + downloadDateTodayPrefix + 'Here to help - Give him what he wants '
 '19-06-07.mp3" ...',
 '',
 'MoviePy - Writing audio in '
 '{}\\ctr1\\test_audio_downloader_two_files_with_time_frames\\'.format(testAudioRootPath) + downloadDateTodayPrefix + 'Here '
 'to help - Give him what he wants 19-06-07_s.mp3',
 'MoviePy - Done.',
 '\ttime frames suppressed:',
 '\t\t0:0:02-0:0:05',
 '\t\t0:0:07-0:0:10',
 '',
 '\ttime frames kept:',
 '\t\t0:0:00-0:0:02',
 '\t\t0:0:05-0:0:07',
 '\t\t0:0:10-0:0:15',
 '',
 '"test_audio_downloader_two_files_with_time_frames" playlist audio(s) '
 'extraction/suppression terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		createdFileLst = os.listdir(downloadDir)
		
		self.assertEqual(
			['' + downloadDateTodayPrefix + 'Here to help - Give him what he wants 19-06-07.mp3',
			 '' + downloadDateTodayPrefix + 'Here to help - Give him what he wants 19-06-07_s.mp3',
			 '' + downloadDateTodayPrefix + 'Wear a mask. Help slow the spread of Covid-19. 20-07-31.mp3',
			 '' + downloadDateTodayPrefix + 'Wear a mask. Help slow the spread of Covid-19. 20-07-31_1.mp3',
			 'test_audio_downloader_two_files_with_time_frames_dic.txt'],
			createdFileLst)
		
		# deleting clipped mp3 files in test dir to avoid uploading them on GitHub
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
	
	def testDownloadVideosReferencedInPlaylist_withTimeFrame_renaming(self):
		playlistTitle = 'test_audio_downloader_two_files_with_time_frames (e0:0:2-0:0:8) (s0:0:2-0:0:5 s0:0:7-0:0:10)'
		playlistName = 'test_audio_downloader_two_files_with_time_frames'
		playlistTitleModified = 'test_audio_downloader_two_files_with_time_frames_renamed (e0:0:2-0:0:8) (s0:0:2-0:0:5 s0:0:7-0:0:10)'
		playlistNameModified = 'test_audio_downloader_two_files_with_time_frames_renamed'
		playlistUrl = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMSFWGrRGKOypqN29MlyuQvn"
		subTestDirName = 'ctr1'
		validPlaylistDirName = DirUtil.replaceUnauthorizedDirOrFileNameChars(playlistNameModified)
		testAudioRootPath = DirUtil.getTestAudioRootPath()
		testAudioRootSubDirPath = testAudioRootPath + sep + subTestDirName
		downloadDir = testAudioRootSubDirPath + sep + validPlaylistDirName
		isIndexAddedToPlaylistVideo = True
		isUploadDateAddedToPlaylistVideo = True
		
		DirUtil.createTargetDirIfNotExist(rootDir=testAudioRootPath,
		                                  targetAudioDir=downloadDir)
		# deleting files in downloadDir
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManagerStub(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		downloadVideoInfoDic, indexAndDateSettingWarningMsg = audioController.getDownloadVideoInfoDicAndIndexDateSettingWarningMsg(
			playlistOrSingleVideoUrl=playlistUrl,
			playlistOrSingleVideoDownloadPath=testAudioRootSubDirPath,
			originalPlaylistTitle=playlistTitle,
			modifiedPlaylistTitle=playlistTitleModified,
			isIndexAddedToPlaylistVideo=isIndexAddedToPlaylistVideo,
			isUploadDateAddedToPlaylistVideo=isUploadDateAddedToPlaylistVideo)
		
		audioController.downloadVideosReferencedInPlaylist(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                   isIndexAddedToPlaylistVideo=isIndexAddedToPlaylistVideo,
		                                                   isUploadDateAddedToPlaylistVideo=isUploadDateAddedToPlaylistVideo)
		
		sys.stdout = stdout

		downloadDateTodayPrefix = datetime.datetime.today().strftime("%y%m%d") + '-'

		if os.name == 'posix':
			pass
		else:
			self.assertEqual(['downloading "' + downloadDateTodayPrefix + 'Wear a mask. Help slow the spread of Covid-19. '
 '20-07-31.mp3" audio ...',
 '',
 'video download complete.',
 '',
 'downloading "' + downloadDateTodayPrefix + 'Here to help - Give him what he wants 19-06-07.mp3" '
 'audio ...',
 '',
 'video download complete.',
 '',
 '"test_audio_downloader_two_files_with_time_frames" playlist audio(s) '
 'download terminated.',
 '',
 '',
 'extracting portions of "' + downloadDateTodayPrefix + 'Wear a mask. Help slow the spread of '
 'Covid-19. 20-07-31.mp3" ...',
 '',
 'MoviePy - Writing audio in '
 '{}\\ctr1\\test_audio_downloader_two_files_with_time_frames_renamed\\'.format(testAudioRootPath) + downloadDateTodayPrefix + 'Wear '
 'a mask. Help slow the spread of Covid-19. 20-07-31_1.mp3',
 'MoviePy - Done.',
 '\ttime frames extracted',
 '\t\t0:0:02-0:0:08',
 '',
 'suppressing portions of "' + downloadDateTodayPrefix + 'Here to help - Give him what he wants '
 '19-06-07.mp3" ...',
 '',
 'MoviePy - Writing audio in '
 '{}\\ctr1\\test_audio_downloader_two_files_with_time_frames_renamed\\'.format(testAudioRootPath) + downloadDateTodayPrefix + 'Here '
 'to help - Give him what he wants 19-06-07_s.mp3',
 'MoviePy - Done.',
 '\ttime frames suppressed:',
 '\t\t0:0:02-0:0:05',
 '\t\t0:0:07-0:0:10',
 '',
 '\ttime frames kept:',
 '\t\t0:0:00-0:0:02',
 '\t\t0:0:05-0:0:07',
 '\t\t0:0:10-0:0:15',
 '',
 '"test_audio_downloader_two_files_with_time_frames" playlist audio(s) '
 'extraction/suppression terminated.',
 '',
 ''], outputCapturingString.getvalue().split('\n'))
		
		createdFileLst = os.listdir(downloadDir)
		
		self.assertEqual(
			['' + downloadDateTodayPrefix + 'Here to help - Give him what he wants 19-06-07.mp3',
			 '' + downloadDateTodayPrefix + 'Here to help - Give him what he wants 19-06-07_s.mp3',
			 '' + downloadDateTodayPrefix + 'Wear a mask. Help slow the spread of Covid-19. 20-07-31.mp3',
			 '' + downloadDateTodayPrefix + 'Wear a mask. Help slow the spread of Covid-19. 20-07-31_1.mp3',
			 'test_audio_downloader_two_files_with_time_frames_renamed_dic.txt'],
			createdFileLst)
		
		# deleting clipped mp3 files in test dir to avoid uploading them on GitHub
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)


if __name__ == '__main__':
#	unittest.main()
	tst = TestAudioController()
	tst.testDeleteAudioFilesFromDirAndFromDic_all()
