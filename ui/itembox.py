# -*- coding:gb2312 -*-
# -*- $Id: itembox.py 2 2009-04-20 03:10:36Z fengyu05 $ -*-

import pygame
from pygame.locals import *
import animsprite

__all__ = ['ItemBox']

# 道具栏UI
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
yellow = (255,255,0)
dark_green = (200,255,200)
blue = (100,0,255)
dark_yellow = (255,255,200)
orange = (200,200,0)
pink = (255,128,0)


class ItemBox(object):

	def __init__(self, screen, width, height, font, size, border=2, \
			colors=(dark_green, green, orange)):
		self.screen = screen
		self.width = width
		self.height = height
		self.font = font
		self.border = border
		self.colors = colors
		self.size = size

		self.background = pygame.Surface((width, height))
		self.background.fill(self.colors[0])

		vgap = self.border * 2
		hgap = self.border * (size + 1)

		self.box_width = (width - hgap) / size
		self.box_height = height - vgap

		self.box_background = pygame.Surface((self.box_width, self.box_height))

		self.items = [0] * size
		self.anim = []


	def bind_anim(self, lis, related_pos):
		self.anim = lis
		self.related_pos = related_pos

	def change_item(self, items):
		self.items = items
		for sprite in self.anim:
			if sprite is not None:
				sprite.update()

	def render(self, pos=(0,0)):
		self.screen.blit(self.background, pos)
		for i in range(self.size):
			posx = pos[0] + self.border * (i + 1) + (i * self.box_width)
			posy = pos[1] + self.border
			if self.items[i] == 0:
				self.box_background.fill(self.colors[2])
			else:
				self.box_background.fill(self.colors[1])
				self.box_background.blit(self.anim[self.items[i]].image, self.related_pos)

			self.screen.blit(self.box_background, (posx, posy))
			text = self.font.render("%d" % (i+1) , 1, white)
			self.screen.blit(text, (posx + self.box_width / 2, posy + self.box_height / 2) )


