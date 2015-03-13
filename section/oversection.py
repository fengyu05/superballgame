# -*- coding:gb2312 -*-
# -*- $Id: oversection.py 2 2009-04-20 03:10:36Z fengyu05 $ -*-
import sys
import pygame
from pygame.locals import *
import gamectrl.const as const
from gamectrl.gamectrl import GameCtrl , GameSection
import ui.menu as menu




class OverSection(GameSection):

	def __init__(self):
		super(OverSection, self).__init__()

		self.text = self.font.render("Oh,!!!!",1, const.COLOR_WHITE)
		def new_game():
			self.ctrl.go_to_section(const.BALL_SECTION)
		def return_to_menu():
			self.ctrl.go_to_section(const.MENU_SECTION)
		def load_game():
			self.ctrl.go_to_section(const.BALL_SECTION)
			ball_section = self.ctrl.get_section(const.BALL_SECTION)
			ball_section.load_game()

		self.menu = menu.Menu(
				self.screen,
				"GameOver",
				[
					['Try Again', new_game],
					['Load Game', load_game],
					['Return to Menu', return_to_menu],
					['Quit & Bye', sys.exit],
				],
				font = self.font
				)

		self.level = 0
		self.next_menu = menu.Menu(
				self.screen,
				"Level Clean",
				[
					['Next Level', self.next_level],
					['Quit & Bye', sys.exit],
				],
				font = self.font
				)

	def next_level(self):
		if self.level == min(const.OPEN_LEVEL,const.MAX_LEVEL):
			sys.exit()
		self.ctrl.go_to_section(const.BALL_SECTION, (self.level + 1,) )

	def init(self, init_args):
		self.level = init_args[0]

	def render(self):
		self.screen.fill(const.COLOR_BLACK)
		self.screen.blit(self.text, (50,50))
		if self.level == 0:
			self.menu.draw(self.screen)
		else:
			self.next_menu.draw(self.screen)
		super(OverSection, self).render()

	def handle_event(self,event):
		if self.level == 0:
			self.menu.event(event)
		else:
			self.next_menu.event(event)

