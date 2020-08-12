import discord
from discord.ext import commands
import random
import sys
import requests
import json
import os
import opuslib
import subprocess
import time
import audioread

description = '''CheatCoder#6969's bot.

ALL HAIL THE MAGIC CONCH!'''
bot = commands.Bot(command_prefix='!', description=description)
activity = discord.CustomActivity('Watching you.')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def ping(ctx):
    '''test the bot'''
    await ctx.send('pong!')

@bot.command()
async def deleteserver(ctx):
    '''delete the server'''
    await ctx.send(':warning: SELF DESTRUCT SEQUENCE INITIATED. 1 MINUTE UNTIL SERVER DELETE :warning:', tts=True)

@bot.command()
async def rip(ctx):
    '''pay respects to the user above'''
    await ctx.send('Press **F** to pay respects. RIP.', tts=True)

@bot.command()
async def oof(ctx):
    '''oof'''
    await ctx.send(file=discord.File('oof.wav'))

@bot.command()
async def lenny(ctx):
    '''( ͡° ͜ʖ ͡°)'''
    await ctx.send(file=discord.File('lenny.png'))

@bot.command()
async def ayylmao(ctx):
    '''ayy lmao'''
    await ctx.send(file=discord.File('ayylmao.gif'))

@bot.command()
async def conch(ctx):
    '''consult the magic conch!'''
    message = random.choice(list(open('8ball.txt')))
    await ctx.send(message, tts=True)

@bot.command()
async def insult(ctx, user: str):
    '''insult a user'''
    if user != '<@!458779902649303040>':
        await ctx.send('{0} {1}'.format(user, random.choice(list(open('insults.txt')))))
    else:
        await ctx.send('no u')

@bot.command()
async def awkward(ctx):
    '''awkward'''
    await ctx.send('https://www.youtube.com/watch?v=qzPvx8VUSDw&t=11')

@bot.command()
async def jets(ctx):
    '''show the next winnipeg jets game'''
    uri = 'https://statsapi.web.nhl.com/api/v1/teams/52?expand=team.schedule.next'
    r = requests.get(url = uri)
    dict = r.json()
    game = dict['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]
    await ctx.send('Game date/time: {0}\n{1}: {2},\n{3}: {4}'.format(game['gameDate'], game['teams']['away']['team']['name'], game['teams']['away']['score'], game['teams']['home']['team']['name'], game['teams']['home']['score']))

@bot.command()
async def urban(ctx, search: str):
    '''get a definition from urban dictionary'''
    uri = 'https://api.urbandictionary.com/v0/define?term={0}'.format(search)
    r = requests.get(url = uri)
    dict = r.json()
    definition = dict['list'][0]['definition']
    permalink = dict['list'][0]['permalink']
    written_on = str(dict['list'][0]['written_on']).split('T')[0]
    embed = discord.Embed(title=str(search), url=str(permalink), description='**{0}**'.format(definition), color=0x00ff00)
    embed.set_author(name='Urban Dictionary Definitions', icon_url='https://lh3.googleusercontent.com/unQjigibyJQvru9rcCOX7UCqyByuf5-h_tLpA-9fYH93uqrRAnZ0J2IummiejMMhi5Ch=s180')
    embed.set_footer(text='Written on {0}'.format(str(written_on)))
    await ctx.send(embed=embed)

@bot.command()
async def roll(ctx, dice: str):
    '''Rolls a dice in NdN format.'''
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.listen()
async def on_message(message):
    print('Message from {0.author}: {0.content}'.format(message))
    if message.author == bot.user:
        return
    
    if 'r/' in message.content:
        string = message.content.split('/r/')[1].split('/')[0]
        await message.channel.send('Subreddit mentioned in the previous message: https://reddit.com/r/{0}'.format(string))


if len(sys.argv) == 2:
    bot.run(str(sys.argv[1]))
else:
    print('you must provide a token as the first argument!')
