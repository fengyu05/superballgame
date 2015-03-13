# -*- coding:gb2312 -*-
# -*- $Id: itemmanager.py 2 2009-04-20 03:10:36Z fengyu05 $ -*-

import random
import math
import gamectrl.const as const


class ItemType(object):

	def __init__(self, type=0, rate=10, contain=500, life=300, last_time=0,usage=False, name=""):
		self.type = type # �ӻ��߼��� 0���� 1��
		self.speed = const.ITEM_SPEED
		self.contain = contain
		self.life = life
		self.rate = rate
		self.last_time = last_time
		self.usage = usage # �Ƿ�����ʹ��
		self.name = name


class Item(object):

	def __init__(self, item_type):
		self.item_type = item_type
		self.life = self.item_type.life
		self.status = const.ITEM_STATUS_CREATE
		self.in_brick = False
		self.index = 0
		# ��ʼ��λ��
		posx = random.randint(1, const.GRID_NUM_X - 2)
		self.gridpos = (posx, 0)
		if posx == 1:
			posx = const.GRID_SIZE * 3 / 2
		else:
			posx = const.GRID_SIZE * posx + const.GRID_SIZE / 2
		self.pos = (posx, 0)

	# ��õ��ߴ����Լ������������ڴ��С�����
	def on_eaten(self):
		self.status = const.ITEM_STATUS_KILL

	# ������...
	def on_brick_eaten(self):
		pass

