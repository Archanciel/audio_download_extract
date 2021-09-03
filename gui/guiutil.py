import os
from os.path import sep

class GuiUtil:
    SD_CARD_DIR_TABLET = '/storage/0000-0000'
    SD_CARD_DIR_SMARTPHONE = '/storage/9016-4EF8'
    SEPARATORS = [sep, ' ', ',', '.', ':', '-', '_']

    @staticmethod
    def onSmartPhone():
        return os.path.isdir(GuiUtil.SD_CARD_DIR_SMARTPHONE)

    @staticmethod
    def splitLineToLines(longLine, maxLineLen, replaceUnderscoreBySpace=False):
        '''
		Add '\n' chars to the passed lonLine in order to respect the passed maxLineLen.
        This method is replaced by GuiUtil.reformatString().
        
		:param longLine:
		:param maxLineLen:
		:param replaceUnderscoreBySpace
		:return:
		'''
        if longLine == '':
            return []
    
        if replaceUnderscoreBySpace:
            longLine = longLine.replace('_', ' ')
    
        noteWordList = longLine.split(' ')
        noteLine = noteWordList[0]
        noteLineLen = len(noteLine)
        noteLineList = []
    
        for word in noteWordList[1:]:
            wordLen = len(word)
        
            if noteLineLen + wordLen + 1 > maxLineLen:
                noteLineList.append(noteLine)
                noteLine = word
                noteLineLen = wordLen
            else:
                noteLine += ' ' + word
                noteLineLen += wordLen + 1
    
        noteLineList.append(noteLine)
    
        return '\n'.join(noteLineList)

    @staticmethod
    def reformatString(sourceStr, maxLength):
        """
        Re-formats the passed sourceString so that the returned formattedStr contains
        new line (\n) chars in order for the formattedStr to contain lines shorter or equal
        to the passed maxLength char number.
        
        :param sourceStr:
        :param maxLength:

        :return: formattedStr
        """
        previousSepIndex = 0
        previousSepChar = ''
        currIndex = 0
        currSplitLength = 0
        formattedStr = ''
        previousSplitIndex = 0
    
        for c in sourceStr:
            if c in GuiUtil.SEPARATORS:
                previousSepIndex = currIndex
                previousSepChar = c
        
            currIndex += 1
            currSplitLength += 1
        
            if previousSepChar != ' ':
                if currSplitLength >= maxLength - 1:
                    splitEndIndex = previousSepIndex + 1
                    splitStr = sourceStr[previousSplitIndex:splitEndIndex]
                
                    if splitStr == '':
                        continue
                
                    formattedStr += splitStr + '\n'
                    previousSplitIndex = splitEndIndex
                    currSplitLength = currIndex - splitEndIndex
            else:
                if currSplitLength > maxLength:
                    splitEndIndex = previousSepIndex + 1
                    splitStr = sourceStr[previousSplitIndex:splitEndIndex]
                
                    if splitStr == '':
                        continue
                
                    formattedStr += splitStr + '\n'
                    previousSplitIndex = splitEndIndex
                    currSplitLength = currIndex - splitEndIndex - 1
    
        formattedStr += sourceStr[previousSplitIndex:]
    
        return formattedStr

