import discord
from discord.ext import commands
from discord.utils import find
import random
import sys
import requests
import json
import os
import subprocess
import time

description = '''CheatCoder#6969's bot.

ALL HAIL THE MAGIC CONCH!'''
bot = commands.Bot(command_prefix='!', description=description)
activity = discord.CustomActivity('Watching you.')
slots_file = 'slots_players.json'

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    print('SLOTS SCORES')
    print('------')
    with open('slots_players.json') as json_file:
        data = json.load(json_file)
        for p in data['people']:
            print("alias: '" + p['name'] + "' has " + str(p['coins']) + ' coins.')
            

@bot.command()
async def ping(ctx):
    '''test the bot'''
    await ctx.send('pong!')

@bot.command()
async def deleteserver(ctx):
    '''delete the server'''
    await ctx.send(':warning: SELF DESTRUCT SEQUENCE INITIATED. 1 MINUTE UNTIL SERVER DELETE :warning:')

@bot.command()
async def rip(ctx):
    '''pay respects to the user above'''
    await ctx.send('Press **F** to pay respects. RIP.')

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
async def insult(ctx, user: discord.User):
    '''insult a user'''
    if user.id != '458779902649303040':
        await ctx.send('{0} {1}'.format(user.mention, random.choice(list(open('insults.txt')))))
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
    '''rolls a dice in NdN format.'''
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
async def mock(ctx):
    '''mocks a user with alternating caps'''
    message_history = ctx.channel.history()
    last_message = None
    message = ctx.message.content.strip()[6:len(ctx.message.content)] # 6 because '!mock ' has 6 chars
    if message.startswith('<@'):
        if message.startswith('<@!') or message.startswith('<@&'):
            last_message = await find(lambda m: m.author.id == message[message.index('<@')+3:message.index('>')], ctx.channel.history().flatten())
        else:
            last_message = await find(lambda m: m.author.id == message[message.index('<@')+2:message.index('>')], ctx.channel.history().flatten())
    elif len(message) > 0:
        last_message = message
    else:
        last_message = await ctx.channel.history().get().content
    
    res = [ele.upper() if not idx % 2 else ele.lower() for idx, ele in enumerate(last_message)]
    res = "".join(res)
    await ctx.send(res)

@bot.command()
async def avatar(ctx, user: discord.User):
    '''displays a user's avatar'''
    await ctx.send(user.avatar_url)

@bot.command()
async def balance(ctx):
    '''lets a player get their coins balance'''
    player = find_player(ctx, slots_file)
    await ctx.send('<@{0}>, you have {1} coins.'.format(player['id'], player['coins']))

@bot.command()
async def slots(ctx, bet: int):
    '''plays a slot machine game with a bet'''
    if bet <= 0 or bet == None:
        await ctx.send('invalid bet!')
        return
    
    # constants:
    ITEMS = ["CHERRY", "LEMON", "ORANGE", "PLUM", "BELL", "BAR", "7"]
    # vars:
    player = find_player(ctx, slots_file)
    winnings = None
    first_wheel = ITEMS[random.randint(0, 6)]
    second_wheel = ITEMS[random.randint(0, 6)]
    third_wheel = ITEMS[random.randint(0, 6)]
    
    #determine winnings
    if((first_wheel == "CHERRY") and (second_wheel != "CHERRY")): # win 2x bet
        winnings = bet*2
    elif((first_wheel == "CHERRY") and (second_wheel == "CHERRY") and (third_wheel != "CHERRY")): # win 5x bet
        winnings = bet*5
    elif((first_wheel == "CHERRY") and (second_wheel == "CHERRY") and (third_wheel == "CHERRY")): # win 7x bet
        winnings = bet*7
    elif((first_wheel == "ORANGE") and (second_wheel == "ORANGE") and ((third_wheel == "ORANGE") or (third_wheel == "BAR"))): # win 10x bet
        winnings = bet*10
    elif((first_wheel == "PLUM") and (second_wheel == "PLUM") and ((third_wheel == "PLUM") or (third_wheel == "BAR"))): # win 20x bet
        winnings = bet*20
    elif((first_wheel == "BELL") and (second_wheel == "BELL") and ((third_wheel == "BELL") or (third_wheel == "BAR"))): # win 50x bet
        winnings = bet*50
    elif((first_wheel == "BAR") and (second_wheel == "BAR") and (third_wheel == "BAR")): # win 100x bet
        winnings = bet*100
    elif((first_wheel == "7") and (second_wheel == "7") and (third_wheel == "7")): # win jackpot!
        winnings = jackpot_win(slots_file)
    else:
        winnings = 0-bet
        new_jackpot = jackpot_up(bet, slots_file)
        
    if winnings > 0:
        answer = "The slot spun:\n{0} | {1} | {2}\n\nYou won ${3}!".format(first_wheel, second_wheel, third_wheel, winnings)
    if winnings < 0:
        answer = "The slot spun:\n{0} | {1} | {2}\n\nYou lost your bet of ${3}.\nJackpot is now ${4}".format(first_wheel, second_wheel, third_wheel, abs(winnings), new_jackpot)
    await ctx.send(answer)
    balance_change(ctx, winnings, slots_file)
        
def jackpot_up(bet: int, file_str: str):
    with open(file_str) as json_file: # open the data file
        data = json.load(json_file) # import data
        data['jackpot'] += bet
        jackpot = data['jackpot']
        with open(file_str, 'w') as outfile:
            json.dump(data, outfile)
        return jackpot

def balance_change(ctx, winnings: int, file_str: str):
   with open(file_str) as json_file: # open the data file
        data = json.load(json_file) # import data
        # find the correct player
        player = None
        for p in data['people']:
            if p['id'] == ctx.message.author.id:
                player = p
        player['coins'] += winnings
        if player['coins'] < 100:
            player['coins'] = 100
        with open(file_str, 'w') as outfile:
            json.dump(data, outfile)
        
def jackpot_win(file_str: str):
    with open(file_str) as json_file: # open the data file
        data = json.load(json_file) # import data
        winnings = data['jackpot']
        data['jackpot'] = 5000
        with open(file_str, 'w') as outfile:
            json.dump(data, outfile)
        return winnings

def find_player(ctx, file_str: str):
    with open(file_str) as json_file: # open the data file
        data = json.load(json_file) # import data
        # find the correct player
        player = None
        for p in data['people']:
            if p['id'] == ctx.message.author.id:
                player = p
        # if the player does not exist, create one and write
        if player == None:
            data['people'].append({
            'id': ctx.message.author.id,
            'name': ctx.message.author.display_name,
            'coins': 1000
            })
            with open(file_str, 'w') as outfile:
                json.dump(data, outfile)
            return find_player(ctx, file_str)
        else:
            return player

@bot.listen()
async def on_message(message):
    print('Message from {0.author}: {0.content}'.format(message))
    if message.author == bot.user:
        return
    
    if 'r/' in message.content:
        string = message.content.split('/r/')[1].split('/')[0].split('\s')[0]
        await message.channel.send('Subreddit mentioned in the previous message: https://reddit.com/r/{0}'.format(string))


if len(sys.argv) == 2:
    bot.run(str(sys.argv[1]))
else:
    print('you must provide a token as the first argument!')
