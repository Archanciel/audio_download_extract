import os
from unittest import TestLoader, TextTestRunner, TestSuite

from testguioutput import TestGuiOutput
from testyoutubeaudiodownloaderdownloadmethods import TestYoutubeAudioDownloaderDownloadMethods
from testyoutubeaudiodownloaderothermethods import TestYoutubeAudioDownloaderOtherMethods
from testaudioextractor import TestAudioExtractor
from testdownloadedvideoinfodic import TestDownloadedVideoInfoDic
from testplaylisttitleparser import TestPlaylistTitleParser
from testaudiocontroller import TestAudioController

if __name__ == "__main__":
    loader = TestLoader()
    
    if os.name == 'posix':
        # running TestGuiOutput on Android is not possible !
        # running TestAudioExtractor on Android is not possible !
        suite = TestSuite((loader.loadTestsFromTestCase(TestYoutubeAudioDownloaderDownloadMethods),
                           loader.loadTestsFromTestCase(TestYoutubeAudioDownloaderOtherMethods),
                           loader.loadTestsFromTestCase(TestDownloadedVideoInfoDic),
                           loader.loadTestsFromTestCase(TestPlaylistTitleParser),
                           ))
    else:
        suite = TestSuite((loader.loadTestsFromTestCase(TestGuiOutput),
                    	   loader.loadTestsFromTestCase(TestYoutubeAudioDownloaderDownloadMethods),
                           loader.loadTestsFromTestCase(TestYoutubeAudioDownloaderOtherMethods),
                           loader.loadTestsFromTestCase(TestAudioExtractor),
                           loader.loadTestsFromTestCase(TestDownloadedVideoInfoDic),
                           loader.loadTestsFromTestCase(TestPlaylistTitleParser),
                           loader.loadTestsFromTestCase(TestAudioController),
                           ))
        
    runner = TextTestRunner(verbosity = 2)
    runner.run(suite)
