# -*- coding: gb2312 -*-
# -*- $Id: ctrlbar.py 2 2009-04-20 03:10:36Z fengyu05 $ -*-

import gamectrl.const as const
import math
import random


# CtrlBar�࣬���û����Ƶ�CtrlBar�����߼��ϵ����ݴ���
class CtrlBar(object):

	def __init__(self, style=0, power_type=const.INIT_POWER_TYPE):
		self.speed = 0
		self.status = 0  # ��ʼû���κ�״̬���������֮��仯
		self.style = style # 0Ϊ�²��ƶ��ģ�1Ϊ�ϲ��ƶ���
		self.life = const.CTRL_BAR_LIFE
		self.energy = 0
		self.pos = const.CTRL_BAR_INIT_POS
		self.scores = 0

		# ��ʼ��pwoer_type
		self.change_power(power_type)

		# ��ʼ��������
		self.itemboxs = [0] * (const.ITEMBOX_SIZE + 1) # ���һ��λ��Ϊ ����
		# �Ƿ�ʹ���˵���
		self.used_item_type = None
		self.item_last_time = 0
		self.used_item_name = None

		self._just_use_flag = 0

	# �ı����������������
	def change_power(self, power_type=const.FIRE):
		# ���°���power_type��صı���
		self.power_type = power_type

		self.width = const.CTRL_BAR_WIDTH
		self.height = const.CTRL_BAR_HEIGHT

		self.acceleration = const.CTRL_ACCELERATION[power_type]
		self.limit_speed = const.CTRL_MAX_SPEED[power_type]
		self.speed_weaken = const.CTRL_SPEED_WEAKEN[power_type]
		self.friction = const.CTRL_FRICTION[power_type]
		self.max_life = const.CTRL_MAX_LIFE[power_type]
		self.max_acceleration = const.CTRL_MAX_ACCELERATION[power_type]
		self.max_energy = const.CTRL_MAX_ENERGY[power_type]

	def add_energy(self, val):
		self.energy += val
		if self.energy > self.max_energy:
			self.energy = self.max_energy

	def add_life(self, val):
		self.life += val
		if self.life > self.max_life:
			self.life = self.max_life
		elif self.life <=0:
			self.life = 1

	def get_item(self, item_type):
		for i in range(const.ITEMBOX_SIZE):
			if self.itemboxs[i] == 0:
				self.itemboxs[i] = item_type
				break

	# ����ʹ�õ���, �ɹ����ص�������, ���򷵻�None
	def use_item(self, pos):
		if self.itemboxs[pos]!=0:
			item_type = self.itemboxs[pos]
			self.itemboxs[pos] = 0
			for i in range(pos, const.ITEMBOX_SIZE):
				self.itemboxs[i] = self.itemboxs[i + 1]
			return item_type
		return None

	def update_item_effect(self, time):
		if self.used_item_type:
			self.item_last_time -= time
			if self.item_last_time < 0:
				self.used_item_type = None
				self.used_item_name = None
				# �ָ�Ч�� = ���°󶨲���
				self.change_power(self.power_type)

	# ��¼ʹ���˵���
	def record_use_item(self, time, type, name):
		if self.used_item_type != None:
			# �Ѿ�ʹ���˵���, �ظ�����Ч��
			self.change_power(self.power_type)
		self.used_item_type = type
		self.item_last_time = time
		self.used_item_name = name

	# ����bar���ƶ���������bar���²���ctrl_bar
	def move(self, tag, time):
		if self.style == const.CTRL_BAR_STYLE_BOTTOM:
			self._movex(tag, time)
		else:
			self._movey(tag, time)

	# �����²���ctrl_bar���ƶ�
	# 1.����һ�κ����ٶ����ż��ٶȱ仯һ��
	# 2.�����ٶ��ƶ�λ��
	def _movex(self, tag, time):
		halfwidth = self.width / 2
		nextposx = self.pos[0]

		if tag == const.LEFT: # left
			self.speed -= self.acceleration
		else:
			self.speed += self.acceleration
		if self.speed <= -self.limit_speed:
			self.speed = -self.limit_speed
		if self.speed >= self.limit_speed:
			self.speed = self.limit_speed

		nextposx += self.speed * time
		# �ж����Ƿ���ײ�߽磬������
		hit_res = self._is_hit_edge(nextposx, const.CTRL_BAR_STYLE_BOTTOM)
		if hit_res:
			self.on_hit_edge(hit_res, const.CTRL_BAR_STYLE_BOTTOM, nextposx)
			self.speed = 0
			return

		nextpos = (nextposx, self.pos[1])
		self.pos = nextpos

	# �����������ҵ�ctrl_bar���ƶ�
	def _movey(self, tag, time):
		halfheight = self.height / 2
		nextposy = self.pos[1]
		if tag == const.UP: # up
			self.speed -= self.acceleration
		else:
			self.speed += self.acceleration
		if self.speed <= -self.limit_speed:
			self.speed = -self.limit_speed
		if self.speed >= self.limit_speed:
			self.speed = self.limit_speed

		nextposy += self.speed * time
		#�ж����Ƿ���ײ���±߽�
		hit_res = self._is_hit_edge(nextposy, const.CTRL_BAR_STYLE_SIDES)
		if hit_res:
			self.on_hit_edge(hit_res, const.CTRL_BAR_STYLE_SIDES, nextposy)
			self.speed = 0
			return

		nextpos = (self.pos[0], nextposy)
		self.pos = nextpos

	# ��bar��λ�ý��и���
	# bar��û�����û�а����һ��������ƶ���ʱ�������ٶ�
	# ����λ���ƶ�����������Ħ�������ٶȼ��٣�����ͣ��
	def update(self, time):
		# ���µ���Ч��
		self.update_item_effect(time)
		# �ٶ�˥��
		if self.speed > 0:
			self.speed -= self.speed_weaken
		elif self.speed < 0:
			self.speed += self.speed_weaken
		# bar��Ȼ�ƶ�
		if self.style == const.CTRL_BAR_STYLE_BOTTOM:
			nextposx = self.pos[0]
			nextposx += self.speed * time
			# �ж����Ƿ񵽱߽�
			hit_res = self._is_hit_edge(nextposx, const.CTRL_BAR_STYLE_BOTTOM)
			if hit_res:
				self.on_hit_edge(hit_res, const.CTRL_BAR_STYLE_BOTTOM, nextposx)
				return
		else:
			nextposy = self.pos[1]
			nextposy += self.speed * time
			self.pos = (self.pos[0], nextposy)

		nextpos = (nextposx, self.pos[1])
		self.pos = nextpos

	# Ԥ���ӿڣ����������ײ������������˺�
	def on_ball_hit(self):
		pass

	# ��bar�Ƿ���ײ���˱߽�����ж�
	def _is_hit_edge(self, pos, tag):
		halfwidth = self.width / 2
		brickheight = const.GRID_SIZE
		win_width = const.MAIN_WIN_WIDTH
		if tag == const.CTRL_BAR_STYLE_BOTTOM:
			if pos <= halfwidth + brickheight:
				return const.LEFT
			if pos >= win_width - brickheight - halfwidth:
				return const.RIGHT
			return False
		else:
			if pos <= halfwidth:
				return const.UP
			if pos >= self.pos[1]- halfwidth:
				return const.DOWN

	# ���bar��ײ���˱߽磬���д���
	# �ٶȲ�Ϊ��Ļ���Ϊ�㣬λ���ƶ�����׼��ײ��λ��
	def on_hit_edge(self, tag, style_tag, pos):
		brickheight = const.GRID_SIZE
		halfwidth = self.width / 2
		win_width = const.MAIN_WIN_WIDTH

		nextposx = self.pos[0]
		nextposy = self.pos[1]
		if style_tag == const.CTRL_BAR_STYLE_BOTTOM:
			if tag == const.LEFT:
				nextposx = brickheight + halfwidth
			elif tag == const.RIGHT:
				nextposx = win_width - brickheight - halfwidth
		else:
			if tag == const.UP:
				nextposy = halfwidth
			elif tag == const.DOWN:
				nextposy = self.pos[1] - halfwidth
		self.pos = (nextposx, nextposy)
		self.speed = 0

	# ���������������к���İ���
	def on_kill(self):
		self.pos = const.CTRL_BAR_INIT_POS
		self.speed = 0

	# �ԳԵ�����Ʒ�������ݸ���
	def on_eate(self, item):
		type = item.item_type
		if type.usage == False:
			if type.type == const.ITEM_TYPE_ADD_BAR_LIFE: # ������
				self.add_life(type.contain)
			if type.type == const.ITEM_TYPE_SUB_BAR_LIFE: # ������
				self.add_life(type.contain)
			if type.type == const.ITEM_TYPE_ADD_BAR_EN:  # ������
				self.add_energy(type.contain)
			'''if type.type == const.ITEM_TYPE_FIRE_BALL: # ��ɻ���
				self.change_power(const.FIRE)
			if type.type == const.ITEM_TYPE_ICE_BALL: # ��ɱ���
				self.change_power(const.ICE)
			if type.type == const.ITEM_TYPE_THUNDER_BALL: # ����׵���
				self.change_power(const.THUNDER)
			'''
		else:
			# ���ʹ�õ���
			self.get_item(type.type)

	def get_left(self):
		return self.pos[0] - self.width / 2

	def get_right(self):
		return self.pos[0] + self.width / 2
