# -*- coding:gb2312 -*-
# -*- $Id: brickmanager.py 2 2009-04-20 03:10:36Z fengyu05 $ -*-

import gamectrl.const as const
import random
import math
import mymap
from collections import deque


# bricktype�࣬������Ϸ�г��ֵ�brick������
class BrickType(object):

	def __init__(self, width=1 , height=1 , material=1 , life=100 ):
		self.width = width
		self.height = height
		self.material = material # ����ϵ��,Խ�󷴵�Խ��
		self.life = life
		self.scores = life


# brick�࣬������Ϸ��brick�����ݺ���Ϊ
class Brick(object):

	def __init__(self, brick_type):
		self.brick_type = brick_type
		self.life = self.brick_type.life
		self.has_item = False
		self.status = const.BRICK_CREATE
		self.be_hit = False

	def on_damage(self, damage):
		self.life -= damage
		if self.life <=0:
			self.status = const.BRICK_DEATH
			self.manager.bricks_num -= 1
		else:
			self.status = const.BRICK_BEHIT

	# ״̬ת�ƹ���
	# CREATE -> NORMAL
	# BEHIT -> NORMAL
	# DEATH -> IGNORE
	# ��״̬Ϊ const.BRICK_IGNORE ʱ, שͷ���������ڴ���
	def fetch_status(self):
		# ��¼, ת��״̬, ����ԭ����
		res = self.status
		if res == const.BRICK_CREATE:
			self.status = const.BRICK_NORMAL
		elif res == const.BRICK_BEHIT:
			self.status = const.BRICK_NORMAL
		elif res == const.BRICK_DEATH:
			self.status = const.BRICK_IGNORE
		else:
			pass
		return res


WALL_ID = 6

# BrickManager������������Ϸ�еĲ�����brick���й���
# ������Ϸ�в���brick�Ĺ���һֱ������brick�Ĺ���
class BrickManager(object):

	def __init__(self):
		self._brick_prototype = {}
		self.grids = deque()

	# ��ʼ��שͷ����
	def init_brick_type(self):
		prototypes = self._brick_prototype
		prototypes[1] = BrickType(1, 1, 0, 50) #
		prototypes[2] = BrickType(1, 1, 5, 100) #
		prototypes[3] = BrickType(1, 1, 10, 150) #
		prototypes[4] = BrickType(1, 1, 50, 200) #
		prototypes[5] = BrickType(1, 1, 0, 250)
		prototypes[WALL_ID] = BrickType(1, 1, 5, 1000000)

	# ����ש��
	def create_brick(self, type_id, x):
		if type_id == 0:
			return None
		assert( type_id in self._brick_prototype)
		brick = Brick(self._brick_prototype[type_id])
		brick.type_id = type_id
		brick.y_index = 0
		brick.x_index = x
		brick.manager = self
		return brick

	def my_import(self, name):
		mod = __import__(name)
		components = name.split('.')
		for comp in components[1:]:
			mod = getattr(mod, comp)
		return mod

	# ���ݵ�ͼ�ļ����� ��ͼ
	def create_gridmap(self, level):
		name = "mymap.lv%d" % level
		gridmap = self.my_import(name).gridmap
		self.gridmap_height = len(gridmap) # �ؿ���ͼ�ܸ߶�
		self.gridmap_y_now = self.gridmap_height # �ؿ���ͼ�����ڸ߶�λ��, �ݼ�Ϊ0

		self.preload_grids = []
		for y in xrange(self.gridmap_height):
			self.preload_grids.append([])
			for x in xrange(const.GRID_NUM_X):
				brick = self.create_brick(gridmap[y][x], x)
				if brick:
					self.bricks_num += 1
				self.preload_grids[y].append(brick)

		# ����ǽ
		for y in xrange(const.GRID_NUM_Y):
			self.append_newline( [None] * const.GRID_NUM_X)

		for y in xrange(const.BRICK_INIT_HEIGHT):
			self.add_line()

	def is_win(self):
		return self.bricks_num <= 1

	# ��girdsȫ����None���, ��ʼ��
	def init_grids(self):
		self.grids.clear()
		for y in xrange(const.GRID_NUM_Y):
			self.grids.append([None] * const.GRID_NUM_X)

		self.bricks_num = 0

	# ���µ��в��뵽grids����
	def append_newline(self ,line, has_wall=True):
		# שͷ��y��������
		for y in xrange(const.GRID_NUM_Y):
			for x in xrange(const.GRID_NUM_X):
				brick = self.grids[y][x]
				if brick:
					brick.y_index += 1

		# ����ǽ
		if has_wall:
			line[0] = self.create_brick( WALL_ID, 0)
			line[const.GRID_NUM_X-1] = self.create_brick( WALL_ID, const.GRID_NUM_X - 1)

		self.grids.appendleft(line)
		if len(self.grids) >= const.GRID_NUM_Y:
			self.grids.pop()


	# �����µ���, �ⲿ����
	def add_line(self):
		self.gridmap_y_now -= 1
		if self.gridmap_y_now >=0:
			self.append_newline( self.preload_grids[self.gridmap_y_now] )
		else:
			self.append_newline( [None] * const.GRID_NUM_X)

	def is_outside_grid(self, x, y):
		return x <0 or y < 0 or x >= const.GRID_NUM_X or y >= const.GRID_NUM_Y


	# �ж�שͷ�Ƿ����
	# ����, ����brick ,���� ����None
	def try_get_brick(self, x, y):
		if x < 0:
			x = 0
		if y < 0:
			y = 0
		if x >= const.GRID_NUM_X:
			x = const.GRID_NUM_X - 1
		if y >= const.GRID_NUM_Y:
			y = const.GRID_NUM_Y - 1
		brick = self.grids[y][x]
		if brick and brick.status != const.BRICK_IGNORE and brick.status != const.BRICK_DEATH:
			return brick
		else:
			return None

	# שͷѹ������
	def is_following_down(self):
		for i  in xrange(1,const.GRID_NUM_X - 2):
			if self.try_get_brick(i, const.GRID_NUM_Y - 1):
				return True
		return False

	# ��ļ���
	def handle_skill(self, x, y, power_type, level, itemmanager):
		ranx = const.BALL_SKILL_RANGE_X[power_type]
		rany = const.BALL_SKILL_RANGE_Y[power_type]
		dam = const.BALL_SKILL_DAMAGE[power_type]
		for i in xrange(-ranx,ranx + 1):
			for j in xrange(-rany,rany + 1):
				nx = x + i
				ny = y + j
				if self.is_outside_grid(nx, ny):
					continue
				brick = self.try_get_brick(nx, ny)
				if brick:
					brick.on_damage(dam)
					if brick.has_item:
						itemmanager.drop_item_at(nx, ny)
