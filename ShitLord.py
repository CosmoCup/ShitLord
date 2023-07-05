import asyncio
import discord
from gtts import gTTS
import random
from pydub import AudioSegment

client = discord.Client()

mp3FileName = "temp/text.mp3"

Boom = AudioSegment.from_mp3("temp/boom.mp3")

tokenf = open(".env", "r")
token = tokenf.read()

print("Init done")

@client.event
async def on_ready():
    print(client.user.name + " online")


@client.event
async def on_message(msg):
    author = msg.author
    if author == client.user:
        return

    if client.user.mentioned_in(msg):
        if '[ADD]' in msg.content:
            if msg.author.guild_permissions.administrator: 
                await add_roast(msg)
            else:
                message = str(msg.author.mention) + " : You worthless peasant, you need admin for that!"
                await msg.channel.send(message)
        else:
            await roast(msg)

async def add_roast(msg):
    text = str(msg.content)
    newInsult = text.split('[ADD]')[1]
    newInsult = newInsult.strip()
    if newInsult == "" :
        message = str(msg.author.mention) + " : New insult cannot be blank, dumb shit."
        await msg.channel.send(message)
    else:
        with open("temp/insults.txt","a") as insultFile:
            insultFile.write("\n"+newInsult)
        message = str(msg.author.mention) + " : New Insult Added! : '" + newInsult + "' "
        await msg.channel.send(message)
        print(msg.author.name + " added new insult : " +newInsult)

async def roast(msg):
    if (msg.author.voice == None):
        message = str(msg.author.mention) + " Join a voice channel, pussy lips..\n"+createInsult()
        await msg.channel.send(message)
        return
    
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
  first = random.choice(open("temp/first.txt","r").readlines())
  last = random.choice(open("temp/last.txt","r").readlines())
  word = first + " " + last
  return word

client.run(token)
