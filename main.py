import discord
from discord import *
from discord import activity
from discord.enums import ActivityType, Status
from discord.ext import commands
import asyncio
import random
import json
import os
import time
import threading
import datetime
import aiofiles

def get_prefix(client, message):
    with open ('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix,  activity = discord.Activity(type=discord.ActivityType.streaming, name="Getting coded in dpy"), intents = discord.Intents.all())
client.remove_command('help')
client.warnings = {} # guild_id : {member.id : [count, [{admin_id, reason}]]}


# Cogs

# Loads cogs when the load command is ran
@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

    Loaded = discord.Embed(
        title = 'Loaded.',
        description = f'Successfully loaded the {extension} cog.',
        color = ctx.author.color
    )

    await ctx.send(embed = Loaded)

# Unloads the selected cog when the unload command is ran.
@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

    Unloaded = discord.Embed(
        title = 'Unloaded.',
        description = f'Successfully unloaded the {extension} cog.',
        color = ctx.author.color
    )

    await ctx.send(embed = Unloaded)

# Loads all cogs when bot is ran.
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.reload_extension(f'cogs.{extension}')

    Reloaded = discord.Embed(
        title = 'Reloaded.',
        description = f'Successfully reloaded the {extension} cog.',
        color = ctx.author.color
    )

    await ctx.send(embed = Reloaded)

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '*'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

        prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

@client.command()
@commands.has_permissions(administrator = True)
async def setprefix(ctx, prefix):

    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

    ChangedEmbed = discord.Embed(
        title = 'Command completed successfully.',
        description = f'Set server prefix to {prefix}',
        color = discord.Color.green()
    )

    await ctx.send(embed = ChangedEmbed)

if os.path.exists(os.getcwd() + "./config.json"):
    with open('./config.json') as f:
        configData = json.load(f)

import contextlib
import io
@client.command()
async def eval(ctx, *, code):
    str_obj = io.StringIO() #Retrieves a stream of data
    try:
        with contextlib.redirect_stdout(str_obj):
            exec(code)
    except Exception as e:
        return await ctx.send(f"```{e.__class__.__name__}: {e}```")
    await ctx.send(f'```{str_obj.getvalue()}```')

@client.command()
async def lscpu(ctx):
    import subprocess as sp
    import os
    
    lscpu = sp.getoutput("lscpu")
    
    await ctx.send(f'output: ' + f"""```txt
{lscpu}
```    """)

token = 'OTQwNTk2NjY5NjYwMTYwMDEx.YgJs6Q.T8O1H4_AeXdqGQi16YnLVJp1GoM'

@client.command()
async def terminal(ctx, *, cmd):
    import subprocess as sp
    
    cmd_output = sp.getoutput(cmd)
    
    OutPut = discord.Embed(
        title = "Terminal | PlutoHost",
        description = f"""```txt
{cmd_output}
```"""
    )
    
    await ctx.send(embed = OutPut)

client.run(token)
