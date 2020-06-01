import random2
import discord
from discord.ext import commands
import os
import config
from bs4 import BeautifulSoup
import requests
from PIL import Image
from PIL import ImageDraw, ImageFont
import qrcode
import datetime
from fuzzywuzzy import fuzz
import subprocess

_wins = ['windows', 'шиндовс', 'видоувз', 'виндоус', 'винда']

_games = ['/help', 'CAT-BOT', 'cathook', 'cathook by nullworks',
          'made by nullifiedvlad', 'we need some cats']

bot = commands.Bot(command_prefix='/')  # префикс для комманд
bot.remove_command('help')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(_games[0]))


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    global chaise
    msg = message.content
    if fuzz.ratio(msg, 'cat') >= 50 and message.author.id != 709698597415026707 and message.content != '/card' or \
            message.content != 'cat':
        await message.channel.send('Someone said the cat? :zoomer:')

    for _ in _wins:
        chaise = fuzz.ratio(msg, _)
        if chaise >= 50:
            break
    print(str(chaise))
    if chaise >= 50 and message.author.id != 709698597415026707:
        await message.delete()
        await message.channel.send("We don't like windows here!")
    pass


@bot.command()
async def help(ctx):  # send help message
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
    embed.add_field(name='**/sourcecode**', value='Send bot source code.', inline=False)
    embed.add_field(name='**/cathook**', value='Send cathook github repo.', inline=False)
    embed.add_field(name='**/howgayiam**', value='Show gayness percent.', inline=False)
    embed.add_field(name='**/py3**', value='Interpritate python3code.', inline=False)
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
async def steam(ctx, url):
    await ctx.message.delete()
    heads = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0'}
    r = requests.get(url, headers=heads)
    soup = BeautifulSoup(r.text, 'html.parser')
    # получаем ник и уровень
    nick = soup.findAll('span', {'class': 'actual_persona_name'})
    lvl = soup.findAll('span', {'class': 'friendPlayerLevelNum'})
    # получаем статус и вак статус
    status = soup.findAll('div', {'class': 'profile_in_game_header'})
    isVAC = soup.find('div', {'class': 'profile_ban_status'})
    # получаем коллтчество коментариев
    try:
        comments_block = soup.find('a', {'class': 'commentthread_allcommentslink'})
        com_count = comments_block.find('span')

        # проверка вак бана
        if bool(isVAC):
            isVAC = 'VAC ban on record!'
        else:
            isVAC = 'No VAC on record!'
        # отправка сообщения
        await ctx.send(f'''
**Nickname: **{nick[0].text}
**VAC: **{isVAC}
**Level: **{lvl[0].text}
**Status: **{status[0].text}
**Comments: **{com_count.text}
    ''')
    except AttributeError:
        await ctx.send('Sorry, this profile is private!')


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
    font_name = 'media/fonts/arialbd.ttf'
    # получаем инфу
    author = ctx.message.author
    guild = ctx.message.guild.name
    avatar = str(ctx.author.avatar_url)

    # парсим и сохраняем аву
    image = requests.get(avatar, headers=config.Bot_info.heads)
    with open('ava.webp', 'wb') as f:
        f.write(image.content)

    # создаём изображение
    image = Image.open('media/card/background.jpg')
    draw = ImageDraw.Draw(image)

    # получаем аватар и подгоняем размер

    avatar = Image.open('ava.webp')
    avatar = avatar.convert('RGB')
    avatar = avatar.resize((421, 421), Image.ANTIALIAS)

    # получаем фотку бота и подгоняем по размеру
    bot_avatar = Image.open('media/card/cat.jpg')
    bot_avatar = bot_avatar.convert('RGB')
    bot_avatar = bot_avatar.resize((124, 124), Image.ANTIALIAS)

    # Ник
    font = ImageFont.truetype(font_name, 90, encoding="unic")
    draw.text((460, 0), str(author.name), fill=(3, 150, 255), font=font)
    # тег
    font = ImageFont.truetype(font_name, 50, encoding="unic")
    draw.text((460, 90), 'TAG: #' + str(author.discriminator), fill=(51, 255, 0), font=font)
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


bot.run(config.Bot_info.token)
