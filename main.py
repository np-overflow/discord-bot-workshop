import discord
import os
from dotenv import load_dotenv
import requests

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