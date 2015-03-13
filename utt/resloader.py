# -*- coding:gb2312 -*-
# -*- $Id: resloader.py 2 2009-04-20 03:10:36Z fengyu05 $ -*-

import pygame
def load_image(name, colorkey=None):
	try:
		image = pygame.image.load(name)
	except pygame.error, message:
		print 'Cannot load image:', name
		raise SystemExit, message
	if colorkey is not None:
		image = image.convert()
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, pygame.RLEACCEL)
	else:
		image = image.convert_alpha()
	return image
