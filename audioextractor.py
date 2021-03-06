import os, shutil
from pydub import AudioSegment
import soundfile as sf
import pyrubberband as pyrb

from constants import *

if os.name == 'posix':
	pass
else:
	import moviepy.editor as mp  # not working on Android

class AudioExtractor:
	def __init__(self, audioController, targetAudioDir, downloadVideoInfoDictionary):
		self.audioController = audioController
		self.targetAudioDir = targetAudioDir
		self.downloadVideoInfoDictionary = downloadVideoInfoDictionary

	def extractPlaylistAudio(self, downloadVideoInfoDic):
		for videoIndex in downloadVideoInfoDic.getVideoIndexes():
			videoFileName = downloadVideoInfoDic.getVideoFileNameForVideoIndex(videoIndex)
			if videoFileName is None:
				# downloading the video failed
				continue
			if downloadVideoInfoDic.isExtractTimeFrameDataAvailableForVideoIndex(videoIndex):
				if downloadVideoInfoDic.isExtractedFileInfoAvailableForVideoIndex(videoIndex):
					msgText = '\nextracting portions for "{}" was already performed. Extraction skipped.'.format(videoFileName)
					self.audioController.displayMessage(msgText)
				else:
					self.extractAudioPortions(videoIndex, videoFileName, downloadVideoInfoDic)

			if downloadVideoInfoDic.isSuppressTimeFrameDataAvailableForVideoIndex(videoIndex):
				if downloadVideoInfoDic.isSuppressedFileInfoAvailableForVideoIndex(videoIndex):
					msgText = '\nsuppressing portions for "{}" was already performed. Suppression skipped.'.format(videoFileName)
					self.audioController.displayMessage(msgText)
				else:
					self.suppressAudioPortions(videoIndex, videoFileName, downloadVideoInfoDic)

		msgText = '\n"{}" playlist audio(s) extraction/suppression terminated.\n'.format(downloadVideoInfoDic.getPlaylistName())
		self.audioController.displayMessage(msgText)

	def extractAudioPortions(self,
	                         videoIndex,
	                         videoFileName,
	                         downloadVideoInfoDic,
	                         floatSpeed=1.0):
		mp4FilePathName = os.path.join(self.targetAudioDir, videoFileName)
		extractStartEndSecondsLists = downloadVideoInfoDic.getExtractStartEndSecondsListsForVideoIndex(videoIndex)
		timeFrameIndex = 1

		msgText = '\nextracting portions of "{}" ...\n'.format(videoFileName)
		self.audioController.displayMessage(msgText)
		
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
			
			# now changing the speed of the split audio file
			if floatSpeed != 1.0:
				self.changeSpeed(mp3FilePathName=mp3FilePathName,
				                 floatSpeed=floatSpeed)
				
			HHMMSS_TimeFrameList = self.convertStartEndSecondsListTo_HHMMSS_TimeFrameList(extractStartEndSecondsList)
			downloadVideoInfoDic.addExtractedFileInfoForVideoIndexTimeFrameIndex(videoIndex,
			                                                                     timeFrameIndex,
			                                                                     mp3FileName,
			                                                                     HHMMSS_TimeFrameList)
			
			msgText = '\ttime frames extracted'
			self.audioController.displayMessage(msgText)
			
			msgText = '\t\t{}-{}'.format(HHMMSS_TimeFrameList[0], HHMMSS_TimeFrameList[1])
			self.audioController.displayMessage(msgText)

			if floatSpeed != 1.0:
				msgText = '\tspeed'
				self.audioController.displayMessage(msgText)
				
				msgText = '\t\t{}'.format(floatSpeed)
				self.audioController.displayMessage(msgText)
			
			timeFrameIndex += 1
	
	def suppressAudioPortions(self, videoIndex, videoFileName, downloadVideoInfoDic):
		mp4FilePathName = os.path.join(self.targetAudioDir, videoFileName)
		suppressStartEndSecondsLists = downloadVideoInfoDic.getSuppressStartEndSecondsListsForVideoIndex(videoIndex)
		suppressFrameNb = len(suppressStartEndSecondsLists)
		videoAudioFrame = mp.AudioFileClip(mp4FilePathName)
		duration = videoAudioFrame.duration
		clips = []
		keptStartEndSecondsLists = []
		
		msgText = '\nsuppressing portions of "{}" ...\n'.format(videoFileName)
		self.audioController.displayMessage(msgText)
		
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

		clip = mp.concatenate_audioclips(clips)
		mp3FileName = os.path.splitext(videoFileName)[0] + '_s.mp3'
		mp3FilePathName = os.path.join(self.targetAudioDir,
		                               mp3FileName)
		clip.write_audiofile(mp3FilePathName)
		clip.close()
		videoAudioFrame.close()
		HHMMSS_suppressedTimeFramesList = self.convertStartEndSecondsListsTo_HHMMSS_TimeFramesList(suppressStartEndSecondsLists)
		HHMMSS_keptTimeFramesList = self.convertStartEndSecondsListsTo_HHMMSS_TimeFramesList(keptStartEndSecondsLists)
		downloadVideoInfoDic.addSuppressedFileInfoForVideoIndex(videoIndex,
                                                                  mp3FileName,
                                                                  HHMMSS_suppressedTimeFramesList,
		                                                          HHMMSS_keptTimeFramesList)
		
		self.displayFramesMsg('\ttime frames suppressed:', HHMMSS_suppressedTimeFramesList)
		self.displayFramesMsg('\n\ttime frames kept:', HHMMSS_keptTimeFramesList)
	
	def displayFramesMsg(self, startMsgText, HHMMSS_timeFramesList):
		self.audioController.displayMessage(startMsgText)
		
		for HHMMSS_timeFrame in HHMMSS_timeFramesList:
			msgText = '\t\t{}-{}'.format(HHMMSS_timeFrame[0], HHMMSS_timeFrame[1])
			self.audioController.displayMessage(msgText)

	def convertDownloadedMp3ToKivySoundLoaderCompliantMp3(self, downloadedAudioFileName):
		"""
		No longer necessary since youtube_dl option 'outtmpl' was fixed !
		Additionaly, moviepy being not usable on Android, this method
		can not be used on Android to make the mp3 files downloaded by
		youtube_dl compliant with kivy SoundLoader !
		
		:param downloadedAudioFileName:
		:return:
		"""
		msgText = '\nconverting "{}" to compliant mp3 ...\n'.format(downloadedAudioFileName)
		self.audioController.displayMessage(msgText)

		downloadedAudioFilePathName = os.path.join(self.targetAudioDir,
		                                 downloadedAudioFileName)
		compliantAudioFileName = os.path.splitext(downloadedAudioFileName)[0] + '_full' + '.mp3'
		compliantAudioFilePathName = os.path.join(self.targetAudioDir,
		                               compliantAudioFileName)
		clip = mp.AudioFileClip(downloadedAudioFilePathName).subclip()
		clip.write_audiofile(compliantAudioFilePathName)
		clip.close()

		msgText = '"{}" converted to {}\n'.format(downloadedAudioFileName, compliantAudioFileName)
		self.audioController.displayMessage(msgText)
	
	def convertVideoToAudio(self, videoFileName, fileNameSuffix = ''):
		"""
		No longer used since youtube_dl replaces pytube for downloading video audio tracks.
		THIS IS NOT COMPATIBLE WITH USING Kivy SoundLoader !!!!! Renaming mp4 file to mp3
		file makes SoundLoader fail with 'Unrecognized audio format' error !
		
		:param videoFileName:
		:param fileNameSuffix:
		:return:
		"""
		mp4FilePathName = os.path.join(self.targetAudioDir, videoFileName)
		
		if fileNameSuffix != '':
			fileNameSuffix = '_' + fileNameSuffix
			
		mp3FileName = os.path.splitext(videoFileName)[0] + fileNameSuffix + '.mp3'
		mp3FilePathName = os.path.join(self.targetAudioDir, mp3FileName)
		
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
		SS = round(remainSeconds) - MM * 60
		leftZero = ''
		
		if SS < 10:
			leftZero = '0'
		
		return str(HH) + ':' + str(MM) + ':' + leftZero + str(SS)

	def changeSpeed(self,
	                mp3FilePathName,
	                floatSpeed):
		sound = AudioSegment.from_file(mp3FilePathName)
		wavFilePathName = mp3FilePathName.split('.')[0] + '.wav'
		sound.export(wavFilePathName, format="wav")
		y, sr = sf.read(wavFilePathName)
		
		y_stretch = pyrb.time_stretch(y, sr, floatSpeed)
		sf.write(wavFilePathName, y_stretch, sr, format='wav')
		
		sound = AudioSegment.from_wav(wavFilePathName)
		
#		mp3FilePathNameAccelerated = mp3FilePathName.split('.')[0] + '_speeded' + '.mp3'
		sound.export(mp3FilePathName, format="mp3")
		os.remove(wavFilePathName)
