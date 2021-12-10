import os
from unittest import TestLoader, TextTestRunner, TestSuite

from testyoutubedlaudiodownloaderdownloadmethods import TestYoutubeDlAudioDownloaderDownloadMethods
from testyoutubedlaudiodownloaderothermethods import YoutubeDlAudioDownloader
from testaudioextractor import TestAudioExtractor
from testdownloadplaylistinfodic import TestDownloadPlaylistInfoDic
from testplaylisttitleparser import TestPlaylistTitleParser
from testaudiocontroller import TestAudioController
from testyoutubedlaudiodownloaderdownloadmethodssinglevideo import TestYoutubeDlAudioDownloaderDownloadMethodsSingleVideo

if __name__ == "__main__":
    loader = TestLoader()
    
    if os.name == 'posix':
        # running TestGuiOutput on Android is not possible !
        # running TestAudioExtractor on Android is not possible !
        # running TestAudioController on Android is not possible !
        suite = TestSuite((loader.loadTestsFromTestCase(TestYoutubeDlAudioDownloaderDownloadMethods),
                           loader.loadTestsFromTestCase(YoutubeDlAudioDownloader),
                           loader.loadTestsFromTestCase(TestDownloadPlaylistInfoDic),
                           loader.loadTestsFromTestCase(TestPlaylistTitleParser),
                           loader.loadTestsFromTestCase(TestYoutubeDlAudioDownloaderDownloadMethodsSingleVideo),
                           ))
    else:
        suite = TestSuite((loader.loadTestsFromTestCase(TestYoutubeDlAudioDownloaderDownloadMethods),
                           loader.loadTestsFromTestCase(YoutubeDlAudioDownloader),
                           loader.loadTestsFromTestCase(TestAudioExtractor),
                           loader.loadTestsFromTestCase(TestDownloadPlaylistInfoDic),
                           loader.loadTestsFromTestCase(TestPlaylistTitleParser),
                           loader.loadTestsFromTestCase(TestAudioController),
                           loader.loadTestsFromTestCase(TestYoutubeDlAudioDownloaderDownloadMethodsSingleVideo),
                           ))
        
    runner = TextTestRunner(verbosity = 2)
    runner.run(suite)
