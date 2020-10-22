import re
from urllib.error import URLError
from pytube import Playlist
import http.client

from accesserror import AccessError


def getPlaylistObjectForPlaylistUrl(playlistUrl):
	"""
	Returns the pytube.Playlist object corresponding to the passed playlistUrl the
	playlistObject title and None if no problem happened.

	:param playlistUrl:
	:return: playlistObject - Playlist object
			 playlistTitle
			 accessError in case of problem, None otherwise
	"""
	playlistObject = None
	playlistTitle = None
	accessError = None
	
	try:
		playlistObject = Playlist(playlistUrl)
		playlistObject._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
		playlistTitle = playlistObject.title()
	except http.client.InvalidURL as e:
		accessError = AccessError(AccessError.ERROR_TYPE_PLAYLIST_URL_INVALID, str(e))
	except AttributeError as e:
		accessError = AccessError(AccessError.ERROR_TYPE_PLAYLIST_URL_INVALID, str(e))
	except URLError:
		accessError = AccessError(AccessError.ERROR_TYPE_NO_INTERNET, 'No internet access. Fix the problem and retry !')
	
	if accessError is None and (playlistTitle is None or 'Oops' in playlistTitle):
		accessError = AccessError(AccessError.ERROR_TYPE_NOT_PLAYLIST_URL, playlistUrl)
	
	return playlistObject, playlistTitle, accessError

if __name__ == "__main__":
	url = "https://www.youtube.com/playlist?list=PLzwWSJNcZTMSFWGrRGKOypqN29MlyuQvn"
	getPlaylistObjectForPlaylistUrl(url)
