import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import os

bot = commands.Bot(command_prefix="!")
BLOCKED_LINKS = ['discord.gg']
BLOCKED_MESSAGES_RACIST = ['nigga', 'nigger', 'jew', 'chink']
BLOCKED_MESSAGES_HOMOPHOBIC = ['faggot', 'gayboy', 'fagg0t']

async def messageRemoval(reason_title, reason_body, message, old_message=None):
    embed = discord.Embed(title=":zap: Hastebot", description="", color=0x206694)
    embed.add_field(name="{}, The message that you sent was detected as: {}".format(str(message.author.name), reason_title), value="{}".format(reason_body), inline=False)
    embed.set_footer(text="Powered By HasteBot | Version 0.1 | By Sargera")

    if old_message != None:
        embed.add_field(name="Original message (edited):", value="```{}```".format(old_message.content  ))
    
    embed_message = await bot.send_message(message.channel, embed=embed)
    await bot.delete_message(message)

    await asyncio.sleep(8)
    await bot.delete_message(embed_message)

@bot.event
async def on_ready():
    print("[CONSOLE] Running 'HasteBot' Version 0.1 (Author: Sargera)")
    await bot.change_presence(game=discord.Game(name="haste.minehug.gg", type=3))

@bot.event
async def on_member_join(member):
    totalMembers = 0
    for server in bot.servers:
        for member in server.members:
            totalMembers = totalMembers + 1
    
    for channel in member.server.channels:
        if channel.name == 'welcomes':
            await bot.send_message(channel, ':zap: {} has just joined the server, welcome them! **(Total Members: {})**'.format(member.mention, totalMembers))

@bot.event
async def on_message(message):
    if message.content.startswith('!join'):
        embed = discord.Embed(title=":zap: Hastebot", description="Haste is hosted by Minehut, meaning there are two ways to join us. These methods will be listed below, we hope to see you ingame.", color=0x206694)
        embed.add_field(name="Direct connect through the IP", value="```haste.minehut.gg```", inline=False)
        embed.add_field(name="Connect through the Minehut lobby", value="```/join Haste```", inline=False)
        embed.set_footer(text="Powered By HasteBot | Version 0.1 | By Sargera")
        await bot.send_message(message.channel, embed=embed)

    if message.content.startswith('!apply'):
        embed = discord.Embed(title=":zap: Hastebot", description="Thank you for registering your interest in applying for staff! Unfortunately, we do not allow traditional staff applications. Please read below", color=0x206694)
        embed.add_field(name="How is staff obtained?", value="```Staff will be hand picked when needed out of the most active, helpful and mature players that play Haste. The best thing you can do is stay patient and follow the server rules.```", inline=False)
        embed.add_field(name="Other requirements?", value="```Only that you have played the server for at least 2 weeks. But aside from this, nope. Only the above mentioned reasons will be considered when picking new staff! Stay friendly :heart:```", inline=False)
        embed.set_footer(text="Powered By HasteBot | Version 0.1 | By Sargera")
        await bot.send_message(message.channel, embed=embed)

    if message.content.startswith('!help'):
        embed = discord.Embed(title=":zap: Hastebot", description="Now, I know what you're thinking... Who made this amazing bot and what are the commands for it? (this command only answers one of those questions)", color=0x206694)
        embed.add_field(name="Command: `!join`", value="```View the methods of joining the Haste Server on Minehut. We hope to see you online!```", inline=False)
        embed.add_field(name="Command: `!help`", value="```This one is pretty obvious (you typed it to get this menu!) shows the help menu of commands```", inline=False)
        embed.add_field(name="Command: `!apply`", value="```Shows all the relevant information needed about becoming staff on Haste```", inline=False)
        embed.set_footer(text="Powered By HasteBot | Version 0.1 | By Sargera")
        await bot.send_message(message.channel, embed=embed)

    for element in BLOCKED_LINKS:
        if element in message.content:
            await messageRemoval("unauthorised link", "Please do not attempt to send links to other discords through our server. Any attempt to do so will result in removal of the message. Repeat offenders will receive the appropriate punishment.", message)

    for element in BLOCKED_MESSAGES_RACIST:
        if element in message.content:
            await messageRemoval("racist remark", "Our goal is to create a friendly environment on our server. As such, any messages which contain potential racism will be removed.", message)

    for element in BLOCKED_MESSAGES_HOMOPHOBIC:
        if element in message.content:
            await messageRemoval("homophobic comment", "Our goal is to create a friendly environment on our server. As such, any messages which contain potential homophobia will be removed.", message)

@bot.event
async def on_message_edit(old_message, new_message):

    for element in BLOCKED_LINKS:
        if element in new_message.content:
            await messageRemoval("unauthorised link", "Please do not attempt to send links to other discords through our server. Any attempt to do so will result in removal of the message. Repeat offenders will receive the appropriate punishment.", new_message, old_message)

    for element in BLOCKED_MESSAGES_RACIST:
        if element in new_message.content:
            await messageRemoval("racist remark", "Our goal is to create a friendly environment on our server. As such, any messages which contain potential racism will be removed.", new_message, old_message)

    for element in BLOCKED_MESSAGES_HOMOPHOBIC:
        if element in new_message.content:
            await messageRemoval("homophobic comment", "Our goal is to create a friendly environment on our server. As such, any messages which contain potential homophobia will be removed.", new_message, old_message)


bot.run('-- HIDDEN -- ')
    
