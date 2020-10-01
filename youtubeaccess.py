import re, os
from pytube import YouTube, Playlist 
import http.client

from constants import *
from playlisttimeframedata import PlaylistTimeFrameData

class YoutubeAccess:
	def __init__(self, guiOutput):
		self.guiOutput = guiOutput
		self.msgText = ''
		
	def downloadAudioFromPlaylist(self, playlistUrl):

		playlist = self.getPlaylistObject(playlistUrl)
		
		if playlist == None:
			return
		
		playlistTitle = playlist.title()

		if playlistTitle == None or \
			'Oops' in playlistTitle:
			self.guiOutput.displayError('The URL obtained from clipboard is not pointing to a playlist. Program closed.')
			return
			
		playlistName, timeInfo = self.splitPlayListTitle(playlistTitle)
		targetAudioDir = AUDIO_DIR + DIR_SEP + playlistName
		
		if not os.path.isdir(targetAudioDir):
			targetAudioDirList = targetAudioDir.split(DIR_SEP)
			targetAudioDirShort = DIR_SEP.join(targetAudioDirList[-2:])
			
			if not self.guiOutput.getConfirmation("Directory\n{}\nwill be created.\n\nContinue with download ?".format(targetAudioDirShort)):
				return
				
			os.makedirs(targetAudioDir)
				
		for video in playlist.videos:
			audioStream = video.streams.get_by_itag(YOUTUBE_STREAM_AUDIO)
			videoTitle = video.title
			self.msgText = self.msgText + 'downloading ' + videoTitle + '\n'
			self.guiOutput.setMessage(self.msgText)
			audioStream.download(output_path=targetAudioDir)
		
		return timeInfo, targetAudioDir
	
	def getPlaylistObject(self, playlistUrl):
		playlist = None
		
		try:
			playlist = Playlist(playlistUrl)
			playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
		except KeyError as e:
			self.guiOutput.displayError('Playlist URL not in clipboard. Program closed.')
		except http.client.InvalidURL as e:
			self.guiOutput.displayError(str(e))
		except AttributeError as e:
			self.guiOutput.displayError('playlist URL == None')

		return playlist
	
	def splitPlayListTitle(self, playlistTitle):
		'''
		Returns the playlist name and a dictionary whose key is the video index
		and value is a list of two lists, one containing the start and
		end extract positions in seconds, the second list containing the start
		and end suppress positions in seconds.
		'''
		playlistNamePattern = r'([a-zaA-Z_\d]+)(?: ([\(se\d:\- \)]*))?'
		
		match = re.match(playlistNamePattern, playlistTitle)
		playlistName = match.group(1)
		videoTimeFramesInfo = match.group(2)
		playlistTimeFrameData = None
		
		if videoTimeFramesInfo != None:
			playlistTimeFrameData = self.extractTimeInfo(videoTimeFramesInfo)
		
		return playlistName, playlistTimeFrameData
	
	def extractTimeInfo(self, playlistName):
		videoTimeFramesPattern = r'(\([se\d:\- ]*\) ?)'
		startEndTimeFramePattern = r'([\dsSeE:\-]+)'
		playlistTimeFrameData = PlaylistTimeFrameData()
		videoIndex = 1
		
		for videoTimeFramesGroup in re.finditer(videoTimeFramesPattern, playlistName):
			playlistTimeFrameData.addVideoTimeFrameData(videoIndex)
			#print('video {} timeFrames'.format(videoIndex), videoTimeFramesGroup.group(0))
			
			for startEndTimeFrameGroup in re.finditer(startEndTimeFramePattern, videoTimeFramesGroup.group(0)):
				startEndTimeFrame = startEndTimeFrameGroup.group(0)
				startEndSecondsList = self.convertToStartEndSeconds(startEndTimeFrame[1:])
				if startEndTimeFrame[0].upper() == 'E':
					playlistTimeFrameData.addExtractStartEndSecondsList(videoIndex, startEndSecondsList)
				elif startEndTimeFrame[0].upper() == 'S': 
					playlistTimeFrameData.addSuppressStartEndSecondsList(videoIndex, startEndSecondsList)
				#print(startEndTimeFrame)
			videoIndex += 1
		
		return playlistTimeFrameData

	def convertToStartEndSeconds(self, startEndTimeFrame):
		timeLst = startEndTimeFrame.split('-')
		timeStartHHMMSS = timeLst[0].split(':')
		timeEndHHMMSS = timeLst[1].split(':')

		timeStartSec = int(timeStartHHMMSS[0]) * 3600 + int(timeStartHHMMSS[1]) * 60 + int(timeStartHHMMSS[2])
		timeEndSec = int(timeEndHHMMSS[0]) * 3600 + int(timeEndHHMMSS[1]) * 60 + int(timeEndHHMMSS[2])

		return [timeStartSec, timeEndSec]
