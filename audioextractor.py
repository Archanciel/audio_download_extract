import os, glob, re

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
					mp3FilePathName = os.path.join(self.targetAudioDir,
					                               os.path.splitext(videoFileName)[0] + '_' + str(timeFrameIndex) + '.mp3')
					clip.write_audiofile(mp3FilePathName)
					clip.close()
					timeFrameIndex += 1
				os.remove(mp4FilePathName)
			else:
				mp4FilePathName = os.path.join(self.targetAudioDir, videoFileName)
				mp3FilePathName = os.path.join(self.targetAudioDir, os.path.splitext(videoFileName)[0] + '.mp3')
				
				if os.path.isfile(mp3FilePathName):
					os.remove(mp3FilePathName)
				
				os.rename(mp4FilePathName, mp3FilePathName)
