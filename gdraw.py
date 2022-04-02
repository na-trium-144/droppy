import pygame
from pygame.locals import *
import os
import time
import math

scr_size_debug = None #(640, 480)

#1280x720基準で設定し、画面サイズに合わせて拡大縮小
#(1280,720)x3以上を指定すると左上基準
#(-1280,-720)x3未満を設定すると右下基準
#scr_size_org*7でmodをとり、最後にscr_sizeをひく
#(画面外を負数にすることなく画面外として処理するため)
scr_size_org = (1280, 720)
(scr_w_org, scr_h_org) = scr_size_org
def s_topleft(x,y):
	return (x + scr_w_org * 3, y + scr_h_org * 3)
def s_bottomright(x,y):
	return (x - scr_w_org * 4, y - scr_h_org * 4)
def s_center(x,y):
	return (x - scr_w_org / 2, y - scr_h_org / 2)
def scale_size(wh, scale):
	(w, h) = wh
	return (w * scale, h * scale)
def scale_rect(rect, scale, scr_size):
	# rect_org = rect
	(scr_w, scr_h) = scr_size
	if rect.x >= scr_w_org:
		rect = Rect((rect.x - scr_w_org * 3, rect.y - scr_h_org * 3), rect.size)
		rect = Rect(scale_size(rect.topleft, scale), scale_size(rect.size, scale))
	elif rect.x < -scr_w_org:
		rect = Rect((rect.x + scr_w_org * 3, rect.y + scr_h_org * 3), rect.size)
		rect = Rect(scale_size(rect.topleft, scale), scale_size(rect.size, scale))
		rect = Rect((rect.x + scr_w, rect.y + scr_h), rect.size)
	else:
		rect = Rect(scale_size(rect.topleft, scale), scale_size(rect.size, scale))
		rect = Rect((rect.x + scr_w / 2, rect.y + scr_h / 2), rect.size)

	# rect = Rect((rect.x % (scr_ * 3) - scr_x, rect.y % (scr_y * 3) - scr_y), rect.size
	return rect
tg = s_bottomright(560, 480)
bg_angle = 33.69
mslen = 240 * math.sqrt(13) * 1.1
hrlen = 320
anim_y = 10
anim_t = 4 / 60
slidein_x = 20
slidein_t1 = 8 / 60
slidein_t2 = 30 / 60
large_t = 20 / 60
large_scale = 3

note_col_count = 9
note_size = {1:(60, 40), 2:(90, 60)}

title_rect = Rect(s_bottomright(200,530), (1040,60))
subtitle_rect = Rect(s_bottomright(200,600), (1040,30))
lv_t = "レベル:"
hard_t_rect = Rect(s_bottomright(200,660), (1040-70,30))
hard_t = ("かんたん  " + lv_t, "むずい  " + lv_t)
hard_rect = Rect(s_bottomright(1240-70,630), (70,60))
auto_rect = Rect(s_bottomright(200,490), (1040,40))
auto_t = "[オートプレイ]"

score_t_rect = Rect(s_topleft(40,40), (180,60))
score_t = "スコア"
scgauge_rect = Rect(s_topleft(40,110), (440,15))
hiscore_t_rect = Rect(s_topleft(40,130), (180,30))
hiscore_t = "ハイスコア"
hnt_t_rect = {i:Rect(s_topleft(40,150+40*i+5), (100,40)) for i in range(1,6)}
hnt_t = {1:"よい", 2:"ふつう", 3:"だめ", 4:"ミス", 5:"のこり"}
combo_t_rect = Rect(s_topleft(400-40,310), (80,30))
combo_t = "コンボ"

scoreadd_rect = Rect(s_topleft(260,15), (220,60))
score_rect = Rect(s_topleft(260,40), (220,60))
hiscore_rect = Rect(s_topleft(260,130), (215,30))
hnt_rect = {i:Rect(s_topleft(100,150+40*i), (110,40)) for i in range(1,6)}
combo_rect = Rect(s_topleft(400-60,240), (120,75))
combo_large_rect = Rect(s_topleft(400-60-120,240-75), (120*3,75*3))

# easy, hard, easy_selected, hard_selected
item_wh = [(720, 60), (720, 60), (900, 135), (900, 135)]
item_span_y = 90
item_selected_span_y = 30
item_bkcolor = [(64, 127, 255), (255, 127, 64), (64, 127, 255), (255, 127, 64)]
item_color = [(255, 255, 255), (255, 255, 0), (255, 255, 255), (255, 255, 0)]
item_ofs = [
	{'title':(30, 15)},
	{'title':(30, 15)},
	{'title':(30, 20), 'subtitle':(30, 90), 'level0':(870, 60), 'hard0':(800, 90)},
	{'title':(30, 20), 'subtitle':(30, 90), 'level1':(870, 60), 'hard1':(800, 90)}
]
item_align = {'title':-1, 'subtitle':-1, 'level0':1, 'level1':1, 'hard0':1, 'hard1':1}

