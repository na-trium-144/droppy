import pygame
from pygame.locals import *
import os
import time
import math

caption = "Droppy ver1.1"

scr_size_debug = None #(640, 480)

scr_size_org = (1280, 720)
(scr_w_org, scr_h_org) = scr_size_org

class AlignedRect(pygame.Rect):
	def __init__(self, align, xy=(0,0), size=(0,0)):
		pygame.Rect.__init__(self, xy, size)
		self.org = pygame.Rect(xy, size)
		self.align = align
		self.scale = 1
		self.scr_size = scr_size_org

	def setScale(self, scr_size=None, scale=None):
		if scr_size is not None:
			self.scale = scale
			self.scr_size = scr_size
		else:
			scale = self.scale
			scr_size = self.scr_size
		(scr_w, scr_h) = scr_size
		(scr_org_w, scr_org_h) = scr_size_org
		self.width = self.org.width * scale
		self.height = self.org.height * scale
		if self.align == -1:
			self.top = self.org.top * scale
			self.left = self.org.left * scale
		elif self.align == 1:
			self.bottom = scr_h - (scr_org_h - self.org.bottom) * scale
			self.right = scr_w - (scr_org_w - self.org.right) * scale
		else:
			self.centery = scr_h/2 - (scr_org_h/2 - self.org.centery) * scale
			self.centerx = scr_w/2 - (scr_org_w/2 - self.org.centerx) * scale
def scale_size(wh, scale):
	(w, h) = wh
	return (w * scale, h * scale)

tg = (560, 480)
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

title_rect = AlignedRect(1, (200,530), (1040,60))
subtitle_rect = AlignedRect(1, (200,600), (1040,30))
lv_t = "レベル:"
hard_t_rect = AlignedRect(1, (200,660), (1040-70,30))
hard_name_t = ("かんたん", "むずい")
hard_t = [f"{hard_name_t[h]}  {lv_t}" for h in range(2)]
hard_rect = AlignedRect(1, (1240-70,630), (70,60))
auto_rect = AlignedRect(1, (200,490), (1040,40))
auto_t = "[オートプレイ]"
logo_s_rect = AlignedRect(1, (1240-750/4,380), (750/4, 350/4))
fps_game_rect = AlignedRect(1, (200, 320), (1040, 40))
fps_menu_rect = AlignedRect(1, (200, 20), (1040, 40))

score_t_rect = AlignedRect(-1, (40,40), (180,60))
score_t = "スコア"
scgauge_rect = AlignedRect(-1, (40,110), (440,15))
hiscore_t_rect = AlignedRect(-1, (40,130), (180,30))
hiscore_t = "ハイスコア"
hnt_t_rect = {i:AlignedRect(-1, (40,150+40*i+5), (100,40)) for i in range(1,6)}
hnt_t = {1:"よい", 2:"ふつう", 3:"だめ", 4:"ミス", 5:"のこり"}
combo_t_rect = AlignedRect(-1, (400-40,310), (80,30))
combo_t = "コンボ"

scoreadd_rect = AlignedRect(-1, (260,15), (220,60))
score_rect = AlignedRect(-1, (260,40), (220,60))
hiscore_rect = AlignedRect(-1, (260,130), (215,30))
hnt_rect = {i:AlignedRect(-1, (100,150+40*i), (110,40)) for i in range(1,6)}
combo_rect = AlignedRect(-1, (400-60,240), (120,75))
combo_large_rect = AlignedRect(-1, (400-60-120,240-75), (120*3,75*3))

# easy, hard, easy_selected, hard_selected
item_wh = [(720, 60), (720, 60), (900, 135), (900, 135)]
item_span_y = 90
item_center_y = -80
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
item_anim_t = 15 / 60
item_ofs_t = 10 / 60

