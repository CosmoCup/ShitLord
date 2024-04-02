import os
import asyncio
import discord
from gtts import gTTS
import random
from pydub import AudioSegment
from dotenv import load_dotenv

load_dotenv()
client = discord.Client(intents=discord.Intents.default())
mp3FileName = "temp/text.mp3"
Boom = AudioSegment.from_mp3("temp/boom.mp3")
token = os.getenv('TOKEN')

@client.event
async def on_ready():
    print("Shit Lord is on the hunt.")

@client.event
async def on_message(msg):
    author = msg.author
    if author == client.user: return
    if client.user.mentioned_in(msg):
            await roast(msg)

async def roast(msg):
    if (msg.author.voice == None):
        message = str(msg.author.mention) + " Join a voice channel, pussy lips.."
        await msg.channel.send(message)
        return
    
    await msg.delete()
    channel = msg.author.voice.channel

    text = createInsult()
    count = 1
    while count < 4 :
        if count == 1 :
            word = gTTS(msg.author.name + ", you, " + createWord())
        else :
            word = gTTS(createWord())
        word.save("temp/"+ str(count) + ".mp3")
        count+=1
    speech = gTTS(text)
    speech.save(mp3FileName)
    
    trimTimeMills = 350

    One = AudioSegment.from_mp3("temp/1.mp3")
    One = One[:(One.duration_seconds*1000) - trimTimeMills]
    Two = AudioSegment.from_mp3("temp/2.mp3")
    Two = Two[:(Two.duration_seconds*1000) - trimTimeMills]
    Three = AudioSegment.from_mp3("temp/3.mp3")
    Three = Three[:(Three.duration_seconds*1000) - trimTimeMills]
    Insult = AudioSegment.from_mp3("temp/text.mp3")
    Insult = Insult[:(Insult.duration_seconds*1000) - trimTimeMills]
    Earrape = AudioSegment.from_mp3("temp/earrape.mp3")
    
    FullAudio = One + Boom + Two + Boom + Three + Boom + Insult + Earrape
    FullAudio.export("temp/"+ "full.mp3", format="mp3")

    connection = await channel.connect()
  
    connection.play(discord.FFmpegPCMAudio("temp/full.mp3"))
    while connection.is_playing():
        await asyncio.sleep(0.1)
    connection.stop()
    await connection.disconnect()

def createInsult():
  return random.choice(open("temp/insults.txt","r").readlines()).lower()

def createWord():
  first = random.choice(open("temp/first.txt","r").readlines()).lower()
  last = random.choice(open("temp/last.txt","r").readlines()).lower()
  word = first + " " + last
  return word

client.run(token)