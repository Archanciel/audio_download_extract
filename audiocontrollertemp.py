import os


class AudioControllerTemp:
    '''
    Instanciate the app components and
    control the rep loop
    :seqdiag_note Entry point of the business layer
    '''
    def __init__(self, configMgr):
        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptopricer.ini'
        else:
            FILE_PATH = 'c:\\temp\\cryptopricer.ini'

        self.configMgr = configMgr


    def getPrintableResultForInput(self, inputStr, copyResultToClipboard=True):
        '''
        Return the printable request result, the full request command without any command option and
        the full request command with any specified save mode option (option which is to be saved in the
        command history list.

        :param inputStr:
        :param copyResultToClipboard: set to True by default. Whreplaying all requests
                                      stored in history, set to False, which avoids
                                      problem on Android
        :seqdiag_return printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions

        :return: 1/ printable request result
                 2/ full request command without any command option
                 3/ full request command with any non save command option
                 4/ full request command with any specified save mode option, None if no save mode option
                    is in effect

                 Ex: 1/ 0.1 ETH/36 USD on Bitfinex: 21/11/17 10:00 360
                     2/ eth usd 0 bitfinex
                     3/ None (value command with save mode in effect !)
                     4/ eth usd 0 bitfinex -vs0.1eth

                     1/ 0.1 ETH/36 USD on Bitfinex: 21/11/17 10:00 360
                     2/ eth usd 0 bitfinex
                     3/ eth usd 0 bitfinex -v0.1eth
                     4/ None (no value command save option in effect)

                     1/ ETH/USD on Bitfinex: 21/11/17 10:00 360
                     2/ eth usd 0 bitfinex
                     3/ None (no value command in effect)
                     4/ None (no value command save option in effect)
        '''
        return 'printResult', 'fullCommandStrNoOptions', 'fullCommandStrWithOptions', 'fullCommandStrWithSaveModeOptions', 'fullCommandStrForStatusBar'


if __name__ == '__main__':
    pass