hscore_bg_x = 1280 - 450
hscore_bg_y = 720/2 + item_center_y + 80
hscore_bg_w = 400
hscore_bg_h = 190
hscore_bg_wh = (hscore_bg_w, hscore_bg_h)
hscore_bg_rect = AlignedRect(1, (hscore_bg_x, hscore_bg_y), hscore_bg_wh)
hscore_score_t_rect = AlignedRect(1, (hscore_bg_x+20, hscore_bg_y+20),(hscore_bg_w-40,80))
hscore_score_rect = AlignedRect(1, (hscore_bg_x+20, hscore_bg_y+10),(hscore_bg_w-40,40))
hscore_score_t = "ハイスコア"
hscore_star_rect = AlignedRect(1, (hscore_bg_x+20, hscore_bg_y+50),(140,40))
hscore_star_t = "ランク"
hscore_hnt_t_rect = {
    i:AlignedRect(1, (hscore_bg_x+20+90*(i-1),hscore_bg_y+100), (90, 40))
    for i in range(1,5)
}
hscore_hnt_rect = {
    i:AlignedRect(1, (hscore_bg_x+20+15+90*(i-1),hscore_bg_y+140), (60, 40))
    for i in range(1,5)
}
starall_bg_x = 50
starall_bg_y = hscore_bg_y + 40
starall_bg_w = 250
starall_bg_h = 150
starall_bg_rect = AlignedRect(-1, (starall_bg_x, starall_bg_y), (starall_bg_w, starall_bg_h))
starall_t1 = "きろく ごうけい"
starall_t1_rect = AlignedRect(-1, (starall_bg_x+20, starall_bg_y+20),(starall_bg_w-40,40))
starall_t2 = ""
starall_t2_rect = AlignedRect(-1, (starall_bg_x+20+70, starall_bg_y+20),(starall_bg_w-40,40))
starall_t3 = "★"
starall_t3_rect = AlignedRect(-1, (starall_bg_x+20, starall_bg_y+60+5),(300,40))
starall_t4 = "x"
starall_t4_rect = AlignedRect(-1, (starall_bg_x+20+70, starall_bg_y+60+5),(300,40))
starall_star_rect = AlignedRect(-1, (starall_bg_x+20, starall_bg_y+60), (starall_bg_w-40-5,80))

ss_help_t = [
	(" [W]/[S]",     " [A]/[D]",        "",             "[Space]"),
	("         きょく","         なんいど","[P] オート: {}","        スタート"),
	("[↑]/[↓]",      "[←]/[→]",       "",             "[Enter]")
]
ss_help_auto_t = ("オフ","オン")
ss_help_rect = [
	[
		AlignedRect(0, ((100,380,690,950)[x], 630 + 20 * y), (200,30))
		for x in range(4)
	]
	for y in range(3)
]

rslt_rank_t = "ランク"
rslt_rank_t_rect = AlignedRect(-1, (400-60, 240), (120, 30))
rslt_star_rect = [
	AlignedRect(-1, (400 - 150 + 100*i, 270), (100, 100))
	for i in range(3)
]
rslt_text = ["しっぱい", "クリア", "フルコンボ!", "パーフェクト!"]
rslt_text_color = [(255, 255, 255), (255, 255, 255), (255, 255, 0), (255, 255, 0)]
rslt_text_rect = AlignedRect(-1, (400-120, 380), (240, 60))
rslt_hiscore_t = "ハイスコアこうしん!"
rslt_hiscore_t_rect = AlignedRect(-1, (400 - 120, 160), (240, 60))
rslt_hiscore_t_color = (255, 255, 0)

tit_title = "リズムゲーム Droppy"
tit_title_rect = AlignedRect(0, (0, 630), (1280, 20))
tit_press = "どれかのキーを押してスタート!"
tit_press_rect = AlignedRect(0, (0, 450), (1280, 60))
tit_copyright = "(c)2020-2022 na trium"
tit_copyright_rect = AlignedRect(0, (0, 670), (1280, 20))

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
		self.rect = AlignedRect(1)
		self.home_xy = {s:(note_size[s][0] / 2, note_size[s][1]) for s in range(1,3)}
		#self.image = note_img
		self.stat = ninfo.stat
		self.scr_scale = 1

	#画像の初期化 1度しか呼ばれない
	#setscaleも兼ねる
	def setImage(self, note_img, scr_size, scale):
		self.image_def_org = note_img[self.col]
		self.image_scale = 1
		self.image_rot = 0
		self.setScale(scr_size, scale)

	def setScale(self, scr_size, scale):
		self.scr_size = scr_size
		self.scr_scale = scale
		self.rect.setScale(scr_size, scale)
		self.updateImgDef()

	#元画像image_def_orgを画面スケールに合わせて拡大縮小
	def updateImgDef(self):
		self.image_def = {
			s:pygame.transform.smoothscale(self.image_def_org[s], scale_size(self.image_def_org[s].get_size(), self.scr_scale))
			for s in (1, 2)
		}
		self.updateImg()

	#元画像image_defから音符サイズ(x1,x2)を選択、回転
	def updateImg(self):
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
			self.rect.org.x = tg[0] + xd * 3 / math.sqrt(13)
			self.rect.org.y = tg[1] - xd * 2 / math.sqrt(13) - (d - xd)
			rot = 0
		elif (d > 0): #mv1
			self.rect.org.x = tg[0] + d * 3 / math.sqrt(13)
			self.rect.org.y = tg[1] - d * 2 / math.sqrt(13)
			rot = bg_angle
		elif (d > -hrlen): #mv2
			self.rect.org.x = tg[0] + d
			self.rect.org.y = tg[1]
			rot = 0
		else: #mv3
			self.rect.org.x = tg[0] - hrlen + (d + hrlen) / 2
			self.rect.org.y = tg[1] + (d + hrlen) ** 2 / 100
		if (self.rect.org.y > scr_size_org[1]):
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
			self.updateImg()
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
		self.rect.org.x -= hx
		self.rect.org.y -= hy
		self.rect.org.size = self.image.get_size()

		self.rect.setScale()