ss_help_t = [
	(" [W]/[S]",     " [A]/[D]",        "",             "[Space]"),
	("         きょく","         なんいど","[P] オート: {}","        スタート"),
	("[↑]/[↓]",      "[←]/[→]",       "",             "[Enter]")
]
ss_help_auto_t = ("オフ","オン")
ss_help_rect = [
	[
		Rect(s_center((100,380,690,950)[x], 630 + 20 * y), (200,30))
		for x in range(4)
	]
	for y in range(3)
]

rslt_rank_t = "ランク"
rslt_rank_t_rect = Rect(s_topleft(400-60, 240), (120, 30))
rslt_star_rect = [
	Rect(s_topleft(400 - 150 + 100*i, 270), (100, 100))
	for i in range(3)
]
rslt_text = ["しっぱい", "クリア", "フルコンボ!", "パーフェクト!"]
rslt_text_color = [(255, 255, 255), (255, 255, 255), (255, 255, 0), (255, 255, 0)]
rslt_text_rect = Rect(s_topleft(400-120, 380), (240, 60))
rslt_hiscore_t = "ハイスコアこうしん!"
rslt_hiscore_t_rect = Rect(s_topleft(400 - 120, 200), (240, 60))
rslt_hiscore_t_color = (255, 255, 0)

tit_title = "リズムゲーム Droppy"
tit_title_rect = Rect(s_center(0, 630), (1280, 20))
tit_press = "どれかのキーを押してスタート!"
tit_press_rect = Rect(s_center(0, 450), (1280, 60))
tit_copyright = "(c)2020-2022 na trium"
tit_copyright_rect = Rect(s_center(0, 670), (1280, 20))

#音符スプライト
#表示前にも音符情報の保持に使用
class DNoteSprite(pygame.sprite.Sprite):
	def __init__(self, ninfo, zero_time):
		pygame.sprite.Sprite.__init__(self)
		self.t1 = ninfo.t1
		self.t2 = ninfo.t2
		self.t1_by_sec = ninfo.t1_by_sec + zero_time
		self.t2_by_sec = ninfo.t2_by_sec + zero_time
		self.xp = ninfo.xp
		self.col = ninfo.col
		self.wav = ninfo.wav
		self.wav_key = ninfo.wav_key
		self.rect = Rect(0,0,0,0)
		self.home_xy = {s:(note_size[s][0] / 2, note_size[s][1]) for s in range(1,3)}
		#self.image = note_img
		self.stat = ninfo.stat
		self.scr_scale = 1

	#画像の初期化 1度しか呼ばれない
	#setscaleも兼ねる
	def setimage(self, note_img, scr_size, scale):
		self.image_def_org = note_img[self.col]
		self.image_scale = 1
		self.image_rot = 0
		self.setscale(scr_size, scale)

	def setscale(self, scr_size, scale):
		self.scr_size = scr_size
		self.scr_scale = scale
		self.update_img_def()

	#元画像image_def_orgを画面スケールに合わせて拡大縮小
	def update_img_def(self):
		self.image_def = {
			s:pygame.transform.smoothscale(self.image_def_org[s], scale_size(self.image_def_org[s].get_size(), self.scr_scale))
			for s in (1, 2)
		}
		self.update_img()

	#元画像image_defから音符サイズ(x1,x2)を選択、回転
	def update_img(self):
		self.image = self.image_def[self.image_scale]
		if (self.image_rot != 0):
			self.image = pygame.transform.rotate(self.image, self.image_rot)

	def update(self):
		xp = self.xp
		xd = mslen * xp / 100
		p = (self.t2_by_sec - time.time()) / (self.t2_by_sec - self.t1_by_sec) * 1.1
		d = mslen * p
		rot = 0
		scale = 1
		if (d > xd): #mv0
			self.rect.x = tg[0] + xd * 3 / math.sqrt(13)
			self.rect.y = tg[1] - xd * 2 / math.sqrt(13) - (d - xd)
			rot = 0
		elif (d > 0): #mv1
			self.rect.x = tg[0] + d * 3 / math.sqrt(13)
			self.rect.y = tg[1] - d * 2 / math.sqrt(13)
			rot = bg_angle
		elif (d > -hrlen): #mv2
			self.rect.x = tg[0] + d
			self.rect.y = tg[1]
			rot = 0
		else: #mv3
			self.rect.x = tg[0] - hrlen + (d + hrlen) / 2
			self.rect.y = tg[1] + (d + hrlen) ** 2 / 100
		if (self.rect.y > scr_size_org[1]):
				self.stat = -100

		if (self.stat < 0):
			self.kill()

		if (self.stat == 2):
			scale = 2
		elif (self.stat == 1):
			scale = 1
		else:
			scale = self.image_scale

		if (self.image_rot != rot or self.image_scale != scale):
			self.image_scale = scale
			self.image_rot = rot
			self.update_img()
		self.image_scale = scale
		self.image_rot = rot

		(hx,hy) = self.home_xy[scale]
		if (rot != 0):
			cx1 = note_size[scale][0] / 2
			cy1 = note_size[scale][0] / 2
			cx = self.image.get_rect().width / 2
			cy = self.image.get_rect().height / 2
			(hx,hy) = (cx + (hx - cx1) * math.cos(math.radians(-rot)) - (hy - cy1) * math.sin(math.radians(-rot)), \
					cy + (hx - cx1) * math.sin(math.radians(-rot)) + (hy - cy1) * math.cos(math.radians(-rot)))
		self.rect.x -= hx
		self.rect.y -= hy

		self.rect = scale_rect(self.rect, self.scr_scale, self.scr_size)

