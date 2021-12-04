from gui.helputil import HelpUtil
from gui.scrollablelabelpopup import ScrollableLabelPopup

from kivy import platform

class HelpPopup(ScrollableLabelPopup):
	def _getContentPageList(self):
		helpFileName = 'help.txt'

		with open(helpFileName) as helpFile:
			formattedHelpTextPageList = HelpUtil.sizeParagraphsForKivyLabelFromFile(helpFile, self.textWidth)

		return formattedHelpTextPageList
