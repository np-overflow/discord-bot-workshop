import discord
import os
from dotenv import load_dotenv
import requests
import random
from datetime import datetime

load_dotenv()
bot = discord.Bot()

# Print a message when the bot is ready
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

# Display a Welcome Message to a User when they join the Server
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(os.getenv('BOT_CHANNEL')))
    await channel.send("Welcome {}".format(member.mention))

# Display a Leaving Message when a User leaves the Server
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(int(os.getenv('BOT_CHANNEL')))
    await channel.send("Why did you leave us?!")

# Slash command '/ping' to display the bot's latency
@bot.slash_command(description="Sends the bot's latency.")
async def ping(ctx): # a command called "ping" will be made
    await ctx.respond(f"Latency is {bot.latency} ms")

# Slash command '/join' with two str parameters that will join two strings together and return the joined string
@bot.slash_command(description="Joins two strings")
async def join(ctx, string1: str, string2: str):
    finalstr = string1 + string2
    await ctx.respond(f"The final string is {finalstr}")

# Create Slash Command group with bot.create_group
fun = bot.create_group("fun", "Fun commands!!")

# Fun command examples that discord bot can do (import random first!!)
# Chooses between two strings randomly and displays the chosen string
@fun.command(description="Chooses randomly from choice 1 and 2")
async def choose(ctx, choice1: str, choice2: str):
    choice = random.choice([choice1, choice2])
    await ctx.respond(f"The final choice is {choice}!!!!!")

# Roll a dice and get the result (from 1 to 6)
@fun.command(description="Rolls a six-sided dice")
async def dice(ctx):
    result = random.randint(1, 6)
    await ctx.respond(f"...and you rolled a {result}!!")

# Get the Current Weather Forecast for Singapore and Display it
@bot.slash_command(name="weather", description="Get the 24h weather forecast for Singapore")
async def get_weather(ctx: discord.ApplicationContext):
    # Make a Request to the Weather API
    apiUrl = "https://api.data.gov.sg/v1/environment/24-hour-weather-forecast"
    weatherData = requests.get(apiUrl).json()
    print(weatherData)
    
    
    # Extract relevant information from the weather data
    forecast = weatherData["items"][0]["general"]["forecast"]
    
    temperature = weatherData["items"][0]["general"]["temperature"]
    temperatureRangeText = f"{temperature['low']}°C - {temperature['high']}°C"
    
    wind = weatherData["items"][0]["general"]["wind"]
    windText = f"{wind['speed']['low']} - {wind['speed']['high']} km/h -- {wind['direction']}"
    
    # Format the message
    weatherMessage = (
        f"**24-Hour Weather Forecast**\n"
        f"Forecast: {forecast}\n"
        f"Temperature: {temperatureRangeText}\n"
        f"Wind: {windText}\n"
    )
    
    await ctx.respond(weatherMessage)

# Advanced Weather Fetching using Slash Commands with Subgroups
@bot.slash_command(name="weatherregions", description="Get the 24h weather forecast for Singapore, with REGIONS")
async def get_weather_regions(ctx: discord.ApplicationContext, region: str):
    # Check if the region is valid
    if region not in ['west', 'east', 'central', 'south', 'north']:
        await ctx.respond("Invalid region! Please choose from west, east, central, south, north.")
        return
    
    # Make a Request to the Weather API
    apiUrl = "https://api.data.gov.sg/v1/environment/24-hour-weather-forecast"
    weatherData = requests.get(apiUrl).json()
    
    # Create the Formatted Message using Embed
    embed = discord.Embed(
        title="24-Hour Weather Forecast", 
        description=f"Region: {region}",
        color=discord.Color.teal()
    )

    # Return the General Weather Forecast of the region
    periods = weatherData["items"][0]["periods"]
    for period in periods:
        # Format the Timestamps
        timeStart = datetime.fromisoformat(period['time']['start']).strftime('%m-%d %H:%M')
        timeEnd = datetime.fromisoformat(period['time']['end']).strftime('%m-%d %H:%M')
        regionWeatherAtTime = period['regions'][region]
        
        embed.add_field(
            name=f"{timeStart} - {timeEnd}",
            value=f"**Forecast:** {regionWeatherAtTime}\n"
        )

    await ctx.respond(embed=embed)

# Run the Bot
bot.run(os.getenv('TOKEN'))
