import discord
from discord.utils import get
from discord.ext import commands
from datetime import datetime, timedelta
from songs import songAPI

import os
from dotenv import load_dotenv #Hide token
load_dotenv()
token = os.getenv('TOKEN')

songsInstance = songAPI()
bot = commands.Bot(command_prefix='!',help_command=None)
message_lastseen = datetime.now()
rqmChannel = "🎵-request-music"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command() 
async def help(ctx):
    emBed = discord.Embed(title="E11 Bot help", description="All available bot commands", color=0x42f5a7)
    emBed.add_field(name="!help", value="Get help command", inline=False)
    emBed.add_field(name="command", value="Play music : !play or !p\nPause music : !pause\nResume playing : !resume\nStop playing : !stop\nBot leave channel : !leave\nShow queue : !queue or !q\nSkip playing : !skip ", inline=False)
    await ctx.channel.send(embed=emBed)
    
@bot.event #async/await
async def on_message(message):
    global message_lastseen
    mes = message.content.lower()
    if mes == 'hi' and datetime.now() >= message_lastseen:
        message_lastseen = datetime.now() + timedelta(seconds=5)
        await message.channel.send('Hello ' + str(message.author.name))
    elif mes == 'stream' or  mes == 'live':
        await message.channel.send('E11 Streaming on Facebook gaming https://www.facebook.com/gaming/E11Streaming\nHighlight and Re-broadcast on YouTube E11 Streaming https://www.youtube.com/channel/UCk_jFRCQyjYPmJKhn9jwpKQ')
    elif message.content == '!logout':
        await bot.logout()
    await bot.process_commands(message)

@bot.command() 
async def play(ctx,* ,search: str):
    result = await checkRQM(ctx)
    if result:
        await songsInstance.play(ctx, search)

@bot.command() 
async def p(ctx,* ,search: str):
    result = await checkRQM(ctx)
    if result:
        await songsInstance.play(ctx, search)

@bot.command()
async def pause(ctx):
    result = await checkRQM(ctx)
    if result:
        await songsInstance.pause(ctx)

@bot.command()
async def resume(ctx):
    result = await checkRQM(ctx)
    if result:
        await songsInstance.resume(ctx)

@bot.command()
async def stop(ctx):
    result = await checkRQM(ctx)
    if result:
        await songsInstance.stop(ctx)

@bot.command()
async def leave(ctx):
    await songsInstance.leave(ctx)

@bot.command()
async def queue(ctx):
    result = await checkRQM(ctx)
    if result:
        await songsInstance.queueList(ctx)

@bot.command()
async def q(ctx):
    result = await checkRQM(ctx)
    if result:
        await songsInstance.queueList(ctx)

@bot.command()
async def skip(ctx):
    result = await checkRQM(ctx)
    if result:
        await songsInstance.skip(ctx)
    
async def checkRQM(ctx):
    print(f"${str(ctx.channel)}  ${rqmChannel}")
    if str(ctx.channel) != rqmChannel:
        await ctx.channel.send("This channel can't request songs, please type in request-music.")
        return False
    else :
        return True

bot.run(token)