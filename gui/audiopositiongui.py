from datetime import datetime

from audiogui import AudioGUI

class AudioPositionGUI(AudioGUI):
	"""
	Abstract class hosting common methods of its sub classes.
	"""
	def __init__(self, **kw):
		super().__init__(**kw)
	
	def convertTimeStringToSeconds(self, timeString):
		dateTimeStart1900 = datetime.strptime(timeString, "%H:%M:%S")
		dateTimeDelta = dateTimeStart1900 - datetime(1900, 1, 1)
		
		return dateTimeDelta.total_seconds()
	
	def updateFileSoundPos(self,
	                       soundloaderMp3Obj,
	                       newSoundPos,
	                       soundFilePlayButton):
		"""
		This method avoids duplicating several time the same code.
		
		:param soundloaderMp3Obj:
		:param newSoundPos:
		:param soundFilePlayButton:
		"""
		soundloaderMp3Obj.seek(newSoundPos)
		
		if soundloaderMp3Obj.status == 'stop':
			# here, the mp3 was played until its end
			soundloaderMp3Obj.play()

		soundFilePlayButton.disabled = True