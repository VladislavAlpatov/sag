import datetime
import os
import SiteParser
import discord
import qrcode
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
from discord.ext import commands
import config
import markovify


def sentense(file: str):
    with open(file, 'r') as f:
        text = f.read()

    out = None
    text_model = markovify.Text(text
                                )
    while out is None:
        out = text_model.make_sentence()
    return out


bot = commands.Bot(command_prefix='cat_', intents=discord.Intents.all())  # префикс для комманд
bot.remove_command('help')


@bot.event
async def on_ready():
    print('READY!')
    await bot.change_presence(activity=discord.Game(f'cathook.club'))


@bot.event
async def on_message(message):
    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    # выдача ролец для своего сервер (Hacker space)
    print(member)


@bot.command(aliases=['help'])
async def help_message(ctx):  # send help message
    date = datetime.datetime.now()
    embed = discord.Embed(title='**FEATURES**', description='Discord cathook bot.', color=0x0095ff, )
    # заголовки
    embed.add_field(name=f'**{bot.command_prefix}help**', value='Send this message.', inline=False)
    embed.add_field(name=f'**{bot.command_prefix}cat**', value='Send random cat image.', inline=False)
    embed.add_field(name=f'**{bot.command_prefix}feature**', value='Random cathook feature.', inline=False)
    embed.add_field(name=f'**{bot.command_prefix}joke**', value='Send joke.', inline=False)
    embed.add_field(name=f'**{bot.command_prefix}steam**', value='Check steam profile.', inline=False)
    embed.add_field(name=f'**{bot.command_prefix}card**', value='Send your profile card.', inline=False)
    embed.add_field(name=f'**{bot.command_prefix}nigga**', value='Make nigga meme.', inline=False)
    embed.add_field(name=f'**{bot.command_prefix}qr**', value='Make qrcode.', inline=False)
    embed.add_field(name=f'**{bot.command_prefix}online**', value='Show TF2 online stats.', inline=False)
    embed.add_field(name=f'**{bot.command_prefix}cathook**', value='Send cathook github repo.', inline=False)
    embed.add_field(name=f'**{bot.command_prefix}howgayami**', value='Show gayness percent.', inline=False)
    embed.add_field(name=f'**{bot.command_prefix}why**', value='Another russian meme.', inline=False)
    embed.add_field(name=f'**{bot.command_prefix}howfurryami**', value='Show furry percent.', inline=False)
    embed.add_field(name=f'**{bot.command_prefix}think**', value='Make russian meme.', inline=False)
    embed.set_thumbnail(url='https://i.imgur.com/WK520CI.jpg')
    embed.set_footer(text=f'cathook.club {date.day}/{date.month}/{date.year}',
                     icon_url='https://i.imgur.com/WK520CI.jpg')
    embed.set_author(name=bot.user.name, icon_url='https://i.imgur.com/WK520CI.jpg')
    await ctx.send(embed=embed)


@bot.command()
async def cat(ctx):
    image = requests.get('https://thiscatdoesnotexist.com/', headers=config.Bot_info.heads)
    with open('cat.jpg', 'wb') as f:
        f.write(image.content)
    await ctx.send(file=discord.File('cat.jpg'))
    os.remove('cat.jpg')


@bot.command()
async def feature(ctx):
    await ctx.send(sentense('text-models/features-model.txt'))


@bot.command()
async def cathook(ctx):
    await ctx.send("https://github.com/nullworks/cathook")


@bot.command()
async def joke(ctx):
    url = requests.get('https://jokes.lol/random-jokes/', headers=config.Bot_info.heads)
    soup = BeautifulSoup(url.text, 'html.parser')
    soup = soup.find('div', {'class': 'query-field query-field-post_content'})
    await ctx.send(soup.text)


@bot.command()
async def steam(ctx, url_custom):
    account = SiteParser.Steam(url_custom)

    embed = discord.Embed(title=f'**{account.getNick()}**', description=account.getGameStatus(), color=0x0095ff)
    embed.add_field(name='**Profile lvl.**', value=account.getLvl(), inline=False)
    embed.add_field(name='**VAC**', value=account.getVacStatus(), inline=False)
    embed.add_field(name='**Comments.**', value=account.getTotalComments(), inline=False)
    embed.add_field(name='**Friends.**', value=account.getTotalFriends(), inline=False)
    embed.add_field(name='**Games.**', value=account.getTotalGames(), inline=False)
    embed.add_field(name='**Bages.**', value=account.getTotalBages(), inline=False)
    embed.add_field(name='**Screenshots.**', value=account.getTotalScreenshots(), inline=False)
    embed.set_thumbnail(url=account.getProfilePicture())
    embed.set_author(name='Steam profile checker.', icon_url='https://i.imgur.com/WK520CI.jpg')
    embed.set_footer(text=url_custom,
                     icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/512px'
                              '-Steam_icon_logo.svg.png')
    try:
        await ctx.message.delete()
    except discord.errors.Forbidden:
        pass

    await ctx.send(embed=embed)


