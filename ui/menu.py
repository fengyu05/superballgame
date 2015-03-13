# -*- coding:gb2312 -*-
# -*- $Id: menu.py 2 2009-04-20 03:10:36Z fengyu05 $ -*-
import pygame
from pygame.locals import *


class Menu(object):
	def __init__(self, screen, title, buttons,
			fgc=(255, 255, 255), mgc=(64, 64, 64), bgc=(0, 0, 0),
			size=64, font=None):

		# 自动中间对齐
		self.font = font
		self.title_surface = self.font.render(title, True, mgc, bgc)
		self.width = screen.get_rect().width
		self.height = screen.get_rect().height
		midx = self.width/2
		midy = self.height/2
		bh = (size/2+10)
		th = len(buttons)*bh
		self.tpos = (midx-self.title_surface.get_rect().width/2, midy-th/2-10-self.title_surface.get_rect().height)

		for button in buttons:
			if len(button) == 2:
				button.append(None)
		# 构造button { button[0] : text , button[1] : callable }
		self.buttons =[
				Button(self, i, self.width/2, self.height/2-th/2+i*bh, button[0], button[1] , button[2],
					fgc, (200, 200, 200), bgc, size/2, font,cx=1)
				for i, button in enumerate(buttons)]
		self.bgc = bgc
		self.fgc = fgc

		self.focus = None

	def draw(self, screen):
		screen.blit(self.title_surface, self.tpos)
		[b.draw(screen) for b in self.buttons]


	def event(self, event):
		if event.type == KEYUP:
			last = len(self.buttons) - 1
			if event.key == K_DOWN:
				if self.focus is None:
					self.focus = 0
				elif self.focus == last:
					self.focus = 0
				else:
					self.focus += 1
				button = self.buttons[self.focus]
				pygame.mouse.set_pos(button.rect.center)
			elif event.key == K_UP:
				if self.focus is None:
					self.focus = last
				elif self.focus == 0:
					self.focus = last
				else:
					self.focus -= 1
				button = self.buttons[self.focus]
				pygame.mouse.set_pos(button.rect.center)
			elif event.key == K_RETURN:
				if not self.focus is None:
					self.buttons[self.focus].do()

		[b.event(event) for b in self.buttons]


class Button(object):
	def __init__(self, parent, id, x, y, text, action, arg,
			fgc, mgc, bgc, size, font=None, margin=[10, 5], cx=0, cy=0):

		self.id = id
		self.font = font
		self.action = action
		self.arg = arg
		self.parent = parent
		self.text = text
		w, h = self.font.size(text)
		x-=(w/2+margin[0])*cx
		y-=(h/2+margin[1])*cy
		self.rect = Rect(x, y, w+margin[0]*2, h+margin[1]*2)

		img = pygame.Surface((w+margin[0]*2, h+margin[1]*2))
		img.fill(bgc)
		img.blit(self.font.render(text, True, fgc, bgc), margin)
		pygame.draw.rect(img, fgc, (0, 0, w+margin[0]*2, h+margin[1]*2), 3)

		img2 = pygame.Surface((w+margin[0]*2, h+margin[1]*2))
		img2.fill(mgc)
		img2.blit(self.font.render(text, True, fgc, mgc), margin)
		pygame.draw.rect(img2, fgc, (0, 0, w+margin[0]*2, h+margin[1]*2), 3)

		img3 = pygame.Surface((w+margin[0]*2, h+margin[1]*2))
		img3.fill(mgc)
		img3.blit(self.font.render(text, True, bgc, mgc), margin)
		pygame.draw.rect(img3, fgc, (0, 0, w+margin[0]*2, h+margin[1]*2), 3)
		self.img = [img, img2, img3]
		self.hover = 0
		self.clicked = False

	def do(self):
		if self.arg is None:
			self.action()
		else:
			self.action(*self.arg)

	def draw(self, screen):
		screen.blit(self.img[self.hover], self.rect.topleft)

	def event(self, event):
		if event.type==MOUSEMOTION:
			if self.rect.collidepoint(event.pos):
				if not self.hover:
					self.hover = 1
					self.parent.focus = self.id
			else:
				self.hover = 0
		elif event.type==MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.hover = 2
				self.clicked = True
		elif event.type==MOUSEBUTTONUP:
			if self.clicked and self.rect.collidepoint(event.pos):
				self.do()
				self.hover = 0
			self.clicked = False




