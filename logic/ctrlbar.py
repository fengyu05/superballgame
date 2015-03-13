# -*- coding: gb2312 -*-
# -*- $Id: ctrlbar.py 2 2009-04-20 03:10:36Z fengyu05 $ -*-

import gamectrl.const as const
import math
import random


# CtrlBar类，对用户控制的CtrlBar进行逻辑上的数据处理
class CtrlBar(object):

	def __init__(self, style=0, power_type=const.INIT_POWER_TYPE):
		self.speed = 0
		self.status = 0  # 初始没有任何状态，被球击中之后变化
		self.style = style # 0为下部移动的，1为上部移动的
		self.life = const.CTRL_BAR_LIFE
		self.energy = 0
		self.pos = const.CTRL_BAR_INIT_POS
		self.scores = 0

		# 初始化pwoer_type
		self.change_power(power_type)

		# 初始化道具栏
		self.itemboxs = [0] * (const.ITEMBOX_SIZE + 1) # 最后一个位置为 保卫
		# 是否使用了道具
		self.used_item_type = None
		self.item_last_time = 0
		self.used_item_name = None

		self._just_use_flag = 0

	# 改变控制栏的能量类型
	def change_power(self, power_type=const.FIRE):
		# 重新绑定与power_type相关的变量
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

	# 尝试使用道具, 成功返回道具类型, 否则返回None
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
				# 恢复效果 = 重新绑定参数
				self.change_power(self.power_type)

	# 记录使用了道具
	def record_use_item(self, time, type, name):
		if self.used_item_type != None:
			# 已经使用了道具, 回复道具效果
			self.change_power(self.power_type)
		self.used_item_type = type
		self.item_last_time = time
		self.used_item_name = name

	# 控制bar的移动，分左右bar和下部的ctrl_bar
	def move(self, tag, time):
		if self.style == const.CTRL_BAR_STYLE_BOTTOM:
			self._movex(tag, time)
		else:
			self._movey(tag, time)

	# 控制下部的ctrl_bar的移动
	# 1.调用一次函数速度随着加速度变化一次
	# 2.根据速度移动位置
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
		# 判断其是否碰撞边界，并处理
		hit_res = self._is_hit_edge(nextposx, const.CTRL_BAR_STYLE_BOTTOM)
		if hit_res:
			self.on_hit_edge(hit_res, const.CTRL_BAR_STYLE_BOTTOM, nextposx)
			self.speed = 0
			return

		nextpos = (nextposx, self.pos[1])
		self.pos = nextpos

	# 将来控制左右的ctrl_bar的移动
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
		#判断其是否碰撞上下边界
		hit_res = self._is_hit_edge(nextposy, const.CTRL_BAR_STYLE_SIDES)
		if hit_res:
			self.on_hit_edge(hit_res, const.CTRL_BAR_STYLE_SIDES, nextposy)
			self.speed = 0
			return

		nextpos = (self.pos[0], nextposy)
		self.pos = nextpos

	# 对bar的位置进行更新
	# bar在没有玩家没有按左右或者上下移动的时候仍有速度
	# 所以位置移动，但是由于摩擦力，速度减少，最终停下
	def update(self, time):
		# 更新道具效果
		self.update_item_effect(time)
		# 速度衰减
		if self.speed > 0:
			self.speed -= self.speed_weaken
		elif self.speed < 0:
			self.speed += self.speed_weaken
		# bar仍然移动
		if self.style == const.CTRL_BAR_STYLE_BOTTOM:
			nextposx = self.pos[0]
			nextposx += self.speed * time
			# 判断其是否到边界
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

	# 预留接口，可能球的碰撞会产生生命的伤害
	def on_ball_hit(self):
		pass

	# 对bar是否碰撞到了边界进行判断
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

	# 如果bar碰撞到了边界，进行处理
	# 速度不为零的话设为零，位置移动到标准碰撞的位置
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

	# 对生命的死亡进行合理的安排
	def on_kill(self):
		self.pos = const.CTRL_BAR_INIT_POS
		self.speed = 0

	# 对吃到了物品进行数据更新
	def on_eate(self, item):
		type = item.item_type
		if type.usage == False:
			if type.type == const.ITEM_TYPE_ADD_BAR_LIFE: # 加生命
				self.add_life(type.contain)
			if type.type == const.ITEM_TYPE_SUB_BAR_LIFE: # 加生命
				self.add_life(type.contain)
			if type.type == const.ITEM_TYPE_ADD_BAR_EN:  # 加能量
				self.add_energy(type.contain)
			'''if type.type == const.ITEM_TYPE_FIRE_BALL: # 变成火球
				self.change_power(const.FIRE)
			if type.type == const.ITEM_TYPE_ICE_BALL: # 变成冰球
				self.change_power(const.ICE)
			if type.type == const.ITEM_TYPE_THUNDER_BALL: # 变成雷电球
				self.change_power(const.THUNDER)
			'''
		else:
			# 获得使用道具
			self.get_item(type.type)

	def get_left(self):
		return self.pos[0] - self.width / 2

	def get_right(self):
		return self.pos[0] + self.width / 2