@bot.command()
async def card(ctx):
    class Card:
        """
        User card generator
        Draw:nick,id,teg,avatar,server,creator checker
        """
        def __init__(self, font, wallpaper):
            self.font = font  # шрифт
            self.author = ctx.message.author
            self.guild = ctx.message.guild.name
            self.body = Image.open(wallpaper)
            self.draw = ImageDraw.Draw(self.body)

        def __del__(self):
            print(f'{self} was deleted!')

        def addavatar(self):
            avatar = str(ctx.author.avatar_url)
            img = requests.get(avatar, headers=config.Bot_info.heads)

            with open('ava.webp', 'wb') as f:
                f.write(img.content)

            with Image.open('ava.webp') as avatar:
                avatar = avatar.convert('RGB')
                avatar = avatar.resize((164, 164), Image.ANTIALIAS)
                self.body.paste(avatar, (27, 34))

        def build(self):
            # ник
            font = ImageFont.truetype(self.font, 50, encoding="unic")
            self.draw.text((207, 18), self.author.name, font=font)
            # тег
            font = ImageFont.truetype(self.font, 30, encoding="unic")
            self.draw.text((207, 78), 'TAG: #' + str(self.author.discriminator), font=font)
            # id
            font = ImageFont.truetype(self.font, 25, encoding="unic")
            self.draw.text((207, 118), 'ID: ' + str(self.author.id), font=font)
            # серер
            font = ImageFont.truetype(self.font, 25, encoding="unic")
            self.draw.text((207, 150), 'SERVER: ' + self.guild, font=font)
            # метка создателя
            if self.author.id == 566653752451399700:
                with Image.open('media/card/developer_ico.png') as avatar:
                    avatar = avatar.resize((100, 100), Image.ANTIALIAS)
                    avatar.convert('RGB')
                    self.body.paste(avatar, (573, 0), avatar)
            else:
                pass

            # сохраняем
            self.body.save('card.jpg')

        @staticmethod
        def cleanfiles():
            # удаление файлов
            os.remove('card.jpg')
            os.remove('ava.webp')

    user = Card('media/fonts/sans.ttf',
                'media/card/steam_background.jpg')
    user.addavatar()
    user.build()
    await ctx.send(file=discord.File('card.jpg'))
    user.cleanfiles()
    del user


@bot.command()
async def nigga(ctx, *, text):
    if int(len(text)) < 40:
        if 8 <= int(len(text)) <= 10:
            large = 65
        elif int(len(text)) >= 12:
            large = 50
        else:
            large = 90

        if int(len(text)) >= 4:
            to_sum = 8
        else:
            to_sum = 3

        image = Image.open('media/nigga/nigga.jpg')
        draw = ImageDraw.Draw(image)
        font_name = 'media/fonts/arialbd.ttf'
        font = ImageFont.truetype(font_name, large, encoding="unic")
        draw.text((200 - int(len(text)) * to_sum, 600 - large), str(text), fill=(0, 0, 0), font=font)
        image.save('nigga-out.jpg')
        await ctx.send(file=discord.File('nigga-out.jpg'))
        os.remove('nigga-out.jpg')
    else:
        await ctx.send('To many symbols')


@bot.command()
async def rename(ctx, *, name):
    if ctx.message.author.id == 566653752451399700:
        try:
            await bot.user.edit(username=name)
            await ctx.send(f'Nickname was changed on {str(name)} ')
        except discord.errors.HTTPException as e:
            await ctx.send(e)
    else:
        await ctx.send('Access denied!')


@bot.command()
async def qr(ctx, *, text):
    if int(len(text)) <= 100:
        image = qrcode.make(str(text))
        image.save('code.png')

        await ctx.send(file=discord.File('code.png'))
        os.remove('code.png')
    else:
        await ctx.send('You cant create qrcode with 100 symbols or more!')


@bot.command()
async def howgayami(ctx):
    await ctx.send(f'Look! {ctx.message.author} is {str(random.randint(0, 100))}% gay!')


@bot.command()
async def howfurryami(ctx):
    if ctx.message.author.id == 566653752451399700:
        await ctx.send(content=f'{ctx.message.author} is **100%** furry!')
    else:
        await ctx.send(content=f'{ctx.message.author} is **{str(random.randint(0, 100))}%** furry!')


@bot.command(aliases=['мысль', 'гигант'])
async def think(ctx):
    url = ctx.message.attachments[0].url
    r = requests.get(str(url))

    with open('image.jpg', 'wb') as f:
        f.write(r.content)

    image = Image.open('media/think/гигант_мысли.jpg')
    image_on_paste = Image.open('image.jpg')

    image_on_paste = image_on_paste.resize((500, 400), Image.ANTIALIAS)
    image.paste(image_on_paste, (130, 13))

    image.save(f'{str(ctx.author.id)}.png')

    await ctx.message.delete()
    await ctx.send(file=discord.File(f'{str(ctx.author.id)}.png'))

    os.remove(f'{str(ctx.author.id)}.png')
    os.remove('image.jpg')


@bot.command(aliases=['зачем', 'нахуя'])
async def why(ctx):
    url = ctx.message.attachments[0].url
    r = requests.get(str(url))

    with open('image.jpg', 'wb') as f:
        f.write(r.content)

    image = Image.open('media/think/why.jpg')
    image_on_paste = Image.open('image.jpg')

    image_on_paste = image_on_paste.resize((614, 336), Image.ANTIALIAS)
    image.paste(image_on_paste, (72, 42))

    image.save(f'{str(ctx.author.id)}.png')

    await ctx.message.delete()
    await ctx.send(file=discord.File(f'{str(ctx.author.id)}.png'))

    os.remove(f'{str(ctx.author.id)}.png')
    os.remove('image.jpg')


@bot.command(aliases=['stats', 'tf2', 'online'])
async def tf2stats(ctx):
    class Stats(SiteParser.Tf2stats):

        def __init__(self, font, color):
            self.font = font
            self.color = color
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
            self.body.save(f'{str(ctx.author.id)}.png')

        @staticmethod
        def cleanfiles():
            os.remove(f'{str(ctx.author.id)}.png')

    img = Stats('media/fonts/tf2build.ttf', (255, 255, 255))
    img.build()
    await ctx.send(file=discord.File(f'{str(ctx.author.id)}.png'))
    img.cleanfiles()


bot.run('NzY3MDY4MDA1Nzk5OTUyMzg1.X8YcPA.eYn8HACFeR2fodTDZlUas31MtM8', bot=False)
