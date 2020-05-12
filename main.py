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

bot.run(config.Bot_info.token)
