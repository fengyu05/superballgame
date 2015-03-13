# -*- coding:gb2312 -*-
# -*- $Id: const.py 2 2009-04-20 03:10:36Z fengyu05 $ -*-
# ����ģ��

import math

# ��ܳ���
OPEN_LEVEL = 5
MAX_LEVEL = 8

WIN_WIDTH = 824
WIN_HEIGHT = 730
WIN_SIZE = (WIN_WIDTH,WIN_HEIGHT)
FONT_SIZE = 18
FPS = 30 # ֡��
INIT_HEIGHT= 680 # ����������ڵĸ߶�
DROP_LINE = 730 # ����߶�, yֵ������ʱ������
SAVE_LINE = 710 # �����ߣ������������Ͻ���ײ�ǿ��Ծ����
MAIN_WIN_WIDTH = 600 # ��Ϸ��Ϸ���
MIN_TIME = 1.0 / 41.0 # �߼�֡���ʱ��Ƭ
MIN_RENDER_AMOUNT = 5 #�ڿ���������߼�ִ֡��5�Σ�����ִ��һ����Ⱦ֡

TEXT_POS_X = MAIN_WIN_WIDTH + 25
HP_POS = (MAIN_WIN_WIDTH + 30, 200) # Ѫ��λ��
EM_POS = (MAIN_WIN_WIDTH + 30, 400) # ������λ��
HELP_POS = (100, 30)

HP_LENGTH = 170 # Ѫ�۳���
HP_HEIHGT = 25 # Ѫ�۸߶�
SOUND_DEFALUT_FREQUENCY = 22050
SOUND_BUFFER = 128

ITEMBOX_WIDTH = 198 # ����������
ITEMBOX_HEIGHT = 50 # �������߶�
ITEMBOX_SIZE = 4 # ��������С
ITEMBOX_POS = (MAIN_WIN_WIDTH + 12,600)
ITEMBOX_RELATED_POS = (-10, -10)# ���λ��

COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)

# Grids ����
GRID_SIZE = 50 # ���Ӵ�С
GRID_NUM_X = 12 # һ�еĸ����������:16
GRID_NUM_Y = 15 # һ�еĸ����������


# Section Id
MENU_SECTION = 1
BALL_SECTION = 2
OVER_SECTION = 3


# Ч������
FIRE = 1
ICE = 2
THUNDER = 3

INIT_POWER_TYPE = ICE

# ctrl_bar����
CTRL_BAR_WIDTH = 140 # ��������Ĭ�Ͽ��
CTRL_BAR_HEIGHT = 0
CTRL_BAR_STYLE_BOTTOM = 0 # �²��ĵ���
CTRL_BAR_STYLE_SIDES = 1 # ���ߵĵ���
CTRL_BAR_INIT_POS = (MAIN_WIN_WIDTH / 2 , INIT_HEIGHT) # �����ʼλ��

CTRL_BAR_LIFE = 600

CTRL_ENERYG_ADD = 5 # ����שͷʱ��������
CTRL_SKILL_ENERYG = 75 # һ�μ��ܵ�����

# ��������ͬ�������͵�Ĭ����ֵ
# ���ٶ�
CTRL_ACCELERATION = [0, 80, 70, 90] # 0, FIRE, ICE, THUNDER
# û����ʱ���ٶ�˥��
CTRL_SPEED_WEAKEN = [0, 30, 30, 20]
# �˶����Ħ��
CTRL_FRICTION = [0, 1, 0.5, 1.5]
# ����ٶ�
CTRL_MAX_SPEED = [0, 800, 900, 900 ]
# ���������
CTRL_MAX_LIFE = [0, 700, 800, 600]
# �����ٶ�
CTRL_MAX_ACCELERATION = [0, 150, 150, 200]
# �������
CTRL_MAX_ENERGY = [0, 100, 100, 100]


