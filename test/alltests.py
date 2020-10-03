import os
from unittest import TestLoader, TextTestRunner, TestSuite

from testguioutput import TestGuiOutput
from testyoutubeaccessdownloadmethods import TestYoutubeAccessDownloadMethods
from testyoutubeaccessothermethods import TestYoutubeAccessOtherMethods
from testaudioextractor import TestAudioExtractor
from testdownloadedvideoinfodic import TestDownloadedVideoInfoDic
from testplaylisttimeframedata import TestPlaylistTimeFrameData

if __name__ == "__main__":
    loader = TestLoader()
    
    if os.name == 'posix':
        # running TestGuiOutput on Android is not possible !
        # running TestAudioExtractor on Android is not possible !
        suite = TestSuite((loader.loadTestsFromTestCase(TestYoutubeAccessDownloadMethods),
                           loader.loadTestsFromTestCase(TestYoutubeAccessOtherMethods),
                           loader.loadTestsFromTestCase(TestDownloadedVideoInfoDic),
                           loader.loadTestsFromTestCase(TestPlaylistTimeFrameData),
                           ))
    else:
        suite = TestSuite((loader.loadTestsFromTestCase(TestGuiOutput),
                    	   loader.loadTestsFromTestCase(TestYoutubeAccessDownloadMethods),
                           loader.loadTestsFromTestCase(TestYoutubeAccessOtherMethods),
                           loader.loadTestsFromTestCase(TestAudioExtractor),
                           loader.loadTestsFromTestCase(TestDownloadedVideoInfoDic),
                           loader.loadTestsFromTestCase(TestPlaylistTimeFrameData),
                           ))
        
    runner = TextTestRunner(verbosity = 2)
    runner.run(suite)
