import datetime
import os
import subprocess
import SiteParser
import discord
import qrcode
import random
import requests
from PIL import Image
from PIL import ImageDraw, ImageFont
from bs4 import BeautifulSoup
from discord.ext import commands
import asyncio
import config

bot = commands.Bot(command_prefix='/')  # префикс для комманд
bot.remove_command('help')


@bot.event
async def on_ready():
    print('READY!')

    with open('media/id.txt', 'r') as f:
        sid = f.read()

    channel = bot.get_channel(724987876911218690)

    while True:
        site = SiteParser.CtfBans('https://bans.creators.tf/index.php?p=banlist')
        sid_now = site.steam_id

        if sid != sid_now:
            # информация о забаненом игроке
            prof_url = site.steam_ulr.replace('\n', '')
            profile = SiteParser.Steam(prof_url)
            image = profile.getProfilePicture()
            # создание ембиенда
            embed = discord.Embed(title=f'**{site.name}**', color=0xff5959, )
            embed.add_field(name='**LENGTH**', value=site.length, inline=False)
            embed.add_field(name='**DATE**', value=site.date, inline=False)
            embed.add_field(name='**STEAM ID**', value=site.steam_id, inline=False)
            embed.add_field(name='**REASON**', value=site.reason, inline=False)
            embed.set_footer(text=site.steam_ulr, icon_url='https://bit.ly/2NrVOIk')
            embed.set_thumbnail(url=image)
            await channel.send(embed=embed)
            # обновленик sid
            sid = sid_now
            with open('media/id.txt', 'w') as f:
                f.write(sid)

        else:
            pass
        await bot.change_presence(activity=discord.Game(f'with {len(bot.guilds)} servers.'))
        await asyncio.sleep(5)


@bot.event
async def on_message(message):
    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    # выдача ролец для своего сервер (Hacker space)
    if member.guild.id == 665856387439656972:
        role = member.guild.get_role(665877780864565249)
        await member.add_roles(role)
    else:
        pass

    await member.send(f'Welcome to {member.guild}!')


@bot.command(aliases=['help'])
async def help_message(ctx):  # send help message
    date = datetime.datetime.now()
    embed = discord.Embed(title='**FEATURES**', description='Discord cathook bot.', color=0x0095ff, )
    # заголовки
    embed.add_field(name='**/help**', value='Send this message.', inline=False)
    embed.add_field(name='**/cat**', value='Send random cat image.', inline=False)
    # embed.add_field(name='**/feature**', value='Random cathook feature.', inline=False)
    embed.add_field(name='**/joke**', value='Send joke.', inline=False)
    embed.add_field(name='**/steam**', value='Check steam profile.', inline=False)
    embed.add_field(name='**/card**', value='Send your profile card.', inline=False)
    embed.add_field(name='**/invite**', value='Send bot invitation.', inline=False)
    embed.add_field(name='**/nigga**', value='Make nigga meme.', inline=False)
    embed.add_field(name='**/qr**', value='Make qrcode.', inline=False)
    embed.add_field(name='**/cathook**', value='Send cathook github repo.', inline=False)
    embed.add_field(name='**/howgayami**', value='Show gayness percent.', inline=False)
    embed.add_field(name='**/why**', value='Another russian meme.', inline=False)
    embed.add_field(name='**/howfurryami**', value='Show furry percent.', inline=False)
    embed.add_field(name='**/think**', value='Make russian meme.', inline=False)
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
    await ctx.send(random.choice(config.Cathook.features))


@bot.command()
async def cathook(ctx):
    await ctx.send(config.Cathook.download)


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
    embed.add_field(name='**Profile lvl.**', value=str(account.getLvl()), inline=False)
    embed.add_field(name='**VAC.**', value=str(account.getVacStatus()), inline=False)
    embed.add_field(name='**Total comments.**', value=str(account.getTotalComments()), inline=False)
    embed.add_field(name='**Total friends.**', value=str(account.getTotalFriends()), inline=False)
    embed.add_field(name='**Total games.**', value=str(account.getTotalGames()), inline=False)
    embed.add_field(name='**Total bages.**', value=str(account.getTotalBages()), inline=False)
    embed.add_field(name='**Total screenshots.**', value=str(account.getTotalScreenshots()), inline=False)
    embed.set_thumbnail(url=account.getProfilePicture())
    embed.set_author(name='Steam profile checker.', icon_url='https://i.imgur.com/WK520CI.jpg')
    embed.set_footer(text=url_custom,
                     icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/512px'
                              '-Steam_icon_logo.svg.png')
    await ctx.message.delete()
    await ctx.send(embed=embed)


