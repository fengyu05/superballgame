# -*- coding:gb2312 -*-
# -*- $Id: gamectrl.py 2 2009-04-20 03:10:36Z fengyu05 $ -*-

import sys
import pygame
import const
from pygame.locals import *

__all__ = ['GameSection','GameCtrl']


# ��ϷSection�Ļ���, �½�Section�����̳�
class GameSection(object):

	def __init__(self):
		self.win_size = const.WIN_SIZE
		self.screen = pygame.Surface(const.WIN_SIZE)
		self.real_screen = pygame.display.set_mode(const.WIN_SIZE, RESIZABLE)

		self.font = pygame.font.Font('res\\fonts\\levity.ttf',24)

	# �¼������
	def handle_key_down(self, event):
		key = event.key
		if key == K_ESCAPE:
			sys.exit()

	def handle_mouse_up(self, event):
		pass


	def handle_event(self, event):
		pass

	# ��ʼ��, �ڿ�ʼ��ѭ��ǰ����
	def init(self, init_args=None):
		pass

	# �߼�����
	def update(self, deta_time):
		pass

	# ��Ⱦ
	def render(self):
		screen = self.screen
		if self.win_size != const.WIN_SIZE:
			screen = pygame.transform.scale(screen, self.win_size)
		self.real_screen.blit(screen,(0,0))

	def end(self):
		pass

# ��Ϸ������, ʹ����������Section֮��Ľ���, ���Ҷ���ѭ����ܽ��з�װ
class GameCtrl(object):

	def __init__(self, logic):
		self.logic = logic
		self.sections = {}
		self.is_end = False
		self.section_id = -1
		self.cur_section = None

		pygame.mixer.pre_init(const.SOUND_DEFALUT_FREQUENCY, -16, 1,const.SOUND_BUFFER)
		pygame.init()
		self.clock = pygame.time.Clock()

		self.normal_deta_time = 1.0/const.FPS
		self.delay_time = 0.0
		self.tolerate_time = 0.1

		self.escape_render = False # �Ƿ������Ⱦ֡

	# ���Section
	def add_section(self, section, section_id):
		section.ctrl = self
		section.logic = self.logic
		self.sections[section_id]=section

	# ����Section
	def get_section(self, id):
		return self.sections[id]

	# ת�Ƶ�ָ��Section
	def go_to_section(self, id, init_args=None):
		self.cur_section.end()
		self.section_id = id
		self.cur_section = self.sections[id]
		self.cur_section.init(init_args)

	def toggle_escape_render(self):
		self.escape_render = not self.escape_render

	# ��ʼ��ѭ��
	def start_main_loop(self, section_id):
		self.section_id = section_id
		try:
			self.cur_section = self.sections[self.section_id]
		except IndexError:
			raise SystemError, "No main logic section"
		self.cur_section.init(None)
		self.ticks = pygame.time.get_ticks()
		while not self.is_end:
			self.clock.tick(const.FPS)
			if self.cur_section == None:
				sys.exit()

			# �¼�����
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:
					self.is_end = True
					break
				elif event.type == VIDEORESIZE:
					self.cur_section.win_size = event.size
					self.cur_section.real_screen = pygame.display.set_mode(event.size, RESIZABLE)
				elif event.type == KEYDOWN:
					if event.key == K_r:
						self.toggle_escape_render()
					self.cur_section.handle_key_down(event)
				elif event.type == MOUSEBUTTONUP:
					self.cur_section.handle_mouse_up(event)

				self.cur_section.handle_event(event)

			# ����ʵ�ʾ�����ʱ��
			now_ticks = pygame.time.get_ticks()
			deta = now_ticks - self.ticks
			self.ticks = now_ticks

			# ��ʱ�侭����ʱ����ִ���߼�֡
			delta_time = 1.0 * deta / 1000.0
			amount = 0 # ��¼�߼�ִ֡�д���
			while delta_time > 0:
				if delta_time <= const.MIN_TIME:
					self.cur_section.update(delta_time)
				else:
					self.cur_section.update(const.MIN_TIME)
				amount += 1
				delta_time -= const.MIN_TIME
				if amount >= const.MIN_RENDER_AMOUNT or delta_time <= 0:
					self.cur_section.render()
					amount -= const.MIN_RENDER_AMOUNT

			pygame.display.flip()



