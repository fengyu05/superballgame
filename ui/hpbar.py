# -*- coding:gb2312 -*-
# -*- $Id: hpbar.py 2 2009-04-20 03:10:36Z fengyu05 $ -*-
import pygame
from pygame.locals import *

__all__ = ['HpBar']

# 血槽UI

red = (255,0,0)
green = (0,255,0)
yellow = (255,255,0)
dark_green = (200,255,200)
blue = (100,0,255)
dark_yellow = (255,255,200)
orange = (200,200,0)
pink = (255,128,0)

class HpBar(object):

	def __init__(self, screen, length, height, border=2, colors=(green,yellow,red,dark_green)):
		self.length = length
		self.height = height
		self.hp_max = 100
		self.hp = 0
		self.screen = screen

		if colors == -1:
			self.colors=(blue, orange, pink, dark_yellow)
		else:
			self.colors = colors

		self.background = pygame.Surface((length, height))
		self.background.fill(self.colors[3])

		self.border = border
		gap = border * 2
		self.front = pygame.Surface((length - gap, height - gap))


	# 修改HP百分率 输入 0 ~ 100 之间的数值
	def change_hp(self, hp):
		self.hp = hp
		self.front.fill(dark_green)
		rect = self.front.get_rect()
		rect.width = self.length * hp / 100
		if hp > 50:
			self.front.fill(self.colors[0], rect)
		elif hp > 30:
			self.front.fill(self.colors[1], rect)
		else:
			self.front.fill(self.colors[2], rect)


	def render(self, pos=(0,0)):
		self.screen.blit( self.background, pos)
		self.screen.blit( self.front, (pos[0] + self.border, pos[1] + self.border) )


