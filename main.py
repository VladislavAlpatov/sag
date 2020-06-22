import datetime
import os
import subprocess

import discord
import qrcode
import random2
import requests
from PIL import Image
from PIL import ImageDraw, ImageFont
from bs4 import BeautifulSoup
from discord.ext import commands

import config

_wins = ['windows', 'шиндовс', 'видоувз', 'виндоус', 'винда']

_games = ['/help', 'CAT-BOT', 'cathook', 'cathook by nullworks',
          'made by nullifiedvlad', 'we need some cats']

bot = commands.Bot(command_prefix='/')  # префикс для комманд
bot.remove_command('help')


@bot.event
async def on_ready():
    print('READY!')


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    """
    global chaise
    msg = message.content
    for _ in _wins:
        chaise = fuzz.ratio(msg, _)
        if chaise >= 50:
            break
    print(str(chaise))
    if chaise >= 50 and message.author.id != 709698597415026707:
        await message.delete()
        await message.channel.send("We don't like windows here!")
    pass
"""


@bot.command(aliases=['help'])
async def help_message(ctx):  # send help message
    date = datetime.datetime.now()
    embed = discord.Embed(title='**FEATURES**', description='Discord cathook bot.', color=0x0095ff, )
    # заголовки
    embed.add_field(name='**/help**', value='Send this message.', inline=False)
    embed.add_field(name='**/cat**', value='Send random cat image.', inline=False)
    embed.add_field(name='**/feature**', value='Random cathook feature.', inline=False)
    embed.add_field(name='**/joke**', value='Send joke.', inline=False)
    embed.add_field(name='**/steam**', value='Check steam profile.', inline=False)
    embed.add_field(name='**/card**', value='Send your profile card.', inline=False)
    embed.add_field(name='**/invite**', value='Send bot invitation.', inline=False)
    embed.add_field(name='**/nigga**', value='Make nigga meme.', inline=False)
    embed.add_field(name='**/qr**', value='Make qrcode.', inline=False)
    embed.add_field(name='**/cathook**', value='Send cathook github repo.', inline=False)
    embed.add_field(name='**/howgayiam**', value='Show gayness percent.', inline=False)
    embed.add_field(name='**/py3**', value='Interpritate python3 code.', inline=False)
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
    await ctx.send(random2.choice(config.Cathook.features))


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
    class Steam:
        def __init__(self, data):
            self.data = BeautifulSoup(requests.get(str(data)).text, 'html.parser')
            self.url = str(url_custom)

        def getNick(self):
            return self.data.find('span', {'class': 'actual_persona_name'}).text

        def getLvl(self):
            return int(self.data.find('span', {'class': 'friendPlayerLevelNum'}).text)

        def getGameStatus(self):
            return self.data.find('div', {'class': 'profile_in_game_header'}).text

        def getVacStatus(self):
            if bool(self.data.find('div', {'class': 'profile_ban'})):
                return str(self.data.find('div', {'class': 'profile_ban'}).text[:-7])
            else:
                return str('No VAC on record.')

        def getProfilePicture(self):
            image = self.data.find('div', {'class': 'playerAvatarAutoSizeInner'})
            image = str(image.find('img'))
            return image[10:-3]

        def getTotalGames(self):
            try:
                games_block = self.data.find('a', {'href': f'{self.url}games/?tab=all'})
                return int(games_block.find('span', {'class': 'profile_count_link_total'}).text)

            except Exception as e:
                print(e)
                return str('Not stated')

        def getTotalComments(self):
            try:
                comments_block = self.data.find('a', {'class': 'commentthread_allcommentslink'})
                return comments_block.find('span').text

            except Exception as e:
                print(e)
                return str('Not stated')

        def getTotalScreenshots(self):
            try:
                screenshot_block = self.data.find('a', {'href': f'{self.url}screenshots/'})
                return int(screenshot_block.find('span', {'class': 'profile_count_link_total'}).text)
            except Exception as e:
                print(e)
                return str('Not stated')

        def getTotalFriends(self):
            try:
                friend_block = self.data.find('a', {'href': f'{self.url}friends/'})
                friends = friend_block.find('span', {'class': 'profile_count_link_total'})

                del friend_block
                return int(friends.text)
            except Exception as e:
                print(e)
                return str('Not stated')

        def getTotalBages(self):
            try:
                bages_block = self.data.find('a', {'href': f'{self.url}badges/'})
                return bages_block.find('span', {'class': 'profile_count_link_total'}).text
            except Exception as e:
                print(e)
                return str('Not stated')

    account = Steam(data=url_custom)

    embed = discord.Embed(title=f'**{account.getNick()}**', description=account.getGameStatus(), color=0x0095ff)
    embed.add_field(name='**Profile lvl.**', value=str(account.getLvl()), inline=False)
    embed.add_field(name='**VAC.**', value=str(account.getVacStatus()), inline=False)
    embed.add_field(name='**Total comments.**', value=str(account.getTotalComments()), inline=False)
    embed.add_field(name='**Total friends.**', value=str(account.getTotalFriends()), inline=False)
    embed.add_field(name='**Total games.**', value=str(account.getTotalGames()), inline=False)
    embed.add_field(name='**Total bages.**', value=str(account.getTotalBages()), inline=False)
    embed.add_field(name='**Total screenshots.**', value=str(account.getTotalScreenshots()), inline=False)
    embed.set_thumbnail(url=account.getProfilePicture())
    embed.set_footer(text=url_custom)
    await ctx.message.delete()
    await ctx.send(embed=embed)


