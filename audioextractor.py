import os, re

class AudioExtractor:
	def __init__(self, guiOutput, targetAudioDir):
		self.guiOutput = guiOutput
		self.targetAudioDir = targetAudioDir

	def extractAudioPortion(self, timeInfo):
		for file in [n for n in os.listdir(self.targetAudioDir) if re.search('mp4', n)]:
			mp4FilePathName = os.path.join(self.targetAudioDir, file)
			mp3FilePathName = os.path.join(self.targetAudioDir, os.path.splitext(file)[0] + '.mp3')

			if timeInfo:
				timeStartSec, timeEndSec = self.splitTimeInfo(timeInfo)
				import moviepy.editor as mp  # not working on Android
				clip = mp.AudioFileClip(mp4FilePathName).subclip(timeStartSec, timeEndSec)  # disable if do not want any clipping
				clip.write_audiofile(mp3FilePathName)
				clip.close()
				os.remove(mp4FilePathName)
			else:
				if os.path.isfile(mp3FilePathName):
					os.remove(mp3FilePathName)

				os.rename(mp4FilePathName, mp3FilePathName)
			
	def splitTimeInfo(self, timeInfo):
		timeLst = timeInfo.split('/')
		timeStartHHMMSS = timeLst[0].split('.')
		timeEndHHMMSS = timeLst[1].split('.')

		timeStartSec = int(timeStartHHMMSS[0]) * 3600 + int(timeStartHHMMSS[1]) * 60 + int(timeStartHHMMSS[2])
		timeEndSec = int(timeEndHHMMSS[0]) * 3600 + int(timeEndHHMMSS[1]) * 60 + int(timeEndHHMMSS[2])

		return timeStartSec, timeEndSec