def fontsRender(fonts, text, color):
	text_1 = ""
	text_3 = ""
	if text.startswith("<"):
		text_1 = text[1:text.find(">")]
		text = text[text.find(">")+1:]
	if text.endswith(">"):
		text_3 = text[text.rfind("<")+1:-1]
		text = text[:text.rfind("<")]
	if type(fonts) == tuple:
		(font_l, font_s) = fonts
	else:
		return fonts.render(text, True, color)
	img_text_1 = font_s.render(text_1, True, color)
	img_text_2 = font_l.render(text, True, color)
	img_text_3 = font_s.render(text_3, True, color)
	img = pygame.Surface((img_text_1.get_width() + img_text_2.get_width() + img_text_3.get_width(), img_text_2.get_height()), pygame.SRCALPHA)
	img.blit(img_text_1, (0, img_text_2.get_height()*0.9 - img_text_2.get_height()))
	img.blit(img_text_2, (img_text_1.get_width(), 0))
	img.blit(img_text_3, (img_text_1.get_width() + img_text_2.get_width(), img_text_2.get_height()*0.9 - img_text_3.get_height()))
	return img

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
		self.rect = AlignedRect(rect.align) #slideinの移動先etcに使う
		self.image_org = None
		self.image_static_org = None #animで動かない側
		self.image_anim_org = None #animで動く側
		self.image_notlarge_org = None #拡大前画像
		self.scr_scale = 1
		self.scr_size = scr_size_org
		self.setText(text, color) #描画

	def setScale(self, scr_size, scale):
		self.scr_size = scr_size
		self.scr_scale = scale
		self.rect.setScale(scr_size, scale)
		self.updateImg()

	#image_*_orgを拡大縮小
	def updateImg(self):
		if self.image_org is not None:
			self.image = pygame.transform.smoothscale(self.image_org, [self.scr_scale * self.image_org.get_size()[i] for i in range(2)])
		if self.image_notlarge_org is not None:
			self.image_notlarge = pygame.transform.smoothscale(self.image_notlarge_org, [self.scr_scale * self.image_notlarge_org.get_size()[i] for i in range(2)])
		if self.image_static_org is not None:
			self.image_static = pygame.transform.smoothscale(self.image_static_org, [self.scr_scale * self.image_static_org.get_size()[i] for i in range(2)])
		if self.image_anim_org is not None:
			self.image_anim = pygame.transform.smoothscale(self.image_anim_org, [self.scr_scale * self.image_anim_org.get_size()[i] for i in range(2)])

	def setXY(self, xy):
		self.set_rect.org.topleft = xy
		self.updateRectDef(self.rect_default.size)

	def updateRectDef(self, image_size):
		(image_w, image_h) = image_size
		(x, y) = self.set_rect.org.topleft
		if (self.set_align == -1):
			pass
		if (self.set_align == 0):
			x += self.set_rect.org.width / 2 - image_w / 2
		if (self.set_align == 1):
			x += self.set_rect.org.width - image_w
		# if (self.set_align_v == -1):
		# 	pass
		# if (self.set_align_v == 0):
		# 	y += self.set_rect.height / 2 - image_h / 2
		# if (self.set_align_v == 1):
		# 	y += self.set_rect.height - image_h
		self.rect.org = Rect((x, y), (image_w, image_h))

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
			self.image_static_org = fontsRender(self.set_font, text_static, color)
			self.image_anim_org = fontsRender(self.set_font, text_anim, color)
			self.rect_static = Rect((0, anim_y), self.image_static_org.get_size())
			#動く側文字の座標(image_static_org左上からの相対座標)
			self.rect_anim = Rect((self.rect_static.width, 0), (self.image_anim_org.get_rect().width, self.image_anim_org.get_rect().height + anim_y))
			image_size = (self.rect_anim.width + self.rect_static.width, self.rect_static.height + anim_y)
		elif large:
			self.image_notlarge_org = fontsRender(self.set_font, text, color)
			image_size = (self.image_notlarge_org.get_width() * large_scale, self.image_notlarge_org.get_height() * large_scale)
		else:
			self.image_org = fontsRender(self.set_font, text, color)
			image_size = (self.image_org.get_size())

		self.updateRectDef(image_size)

		if anim:
			self.anim_start = time.time()
			self.rect.org.move_ip(0, -anim_y)
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

		self.updateImg()

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

		self.rect.setScale()

		if self.slidein_start is not None:
			slidein_time = time.time() - self.slidein_start
			if (slidein_time > slidein_t2):
				self.image = pygame.Surface((0,0))
			else:
				slidein_ofs = slidein_time / slidein_t1
				if (slidein_ofs > 1):
					slidein_ofs = 1
				self.rect.move_ip(slidein_x * (1 - slidein_ofs), 0)
		else:
			pass
			# self.rect = self.rect_default.


