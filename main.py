import os
import discord
import logging
import asyncio
import base64
from PIL import Image
from discord.ext import commands
from data import db_session
from data.users import User
from tools import get_question

TOKEN = "MTA5ODIyMTkwMDg0MjQwNTkwOA.GmsZQ3.WTgn9LZ7PP35Q9yuHiwnL7BhaB3ckWBs3RfYYE"

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

db_session.global_init("db/discord_bot.db")

bot = commands.Bot(command_prefix='!', intents=intents)


def add_user_if_not_found(user):
    id, name = user.id, user.name
    db_sess = db_session.create_session()
    user_ = db_sess.query(User).filter(User.id == id).first()
    if not user_:
        user_ = User(id=id, name=name)
        db_sess.add(user_)
        db_sess.commit()


@bot.command(name='question')
async def question(ctx, complexity):
    complexity_list = ['easy', 'normal', 'hard', 'impossible']
    complexity = complexity if complexity in complexity_list else 'normal'
    add_user_if_not_found(ctx.author)
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == ctx.author.id).first()
    data = get_question(complexity, country=user.last_ans)
    if user.last_ans == '':
        user.last_ans = data['country']
    if user.last_complexity == '' or complexity_list.index(user.last_complexity) > complexity_list.index(complexity):
        user.last_complexity = complexity
    db_sess.commit()
    img_bytes = bytes(data['content'], data['encoding'])
    f_name = f'img/{data["country"]}.png'
    if f_name not in [i for i in os.walk('img')][0][2]:
        with open(f_name, 'wb') as f:
            f.write(img_bytes)
    if complexity != 'impossible':
        content = f'Варианты ответа:\n{"; ".join([i for i in data["variants"]])}'
    else:
        content = 'Введите ответ'
    await ctx.send(file=discord.File(f_name), content=content)


@bot.command(name='answer')
async def answer(ctx, ans):
    complexity_dict = {'easy': 1, 'normal': 5, 'hard': 25, 'impossible': 125}
    add_user_if_not_found(ctx.author)
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == ctx.author.id).first()
    if user.last_ans == '':
        return
    if user.last_ans == ans:
        user.score += complexity_dict[user.last_complexity]
        response = 'Верно!'
    else:
        user.score -= complexity_dict[user.last_complexity]
        response = 'Неверно!'
    response += f'\nТекущий счёт:{user.score}'
    user.last_ans = ''
    user.last_complexity = ''
    db_sess.commit()
    await ctx.send(response)


@bot.command(name='profile')
async def profile(ctx):
    add_user_if_not_found(ctx.author)
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == ctx.author.id).first()
    await ctx.send(f'Discord-id: {user.id}\nИмя: {user.name}\nОчки: {user.score}')


@bot.command(name='inf')
async def inf(ctx):
    await ctx.send("Sat Guess bot - это discord-бот сайта https://sat-guess.glitch.me/, который"
                   " даёт возможность отгадывать страны по их снимкам со спутника. Команды "
                   "бота:\n!inf - информация о боте\n!profile - выводит информацию об аккаунте\n!question <сложность> -"
                   " выводит вопрос соответствующей сложности (easy - легко, normal - нормально, hard - сложно,"
                   " impossible - невозможно)\n!answer <ответ> - ответить на вопрос")


bot.run(TOKEN)
