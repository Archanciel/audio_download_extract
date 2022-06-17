import shutil
import unittest
import os, sys, inspect, glob
from os.path import sep
from datetime import datetime
from io import StringIO

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)
		
from downloadUrlinfodic import DownloadUrlInfoDic
from urldownloaddata import UrlDownloadData
from constants import *
from dirutil import DirUtil
			
class TestDownloadUrlInfoDic(unittest.TestCase):
	
	def testAddUrlInfoForPlaylistOrVideo_new_DownloadUrlInfoDic_file(self):
		audioDirRoot = DirUtil.getTestAudioRootPath()
		downloadDir = audioDirRoot + sep + 'tst_url_info_dic_1'
		urlDicFileName = 'urlListDic'

		if not os.path.exists(downloadDir):
			os.mkdir(downloadDir)
		
		# deleting url info dic file
		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
		
		dui = DownloadUrlInfoDic(
			audioRootDir=audioDirRoot,
			urlListDicFileName=urlDicFileName,
			generalTotalDownlResultTuple=(13, 4, 7),
			generalTotalDownlSuccessTuple=(3, 5, 1, 1, 2),
			generalTotalDownlFailTuple=(0, 2, 0, 0, 2),
			generalTotalDownlSkipTuple=(1, 2, 0, 0, 4),
			loadDicIfDicFileExist=True,
			existingDicFilePathName=None)
		
		# adding 11 url info in order to test
		# DownloadUrlInfoDic.getSortedUrlIndexLst()
		
		urlTitle_1 = 'test warning index date files_noIndexNoDate'
		url_1 = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRVKblKqskAyseCgsUmhlSc'
		dui.addUrlInfo(urlType=DownloadUrlInfoDic.URL_TYPE_PLAYLIST,
		               urlTitle=urlTitle_1,
		               url=url_1,
		               downloadDir='C:\\Users\\Jean-Pierre\\Downloads\\Audio\\Christophe A')
		urlTitle_2 = 'Here to help: Give him what he wants'
		url_2 = 'https://www.youtube.com/watch?v=Eqy6M6qLWGw'
		dui.addUrlInfo(urlType=DownloadUrlInfoDic.URL_TYPE_SINGLE_VIDEO,
		               urlTitle=urlTitle_2,
		               url=url_2,
		               downloadDir='C:\\Users\\Jean-Pierre\\Downloads\\Audio\\other dir')

		urlTitle_3 = 'Here to help: Give him what he wants_3'
		url_3 = 'https://www.youtube.com/watch?v=Eqy6M6qLWGw'
		dui.addUrlInfo(urlType=DownloadUrlInfoDic.URL_TYPE_SINGLE_VIDEO,
		               urlTitle=urlTitle_3,
		               url=url_3,
		               downloadDir='')

		urlTitle_4 = 'Here to help: Give him what he wants_4'
		url_4 = 'https://www.youtube.com/watch?v=Eqy6M6qLWGw'
		dui.addUrlInfo(urlType=DownloadUrlInfoDic.URL_TYPE_SINGLE_VIDEO,
		               urlTitle=urlTitle_4,
		               url=url_4,
		               downloadDir='')

		urlTitle_5 = 'Here to help: Give him what he wants_5'
		url_5 = 'https://www.youtube.com/watch?v=Eqy6M6qLWGw'
		dui.addUrlInfo(urlType=DownloadUrlInfoDic.URL_TYPE_SINGLE_VIDEO,
		               urlTitle=urlTitle_5,
		               url=url_5,
		               downloadDir='')

		urlTitle_6 = 'Here to help: Give him what he wants_6'
		url_6 = 'https://www.youtube.com/watch?v=Eqy6M6qLWGw'
		dui.addUrlInfo(urlType=DownloadUrlInfoDic.URL_TYPE_SINGLE_VIDEO,
		               urlTitle=urlTitle_6,
		               url=url_6,
		               downloadDir='')

		urlTitle_7 = 'Here to help: Give him what he wants_7'
		url_7 = 'https://www.youtube.com/watch?v=Eqy6M6qLWGw'
		dui.addUrlInfo(urlType=DownloadUrlInfoDic.URL_TYPE_SINGLE_VIDEO,
		               urlTitle=urlTitle_7,
		               url=url_7,
		               downloadDir='')

		urlTitle_8 = 'Here to help: Give him what he wants_8'
		url_8 = 'https://www.youtube.com/watch?v=Eqy6M6qLWGw'
		dui.addUrlInfo(urlType=DownloadUrlInfoDic.URL_TYPE_SINGLE_VIDEO,
		               urlTitle=urlTitle_8,
		               url=url_8,
		               downloadDir='')

		urlTitle_9 = 'Here to help: Give him what he wants_9'
		url_9 = 'https://www.youtube.com/watch?v=Eqy6M6qLWGw'
		dui.addUrlInfo(urlType=DownloadUrlInfoDic.URL_TYPE_SINGLE_VIDEO,
		               urlTitle=urlTitle_9,
		               url=url_9,
		               downloadDir='')

		urlTitle_10 = 'Here to help: Give him what he wants_10'
		url_10 = 'https://www.youtube.com/watch?v=Eqy6M6qLWGw'
		dui.addUrlInfo(urlType=DownloadUrlInfoDic.URL_TYPE_SINGLE_VIDEO,
		               urlTitle=urlTitle_10,
		               url=url_10,
		               downloadDir='')

		urlTitle_11 = 'Here to help: Give him what he wants_11'
		url_11 = 'https://www.youtube.com/watch?v=Eqy6M6qLWGw'
		dui.addUrlInfo(urlType=DownloadUrlInfoDic.URL_TYPE_SINGLE_VIDEO,
		               urlTitle=urlTitle_11,
		               url=url_11,
		               downloadDir='')

		dui.saveDic(downloadDir)
		
		additionTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_DOWNLOAD_DIC_FILE)

		
		self.assertEqual(url_1, dui.getUrlForUrlTitle(urlTitle_1))
		self.assertEqual(url_1, dui.getUrlForUrlIndex(1))
		self.assertEqual(url_1, dui.getUrlForUrlKey('1'))
		self.assertEqual(url_2, dui.getUrlForUrlTitle(urlTitle_2))
		self.assertEqual(url_2, dui.getUrlForUrlIndex(2))
		self.assertEqual(url_2, dui.getUrlForUrlKey('2'))
		self.assertEqual(url_10, dui.getUrlForUrlIndex(10))
		self.assertEqual(url_10, dui.getUrlForUrlKey('10'))
		self.assertEqual(urlTitle_10, dui.getUrlTitleForUrlIndex(10))
		
		self.assertEqual(DownloadUrlInfoDic.URL_TYPE_PLAYLIST, dui.getUrlTypeForUrlIndex(1))
		self.assertEqual(DownloadUrlInfoDic.URL_TYPE_SINGLE_VIDEO, dui.getUrlTypeForUrlIndex(2))

		self.assertEqual(urlDicFileName, dui.getUrlListDicFileName())
		
		self.assertEqual([1,2,3,4,5,6,7,8,9,10,11], dui.getSortedUrlIndexLst())
		
		self.assertEqual(additionTimeStr, dui.getVideoDownloadTimeForVideoTitle(urlTitle_1))
		self.assertEqual(additionTimeStr, dui.getVideoDownloadTimeForVideoTitle(urlTitle_2))

		self.assertEqual(urlTitle_1, dui.getUrlTitleForUrlIndex(1))

		self.assertEqual('C:\\Users\\Jean-Pierre\\Downloads\\Audio\\Christophe A', dui.getUrlDownloadDirForUrlIndex(1))
		self.assertEqual('C:\\Users\\Jean-Pierre\\Downloads\\Audio\\Christophe A', dui.getUrlDownloadDirForUrlTitle(urlTitle_1))
		self.assertEqual('C:\\Users\\Jean-Pierre\\Downloads\\Audio\\other dir', dui.getUrlDownloadDirForUrlIndex(2))
		self.assertEqual('C:\\Users\\Jean-Pierre\\Downloads\\Audio\\other dir', dui.getUrlDownloadDirForUrlTitle(urlTitle_2))
		
		self.assertEqual(12, dui.getNextUrlIndex())
		
		udl = dui.getUrlDownloadDataForUrlIndex(1)
		
		self.assertEqual(DownloadUrlInfoDic.URL_TYPE_PLAYLIST, udl.type)
		self.assertEqual(urlTitle_1, udl.title)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		for udl in dui.getAllUrlDownloadDataSortedList():
			print(udl)
		
		sys.stdout = stdout

		self.assertEqual(['playlist, C:\\Users\\Jean-Pierre\\Downloads\\Audio\\Christophe A\\test warning index date files_noIndexNoDate, '
 'https://youtube.com/playlist?list=PLzwWSJNcZTMRVKblKqskAyseCgsUmhlSc',
 'video, C:\\Users\\Jean-Pierre\\Downloads\\Audio\\other dir\\Here to help: Give him what he wants, '
 'https://www.youtube.com/watch?v=Eqy6M6qLWGw',
 'video, Here to help: Give him what he wants_3, '
 'https://www.youtube.com/watch?v=Eqy6M6qLWGw',
 'video, Here to help: Give him what he wants_4, '
 'https://www.youtube.com/watch?v=Eqy6M6qLWGw',
 'video, Here to help: Give him what he wants_5, '
 'https://www.youtube.com/watch?v=Eqy6M6qLWGw',
 'video, Here to help: Give him what he wants_6, '
 'https://www.youtube.com/watch?v=Eqy6M6qLWGw',
 'video, Here to help: Give him what he wants_7, '
 'https://www.youtube.com/watch?v=Eqy6M6qLWGw',
 'video, Here to help: Give him what he wants_8, '
 'https://www.youtube.com/watch?v=Eqy6M6qLWGw',
 'video, Here to help: Give him what he wants_9, '
 'https://www.youtube.com/watch?v=Eqy6M6qLWGw',
 'video, Here to help: Give him what he wants_10, '
 'https://www.youtube.com/watch?v=Eqy6M6qLWGw',
 'video, Here to help: Give him what he wants_11, '
 'https://www.youtube.com/watch?v=Eqy6M6qLWGw',
 ''], outputCapturingString.getvalue().split('\n'))

		dicFilePathNameLst = DirUtil.getFilePathNamesInDirForPattern(downloadDir, '*' + DownloadUrlInfoDic.DIC_FILE_NAME_EXTENT)
		dui_reloaded = DownloadUrlInfoDic(existingDicFilePathName=dicFilePathNameLst[0])
		
		self.assertEqual(url_1, dui_reloaded.getUrlForUrlTitle(urlTitle_1))
		self.assertEqual(url_1, dui_reloaded.getUrlForUrlIndex(1))
		self.assertEqual(url_1, dui_reloaded.getUrlForUrlKey('1'))
		self.assertEqual(url_2, dui_reloaded.getUrlForUrlTitle(urlTitle_2))
		self.assertEqual(url_2, dui_reloaded.getUrlForUrlIndex(2))
		self.assertEqual(url_2, dui_reloaded.getUrlForUrlKey('2'))
		self.assertEqual(url_10, dui_reloaded.getUrlForUrlIndex(10))
		self.assertEqual(url_10, dui_reloaded.getUrlForUrlKey('10'))
		self.assertEqual(urlTitle_10, dui_reloaded.getUrlTitleForUrlIndex(10))

		self.assertEqual('C:\\Users\\Jean-Pierre\\Downloads\\Audio\\Christophe A', dui_reloaded.getUrlDownloadDirForUrlIndex(1))
		self.assertEqual('C:\\Users\\Jean-Pierre\\Downloads\\Audio\\Christophe A', dui_reloaded.getUrlDownloadDirForUrlTitle(urlTitle_1))
		self.assertEqual('C:\\Users\\Jean-Pierre\\Downloads\\Audio\\other dir', dui_reloaded.getUrlDownloadDirForUrlIndex(2))
		self.assertEqual('C:\\Users\\Jean-Pierre\\Downloads\\Audio\\other dir', dui_reloaded.getUrlDownloadDirForUrlTitle(urlTitle_2))

		self.assertEqual(DownloadUrlInfoDic.URL_TYPE_PLAYLIST, dui_reloaded.getUrlTypeForUrlIndex(1))
		self.assertEqual(DownloadUrlInfoDic.URL_TYPE_SINGLE_VIDEO, dui_reloaded.getUrlTypeForUrlIndex(2))

		self.assertEqual(urlDicFileName, dui_reloaded.getUrlListDicFileName())

		self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], dui_reloaded.getSortedUrlIndexLst())
		
		self.assertEqual(additionTimeStr, dui_reloaded.getVideoDownloadTimeForVideoTitle(urlTitle_1))
		self.assertEqual(additionTimeStr, dui_reloaded.getVideoDownloadTimeForVideoTitle(urlTitle_2))
		
		self.assertEqual(urlTitle_1, dui_reloaded.getUrlTitleForUrlIndex(1))
		
		self.assertEqual('C:\\Users\\Jean-Pierre\\Downloads\\Audio\\Christophe A', dui.getUrlDownloadDirForUrlIndex(1))
		self.assertEqual('C:\\Users\\Jean-Pierre\\Downloads\\Audio\\Christophe A', dui_reloaded.getUrlDownloadDirForUrlTitle(urlTitle_1))
		self.assertEqual('C:\\Users\\Jean-Pierre\\Downloads\\Audio\\other dir', dui_reloaded.getUrlDownloadDirForUrlIndex(2))
		self.assertEqual('C:\\Users\\Jean-Pierre\\Downloads\\Audio\\other dir', dui_reloaded.getUrlDownloadDirForUrlTitle(urlTitle_2))
		
		self.assertEqual(12, dui_reloaded.getNextUrlIndex())
		
		udl = dui_reloaded.getUrlDownloadDataForUrlIndex(1)
		
		self.assertEqual(DownloadUrlInfoDic.URL_TYPE_PLAYLIST, udl.type)
		self.assertEqual(urlTitle_1, udl.title)
		self.assertEqual('C:\\Users\\Jean-Pierre\\Downloads\\Audio\\Christophe A', udl.downloadDir)
		
		udl = dui_reloaded.getUrlDownloadDataForUrlIndex(2)
		
		self.assertEqual(DownloadUrlInfoDic.URL_TYPE_SINGLE_VIDEO, udl.type)
		self.assertEqual(urlTitle_2, udl.title)
		self.assertEqual('C:\\Users\\Jean-Pierre\\Downloads\\Audio\\other dir', udl.downloadDir)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		for udl in dui_reloaded.getAllUrlDownloadDataSortedList():
			print(udl)
		
		sys.stdout = stdout
		
		self.assertEqual(['playlist, C:\\Users\\Jean-Pierre\\Downloads\\Audio\\Christophe A\\test warning index date files_noIndexNoDate, '
		                  'https://youtube.com/playlist?list=PLzwWSJNcZTMRVKblKqskAyseCgsUmhlSc',
		                  'video, C:\\Users\\Jean-Pierre\\Downloads\\Audio\\other dir\\Here to help: Give him what he wants, '
		                  'https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                  'video, Here to help: Give him what he wants_3, '
		                  'https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                  'video, Here to help: Give him what he wants_4, '
		                  'https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                  'video, Here to help: Give him what he wants_5, '
		                  'https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                  'video, Here to help: Give him what he wants_6, '
		                  'https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                  'video, Here to help: Give him what he wants_7, '
		                  'https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                  'video, Here to help: Give him what he wants_8, '
		                  'https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                  'video, Here to help: Give him what he wants_9, '
		                  'https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                  'video, Here to help: Give him what he wants_10, '
		                  'https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                  'video, Here to help: Give him what he wants_11, '
		                  'https://www.youtube.com/watch?v=Eqy6M6qLWGw',
		                  ''], outputCapturingString.getvalue().split('\n'))

		# deleting files in test dir so that it is not uploaded on GitHub

		files = glob.glob(downloadDir + sep + '*')
		
		for f in files:
			os.remove(f)
	
	def testLoadExistingDownloadUrlInfoDic_specifying_only_info_dic_filePathName(self):
		audioDirRoot = DirUtil.getTestAudioRootPath()
		downloadDir = audioDirRoot + sep + 'tst_url_info_dic_2'
		testDirNameSaved = downloadDir + sep + 'save'

		# deleting files in downloadDir
		
		DirUtil.deleteFilesInDirForPattern(downloadDir, '*')
		
		# restoring dic file
		
		DirUtil.copyFilesInDirToDirForPattern(sourceDir=testDirNameSaved,
		                                      targetDir=downloadDir,
		                                      fileNamePattern='*')

		urlTitle_1 = 'test warning index date files_noIndexNoDate'
		url_1 = 'https://youtube.com/playlist?list=PLzwWSJNcZTMRVKblKqskAyseCgsUmhlSc'
		urlTitle_2 = 'Here to help: Give him what he wants'
		url_2 = 'https://www.youtube.com/watch?v=Eqy6M6qLWGw'
		
		dicFilePathNameLst = DirUtil.getFilePathNamesInDirForPattern(downloadDir, '*' + DownloadUrlInfoDic.DIC_FILE_NAME_EXTENT)
		dui = DownloadUrlInfoDic(existingDicFilePathName=dicFilePathNameLst[0])
		
		self.assertEqual(url_1, dui.getUrlForUrlTitle(urlTitle_1))
		self.assertEqual(url_1, dui.getUrlForUrlIndex(1))
		self.assertEqual(url_1, dui.getUrlForUrlKey('1'))
		self.assertEqual(url_2, dui.getUrlForUrlTitle(urlTitle_2))
		self.assertEqual(url_2, dui.getUrlForUrlIndex(2))
		self.assertEqual(url_2, dui.getUrlForUrlKey('2'))

		additionTimeStr = '14/12/2021 18:30:55'
		self.assertEqual(additionTimeStr, dui.getVideoDownloadTimeForVideoTitle(urlTitle_1))
		self.assertEqual(additionTimeStr, dui.getVideoDownloadTimeForVideoTitle(urlTitle_2))
		
		self.assertEqual(urlTitle_1, dui.getUrlTitleForUrlIndex(1))
		
		self.assertEqual('', dui.getUrlDownloadDirForUrlIndex(1))
		self.assertEqual('', dui.getUrlDownloadDirForUrlTitle(urlTitle_1))
		self.assertEqual('', dui.getUrlDownloadDirForUrlIndex(2))
		self.assertEqual('', dui.getUrlDownloadDirForUrlTitle(urlTitle_2))
		
		self.assertEqual(3, dui.getNextUrlIndex())

		# deleting files in test dir so that it is not uploaded on GitHub
		DirUtil.deleteFilesInDirForPattern(downloadDir, '*')


if __name__ == '__main__':
#	unittest.main()
	tst = TestDownloadUrlInfoDic()
	tst.testDeleteVideoInfoForVideoFileName()
