import os
import glob
import random
import sublime, sublime_plugin,wave
from subprocess import call
from .libs.decorators import thread

try:
    import winsound
except Exception:
    pass

SETTING_NAME = "CodeChampion.sublime-settings"

class PlaySound():
	platform = sublime.platform()
	soundType = 'win'
	is_playing = False
	def play(self):
		if(self.platform == 'osx'):
			self.osx_play()
		elif(self.platform == 'windows'):
			self.windows_play()
		elif(self.platform == 'linux'):
			self.linux_play()
	@thread
	def osx_play(self):
		if(self.is_playing == False):
			self.is_playing = True
			soundFilePath = self.get_sound_file_path(self.soundType)
			call(["afplay", "-v", str(1), soundFilePath])
			self.is_playing = False
	@thread
	def windows_play(self):
		if(self.is_playing == False):
			self.is_playing = True
			soundFilePath = self.get_sound_file_path(self.soundType)
			winsound.PlaySound(soundFilePath, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT)
			self.is_playing = False
	@thread
	def linux_play(self):
		if(self.is_playing == False):
			self.is_playing = True
			soundFilePath = self.get_sound_file_path(self.soundType)
			call(["aplay", soundFilePath])
			self.is_playing = False

	def get_sound_file_path(self, soundType):
		soundFilePath = ''
		soundFile = sublime.load_settings(SETTING_NAME).get(soundType)
		baseDirectory = os.path.join(sublime.packages_path(), 'CodeChampion', 'sounds', soundType)

		if soundFile == 'Random':
			allSoundFiles = glob.glob(os.path.join(baseDirectory, '*'))
			soundFilePath = random.choice(allSoundFiles)
		else:
			soundFilePath = os.path.join(baseDirectory, soundFile)

		return soundFilePath


class PlaychampionCommand(sublime_plugin.TextCommand):
	is_playing = False
	player = PlaySound()
	def run(self, edit, type):
		self.player.soundType = type
		self.player.play()

class ChangesoundCommand(sublime_plugin.TextCommand):
	def run(self, edit, sound, type):
		sublime.load_settings(SETTING_NAME).set(type, sound)
		sublime.save_settings(SETTING_NAME)
