import re

class GuiUtil:
    @staticmethod
    def _splitLongLineToShorterLines(longLine, shorterLinesMaxLen):
        '''
        Splits the longLine string into lines not exceeding shorterLinesMaxLen and returns the lines
        into a list.

        :param longLine:
        :param shorterLinesMaxLen:
        :return:
        '''
        if longLine == '':
            return []

        wordList = longLine.split(' ')
        shortenedLine = wordList[0]
        shortenedLineLen = len(shortenedLine)
        shortenedLineList = []

        for word in wordList[1:]:
            wordLen = len(word)

            if shortenedLineLen + wordLen + 1 > shorterLinesMaxLen:
                shortenedLineList.append(shortenedLine)
                shortenedLine = word
                shortenedLineLen = wordLen
            else:
                shortenedLine += ' ' + word
                shortenedLineLen += wordLen + 1

        shortenedLineList.append(shortenedLine)

        return shortenedLineList
