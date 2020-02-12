import sys
import discord
import requests
import json
import os
import opuslib
import subprocess
import time
import audioread
import random


class MyClient(discord.Client):

	def __init__(self):
		super().__init__()
		self.voice = None
	
	def voice_disconnect(error, self):
		print(error)
		print(self)
		time.sleep(2)
		self.voice.disconnect()
	
	async def on_ready(self):
		print("Logged on as {0}!".format(self.user))
	
	async def on_message(self, message):
		print("Message from {0.author}: {0.content}".format(message))
		if message.author == client.user:
			return
		
		#test the bot
		if message.content.startswith("!ping"):
			await message.channel.send('pong!')
		
		#list all commands
		if message.content.startswith("!commands"):
			await message.channel.send("not implemented yet, sorry")
		
		#prank delete the server
		if message.content.startswith("!deleteserver"):
			await message.channel.send(":warning: SELF DESTRUCT SEQUENCE INITIATED. 1 MINUTE UNTIL SERVER DELETE :warning:", tts=True)
		
		#pay respects to the user above
		if message.content.startswith("!rip") or message.content.startswith("!f"):
			await message.channel.send("press **F** to pay respects. RIP.", tts=True)
		
		#oof
		if message.content.startswith("!oof"):
			await message.channel.send(file=discord.File("oof.wav"))
		
		#lenny
		if message.content.startswith("!lenny"):
			await message.channel.send(file=discord.File("lenny.png"))
		
		#ayylmao
		if message.content.startswith("!ayy"):
			await message.channel.send(file=discord.File("ayylmao.gif"))
		
		#8ball / magic conch
		if message.content.startswith("!8ball") or message.content.startswith("!conch"):
			await message.channel.send(random.choice(list(open("8ball.txt"))))
		
		#insult
		if message.content.startswith("!insult"):
			string = message.content.split("@")[1].split(" ")[0]
			await message.channel.send("{0} {1}".format("<@"+string, random.choice(list(open("insults.txt")))))
			#TODO: when user insults bot say "no u".
		
		#reddit link (r/)
		if "r/" in message.content:
			string = message.content.split("/r/")[1].split("/")[0]
			await message.channel.send("Subreddit mentioned in the previous message: https://reddit.com/r/{0}".format(string))
		
		#NHL JSON test
		if message.content.startswith("!jets"):
			uri = "https://statsapi.web.nhl.com/api/v1/teams/52?expand=team.schedule.next"
			r = requests.get(url = uri)
			dict = r.json()
			game = dict["teams"][0]["nextGameSchedule"]["dates"][0]["games"][0]
			await message.channel.send("Game date/time: {0}\n{1}: {2},\n{3}: {4}".format(game["gameDate"], game["teams"]["away"]["team"]["name"], game["teams"]["away"]["score"],
																										game["teams"]["home"]["team"]["name"], game["teams"]["home"]["score"]))
		
		#play youtube audio in current voice channel
		if message.content.startswith("!play"):
			if os.path.exists("audio.mp3"):
				print("audio.mp3 already exists! removing...")
				os.remove("audio.mp3")
			print(self.voice)
			#if self.voice.is_connected()
				#self.voice.disconnect()
			string = message.content.split()[1]
			discord.opus.load_opus("libopus.so.0")
			subprocess.run(["youtube-dl", "-o", "audio.mp3", "-f", "251", string])
			self.voice = await discord.VoiceChannel.connect(message.author.voice.channel)
			source = await discord.FFmpegOpusAudio.from_probe("audio.mp3")
			self.voice.play(source)
			time.sleep(audioread.audio_open("audio.mp3").duration + 2)
			await self.voice.disconnect()
		

if len(sys.argv) == 2:
	client = MyClient()
	client.run(str(sys.argv[1]))
else:
	print("you must provide a token as the first argument!")