#テキストのスプライト
#初期化で描画、setTextで再描画
#setText時にanim=Trueでスコアなどのアニメーション
#setText時にslidein=Trueで横からスライドイン
#setText時にlarge=Trueで拡大フェードアウトアニメーション
class DTextSprite(pygame.sprite.Sprite):
	def __init__(self, spgroup, font, text, rect, align=-1, color=(255,255,255)):
		pygame.sprite.Sprite.__init__(self)
		spgroup.add(self)
		self.set_font = font
		self.set_rect = rect #右寄せなどすると指定したrectと実際のrectは一致しない
		self.set_align = align
		# self.set_align_v = align_v
		self.set_text = None
		self.set_color = (255,255,255)
		self.anim_start = None
		self.slidein_start = None
		self.large_start = None
		self.rect_default = Rect(0,0,0,0) #slideinの移動先etcに使う
		self.image_org = None
		self.image_static_org = None #animで動かない側
		self.image_anim_org = None #animで動く側
		self.image_notlarge_org = None #拡大前画像
		self.scr_scale = 1
		self.scr_size = scr_size_org
		self.setText(text, color) #描画

	def setscale(self, scr_size, scale):
		self.scr_size = scr_size
		self.scr_scale = scale
		self.update_img()

	#image_*_orgを拡大縮小
	def update_img(self):
		if self.image_org is not None:
			self.image = pygame.transform.smoothscale(self.image_org, [self.scr_scale * self.image_org.get_size()[i] for i in range(2)])
		if self.image_notlarge_org is not None:
			self.image_notlarge = pygame.transform.smoothscale(self.image_notlarge_org, [self.scr_scale * self.image_notlarge_org.get_size()[i] for i in range(2)])
		if self.image_static_org is not None:
			self.image_static = pygame.transform.smoothscale(self.image_static_org, [self.scr_scale * self.image_static_org.get_size()[i] for i in range(2)])
		if self.image_anim_org is not None:
			self.image_anim = pygame.transform.smoothscale(self.image_anim_org, [self.scr_scale * self.image_anim_org.get_size()[i] for i in range(2)])

	def setxy(self, xy):
		self.set_rect = Rect(xy, self.set_rect.size)
		self.update_rect_def(self.rect_default.size)

	def update_rect_def(self, image_size):
		(image_w, image_h) = image_size
		(x, y) = self.set_rect.topleft
		if (self.set_align == -1):
			pass
		if (self.set_align == 0):
			x += self.set_rect.width / 2 - image_w / 2
		if (self.set_align == 1):
			x += self.set_rect.width - image_w
		# if (self.set_align_v == -1):
		# 	pass
		# if (self.set_align_v == 0):
		# 	y += self.set_rect.height / 2 - image_h / 2
		# if (self.set_align_v == 1):
		# 	y += self.set_rect.height - image_h
		self.rect_default = Rect((x, y), (image_w, image_h))

	def setText(self, text, color=None, anim=False, slidein=False, large=False):
		if color is None:
			color = self.set_color
		if self.set_text == text and self.set_color == color and not slidein and not large:
			return

		if anim:
			text_static = ""
			text_anim = ""
			if (len(text) != len(self.set_text)):
				text_anim = text
			else:
				char_changed = False
				for (new_c, old_c) in zip(text, self.set_text):
					if (new_c == old_c and not char_changed):
						text_static += new_c
					else:
						text_anim += new_c
						char_changed = True
			self.image_static_org = self.set_font.render(text_static, True, color)
			self.image_anim_org = self.set_font.render(text_anim, True, color)
			self.rect_static = Rect((0, anim_y), self.image_static_org.get_size())
			#動く側文字の座標(image_static_org左上からの相対座標)
			self.rect_anim = Rect((self.rect_static.width, 0), (self.image_anim_org.get_rect().width, self.image_anim_org.get_rect().height + anim_y))
			image_size = (self.rect_anim.width + self.rect_static.width, self.rect_static.height + anim_y)
		elif large:
			self.image_notlarge_org = self.set_font.render(text, True, color)
			image_size = (self.image_notlarge_org.get_width() * large_scale, self.image_notlarge_org.get_height() * large_scale)
		else:
			self.image_org = self.set_font.render(text, True, color)
			image_size = (self.image_org.get_size())

		self.update_rect_def(image_size)

		if anim:
			self.anim_start = time.time()
			self.rect_default = self.rect_default.move(0, -anim_y)
		else:
			self.anim_start = None

		if slidein:
			self.slidein_start = time.time()
		else:
			self.slidein_start = None

		if large:
			self.large_start = time.time()
		else:
			self.large_start = None

		self.set_text = text
		self.set_color = color

		self.update_img()

	def update(self):
		if self.anim_start is not None:
			anim_ofs = (time.time() - self.anim_start) / anim_t
			if (anim_ofs > 1):
				anim_ofs = 1
				self.anim_start = None
			self.image = pygame.Surface(self.rect.size, SRCALPHA)
			self.image.blit(self.image_static, [self.scr_scale * self.rect_static.topleft[i] for i in range(2)])
			self.image.blit(self.image_anim, [self.scr_scale * self.rect_anim.move(0, anim_y * anim_ofs).topleft[i] for i in range(2)])

		if self.large_start is not None:
			large_ofs = (time.time() - self.large_start) / large_t
			if large_ofs > 1:
				large_ofs = 1
				self.large_start = None
			now_scale = 1 + large_ofs * (large_scale - 1)
			scaled_size = (now_scale * self.image_notlarge.get_width(), now_scale * self.image_notlarge.get_height())
			max_size = (large_scale * self.image_notlarge.get_width(), large_scale * self.image_notlarge.get_height())
			self.image = pygame.Surface(max_size, pygame.SRCALPHA)
			scaled_image = pygame.transform.smoothscale(self.image_notlarge, scaled_size)
			mask_image = pygame.Surface(max_size, pygame.SRCALPHA)
			mask_image.fill((0, 0, 0, large_ofs * 255))
			self.image.blit(scaled_image, (self.image.get_width() / 2 - scaled_image.get_width() / 2, self.image.get_height() / 2 - scaled_image.get_height() / 2))
			self.image.blit(mask_image, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

		if self.slidein_start is not None:
			slidein_time = time.time() - self.slidein_start
			if (slidein_time > slidein_t2):
				self.image = pygame.Surface((0,0))
			else:
				slidein_ofs = slidein_time / slidein_t1
				if (slidein_ofs > 1):
					slidein_ofs = 1
				self.rect = scale_rect(self.rect_default, self.scr_scale, self.scr_size).move(slidein_x * (1 - slidein_ofs), 0)
		else:
			self.rect = scale_rect(self.rect_default, self.scr_scale, self.scr_size)


class DScGaugeSprite(pygame.sprite.Sprite):
	def __init__(self, spgroup):
		pygame.sprite.Sprite.__init__(self)
		spgroup.add(self)
		self.rect_org = scgauge_rect
		self.set_score = None
		self.rect = self.rect_org
		self.scr_scale = 1

	def setscale(self, scr_size, scale):
		self.scr_size = scr_size
		self.scr_scale = scale
		self.rect = scale_rect(self.rect_org, self.scr_scale, self.scr_size)
		self.update_img()

	def setv(self, score, clrs, maxs):
		if (maxs <= score):
			score = maxs
		# if (self.set_score == score):
		# 	return
		self.set_score = score
		self.clrs = clrs
		self.maxs = maxs
		self.update_img()
	def update_img(self):
		if self.set_score is None:
			return
		(w,h) = self.rect.size
		w -= 2
		h -= 2
		ch = round(h * 2 / 3)
		clrw = round(w * self.clrs / self.maxs)
		scw = round(w * self.set_score / self.maxs)
		self.image = pygame.Surface(self.rect.size, SRCALPHA)
		if(scw < clrw):
			scw1 = scw
			scw2 = clrw
		else:
			scw1 = clrw
			scw2 = scw
		self.image.fill((0,255,24), Rect(1, 1, scw1, ch))
		self.image.fill((32,128,48), Rect(1, 1+ch, scw1, h-ch))
		self.image.fill((56,56,56), Rect(1+scw1, 1, clrw-scw1, ch))
		self.image.fill((40,40,40), Rect(1+scw1, 1+ch, clrw-scw1, h-ch))
		self.image.fill((255,160,0), Rect(1+clrw, 1, scw2-clrw, ch))
		self.image.fill((140,90,60), Rect(1+clrw, 1+ch, scw2-clrw, h-ch))
		self.image.fill((80,64,80), Rect(1+scw2, 1, w-scw2, ch))
		self.image.fill((64,64,64), Rect(1+scw2, 1+ch, w-scw2, h-ch))
		pygame.draw.line(self.image, (255,255,255), (1,0), (w,0))
		pygame.draw.line(self.image, (255,255,255), (1,1+h), (w,1+h))
		pygame.draw.line(self.image, (255,255,255), (0,1), (0,h))
		pygame.draw.line(self.image, (255,255,255), (1+w,1), (1+w,h))

class DSelItemSprite(pygame.sprite.Sprite):
	def __init__(self, spgroup, iteminfo, item_img, fonts):
		pygame.sprite.Sprite.__init__(self)
		spgroup.add(self)
		iteminfo.meta['hard0'] = hard_t[0]
		iteminfo.meta['hard1'] = hard_t[1]
		self.set_image = []
		for i in range(4):
			self.set_image.append(pygame.Surface(item_wh[i], SRCALPHA))
			# self.set_image[i].fill(item_bkcolor[i])
			self.set_image[i].blit(item_img[i], (0, 0))
			for k in item_ofs[i]:
				(ofs_x, ofs_y) = item_ofs[i][k]
				txt_img = fonts[i][k].render(iteminfo.meta[k], True, item_color[i])
				if item_align[k] == 1:
					ofs_x -= txt_img.get_width()
				self.set_image[i].blit(txt_img, (ofs_x, ofs_y))
		self.set_xy = (0, 0)
		self.scr_size = scr_size_org
		self.scr_scale = 1
		self.setstate(False, False)

	def setscale(self, scr_size, scale):
		self.scr_size = scr_size
		self.scr_scale = scale
		self.update_img()
		self.update_rect()

	def update_img(self):
		self.image = pygame.transform.smoothscale(self.set_image[self.state], [self.scr_scale * self.set_image[self.state].get_size()[i] for i in range(2)])

	def update_rect(self):
		self.rect = scale_rect(Rect(self.set_xy, self.size_org), self.scr_scale, self.scr_size)
		# 中央揃え

	def setstate(self, ex, selected):
		self.state = (1 if ex else 0) + (2 if selected else 0)
		self.size_org = item_wh[self.state]
		self.update_img()
		self.update_rect()

	def setxy(self, xy):
		# (x,y) = xy
		# self.set_xy = s_topleft(x,y)
		self.set_xy = xy
		self.update_rect()

class DImageSprite(pygame.sprite.Sprite):
	def __init__(self, spgroup, image, rect):
		pygame.sprite.Sprite.__init__(self)
		spgroup.add(self)
		self.image_org = image
		self.set_rect = rect
		self.scr_scale = 1
		self.scr_size = scr_size_org
		self.update_img()
		self.rect = scale_rect(self.set_rect, self.scr_scale, self.scr_size)

	def setscale(self, scr_size, scale):
		self.scr_size = scr_size
		self.scr_scale = scale
		self.update_img()
		self.rect = scale_rect(self.set_rect, self.scr_scale, self.scr_size)
	def set_image(self, image):
		self.image_org = image
		self.update_img()
	def update_img(self):
		self.image = pygame.transform.smoothscale(self.image_org, [self.scr_scale * self.image_org.get_size()[i] for i in range(2)])


class DDraw():
	def __init__(self, res_dir):
		if scr_size_debug is not None:
			self.screen = pygame.display.set_mode(scr_size_debug)
		else:
			self.screen = pygame.display.set_mode(scr_size_org, RESIZABLE)
		self.spgroup = pygame.sprite.RenderUpdates()
		pygame.font.init()

		self.font_l = pygame.font.Font(os.path.join(res_dir,"azukiLP.ttf"), 60)
		self.font_s = pygame.font.Font(os.path.join(res_dir,"azukiLP.ttf"), 30)
		self.font_tl = pygame.font.Font(os.path.join(res_dir,"migmix-2p-regular.ttf"), 50)
		self.font_ts = pygame.font.Font(os.path.join(res_dir,"migmix-2p-regular.ttf"), 25)
		self.font_n = pygame.font.Font(os.path.join(res_dir,"Qarmic_sans_Abridged.ttf"), 50)
		self.font_ns = pygame.font.Font(os.path.join(res_dir,"Qarmic_sans_Abridged.ttf"), 30)

		self.bg0_img_org = pygame.image.load(os.path.join(res_dir, "bg0.png")).convert_alpha()
		self.bg1_img_org = pygame.image.load(os.path.join(res_dir, "bg1.png")).convert_alpha()
		self.bg1_s_img_org = pygame.image.load(os.path.join(res_dir, "bg1_s.png")).convert_alpha()
		self.star0_img_org = pygame.image.load(os.path.join(res_dir, "star0.png")).convert_alpha()
		self.star1_img_org = pygame.image.load(os.path.join(res_dir, "star1.png")).convert_alpha()

		self.note_img_org = [
			pygame.image.load(os.path.join(res_dir, "note{}.png".format(c))).convert_alpha()
			for c in range(note_col_count)
		]

		self.note_img = [
				{s:
					pygame.transform.smoothscale(self.note_img_org[c], note_size[s])
					for s in range(1,3)
				}
			for c in range(note_col_count)
		]
			#note_img[col][scale]

		self.item_img = [
				pygame.transform.smoothscale(
					pygame.image.load(os.path.join(res_dir, f"sel{i}.png")).convert_alpha(),
					item_wh[i]
				)
				for i in range(4)
			]

		if scr_size_debug is not None:
			self.resize(scr_size_debug)
		else:
			self.resize(scr_size_org)

	def resize(self, scr_size_new):
		self.scr_size = scr_size_new
		self.scr_scale = scr_size_new[1] / scr_size_org[1]
		self.bg0_img = pygame.transform.scale(self.bg0_img_org, self.scr_size)
		self.bg1_img = pygame.transform.scale(self.bg1_img_org, scale_size(scr_size_org, self.scr_scale))
		self.bg1_s_img = pygame.transform.scale(self.bg1_s_img_org, self.scr_size)
		for sp in self.spgroup:
			sp.setscale(self.scr_size, self.scr_scale)

	def tit_init(self):
		self.spgroup.empty()
		self.tit_cnt = 0

		DTextSprite(self.spgroup, self.font_s, tit_title, tit_title_rect, 0)
		DTextSprite(self.spgroup, self.font_l, tit_press, tit_press_rect, 0)
		DTextSprite(self.spgroup, self.font_s, tit_copyright, tit_copyright_rect, 0)
		for sp in self.spgroup:
			sp.setscale(self.scr_size, self.scr_scale)
		
	def tit_update(self):
		self.screen.blit(self.bg0_img, (0, 0))
		self.screen.blit(self.bg1_s_img, (0, 0))

		self.spgroup.update()
		dirty_rects = self.spgroup.draw(self.screen)
		# pygame.display.update(dirty_rects)
		pygame.display.update()

	def sel_init(self, sel_items):
		self.spgroup.empty()

		self.help_sp = [[None for _ in  range(4)] for _2 in range(3)]
		for (y, (help_y_t, help_y_rect)) in enumerate(zip(ss_help_t, ss_help_rect)):
			for (x, (help_t, help_rect)) in enumerate(zip(help_y_t, help_y_rect)):
				self.help_sp[y][x] = DTextSprite(self.spgroup, self.font_s, help_t, help_rect)
				self.help_sp[y][x].setscale(self.scr_size, self.scr_scale)

		itemfonts = [
			{'title':self.font_ts},
			{'title':self.font_ts},
			{'title':self.font_tl, 'subtitle':self.font_ts, 'level0':self.font_n, 'hard0':self.font_s},
			{'title':self.font_tl, 'subtitle':self.font_ts, 'level1':self.font_n, 'hard1':self.font_s}
		]
		for iteminfo in sel_items:
			iteminfo.item_sp = DSelItemSprite(self.spgroup, iteminfo, self.item_img, itemfonts)
			# iteminfo.sp['title'] = DTextSprite(self.font_s, iteminfo.value['title'], Rect(0,0,0,0), -1)
			iteminfo.item_sp.setscale(self.scr_size, self.scr_scale)
			# self.spgroup.add(iteminfo.tit1_sp)

		self.sel_items = sel_items
		self.sel_num = 0
		self.set_ex(0)
		self.set_auto(False)
		self.sel_update()
		pygame.display.update()

	def set_sel_num(self, num):
		if num < 0:
			num = 0
		if num >= len(self.sel_items):
			num = len(self.sel_items) - 1
		self.sel_num = num
	def set_ex(self, ex):
		self.ex = ex
	def set_auto(self, auto):
		self.help_sp[1][2].setText(ss_help_t[1][2].format(ss_help_auto_t[1 if auto else 0]))
		self.auto = auto
	def sel_update(self):
		self.screen.blit(self.bg0_img, (0, 0))
		self.screen.blit(self.bg1_s_img, (0, 0))

		for (n,iteminfo) in enumerate(self.sel_items):
			iteminfo.item_sp.setstate(self.ex, n == self.sel_num)
			(i_w, i_h) = iteminfo.item_sp.size_org
			i_x = - i_w / 2
			i_y = - i_h / 2 + item_span_y * (n - self.sel_num)
			if n < self.sel_num:
				i_y -= item_selected_span_y
			if n > self.sel_num:
				i_y += item_selected_span_y
			iteminfo.item_sp.setxy((i_x, i_y))
			# iteminfo.tit1_sp.setxy((i_x + itit_x, i_y + itit_y))
		self.spgroup.update()
		dirty_rects = self.spgroup.draw(self.screen)
		# pygame.display.update(dirty_rects)
		pygame.display.update()

	def game_init(self, ex, auto, dmusic, dresult):
		self.spgroup.empty()

		self.title = dmusic.title
		self.subtitle = dmusic.subtitle
		self.ex = ex
		self.level = dmusic.level
		self.dresult = dresult
		self.auto = auto

		DTextSprite(self.spgroup, self.font_tl, self.title, title_rect, 1)
		DTextSprite(self.spgroup, self.font_ts, self.subtitle, subtitle_rect, 1)
		DTextSprite(self.spgroup, self.font_n, str(self.level), hard_rect, 1)
		DTextSprite(self.spgroup, self.font_s, hard_t[self.ex], hard_t_rect, 1)
		self.auto_sp = DTextSprite(self.spgroup, self.font_s, auto_t if self.auto else "", auto_rect, 1)
		DTextSprite(self.spgroup, self.font_l, score_t, score_t_rect)
		DTextSprite(self.spgroup, self.font_s, hiscore_t, hiscore_t_rect)
		for i in range(1,6):
			DTextSprite(self.spgroup, self.font_s, hnt_t[i], hnt_t_rect[i])
		self.combo_t_sp = DTextSprite(self.spgroup, self.font_s, "", combo_t_rect, 0)

		self.scgauge_sp = DScGaugeSprite(self.spgroup)

		#self.result_sp = [DTextSprite(font_, "", rect_, align_) for (font_, rect_, align_) in \
		self.combo_sp = DTextSprite(self.spgroup, self.font_n, "", combo_rect, 0)
		self.combo_large_sp = DTextSprite(self.spgroup, self.font_n, "", combo_large_rect, 0)
		self.score_sp = DTextSprite(self.spgroup, self.font_n, "", score_rect, 1)
		self.hiscore_sp = DTextSprite(self.spgroup, self.font_s, "", hiscore_rect, 1)
		self.scoreadd_sp = DTextSprite(self.spgroup, self.font_n, "", scoreadd_rect, 1)
		self.hnt_sp = {}
		for i in range(1,5):
			self.hnt_sp[i] = DTextSprite(self.spgroup, self.font_ns, "", hnt_rect[i], 1)
		self.rest_sp = DTextSprite(self.spgroup, self.font_ns, "", hnt_rect[5], 1)
		# self.sp_combo = DTextSprite(self.font_n, "", rect_, align_)

		# for i in range(9):
			# font_ = self.font_n
			# rect_ = score_rect
			# #col_ = (255,255,255)
			# align_ = 1
			# if (i == -2):
				# rect_ = combo_rect
				# #col_ = combo_col
				# align_ = 0
			# if (i == 0):
				# font_ = self.font_s
				# rect_ = hiscore_rect
			# if (i >= 1):
				# font_ = self.font_ns
				# rect_ = hnt_rect[i]
			# sp_ = DTextSprite(font_, "", rect_, align_)
			# self.result_sp.append(sp_)
		for sp in self.spgroup:
			sp.setscale(self.scr_size, self.scr_scale)

		self.game_update()
		pygame.display.update()

	def addnote(self, notesp):
		notesp.setimage(self.note_img, self.scr_size, self.scr_scale)
		# notesp.setscale(self.scr_size, self.scr_scale)
		self.spgroup.add(notesp)

	def combo_large(self):
		combo_col = (255,255,255)
		if (self.dresult.combo == 0):
			pass
		elif (self.dresult.combo < 100):
			pass
		else:
			combo_col = (255,231,0)
		self.combo_large_sp.setText(str(self.dresult.combo) if self.dresult.combo > 0 else "", color=combo_col, large=True)

	def rslt_rank_t(self):
		rank_t_sp = DTextSprite(self.spgroup, self.font_s, rslt_rank_t, rslt_rank_t_rect, 0)
		rank_t_sp.setscale(self.scr_size, self.scr_scale)
		rank_t_sp.update()
		self.star_sp = [
			DImageSprite(self.spgroup, self.star0_img_org, rslt_star_rect[i])
			for i in range(3)
		]
		for i in range(3):
			self.star_sp[i].setscale(self.scr_size, self.scr_scale)
			self.star_sp[i].update()
		dirty_rects = self.spgroup.draw(self.screen)
		# pygame.display.update(dirty_rects)
		pygame.display.update()
	def rslt_comboclear(self):
		self.screen.blit(self.bg0_img, (0, 0))
		self.screen.blit(self.bg1_img, (self.scr_size[0] - scr_size_org[0] * self.scr_scale, 0))
		self.combo_sp.setText("")
		self.combo_t_sp.setText("")
		self.combo_sp.update()
		self.combo_t_sp.update()
		dirty_rects = self.spgroup.draw(self.screen)
		# pygame.display.update(dirty_rects)
		pygame.display.update()

	def rslt_star(self, i):
		self.star_sp[i].set_image(self.star1_img_org)
		self.star_sp[i].update()
		dirty_rects = self.spgroup.draw(self.screen)
		# pygame.display.update(dirty_rects)
		pygame.display.update()
	def rslt_text(self, i):
		rslt_text_sp = DTextSprite(self.spgroup, self.font_l, rslt_text[i], rslt_text_rect, 0, rslt_text_color[i])
		rslt_text_sp.setscale(self.scr_size, self.scr_scale)
		rslt_text_sp.update()
		dirty_rects = self.spgroup.draw(self.screen)
		# pygame.display.update(dirty_rects)
		pygame.display.update()
	def rslt_hiscore(self):
		rslt_hiscore_sp = DTextSprite(self.spgroup, self.font_l, rslt_hiscore_t, rslt_hiscore_t_rect, 0, rslt_hiscore_t_color)
		rslt_hiscore_sp.setscale(self.scr_size, self.scr_scale)
		rslt_hiscore_sp.update()
		dirty_rects = self.spgroup.draw(self.screen)
		# pygame.display.update(dirty_rects)
		pygame.display.update()


	def game_update(self):
		self.screen.blit(self.bg0_img, (0, 0))
		self.screen.blit(self.bg1_img, (self.scr_size[0] - scr_size_org[0] * self.scr_scale, 0))

		self.scgauge_sp.setv(self.dresult.score, self.dresult.scgclrs, self.dresult.scgmaxs)

		combo_col = (255,255,255)
		combo_t2 = combo_t
		if (self.dresult.combo == 0):
			combo_t2 = ""
		elif (self.dresult.combo < 100):
			pass
		else:
			combo_col = (255,231,0)

		#self.render_align(self.font_s, combo_t2, combo_col, combo_t_rect, 0)
		self.combo_t_sp.setText(combo_t2, combo_col)

		self.combo_sp.setText(str(self.dresult.combo) if self.dresult.combo > 0 else "", color=combo_col, anim=True)
		self.score_sp.setText(str(self.dresult.score), anim=(self.dresult.scadd > 0))
		self.hiscore_sp.setText(str(self.dresult.hiscore))
		if (self.dresult.scadd != 0):
			self.scoreadd_sp.setText(str(self.dresult.scadd), color=(255,231,0) if self.dresult.scadd >= 0 else (0,255,255), slidein=True)
			self.dresult.scadd = 0
		for i in range(1,5):
			self.hnt_sp[i].setText(str(self.dresult.hntcount[i]))
		self.rest_sp.setText(str(self.dresult.rest))


		self.spgroup.update()
		dirty_rects = self.spgroup.draw(self.screen)
		# pygame.display.update(dirty_rects)
		pygame.display.update()

	def render_align(self, font, text, color, rect, align=-1, before=None):
		text_img = font.render(text, True, color)
		text_rect = rect
		if(align == 0):
			text_rect = Rect(rect.x + rect.width / 2 - text_img.get_rect().width / 2, rect.y, text_img.get_rect().width, text_img.get_rect().height)
		if(align == 1):
			text_rect = Rect(rect.x + rect.width - text_img.get_rect().width, rect.y, text_img.get_rect().width, text_img.get_rect().height)

		self.screen.blit(text_img, (text_rect.x, text_rect.y))
		if (before is not None and text != before):
			pygame.display.update(rect)