# ���߹�����
class ItemManager(object):

	def __init__(self):
		self._items_prototype = {}
		self.rate_sum = 0 # ȫ�����͵ĸ��ʱ�ͼ��ֵ
		self.rate_in_brick = const.ITEM_IN_BRICK_RATE

	# ��ʼ����������
	def init_item_types(self):
		prototypes = self._items_prototype

		prototypes[const.ITEM_TYPE_FIRE_BALL] = \
				ItemType(const.ITEM_TYPE_FIRE_BALL, const.ITEM_RATE_BALL_TYPE, usage=True)
		prototypes[const.ITEM_TYPE_ICE_BALL] = \
				ItemType(const.ITEM_TYPE_ICE_BALL,const. ITEM_RATE_BALL_TYPE, usage=True)
		prototypes[const.ITEM_TYPE_THUNDER_BALL] = \
				ItemType(const.ITEM_TYPE_THUNDER_BALL, const.ITEM_RATE_BALL_TYPE, usage=True)

		# ��bar��������Ʒ
		prototypes[const.ITEM_TYPE_ADD_BAR_LIFE] = \
				ItemType(const.ITEM_TYPE_ADD_BAR_LIFE, 80, 150)
		# ��bar��������Ʒ
		prototypes[const.ITEM_TYPE_SUB_BAR_LIFE] = \
				ItemType(const.ITEM_TYPE_SUB_BAR_LIFE, 80, -150)
		# ��bar��������Ʒ
		prototypes[const.ITEM_TYPE_ADD_BAR_EN] = \
				ItemType(const.ITEM_TYPE_ADD_BAR_EN, 50, 50)

		# ��ctrlbar�ļ��ٶȵ���Ʒ
		prototypes[const.ITEM_TYPE_ADD_BAR_ACC] = \
				ItemType(const.ITEM_TYPE_ADD_BAR_ACC, 50, last_time=10, usage=True, name='Speed Up')
		# ��bar���ȵ���Ʒ
		prototypes[const.ITEM_TYPE_ADD_BAR_LEN] = \
				ItemType(const.ITEM_TYPE_ADD_BAR_LEN, 150, last_time=20, usage=True, name='Longest')
		# ʱ�������Ʒ
		prototypes[const.ITEM_TYPE_TIME_SLOW] = \
				ItemType(const.ITEM_TYPE_TIME_SLOW, 150, last_time=5, usage=True, name='Time Slow')
		# ������ǿ
		prototypes[const.ITEM_TYPE_ADD_DAMAGE] = \
				ItemType(const.ITEM_TYPE_ADD_DAMAGE, 100, last_time=5, usage=True, name='Damage Up')

		# #
		for index in prototypes:
			self.rate_sum += prototypes[index].rate

	def init_items(self):
		self.interval = const.ITEM_INTERVAL
		self.create_time = self.interval
		self.itemdict = {}
		self.itemnum = 0
		self.cur_id = 1
		self.level = 1

	def get_item_type(self, id):
		assert id in self._items_prototype
		return self._items_prototype[id]

	# �����µ���
	def create_item(self, type_id):
		if type_id == 0:
			return None
		assert(type_id in self._items_prototype)
		item = Item(self._items_prototype[type_id])
		return item

	# �����䵽שͷ����
	def on_hit_brick(self, brick, item):
		item.pos = (item.pos[0], item.gridpos[1] * const.GRID_SIZE + const.GRID_SIZE / 2)
		in_rate = random.randint(1, 100)
		if in_rate <= self.rate_in_brick:
			item.status = const.ITEM_STATUS_IN_BRICK
			brick.has_item = True
		else:
			if item.gridpos[1] < 14:
				item.gridpos = (item.gridpos[0], item.gridpos[1] + 1)
			else:
				item.gridpos = (item,gridpos[0], 14)

	# ���߸�����ѹЧ��
	def on_add_line(self):
		for index in self.itemdict:
			item = self.itemdict[index]
			if item.status == const.ITEM_STATUS_IN_BRICK:
				item.gridpos = (item.gridpos[0], item.gridpos[1] + 1)
				item.pos = (item.pos[0], item.gridpos[1] * const.GRID_SIZE + const.GRID_SIZE / 2)

	# ������ʧ
	def on_kill(self, index):
		self.itemnum -= 1
		del self.itemdict[index]

	# ����������, �����ӵ�
	def on_hitball(self):
		pass

	# ��������
	def drop_item_at(self, index_x, index_y):
		for index in self.itemdict:
			item = self.itemdict[index]
			if item.gridpos == (index_x, index_y) and item.status == const.ITEM_STATUS_IN_BRICK:
				item.status = const.ITEM_STATUS_ACTIVE
				return index

	# ���ݼ��������µ���
	def new_item(self):
		# ����һ��С��self.rate_sum�������
		# �����������ȥ������Ʒ�е�rate��ȷ������������Ʒ
		id = random.randint(1, self.rate_sum)
		item = None
		for index in self._items_prototype:
			type = self._items_prototype[index]
			id -= type.rate
			if id <= 0:
				item = self.create_item(type.type)
				break

		if item == None:
			return None
		item.status = const.ITEM_STATUS_ACTIVE
		item.index = self.cur_id
		self.itemdict[self.cur_id] = item
		self.cur_id += 1
		self.itemnum += 1

		return self.cur_id - 1

	# ���߹�����Ӧ����
	def update(self, level, brickgrids, bottombar, ball, time):
		createnew = [] # �����ӵ���Ʒ
		drop_item = [] # �����ȥ����Ʒ
		eaten_item = [] # ���Ե�����Ʒ
		if self.level != level:
			self.rate_in_brick = const.ITEM_IN_BRICK_RATE + level * const.ITEM_IN_RATE_FACTOR
		if self.create_time <= 0:
			self.create_time = self.interval
			# ��ʱ�������Ʒ��
			if self.itemnum < const.ITEM_MAX_NUM:
				id = self.new_item()
				if id:
					createnew.append(id)
		else:
			self.create_time -= time
		# update��Ʒ��Ϣ
		for index in self.itemdict.keys():
			item = self.itemdict[index]
			if item.status == const.ITEM_STATUS_ACTIVE:
				# ��һ��λ��
				nextposy = item.pos[1] + item.item_type.speed * time
				# ����Ƿ��˸�grid����,���˾����Ƿ���ש��
				if nextposy >= item.gridpos[1] * const.GRID_SIZE + const.GRID_SIZE / 2:
					brick = brickgrids[item.gridpos[1]][item.gridpos[0]]
					if brick and brick.has_item == False and brick.status != const.BRICK_IGNORE:
						self.on_hit_brick(brick, item)
					else:
						item.gridpos = (item.gridpos[0], item.gridpos[1] + 1)
				else:
					item.pos = (item.pos[0], nextposy)
				# ����Ƿ񱻳Ե�
				if nextposy >= bottombar.pos[1]:
					if item.pos[0] >= bottombar.pos[0] - bottombar.width / 2 \
						and item.pos[0] <= bottombar.pos[0] + bottombar.width /2:
							item.pos = (item.pos[0], bottombar.pos[1])
							bottombar.on_eate(item)
							item.on_eaten()
							# ���뱻���˸����б�
							eaten_item.append(index)
							continue
					else:
						item.gridpos = (item.gridpos[0], 14)
						item.status = const.ITEM_STATUS_KILL
						drop_item.append(index)
						continue
			if item.status == const.ITEM_STATUS_KILL:
				self.on_kill(index)
			if item.status == const.ITEM_STATUS_IN_BRICK:
				continue
		return createnew, drop_item, eaten_item

