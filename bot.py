import discord
from discord.ext import commands
import json
import requests
from time import sleep
from random import choice

intents = discord.Intents().all()
intents.members = True
bot_name = "STKLF"
command_prefix = "!"
server_name = "STKLF"
bot = commands.Bot(command_prefix, intents=intents)
bot.remove_command("help")
admin = 4895734985793847 #change this

@bot.event
async def on_ready():
    print(f"Bot connected {bot.user}")
    await bot.change_presence(status=discord.Status.dnd, activity=activity)


@bot.event
async def on_message(message):
    msg = message.content.lower()
    if "bet" in msg or "1x" in msg or "casino" in msg or "porn" in msg:
        await message.delete()
    print(f"{message.author}: {message.content}")
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("This command does not exists!")
    else:
        pass


@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, id=12345667890123) # change this
    await member.add_roles(role)


# HELP COMMANDS
@bot.command(pass_context=True)
async def help(ctx):
    emb = discord.Embed(title=f"Commands for {bot_name}", color=0xFF9910)
    emb.add_field(
        name=f"{command_prefix}help_fun",
        value="Fun commands",
    )
    emb.add_field(
        name=f"{command_prefix}help_moder",
        value="Moder.commands",
    )
    await ctx.send(embed=emb)
    await ctx.message.add_reaction("✅")


@bot.command(pass_context=True, aliases=["moder", "moderator"])
async def help_moder(ctx):
    emb = discord.Embed(title=f"Commands for {bot_name} - moder", color=0xFF9910)
    emb.add_field(
        name=f"{command_prefix}clear", value="clear chat"
    )
    emb.add_field(
        name=f"{command_prefix}kick",
        value="{command_prefix}kick @user reason",
    )
    emb.add_field(
        name=f"{command_prefix}ban",
        value="{command_prefix}ban @user reason",
    )
    emb.add_field(
        name=f"{command_prefix}mute",
        value=f"{command_prefix}mute @user reason",
    )
    emb.add_field(
        name=f"{command_prefix}tempmute",
        value=f'{command_prefix}tempmute @user time/s/m/y reason',
    )
    emb.add_field(
        name=f"{command_prefix}unmute",
        value=f"{command_prefix}unmute @user",
    )
    await ctx.send(embed=emb)
    await ctx.message.add_reaction("✅")


@bot.command(pass_context=True, aliases=["fun"])
async def help_fun(ctx):
    emb = discord.Embed(title=f"Commands for {bot_name} fun", color=0xFF9910)
    emb.add_field(
        name=f"{command_prefix}cat", 
        value="Send photo with cat"
    )
    emb.add_field(
        name=f"{command_prefix}dog", 
        value="Send photo with dog"
    )
    emb.add_field(
        name=f"{command_prefix}pat", 
        value="Anime"
    )
    emb.add_field(
        name=f"{command_prefix}neko",
        value=f"Neko img"
    )
    await ctx.send(embed=emb)
    await ctx.message.add_reaction("✅")


# FINISHED HELP COMMANDS

# MODER COMMANDS


@bot.command(aliases="Mute")
@commands.has_any_role(admin)
async def mute(ctx, member: discord.Member, *, reason="No reason"):
    mute_role = discord.utils.get(ctx.message.guild.roles, id=1234567889076) #change id to you role id for mute
    await ctx.send(f"{member.name}, be muted! reason `{reason}`")
    await member.add_roles(mute_role)
    try:
        await member.send(
            f"{member.name} you will be muted `{server_name}`! Reason `{reason}`"
        )
    except:
        print("Might not be receiving messages")
    await ctx.message.add_reaction("✅")


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("[ERROR], you need to write user name!")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("[ERROR, you are not right enough!")


@bot.command(aliases="Unmute")
@commands.has_any_role(admin)
async def unmute(ctx, member: discord.Member):
    mute_role = discord.utils.get(ctx.message.guild.roles, id=790274663791853568)
    await ctx.send(f"{member.mention}, now can write to chat!")
    await member.remove_roles(mute_role)

    await ctx.message.add_reaction("✅")


@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("[ERROR], you need to write user name!")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("[ERROR, you are not right enough!")


