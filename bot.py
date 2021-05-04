import discord
from discord import utils
from discord.ext import commands
import json
import requests
from discord.utils import get
import os
import asyncio
from asyncio import sleep

#Translate with Google Translate.I so sorry if you do not understand what is written here.

intents = discord.Intents().all()
intents.members = True
bot_name = 'Bot Name' #Add bot name
server_name = 'Server' #add server name
server_invite = '' #add invite to your server
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('This command does not exist!')

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="Porn Hub"))
    print("Bot connected {0.user}".format(bot))


@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, id=  ) #Add for the member who just joined
    await member.add_roles(role)

#HELP COMMANDS
@bot.command(pass_context=True)
async def help(ctx):
    emb = discord.Embed(title='Commands for bot {}'.format(bot_name), color=0xff9910)
    emb.add_field(name='{}help_fun'.format('$'), value='Enter this command to see commands for fun')
    emb.add_field(name='{}help_moder'.format('$'), value='Enter this command to see commands for moderation')
    await ctx.send(embed=emb)
    await ctx.message.add_reaction('✅')
#FINISHED HELP COMMANDS

#MODER COMMANDS
@bot.command(pass_context=True, aliases=['moder', 'moderator'])
async def help_moder(ctx):
    emb = discord.Embed(title='Commands for bot {} - moderation'.format(bot_name), color=0xff9910)
    emb.add_field(name='{}clear'.format('$'),value='Clear chat (max 100). $clear number')
    emb.add_field(name='{}kick'.format('$'),value='Kick a server member. $kick @user reason')
    emb.add_field(name='{}ban'.format('$'),value='Ban a server member. $ban @user reason')
    emb.add_field(name='{}mute'.format('$'), value='Issue a mut to the participant (prohibit chatting). $mute @user reason')
    emb.add_field(name='{}tempmute'.format('$'), value='Issue a temporary mut to the participant. $tempmute @user "time in minutes" and reason')
    emb.add_field(name='{}unmute'.format('$'),value='Allow member to chat. $unmute @user')
    emb.add_field(name='{}warn'.format('$'),value='Issue a warning to the member. $warn @user reason')
    await ctx.send(embed=emb)
    await ctx.message.add_reaction('✅')

@bot.command(aliases=['Mute'])
@commands.has_any_role()#Id Role or 'NameRole'.example - @commands.has_any_role('Moderator','Administator') .example2 - @commands.has_any_role(810096905472049192,810113817681199125,650413799471316992, 667821257496199180)
async def mute(ctx, member: discord.Member, reason='None'):
    emb = discord.Embed(title='Mute', color=0xff9910)
    mute_role = discord.utils.get(ctx.message.guild.roles, name='Muted')
    emb.add_field(name='Mute System', value=f'{member.name},has been muted on the server!Reason `{reason}`')
    await member.add_roles(mute_role)
    await ctx.send(embed=emb)
    await member.send(f'{member.name} you were muted on the server `{server_name}`!Reason `{reason}`')
    await ctx.message.add_reaction('✅')
@mute.error
async def mute_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('[ERROR], you must provide the name of the offender and the reason!')

@bot.command(aliases=['Unmute'])
@commands.has_any_role()#Id Role or 'NameRole'.example - @commands.has_any_role('Moderator','Administator') .example2 - @commands.has_any_role(810096905472049192,810113817681199125,650413799471316992, 667821257496199180)
async def unmute(ctx, member: discord.Member):
    emb = discord.Embed(title='Unmute', color=0xff9910)
    mute_role = discord.utils.get(ctx.message.guild.roles, name='Muted')
    emb.add_field(name='Mute System', value=f'{member.mention},can now write to chat!')
    await member.remove_roles(mute_role)
    await ctx.send(embed = emb)
    await member.send(f'{member.name}, you can now write on the server `{server_name}`')
    await ctx.message.add_reaction('✅')


@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("[ERROR], you must enter the participant's name!")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('[ERROR], you do not have sufficient rights!')

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("[ERROR], you must enter the participant's name!")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('[ERROR], you do not have sufficient rights!')


@bot.command(aliases=['Tempmute'])
@commands.has_any_role()#Id Role or 'NameRole'.example - @commands.has_any_role('Moderator','Administator') .example2 - @commands.has_any_role(810096905472049192,810113817681199125,650413799471316992, 667821257496199180)
async def tempmute(ctx, member: discord.Member, time: int, reason=None):
    role = member.guild.get_role('name_role') #NameRole for mute
    await member.send(f'`{member.name}`, you were muted on the server `{server_name}` in `{time}` minutes! Reason`{reason}`!')
    await member.add_roles(role)
    await member.move_to(None)
    await ctx.message.add_reaction('✅')
    await ctx.send(f'{member.mention} got a mute chat on `{time}` minutes! Reason: `{reason}`')
    await asyncio.sleep(time * 60)
    await member.remove_roles(role)


