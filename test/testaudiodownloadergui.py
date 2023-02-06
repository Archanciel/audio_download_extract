import unittest

from gui.audiodownloadergui import AudioDownloaderGUI

class TestAudioDownloaderGUI(unittest.TestCase):
    def setUp(self):
        self.calculator = AudioDownloaderGUI()

    def test_increasePlaylistVideoDownloadNumber(self):
        self.calculator.increasePlaylistVideoDownloadNumber("playlist1")
        self.assertEqual(self.calculator.partiallyDownloadedPlaylistDic, {"playlist1": 1})

        self.calculator.increasePlaylistVideoDownloadNumber("playlist2")
        self.assertEqual(self.calculator.partiallyDownloadedPlaylistDic, {"playlist1": 1, "playlist2": 1})

        self.calculator.increasePlaylistVideoDownloadNumber("playlist1")
        self.assertEqual(self.calculator.partiallyDownloadedPlaylistDic, {"playlist1": 2, "playlist2": 1})

    def test_decreasePlaylistVideoDownloadNumber(self):
        self.calculator.decreasePlaylistVideoDownloadNumber("playlist1")
        self.assertEqual(self.calculator.partiallyDownloadedPlaylistDic, {})

        self.calculator.increasePlaylistVideoDownloadNumber("playlist1")
        self.calculator.increasePlaylistVideoDownloadNumber("playlist1")
        self.calculator.decreasePlaylistVideoDownloadNumber("playlist1")
        self.assertEqual(self.calculator.partiallyDownloadedPlaylistDic, {"playlist1": 1})

        self.calculator.decreasePlaylistVideoDownloadNumber("playlist1")
        self.assertEqual(self.calculator.partiallyDownloadedPlaylistDic, {})

        self.calculator.decreasePlaylistVideoDownloadNumber("playlist2")
        self.assertEqual(self.calculator.partiallyDownloadedPlaylistDic, {})

if __name__ == '__main__':
    unittest.main()
