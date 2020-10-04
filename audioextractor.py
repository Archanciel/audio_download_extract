import os, glob, re

from constants import *

class AudioExtractor:
	def __init__(self, guiOutput, targetAudioDir, downloadedVideoInfoDictionary):
		self.guiOutput = guiOutput
		self.targetAudioDir = targetAudioDir
		self.downloadedVideoInfoDictionary = downloadedVideoInfoDictionary

	def extractAudioPortion(self, playlistTimeFrameData):
		files = glob.glob(self.targetAudioDir + DIR_SEP + "*.mp4")
		files.sort(key=os.path.getmtime)
		videoIndex = 1
		
		if playlistTimeFrameData:
			import moviepy.editor as mp  # not working on Android
			for file in files:
				mp4FilePathName = os.path.join(self.targetAudioDir, file)
				extractStartEndSecondsLists = playlistTimeFrameData.getExtractStartEndSecondsLists(videoIndex)
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
	
	# def extractAudioPortionAlt(self, playlistTimeFrameData):
	# 	# is slower in fact !!!
	# 	from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
	# 	files = glob.glob(self.targetAudioDir + DIR_SEP + "*.mp4")
	# 	files.sort(key=os.path.getmtime)
	# 	videoIndex = 1
	#
	# 	if playlistTimeFrameData:
	# 		import moviepy.editor as mp  # not working on Android
	# 		for file in files:
	# 			mp4ExtractFilePathName = os.path.join(self.targetAudioDir, 'extr.mp4')
	# 			extractStartEndSecondsLists = playlistTimeFrameData.getExtractStartEndSecondsLists(videoIndex)
	# 			timeFrameIndex = 1
	# 			for extractStartEndSecondsList in extractStartEndSecondsLists:
	# 				timeStartSec = extractStartEndSecondsList[0]
	# 				timeEndSec = extractStartEndSecondsList[1]
	#
	# 				ffmpeg_extract_subclip(file, timeStartSec, timeEndSec, targetname=mp4ExtractFilePathName)
	# 				extrVideo = mp.VideoFileClip(mp4ExtractFilePathName)
	# 				audio = extrVideo.audio
	# 				mp3FilePathName = os.path.join(self.targetAudioDir,
	# 				                               os.path.splitext(file)[0] + '_' + str(timeFrameIndex) + '.mp3')
	# 				audio.write_audiofile(mp3FilePathName)
	# 				audio.close()
	# 				extrVideo.close()
	# 				#
	# 				# clip = mp.AudioFileClip(mp4FilePathName).subclip(timeStartSec,
	# 				#                                                  timeEndSec)  # disable if do not want any clipping
	# 				# clip.write_audiofile(mp3FilePathName)
	# 				# clip.close()
	# 				timeFrameIndex += 1
	# 			os.remove(file)
	# 			os.remove(mp4ExtractFilePathName)
	# 			videoIndex += 1
	# 	else:
	# 		for file in files:
	# 			mp4FilePathName = os.path.join(self.targetAudioDir, file)
	# 			mp3FilePathName = os.path.join(self.targetAudioDir, os.path.splitext(file)[0] + '.mp3')
	#
	# 			if os.path.isfile(mp3FilePathName):
	# 				os.remove(mp3FilePathName)
	#
	# 			os.rename(mp4FilePathName, mp3FilePathName)
