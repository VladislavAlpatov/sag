import random2
import discord
from discord.ext import commands
import os
import config
from bs4 import BeautifulSoup
import requests
from PIL import Image
from PIL import ImageDraw, ImageFont

bot = commands.Bot(command_prefix='/')  # префикс для комманд
bot.remove_command('help')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(config.Bot_info.game))


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    author = message.author
    msg = message.content
    if str(author) == 'cat-bot#4210' or message.guild.id == 665856387439656972:
        pass
    else:
        channel = bot.get_channel(config.Nullserver.id)
        await channel.send(f'<{message.guild.name}>  <{message.channel.name}> **{author}** :{msg} ')


@bot.command()
async def help(ctx):
    await ctx.send(config.Messages.help_message, file=discord.File('cathook-banner.png'))


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
    url = requests.get('https://www.ajokeaday.com/jokes/random', headers=config.Bot_info.heads)
    soup = BeautifulSoup(url.text, 'html.parser')
    soup = soup.find('div', {'class': 'jd-body jubilat'})
    await ctx.send(soup.text)


@bot.command()
async def steam(ctx, url):

    heads = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0'}
    r = requests.get(url, headers=heads)
    soup = BeautifulSoup(r.text, 'html.parser')
    # получаем ник и уровень
    nick = soup.findAll('span', {'class': 'actual_persona_name'})
    lvl = soup.findAll('span', {'class': 'friendPlayerLevelNum'})
    # получаем статус и вак статус
    status = soup.findAll('div', {'class': 'profile_in_game_header'})
    vac_status = soup.find('div', {'class': 'profile_ban_status'})
    # получаем коллтчество коментариев
    comments_block = soup.find('a', {'class': 'commentthread_allcommentslink'})
    com_count = comments_block.find('span')

    # проверка вак бана
    if bool(vac_status):
        vac_status = 'VAC ban on record!'
    else:
        vac_status = 'No VAC on record!'
    # отправка сообщения
    await ctx.send(f'''
**Nickname: **{nick[0].text}
**VAC: **{vac_status}
**Level: **{lvl[0].text}
**Status: **{status[0].text}
**Comments: **{com_count.text}
''')


@bot.command()
async def img(ctx, *, text):
    x = len(text) * 6
    color = (255, 0, 229)
    image = Image.new('RGB', (x + 10, 50), color)
    draw_on_image = ImageDraw.Draw(image)
    draw_on_image.text((10, 20), str(text),)
    image.save('img.jpg')

    await ctx.send(file=discord.File('img.jpg'))
    os.remove('img.jpg')


@bot.command()
async def card(ctx):
    font_name = "bit.ttf"
    # получаем инфу
    author = ctx.message.author
    guild = ctx.message.guild.name
    avatar = str(ctx.author.avatar_url)

    # парсим и сохраняем аву
    image = requests.get(avatar, headers=config.Bot_info.heads)
    with open('ava.webp', 'wb') as f:
        f.write(image.content)

    # задаём цвет фона
    color = (84, 84, 84)

    # создаём изображение
    image = Image.new('RGB', (1500, 410), color)
    draw = ImageDraw.Draw(image)

    # получаем аватар и подгоняем размер
    avatar = Image.open('ava.webp')
    avatar = avatar.convert('RGB')
    avatar = avatar.resize((421, 421), Image.ANTIALIAS)

    # Ник
    font = ImageFont.truetype(font_name, 90, encoding="unic")
    draw.text((460, 0), str(author.name), fill=(3, 150, 255), font=font)
    # тег
    font = ImageFont.truetype(font_name, 50, encoding="unic")
    draw.text((460, 90), 'TAG: #' + str(author.discriminator), fill=(51, 255, 0), font=font)
    # id
    font = ImageFont.truetype(font_name, 50, encoding="unic")
    draw.text((460, 180), 'ID: ' + str(author.id), font=font)
    # сервер
    font = ImageFont.truetype(font_name, 50, encoding="unic")
    draw.text((460, 270), 'SERVER: ' + str(guild), fill=(0, 238, 255), font=font)
    # вотер марка
    font = ImageFont.truetype(font_name, 30, encoding="unic")
    draw.text((1300, 350), 'Nullserver', fill=(0, 238, 255), font=font)

    # проверка на создателя
    if author.id == 566653752451399700:
        font = ImageFont.truetype(font_name, 50, encoding="unic")
        draw.text((460, 360), 'Creator of this bot', font=font, fill=(255, 0, 229))
    else:
        pass

    # вставляем фото
    image.paste(avatar, (0, 0))
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

    if int(len(text)) >= 8:
        large = 60
        print('ok')
    else:
        large = 90

    if int(len(text)) >= 4:
        to_sum = 8
    else:
        to_sum = 3

    image = Image.open('nigga.jpg')
    draw = ImageDraw.Draw(image)
    font_name = 'bit.ttf'
    font = ImageFont.truetype(font_name, large, encoding="unic")
    draw.text((200-int(len(text)) * to_sum, 600-large), str(text), fill=(0, 0, 0), font=font)
    image.save('nigga-out.jpg')
    await ctx.send(file=discord.File('nigga-out.jpg'))
    os.remove('nigga-out.jpg')

bot.run(config.Bot_info.token)
