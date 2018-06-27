import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import os

DISABLED_CHANNELS = ['announcements', 'welcomes', 'community-polls', 'update-log', 'information']
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("[CONSOLE] Running 'HasteBot' Version 0.1 (Author: Sargera)")

@bot.event
async def on_member_join(member):
    totalMembers = 0
    for server in bot.servers:
        for member in server.members:
            totalMembers = totalMembers + 1
    
    for channel in member.server.channels:
        if channel.name == 'welcomes':
            await bot.send_message(channel, ':zap: {} has just joined the server, welcome them! **(Total Members: {})**'.format(member.mention, totalMembers))

bot.run('NDU2NTI2Nzk0NDQzNzE4NjY3.DgL1fQ.t43tAhwGZsRHv1AQFbe-aS6XFO0')