@bot.command()
async def card(ctx):
    class Card:
        def __init__(self, font, wallpaper):
            self.font = font  # шрифт
            self.wallpaper = wallpaper  # фон картинки
            self.author = ctx.message.author
            self.guild = ctx.message.guild.name
            self.body = Image.open(self.wallpaper)
            self.draw = ImageDraw.Draw(self.body)
        
        def addAvatar(self):
            avatar = str(ctx.author.avatar_url)
            img = requests.get(avatar, headers=config.Bot_info.heads)

            with open('ava.webp', 'wb') as f:
                f.write(img.content)

            with Image.open('ava.webp') as avatar:
                avatar = avatar.convert('RGB')
                avatar = avatar.resize((164, 164), Image.ANTIALIAS)
                self.body.paste(avatar, (27, 34))

        def drawNick(self):
            font = ImageFont.truetype(self.font, 50, encoding="unic")
            self.draw.text((207, 18), self.author.name, font=font)

        def drawTeg(self):
            font = ImageFont.truetype(self.font, 30, encoding="unic")
            self.draw.text((207, 78), 'TAG: #' + str(self.author.discriminator), font=font)

        def drawID(self):
            font = ImageFont.truetype(self.font, 25, encoding="unic")
            self.draw.text((207, 118), 'ID: ' + str(self.author.id), font=font)

        def drawServer(self):
            font = ImageFont.truetype(self.font, 25, encoding="unic")
            self.draw.text((207, 150), 'SERVER: ' + self.guild, font=font)

        def creatorChecker(self):
            if self.author.id == 566653752451399700:
                with Image.open('media/card/developer_ico.png') as avatar:
                    avatar = avatar.resize((100, 100), Image.ANTIALIAS)
                    avatar.convert('RGB')
                    self.body.paste(avatar, (573, 0), avatar)
            else:
                pass

            # сохраняем и отправляем карточку

        def build(self, name: str):
            self.body.save(name)

        @staticmethod
        def cleanFiles():
            # удаление файлов
            os.remove('card.jpg')
            os.remove('ava.webp')

    user = Card('media/fonts/sans.ttf',
                'media/card/steam_background.jpg')

    user.addAvatar()
    user.drawNick()
    user.drawID()
    user.drawTeg()
    user.drawServer()
    user.creatorChecker()
    user.build('card.jpg')
    await ctx.send(file=discord.File('card.jpg'))
    user.cleanFiles()


@bot.command()
async def invite(ctx):
    await ctx.send(config.Messages.invite)


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
async def banner(ctx, *, text):
    symbols = int(len(text))
    print(str(symbols))
    if symbols < 30:

        if 1 <= symbols < 12:
            y = 30
        elif 12 <= symbols < 24:
            y = 37
        else:
            y = 15
        image = Image.new('RGB', ((symbols * y), 70), (59, 196, 255))
        draw = ImageDraw.Draw(image)
        font_name = 'media/fonts/arialbd.ttf'
        large = 40
        font = ImageFont.truetype(font_name, large, encoding="unic")
        draw.text((10, 20), str(text), font=font)

        image.save('banner.jpg')
        await ctx.send(file=discord.File('banner.jpg'))
        os.remove('banner.jpg')
    else:
        await ctx.send('You cant create banner with 30 symbols or more!')


@bot.command()
async def howgayami(ctx):
    await ctx.send(f'Look! {ctx.message.author} is {str(random.randint(0, 100))}% gay!')


@bot.command()
async def howfurryami(ctx):
    if ctx.message.author.id == 566653752451399700:
        result = 100
        await ctx.send(content=f'{ctx.message.author} is **{result}%** furry!')
    else:
        await ctx.send(content=f'{ctx.message.author} is **{str(random.randint(0, 100))}%** furry!')


@bot.command()
async def py3(ctx, *, code):
    if ctx.message.author.id == 566653752451399700:
        _banned_commands = ['os.remove', 'os.system', 'os.kill', 'subprocess.check_output']
        code = code[:-3]
        code = code[5:]
        for command in _banned_commands:
            code = code.replace(command, 'print')
        with open('code.py', 'w') as f:
            f.write(str(code))
        out = subprocess.check_output(['python3', 'code.py'])
        os.remove('code.py')
        await ctx.send(f'```{out}```')
    else:
        await ctx.send('Access denied!')


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

    image.save('think.jpg')

    await ctx.message.delete()
    await ctx.send(file=discord.File('think.jpg'))

    os.remove('think.jpg')
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

    image.save('think.jpg')

    await ctx.message.delete()
    await ctx.send(file=discord.File('think.jpg'))

    os.remove('think.jpg')
    os.remove('image.jpg')


bot.run(config.Bot_info.token)
