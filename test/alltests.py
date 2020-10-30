import os
from unittest import TestLoader, TextTestRunner, TestSuite

from testyoutubedlaudiodownloaderdownloadmethods import TestYoutubeDlAudioDownloaderDownloadMethods
from testyoutubedlaudiodownloaderothermethods import YoutubeDlAudioDownloader
from testaudioextractor import TestAudioExtractor
from testdownloadvideoinfodic import TestDownloadVideoInfoDic
from testplaylisttitleparser import TestPlaylistTitleParser
from testaudiocontroller import TestAudioController

if __name__ == "__main__":
    loader = TestLoader()
    
    if os.name == 'posix':
        # running TestGuiOutput on Android is not possible !
        # running TestAudioExtractor on Android is not possible !
        # running TestAudioController on Android is not possible !
        suite = TestSuite((loader.loadTestsFromTestCase(TestYoutubeDlAudioDownloaderDownloadMethods),
                           loader.loadTestsFromTestCase(YoutubeDlAudioDownloader),
                           loader.loadTestsFromTestCase(TestDownloadVideoInfoDic),
                           loader.loadTestsFromTestCase(TestPlaylistTitleParser),
                           ))
    else:
        suite = TestSuite((loader.loadTestsFromTestCase(TestYoutubeDlAudioDownloaderDownloadMethods),
                           loader.loadTestsFromTestCase(YoutubeDlAudioDownloader),
                           loader.loadTestsFromTestCase(TestAudioExtractor),
                           loader.loadTestsFromTestCase(TestDownloadVideoInfoDic),
                           loader.loadTestsFromTestCase(TestPlaylistTitleParser),
                           loader.loadTestsFromTestCase(TestAudioController),
                           ))
        
    runner = TextTestRunner(verbosity = 2)
    runner.run(suite)