class DScGaugeSprite(pygame.sprite.Sprite):
	def __init__(self, spgroup):
		pygame.sprite.Sprite.__init__(self)
		spgroup.add(self)
		self.rect_org = scgauge_rect
		self.set_score = None
		self.rect = self.rect_org
		self.scr_scale = 1

	def setScale(self, scr_size, scale):
		self.scr_size = scr_size
		self.scr_scale = scale
		self.rect.setScale(self.scr_size, self.scr_scale)
		self.updateImg()

	def setV(self, score, clrs, maxs):
		if (maxs <= score):
			score = maxs
		# if (self.set_score == score):
		# 	return
		self.set_score = score
		self.clrs = clrs
		self.maxs = maxs
		self.updateImg()
	def updateImg(self):
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
				# txt_img = fonts[i][k].render(iteminfo.meta[k], True, item_color[i])
				txt_img = fontsRender(fonts[i][k], iteminfo.meta[k], item_color[i])
				if item_align[k] == 1:
					ofs_x -= txt_img.get_width()
				self.set_image[i].blit(txt_img, (ofs_x, ofs_y))
		self.set_xy = (0, 0)
		self.old_xy = (0, 0)
		self.scr_size = scr_size_org
		self.scr_scale = 1
		self.img_state = 0
		self.state = 0
		self.anim_start = None
		self.ofs_start = None
		self.setState(False, False)

	def setScale(self, scr_size, scale):
		self.scr_size = scr_size
		self.scr_scale = scale
		self.updateRect()
		self.updateImg()

	def updateImg(self):
		scalex = 1
		if self.anim_start is not None:
			t = time.time() - self.anim_start
			if self.state & 2:
				scalex = abs(math.cos(t / item_anim_t * math.pi / 2))
		self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
		image_s = pygame.transform.smoothscale(self.set_image[self.img_state], (self.scr_scale * self.set_image[self.img_state].get_width() * scalex, self.scr_scale * self.set_image[self.img_state].get_height()))
		self.image.blit(image_s, (self.rect.width / 2 * (1 - scalex), 0))

	def updateRect(self):
		xy = self.set_xy
		if self.ofs_start is not None:
			xy = (self.set_xy[0], self.old_xy[1] + (self.set_xy[1] - self.old_xy[1]) * (time.time() - self.ofs_start) / item_ofs_t)
		self.rect = AlignedRect(0, xy, self.size_org)
		self.rect.setScale(self.scr_size, self.scr_scale)
		# 中央揃え

	def setState(self, ex, selected):
		if bool(self.state & 1) != ex:
			self.anim_start = time.time()
		self.state = (1 if ex else 0) + (2 if selected else 0)
		self.img_state = (self.img_state & 1) | (2 if selected else 0)
		self.size_org = item_wh[self.state]
		self.updateRect()
		self.updateImg()

	def setXY(self, xy, anim=False):
		# (x,y) = xy
		# self.set_xy = s_topleft(x,y)
		if anim:
			self.ofs_start = time.time()
		else:
			self.old_xy = xy
		self.set_xy = xy
		self.updateRect()

	def update(self):
		if self.anim_start is not None:
			t = time.time() - self.anim_start
			if t >= item_anim_t and self.img_state != self.state:
				self.img_state = self.state
			if t > 2*item_anim_t:
				self.anim_start = None
			self.updateImg()
		if self.ofs_start is not None:
			if time.time() - self.ofs_start > item_ofs_t:
				self.ofs_start = None
				self.old_xy = self.set_xy
			self.updateRect()

