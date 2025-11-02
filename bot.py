import discord
import logging
import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands
from weather import get_weather, get_forecast

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a+')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
guild = bot.get_guild(1418320366048378923)


check_task_started = False
@bot.event
async def on_ready():
    global check_task_started
    if not check_task_started:
        bot.loop.create_task(checkTime())
        check_task_started = True


async def checkTime():
    await bot.wait_until_ready()
    channel = bot.get_channel(1418320366501367883)
    last_sent_date = None

    while not bot.is_closed():
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        current_date = now.date().strftime('%d-%m-%Y')


        if current_time == "05:00:00" and last_sent_date != current_date:
            await channel.send(get_forecast('Rybnik'))
            await channel.send(get_forecast('Katowice'))
            last_sent_date = current_date

        await asyncio.sleep(1)

@bot.command(name='pogoda', description="Returns current weather condition for given city")
async def pogoda(ctx, *, city=None):
    if city is None:
        await ctx.send('❌ Misiu kolorowy, musisz podać miasto :/')
    else:
        conditions = get_weather(city)
        await ctx.send(f"{ctx.author.mention}\n{conditions}")

@bot.command(name='prognoza', description="Returns weather forecast for next 12 hours")
async def prognoza(ctx, *, city=None):
    if city is None:
        await ctx.send('❌ Misiu kolorowy, musisz podać miasto :/')
    else:
        forecast = get_forecast(city)
        await ctx.send(f"{ctx.author.mention}\n{forecast}")

@bot.command(name="subscribe")
async def subscribe(ctx, *, city):
    guild = ctx.guild
    role = discord.utils.get(ctx.guild.roles, name=city)
    if role is None:
        role = await guild.create_role(name=city)
        await ctx.send(f"Rola {city} została stworzona")
    await ctx.author.add_roles(role)
    await ctx.send(f"{ctx.author.mention} zasubskrybował {city}!")

@bot.command(name="unsubscribe")
async def unsubscribe(ctx, *, city=None):
    role = discord.utils.get(ctx.guild.roles, name=city)
    if city is None or role is None:
        await ctx.send(f"{ctx.author.mention} musisz podać miasto, lub rola dla podanego miasta nie istnieje ❌")
    else:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} odsubskrybował {city}!")



bot.run(token)
