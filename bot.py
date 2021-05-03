import discord
from discord import utils
from discord.ext import commands
import json
import requests
from discord.utils import get
import os
import asyncio
from asyncio import sleep

intents = discord.Intents().all()
intents.members = True
bot_name = 'FWadels'
bot = commands.Bot(command_prefix='$', intents=intents)
bot.remove_command('help')

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Данной команды не существует!')

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="Porn Hub"))
    print("Бот подключен {0.user}".format(bot))


@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, id=783321672539308053)
    await member.add_roles(role)

#HELP COMMANDS
@bot.command(pass_context=True)
async def help(ctx):
    emb = discord.Embed(title='Команды для бота {}'.format(bot_name), color=0xff9910)
    emb.add_field(name='{}help_fun'.format('$'), value='Введите данную команду чтобы увидеть команды для веселья')
    emb.add_field(name='{}help_moder'.format('$'), value='Введите данную команду чтобы увидеть команды для модерации')
    await ctx.send(embed=emb)
    await ctx.message.add_reaction('✅')
#FINISHED HELP COMMANDS

#MODER COMMANDS
@bot.command(pass_context=True, aliases=['moder', 'moderator'])
async def help_moder(ctx):
    emb = discord.Embed(title='Команды бота {} - модерация'.format(bot_name), color=0xff9910)
    emb.add_field(name='{}clear'.format('$'),
                  value='Очистить чат(макс.100).$clear число')
    emb.add_field(name='{}kick'.format('$'),
                  value='Кикнуть участника сервера.$kick @user причина')
    emb.add_field(name='{}ban'.format('$'),
                  value='Заблокировать участника сервера.$ban @user причина')
    emb.add_field(name='{}mute'.format(
        '$'), value='Выдать мут участнику (запретить писать в чат).$mute @user причина')
    emb.add_field(name='{}tempmute'.format(
        '$'), value='Выдать временый мут участнику (запретить писать в чат).$tempmute @user "время в минутах" и причина')
    emb.add_field(name='{}unmute'.format('$'),
                  value='Разрешить участнику писать в чат.$unmute @user')
    emb.add_field(name='{}warn'.format('$'),
                  value='Выдать предупреждение участнику.$warn @user причина')
    await ctx.send(embed=emb)
    await ctx.message.add_reaction('✅')

@bot.command(aliases=['Mute'])
@commands.has_any_role(810096905472049192,810113817681199125,650413799471316992, 667821257496199180)
async def mute(ctx, member: discord.Member, reason='Без причины'):
    emb = discord.Embed(title='Mute', color=0xff9910)
    mute_role = discord.utils.get(ctx.message.guild.roles, name='Muted')
    emb.add_field(name='Mute System', value=f'{member.name},был замьючены на сервере!Причина `{reason}`')
    await member.add_roles(mute_role)
    await ctx.send(embed=emb)
    await member.send(f'{member.name} вы были замьючены на сервере `🔰STKLF Squad🔰`!Причина `{reason}`')
    await ctx.message.add_reaction('✅')
@mute.error
async def mute_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('[ОШИБКА],вы должны указать имя нарушителя и причину!')

@bot.command(aliases=['Unmute'])
@commands.has_any_role(810096905472049192,810113817681199125,650413799471316992, 667821257496199180)
async def unmute(ctx, member: discord.Member):
    emb = discord.Embed(title='Unmute', color=0xff9910)
    mute_role = discord.utils.get(ctx.message.guild.roles, name='Muted')
    emb.add_field(name='Mute System', value=f'{member.mention},теперь может писать в чат!')
    await member.remove_roles(mute_role)
    await ctx.send(embed = emb)
    await member.send(f'{member.name}, вы были размьючены на сервере `🔰STKLF Squad🔰`')
    await ctx.message.add_reaction('✅')


@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('[ОШИБКА],вы должны указать имя участника!')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('[ОШИБКА],у вас недостаточно прав!')

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('[ОШИБКА],вы должны указать имя участника!')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('[ОШИБКА],у вас недостаточно прав!')


@bot.command(aliases=['Tempmute'])
@commands.has_any_role(810096905472049192,810113817681199125,650413799471316992, 667821257496199180)
async def tempmute(ctx, member: discord.Member, time: int, reason=None):
    role = member.guild.get_role(790274663791853568)
    await member.send(f'`{member.name}`, вы были замьючены на сервере `🔰STKLF Squad🔰` на `{time}` минут!Причина`{reason}`!')
    await member.add_roles(role)
    await member.move_to(None)
    await ctx.message.add_reaction('✅')
    await ctx.send(f'{member.mention} получил мут на `{time}` минут по причине: `{reason}`')
    await asyncio.sleep(time * 60)
    await member.remove_roles(role)


@tempmute.error
async def tempmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('[ОШИБКА],вы должны указать имя нарушителя,время и причину!')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('[ОШИБКА],у вас недостаточно прав!')

@bot.command(pass_context=True, aliases=['очистка','Clear'])
@commands.has_any_role(810096905472049192,810113817681199125,650413799471316992, 667821257496199180)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Было очищено `{amount}` сообщений')


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('[ОШИБКА],вы должны указать кол.во сообщений которые нужно удалить!')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('[ОШИБКА],у вас недостаточно прав!')

@bot.command(pass_context=True, aliases=['кик','Kick'])
@commands.has_any_role(810096905472049192,810113817681199125,650413799471316992, 667821257496199180)
async def kick(ctx, member: discord.Member, *, reason='Без причины'):
    await member.send(f'`{member.name}`, вы были изгнаны из сервера `🔰STKLF Squad🔰`!https://discord.gg/UQuWPYKfYf впредь не нарушайте правило: `{reason}`')
    await ctx.send(f'{member.mention} был кикнут с сервера!Причина `{reason}`')
    await member.kick(reason=reason)
    await ctx.message.add_reaction('✅')

@kick.error
async def kick_error(ctx,error):  
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('[ОШИБКА],вы должны указать имя участника и причину!')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send('[ОШИБКА],у вас недостаточно прав!')

@bot.command()
@commands.has_any_role(810096905472049192,810113817681199125,650413799471316992, 667821257496199180)
async def warn(ctx, member: discord.Member, reason=None):
    if reason is None:
        await ctx.send(f'[ОШИБКА],вы должны указать причину')

    else:
        await ctx.send(f'{member.name},получил предупреждение по причине `{reason}`')


@bot.command(pass_context=True, aliases=['бан','Ban'])
@commands.has_any_role(810096905472049192,810113817681199125,650413799471316992, 667821257496199180)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.send(f'`{member.name}`, вы были заблокированы на сервере `🔰STKLF Squad🔰`!Причина : `{reason}`')
    await ctx.send(f'{member.mention} был заблокирован на сервере!Причина: `{reason}`')
    await member.ban(reason=reason)
    await ctx.message.add_reaction('✅')


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('[ОШИБКА],вы должны указать имя участника и причину!')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send('[ОШИБКА],у вас недостаточно прав!')
#FINISHED MODER COMMANDS

#FUN COMMANDS
@bot.command(pass_context=True, aliases=['fun'])
async def help_fun(ctx):
    emb = discord.Embed(title='Команды бота {} - для веселья'.format(bot_name), color=0xff9910)
    emb.add_field(name='{}Въебать'.format('$'),value='Въебать участнику')
    emb.add_field(name='{}cat'.format('$'), value='Отправка картинки котика вам в ЛС')
    emb.add_field(name='{}кот'.format('$'), value='Отправка картинки котика в общий чат')
    emb.add_field(name='{}пёс'.format('$'), value='Отправка картинки собаки в общий чат')
    emb.add_field(name='{}pat'.format('$'), value='Далбоёб который это писал не знает что такое "pat"')
    await ctx.send(embed=emb)
    await ctx.message.add_reaction('✅')

@bot.command()
async def Въебать(ctx):
    author = ctx.message.author
    await ctx.send(f"Въебать {author.mention} произошло успешно!")
    await ctx.message.add_reaction('✅')

@bot.command()
async def кот(ctx):
    response = requests.get('https://some-random-api.ml/img/cat')
    json_data = json.loads(response.text)

    embed = discord.Embed(color=0xff9910, title='Котейка')
    embed.set_image(url=json_data['link'])
    await ctx.send(embed=embed)
    await ctx.message.add_reaction('✅')


@bot.command()
async def пёс(ctx):
    response = requests.get('https://some-random-api.ml/img/dog')
    json_data = json.loads(response.text)

    embed = discord.Embed(color=0xff9910, title='Пёсик')
    embed.set_image(url=json_data['link'])
    await ctx.send(embed=embed)
    await ctx.message.add_reaction('✅')

@bot.command()
async def cat(ctx):
    response = requests.get('https://some-random-api.ml/img/cat')
    json_data = json.loads(response.text)

    embed = discord.Embed(color=0xff9910, title='Котейка')
    embed.set_image(url=json_data['link'])
    await ctx.author.send(embed=embed)

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