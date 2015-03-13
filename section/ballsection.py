# -*- coding:gb2312 -*-
# -*- $Id: ballsection.py 2 2009-04-20 03:10:36Z fengyu05 $ -*-
import sys
import random
import pygame
from pygame.locals import *
import gamectrl.const as const
from gamectrl.gamectrl import GameCtrl , GameSection
import ui.menu as menu
import logic.gamelogic as gamelogic
from ui.animsprite import AnimSprite, make_anim
import cPickle
import section.animbind as animbind
from ui.hpbar import HpBar
from ui.itembox import ItemBox
from section.sound import Sound

# ��Ϸ����ҪSection
class BallSection(GameSection):

	def __init__(self):
		super(BallSection, self).__init__()

		self.load_resource()

	# ������Դ, ֻ����һ��
	def load_resource(self):
		self.background = pygame.image.load("res\\bg\\bgg.jpg").convert()
		self.info_bar = pygame.image.load("res\\bg\\info.jpg").convert()
		self.helpimage = pygame.image.load("res\\bg\\help.png").convert_alpha()

		# �ص��¼�
		def return_to_menu():
			self.ctrl.go_to_section(const.MENU_SECTION)

		# ������Ϣ
		# ��һ�μ�����Ϸʱ�Զ�show help
		self.show_help = True
		def show_help():
			self.show_help = True
		# ���ܲ˵���
		self.menu = menu.Menu(
				self.screen,
				"[Pause...]",
				[
					['! Resume !', self.pause_resume ],
					['Return to Menu', return_to_menu],
					['Save game', self.save_game],
					['Load game', self.load_game],
					['Toggle Sound', self.toggle_sound],
					['Show Help', show_help],
					['Quit & Bye', sys.exit],
				],
				font = self.font
				)

		self.hp_bar = HpBar(self.screen, const.HP_LENGTH, const.HP_HEIHGT)
		self.em_bar = HpBar(self.screen, const.HP_LENGTH, const.HP_HEIHGT, colors=-1)
		self.item_box = ItemBox(self.screen, const.ITEMBOX_WIDTH, const.ITEMBOX_HEIGHT,
				self.font, const.ITEMBOX_SIZE)

		self.sprite_group = pygame.sprite.OrderedUpdates()
		# �󶨶�������
		# �հ׶���
		self.none_anim = animbind.make_anim_from_one_textrue('res\\none.jpg',1,1,1,-1,10000)
		# ����
		self.setup_ctrlbar()
		# ש��
		self.setup_bricks()
		# ����
		self.setup_ball()
		# ����Ч��
		self.setup_effects()
		# ����
		self.setup_item()
		# ������
		self.setup_itemboxs()

		self.has_sound = True
		self.sound = Sound('res\\sound')


	# ��Ϸ�浵
	def save_game(self):
		f = open('game.save', 'w')
		cPickle.dump(self.logic, f)
		f.close()
		self.pause = False

	# ������Ϸ
	def load_game(self):
		f = open('game.save', 'r')
		self.logic = cPickle.load(f)
		f.close()
		self.pause = False
		self.reinit_for_load()



	# ��������
	def setup_ball(self):
		self.ball_sprite = AnimSprite()
		animbind.setup_anim(self.ball_sprite, 'ball', [ animbind.BALL_ANIM] )
		self.sprite_group.add(self.ball_sprite)

	# �󶨿���������
	def setup_ctrlbar(self):
		self.ctrl_sprite = AnimSprite(anchor='centermiddle')
		animbind.setup_anim(self.ctrl_sprite, 'ctrl' , [ animbind.CTRL_ANIM,
			animbind.CTRL_LONG_ANIM])
		self.sprite_group.add(self.ctrl_sprite)


	# �󶨵�������
	def setup_item(self):
		self.item_sprites = []
		animbind.setup_animlis(self.item_sprites, const.ANIM_ITEM_MAX_NUM, 'item', [ animbind.ITEM_ANIM], self.none_anim)
		self.item_sprites_index = 0
		self.sprite_group.add(*self.item_sprites)


	def setup_itemboxs(self):
		self.item_box_sprites = [ None ]
		for i in range(1, const.ITEM_TYPE_NUM + 1):
			itemicon = AnimSprite()
			itemicon.add_anim('icon', animbind.make_anim_from_one_textrue(
				'res\\item\\item_%d.png' % i , 5, 2, 10)
				)

			self.item_box_sprites.append(itemicon)

		self.item_box.bind_anim(self.item_box_sprites, const.ITEMBOX_RELATED_POS)

	# ��Ч������
	def setup_effects(self):
		self.effect_sprites = []
		animbind.setup_animlis(self.effect_sprites, const.ANIM_EFFECT_MAX_NUM, 'effect',
				[   animbind.EFFECT_HIT_ANIM,
					animbind.EFFECT_DROP_ANIM,
					animbind.EFFECT_SKILL_ANIM,
					animbind.EFFECT_USE_ITEM,
					animbind.EFFECT_GET_ITEM,
				], self.none_anim, 'centermiddle')
		self.effect_sprites_index = 0
		self.sprite_group.add(*self.effect_sprites)

	# ��שͷ����
	def setup_bricks(self):
		self.bricks_sprite = []
		bricks_anim = animbind.load_anim('brick', 'brick', const.BRICK_TYPE_NUM, 4, 1, 4, 200)
		bricks_create_anim = animbind.load_anim('brick', 'brick_create', const.BRICK_TYPE_NUM, 5, 1, 5, 100)

		for x in xrange(const.GRID_NUM_X):
			self.bricks_sprite.append([])
			for y in xrange(const.GRID_NUM_Y):
				tmp_sprite = AnimSprite()
				tmp_sprite.add_anim('none', self.none_anim)
				animbind.add_anim_to_sprite(tmp_sprite, bricks_anim)
				animbind.add_anim_to_sprite(tmp_sprite, bricks_create_anim)
				tmp_sprite.rect.topleft = ( x * const.GRID_SIZE , y * const.GRID_SIZE )

				self.bricks_sprite[x].append( tmp_sprite)
				self.sprite_group.add(tmp_sprite)

	def reinit_for_load(self):
		self.init_sprite()
		self.item_dict = {}
		for id in self.logic.item_manager.itemdict.iterkeys():
			self.bing_new_item(id)

	def init_sprite(self):
		self.ctrl_power_type = const.INIT_POWER_TYPE
		self.ball_power_type = const.INIT_POWER_TYPE
		self.bind_brick_anim()

		self.change_bar_status()
		self.change_ball_status()

		self.set_sprites_play(self.item_sprites, 'none')
		self.set_sprites_play(self.effect_sprites, 'none')
		self.set_sprites_play(self.item_box_sprites, 'icon')

	# ############################################################################################################

	# SectionԪ�س�ʼ��
	def init(self, args):
		if args is None:
			args = (1,)
		level = args[0]
		self.logic.logic_start(level)
		self.item_dict = {}  # id: item

		self.init_sprite()
		self.pause = False
		if self.has_sound:
			self.sound.play('bg', -1)

	def end(self):
		if self.has_sound:
			self.sound.fadeout('bg', 3000)


	# �󶨶������鲥��none����
	def set_sprites_play(self, sprite_lis, title):
		for sprite in sprite_lis:
			if sprite:
				sprite.play(title, loop=True)

	# ����ש��״̬����
	def update_brick_status(self, x, y):
		brick = self.logic.get_brick_at(x , y)
		tmp_sprite = self.bricks_sprite[x][y]
		if brick :
			create_name = 'brick_create_%d' % (brick.type_id)
			name = 'brick_%d' % (brick.type_id)
			# שͷ��״̬�仯
			status = brick.fetch_status()
			if status == const.BRICK_CREATE:
				tmp_sprite.play_list(
						[ [create_name, False, None, None],
							[name , False, None, None],
						]
						)
			elif status == const.BRICK_NORMAL:
				tmp_sprite.play( name , loop=True)
			elif status == const.BRICK_BEHIT:
				hitsound = 'hit_%d' % random.randint(1,4)
				if self.has_sound:
					self.sound.channel_play('hit_2')
				pos = (x*const.GRID_SIZE , y*const.GRID_SIZE )
				self.play_effect(pos, 'hit_%d' % (self.ball_power_type))
			elif status == const.BRICK_DEATH:
				if self.has_sound:
					self.sound.channel_play('death_%d' % random.randint(1,2))
				tmp_sprite.play_list(
						[ [ create_name, True, None, None],
						  ['none', False, None, None],
						]
						)
				pos = (x*const.GRID_SIZE , y*const.GRID_SIZE )
				self.play_effect(pos, 'hit_%d' % (self.ball_power_type))
			elif status == const.BRICK_IGNORE:
				tmp_sprite.play('none')
		else:
			tmp_sprite.play( 'none' )

	# ���µ���λ��
	def update_item_pos(self):
		for id, sprite in self.item_dict.iteritems():
			sprite.rect.center = self.logic.get_item(id).pos

	# ��ȫ��שͷ��״̬����
	def bind_brick_anim(self):
		for x in xrange(const.GRID_NUM_X):
			for y in xrange(const.GRID_NUM_Y):
				self.update_brick_status(x, y)

	# ���Ŀ�������״̬
	def change_bar_status(self):
		self.ctrl_power_type = self.logic.ctrl_bar.power_type
		self.ctrl_sprite.play('ctrl_%d' % self.ctrl_power_type, loop=True , begin=5, end=15, rollback=True)

	# �������״̬
	def change_ball_status(self):
		self.ball_power_type = self.logic.ball.power_type
		self.ball_sprite.play('ball_%d' % self.ball_power_type, loop=True ,rollback=True)

	# ����Ч��
	def play_effect(self, pos, name):
		new_effect_sprite = self.effect_sprites[self.effect_sprites_index]
		self.effect_sprites_index += 1
		if self.effect_sprites_index == const.ANIM_EFFECT_MAX_NUM:
			self.effect_sprites_index = 0

		new_effect_sprite.rect.center = pos
		new_effect_sprite.play_list(
				[
					[name ,False,None,None],
					['none' , False, None, None],
				])

	# �����µ���ʱ, Ϊ���󶨶���
	def bing_new_item(self, item_id):
		new_item_sprite = self.item_sprites[self.item_sprites_index]
		self.item_sprites_index += 1
		if self.item_sprites_index == const.ANIM_EFFECT_MAX_NUM:
			self.item_sprites_index = 0

		item = self.logic.get_item( item_id )
		self.item_dict[ item_id] = new_item_sprite
		new_item_sprite.rect.center = item.pos
		new_item_sprite.play('item_%d' %(item.item_type.type), loop=True, rollback=True)

	# ������ʧ����
	def delete_item(self, item_id):
		self.item_dict[ item_id].play('none')
		del self.item_dict[ item_id ]

	# ֹͣ
	def pause_resume(self):
		self.pause = not self.pause

	def toggle_sound(self):
		if self.has_sound:
			self.sound.stop('bg')
		else:
			self.sound.play('bg')
		self.has_sound = not self.has_sound
		self.pause = False



	# ����
	def update(self, deta_time):
		if not self.pause:

			logic = self.logic # ȡ��game logic

			# �ж���Ϸ�Ƿ����
			if logic.game_over:
				self.ctrl.go_to_section(const.OVER_SECTION, (0,))

			# ʤ��
			if logic.win:
				self.ctrl.go_to_section(const.OVER_SECTION, (self.logic.level,))

			# ������Ϣ
			pressed_keys = pygame.key.get_pressed()
			if pressed_keys[K_LEFT]:
				logic.player_move( const.LEFT, deta_time)
			elif pressed_keys[K_RIGHT]:
				logic.player_move( const.RIGHT,deta_time)

			ball = logic.ball
			ctrl_bar = logic.ctrl_bar

			is_drop, is_hit_bar ,bricks_collide = logic.update(deta_time)
			# ���ײ��������
			if is_hit_bar:
				if self.has_sound:
					self.sound.channel_play('reflect_%d' % self.ctrl_power_type)

			# �����´���
			if is_drop:
				if logic.ctrl_bar.life<= 0:
					logic.game_over = True
					return
				self.play_effect((ball.death_pos[0], ball.death_pos[1] - 50), 'drop_%d' %(self.ball_power_type) )
				if self.has_sound:
					self.sound.channel_play('drop')


			# ש��״̬���´���
			for brick in bricks_collide:
				#self.bind_brick_anim()
				self.update_brick_status(brick.x_index, brick.y_index)

			# ����������쳤����
			change_len_state = logic.change_ctrl_len()
			if change_len_state > 0:
				self.ctrl_sprite.play('ctrl_long_%d' % self.ctrl_power_type, loop=True , begin=4, end=15, rollback=True)
			elif change_len_state < 0:
				self.ctrl_sprite.play('ctrl_%d' % self.ctrl_power_type, loop=True , begin=4, end=15, rollback=True)

			# ��Ʒupdate
			items_new, items_death, items_get = logic.item_update(deta_time)
			# �����µ��ߴ���
			for item_id in items_new:
				self.bing_new_item( item_id)
			for item_id in items_death + items_get:
				self.delete_item( item_id)

			# �õ����ߴ���
			if len(items_get) > 0:
				self.play_effect(ctrl_bar.pos, 'get_item_1')
				if self.has_sound:
					self.sound.channel_play('get_item')

			# ����״̬�ı䴦��
			if self.ctrl_power_type != ctrl_bar.power_type:
				self.change_bar_status()
			if self.ball_power_type != ball.power_type:
				self.change_ball_status()

			# ��ѹ����
			if logic.line_following_update(deta_time):
				self.bind_brick_anim()

			# ������λ��
			self.ball_sprite.rect.center = ball.pos
			# ���¿�����λ��
			self.ctrl_sprite.rect.center = ctrl_bar.pos

			self.update_item_pos()
			self.sprite_group.update()

			self.hp_bar.change_hp( 100 * ctrl_bar.life / ctrl_bar.max_life )
			self.em_bar.change_hp( 100 * ctrl_bar.energy / ctrl_bar.max_energy)
			self.item_box.change_item( ctrl_bar.itemboxs)

	# ��������
	def handle_key_down(self,event):
		key = event.key
		#option_dict = {}
		if key == K_ESCAPE:
			self.pause_resume()
			self.show_help = False
		elif key == K_q:
			sys.exit()
		# �����ù���
		elif key == K_a:
			self.logic.add_line()
			self.bind_brick_anim()

		elif key == K_y:
			self.logic.ball.no_drop = not self.logic.ball.no_drop
		elif key == K_z:
			self.bind_brick_anim()
		elif key == K_SPACE:
			# һ������, ������ͱ�ɱ��
			if self.logic.ball.staying:
				self.logic.ball.start_move()
			else:
				if self.logic.player_use_skill():
					self.play_effect(self.logic.ball.pos, 'skill_%d' % self.ball_power_type)
					self.bind_brick_anim()
			# ��һ�η����رհ���
			if self.show_help:
				self.show_help = False
		elif key >= K_1 and key <= K_4:
			key_id = key - K_0
			if key_id > 0 and key_id <= const.ITEMBOX_SIZE:
				if self.logic.player_use_item(key_id - 1):
					self.play_effect(self.logic.ctrl_bar.pos,'use_item_1')
					if self.has_sound:
						self.sound.channel_play('use_item')
		elif key >= K_7 and key <= K_9:
			self.logic.ctrl_bar.change_power( key - K_7 + 1)
		else:
			pass

	# ����������Ϣ
	def draw_info(self):
		# ��������Ϣ���
		font_color = (255,255,255)
		ctrl_bar = self.logic.ctrl_bar
		ball = self.logic.ball

		level = " Level: %d" % self.logic.level
		text = self.font.render(level, 1, font_color)
		self.screen.blit(text, (const.TEXT_POS_X, 100))

		scores = " Scores: %d" % ctrl_bar.scores
		text = self.font.render(scores, 1, font_color)
		self.screen.blit(text, (const.TEXT_POS_X, 130))

		acc = "Accelerate: %d" % ctrl_bar.acceleration
		text = self.font.render(acc, 1, font_color)
		self.screen.blit(text, (const.TEXT_POS_X, 250))

		dam = "Damage: %d" % ball.damage
		text = self.font.render(dam, 1, font_color)
		self.screen.blit(text, (const.TEXT_POS_X, 280))

		speed = "Speed: %d" % ball.speed
		text = self.font.render(speed, 1, font_color)
		self.screen.blit(text, (const.TEXT_POS_X,320))

		hp = "HP: [%d/%d]" % (ctrl_bar.life, ctrl_bar.max_life)
		text = self.font.render(hp, 1, font_color)
		self.screen.blit(text, (const.TEXT_POS_X, 180))

		en = "EN: [%d/%d]" % (ctrl_bar.energy, ctrl_bar.max_energy)
		text = self.font.render(en, 1, font_color)
		self.screen.blit(text, (const.TEXT_POS_X, 380))


		if ball.used_item_type:
			item = "%s : %d" % (ball.used_item_name, ball.item_last_time)
			text = self.font.render(item, 1, font_color)
			self.screen.blit(text, (const.TEXT_POS_X,500))

		if ctrl_bar.used_item_type:
			item = "%s : %d" % (ctrl_bar.used_item_name, ctrl_bar.item_last_time)
			text = self.font.render(item, 1, font_color)
			self.screen.blit(text, (const.TEXT_POS_X,550))

	# ģ�⿨������ĺ�������
	def make_it_busy(self):
		pygame.time.delay(50)
		#for i in range(100000):
		#	pass

	# ��Ⱦ
	def render(self):
		# ���Կ������
		# self.make_it_busy()
		self.screen.blit(self.background, (0, 0))
		self.screen.blit(self.info_bar, (const.MAIN_WIN_WIDTH,0))
		self.draw_info()
		self.hp_bar.render( const.HP_POS )
		self.em_bar.render( const.EM_POS )
		self.item_box.render( const.ITEMBOX_POS)
		self.sprite_group.draw(self.screen)
		if self.pause:
			self.menu.draw(self.screen)
		# ���������Ϣ
		if self.show_help:
			self.screen.blit(self.helpimage, const.HELP_POS)
		super(BallSection, self).render()


	def handle_event(self,event):
		if self.pause:
			self.menu.event(event)

