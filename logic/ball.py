# -*- coding:gb2312 -*-
# -*- $Id: ball.py 2 2009-04-20 03:10:36Z fengyu05 $ -*-

import gamectrl.const as const
import math
import random


# Ball类，对球的运动和撞击进行逻辑上的的数据处理
class Ball(object):

	def __init__(self, power_type=const.INIT_POWER_TYPE):
		self.kill = False
		self.radius = const.BALL_RADIUS
		self.pos = const.BALL_INIT_POS
		self.angle = random.randint(225, 315) * math.pi / 180
		# 初始化power_type
		self.change_power(power_type)

		# 处理球停留的变量
		self.staytime = self.conststaytime
		self.staying = True
		self.startstay = True

		# 暂时停止球的运行的时间标记, 释放skill时需要
		self.suspend = None

		# 得到无敌道具时的处理, 不掉落
		self.no_drop = const.BALL_NOT_DROP

		# 是否使用了道具
		self.used_item_type = None
		self.item_last_time = 0
		self.used_item_name = None

	# 改变球的能量类型
	def change_power(self, power_type=const.FIRE):
		# 重新绑定与power_type相关的变量
		self.power_type = power_type
		self.speed = const.BALL_SPEED[power_type]
		self.damage = const.BALL_DAMAGE[power_type]
		self.conststaytime = const.BALL_STAY_TIME[power_type]
		self.damage_status = const.BALL_ABILITY[power_type] # 暂时无视

	def start_move(self):
		if self.startstay:
			self.staying = False
			self.startstay = False

	# 暂时停止球的运行, 释放skill时需要
	def suspend_speed(self, suspend_time):
		self.suspend = suspend_time

	def update_suspend(self, time):
		if self.suspend:
			self.suspend -= time
			if self.suspend < 0:
				self.suspend = None
			return True
		else:
			return False

	# 记录使用了道具
	def record_use_item(self, time, type, name):
		if self.used_item_type != None:
			# 已经使用了道具, 回复道具效果
			self.change_power(self.power_type)
		self.item_last_time = time
		self.used_item_type = type
		self.used_item_name = name

	def update_item_effect(self, time):
		if self.used_item_type:
			self.item_last_time -= time
			if self.item_last_time < 0:
				self.used_item_type = None
				self.used_item_name = None
				# 恢复效果 = 重新绑定参数
				self.change_power(self.power_type)

	def set_pos(self, pos):
		self.pos = pos

	def set_speed(self, speed):
		if speed > const.BALL_MAX_SPEED:
			self.speed = const.BALL_MAX_SPEED
		else:
			self.speed = speed

	def set_angle(self, angle):
		angle = angle % (2 * math.pi)
		# 微调角度，如果角度接近平行，增大角度
		if angle >= const.BALL_MIN_ANGLE[0][0] and angle < const.BALL_MIN_ANGLE[0][1]:
			angle += const.BALL_ANGLE_DELTA
		elif angle >= const.BALL_MIN_ANGLE[1][0] and angle < const.BALL_MIN_ANGLE[1][1]:
			angle -= const.BALL_ANGLE_DELTA
		elif angle >= const.BALL_MIN_ANGLE[2][0] and angle < const.BALL_MIN_ANGLE[2][1]:
			angle += const.BALL_ANGLE_DELTA
		elif angle >= const.BALL_MIN_ANGLE[3][0] and angle < const.BALL_MIN_ANGLE[3][1]:
			angle -= const.BALL_ANGLE_DELTA
		self.angle = angle

	# 预留接口，可能设计球可以直接吃掉掉落的物品
	def on_eat(self, thing):
		pass

	# 对球碰到砖块之后的方向和速度的处理
	def on_hit_brick(self, brick, tag, res):
		if tag == const.LEFT:
			self.set_angle(math.pi - self.angle)
		if tag == const.RIGHT:
			self.set_angle(math.pi - self.angle)
		if tag == const.UP:
			self.set_angle(2 * math.pi - self.angle)
		if tag == const.DOWN:
			self.set_angle(-self.angle)

		res.append(brick)
		brick.on_damage(self.damage)
		speed = (brick.brick_type.material - 5) * const.MATERIAL_FACTOR + self.speed
		# 最小将为默认速度
		if speed < self.speed:
			speed = const.BALL_SPEED[self.power_type]
		self.set_speed(speed)

	def on_hit_brick_corner(self, brick, nextpos, hitpos, distance, res):
		distancex = nextpos[0] - hitpos[0]
		angle = math.acos(distancex / distance)
		self.set_angle(angle)

		res.append(brick)
		brick.on_damage(self.damage)
		speed = (brick.brick_type.material - 5) * const.MATERIAL_FACTOR + self.speed
		if speed < const.BALL_SPEED[self.power_type]:
			speed = const.BALL_SPEED[self.power_type]
		self.set_speed(speed)

	# 预留接口， 可能设计球对掉落的物品有伤害
	def on_hit_thing(self):
		pass

	# 球掉落到了安全线一下或者是两边之外
	# 重新定义球的数据
	def on_kill(self):
		self.kill = False
		self.startstay = True
		self.staying = True
		self.death_pos = self.pos
		self.pos = const.BALL_INIT_POS
		self.set_speed(const.BALL_SPEED[self.power_type])
		angle = random.randint(225, 315) * math.pi / 180
		self.set_angle(angle)

	# 球碰撞到了ctrl_bar的处理
	# 由于受到bar的摩擦，球的角度改变，速度不变
	def on_hit_ctrl_bar(self, bar, tag):
		if tag == const.CTRL_BAR_STYLE_BOTTOM:
			speedx = math.cos(self.angle) * self.speed
			speedy = math.sin(self.angle) * self.speed
			speedx += bar.speed * bar.friction
			if speedx >= 0:
				speedx = max(speedx, const.BALL_MIN_SPEEDX)
			if speedx < 0:
				speedx = -max(speedx, const.BALL_MIN_SPEEDX)
			self.set_angle(-math.atan2(speedy , speedx))
			hit_posy = bar.pos[1] - self.radius
			self.pos = (self.pos[0], hit_posy)
		else:
			pass

	# 球碰撞到了ctrl_bar的角的处理，角碰撞不会有停留时间
	# 为了增加球的y方向的速度和玩家一种“英雄”救球的感觉
	# 在球和ctrl_bar的边角小于某个角度时让球以较大角度和不小于bar的速度发射
	def on_hit_bar_corner(self, bar, styletag, nextpos, postag):
		if styletag == const.CTRL_BAR_STYLE_BOTTOM:
			distance = self.distance
			leftx = abs(nextpos[0] - bar.get_left())
			rightx = abs(nextpos[0] - bar.get_right())

			if postag == const.LEFT:
				angle = math.pi + math.acos(leftx / distance)
				if angle < const.BALL_SAVE_MIN_ANGLE:
					angle = const.BALL_SAVE_MIN_ANGLE
			if postag == const.RIGHT:
				angle = 2 * math.pi - math.acos(rightx / distance)
				if angle > const.BALL_SAVE_MAX_ANGLE:
					angle = const.BALL_SAVE_MAX_ANGLE

			speedx = abs(math.cos(angle) * self.speed)
			if abs(speedx) < math.fabs(bar.speed):
				# 处理救球时候可能出现的除零错误
				alpha = max(abs(math.cos(angle)), const.BALL_MIN_DETA)
				self.set_speed(abs(bar.speed) / alpha)
			self.set_angle(angle)
		else:
			pass

	# 根据ctrlbar的质地，使球在bar上有一个短暂的停留，符合物理规律
	# 并且随着自己的速度在bar上移动
	def on_staying(self, bar, time):
		if self.staytime <= 0:
			self.staytime = self.conststaytime
			self.staying = False
		else:
			# 停留在bar上
			# 并且根据自己的x轴速度水平移动
			# 若停留时间比较长不会突兀
			if self.startstay:
				return
			self.staytime -= time
			speedx = math.cos(self.angle) * self.speed
			nextposx = self.pos[0] + speedx * time
			self.pos = (nextposx, self.pos[1])

	# 对球碰撞到了屏幕的上表面进行方向和位置的处理
	def on_hit_wall(self, tag):
		if tag == const.SIDES_WALL_TAG:
			pass
		else:
			self.set_angle(2 * math.pi - self.angle)
			# 移动到与墙碰撞的位置
			hit_posy = self.radius
			self.pos = (self.pos[0], hit_posy)

	# 对球碰撞到了屏幕底进行角度的处理
	# 留此接口为以后无敌物品使用
	def on_no_drop(self):
		self.set_angle(-self.angle)

	# 根据时间对球的状态进行更新
	# 更新位置的数据，是否碰撞，处理
	# 返回 碰撞到得砖头, 是否碰撞控制栏
	def update(self, level, brickmanager, bottombar, time):
		if self.update_suspend(time):
			return [], False
		if self.startstay:
			self.pos = bottombar.pos
			return [], False
		self.update_item_effect(time)
		angle = self.angle
		nextposx = self.pos[0] + time * self.speed * math.cos(angle)
		nextposy = self.pos[1] + time * self.speed * math.sin(angle)
		nextpos = (nextposx, nextposy)

		need_pos = False
		# 撞到上墙
		if self._is_hit_up(nextpos):
			self.on_hit_wall(const.UP_WALL_TAG)
			need_pos = True
		# 掉落死亡
		if self.no_drop:
			if self._is_kill(nextpos):
				self.on_no_drop()
				need_pos = True
		else:
			if self._is_kill(nextpos):
				self.kill = True
				need_pos = True
		# 检测与bottom ctrl bar 的碰撞
		is_hit_bar = False
		if self.staying:
			self.on_staying(bottombar, time)
			need_pos = True
		else:
			hit_res = self._is_hit_bottom_bar(bottombar, nextpos)
			if hit_res:
				is_hit_bar = True

			# 如果ball 与ctrl_bar 的 power_type 不同, 改变ball的power_type
			if hit_res and self.power_type != bottombar.power_type:
				self.change_power(bottombar.power_type)

			if hit_res == const.BALL_HIT_BAR_MID:
				self.on_hit_ctrl_bar(bottombar, const.CTRL_BAR_STYLE_BOTTOM)
				need_pos = True
			elif hit_res == const.LEFT or hit_res == const.RIGHT:
				self.on_hit_bar_corner(bottombar, const.CTRL_BAR_STYLE_BOTTOM, nextpos, hit_res)
				need_pos = True

		# 处理和brick的碰撞
		res = []
		self.update_hit_brick(brickmanager, nextpos, res)
		if len(res):
			need_pos = True

		if not need_pos:
			self.pos = nextpos

		return res, is_hit_bar

	# 对球是否碰撞到上面的墙进行判断
	def _is_hit_up(self, pos):
		ball_radius = const.BALL_RADIUS
		if pos[1] <= 0 + ball_radius:
			return True
		else:
			return False

	# 对球是否死亡进行判断
	def _is_kill(self, pos):
		if pos[1] > const.DROP_LINE:
			return True
		else:
			return False

	# 对球是否碰撞到ctrl_bar进行判断
	def _is_hit_bottom_bar(self, bar, nextpos):
		barleft = bar.get_left()
		barright = bar.get_right()
		barup = bar.pos[1] - self.radius
		bardown = bar.pos[1]
		res = -1

		if math.sin(self.angle) > 0:
			if nextpos[0] >=barleft and nextpos[0] <= barright:
				if nextpos[1] >= barup and nextpos[1] <= const.SAVE_LINE:
					self.staying = True
					return const.BALL_HIT_BAR_MID # 碰到中部

			else:
				if nextpos[1] >= barup and nextpos[1] <= const.SAVE_LINE:
					if nextpos[0] <= barleft:
						self.distance = self.calcu_distance(nextpos, (barleft, bar.pos[1]))
						res = const.LEFT
					elif nextpos[0] >= barright:
						self.distance = self.calcu_distance(nextpos, (barright, bar.pos[1]))
						res = const.RIGHT
		if not res == -1:
			if self.distance <= self.radius * 1.2:
				return res

		return False

	# 判断并处理球对砖块的碰撞
	# 1.首先计算球在网格中的位置
	# 2.把网格的上下左右边界计算出来
	# 3.看看以球现在的速度，下个位置是否发生碰撞
	# 4.发生碰撞的话就处理碰撞
	# 5.并且判断继续进行是否碰到其他位置的判断处理（可能碰到两个位置）
	def update_hit_brick(self, brickmanager, nextpos, res):
		# 计算下个位置所在的网格位置x y
		cur_x = int(nextpos[0] / const.GRID_SIZE)
		cur_y = int(nextpos[1] / const.GRID_SIZE)

		upline = cur_y * const.GRID_SIZE
		leftline = cur_x * const.GRID_SIZE
		downline = upline + const.GRID_SIZE
		rightline = leftline + const.GRID_SIZE

		offset_bricks = (
				brickmanager.try_get_brick(cur_x - 1, cur_y),
				brickmanager.try_get_brick(cur_x + 1, cur_y),
				brickmanager.try_get_brick(cur_x, cur_y - 1),
				brickmanager.try_get_brick(cur_x, cur_y + 1),
				)

		if nextpos[0] - self.radius <= leftline: # left
			if offset_bricks[0]:
				self.on_hit_brick(offset_bricks[0], const.LEFT, res)
				self.pos = (leftline + self.radius, self.pos[1])
		if nextpos[0] + self.radius >= rightline: # right
			if offset_bricks[1]:
				self.on_hit_brick(offset_bricks[1], const.RIGHT, res)
				self.pos = (rightline - self.radius, self.pos[1])
		if nextpos[1] - self.radius <= upline: # up
			if offset_bricks[2]:
				self.on_hit_brick(offset_bricks[2], const.UP, res)
				self.pos = (self.pos[0], upline + self.radius)
		if nextpos[1] + self.radius >= downline: # down
			if offset_bricks[3]:
				self.on_hit_brick(offset_bricks[3], const.DOWN, res)
				self.pos = (self.pos[0], downline - self.radius)

		# 角碰撞
		# 四个顶点,按照四个象限排序
		bottomright = (rightline, downline)
		bottomleft = (leftline, downline)
		topleft = (leftline, upline)
		topright = (rightline, upline)
		# 有没有砖块，按照四个象限排序
		offset_bricks = (
				0, # 填充用
				brickmanager.try_get_brick(cur_x + 1, cur_y + 1),
				brickmanager.try_get_brick(cur_x - 1, cur_y + 1),
				brickmanager.try_get_brick(cur_x - 1, cur_y - 1),
				brickmanager.try_get_brick(cur_x + 1, cur_y - 1)
				)
		# 需要计算是否碰撞的顶点
		hit = (0, 0, 0)
		if cur_x - 1 <= 0 or cur_x + 1 >= const.GRID_NUM_X - 1:
			return

		distance = (
				0, # 填充用
				self.calcu_distance(nextpos, bottomright),
				self.calcu_distance(nextpos, bottomleft),
				self.calcu_distance(nextpos, topleft),
				self.calcu_distance(nextpos, topright),
				)

		hit_vertex = (
				0, # 填充用
				bottomright,
				bottomleft,
				topleft,
				topright
				)

		if len(res) == 0:
			angle = self.angle
			if angle < const.BALL_FIRST_QURD:
				hit = (0, 1, 2, 4)
			elif angle < const.BALL_SECOND_QURD:
				hit = (0, 1, 2, 3)
			elif angle <= const.BALL_THIRD_QURD:
				hit = (0, 2, 3, 4)
			elif angle <= const.BALL_FORTH_QURD:
				hit = (0, 1, 3, 4)

			for index in xrange(1, 4):
				if offset_bricks[hit[index]] and distance[hit[index]] <= self.radius * 1.1:
					self.on_hit_brick_corner(offset_bricks[hit[index]], \
							nextpos, hit_vertex[hit[index]], distance[hit[index]], res)
					break

	# 计算两点的距离
	def calcu_distance(self, pos1, pos2):
		distance = (pos1[0] - pos2[0]) ** 2
		distance += (pos1[1] - pos2[1]) ** 2
		return math.sqrt(distance)
