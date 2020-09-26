from unittest import TestLoader, TextTestRunner, TestSuite

from testguioutput import TestGuiOutput
from testaudiodownloader import TestAudioDownloader

if __name__ == "__main__":
    '''
    This test suite runs on Android in Pydroid, but fails in QPython !
    '''
    loader = TestLoader()
    suite = TestSuite((loader.loadTestsFromTestCase(TestGuiOutput),
                       loader.loadTestsFromTestCase(TestAudioDownloader),
    ))
    runner = TextTestRunner(verbosity = 2)
    runner.run(suite)
