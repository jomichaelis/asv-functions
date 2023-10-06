from PIL import Image, ImageFont, ImageDraw
import os
import io


def resize_ig(image):
    maxsize = 450
    rs_width, rs_height = image.size
    ratio = min(maxsize/rs_width, maxsize/rs_height)
    return image.resize((round(rs_width*ratio), round(rs_height*ratio)), Image.LANCZOS)


def create_image(home, guest, team_home, team_guest, rank_home, rank_guest, date, time, liga):

    width = 1080
    height = 1920

    img = Image.new('RGB', size=(width, height))

    # paste logos
    home_team_logo = home.get('id') + ".png"
    guest_team_logo = guest.get('id') + ".png"
    background = Image.open(os.path.abspath(os.path.dirname(__file__)) + "/background_black_insta.png")
    img.paste(background)
    home_logo = Image.open(os.path.abspath(os.path.dirname(__file__)) + '/logos/' + home_team_logo)
    guest_logo = Image.open(os.path.abspath(os.path.dirname(__file__)) + '/logos/' + guest_team_logo)
    home_logo_to_draw = resize_ig(home_logo)
    home_x = int(270 - home_logo_to_draw.size[0]/2)
    home_y = int(680 - home_logo_to_draw.size[1]/2)
    guest_logo_to_draw = resize_ig(guest_logo)
    guest_x = int(1080 - 270 - guest_logo_to_draw.size[0]/2)
    guest_y = int(680 - guest_logo_to_draw.size[1]/2)

    img.paste(home_logo_to_draw, (home_x, home_y), home_logo_to_draw)
    img.paste(guest_logo_to_draw, (guest_x, guest_y), guest_logo_to_draw)
   
    home_team_full = list

    #paste teams
    home_long1 = home.get('long1')
    home_long2 = home.get('long2')
    if int(team_home) == 2:
        home_long2 += " 2"
    elif int(team_home) == 3:
        home_long2 += " 3"
    guest_long1 = guest.get('long1')
    guest_long2 = guest.get('long2')
    if int(team_guest) == 2:
        guest_long2 += " 2"
    elif int(team_guest) == 3:
        guest_long2 += " 3"

    fonts_path = os.path.abspath(os.path.dirname(__file__)) + "/fonts/"
    font_teams = ImageFont.truetype(os.path.join(fonts_path, 'CaviarDreams_Bold.ttf'), 60)
    draw = ImageDraw.Draw(img)
    home_team_width1, nw = draw.textsize(home_long1, font=font_teams)
    home_team_width2, nw = draw.textsize(home_long2, font=font_teams)
    guest_team_width1, nw = draw.textsize(guest_long1, font=font_teams)
    guest_team_width2, nw = draw.textsize(guest_long2, font=font_teams)
    draw.text((270-home_team_width1/2, 960), home_long1, (0, 0, 0), font=font_teams)
    draw.text((270-home_team_width2/2, 1040), home_long2, (0, 0, 0), font=font_teams)
    draw.text((1080-270-guest_team_width1/2, 960), guest_long1, (0, 0, 0), font=font_teams)
    draw.text((1080-270-guest_team_width2/2, 1040), guest_long2, (0, 0, 0), font=font_teams)

    # paste date
    # print(date, time)
    font_date = ImageFont.truetype(os.path.join(fonts_path, 'CaviarDreams.ttf'), 100)
    date_a_width, nw = draw.textsize(date[:-4], font=font_date)
    date_b_width, nw = draw.textsize(time, font=font_date)
    draw.text(((1080-date_a_width)/2, 1270), date[:-4], (255, 255, 0), font=font_date)
    draw.text(((1080-date_b_width)/2, 1400), time, (255, 255, 0), font=font_date)
    
    # paste liga
    font_liga = ImageFont.truetype(os.path.join(fonts_path, 'CaviarDreams.ttf'), 58)
    liga_width, nw = draw.textsize(liga, font=font_liga)
    draw.text(((1080-liga_width)/2, 200), liga, (0, 0, 0), font=font_liga)

    # paste table
    font_table = ImageFont.truetype(os.path.join(fonts_path, 'CaviarDreams_Bold.ttf'), 36)
    table_home_team = str.format("{}.", rank_home)
    home_table_width = draw.textsize(table_home_team, font=font_table)[0]
    draw.text((80 - home_table_width/2, 360), table_home_team, (0, 0, 0), font=font_table)
    table_guest_team = str.format("{}.", rank_guest)
    guest_table_width = draw.textsize(table_guest_team, font=font_table)[0]
    draw.text((1080-80-guest_table_width/2, 360), table_guest_team, (0,0,0), font=font_table)

    img_io = io.BytesIO()
    img.save(img_io, 'PNG', quality=100)
    img_io.seek(0)

    # cwd_path = os.path.abspath(os.getcwd())
    # img_name = f"{date[-10:].replace('.', '-').replace(':', '_')}_{time.replace(':', '-')}_{liga}_instagram.png"
    # img_name = f"{liga}_instagram.png"
    # img_path = rf"{cwd_path}\temp-images\{img_name}"
    # img.save(img_path, 'PNG', quality=100)

    return img_io
