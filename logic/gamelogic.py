# -*- coding:gb2312 -*-
# -*- $Id: gamelogic.py 2 2009-04-20 03:10:36Z fengyu05 $ -*-



import gamectrl.const as const
from logic.brickmanager import BrickManager, BrickType, Brick
from logic.itemmanager import ItemManager
import logic.ctrlbar as ctrlbar
import logic.ball as ball
from collections import deque
import math
import random

class GameLogic(object):

	def __init__(self):
		self.brick_manager = BrickManager()
		self.brick_manager.init_brick_type()
		self.item_manager = ItemManager()
		self.item_manager.init_item_types()

	def logic_start(self, level):
		#初始化网格
		self.brick_manager.init_grids()
		self.brick_manager.create_gridmap(level)
		self.item_manager.init_items()

		self.ctrl_bar = ctrlbar.CtrlBar()
		self.ball = ball.Ball()

		# 初始化参数
		self.level = level
		self.game_over = False
		self.win = False
		self.next_following_time = const.NEXT_FOLLOWING_TIME



	# 砖块向下压
	def add_line(self):
		self.brick_manager.add_line()
		self.item_manager.on_add_line()

		if self.brick_manager.is_following_down():
			self.game_over = True

	def logic_end(self):
		pass

	def logic_restart(self, level):
		self.logic_end(self)
		self.logic_start(self, level)

	# 玩家控制处理传递
	def player_move(self, tag, time):
		self.ctrl_bar.move(tag, time)

	# 玩家尝试使用技能
	def player_use_skill(self):
		if self.ctrl_bar.energy >= const.CTRL_SKILL_ENERYG:
			self.ctrl_bar.energy -= const.CTRL_SKILL_ENERYG
			self.ball.suspend_speed(const.BALL_SKILL_TIME)
			#self.ball.set_angle( random.uniform(0, 2 * math.pi))

			cur_x = int(self.ball.pos[0] / const.GRID_SIZE)
			cur_y = int(self.ball.pos[1] / const.GRID_SIZE)
			self.brick_manager.handle_skill(cur_x, cur_y, self.ball.power_type, 1, self.item_manager)
			return True
		return False

	# 玩家尝试使用道具
	def player_use_item(self, pos):
		item_type = self.ctrl_bar.use_item(pos)
		if item_type!= None:
			self.perform_item(item_type)
			return True
		return False

	#
	def perform_item(self, item_type_id):
		item_type = self.item_manager.get_item_type(item_type_id)
		type_id = item_type.type
		last_time = item_type.last_time
		name = item_type.name
		if item_type.type == const.ITEM_TYPE_TIME_SLOW:
			self.ball.record_use_item(last_time, type_id, name)
			self.ball.set_speed(const.BALL_SLOW_SPEED)
		elif item_type.type == const.ITEM_TYPE_ADD_DAMAGE:
			self.ball.record_use_item(last_time, type_id, name)
			self.ball.damage *= 3
		elif item_type.type == const.ITEM_TYPE_ADD_BAR_ACC:
			self.ctrl_bar.record_use_item(last_time, type_id, name)
			self.ctrl_bar.acceleration *= 3
			self.ctrl_bar.limit_speed *= 3
			self.ctrl_bar.speed_weaken *= 3
		elif item_type.type == const.ITEM_TYPE_ADD_BAR_LEN:
			self.ctrl_bar.record_use_item(last_time, type_id, name)
			self.ctrl_bar._just_use_flag = 1 # 标记刚取得
			self.ctrl_bar.width *= 2
		elif item_type.type <= const.ITEM_TYPE_POWER:
			self.ctrl_bar.change_power(item_type.type)
			self.ball.suspend_speed(const.BALL_SKILL_TIME)


	# 返回 1 , 控制栏伸长 -1 , 缩短 0 ,无
	def change_ctrl_len(self):
		if self.ctrl_bar.used_item_type == const.ITEM_TYPE_ADD_BAR_LEN:
			if self.ctrl_bar._just_use_flag > 0:
				self.ctrl_bar._just_use_flag = -1
				return 1
			else:
				return 0
		else:
			if self.ctrl_bar._just_use_flag < 0:
				self.ctrl_bar._just_use_flag = 0
				return -1
			else:
				return 0

	# 返回:  是否死亡,是否撞击, 砖头改变的砖块
	def update(self, time):

		if self.brick_manager.is_win():
			self.win = True
		# update the ball position
		bricks_collide , is_hit_bar = self.ball.update(self.level, self.brick_manager, self.ctrl_bar, time)

		# 球落下
		if self.ball.kill:
			self.ctrl_bar.life -= const.BALL_DAMAGE[self.ball.power_type]
			self.ball.on_kill()
			self.ctrl_bar.on_kill()
			return True, False, []

		# 砖头与球碰撞
		if len(bricks_collide) > 0:
			for brick in bricks_collide:
				if brick.status == const.BRICK_DEATH:
					add_en = brick.brick_type.life / const.BRICK_ENERGY_RATE
					self.ctrl_bar.add_energy(add_en)
					self.ctrl_bar.scores += brick.brick_type.scores
					if brick.has_item:
						self.item_manager.drop_item_at(brick.x_index, brick.y_index)

		# update the ctrl bar position
		self.ctrl_bar.update(time)

		return False, is_hit_bar, bricks_collide

	# 道具更新, 返回: 新加入的道具列表, 消失的道具列表, 玩家获得的道具列表
	def item_update(self, time):
		return self.item_manager.update(self.level, self.brick_manager.grids, self.ctrl_bar, self.ball, time)

	# 升级, 暂时为下压一行
	def line_following_update(self, deta_time):
		self.next_following_time -= deta_time
		if self.next_following_time < 0:
			self.next_following_time = const.NEXT_FOLLOWING_TIME
			self.add_line()
			return True
		return False


	def get_brick_at(self, x, y):
		return self.brick_manager.grids[y][x]


	def set_brick_at(self, x, y, val=None):
		self.brick_manager.grids[y][x] = val

	def get_item(self, item_id):
		return self.item_manager.itemdict[item_id]
