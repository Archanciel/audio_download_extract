import glob, shutil, time, os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import moviepy.editor


AUDIO_DIR = 'D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks'
DIR_SEP = '\\'

playListName = 'moviepy_explore'
targetAudioDir = AUDIO_DIR + DIR_SEP + playListName

# deleting files in downloadDir
files = glob.glob(targetAudioDir + DIR_SEP + '*')

for f in files:
	os.remove(f)

# restoring mp4 file

sourceVideo = 'Magnifique vidéo de Noël.mp4'
sourceVideoFilePath = targetAudioDir + DIR_SEP + sourceVideo
shutil.copy(
	'D:\\Development\\Python\\audiodownload\\test\\testData' + DIR_SEP + sourceVideo,
	sourceVideoFilePath)

ts = time.time()
extractVideoFilePath = targetAudioDir + DIR_SEP + 'extract.mp4'
ffmpeg_extract_subclip(sourceVideoFilePath, 10, 25, targetname=extractVideoFilePath)
extrVideo = moviepy.editor.VideoFileClip(extractVideoFilePath)
audio = extrVideo.audio
extractAudioFilePath = targetAudioDir + DIR_SEP + 'extract.mp3'
audio.write_audiofile(extractAudioFilePath)

print(time.time() - ts)