class DImageSprite(pygame.sprite.Sprite):
	def __init__(self, spgroup, image, rect, large=False):
		pygame.sprite.Sprite.__init__(self)
		spgroup.add(self)
		self.scr_scale = 1
		self.scr_size = scr_size_org
		self.large_start = None
		self.image_org = None
		self.image_notlarge_org = None
		self.setRect(rect, large)
		self.setImage(image, large)

	def setScale(self, scr_size, scale):
		self.scr_size = scr_size
		self.scr_scale = scale
		self.updateImg()
		self.rect.setScale(self.scr_size, self.scr_scale)
	def setImage(self, image, large=False):
		self.image_org = image
		if large:
			self.large_start = time.time()
			self.image_notlarge_org = image
			image_size = (self.image_notlarge_org.get_width() * large_scale, self.image_notlarge_org.get_height() * large_scale)
		self.updateImg()

	def setRect(self, rect, large=False):
		self.rect = AlignedRect(rect.align, rect.org.topleft, rect.org.size)
		if large:
			self.rect.org = Rect((rect.org.x - rect.org.width / 2 * (large_scale - 1), rect.org.y - rect.org.height / 2 * (large_scale - 1)), (rect.org.width * large_scale, rect.org.height * large_scale))
		self.rect.setScale(self.scr_size, self.scr_scale)

	def updateImg(self):
		if self.image_org is not None:
			self.image = pygame.transform.smoothscale(self.image_org, [self.scr_scale * self.image_org.get_size()[i] for i in range(2)])
		if self.image_notlarge_org is not None:
			self.image_notlarge = pygame.transform.smoothscale(self.image_notlarge_org, [self.scr_scale * self.image_notlarge_org.get_size()[i] for i in range(2)])

	def update(self):
		if self.large_start is not None:
			large_ofs = (time.time() - self.large_start) / large_t
			if large_ofs > 1:
				self.kill()
				return
				# large_ofs = 1
				# self.large_start = None
			now_scale = 1 + large_ofs * (large_scale - 1)
			scaled_size = (now_scale * self.image_notlarge.get_width(), now_scale * self.image_notlarge.get_height())
			max_size = (large_scale * self.image_notlarge.get_width(), large_scale * self.image_notlarge.get_height())
			self.image = pygame.Surface(max_size, pygame.SRCALPHA)
			scaled_image = pygame.transform.smoothscale(self.image_notlarge, scaled_size)
			mask_image = pygame.Surface(max_size, pygame.SRCALPHA)
			mask_image.fill((0, 0, 0, large_ofs * 255))
			self.image.blit(scaled_image, (self.image.get_width() / 2 - scaled_image.get_width() / 2, self.image.get_height() / 2 - scaled_image.get_height() / 2))
			self.image.blit(mask_image, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

class DSquareSprite(pygame.sprite.Sprite):
	def __init__(self, spgroup, color, rect):
		pygame.sprite.Sprite.__init__(self)
		spgroup.add(self)
		self.color = color
		self.scr_scale = 1
		self.scr_size = scr_size_org
		self.setRect(rect)
		self.updateImg()

	def setScale(self, scr_size, scale):
		self.scr_size = scr_size
		self.scr_scale = scale
		self.rect.setScale(self.scr_size, self.scr_scale)
		self.updateImg()
	def setRect(self, rect):
		self.rect = rect
		self.rect.setScale(self.scr_size, self.scr_scale)

	def updateImg(self):
		self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
		self.image.fill(self.color)


class DDraw():
	def __init__(self, res_dir):
		if scr_size_debug is not None:
			self.screen = pygame.display.set_mode(scr_size_debug)
		else:
			self.screen = pygame.display.set_mode(scr_size_org, RESIZABLE)
		pygame.display.set_caption(caption)
		pygame.display.set_icon(pygame.image.load(os.path.join(res_dir,"icon.png")).convert_alpha())

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
		self.logo_big_img_org = pygame.image.load(os.path.join(res_dir, "logo.png")).convert_alpha()
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

		self.effect_img_org = [
			pygame.image.load(os.path.join(res_dir, "notec{}.png".format(c))).convert_alpha()
			for c in range(2)
		]
		self.effect_img = [
			{s:
				pygame.transform.smoothscale(self.effect_img_org[c], note_size[s])
				for s in range(1,3)
			}
			for c in range(2)
		]

		self.item_img = [
				pygame.transform.smoothscale(
					pygame.image.load(os.path.join(res_dir, f"sel{i}.png")).convert_alpha(),
					item_wh[i]
				)
				for i in range(4)
			]

		self.frame_time = []
		self.frame_last = 0

		if scr_size_debug is not None:
			self.resize(scr_size_debug)
		else:
			self.resize(scr_size_org)

	def fps_update(self):
		self.frame_time.append(time.time()- self.frame_last)
		self.frame_last = time.time()
		while len(self.frame_time) > 30:
			del self.frame_time[0]
		self.fps_sp.setText(str(int(len(self.frame_time) / sum(self.frame_time))) + " fps")

	def resize(self, scr_size_new):
		self.scr_size = scr_size_new
		self.scr_scale = scr_size_new[1] / scr_size_org[1]
		self.bg0_img = pygame.transform.scale(self.bg0_img_org, self.scr_size)
		self.bg1_img = pygame.transform.scale(self.bg1_img_org, scale_size(scr_size_org, self.scr_scale))
		self.bg1_s_img = pygame.transform.scale(self.bg1_s_img_org, self.scr_size)
		for sp in self.spgroup:
			sp.setScale(self.scr_size, self.scr_scale)

	def tit_init(self):
		pygame.display.set_caption(caption)

		self.spgroup.empty()
		self.tit_cnt = 0

		self.bg1_sp = DImageSprite(self.spgroup, self.bg1_s_img_org, AlignedRect(0, (0, 0), self.scr_size))

		self.fps_sp = DTextSprite(self.spgroup, self.font_s, "", fps_menu_rect, 1)
		DTextSprite(self.spgroup, self.font_s, tit_title, tit_title_rect, 0)
		DTextSprite(self.spgroup, self.font_l, tit_press, tit_press_rect, 0)
		DTextSprite(self.spgroup, self.font_s, tit_copyright, tit_copyright_rect, 0)
		self.logo_big_sp = DImageSprite(self.spgroup, self.logo_big_img_org, AlignedRect(0, (0, 0), self.scr_size))
		for sp in self.spgroup:
			sp.setScale(self.scr_size, self.scr_scale)

	def tit_update(self):
		self.screen.blit(self.bg0_img, (0, 0))
		# self.screen.blit(self.bg1_s_img, (0, 0))
		self.fps_update()

		bx = 240 + 25 * math.sin(0.017 * self.tit_cnt)
		by = 60 + 25 * math.cos(0.026 * self.tit_cnt)
		self.logo_big_sp.setRect(AlignedRect(0, (bx, by), self.scr_size))
		self.tit_cnt += 1

		self.spgroup.update()
		dirty_rects = self.spgroup.draw(self.screen)
		# pygame.display.update(dirty_rects)
		pygame.display.update()

	def sel_init(self, sel_items, sel_num, ex, auto):
		pygame.display.set_caption(caption)

		self.spgroup.empty()

		itemfonts = [
			{'title':self.font_ts},
			{'title':self.font_ts},
			{'title':(self.font_tl, self.font_ts), 'subtitle':self.font_ts, 'level0':self.font_n, 'hard0':self.font_s},
			{'title':(self.font_tl, self.font_ts), 'subtitle':self.font_ts, 'level1':self.font_n, 'hard1':self.font_s}
		]
		for item in sel_items:
			item.item_sp = DSelItemSprite(self.spgroup, item, self.item_img, itemfonts)
			# item.sp['title'] = DTextSprite(self.font_s, iteminfo.value['title'], Rect(0,0,0,0), -1)
			item.item_sp.setScale(self.scr_size, self.scr_scale)
			# self.spgroup.add(item.tit1_sp)

		self.bg1_sp = DImageSprite(self.spgroup, self.bg1_s_img_org, AlignedRect(0, (0, 0), self.scr_size))
		self.fps_sp = DTextSprite(self.spgroup, self.font_s, "", fps_menu_rect, 1)

		self.help_sp = [[None for _ in  range(4)] for _2 in range(3)]
		for (y, (help_y_t, help_y_rect)) in enumerate(zip(ss_help_t, ss_help_rect)):
			for (x, (help_t, help_rect)) in enumerate(zip(help_y_t, help_y_rect)):
				self.help_sp[y][x] = DTextSprite(self.spgroup, self.font_s, help_t, help_rect)
				self.help_sp[y][x].setScale(self.scr_size, self.scr_scale)


		self.hscore_bg_sp = DSquareSprite(self.spgroup, (0, 0, 0, 128), hscore_bg_rect)
		self.hscore_score_t_sp = DTextSprite(self.spgroup, self.font_s, hscore_score_t, hscore_score_t_rect)
		self.hscore_score_sp = DTextSprite(self.spgroup, self.font_n, "", hscore_score_rect, align=1)
		#self.hscore_star_t_sp = DTextSprite(self.spgroup, self.font_s, hscore_star_t, hscore_star_rect)
		self.hscore_star_sp = DTextSprite(self.spgroup, self.font_s, "", hscore_star_rect, align=0, color=(255,255,0))
		self.hscore_hnt_t_sp = {
			i:DTextSprite(self.spgroup, self.font_s, hnt_t[i], hscore_hnt_t_rect[i], align=0)
			for i in range(1,5)
		}
		self.hscore_hnt_sp = {
			i:DTextSprite(self.spgroup, self.font_s, "", hscore_hnt_rect[i], align=1)
			for i in range(1,5)
		}

		self.starall_bg_sp = DSquareSprite(self.spgroup, (0, 0, 0, 128), starall_bg_rect)
		self.starall_t1_sp = DTextSprite(self.spgroup, self.font_s, starall_t1, starall_t1_rect, align=0)
		# self.starall_t2_sp = DTextSprite(self.spgroup, self.font_s, starall_t2, starall_t2_rect, align=-1, color=(255,255,0))
		self.starall_t3_sp = DTextSprite(self.spgroup, self.font_l, starall_t3, starall_t3_rect, color=(255,255,0))
		self.starall_t4_sp = DTextSprite(self.spgroup, self.font_l, starall_t4, starall_t4_rect)
		self.starall_star_sp = DTextSprite(self.spgroup, self.font_n, "", starall_star_rect, align=1)
		self.starall_num = 0
		self.starall_disp = 0

		self.sel_info_sp = [
			self.hscore_bg_sp, self.hscore_score_t_sp, self.hscore_score_sp, self.hscore_star_sp,
			self.hscore_hnt_t_sp[1], self.hscore_hnt_t_sp[2], self.hscore_hnt_t_sp[3], self.hscore_hnt_t_sp[4],
			self.hscore_hnt_sp[1], self.hscore_hnt_sp[2], self.hscore_hnt_sp[3], self.hscore_hnt_sp[4],
			self.starall_bg_sp, self.starall_t1_sp, self.starall_t3_sp, self.starall_t4_sp,
			self.starall_star_sp,
		]
		self.sel_info_visible = True
		self.sel_set_info_visible(False)

		self.sel_items = sel_items
		for si in self.sel_items:
			self.starall_num += si.dsavedat.star[0]
			self.starall_num += si.dsavedat.star[1]

		for sp in self.spgroup:
			sp.setScale(self.scr_size, self.scr_scale)

			self.sel_num = sel_num
			self.set_ex(ex)
			self.set_auto(auto)

		# self.select_anim = False
		self.sel_redraw_unselect()

		self.sel_update()
		pygame.display.update()

	def sel_set_info_visible(self, vis):
		old_vis = self.sel_info_visible
		if old_vis and not vis:
			for sp in self.sel_info_sp:
				self.spgroup.remove(sp)
		if not old_vis and vis:
			for sp in self.sel_info_sp:
				self.spgroup.add(sp)
				sp.setScale(self.scr_size, self.scr_scale)
		self.sel_info_visible = vis

	def set_sel_num(self, num):
		self.sel_redraw_unselect()
		if num < 0:
			num = 0
		if num >= len(self.sel_items):
			num = len(self.sel_items) - 1
		self.sel_num = num
		self.sel_update_hscore()
		self.sel_redraw_move()
		# self.select_anim = False
	def set_ex(self, ex):
		self.ex = ex
		for (n,iteminfo) in enumerate(self.sel_items):
			iteminfo.item_sp.setState(self.ex, n == self.sel_num)
		self.sel_update_hscore()
	def set_auto(self, auto):
		self.help_sp[1][2].setText(ss_help_t[1][2].format(ss_help_auto_t[1 if auto else 0]))
		self.auto = auto
	def sel_update(self):
		self.screen.blit(self.bg0_img, (0, 0))
		# self.screen.blit(self.bg1_s_img, (0, 0))
		self.fps_update()

		# if not self.select_anim and self.sel_items[0].item_sp.ofs_start is None:
		# 	self.sel_redraw_select()

		self.starall_disp += 0.07 * (self.starall_num - self.starall_disp)
		if self.starall_disp > self.starall_num:
			self.starall_disp = self.starall_num
		self.starall_star_sp.setText(str(round(self.starall_disp)))

		self.spgroup.update()
		dirty_rects = self.spgroup.draw(self.screen)
		# pygame.display.update(dirty_rects)
		pygame.display.update()

	def sel_itempos(self, n, item, span=False):
		(i_w, i_h) = item.item_sp.size_org
		i_x = scr_size_org[0] / 2 - i_w / 2
		i_y = scr_size_org[1] / 2 + item_center_y - i_h / 2 + item_span_y * (n - self.sel_num)
		if span:
			if n < self.sel_num:
				i_y -= item_selected_span_y
			if n > self.sel_num:
				i_y += item_selected_span_y
		return (i_x, i_y)

	def sel_redraw_unselect(self):
		for (n,item) in enumerate(self.sel_items):
			item.item_sp.setState(self.ex, False)
			item.item_sp.setXY(self.sel_itempos(n, item, False), False)
		self.sel_set_info_visible(False)

	def sel_redraw_move(self):
		for (n,item) in enumerate(self.sel_items):
			item.item_sp.setXY(self.sel_itempos(n, item, False), True)

	def sel_redraw_select(self):
		for (n,item) in enumerate(self.sel_items):
			item.item_sp.setState(self.ex, n == self.sel_num)
			item.item_sp.setXY(self.sel_itempos(n, item, True), False)
			# iteminfo.tit1_sp.setxy((i_x + itit_x, i_y + itit_y))
		self.sel_set_info_visible(True)


	def sel_update_hscore(self):
		savedat = self.sel_items[self.sel_num].dsavedat
		hsc_score = savedat.score[self.ex]
		hsc_hnt = savedat.hntcount[self.ex]
		hsc_star = savedat.star[self.ex]
		self.hscore_score_sp.setText(str(hsc_score))
		self.hscore_star_sp.setText("★"*hsc_star)
		for i in range(1,5):
			self.hscore_hnt_sp[i].setText(str(hsc_hnt[i]))

	def game_init(self, ex, auto, dmusic, dresult):

		self.spgroup.empty()
		self.bg1_sp = DImageSprite(self.spgroup, self.bg1_img_org, AlignedRect(1, (0, 0), self.scr_size))

		self.fps_sp = DTextSprite(self.spgroup, self.font_s, "", fps_game_rect, 1)

		self.title = dmusic.title
		self.subtitle = dmusic.subtitle
		self.ex = ex
		self.level = dmusic.level
		self.dresult = dresult
		self.auto = auto

		short_title = self.title
		if short_title.startswith("<"):
			short_title = short_title[short_title.find(">")+1:].strip()
		if short_title.endswith(">"):
			short_title = short_title[:short_title.find("<")].strip()

		pygame.display.set_caption(f"{short_title} [{hard_name_t[self.ex]} {self.level}] - {caption}")

		DImageSprite(self.spgroup, pygame.transform.smoothscale(self.logo_big_img_org, logo_s_rect.org.size), logo_s_rect)

		DTextSprite(self.spgroup, (self.font_tl, self.font_ts), self.title, title_rect, 1)
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
			sp.setScale(self.scr_size, self.scr_scale)

		self.game_update()
		pygame.display.update()

	def addnote(self, notesp):
		notesp.setImage(self.note_img, self.scr_size, self.scr_scale)
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
		rank_t_sp.setScale(self.scr_size, self.scr_scale)
		rank_t_sp.update()
		self.star_sp = [
			DImageSprite(self.spgroup, self.star0_img_org, rslt_star_rect[i])
			for i in range(3)
		]
		for i in range(3):
			self.star_sp[i].setScale(self.scr_size, self.scr_scale)
			self.star_sp[i].update()
		self.game_bg()
		dirty_rects = self.spgroup.draw(self.screen)
		# pygame.display.update(dirty_rects)
		pygame.display.update()
	def rslt_comboclear(self):
		self.combo_sp.setText("")
		self.combo_t_sp.setText("")
		self.combo_sp.update()
		self.combo_t_sp.update()
		self.game_bg()
		dirty_rects = self.spgroup.draw(self.screen)
		# pygame.display.update(dirty_rects)
		pygame.display.update()

	def rslt_star(self, i):
		self.star_sp[i].setImage(self.star1_img_org)
		self.star_sp[i].update()
		self.game_bg()
		dirty_rects = self.spgroup.draw(self.screen)
		# pygame.display.update(dirty_rects)
		pygame.display.update()
	def rslt_text(self, i):
		rslt_text_sp = DTextSprite(self.spgroup, self.font_l, rslt_text[i], rslt_text_rect, 0, rslt_text_color[i])
		rslt_text_sp.setScale(self.scr_size, self.scr_scale)
		rslt_text_sp.update()
		self.game_bg()
		dirty_rects = self.spgroup.draw(self.screen)
		# pygame.display.update(dirty_rects)
		pygame.display.update()
	def rslt_hiscore(self):
		rslt_hiscore_sp = DTextSprite(self.spgroup, self.font_l, rslt_hiscore_t, rslt_hiscore_t_rect, 0, rslt_hiscore_t_color)
		rslt_hiscore_sp.setScale(self.scr_size, self.scr_scale)
		rslt_hiscore_sp.update()
		self.game_bg()
		dirty_rects = self.spgroup.draw(self.screen)
		# pygame.display.update(dirty_rects)
		pygame.display.update()

	def game_bg(self):
		self.screen.blit(self.bg0_img, (0, 0))
		# self.screen.blit(self.bg1_img, (self.scr_size[0] - scr_size_org[0] * self.scr_scale, 0))

	def game_create_effect(self, notesp, h):
		effect_sp = DImageSprite(self.spgroup, pygame.transform.rotate(self.effect_img[h][notesp.image_scale], notesp.image_rot), notesp.rect, large=True)
		effect_sp.setScale(self.scr_size, self.scr_scale)

	def game_update(self):
		self.game_bg()
		self.fps_update()

		self.scgauge_sp.setV(self.dresult.score, self.dresult.scgclrs, self.dresult.scgmaxs)

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
