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
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=True,
		                                                                 isUploadDateAddedToPlaylistVideo=True)

		self.assertEqual('', warningMsg)
	
	def testDefineIndexAndDateSettingWarning_TrueTrue_index_false_date_false(self):
		playlistTitle = 'test warning index false date false files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=True,
		                                                                 isUploadDateAddedToPlaylistVideo=True)
		
		self.assertEqual(
			'Currently, index is not used. Continue with adding index ?\nCurrently, upload date is not used. Continue with adding date ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_TrueTrue_index_true_date_false(self):
		playlistTitle = 'test warning index true date false files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=True,
		                                                                 isUploadDateAddedToPlaylistVideo=True)
		
		self.assertEqual(
			'Currently, upload date is not used. Continue with adding date ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_TrueTrue_index_false_date_true(self):
		playlistTitle = 'test warning index false date true files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=True,
		                                                                 isUploadDateAddedToPlaylistVideo=True)
		
		self.assertEqual('Currently, index is not used. Continue with adding index ?', warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseTrue_index_true_date_true(self):
		playlistTitle = 'test warning index true date true files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=False,
		                                                                 isUploadDateAddedToPlaylistVideo=True)
		
		self.assertEqual(
			'Currently, index is used. Continue without adding index ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseTrue_index_false_date_false(self):
		playlistTitle = 'test warning index false date false files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=False,
		                                                                 isUploadDateAddedToPlaylistVideo=True)
		
		self.assertEqual(
			'Currently, upload date is not used. Continue with adding date ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseTrue_index_true_date_false(self):
		playlistTitle = 'test warning index true date false files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=False,
		                                                                 isUploadDateAddedToPlaylistVideo=True)
		
		self.assertEqual(
			'Currently, index is used. Continue without adding index ?\nCurrently, upload date is not used. Continue with adding date ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseTrue_index_false_date_true(self):
		playlistTitle = 'test warning index false date true files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=False,
		                                                                 isUploadDateAddedToPlaylistVideo=True)
		
		self.assertEqual('', warningMsg)



	
	def testDefineIndexAndDateSettingWarning_TrueFalse_index_true_date_true(self):
		playlistTitle = 'test warning index true date true files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=True,
		                                                                 isUploadDateAddedToPlaylistVideo=False)
		
		self.assertEqual('Currently, upload date is used. Continue without adding date ?', warningMsg)
	
	def testDefineIndexAndDateSettingWarning_TrueFalse_index_false_date_false(self):
		playlistTitle = 'test warning index false date false files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=True,
		                                                                 isUploadDateAddedToPlaylistVideo=False)
		
		self.assertEqual(
			'Currently, index is not used. Continue with adding index ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_TrueFalse_index_true_date_false(self):
		playlistTitle = 'test warning index true date false files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=True,
		                                                                 isUploadDateAddedToPlaylistVideo=False)
		
		self.assertEqual(
			'',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_TrueFalse_index_false_date_true(self):
		playlistTitle = 'test warning index false date true files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=True,
		                                                                 isUploadDateAddedToPlaylistVideo=False)
		
		self.assertEqual('Currently, index is not used. Continue with adding index ?\nCurrently, upload date is used. Continue without adding date ?', warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseFalse_index_true_date_true(self):
		playlistTitle = 'test warning index true date true files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=False,
		                                                                 isUploadDateAddedToPlaylistVideo=False)
		
		self.assertEqual('Currently, index is used. Continue without adding index ?\nCurrently, upload date is used. Continue without adding date ?', warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseFalse_index_false_date_false(self):
		playlistTitle = 'test warning index false date false files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=False,
		                                                                 isUploadDateAddedToPlaylistVideo=False)
		
		self.assertEqual(
			'',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseFalse_index_true_date_false(self):
		playlistTitle = 'test warning index true date false files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=False,
		                                                                 isUploadDateAddedToPlaylistVideo=False)
		
		self.assertEqual(
			'Currently, index is used. Continue without adding index ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseFalse_index_false_date_true(self):
		playlistTitle = 'test warning index false date true files'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=False,
		                                                                 isUploadDateAddedToPlaylistVideo=False)
		
		self.assertEqual('Currently, upload date is used. Continue without adding date ?', warningMsg)
	
	def testDefineIndexAndDateSettingWarning_TrueTrue_emptyDir(self):
		playlistTitle = 'test warning index empty dir'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=True,
		                                                                 isUploadDateAddedToPlaylistVideo=True)
		
		self.assertEqual(
			'Playlist directory is empty. Continue with adding index and upload date ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_TrueFalse_emptyDir(self):
		playlistTitle = 'test warning index empty dir'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=True,
		                                                                 isUploadDateAddedToPlaylistVideo=False)
		
		self.assertEqual(
			'Playlist directory is empty. Continue with adding index ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseTrue_emptyDir(self):
		playlistTitle = 'test warning index empty dir'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=False,
		                                                                 isUploadDateAddedToPlaylistVideo=True)
		
		self.assertEqual(
			'Playlist directory is empty. Continue with adding upload date ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseFalse_emptyDir(self):
		playlistTitle = 'test warning index empty dir'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=False,
		                                                                 isUploadDateAddedToPlaylistVideo=False)
		
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
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=True,
		                                                                 isUploadDateAddedToPlaylistVideo=True)
		
		self.assertEqual(
			'Playlist directory does not exist. Continue with adding index and upload date ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_TrueFalse_dirNotExist(self):
		playlistTitle = 'test warning index dir not exist'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=True,
		                                                                 isUploadDateAddedToPlaylistVideo=False)
		
		self.assertEqual(
			'Playlist directory does not exist. Continue with adding index ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseTrue_dirNotExist(self):
		playlistTitle = 'test warning index dir not exist'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=False,
		                                                                 isUploadDateAddedToPlaylistVideo=True)
		
		self.assertEqual(
			'Playlist directory does not exist. Continue with adding upload date ?',
			warningMsg)
	
	def testDefineIndexAndDateSettingWarning_FalseFalse_dirNotExist(self):
		playlistTitle = 'test warning index dir not exist'
		
		testAudioDirRoot = DirUtil.getTestAudioRootPath()
		guiOutput = GuiOutputStub()
		audioController = AudioController(guiOutput,
		                                  ConfigManager(
			                                  DirUtil.getDefaultAudioRootPath() + sep + 'audiodownloader.ini'))
		
		downloadVideoInfoDic = \
			audioController.getDownloadVideoInfoDicForPlaylistTitle(playlistUrl='',  # not usefull
			                                                        playlistOrSingleVideoDownloadPath=testAudioDirRoot,
			                                                        originalPlaylistTitle=playlistTitle,
			                                                        modifiedPlaylistTitle=playlistTitle)
		
		warningMsg = audioController.defineIndexAndDateSettingWarningMsg(downloadVideoInfoDic=downloadVideoInfoDic,
		                                                                 isIndexAddedToPlaylistVideo=False,
		                                                                 isUploadDateAddedToPlaylistVideo=False)
		
		self.assertEqual(
			'',
			warningMsg)


if __name__ == '__main__':
#	unittest.main()
	tst = TestAudioControllerWarningMsg()
	tst.testDefineIndexAndDateSettingWarning_TrueTrue_index_false_date_false()
