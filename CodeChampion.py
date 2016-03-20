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
			soundFile = sublime.load_settings(SETTING_NAME).get(self.soundType)
			call(["afplay", "-v", str(1), sublime.packages_path() + '/CodeChampion/sounds/' + soundFile])
			self.is_playing = False
	@thread
	def windows_play(self):
		if(self.is_playing == False):
			self.is_playing = True
			soundFile = sublime.load_settings(SETTING_NAME).get(self.soundType)
			winsound.PlaySound(sublime.packages_path() + '\\CodeChampion\\sounds\\' + soundFile, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT)
			self.is_playing = False
	@thread
	def linux_play(self):
		if(self.is_playing == False):
			self.is_playing = True
			soundFile = sublime.load_settings(SETTING_NAME).get(self.soundType)
			call(["aplay", sublime.packages_path() + '/CodeChampion/sounds/' + soundFile])
			self.is_playing = False

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
