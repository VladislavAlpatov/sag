import random2
import discord
from discord.ext import commands
import os
import config
from bs4 import BeautifulSoup
import requests

bot = commands.Bot(command_prefix='/')  # префикс для комманд
bot.remove_command('help')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(config.Bot_info.game))


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
    vac_status = soup.find('div', {'class': 'profile_ban_status'})
    # получаем коллтчество коментариев
    comments_block = soup.find('a', {'class': 'commentthread_allcommentslink'})
    com_count = comments_block.find('span')

    # проверка вак бана
    if bool(vac_status):
        vac_status = 'VAC ban on record!'
    else:
        vac_status = 'No VAC ban'
    # отправка сообщения
    await ctx.send(f'''
**Nickname: **{nick[0].text}
**VAC: **{vac_status}
**Level: **{lvl[0].text}
**Comments: **{com_count.text}
''')

bot.run(config.Bot_info.token)
