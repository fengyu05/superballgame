# -*- coding:gb2312 -*-
# -*- $Id: ball.py 2 2009-04-20 03:10:36Z fengyu05 $ -*-

import gamectrl.const as const
import math
import random


# Ball�࣬������˶���ײ�������߼��ϵĵ����ݴ���
class Ball(object):

	def __init__(self, power_type=const.INIT_POWER_TYPE):
		self.kill = False
		self.radius = const.BALL_RADIUS
		self.pos = const.BALL_INIT_POS
		self.angle = random.randint(225, 315) * math.pi / 180
		# ��ʼ��power_type
		self.change_power(power_type)

		# ������ͣ���ı���
		self.staytime = self.conststaytime
		self.staying = True
		self.startstay = True

		# ��ʱֹͣ������е�ʱ����, �ͷ�skillʱ��Ҫ
		self.suspend = None

		# �õ��޵е���ʱ�Ĵ���, ������
		self.no_drop = const.BALL_NOT_DROP

		# �Ƿ�ʹ���˵���
		self.used_item_type = None
		self.item_last_time = 0
		self.used_item_name = None

	# �ı������������
	def change_power(self, power_type=const.FIRE):
		# ���°���power_type��صı���
		self.power_type = power_type
		self.speed = const.BALL_SPEED[power_type]
		self.damage = const.BALL_DAMAGE[power_type]
		self.conststaytime = const.BALL_STAY_TIME[power_type]
		self.damage_status = const.BALL_ABILITY[power_type] # ��ʱ����

	def start_move(self):
		if self.startstay:
			self.staying = False
			self.startstay = False

	# ��ʱֹͣ�������, �ͷ�skillʱ��Ҫ
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

	# ��¼ʹ���˵���
	def record_use_item(self, time, type, name):
		if self.used_item_type != None:
			# �Ѿ�ʹ���˵���, �ظ�����Ч��
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
				# �ָ�Ч�� = ���°󶨲���
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
		# ΢���Ƕȣ�����ǶȽӽ�ƽ�У�����Ƕ�
		if angle >= const.BALL_MIN_ANGLE[0][0] and angle < const.BALL_MIN_ANGLE[0][1]:
			angle += const.BALL_ANGLE_DELTA
		elif angle >= const.BALL_MIN_ANGLE[1][0] and angle < const.BALL_MIN_ANGLE[1][1]:
			angle -= const.BALL_ANGLE_DELTA
		elif angle >= const.BALL_MIN_ANGLE[2][0] and angle < const.BALL_MIN_ANGLE[2][1]:
			angle += const.BALL_ANGLE_DELTA
		elif angle >= const.BALL_MIN_ANGLE[3][0] and angle < const.BALL_MIN_ANGLE[3][1]:
			angle -= const.BALL_ANGLE_DELTA
		self.angle = angle

	# Ԥ���ӿڣ�������������ֱ�ӳԵ��������Ʒ
	def on_eat(self, thing):
		pass

	# ��������ש��֮��ķ�����ٶȵĴ���
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
		# ��С��ΪĬ���ٶ�
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

	# Ԥ���ӿڣ� ���������Ե������Ʒ���˺�
	def on_hit_thing(self):
		pass

	# ����䵽�˰�ȫ��һ�»���������֮��
	# ���¶����������
	def on_kill(self):
		self.kill = False
		self.startstay = True
		self.staying = True
		self.death_pos = self.pos
		self.pos = const.BALL_INIT_POS
		self.set_speed(const.BALL_SPEED[self.power_type])
		angle = random.randint(225, 315) * math.pi / 180
		self.set_angle(angle)

	# ����ײ����ctrl_bar�Ĵ���
	# �����ܵ�bar��Ħ������ĽǶȸı䣬�ٶȲ���
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

	# ����ײ����ctrl_bar�ĽǵĴ�������ײ������ͣ��ʱ��
	# Ϊ���������y������ٶȺ����һ�֡�Ӣ�ۡ�����ĸо�
	# �����ctrl_bar�ı߽�С��ĳ���Ƕ�ʱ�����Խϴ�ǶȺͲ�С��bar���ٶȷ���
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
				# �������ʱ����ܳ��ֵĳ������
				alpha = max(abs(math.cos(angle)), const.BALL_MIN_DETA)
				self.set_speed(abs(bar.speed) / alpha)
			self.set_angle(angle)
		else:
			pass

	# ����ctrlbar���ʵأ�ʹ����bar����һ�����ݵ�ͣ���������������
	# ���������Լ����ٶ���bar���ƶ�
	def on_staying(self, bar, time):
		if self.staytime <= 0:
			self.staytime = self.conststaytime
			self.staying = False
		else:
			# ͣ����bar��
			# ���Ҹ����Լ���x���ٶ�ˮƽ�ƶ�
			# ��ͣ��ʱ��Ƚϳ�����ͻأ
			if self.startstay:
				return
			self.staytime -= time
			speedx = math.cos(self.angle) * self.speed
			nextposx = self.pos[0] + speedx * time
			self.pos = (nextposx, self.pos[1])

	# ������ײ������Ļ���ϱ�����з����λ�õĴ���
	def on_hit_wall(self, tag):
		if tag == const.SIDES_WALL_TAG:
			pass
		else:
			self.set_angle(2 * math.pi - self.angle)
			# �ƶ�����ǽ��ײ��λ��
			hit_posy = self.radius
			self.pos = (self.pos[0], hit_posy)

	# ������ײ������Ļ�׽��нǶȵĴ���
	# ���˽ӿ�Ϊ�Ժ��޵���Ʒʹ��
	def on_no_drop(self):
		self.set_angle(-self.angle)

	# ����ʱ������״̬���и���
	# ����λ�õ����ݣ��Ƿ���ײ������
	# ���� ��ײ����שͷ, �Ƿ���ײ������
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
		# ײ����ǽ
		if self._is_hit_up(nextpos):
			self.on_hit_wall(const.UP_WALL_TAG)
			need_pos = True
		# ��������
		if self.no_drop:
			if self._is_kill(nextpos):
				self.on_no_drop()
				need_pos = True
		else:
			if self._is_kill(nextpos):
				self.kill = True
				need_pos = True
		# �����bottom ctrl bar ����ײ
		is_hit_bar = False
		if self.staying:
			self.on_staying(bottombar, time)
			need_pos = True
		else:
			hit_res = self._is_hit_bottom_bar(bottombar, nextpos)
			if hit_res:
				is_hit_bar = True

			# ���ball ��ctrl_bar �� power_type ��ͬ, �ı�ball��power_type
			if hit_res and self.power_type != bottombar.power_type:
				self.change_power(bottombar.power_type)

			if hit_res == const.BALL_HIT_BAR_MID:
				self.on_hit_ctrl_bar(bottombar, const.CTRL_BAR_STYLE_BOTTOM)
				need_pos = True
			elif hit_res == const.LEFT or hit_res == const.RIGHT:
				self.on_hit_bar_corner(bottombar, const.CTRL_BAR_STYLE_BOTTOM, nextpos, hit_res)
				need_pos = True

		# �����brick����ײ
		res = []
		self.update_hit_brick(brickmanager, nextpos, res)
		if len(res):
			need_pos = True

		if not need_pos:
			self.pos = nextpos

		return res, is_hit_bar

	# �����Ƿ���ײ�������ǽ�����ж�
	def _is_hit_up(self, pos):
		ball_radius = const.BALL_RADIUS
		if pos[1] <= 0 + ball_radius:
			return True
		else:
			return False

	# �����Ƿ����������ж�
	def _is_kill(self, pos):
		if pos[1] > const.DROP_LINE:
			return True
		else:
			return False

	# �����Ƿ���ײ��ctrl_bar�����ж�
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
					return const.BALL_HIT_BAR_MID # �����в�

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

	# �жϲ��������ש�����ײ
	# 1.���ȼ������������е�λ��
	# 2.��������������ұ߽�������
	# 3.�����������ڵ��ٶȣ��¸�λ���Ƿ�����ײ
	# 4.������ײ�Ļ��ʹ�����ײ
	# 5.�����жϼ��������Ƿ���������λ�õ��жϴ���������������λ�ã�
	def update_hit_brick(self, brickmanager, nextpos, res):
		# �����¸�λ�����ڵ�����λ��x y
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

		# ����ײ
		# �ĸ�����,�����ĸ���������
		bottomright = (rightline, downline)
		bottomleft = (leftline, downline)
		topleft = (leftline, upline)
		topright = (rightline, upline)
		# ��û��ש�飬�����ĸ���������
		offset_bricks = (
				0, # �����
				brickmanager.try_get_brick(cur_x + 1, cur_y + 1),
				brickmanager.try_get_brick(cur_x - 1, cur_y + 1),
				brickmanager.try_get_brick(cur_x - 1, cur_y - 1),
				brickmanager.try_get_brick(cur_x + 1, cur_y - 1)
				)
		# ��Ҫ�����Ƿ���ײ�Ķ���
		hit = (0, 0, 0)
		if cur_x - 1 <= 0 or cur_x + 1 >= const.GRID_NUM_X - 1:
			return

		distance = (
				0, # �����
				self.calcu_distance(nextpos, bottomright),
				self.calcu_distance(nextpos, bottomleft),
				self.calcu_distance(nextpos, topleft),
				self.calcu_distance(nextpos, topright),
				)

		hit_vertex = (
				0, # �����
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

	# ��������ľ���
	def calcu_distance(self, pos1, pos2):
		distance = (pos1[0] - pos2[0]) ** 2
		distance += (pos1[1] - pos2[1]) ** 2
		return math.sqrt(distance)
