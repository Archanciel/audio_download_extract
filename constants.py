import os

YOUTUBE_STREAM_AUDIO = '140'
DATE_TIME_FORMAT_VIDEO_INFO_FILE = '%d/%m/%Y %H:%M:%S'

if os.name == 'posix':
	CONVERT = False
	AUDIO_DIR = '/storage/emulated/0/Download/Audiobooks'
	DIR_SEP = '/'
	WIN_WIDTH_RATIO = 1
	WIN_HEIGHT = 800	
else:
	CONVERT = False # can be set to True on Windows only
	AUDIO_DIR = 'D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks'
	DIR_SEP = '\\'
	WIN_WIDTH_RATIO = 0.8
	WIN_HEIGHT = 500	

