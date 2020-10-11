import os, shutil

from constants import *

if os.name == 'posix':
	pass
else:
	import moviepy.editor as mp  # not working on Android

class AudioExtractor:
	def __init__(self, guiOutput, targetAudioDir, downloadedVideoInfoDictionary):
		self.guiOutput = guiOutput
		self.targetAudioDir = targetAudioDir
		self.downloadedVideoInfoDictionary = downloadedVideoInfoDictionary
	
	def extractAudioPortion(self, downloadedVideoInfoDic):
		for videoIndex in downloadedVideoInfoDic.getVideoIndexes():
			videoFileName = downloadedVideoInfoDic.getVideoFileNameForVideoIndex(videoIndex)
			if downloadedVideoInfoDic.isExtractTimeFrameDataAvailableForVideoIndex(videoIndex):
				mp4FilePathName = os.path.join(self.targetAudioDir, videoFileName)
				extractStartEndSecondsLists = downloadedVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(videoIndex)
				timeFrameIndex = 1
				for extractStartEndSecondsList in extractStartEndSecondsLists:
					timeStartSec = extractStartEndSecondsList[0]
					timeEndSec = extractStartEndSecondsList[1]
					
					if timeEndSec == 'end':
						# the extract time frame is from timeStartSec to end of video !
						videoAudioFrame = mp.AudioFileClip(mp4FilePathName)
						timeEndSec = videoAudioFrame.duration
						extractStartEndSecondsList[1] = timeEndSec
						videoAudioFrame.close()
						
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
	
	def suppressAudioPortion(self, downloadedVideoInfoDic):
		for videoIndex in downloadedVideoInfoDic.getVideoIndexes():
			videoFileName = downloadedVideoInfoDic.getVideoFileNameForVideoIndex(videoIndex)
			if downloadedVideoInfoDic.isSuppressTimeFrameDataAvailableForVideoIndex(videoIndex):
				mp4FilePathName = os.path.join(self.targetAudioDir, videoFileName)
				suppressStartEndSecondsLists = downloadedVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(videoIndex)
				suppressFrameNb = len(suppressStartEndSecondsLists)
				videoAudioFrame = mp.AudioFileClip(mp4FilePathName)
				duration = videoAudioFrame.duration
				clips = []
				keptStartEndSecondsLists = []
				
				for extractIdx in range(suppressFrameNb + 1):
					if extractIdx == 0:
						timeFrameEndValue = suppressStartEndSecondsLists[0][0]
						
						if timeFrameEndValue == 0:
							# suppress frame is starting at 0 and so, appending time frame 0-0 is nonsensical !
							continue
						
						extractStartEndSecondsList = [0, timeFrameEndValue]
						keptStartEndSecondsLists.append(extractStartEndSecondsList)
						clips.append(self.extractClip(videoAudioFrame, extractStartEndSecondsList))
					elif extractIdx == suppressFrameNb:
						extractStartEndSecondsList = [suppressStartEndSecondsLists[extractIdx - 1][1], duration]
						
						if extractStartEndSecondsList[0] == 'end':
							suppressStartEndSecondsLists[extractIdx - 1][1] = duration
							continue
							
						keptStartEndSecondsLists.append(extractStartEndSecondsList)
						clips.append(self.extractClip(videoAudioFrame, extractStartEndSecondsList))
					else:
						extractStartEndSecondsList = [suppressStartEndSecondsLists[extractIdx - 1][1],
						                              suppressStartEndSecondsLists[extractIdx][0]]
						keptStartEndSecondsLists.append(extractStartEndSecondsList)
						clips.append(self.extractClip(videoAudioFrame, extractStartEndSecondsList))

				self.guiOutput.setMessage('Time frames kept {}'.format(keptStartEndSecondsLists))
				clip = mp.concatenate_audioclips(clips)
				mp3FileName = os.path.splitext(videoFileName)[0] + '_s.mp3'
				mp3FilePathName = os.path.join(self.targetAudioDir,
				                               mp3FileName)
				clip.write_audiofile(mp3FilePathName)
				clip.close()
				videoAudioFrame.close()
				HHMMSS_suppressedTimeFramesList = self.convertStartEndSecondsListsTo_HHMMSS_TimeFramesList(suppressStartEndSecondsLists)
				HHMMSS_keptTimeFramesList = self.convertStartEndSecondsListsTo_HHMMSS_TimeFramesList(keptStartEndSecondsLists)
				downloadedVideoInfoDic.addSuppressedFileInfoForVideoIndex(videoIndex,
	                                                                      mp3FileName,
	                                                                      HHMMSS_suppressedTimeFramesList,
				                                                          HHMMSS_keptTimeFramesList)
			else:
				mp4FilePathName = os.path.join(self.targetAudioDir, videoFileName)
				mp3FilePathName = os.path.join(self.targetAudioDir, os.path.splitext(videoFileName)[0] + '.mp3')
				
				if os.path.isfile(mp3FilePathName):
					os.remove(mp3FilePathName)
				
				shutil.copy(mp4FilePathName, mp3FilePathName)

	def extractClip(self, videoAudioFrame, extractStartEndSecondsList):
		timeStartSec = extractStartEndSecondsList[0]
		timeEndSec = extractStartEndSecondsList[1]
		
		clip = videoAudioFrame.subclip(timeStartSec,
		                               timeEndSec)
	
		return clip

	def convertStartEndSecondsListsTo_HHMMSS_TimeFramesList(self, suppressStartEndSecondsLists):
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
