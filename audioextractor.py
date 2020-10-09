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
			if downloadedVideoInfoDic.isExtractTimeFrameDataAvailableForVideoIndex(videoIndex):
				import moviepy.editor as mp  # not working on Android
				mp4FilePathName = os.path.join(self.targetAudioDir, videoFileName)
				extractStartEndSecondsLists = downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(videoIndex)
				timeFrameIndex = 1
				for extractStartEndSecondsList in extractStartEndSecondsLists:
					timeStartSec = extractStartEndSecondsList[0]
					timeEndSec = extractStartEndSecondsList[1]
					clip = mp.AudioFileClip(mp4FilePathName).subclip(timeStartSec,
					                                                 timeEndSec)
					mp3FileName = os.path.splitext(videoFileName)[0] + '_' + str(timeFrameIndex) + '.mp3'
					mp3FilePathName = os.path.join(self.targetAudioDir,
					                               mp3FileName)
					clip.write_audiofile(mp3FilePathName)
					clip.close()
					HHMMSS_TimeFrameList = self.convertStartEndSecondsListTo_HHMMSS_TimeFrameList(extractStartEndSecondsList)
					downloadedVideoInfoDic.addExtractedFileInfoForVideoIndexTimeFrameIndex(videoIndex,
					                                                                       timeFrameIndex,
					                                                                       mp3FileName,
					                                                                       HHMMSS_TimeFrameList)
					timeFrameIndex += 1
			else:
				mp4FilePathName = os.path.join(self.targetAudioDir, videoFileName)
				mp3FilePathName = os.path.join(self.targetAudioDir, os.path.splitext(videoFileName)[0] + '.mp3')
				
				if os.path.isfile(mp3FilePathName):
					os.remove(mp3FilePathName)
				
				shutil.copy(mp4FilePathName, mp3FilePathName)
	
	def suppressFrames(self, suppressFrameList):
		suppressFrameNb = len(suppressFrameList)
		clips = []
		duration = 18
		
		for extractIdx in range(suppressFrameNb + 1):
			if extractIdx == 0:
				clips.append([0, suppressFrameList[0][0]])
			elif extractIdx == suppressFrameNb:
				clips.append([suppressFrameList[extractIdx - 1][1], duration])
			else:
				clips.append([suppressFrameList[extractIdx - 1][1], suppressFrameList[extractIdx][0]])
		
		print(clips)
	
	def suppressAudioPortion(self, downloadedVideoInfoDic):
		for videoIndex in downloadedVideoInfoDic.getVideoIndexes():
			videoFileName = downloadedVideoInfoDic.getVideoFileNameForVideoIndex(videoIndex)
			if downloadedVideoInfoDic.isSuppressTimeFrameDataAvailableForVideoIndex(videoIndex):
				import moviepy.editor as mp  # not working on Android
				mp4FilePathName = os.path.join(self.targetAudioDir, videoFileName)
				suppressStartEndSecondsLists = downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(videoIndex)
				suppressFrameNb = len(suppressStartEndSecondsLists)
				videoAudioFrame = mp.AudioFileClip(mp4FilePathName)
				duration = videoAudioFrame.duration
				clips = []
				
				for extractIdx in range(suppressFrameNb + 1):
					if extractIdx == 0:
						clips.append(self.extractClip(mp, videoAudioFrame, [0, suppressStartEndSecondsLists[0][0]]))
					elif extractIdx == suppressFrameNb:
						clips.append(self.extractClip(mp, videoAudioFrame, [suppressStartEndSecondsLists[extractIdx - 1][1], duration]))
					else:
						clips.append(self.extractClip(mp, videoAudioFrame, [suppressStartEndSecondsLists[extractIdx - 1][1], suppressStartEndSecondsLists[extractIdx][0]]))

				clip = mp.concatenate_audioclips(clips)
				mp3FileName = os.path.splitext(videoFileName)[0] + '_s.mp3'
				mp3FilePathName = os.path.join(self.targetAudioDir,
				                               mp3FileName)
				clip.write_audiofile(mp3FilePathName)
				clip.close()
				HHMMSS_SuppressedTimeFramesList = self.convertSuppressStartEndSecondsListsTo_HHMMSS_SuppressedTimeFramesList(suppressStartEndSecondsLists)
				downloadedVideoInfoDic.addSuppressedFileInfoForVideoIndex(videoIndex,
	                                                                      mp3FileName,
	                                                                      HHMMSS_SuppressedTimeFramesList)
			else:
				mp4FilePathName = os.path.join(self.targetAudioDir, videoFileName)
				mp3FilePathName = os.path.join(self.targetAudioDir, os.path.splitext(videoFileName)[0] + '.mp3')
				
				if os.path.isfile(mp3FilePathName):
					os.remove(mp3FilePathName)
				
				shutil.copy(mp4FilePathName, mp3FilePathName)

	def extractClip(self, mp, videoAudioFrame, extractStartEndSecondsList):
		timeStartSec = extractStartEndSecondsList[0]
		timeEndSec = extractStartEndSecondsList[1]
		
		clip = videoAudioFrame.subclip(timeStartSec,
		                               timeEndSec)
	
		return clip

	def convertSuppressStartEndSecondsListsTo_HHMMSS_SuppressedTimeFramesList(self, suppressStartEndSecondsLists):
		HHMMSS_SuppressedTimeFramesList = []
		
		for startEndSecondsList in suppressStartEndSecondsLists:
			HHMMSS_SuppressedTimeFramesList.append(self.convertStartEndSecondsListTo_HHMMSS_TimeFrameList(startEndSecondsList))
		
		return HHMMSS_SuppressedTimeFramesList
	
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
		