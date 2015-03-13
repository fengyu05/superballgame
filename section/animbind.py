# -*- coding:gb2312 -*-
# -*- $Id: animbind.py 2 2009-04-20 03:10:36Z fengyu05 $ -*-

import pygame
import gamectrl.const as const
from ui.animsprite import AnimSprite, make_anim

# 加载图片, 处理colorkey
def load_image(name, colorkey=None):
	try:
		image = pygame.image.load(name)
	except pygame.error, message:
		print 'Cannot load image:', name
		raise IOError, message
	if colorkey is not None:
		image = image.convert()
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, pygame.RLEACCEL)
	else:
		image = image.convert_alpha()
	return image

# 从图片中产生动画
def make_anim_from_one_textrue(name, x, y, num, colorkey=None, interval=100):
	image = load_image(name,colorkey)
	return make_anim(image, x ,y ,num, interval)

# 生成动画序列
def load_anim(foldername, filename, type_num, x, y, num, interval):
	anim_lis = [ None ] # 0 位置用空格填充
	for i in xrange(1, type_num + 1):
		anim_name = '%s_%d' %(filename, i)
		path = 'res\\%s\\%s_%d.png' % (foldername, filename, i)
		anim_lis.append(
			(
				anim_name,
				make_anim_from_one_textrue(path, x, y, num, None, interval)
			)
		)
	return anim_lis

# 将动画加入到动画精灵
def add_anim_to_sprite(sprite, anim_lis):
	for anim_tuple in anim_lis:
		if anim_tuple is None:
			continue
		else:
			sprite.add_anim( anim_tuple[0], anim_tuple[1])

# 批量加载动画到精灵, 根据 params_lis
def setup_anim(sprite, pathname, params_lis):
	for params in params_lis:
		anim = load_anim(pathname,
				params[0], params[1], params[2], params[3], params[4], params[5])
		add_anim_to_sprite(sprite, anim)

# 批量加载动画到精灵列表, 只构造一次动画序列
def setup_animlis(sprite_lis, sprite_cnt, pathname, params_lis, none_anim=None, anchor='topleft'):
	anim_lis = []
	for params in params_lis:
		anim_lis.append(
				load_anim(pathname,
					params[0], params[1], params[2], params[3], params[4], params[5])
		)
	for i in xrange(sprite_cnt):
		tmp = AnimSprite(anchor=anchor)
		if none_anim is not None:
			tmp.add_anim('none', none_anim)
		for anim in anim_lis:
			add_anim_to_sprite(tmp, anim)
		sprite_lis.append(tmp)

# ---------------------------------------------------------------
# 动画资料


# 名字, 种类数量, x帧数, y帧数, 总帧数, 时间间隔
BALL_ANIM = ('ball', 3, 5, 3, 15, 75)
CTRL_ANIM = ('ctrl', 3, 5, 4, 20, 100)
CTRL_LONG_ANIM = ('ctrl_long', 3, 5, 4, 20, 100)
ITEM_ANIM = ('item', 10, 5, 2, 10, 100)

EFFECT_HIT_ANIM = ('hit', 3, 5,2, 10, 75)
EFFECT_DROP_ANIM = ('drop',3, 5, 1, 5, 100)


EFFECT_SKILL_ANIM = ('skill',3, 5,3,15, 100)
EFFECT_USE_ITEM = ('use_item',1,5,3,15,100)
EFFECT_GET_ITEM = ('get_item',1,5,3,15,30)
