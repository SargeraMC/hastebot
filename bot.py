import discord
import asyncio
import requests
from discord.ext.commands import Bot
from discord.ext import commands
import os
from mcstatus import MinecraftServer

bot = commands.Bot(command_prefix="!")
BLOCKED_LINKS = ['discord.gg']
bot.remove_command('help')
BLOCKED_MESSAGES_RACIST = ['nigga', 'nigger', 'jew', 'chink']
BLOCKED_MESSAGES_HOMOPHOBIC = ['faggot', 'gayboy', 'fagg0t']
BOT_CHANNEL = "bot-palace"

@bot.event
async def on_ready():
    print("[CONSOLE] Running 'HasteBot' Version 1.1 (Author: Sargera)")
    await bot.change_presence(game=discord.Game(name="haste.minehug.gg", type=3))

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

@bot.command(pass_context = True)
async def ping(ctx, server_query=None):
    if ".minehut.gg" in server_query:
        server_ping = MinecraftServer.lookup(server_query)
        server_name = server_query.split(".", 1)
        server_address = server_query
    else:
        server_name = server_query
        server_address = server_query + ".minehut.gg"
        server_ping = MinecraftServer.lookup(server_address)
        
    get_status = server_ping.status()
    print(get_status)
    embed = discord.Embed(title=":zap: Hastebot Minehut Server Ping", description="This command allows you to ping the status of any minehut server, using either its direct IP address or simply the name of the server. Returns all kind of useful data to you!", color=0x206694)
    embed.add_field(name="Server Name", value="```{}```".format(server_query))
    embed.add_field(name="Direct Server Connect", value="```{}```".format(server_address))
    embed.add_field(name="Players", value="```{}/{}```".format(get_status.players.online, get_status.players.max), inline=False)
    embed.add_field(name="Server Motd", value="```{}{}```".format(get_status.description['extra'][0]['text'], get_status.description['extra'][1]['text']), inline=False)
    embed.set_footer(text="Powered By HasteBot | Version 0.1 | By Sargera")
    await bot.send_message(ctx.message.channel, "Pong! Here you go, {}".format(ctx.message.author.mention))
    await bot.send_message(ctx.message.channel, embed=embed)

@bot.command(pass_context = True)
async def topservers(ctx, number=None):
    response = requests.get('https://pocket.minehut.com/network/top_servers')
    top_servers = response.json()
    loop_number = 0

    server_list = []
    
    if number == None:
        loop_number = 1
        for server in top_servers['servers']:
            server_name = server['name']
            server_name = server_name
            server_list.append("[{}]: {}".format(loop_number, server_name))
            loop_number = loop_number + 1

        server_list = ("\n".join(server_list))
            
        embed = discord.Embed(title=":zap: Hastebot Minehut Server Ping", description="This command was developed using minehut's top server API. It allows the top servers to be checked using reactions.", color=0x206694)
        embed.set_footer(text="Powered By HasteBot | Version 0.1 | By Sargera")
        embed.add_field(name="Select from the list of current top servers", value="```{}```".format(server_list))
        embed_message = await bot.send_message(ctx.message.channel, embed=embed)
        await bot.add_reaction(embed_message, emoji="\U0001f4c4")
        await bot.add_reaction(embed_message, emoji="\U0000274c")
        await bot.add_reaction(embed_message, emoji="1\u20e3")
        await bot.add_reaction(embed_message, emoji="2\u20e3")
        await bot.add_reaction(embed_message, emoji="3\u20e3")
        await bot.add_reaction(embed_message, emoji="4\u20e3")
        await bot.add_reaction(embed_message, emoji="5\u20e3")

        while True:
            close = await bot.wait_for_reaction(['\U0001f4c4', '\U0000274c', '1\u20e3', '2\u20e3', '3\u20e3', '4\u20e3','5\u20e3'], message=embed_message, user=ctx.message.author)
            
            if close[0].emoji == "\U0000274c":
                await bot.delete_message(embed_message)
                await bot.delete_message(ctx.message)
                break

            if close[0].emoji == "\U0001f4c4":
                 await bot.edit_message(embed_message, embed=embed)

            else:
                index = int(close[0].emoji[0]) - 1
                server_name = top_servers['servers'][index]['name']
                player_count = top_servers['servers'][index]['playerCount']
                max_count = top_servers['servers'][index]['maxPlayers']
                status = top_servers['servers'][index]['status']
                motd = top_servers['servers'][index]['motd']
                online_players = top_servers['servers'][index]['players']
                online_players = "\n".join(map(str, online_players)).replace("None", "(Error obtaining player)")

                server_one_embed = discord.Embed(title=":zap: Hastebot Minehut Server Ping", description="This command was developed using minehut's top server data. It allows the top servers to be checked using reactions.", color=0x206694)
                server_one_embed.set_footer(text="Powered By HasteBot | Version 0.1 | By Sargera")
                server_one_embed.add_field(name="Server Name", value="```[{}]: {}```".format(index, server_name))
                server_one_embed.add_field(name="Direct Connect", value="```{}.minehut.gg```".format(server_name))
                server_one_embed.add_field(name="Server MOTD", value="```{}```".format(motd), inline=False)
                server_one_embed.add_field(name="Server Slots", value="```{}/{}```".format(player_count, max_count), inline=False)
                server_one_embed.add_field(name="Server Status", value="```{}```".format(status), inline=False)
                server_one_embed.add_field(name="Online Players", value="```{}```".format(online_players), inline=False)
                await bot.edit_message(embed_message, embed=server_one_embed)

            await bot.remove_reaction(embed_message, close[0].emoji, ctx.message.author)


