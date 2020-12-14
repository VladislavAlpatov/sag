import os
from PIL import ImageDraw, ImageFont, Image
import requests
from modules import siteParser


class Card:
    """
    User card generator
    Draw:nick,id,teg,avatar,server,creator checker
    """

    def __init__(self, font, author, guild, wallpaper):
        self.font = font  # шрифт
        self.author = author
        self.guild = guild
        self.body = Image.open(wallpaper)
        self.draw = ImageDraw.Draw(self.body)

    def __del__(self):
        print(f'{self} was deleted!')

    def build(self):
        # avatar
        img = requests.get(self.author.avatar_url)

        with open('ava.webp', 'wb') as f:
            f.write(img.content)

        with Image.open('ava.webp') as avatar:
            avatar = avatar.resize((164, 164), Image.ANTIALIAS)
            self.body.paste(avatar, (27, 34))

        # name
        font = ImageFont.truetype(self.font, 50, encoding="unic")
        self.draw.text((207, 18), self.author.name, font=font)
        # tag
        font = ImageFont.truetype(self.font, 30, encoding="unic")
        self.draw.text((207, 78), 'TAG: #' + str(self.author.discriminator), font=font)
        # id
        font = ImageFont.truetype(self.font, 25, encoding="unic")
        self.draw.text((207, 118), 'ID: ' + str(self.author.id), font=font)
        # server
        font = ImageFont.truetype(self.font, 25, encoding="unic")
        self.draw.text((207, 150), 'SERVER: ' + self.guild.name, font=font)
        # creator mark
        if self.author.id == 566653752451399700:
            with Image.open('media/card/developer_ico.png') as avatar:
                avatar = avatar.resize((50, 50), Image.ANTIALIAS)
                self.body.paste(avatar, (625, 0), avatar)
        else:
            pass

        # сохраняем
        self.body.save('card.jpg')

    @staticmethod
    def cleanfiles():
        # clean up
        os.remove('card.jpg')
        os.remove('ava.webp')


class Stats(siteParser.Tf2stats):
    def __init__(self, font, color, author):
        super().__init__()
        self.font = font
        self.color = color
        self.author = author
        self.body = Image.open('media/stats.png')
        self.draw = ImageDraw.Draw(self.body)

    def build(self):
        with Image.open('media/tf2label.png') as f:
            f = f.resize((600, 137), Image.ANTIALIAS)
            f.convert('RGB')
            self.body.paste(f, (0, 50), f)

        font = ImageFont.truetype(self.font, 80, encoding="unic")
        self.draw.text((0, 200), f'Last hour: {self.getMinutesOnline()}', font=font, fill=self.color)
        self.draw.text((0, 305), f'24-hour peak: {self.getDayOnline()}', font=font, fill=self.color)
        self.draw.text((0, 400), f'All-time peak: {self.getAllTimeOnline()}', font=font, fill=self.color)
        self.body.save(f'{self.author.id}.png')

    def cleanfiles(self):
        os.remove(f'{self.author.id}.png')