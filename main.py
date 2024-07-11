import discord
import os
from dotenv import load_dotenv
import requests
import random

load_dotenv()
bot = discord.Bot()

# Print a message when the bot is ready
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

# Display a Welcome Message to a User when they join the Server
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(BOT_CHANNEL)
    await channel.send("Welcome {}".format(member.mention))

# Display a Leaving Message when a User leaves the Server
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(BOT_CHANNEL)
    await channel.send("Why did you leave us?!")

# Slash command '/ping' to display the bot's latency
@bot.command(description="Sends the bot's latency.")​
async def ping(ctx): # a command called "ping" will be made​
    await ctx.respond(f"Latency is {bot.latency}")

# Slash command '/join' with two str parameters that will join two strings together and return the joined string
@bot.command(description="joins two strings") ​
async def join(ctx, string1: str, string2: str): ​
    finalstr = string1 + string2 ​
    await ctx.respond(f"the final string is {finalstr}")

# create Slash Command group with bot.create_group​
fun = bot.create_group("fun", "fun commands!!")​
# instead of @bot.command, use @{groupname}.command

# fun command examples that discord bot can do (import random first!!)
# chooses between two strings randomly and displays the chosen string
@fun.command(description="chooses randomly from choice 1 and 2")​
async def choose(ctx, choice1: str, choice2: str):​
    randomint = random.randint(1,2)​
    if randomint == 1:​
        choice = choice1​
    else:​
        choice = choice2​
    await ctx.respond(f"The final choice is {choice}!!!!!")​

# roll a dice and get the result (from 1 to 6)
@fun.command(description="rolls a six-sided dice")​
async def dice(ctx):​
    result = random.randint(1,6)​
    await ctx.respond(f"...and you rolled a {result}!!")

# Get the Current Weather Forecast for Singapore and Display it
@bot.slash_command(name="weather", description="Get the 24h weather forecast for Singapore")
async def get_weather(ctx: discord.ApplicationContext):
    # Make a Request to the Weather API
    apiUrl = "https://api.data.gov.sg/v1/environment/24-hour-weather-forecast"
    weatherData = requests.get(apiUrl).json()
    
    # Extract relevant information from the weather data
    forecast = weatherData.get('items', [])[0].get('general', {}).get('forecast', 'No data available')
    temperature = weatherData.get('items', [])[0].get('general', {}).get('temperature', {})
    temperature_range = f"{temperature.get('low', 'N/A')}°C - {temperature.get('high', 'N/A')}°C"
    
    # Format the message
    weather_message = (
        f"**24-Hour Weather Forecast**\n"
        f"Forecast: {forecast}\n"
        f"Temperature: {temperature_range}\n"
    )
    
    await ctx.respond(weather_message)
    
# Run the Bot
bot.run(os.getenv('TOKEN'))
