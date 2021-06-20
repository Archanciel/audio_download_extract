import os

YOUTUBE_STREAM_AUDIO = '140'
DATE_TIME_FORMAT_VIDEO_INFO_FILE = '%d/%m/%Y %H:%M:%S'

if os.name == 'posix':
	CONVERT = False
	AUDIO_DIR = '/storage/emulated/0/Download/Audiobooks'
	AUDIO_DIR_TEST = AUDIO_DIR + "/test"
	SINGLE_VIDEO_AUDIO_DIR = '/storage/emulated/0/Download/Audiobooks/Various'
	YOUTUBE_DL_FILE_EXT = 'mp3'
	DIR_SEP = '/'
	WIN_WIDTH_RATIO = 1
	WIN_HEIGHT = 800	
else:
	CONVERT = False # can be set to True on Windows only
	AUDIO_DIR = 'D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks'
	AUDIO_DIR_TEST = AUDIO_DIR + "\\test"
	SINGLE_VIDEO_AUDIO_DIR = 'D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks\\Various'
	YOUTUBE_DL_FILE_EXT = 'mp3'
	DIR_SEP = '\\'
	WIN_WIDTH_RATIO = 0.8
	WIN_HEIGHT = 500	

