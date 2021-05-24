import discord
import random
from discord.ext import commands
from discord.ext import tasks
from itertools import cycle
from discord.ext.commands import has_permissions, MissingPermissions
from discord import Member
from traceback import format_exception
import discord.utils as utils
from discord.utils import *
import io
import contextlib
from io import BytesIO
from pprint import pprint
import textwrap
import asyncio
import json
import datetime


client = commands.Bot(command_prefix ="a.", intents=discord.Intents.all())
client.remove_command("help")
@client.event
async def on_ready():
    print("ready")
    if len(client.guilds) > 1:
        await client.change_presence(status=discord.Status.dnd, activity=discord.Game(f'Helping prevent abuse in {len(client.guilds)} servers'))
    else:
        await client.change_presence(status=discord.Status.dnd, activity=discord.Game(f'Helping prevent abuse in {len(client.guilds)} server'))



@client.command()
@commands.is_owner()
async def reload(ctx, *, module=None):
    modules = ['rpc']
    if module in modules:
        if module.lower() == "rpc":
            await client.change_presence(status=discord.Status.dnd, activity=discord.Game(f'Helping prevent abuse in {len(client.guilds)} servers'))

        await ctx.reply(f'Reloaded {module}!')
    elif module == None:
        await ctx.reply(modules)
    else:
        await ctx.reply(f"Unkown module!\nList of modules:\n{modules}")


@client.command()
@commands.has_permissions(manage_roles=True)
async def heartbeat(ctx):
    guild = ctx.guild
    channel = utils.get(client.get_all_channels(), guild__name=guild.name, name='anti-abuse-logs')
    if channel == None:
        embed = discord.Embed(
            title = 'Anti Abuse +',
            description = 'Error Detected!',
            colour = discord.Colour.red()
        )
    else:
        embed = discord.Embed(
        title = 'Anti Abuse +',
        description = 'No Errors Detected!',
        colour = discord.Colour.blurple()
        )
    if channel == None:
        embed.add_field(name='Heartbeat', value='Warning: You do **not** have a channel called "anti-abuse-logs". Create now to catch abuse!')
#    embed.add_field(name='How to set up', value='Just create a channel called "anti-abuse-logs". its that easy! Soon i may make this customizable.')
    await ctx.send(embed=embed)

@client.event
async def on_member_update(b, a):
    if b.roles != a.roles:
        if len(b.roles) < len(a.roles):
            guild = a.guild
            now = datetime.datetime.now()
            async for entry in guild.audit_logs(action=discord.AuditLogAction.member_role_update, limit=1,  before=now):
                channel = utils.get(client.get_all_channels(), guild__name=guild.name, name='anti-abuse-logs')
                if a == entry.user:
                    embed = discord.Embed(
                        title = 'Possible Abuse Detected!',
                        description = a.name + "#" + a.discriminator + " gave themselves a role!",
                        colour = discord.Colour.red()
                        )
                    for role in a.roles:
                        if role not in b.roles:
                            embed.add_field(name='Role given:', value=role.mention)
                    await channel.send(embed=embed)
                    print(a.name + "#" + a.discriminator + " gave themselves a role!")
            

           
client.run("token")