@tempmute.error
async def tempmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('[ERROR], you must indicate the name of the offender, the time and the reason!')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('[ERROR], you do not have sufficient rights!')

@bot.command(pass_context=True, aliases=['Clear'])
@commands.has_any_role()#Id Role or 'NameRole'.example - @commands.has_any_role('Moderator','Administator') .example2 - @commands.has_any_role(810096905472049192,810113817681199125,650413799471316992, 667821257496199180)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Has been cleared `{amount}` messages')


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('[ERROR], you must indicate the number of messages to be deleted!')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('[ERROR], you do not have sufficient rights!')

@bot.command(pass_context=True, aliases=['Kick'])
@commands.has_any_role()#Id Role or 'NameRole'.example - @commands.has_any_role('Moderator','Administator') .example2 - @commands.has_any_role(810096905472049192,810113817681199125,650413799471316992, 667821257496199180)
async def kick(ctx, member: discord.Member, *, reason='None'):
    await member.send(f'`{member.name}`, you were kicked from the server `{server_name}`!{server_invite} no longer break the rule: `{reason}`')
    await ctx.send(f'{member.mention} was kicked from the server! Reason `{reason}`')
    await member.kick(reason=reason)
    await ctx.message.add_reaction('✅')

@kick.error
async def kick_error(ctx,error):  
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('[ERROR], you must provide the member name and reason!')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send('[ERROR], you do not have sufficient rights!')

@bot.command()
@commands.has_any_role()#Id Role or 'NameRole'.example - @commands.has_any_role('Moderator','Administator') .example2 - @commands.has_any_role(810096905472049192,810113817681199125,650413799471316992, 667821257496199180)
async def warn(ctx, member: discord.Member, reason=None):
    if reason is None:
        await ctx.send(f'[ERROR], you must indicate the reason')

    else:
        await ctx.send(f'{member.name},got a warning for a reason `{reason}`')


@bot.command(pass_context=True, aliases=['Ban'])
@commands.has_any_role()#Id Role or 'NameRole'.example - @commands.has_any_role('Moderator','Administator') .example2 - @commands.has_any_role(810096905472049192,810113817681199125,650413799471316992, 667821257496199180)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.send(f'`{member.name}`, you were blocked on the server `{server_name}`! Reason : `{reason}`')
    await ctx.send(f'{member.mention} was blocked on the server! Reason: `{reason}`')
    await member.ban(reason=reason)
    await ctx.message.add_reaction('✅')


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('[ERROR], you must provide the member name and reason!')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send('[ERROR], you do not have sufficient rights!')
#FINISHED MODER COMMANDS

#FUN COMMANDS
@bot.command(pass_context=True, aliases=['fun'])
async def help_fun(ctx):
    emb = discord.Embed(title='Commands for bot {} - for fun'.format(bot_name), color=0xff9910)
    emb.add_field(name='{}cat'.format('$'), value='Sending a picture of a cat')
    emb.add_field(name='{}dog'.format('$'), value='Sending a picture of a dog')
    emb.add_field(name='{}pat'.format('$'), value='Anime')
    await ctx.send(embed=emb)
    await ctx.message.add_reaction('✅')

@bot.command()
async def cat(ctx):
    response = requests.get('https://some-random-api.ml/img/cat')
    json_data = json.loads(response.text)

    embed = discord.Embed(color=0xff9910, title='Cat')
    embed.set_image(url=json_data['link'])
    await ctx.send(embed=embed)
    await ctx.message.add_reaction('✅')


@bot.command()
async def dog(ctx):
    response = requests.get('https://some-random-api.ml/img/dog')
    json_data = json.loads(response.text)

    embed = discord.Embed(color=0xff9910, title='Dog')
    embed.set_image(url=json_data['link'])
    await ctx.send(embed=embed)
    await ctx.message.add_reaction('✅')

@bot.command()
async def pat(ctx):
    response = requests.get('https://some-random-api.ml/animu/pat')
    json_data = json.loads(response.text)

    embed = discord.Embed(color=0x3862ec, title='Pat')
    embed.set_image(url=json_data['link'])
    await ctx.send(embed=embed)
    await ctx.message.add_reaction('✅')
#FINISHED FUN COMMANDS

bot.run('TOKEN')