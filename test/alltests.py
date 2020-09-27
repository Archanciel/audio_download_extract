import os
from unittest import TestLoader, TextTestRunner, TestSuite

from testguioutput import TestGuiOutput
from testaudiodownloader import TestAudioDownloader
from testaudioextracter import TestAudioExtracter

if __name__ == "__main__":
    loader = TestLoader()
    
    if os.name == 'posix':
        # running TestGuiOutput on Android is not possible !
        suite = TestSuite((loader.loadTestsFromTestCase(TestAudioDownloader),
        ))
    else:
        suite = TestSuite((loader.loadTestsFromTestCase(TestGuiOutput),
                    	   loader.loadTestsFromTestCase(TestAudioDownloader),
                    	   loader.loadTestsFromTestCase(TestAudioExtracter),
        ))
        
    runner = TextTestRunner(verbosity = 2)
    runner.run(suite)