@bot.command(pass_context = True)
async def join(ctx):
    embed = discord.Embed(title=":zap: Hastebot", description="Haste is hosted by Minehut, meaning there are two ways to join us. These methods will be listed below, we hope to see you ingame.", color=0x206694)
    embed.add_field(name="Direct connect through the IP", value="```haste.minehut.gg```", inline=False)
    embed.add_field(name="Connect through the Minehut lobby", value="```/join Haste```", inline=False)
    embed.set_footer(text="Powered By HasteBot | Version 0.1 | By Sargera")
    await bot.send_message(ctx.message.channel, embed=embed)

@bot.command(pass_context=True)
async def apply(ctx):
    embed = discord.Embed(title=":zap: Hastebot", description="Thank you for registering your interest in applying for staff! Unfortunately, we do not allow traditional staff applications. Please read below", color=0x206694)
    embed.add_field(name="How is staff obtained?", value="```Staff will be hand picked when needed out of the most active, helpful and mature players that play Haste. The best thing you can do is stay patient and follow the server rules.```", inline=False)
    embed.add_field(name="Other requirements?", value="```Only that you have played the server for at least 2 weeks. But aside from this, nope. Only the above mentioned reasons will be considered when picking new staff! Stay friendly :heart:```", inline=False)
    embed.set_footer(text="Powered By HasteBot | Version 0.1 | By Sargera")
    await bot.send_message(ctx.message.channel, embed=embed)

@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(title=":zap: Hastebot", description="Now, I know what you're thinking... Who made this amazing bot and what are the commands for it? (this command only answers one of those questions)", color=0x206694)
    embed.add_field(name="Command: `!join`", value="```View the methods of joining the Haste Server on Minehut. We hope to see you online!```", inline=False)
    embed.add_field(name="Command: `!help`", value="```This one is pretty obvious (you typed it to get this menu!) shows the help menu of commands```", inline=False)
    embed.add_field(name="Command: `!apply`", value="```Shows all the relevant information needed about becoming staff on Haste```", inline=False)
    embed.set_footer(text="Powered By HasteBot | Version 0.1 | By Sargera")
    await bot.send_message(ctx.message.channel, embed=embed)

@bot.command(pass_context=True)
async def purge(ctx, number):
    await bot.delete_message(ctx.message)
    await bot.purge_from(ctx.message.channel, limit=int(number))
    embed = discord.Embed(title=":zap: Hastebot", description="The purge command is used for removing messages from a channel, up to 100 at a time. Use it with !purge", color=0x206694)
    embed.add_field(name="Results:".format(ctx.message.channel), value="```Purged {} messages from channel '{}'```".format(number, ctx.message.channel))
    embed.set_footer(text="Powered By HasteBot | Version 0.1 | By Sargera")
    embed_message = await bot.send_message(ctx.message.channel, embed=embed)
    await asyncio.sleep(4)
    await bot.delete_message(embed_message)
    
@bot.event
async def on_message(message):
    COMMANDS = ["!join", "!apply", "!help", "!ping", "!topservers", "!purge"]
    STAFF_ROLES = ["Owners"]

    if message.content.startswith(tuple(COMMANDS)):
        if str(message.channel) == "bot":
            await bot.process_commands(message)
        else:
            for staff_role in STAFF_ROLES:
                if str(staff_role.lower()) in [y.name.lower() for y in message.author.roles]:
                    await bot.process_commands(message)

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

<<<<<<< HEAD
@bot.event
async def on_member_join(member):
    embed = discord.Embed(title=":zap: Hastebot", description="{} has just joined the server. Please feel free to welcome them!".formatm(member.name))
    embed = add_field(name="Subscribe to notifcations", value="{}, would you like to subscribe to receive notifications from announcements on our server? Please react with yes/no respectively. You may unsubscribe at any time".format(member.name))
    embed.set_footer(text="Powered By HasteBot | Version 0.1 | By Sargera")
    embed_message = await bot.send_message(message.channel, embed=embed)
=======

bot.run('-- HIDDEN -- ')
>>>>>>> 688af7913a31b2d3e37c31dbfc82b834a512fb7d
    
bot.run('NDYxNTAwNzI2NzYyNTM2OTYx.DhUN6w.JxALi_hWZsrciyEwtxgVW9A7ttk')    
