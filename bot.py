import discord
import logging
import os
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
