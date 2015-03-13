# -*- coding:gb2312 -*-
# -*- $Id: main.py 2 2009-04-20 03:10:36Z fengyu05 $ -*-


import sys
import os
import pygame
from pygame.locals import *
import gamectrl.const as const
from gamectrl.gamectrl import GameCtrl , GameSection
from section.menusection import MenuSection
from section.ballsection import BallSection
from section.oversection import OverSection
from logic.gamelogic import GameLogic



if __name__ == '__main__':
	# 创建逻辑
	game_logic = GameLogic()
	game_ctrl = GameCtrl(game_logic)

	# 创建游戏Section
	menu_section = MenuSection()
	ball_section = BallSection()
	over_section = OverSection()

	# 绑定Section
	game_ctrl.add_section(menu_section, const.MENU_SECTION)
	game_ctrl.add_section(ball_section, const.BALL_SECTION)
	game_ctrl.add_section(over_section, const.OVER_SECTION)

	# 开始
	game_ctrl.start_main_loop(const.MENU_SECTION)
	#game_ctrl.start_main_loop(const.BALL_SECTION)
