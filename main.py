# created by NullifiedVlad 2020.
import datetime
import os
from modules import siteParser
import discord
import qrcode
import random
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
import markovify
from modules import imageMaker


class Cat(commands.Bot):
    """
    bot: False - official bot , True - self bot
    """
    def __init__(self, command_prefix, token: str, user_bot: bool = False, **options):
        super().__init__(command_prefix, **options)
        self.remove_command('help')
        self.__token = token
        self.user_bot = user_bot

    @staticmethod
    def __sentence(file: str):
        """generate sentence form text modules"""
        with open(file, 'r') as f:
            text = f.read()

        out = None
        text_model = markovify.Text(text)
        while out is None:
            out = text_model.make_sentence()
        return out

    def start_bot(self):
        @self.event
        async def on_ready():
            print('READY!')
            await self.change_presence(activity=discord.Game(f'cathook.club'))

        @self.event
        async def on_message(message):
            await self.process_commands(message)

        @self.command(aliases=['help'])
        async def help_message(ctx):  # send help message
            embed = discord.Embed(title='**FEATURES**', description='Discord cathook self-bot.', color=0x0095ff, )
            # headers
            embed.add_field(name=f'**{self.command_prefix}help**', value='Send this message.')
            embed.add_field(name=f'**{self.command_prefix}cat**', value='Send random cat image.')
            embed.add_field(name=f'**{self.command_prefix}feature**', value='Random cathook feature.')
            embed.add_field(name=f'**{self.command_prefix}joke**', value='Send joke.')
            embed.add_field(name=f'**{self.command_prefix}steam**', value='Check steam profile.')
            embed.add_field(name=f'**{self.command_prefix}card**', value='Send your profile card.')
            embed.add_field(name=f'**{self.command_prefix}qr**', value='Make qrcode.')
            embed.add_field(name=f'**{self.command_prefix}online**', value='Show TF2 online stats.')
            embed.add_field(name=f'**{self.command_prefix}cathook**', value='Send cathook github repo.')
            embed.add_field(name=f'**{self.command_prefix}howgayami**', value='Show gayness percent.')
            embed.add_field(name=f'**{self.command_prefix}howfurryami**', value='Show furry percent.')
            embed.add_field(name=f'**{self.command_prefix}rage**', value='Generate a random killsay..')
            embed.set_thumbnail(url='https://i.imgur.com/WK520CI.jpg')
            embed.set_footer(text=f'Powered by NullifiedVlad',
                             icon_url='https://i.imgur.com/WK520CI.jpg')
            embed.set_author(name=self.user.name, icon_url='https://i.imgur.com/WK520CI.jpg')
            await ctx.send(embed=embed)

        @self.command()
        async def cat(ctx):
            image = requests.get('https://thiscatdoesnotexist.com/',
                                 headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                                                        'rv:75.0) Gecko/20100101 Firefox/75.0'})
            with open(f'{ctx.message.id}.jpg', 'wb') as f:
                f.write(image.content)
            await ctx.send(file=discord.File(f'{ctx.message.id}.jpg'))
            os.remove(f'{ctx.message.id}.jpg')

        @self.command()
        async def feature(ctx):
            await ctx.send(self.__sentence('text-models/features-model.txt'))

        @self.command()
        async def cathook(ctx):
            await ctx.send("https://github.com/nullworks/cathook")

        @self.command()
        async def joke(ctx):
            url = requests.get('https://jokes.lol/random-jokes/',
                               headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                                                      'rv:75.0) Gecko/20100101 Firefox/75.0'})
            soup = BeautifulSoup(url.text, 'html.parser')
            soup = soup.find('div', {'class': 'query-field query-field-post_content'})
            await ctx.send(soup.text[:-15])

        @self.command()
        async def steam(ctx, url_custom):
            account = siteParser.Steam(url_custom)

            embed = discord.Embed(title=f'**{account.getNick()}**', description=account.getGameStatus(), color=0x0095ff)
            embed.add_field(name='**Profile lvl**', value=account.getLvl())
            embed.add_field(name='**VAC**', value=account.getVacStatus())
            embed.add_field(name='**Comments**', value=account.getTotalComments())
            embed.add_field(name='**Friends**', value=account.getTotalFriends())
            embed.add_field(name='**Games**', value=account.getTotalGames())
            embed.add_field(name='**Bages**', value=account.getTotalBages())
            embed.add_field(name='**Screenshots**', value=account.getTotalScreenshots())
            embed.set_thumbnail(url=account.getProfilePicture())
            embed.set_author(name='Steam profile checker.', icon_url='https://i.imgur.com/WK520CI.jpg')
            embed.set_footer(text=url_custom,
                             icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg'
                                      '/512px'
                                      '-Steam_icon_logo.svg.png')
            try:
                await ctx.message.delete()
            except discord.errors.Forbidden:
                pass

            await ctx.send(embed=embed)

        @self.command()
        async def card(ctx):
            user = imageMaker.Card('media/fonts/sans.ttf',
                                   ctx.message.author,
                                   ctx.message.guild,
                                   'media/card/steam_background.jpg')
            user.build()
            await ctx.send(file=discord.File('card.jpg'))

            user.cleanfiles()
            del user

        @self.command()
        async def rename(ctx, *, name):
            if ctx.message.author.id == 566653752451399700:
                try:
                    await self.user.edit(username=name)
                    await ctx.send(f'Nickname was changed on {name} ')
                except discord.errors.HTTPException as e:
                    await ctx.send(e)
            else:
                await ctx.send('Access denied!')

        @self.command()
        async def qr(ctx, *, text):
            if int(len(text)) <= 100:
                image = qrcode.make(text)
                image.save('code.png')

                await ctx.send(file=discord.File('code.png'))
                os.remove('code.png')
            else:
                await ctx.send('You cant create qrcode with 100 symbols or more!')

        @self.command()
        async def howgayami(ctx):
            await ctx.send(f'Look! {ctx.message.author} is {random.randint(0, 100)}% gay!')

        @self.command()
        async def howfurryami(ctx):
            if ctx.message.author.id == 566653752451399700:
                await ctx.send(content=f'{ctx.message.author} is **100%** furry!')
            elif ctx.message.author.id == 782347202437709866:
                await ctx.send(content=f'{ctx.message.author} is **0%** furry!')
            else:
                await ctx.send(content=f'{ctx.message.author} is **{random.randint(0, 100)}%** furry!')

        @self.command(aliases=['killsays', 'rage'])
        async def kill_say(ctx):
            await ctx.send(self.__sentence('text-models/killsays-model.txt'))

        @self.command(aliases=['stats', 'tf2', 'online'])
        async def tf2stats(ctx):

            img = imageMaker.Stats('media/fonts/tf2build.ttf', (255, 255, 255), ctx.author)

            img.build()
            await ctx.send(file=discord.File(f'{ctx.author.id}.png'))
            img.cleanfiles()

        self.run(self.__token, bot=self.user_bot)


if __name__ == '__main__':
    Cat('cat_', os.environ.get('TOKEN'), False).start_bot()
