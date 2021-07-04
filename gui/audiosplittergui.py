from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

class AudioSplitterGUI(Screen):
	def __init__(self, **kw):
		super(AudioSplitterGUI, self).__init__(**kw)

		# WARNING: accessing MainWindow fields defined in kv file
		# in the __init__ ctor is no longer possible when using
		# ScreenManager. Here's the solution:
		# (https://stackoverflow.com/questions/26916262/why-cant-i-access-the-screen-ids)
		Clock.schedule_once(self._finish_init)

	def _finish_init(self, dt):
		pass

	def playAudioFile(self):
		"""
		Executed by pressing the Play button
		example:
		D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks\\Various\\Wear a mask. Help slow the spread of Covid-19..mp3
		"""
		sound = SoundLoader.load(self.sourceAudioFilePathName.text)
		if sound:
			sound.play()