@bot.command(aliases=["Tempmute"])
@commands.has_any_role(650413799471316992, 667821257496199180)
async def tempmute(ctx, member: discord.Member, time, *, reason="Без причины"):
    role = discord.utils.get(ctx.message.guild.roles, id=790274663791853568)
    time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    tempmutee = int(time[:-1]) * time_convert[time[-1]]
    await member.add_roles(role)
    await member.move_to(None)
    await ctx.send(
        f"{member.mention} got mute for a `{time}`. Reason: `{reason}`"
    )
    await member.add_roles(role)
    await member.move_to(None)
    try:
        await member.send(
            f"`{member.name}`, you got mute on a `{server_name}` for a `{time}`! Reason`{reason}`!"
        )
    except:
        pass
    await ctx.message.add_reaction("✅")
    await asyncio.sleep(tempmutee)
    await member.remove_roles(role)


@tempmute.error
async def tempmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("[ERROR], you need to write name and reason!")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("[ERROR, you are not right enough!")


@bot.command(pass_context=True, aliases="Clear")
@commands.has_any_role(admin)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"Was cleared `{amount}`")

@bot.command(pass_context=True)
@commands.has_any_role(admin)
async def kick(ctx, member: discord.Member, *, reason="No reason"):
    await ctx.send(f"{member.mention} was kicked from server ! Reason `{reason}`")
    try:
        await member.send(
            f"`{member.name}`, you have been kicked from the server `{server_name}`! Don't break the rule again `{reason}`"
        )
    except:
        pass
    await member.kick(reason=reason)
    await ctx.message.add_reaction("✅")


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("[ERROR], you must provide a member name and a reason!")

    if isinstance(error, commands.MissingPermissions):
        await ctx.send("[ERROR], you do not have enough rights!")


@bot.command(pass_context=True)
@commands.has_any_role(admin)
async def ban(ctx, member: discord.Member, *, reason=None):
    await ctx.send(f"{member.mention} blocked on the server! Reason `{reason}`")
    try:
        await member.send(
            f"`{member.name}`, you have been banned from the server `{server_name}`! Reason `{reason}`"
        )
    except:
        pass
    await member.ban(reason=reason)
    await ctx.message.add_reaction("✅")


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("[ERROR], you must provide a member name and a reason!")

    if isinstance(error, commands.MissingPermissions):
        await ctx.send("[ОШИБКА], you don't have enough rights!")


# FINISHED MODER COMMANDS

# FUN COMMANDS
@bot.command()
async def neko(ctx):
    if ctx.channel.is_nsfw():
        choises = ['neko', 'fox_girl']
        odpoved = choice(choises)
        response = requests.get(f"https://nekos.life/api/v2/img/{odpoved}")
        json_data = json.loads(response.text)
        embed = discord.Embed(color=0xFF9910, title="Neko")
        embed.set_image(url=json_data["url"])
        await ctx.send(embed=embed)

@bot.command()
async def cat(ctx):
    response = requests.get("https://some-random-api.ml/img/cat")
    json_data = json.loads(response.text)

    embed = discord.Embed(color=0xFF9910, title="CAT!")
    embed.set_image(url=json_data["link"])
    await ctx.send(embed=embed)
    await ctx.message.add_reaction("✅")


@bot.command()
async def dog(ctx):
    response = requests.get("https://some-random-api.ml/img/dog")
    json_data = json.loads(response.text)

    embed = discord.Embed(color=0xFF9910, title="DOG!")
    embed.set_image(url=json_data["link"])
    await ctx.send(embed=embed)
    await ctx.message.add_reaction("✅")

@bot.command(aliases=["pat"])
async def pat(ctx):
    response = requests.get("https://some-random-api.ml/animu/pat")
    json_data = json.loads(response.text)

    embed = discord.Embed(color=0x3862EC, title="Pat")
    embed.set_image(url=json_data["link"])
    await ctx.send(embed=embed)
    await ctx.message.add_reaction("✅")


@bot.command()
async def anon(ctx, member: discord.Member, reason=None):
    if "NAME" not in member.name:
        await member.send(reason)
        await ctx.channel.purge(limit=1)
    else: 
        pass


# FINISHED FUN COMMANDS

bot.run(open("token.txt", 'r').readlines())
