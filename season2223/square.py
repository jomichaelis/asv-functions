from PIL import Image, ImageFont, ImageDraw
import os
import io


def resize_square(image, max_size):
	rs_width, rs_height = image.size
	ratio = min(max_size/rs_width, max_size/rs_height)
	return image.resize((round(rs_width*ratio), round(rs_height*ratio)), Image.ANTIALIAS)


def create_image(home, guest, team_home, team_guest, rank_home, rank_guest, date, time, liga):

	width = 2000
	height = 2000

	img = Image.new('RGB', size=(width, height))

	# paste logos
	home_team_logo = home.get('id') + ".png"
	guest_team_logo = guest.get('id') + ".png"
	background = Image.open(os.path.abspath(os.path.dirname(__file__)) + "/backgrounds/square.png")
	img.paste(background)
	home_logo = Image.open(os.path.abspath(os.path.dirname(__file__)) + '/logos/' + home_team_logo)
	guest_logo = Image.open(os.path.abspath(os.path.dirname(__file__)) + '/logos/' + guest_team_logo)
	home_asv = home.get('id') == "asv"
	max_size = 800 if home_asv else 620
	home_logo_to_draw = resize_square(home_logo, max_size)
	home_x_offset = 10 if home_asv else 0
	home_x = int(600 - home_logo_to_draw.size[0]/2 + home_x_offset)
	home_y_offset = 40 if not home_asv else 0
	home_y = int(680 - home_logo_to_draw.size[1]/2 + home_y_offset)
	max_size = 800 if not home_asv else 620
	guest_logo_to_draw = resize_square(guest_logo, max_size)
	guest_x_offset = 60 if not home_asv else 60
	guest_x = int(1320 - guest_logo_to_draw.size[0]/2 + guest_x_offset)
	guest_y_offset = 40 if home_asv else 0
	guest_y = int(680 - guest_logo_to_draw.size[1]/2 + guest_y_offset)

	img.paste(home_logo_to_draw, (home_x, home_y), home_logo_to_draw)
	img.paste(guest_logo_to_draw, (guest_x, guest_y), guest_logo_to_draw)

	# paste teams
	home_team_name = home.get('name')
	if int(team_home) == 2:
		home_team_name += " 2"
	elif int(team_home) == 3:
		home_team_name += " 3"
	guest_team_name = guest.get('name')
	if int(team_guest) == 2:
		guest_team_name += " 2"
	elif int(team_guest) == 3:
		guest_team_name += " 3"

	fonts_path = os.path.abspath(os.path.dirname(__file__)) + "/fonts/"

	font_teams = ImageFont.truetype(os.path.join(fonts_path, 'BebasNeue.ttf'), 155)
	draw = ImageDraw.Draw(img)
	minus = "-"
	home_team_width1, nw = draw.textsize(home_team_name, font=font_teams)
	guest_team_width1, nw = draw.textsize(guest_team_name, font=font_teams)
	minus_width1, nw = draw.textsize(minus, font=font_teams)
	draw.text((1000-(home_team_width1/2), 1140), home_team_name, (0, 0, 0), font=font_teams)
	draw.text((1000-(minus_width1/2), 1260), minus, (0, 0, 0), font=font_teams)
	draw.text((1000-(guest_team_width1/2), 1380), guest_team_name, (0, 0, 0), font=font_teams)
	# TODO: Fix width of text if too long

	# paste date
	# print(date, time)
	font_date = ImageFont.truetype(os.path.join(fonts_path, 'Manrope-Regular.ttf'), 80)
	date_a_width, nw = draw.textsize(date, font=font_date)
	date_b_width, nw = draw.textsize(time, font=font_date)
	draw.text((1000-(date_a_width/2), 1650), date, (255, 255, 255), font=font_date)
	draw.text((1000-(date_b_width/2), 1780), time, (255, 255, 255), font=font_date)

	# paste liga
	font_liga = ImageFont.truetype(os.path.join(fonts_path, 'BebasNeue.ttf'), 120)
	liga_width, nw = draw.textsize(liga, font=font_liga)
	draw.text((1000-(liga_width/2)+3, 152), liga, (190, 176, 0), font=font_liga)
	draw.text((1000-(liga_width/2), 150), liga, (0, 0, 0), font=font_liga)

	# paste table
	"""
	font_table = ImageFont.truetype(os.path.join(fonts_path, 'Bebas Neue.ttf'), 36)
	table_home_team = str.format("{}.", rank_home)
	home_table_width = draw.textsize(table_home_team, font=font_table)[0]
	draw.text((80 - home_table_width/2, 360), table_home_team, (0, 0, 0), font=font_table)
	table_guest_team = str.format("{}.", rank_guest)
	guest_table_width = draw.textsize(table_guest_team, font=font_table)[0]
	draw.text((1080-80-guest_table_width/2, 360), table_guest_team, (0,0,0), font=font_table)
	"""

	img_io = io.BytesIO()
	img.save(img_io, 'PNG', quality=100)
	img_io.seek(0)

	# cwd_path = os.path.abspath(os.getcwd())
	# img_name = f"{date[-10:].replace('.', '-').replace(':', '_')}_{time.replace(':', '-')}_{liga}_instagram.png"
	# img_name = f"{liga}_instagram.png"
	# img_path = rf"{cwd_path}\temp-images\{img_name}"
	# img.save(img_path, 'PNG', quality=100)

	return img_io
