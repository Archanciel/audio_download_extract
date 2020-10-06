import os, glob, re

from constants import *

class AudioExtractor:
	def __init__(self, guiOutput, targetAudioDir, downloadedVideoInfoDictionary):
		self.guiOutput = guiOutput
		self.targetAudioDir = targetAudioDir
		self.downloadedVideoInfoDictionary = downloadedVideoInfoDictionary

	def extractAudioPortion(self, downloadedVideoInfoDic):
		files = glob.glob(self.targetAudioDir + DIR_SEP + "*.mp4")
		files.sort(key=os.path.getmtime)
		videoIndex = 1
		
		if downloadedVideoInfoDic:
			import moviepy.editor as mp  # not working on Android
			for file in files:
				mp4FilePathName = os.path.join(self.targetAudioDir, file)
				extractStartEndSecondsLists = downloadedVideoInfoDic.getExtractStartEndSecondsLists(videoIndex)
				timeFrameIndex = 1
				for extractStartEndSecondsList in extractStartEndSecondsLists:
					timeStartSec = extractStartEndSecondsList[0]
					timeEndSec = extractStartEndSecondsList[1]
					clip = mp.AudioFileClip(mp4FilePathName).subclip(timeStartSec, timeEndSec)  # disable if do not want any clipping
					mp3FilePathName = os.path.join(self.targetAudioDir, os.path.splitext(file)[0] + '_' + str(timeFrameIndex) + '.mp3')
					clip.write_audiofile(mp3FilePathName)
					clip.close()
					timeFrameIndex += 1
				os.remove(mp4FilePathName)
				videoIndex += 1
		else:
			for file in files:
				mp4FilePathName = os.path.join(self.targetAudioDir, file)
				mp3FilePathName = os.path.join(self.targetAudioDir, os.path.splitext(file)[0] + '.mp3')

				if os.path.isfile(mp3FilePathName):
					os.remove(mp3FilePathName)

				os.rename(mp4FilePathName, mp3FilePathName)
