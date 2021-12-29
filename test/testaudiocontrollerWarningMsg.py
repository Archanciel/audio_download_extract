import unittest
import os, sys, inspect
from os.path import sep

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from guioutputstub import GuiOutputStub
from audiocontroller import AudioController
from configmanager import ConfigManager
from dirutil import DirUtil

class TestAudioControllerWarningMsg(unittest.TestCase):

	def testDefineIndexAndDateSettingWarning_TrueTrue_index_true_date_true(self):
		playlistTitle = 'test warning index true date true files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=True,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=True)

		self.assertEqual('', warningMsg)
	
	def testDefineIndexAndDateSettingWarning_TrueTrue_index_false_date_false(self):
		playlistTitle = 'test warning index false date false files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=True,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=True)
		
		self.assertEqual(
			'Currently, download date prefix is not used. Continue with adding download date prefix ?\nCurrently, upload date suffix is not used. Continue with adding date suffix ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_TrueTrue_index_true_date_false(self):
		playlistTitle = 'test warning index true date false files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=True,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=True)
		
		self.assertEqual(
			'Currently, upload date suffix is not used. Continue with adding date suffix ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_TrueTrue_index_false_date_true(self):
		playlistTitle = 'test warning index false date true files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=True,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=True)
		
		self.assertEqual('Currently, download date prefix is not used. Continue with adding download date prefix ?', warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseTrue_index_true_date_true(self):
		playlistTitle = 'test warning index true date true files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=False,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=True)
		
		self.assertEqual(
			'Currently, download date prefix is used. Continue without adding download date prefix ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseTrue_index_false_date_false(self):
		playlistTitle = 'test warning index false date false files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=False,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=True)
		
		self.assertEqual(
			'Currently, upload date suffix is not used. Continue with adding date suffix ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseTrue_index_true_date_false(self):
		playlistTitle = 'test warning index true date false files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=False,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=True)
		
		self.assertEqual(
			'Currently, download date prefix is used. Continue without adding download date prefix ?\nCurrently, upload date suffix is not used. Continue with adding date suffix ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseTrue_index_false_date_true(self):
		playlistTitle = 'test warning index false date true files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=False,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=True)
		
		self.assertEqual('', warningMsg)



	
	def testDefineIndexAndDateSettingWarning_TrueFalse_index_true_date_true(self):
		playlistTitle = 'test warning index true date true files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=True,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=False)
		
		self.assertEqual('Currently, upload date suffix is used. Continue without adding date suffix ?', warningMsg)
	
	def testDefineIndexAndDateSettingWarning_TrueFalse_index_false_date_false(self):
		playlistTitle = 'test warning index false date false files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=True,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=False)
		
		self.assertEqual(
			'Currently, download date prefix is not used. Continue with adding download date prefix ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_TrueFalse_index_true_date_false(self):
		playlistTitle = 'test warning index true date false files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=True,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=False)
		
		self.assertEqual(
			'',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_TrueFalse_index_false_date_true(self):
		playlistTitle = 'test warning index false date true files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=True,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=False)
		
		self.assertEqual('Currently, download date prefix is not used. Continue with adding download date prefix ?\nCurrently, upload date suffix is used. Continue without adding date suffix ?', warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseFalse_index_true_date_true(self):
		playlistTitle = 'test warning index true date true files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=False,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=False)
		
		self.assertEqual('Currently, download date prefix is used. Continue without adding download date prefix ?\nCurrently, upload date suffix is used. Continue without adding date suffix ?', warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseFalse_index_false_date_false(self):
		playlistTitle = 'test warning index false date false files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=False,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=False)
		
		self.assertEqual(
			'',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseFalse_index_true_date_false(self):
		playlistTitle = 'test warning index true date false files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=False,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=False)
		
		self.assertEqual(
			'Currently, download date prefix is used. Continue without adding download date prefix ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseFalse_index_false_date_true(self):
		playlistTitle = 'test warning index false date true files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=False,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=False)
		
		self.assertEqual('Currently, upload date suffix is used. Continue without adding date suffix ?', warningMsg)
	
	def testDefineIndexAndDateSettingWarning_TrueTrue_emptyDir(self):
		playlistTitle = 'test warning index empty dir'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=True,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=True)
		
		self.assertEqual(
			'Playlist directory is empty. Continue with adding download date prefix and upload date suffix ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_TrueFalse_emptyDir(self):
		playlistTitle = 'test warning index empty dir'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=True,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=False)
		
		self.assertEqual(
			'Playlist directory is empty. Continue with adding download date prefix ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseTrue_emptyDir(self):
		playlistTitle = 'test warning index empty dir'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=False,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=True)
		
		self.assertEqual(
			'Playlist directory is empty. Continue with adding upload date suffix ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseFalse_emptyDir(self):
		playlistTitle = 'test warning index empty dir'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=False,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=False)
		
		self.assertEqual(
			'',
			warningMsg)
#hhhh
	
	def testDefineIndexAndDateSettingWarning_TrueTrue_dirNotExist(self):
		playlistTitle = 'test warning index dir not exist'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=True,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=True)
		
		self.assertEqual(
			'Playlist directory does not exist. Continue with adding download date prefix and upload date suffix ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_TrueFalse_dirNotExist(self):
		playlistTitle = 'test warning index dir not exist'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=True,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=False)
		
		self.assertEqual(
			'Playlist directory does not exist. Continue with adding download date prefix ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseTrue_dirNotExist(self):
		playlistTitle = 'test warning index dir not exist'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=False,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=True)
		
		self.assertEqual(
			'Playlist directory does not exist. Continue with adding upload date suffix ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseFalse_dirNotExist(self):
		playlistTitle = 'test warning index dir not exist'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPathForTest() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isDownloadDatePrefixAddedToPlaylistVideo=False,
		                                                                 isUploadDateSuffixAddedToPlaylistVideo=False)
		
		self.assertEqual(
			'',
			warningMsg)


if __name__ == '__main__':
#	unittest.main()
	tst = TestAudioControllerWarningMsg()
	tst.testDefineIndexAndDateSettingWarning_FalseFalse_index_false_date_true()
