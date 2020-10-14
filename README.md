# youtube_audio_downloader

## Purpose
This Python utility automates the download of Youtube videos, extract the audio
from them - if specified selecting audio parts or suppressing audio portions - and
then shares the audio through mail or through WhatsApp.

## How it works
For the videos to be downloaded and converted to audio, they must be added to
a Youtube playlist. The playlist must be set to public access. If the audio
is to be splitted into parts (the interesting portions of the video audio
track), a list of time frames must be added to the playlist title. Below are
some examples of playlist titles.

### Playlist title examples
My playlist title  
*For each video contained in the playlist, its audio track will be downloaded
fully.*

My two video playlist title (**e**0:0:20-0:02:45)  
*Here, for the first video, the audio portion starting at 20 seconds and ending
at 2 minutes 45 seconds will be extracted (meaning of the **e** - **extract** letter). The audio
of the second video wil be kept unmodified.*

My two video extract playlist title (e0:0:20-0:02:45 e1:22:45-1:25:0) (e0:0:0-0:05:45 e0:22:45-e)  
*Here, for the first video, two audio parts will be extracted. Some thing for
the second video, with the second portion starting at 22 minutes 45 seconds and going
to the end of the audio track (letter **e** means **end** here).*

My one video suppress playlist title (**s**0:0:0-0:02:45 **s**0:22:45-e)  
*Here, the audio portions from beginning to 2 minutes 45 seconds and from
22 minutes 44 seconds to the end will be suppressed (meaning of the
**s** - **suppress** letter). Only one audio file will remain, without the suppressed 
parts.

## Required libraries
- pytube3
- moviepy (not working on Android !)
- mutagen