# ball����
BALL_RADIUS = GRID_SIZE / 2
BALL_HIT_BAR_MID = 1
BALL_HIT_BAR_CORNER = 2
BALL_INIT_POS = (MAIN_WIN_WIDTH / 2, INIT_HEIGHT) # ��ĳ�ʼλ��
BALL_MAX_SPEED = 700
BALL_SLOW_SPEED = 100
BALL_LIFE = 6
BALL_NOT_DROP = False # ������
BALL_MIN_DETA = 0.01
BALL_SAVE_MIN_ANGLE = 5 * math.pi / 4
BALL_SAVE_MAX_ANGLE = 7 * math.pi / 4
BALL_FIRST_QURD = math.pi / 2
BALL_SECOND_QURD = math.pi
BALL_THIRD_QURD = 3 * math.pi / 2
BALL_FORTH_QURD = 2 * math.pi
BALL_MIN_SPEEDX = 100

BALL_SKILL_TIME = 1.0 # ���ͷż���ʱ��

# ��ͬ�������͵�Ĭ����ֵ
BALL_SPEED = [0, 650, 600, 700]
BALL_DAMAGE = [0, 120, 100, 90]
BALL_STAY_TIME = [0, 0.08, 0.03, 0.13]
BALL_ABILITY = [0, FIRE, ICE, THUNDER]
BALL_SKILL_RANGE_X = [0, 3, 1, 1]
BALL_SKILL_RANGE_Y = [0, 2, 2, 5]
BALL_SKILL_DAMAGE = [0, 70, 150, 100]


BALL_MIN_ANGLE = (
		(0, math.pi / 12),
		(11 * math.pi / 12, math.pi),
		(math.pi, 13 * math.pi / 12),
		(23 * math.pi / 12 , 2 * math.pi)
		)
BALL_ANGLE_DELTA = 2 * math.pi / 45




# ��������
ANIM_EFFECT_MAX_NUM = 20 # Ч����������
ANIM_ITEM_MAX_NUM = 20 #��Ʒ��������

# Brick����
BRICK_INIT_HEIGHT = 6 # ��ʼʱשͷ�߶�
BRICK_TYPE_NUM = 6  # ש����������
BRICK_ENERGY_RATE = 10
MATERIAL_FACTOR = 5

# �ؿ�����
NEXT_FOLLOWING_TIME = 15 # שͷ��ѹʱ����

# ש��״̬
BRICK_NORMAL = 0
BRICK_DEATH = 1
BRICK_DAMAGE = 2


# wall����
SIDES_WALL_TAG = 0
UP_WALL_TAG = 1


# ����
UP = 1
RIGHT = 2
DOWN = 4
LEFT = 8


# ש����
MATERIAL_FACTOR = 5


# ש��״̬
BRICK_CREATE = -1
BRICK_NORMAL = 0
BRICK_DEATH = 1
BRICK_BEHIT = 2
BRICK_IGNORE = 3




# ��Ʒ����
ITEM_MAX_NUM = 10 #�������ĵ�������

ITEM_TYPE_NUM = 10 #��������
ITEM_TYPE_FIRE_BALL = 1
ITEM_TYPE_ICE_BALL = 2
ITEM_TYPE_THUNDER_BALL = 3
ITEM_TYPE_POWER = 3


ITEM_TYPE_ADD_BAR_LIFE = 4
ITEM_TYPE_ADD_BAR_EN = 5

ITEM_TYPE_ADD_BAR_ACC = 6
ITEM_TYPE_ADD_BAR_LEN = 7
ITEM_TYPE_TIME_SLOW = 8
ITEM_TYPE_ADD_DAMAGE = 9

ITEM_TYPE_SUB_BAR_LIFE = 10


ITEM_LIFE = 500
ITEM_STATUS_CREATE = 1
ITEM_STATUS_KILL = 0
ITEM_STATUS_ACTIVE = 2 # ������Ĺ�����
ITEM_STATUS_IN_BRICK = 3 # ��שͷ����
ITEM_SPEED = 150
ITEM_INTERVAL = 4
ITEM_LIFE = 500
ITEM_IN_BRICK_RATE = 25 # 15%�ĸ�����Ʒ������ש
ITEM_IN_RATE_FACTOR = 5 # �ȼ�����Ʒ����ש���Ӱ��

ITEM_RATE_BALL_TYPE = 50 # ��������ָ���
