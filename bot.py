import discord
from discord.ext import commands
import json
import requests
from time import sleep
from random import choice

bot_name = "BOT NAME"
command_prefix = "!"
server_name = "SERVER NAME"
intents = discord.Intents().all()
intents.members = True
bot = commands.Bot(command_prefix, intents=intents)
bot.remove_command("help")
streaming = (
    "https://www.youtube.com/watch?v=YVkUvmDQ3HY",
    "https://www.youtube.com/watch?v=eJO5HU_7_1w",
    "https://www.youtube.com/watch?v=r_0JjYUe5jo",
)


@bot.event
async def on_ready():
    activity = discord.Streaming(
        platform="YouTube", name="Eminem", url=choice(streaming)
    )
    print(f"Bot connected {bot.user}")
    await bot.change_presence(status=discord.Status.dnd, activity=activity)


@bot.event
async def on_message(message):
    msg = message.content.lower() 
    if ("http" or "https") in msg:
        if "bet" in msg or "1x" in msg or "casino" in msg or "porn" in msg: # Antispam system
            if message.channel.id != (
                "783322703930851359" or "783327851390304286" or "783323335030210570" # You can write your channel id for ignore antispam system
            ):
                await message.delete()
    print(f"{message.author}: {message.content}")
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("This command does not exest!")
    else:
        pass


@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, id=783321672539308053)
    await member.add_roles(role)


# HELP COMMANDS
@bot.command(pass_context=True)
async def help(ctx):
    emb = discord.Embed(title=f"Commands for bot {bot_name}", color=0xFF9910)
    emb.add_field(
        name=f"{command_prefix}help_fun",
        value="Enter this command to see commands for fun",
    )
    emb.add_field(
        name=f"{command_prefix}help_moder",
        value="Enter this command to see commands for moderation ",
    )
    await ctx.send(embed=emb)
    await ctx.message.add_reaction("✅")


@bot.command(pass_context=True, aliases=["moder", "moderator"])
async def help_moder(ctx):
    emb = discord.Embed(title=f"Commands for bot {bot_name} - moderator", color=0xFF9910)
    emb.add_field(
        name=f"{command_prefix}clear", value="Clear chat (max 100).{command_prefix}clear number "
    )
    emb.add_field(
        name=f"{command_prefix}kick",
        value="Kick the server member.{command_prefix}kick @user reason ",
    )
    emb.add_field(
        name=f"{command_prefix}ban",
        value="Block a server member {command_prefix}Ban @user reason ",
    )
    emb.add_field(
        name=f"{command_prefix}mute",
        value=f"Issue a mute to the person (disable writing to the chat).{command_prefix}mute @user reason ",
    )
    emb.add_field(
        name=f"{command_prefix}tempmute",
        value=f'Issue a temporary mute to the person (prohibit chatting). {command_prefix}tempmute @user "time in minutes" and reason',
    )
    emb.add_field(
        name=f"{command_prefix}unmute",
        value=f"Allow the person to write to the chat. {command_prefix}unmute @user ",
    )
    emb.add_field(
        name=f"{command_prefix}warn",
        value=f"Issue a warning to the principal. {command_prefix}warn @user reason",
    )
    await ctx.send(embed=emb)
    await ctx.message.add_reaction("✅")


@bot.command(pass_context=True, aliases=["fun"])
async def help_fun(ctx):
    emb = discord.Embed(title=f"Commands for bot {bot_name} - for fun", color=0xFF9910)
    emb.add_field(
        name=f"{command_prefix}Cat_to_pm", value="Sending a picture of a cat to your pm chat"
    )
    emb.add_field(
        name=f"{command_prefix}Cat", value="Sending a picture of a cat to the general chat"
    )
    emb.add_field(
        name=f"{command_prefix}Dog", value="Sending a picture of a dog to a general chat"
    )
    emb.add_field(name=f"{command_prefix}Pat", value="Anime")
    await ctx.send(embed=emb)
    await ctx.message.add_reaction("✅")


# FINISHED HELP COMMANDS

# MODER COMMANDS


@bot.command(aliases=["Mute"])
@commands.has_any_role("650413799471316992, 667821257496199180" ) # role id
async def mute(ctx, member: discord.Member, reason="Without reason"):
    emb = discord.Embed(title="Mute", color=0xFF9910)
    mute_role = discord.utils.get(ctx.message.guild.roles, name="Muted")
    await emb.add_field(
        name="Mute System",
        value=f"{member.name}, has been muted on the server! Cause  `{reason}`",
    )
    await member.add_roles(mute_role)
    await ctx.send(embed=emb)
    await member.send(
        f"{member.name} you have been muted to the server `{server_name}`! Cause  `{reason}`"
    )
    await ctx.message.add_reaction("✅")


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("[ERROR], you must enter the participant's name!")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("[ERROR], you do not have sufficient rights!")


@bot.command(aliases=["Unmute"])
@commands.has_any_role("650413799471316992, 667821257496199180") # role id
async def unmute(ctx, member: discord.Member):
    emb = discord.Embed(title="Unmute", color=0xFF9910)
    mute_role = discord.utils.get(ctx.message.guild.roles, name="Muted")
    emb.add_field(
        name="Mute System", value=f"{member.mention}, can now write to chat! "
    )
    await member.remove_roles(mute_role)
    await ctx.send(embed=emb)
    await member.send(f"{member.name}, you were unmuted on the server `{server_name}`")
    await ctx.message.add_reaction("✅")


@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("[ERROR], you must enter the participant's name!")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("[ERROR], you do not have sufficient rights!")


@bot.command(aliases=["Tempmute"])
@commands.has_any_role("650413799471316992, 667821257496199180") # role id 
async def tempmute(ctx, member: discord.Member, time: int, reason=None):
    role = member.guild.get_role("Muted")
    await member.send(
        f"`{member.name}`, you have been mapped to the server `{server_name}` for `{time}` minutes! Reason `{reason}`!"
    )
    await member.add_roles(role)
    await member.move_to(None)
    await ctx.send(
        f"{member.mention} got mut for `{time}` minutes for the reason:  `{reason}`"
    )
    await ctx.message.add_reaction("✅")
    sleep(time * 60)
    await member.remove_roles(role)


@tempmute.error
async def tempmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("[ERROR], you must indicate the name of the offender, the time and the reason!")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("[ERROR], you do not have sufficient rights!")


@bot.command(pass_context=True, aliases=["Clear"])
@commands.has_any_role("650413799471316992, 667821257496199180") # role id
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"Messages `{amount}` have been cleared ")
    sleep(3)
    await ctx.channel.purge(limit=1)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "[ERROR], you must indicate the number of messages to be deleted! "
        )
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("[ERROR], you do not have sufficient rights! ")


@bot.command(pass_context=True, aliases=["Kick"])
@commands.has_any_role("650413799471316992, 667821257496199180" ) # role id
async def kick(ctx, member: discord.Member, *, reason="Без причины"):
    await member.send(
        f"`{member.name}`, you have been kicked out of the server `{server_name}`! No more  "
        f"don't break the rule anymore:  `{reason}`"
    )
    await ctx.send(f"{member.mention} was kicked from the server! Reason  `{reason}`")
    await member.kick(reason=reason)
    await ctx.message.add_reaction("✅")


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("[ERROR], you must provide the member name and reason! ")

    if isinstance(error, commands.MissingPermissions):
        await ctx.send("[ERROR], you do not have sufficient rights! ")


@bot.command()
@commands.has_any_role("650413799471316992, 667821257496199180" ) # role id
async def warn(ctx, member: discord.Member, reason=None):
    if reason is None:
        await ctx.send(f"[ERROR], you must indicate the reason ")

    else:
        await ctx.send(f"{member.name}, got a warning for a reason  `{reason}`")


@bot.command(pass_context=True, aliases=["Ban"])
@commands.has_any_role("650413799471316992, 667821257496199180" ) # role id
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.send(
        f"`{member.name}`, you have been blocked on the server `{server_name}`! Reason: `{reason}`"
    )
    await ctx.send(f"{member.mention} was blocked on the server! Reason:  `{reason}`")
    await member.ban(reason=reason)
    await ctx.message.add_reaction("✅")


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("[ERROR], you must indicate the reason for the ban ")

    if isinstance(error, commands.MissingPermissions):
        await ctx.send("[ERROR], you don't have enough rights! ")


# FINISHED MODER COMMANDS

# FUN COMMANDS

@bot.command(aliases=["cat"])
async def Cat(ctx):                                             # cat
    response = requests.get("https://some-random-api.ml/img/cat")
    json_data = json.loads(response.text)

    embed = discord.Embed(color=0xFF9910, title="Котейка")
    embed.set_image(url=json_data["link"])
    await ctx.send(embed=embed)
    await ctx.message.add_reaction("✅")


@bot.command(aliases=["dog"])
async def Dog(ctx):                                             # dog
    response = requests.get("https://some-random-api.ml/img/dog")
    json_data = json.loads(response.text)

    embed = discord.Embed(color=0xFF9910, title="Пёсик")
    embed.set_image(url=json_data["link"])
    await ctx.send(embed=embed)
    await ctx.message.add_reaction("✅")


@bot.command(aliases=["cat_to_pm", "cat_pm"])
async def Cat_to_pm(ctx):                                       # cat to pm
    response = requests.get("https://some-random-api.ml/img/cat")
    json_data = json.loads(response.text)

    embed = discord.Embed(color=0xFF9910, title="Котейка")
    embed.set_image(url=json_data["link"])
    await ctx.author.send(embed=embed)


@bot.command(aliases=["pat"])
async def Pat(ctx):                                              # Anime
    response = requests.get("https://some-random-api.ml/animu/pat")
    json_data = json.loads(response.text)

    embed = discord.Embed(color=0x3862EC, title="Pat")
    embed.set_image(url=json_data["link"])
    await ctx.send(embed=embed)
    await ctx.message.add_reaction("✅")


@bot.command()
async def sms(ctx, member: discord.Member, reason=None): # Anonim sms
    await member.send(reason)
    await ctx.channel.purge(limit=1)


# FINISHED FUN COMMANDS

bot.run("YOUR TOKEN")