@bot.command()
async def img(ctx, *, text):
    x = len(text) * 6
    color = (255, 0, 229)
    image = Image.new('RGB', (x + 10, 50), color)
    draw_on_image = ImageDraw.Draw(image)
    draw_on_image.text((10, 20), str(text), )
    image.save('img.jpg')

    await ctx.send(file=discord.File('img.jpg'))
    os.remove('img.jpg')


@bot.command()
async def card(ctx):
    font_name = 'media\\fonts\\arialbd.ttf'
    # получаем инфу
    author = ctx.message.author
    guild = ctx.message.guild.name

    # парсим и сохраняем аву
    avatar = str(ctx.author.avatar_url)
    image = requests.get(avatar, headers=config.Bot_info.heads)
    with open('ava.webp', 'wb') as f:
        f.write(image.content)

    # создаём изображение
    image = Image.open('media\\card\\background.jpg')
    draw = ImageDraw.Draw(image)

    # получаем аватар и подгоняем размер

    avatar = Image.open('ava.webp')
    avatar = avatar.convert('RGB')
    avatar = avatar.resize((421, 421), Image.ANTIALIAS)

    # получаем фотку бота и подгоняем по размеру
    bot_avatar = Image.open('media\\card\\cat.jpg')
    bot_avatar = bot_avatar.convert('RGB')
    bot_avatar = bot_avatar.resize((124, 124), Image.ANTIALIAS)

    # Ник
    font = ImageFont.truetype(font_name, 90, encoding="unic")
    draw.text((460, 0), str(author.name), fill=(3, 150, 255), font=font)
    # тег
    font = ImageFont.truetype(font_name, 50, encoding="unic")
    draw.text((460, 92), 'TAG: #' + str(author.discriminator), fill=(51, 255, 0), font=font)
    # id
    font = ImageFont.truetype(font_name, 50, encoding="unic")
    draw.text((460, 150), 'ID: ' + str(author.id), font=font)
    # сервер
    font = ImageFont.truetype(font_name, 50, encoding="unic")
    draw.text((460, 210), 'SERVER: ' + str(guild), fill=(0, 238, 255), font=font)
    # текс под фоткой бота
    font = ImageFont.truetype(font_name, 25, encoding="unic")
    draw.text((1385, 128), 'CAT-BOT', fill=(255, 255, 255), font=font)
    # проверка на создателя
    if author.id == 566653752451399700:
        font = ImageFont.truetype(font_name, 50, encoding="unic")
        draw.text((460, 270), 'Creator of this bot', font=font, fill=(255, 0, 229))
    else:
        pass

    # вставляем фото
    image.paste(avatar, (0, 0))

    # вставляем фото бота
    image.paste(bot_avatar, (1376, 0))

    # сохраняем и отправляем карточку
    image.save('card.jpg')
    await ctx.send(file=discord.File('card.jpg'))

    # удаление файлов
    os.remove('card.jpg')
    os.remove('ava.webp')


@bot.command()
async def invite(ctx):
    await ctx.send(config.Messages.invite)


@bot.command()
async def nigga(ctx, *, text):
    print(len(text))
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

        image = Image.open('media\\nigga\\nigga.jpg')
        draw = ImageDraw.Draw(image)
        font_name = 'media\\fonts\\arialbd.ttf'
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
        font_name = 'media\\fonts\\arialbd.ttf'
        large = 40
        font = ImageFont.truetype(font_name, large, encoding="unic")
        draw.text((10, 20), str(text), font=font)

        image.save('banner.jpg')
        await ctx.send(file=discord.File('banner.jpg'))
        os.remove('banner.jpg')
    else:
        await ctx.send('You cant create banner with 30 symbols or more!')


@bot.command()
async def howgayiam(ctx):
    await ctx.send(f'Look! {ctx.message.author} is {str(random2.randint(0, 100))}% gay!')


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

    image = Image.open('media\\think\\гигант_мысли.jpg')
    image_on_paste = Image.open('image.jpg')

    image_on_paste = image_on_paste.resize((500, 400), Image.ANTIALIAS)
    image.paste(image_on_paste, (130, 13))

    image.save('think.jpg')

    await ctx.message.delete()
    await ctx.send(file=discord.File('think.jpg'))

    os.remove('think.jpg')
    os.remove('image.jpg')


bot.run(config.Bot_info.token)
