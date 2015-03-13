# -*- coding:gb2312 -*-
# -*- $Id: animsprite.py 2 2009-04-20 03:10:36Z fengyu05 $ -*-

__all__ = ['AnimSprite', 'make_anim']
# -*- AnimSprite class create by feng #
import pygame

# 从一个surface里面制作动画
def make_anim(image, x, y, num, interval=100):
	size = image.get_size()
	grid_x , grid_y = size[0] / x , size[1] / y
	anim = []
	for j in xrange(y):
		for i in xrange(x):
			subsur = image.subsurface( ( (grid_x * i, grid_y * j), (grid_x, grid_y) ) )
			anim.append((interval, subsur))
			if len(anim) == num:
				return anim
	return anim


# 动画精灵类
class AnimSprite(pygame.sprite.Sprite):

	def __init__ (self, anchor=None, *args, **kwargs):
		pygame.sprite.Sprite.__init__(self, *args, **kwargs)
		# _anims['title']=[ (interval, surface ), .. ]
		self._anims = {}
		# _current = _anims[_current_title]
		self._current = None
		self._current_title = None
		# 所在动画的帧数索引
		self._frame = None
		# pygame.time.get_ticks() when the previous frame was displayed.
		self._start = None
		# 播放速度乘数
		self._speed = 1.0

		self._loop = None
		self._roolback = None
		self._play_list = None
		self.rect = pygame.rect.Rect(0, 0, 0, 0)
		self.anchor = anchor
		self._xscale = None
		self._yscale = None

	# 速度get set 器
	def _get_speed (self):
		return self._speed
	def _set_speed (self, value):
		if value <= 0:
			self._speed = 0.0
		else:
			self._speed = float(value)
	speed = property(fget=_get_speed, fset=_set_speed)

	# 更新精灵矩形
	def _update_rect (self):
		rect = self.rect
		oldRect = pygame.rect.Rect(rect)
		rect.size = self.image.get_rect().size
		anchor = self.anchor
		if anchor:
			# 'left' and 'top' 为默认值
			if 'center' in anchor:
				rect.centerx = oldRect.centerx
			elif 'right' in anchor:
				rect.right = oldRect.right

			if 'middle' in anchor:
				rect.centery = oldRect.centery
			elif 'bottom' in anchor:
				rect.bottom = oldRect.bottom


	# 添加动画
	def add_anim (self, title, keyframes=None):
		if keyframes:
			for delay, surface in keyframes:
				self.add_frame(title, delay, surface)


	# 添加单独帧
	def add_frame (self, title, delay, surface, index=None):
		if not title in self._anims:
			self._anims[title] = []

		if index:
			self._anims[title].insert(index, (delay, surface))
		else:
			self._anims[title].append((delay, surface))

	# 播放制定的序列
	def play_list(self,lis):
		self._play_list = lis
		this_play = lis[0]
		self._play_list_pos = 0
		loop = False
		if len(self._play_list) == 1:
			loop = True
		self.play(this_play[0], backword=this_play[1], loop=loop, begin=this_play[2], end=this_play[3])

	# 播放动画, backword 为 倒叙播放 , loop 为循环, rollback 为 方向来回反复, begin 和 end 为 收尾位置
	def play(self, title, backword=False, loop=False, rollback=False, begin=None, end=None ):
		assert( title in self._anims )

		self._backup_title = self._current_title
		self._current_title = title
		self._frame_cnt = len(self._anims[title])
		self._current = self._anims[title]
		self._loop = loop
		self._roolback = rollback
		# 计算起始结束
		if begin:
			self._begin = begin
		else:
			self._begin = 0
		if end:
			self._end = end
		else:
			self._end =self._frame_cnt - 1

		assert ( self._begin >=0 and self._begin<=self._end and self._end < self._frame_cnt)
		if backword:
			self._toward = -1
			self._frame = self._end
		else:
			self._toward = 1
			self._frame = self._begin

		self._start = pygame.time.get_ticks()
		self.image = self._current[self._frame][1]
		self._update_rect()


	# 停止播放
	def stop_anim (self):
		self._current = None
		self._frame = 0
		self._current_title = None
		self._loop = None
		self._roolback = None
		self._play_list = None

	def set_scale(self, xscale, yscale=None):
		if yscale is None:
			yscale = xscale
		self._yscale = yscale
		self._xscale = xscale
		if xscale:
			self.rect.width = self.image.get_rect().width * xscale
			self.rect.height = self.image.get_rect().height * yscale


	# 跟新动画
	def update (self):
		pygame.sprite.Sprite.update(self)

		anim = self._current
		if anim and self._end > self._begin:
			now = pygame.time.get_ticks()
			thisTime, thisImage = anim[self._frame]

			if self._start + (thisTime / self.speed) < now:
				# 下一帧
				frame = self._frame
				next_frame = frame + self._toward
				# 检查帧循环
				finish = False
				if next_frame > self._end:
					finish = True
					next_frame = self._begin
				elif next_frame < self._begin:
					finish = True
					next_frame = self._end

				if finish:
					if self._play_list and not self._loop:
						self._play_list_pos += 1
						# 播放下个列表
						this_play = self._play_list[self._play_list_pos]
						if self._play_list_pos == len(self._play_list) - 1:
							self.play(this_play[0], backword=this_play[1], loop=True,\
									begin=this_play[2],end=this_play[3])
							return

						else:
							self.play(this_play[0], backword=this_play[1], loop=False,\
									begin=this_play[2],end=this_play[3])
							return

					if self._loop:
						if self._roolback:
							self._toward = - self._toward
							if self._toward == 1:
								next_frame = self._begin
							else:
								next_frame = self._end
					else:
						self.stop_anim()

				nextTime, nextImage = anim[next_frame]

				self.image = nextImage
				if self._xscale:
					size = self.image.get_size()
					self.image = pygame.transform.scale(self.image, ( int(size[0] * self._xscale), int(size[1] * self._yscale)) )
				self._frame = next_frame
				self._start = now




