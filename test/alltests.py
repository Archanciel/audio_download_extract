from unittest import TestLoader, TextTestRunner, TestSuite

from testguioutput import TestGuiOutput

if __name__ == "__main__":
    '''
    This test suite runs on Android in Pydroid, but fails in QPython !
    '''
    loader = TestLoader()
    suite = TestSuite((loader.loadTestsFromTestCase(TestGuiOutput),
    ))
    runner = TextTestRunner(verbosity = 2)
    runner.run(suite)
