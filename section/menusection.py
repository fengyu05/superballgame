# -*- coding:gb2312 -*-
# -*- $Id: menusection.py 2 2009-04-20 03:10:36Z fengyu05 $ -*-
import sys
import pygame
from pygame.locals import *
import gamectrl.const as const
from gamectrl.gamectrl import GameCtrl , GameSection
import ui.menu as menu



# 游戏菜单Section
class MenuSection(GameSection):

	def __init__(self):
		super(MenuSection, self).__init__()
		pygame.display.set_caption("Super Ball Game!!")

		self.text = self.font.render("Welcome to Super Ball Game !",1, const.COLOR_WHITE)

		# 按键回调处理
		def new_game():
			self.state = 1
		def load_game():
			self.ctrl.go_to_section(const.BALL_SECTION)
			ball_section = self.ctrl.get_section(const.BALL_SECTION)
			ball_section.load_game()

		self.menu = menu.Menu(
				self.screen,
				"Menu",
				[
					['New Game', new_game],
					['Load Game', load_game],
					['About Us', sys.exit],
					['Quit & Bye', sys.exit],
				],
				font = self.font
				)

		self.state = 0
		lis = []
		def start_game(i):
			self.ctrl.go_to_section(const.BALL_SECTION, (i,))

		for i in xrange(1, min(const.OPEN_LEVEL, const.MAX_LEVEL) + 1):
			lis.append( ['Level %d' % i , start_game, [i]] )

		self.select_menu = menu.Menu(
				self.screen,
				"Select Level",
				lis,
				font = self.font
				)

	def render(self):
		self.screen.fill(const.COLOR_BLACK)
		self.screen.blit(self.text, (50,50))
		if self.state == 0:
			self.menu.draw(self.screen)
		else:
			self.select_menu.draw(self.screen)

		super(MenuSection, self).render()

	def handle_event(self,event):
		if self.state == 0:
			self.menu.event(event)
		else:
			self.select_menu.event(event)

