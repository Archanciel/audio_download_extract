import os, shutil

from constants import *

class AudioExtractor:
	def __init__(self, guiOutput, targetAudioDir, downloadedVideoInfoDictionary):
		self.guiOutput = guiOutput
		self.targetAudioDir = targetAudioDir
		self.downloadedVideoInfoDictionary = downloadedVideoInfoDictionary
	
	def extractAudioPortion(self, downloadedVideoInfoDic):
		for videoIndex in downloadedVideoInfoDic.getVideoIndexes():
			videoFileName = downloadedVideoInfoDic.getVideoFileNameForVideoIndex(videoIndex)
			if downloadedVideoInfoDic.isTimeFrameDataAvailableForVideoIndex(videoIndex):
				import moviepy.editor as mp  # not working on Android
				mp4FilePathName = os.path.join(self.targetAudioDir, videoFileName)
				extractStartEndSecondsLists = downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(videoIndex)
				timeFrameIndex = 1
				for extractStartEndSecondsList in extractStartEndSecondsLists:
					timeStartSec = extractStartEndSecondsList[0]
					timeEndSec = extractStartEndSecondsList[1]
					clip = mp.AudioFileClip(mp4FilePathName).subclip(timeStartSec,
					                                                 timeEndSec)  # disable if do not want any clipping
					mp3FileName = os.path.splitext(videoFileName)[0] + '_' + str(timeFrameIndex) + '.mp3'
					mp3FilePathName = os.path.join(self.targetAudioDir,
					                               mp3FileName)
					clip.write_audiofile(mp3FilePathName)
					clip.close()
					HHMMSS_TimeFrameList = self.convertStartEndSecondsListTo_HHMMSS_TimeFrameList(extractStartEndSecondsList)
					downloadedVideoInfoDic.addExtractedFilePathNameForVideoIndex(videoIndex,
									                                             timeFrameIndex,
									                                             HHMMSS_TimeFrameList,
									                                             mp3FileName)
					timeFrameIndex += 1
			else:
				mp4FilePathName = os.path.join(self.targetAudioDir, videoFileName)
				mp3FilePathName = os.path.join(self.targetAudioDir, os.path.splitext(videoFileName)[0] + '.mp3')
				
				if os.path.isfile(mp3FilePathName):
					os.remove(mp3FilePathName)
				
				shutil.copy(mp4FilePathName, mp3FilePathName)

	def convertStartEndSecondsListTo_HHMMSS_TimeFrameList(self, startEndSecondsList):
		startSeconds = startEndSecondsList[0]
		endSeconds = startEndSecondsList[1]
		
		startTimeFrame = self.convertSecondsTo_HHMMSS(startSeconds)
		endTimeFrame = self.convertSecondsTo_HHMMSS(endSeconds)
		
		return [startTimeFrame, endTimeFrame]

	def convertSecondsTo_HHMMSS(self, seconds):
		HH = int(seconds / 3600)
		remainSeconds = seconds - HH * 3600
		MM = int(remainSeconds / 60)
		SS = remainSeconds - MM * 60
		
		return str(HH) + ':' + str(MM) + ':' + str(SS)
		