# -*- coding:gb2312 -*-
# -*- $Id: sound.py 2 2009-04-20 03:10:36Z fengyu05 $ -*-




import pygame
import os
from pygame.locals import *


SOUND_LIS = ['drop','hit_1','hit_2','hit_3','hit_4','bg', 'death_1', 'death_2', 'get_item', 'use_item','reflect_1','reflect_2','reflect_3']

class Sound(object):

	def __init__(self, path):
		self.sounds = {}
		self.path = path
		self._load_lis( SOUND_LIS )

	def _add_sound(self, name):
		file1 = "%s\\%s.wav" % (self.path, name )
		file2 = "%s\\%s.ogg" % (self.path, name )
		if os.path.exists(file1):
			sound = pygame.mixer.Sound(file1)
		elif os.path.exists(file2):
			sound = pygame.mixer.Sound(file2)
		else:
			sound = None

		self.sounds[name] = sound

	def _load_lis(self, lis):
		for v in lis:
			self._add_sound(v)

	def stop(self, title):
		self.sounds[title].stop()

	def fadein(self, title, time):
		self.sounds[title].play(fade_ms=time)

	def fadeout(self, title, time):
		self.sounds[title].fadeout(time)

	def play(self, title, loops=0):
		self.sounds[title].play(loops)

	def channel_play(self, title, loops=0):
		if self.sounds[title] is None:
			# return
			pass

		channel = pygame.mixer.find_channel()
		if channel:
			channel.play(self.sounds[title], loops)
		else:
			self.sounds[title].play(loops)



