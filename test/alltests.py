import os
from unittest import TestLoader, TextTestRunner, TestSuite

from testguioutput import TestGuiOutput
from testyoutubeaccess import TestYoutubeAccess
from testaudioextracter import TestAudioExtracter

if __name__ == "__main__":
    loader = TestLoader()
    
    if os.name == 'posix':
        # running TestGuiOutput on Android is not possible !
        suite = TestSuite((loader.loadTestsFromTestCase(TestYoutubeAccess),
        ))
    else:
        suite = TestSuite((loader.loadTestsFromTestCase(TestGuiOutput),
                    	   loader.loadTestsFromTestCase(TestYoutubeAccess),
                    	   loader.loadTestsFromTestCase(TestAudioExtracter),
        ))
        
    runner = TextTestRunner(verbosity = 2)
    runner.run(suite)
