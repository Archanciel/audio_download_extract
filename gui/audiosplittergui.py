from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

import threading

from asynchsliderupdater import AsynchSliderUpdater


class AudioSplitterGUI(Screen):
	def __init__(self, **kw):
		super(AudioSplitterGUI, self).__init__(**kw)

		# WARNING: accessing MainWindow fields defined in kv file
		# in the __init__ ctor is no longer possible when using
		# ScreenManager. Here's the solution:
		# (https://stackoverflow.com/questions/26916262/why-cant-i-access-the-screen-ids)
		Clock.schedule_once(self._finish_init)

	def _finish_init(self, dt):
		self.soundloaderMp3Obj = None
		self.sliderAsynchUpdater = None
		self.sliderUpdateFrequency = 1

	def playAudioFile(self):
		"""
		Executed by pressing the Play button
		example of audio file pathname:
		D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks\\Various\\Wear a mask. Help slow the spread of Covid-19..mp3
		"""
		# self.sourceAudioFilePathName.text was set either by
		# FileToSplitLoadFileChooserPopup.loadFile() or by
		# AudioDownloaderGUI._doOnStart().
		self.soundloaderMp3Obj = SoundLoader.load(self.sourceAudioFilePathName.text)
		
		if self.soundloaderMp3Obj:
			soundLength = self.soundloaderMp3Obj.length
			self.audioSlider.max = soundLength
			
			if soundLength < 100:
				self.sliderUpdateFrequency = 1 / soundLength
				
			self.startSliderUpdateThread()
			self.playButton.disabled = True
			self.soundloaderMp3Obj.play()
	
	def startSliderUpdateThread(self):
		if self.sliderAsynchUpdater:
			self.sliderAsynchUpdater.stopSliderUpdaterThread = True
			
		self.sliderAsynchUpdater = AsynchSliderUpdater(self,
		                                               self.soundloaderMp3Obj,
		                                               self.ids.slider,
		                                               stopSliderUpdaterThread=False)
		self.sliderUpdaterThread = threading.Thread(target=self.sliderAsynchUpdater.updateSlider, args=())
		self.sliderUpdaterThread.daemon = True
		self.sliderUpdaterThread.start()
	
	def updateSoundPos(self, value):
		"""
		Method called by the slider every time its value changes. The
		value of the slider changes for two reasons:
			1/ the user moved the slider
			2/ the AsynchSliderUpdater.updateSlider() called by a
			   separate thread which updates the slider position
			   every second to reflect the current mp3 playing position
			   was executed.
		:param value:
		:return:
		"""
		if self.soundloaderMp3Obj is not None:
			if abs(self.soundloaderMp3Obj.get_pos() - value) > self.sliderUpdateFrequency:
				# test required to avoid mp3 playing perturbation
				print('AudioSplitterGUI.updateSoundPos: {}'.format(value))
				self.soundloaderMp3Obj.seek(value)
				if self.soundloaderMp3Obj.status == 'stop':
					# here, the mp3 was played until its end
					self.soundloaderMp3Obj.play()
					self.startSliderUpdateThread()
				else:
					# here, the user moved the slider to a position before end
					# of sound
					self.playButton.disabled = True
	
	def stopAudioFile(self):
		"""
		Executed by pressing the Stop button
		"""
		if self.soundloaderMp3Obj:
			self.audioSlider.value = 0
			self.soundloaderMp3Obj.stop()
			self.sliderAsynchUpdater.stopSliderUpdaterThread = True
			self.playButton.disabled = False

