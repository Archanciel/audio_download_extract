import os

YOUTUBE_STREAM_AUDIO = '140'
DATE_TIME_FORMAT_VIDEO_INFO_FILE = '%d/%m/%Y %H:%M:%S'
SEVERAL_SECONDS = 5

if os.name == 'posix':
	CONVERT = False
	AUDIO_DIR_TEST = "/storage/emulated/0/Download/Audiobooks/test"
	YOUTUBE_DL_FILE_EXT = 'mp3'
	DIR_SEP = '/'
	WIN_WIDTH_RATIO = 1
	WIN_HEIGHT = 800	
else:
	CONVERT = False # can be set to True on Windows only
	AUDIO_DIR_TEST = "D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks\\test"
	YOUTUBE_DL_FILE_EXT = 'mp3'
	DIR_SEP = '\\'
	WIN_WIDTH_RATIO = 0.8
	WIN_HEIGHT = 500	

RV_LIST_ITEM_SPACING_ANDROID = 2
RV_LIST_ITEM_SPACING_WINDOWS = 0.5

