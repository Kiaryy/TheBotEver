import os
import time
import discord 
from discord import app_commands
from discord.ext import commands
from random import randint
from dotenv import load_dotenv
from keep_alive import keep_alive
import datetime

keep_alive()

load_dotenv()
API_KEY = os.getenv("API_KEY")

# Create an instance of the bot
bot= commands.Bot(command_prefix='!', intents= discord.Intents.all())
# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print("Ready to do some tomfoolery")
    print('------')
    global dateInit
    dateInit = datetime.datetime.now()
    #! sync commands with bot, only uncomment when you add a new command and then comment again
    # try:
    #     synced = await bot.tree.sync()
    # except Exception as e:
    #     print(e)

# Gets a random file from the shrimple folder
@bot.tree.command(name='shrimple',description="Sends a random Shrimple gif")
async def shrimple(interaction: discord.Interaction):
    await interaction.response.send_message(file=discord.File(f'src/shrimple_gifs/{shrimpleFolder[1][randint(0,shrimpleFolder[0]-1)]}'))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if randint(1,25) == 1:
        await message.channel.send(f"<@{message.author.id}> triggered a random shrimp event!!", file=discord.File(f'src/shrimple_gifs/{shrimpleFolder[1][randint(0,shrimpleFolder[0]-1)]}'))

# Gets a random file from the cats folder
@bot.tree.command(name='cars', description="Sends a random Cat gif")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(file=discord.File(f'src/silly_cars/{cars[1][randint(0,cars[0]-1)]}'))

# Simple number guessing game, with difficulty selector. Bullying included.
@bot.tree.command(name="guess_game", description="Guess the number!")
@app_commands.describe(difficulty="Choose a Difficulty")
@app_commands.choices(difficulty=[
    discord.app_commands.Choice(name="Easy", value=1),
    discord.app_commands.Choice(name="Medium", value=2),
    discord.app_commands.Choice(name="Hard", value=3)
])
async def guessing_game(interaction: discord.Interaction, difficulty: discord.app_commands.Choice[int]):
    guessTop = 0
    if difficulty.name == "Easy":
        guessTop = 10
    elif difficulty.name == "Medium":
        guessTop = 50
    else:
        guessTop = 100
    number = randint(1,guessTop)
    attempts = 3
    def check(m):
        return m.author == interaction.user
    await interaction.response.send_message(f"Im thinking of a number between 1 and {guessTop}")
    while True:
        if attempts < 1:
            await interaction.channel.send(f"That wasnt it, you suck bro @everyone laugh at them\nThe number was {number}")
            break
        msg = await bot.wait_for('message', check=check)
        try:
            guess = int(msg.content)
        except:
            await interaction.channel.send("Thats not a number lil bro")
            attempts-=1
            await interaction.channel.send(f"{attempts} attempts left")
            continue
        if guess == number:
            await interaction.channel.send("Thats the number!")
            break
        elif guess > number:
            attempts-=1
            await interaction.channel.send(f"Too high!")
        else:
            attempts-=1
            await interaction.channel.send(f"Too low!")  
        if attempts != 0:
            await interaction.channel.send(f"{attempts} attempts left")


@bot.tree.command(name="uptime", description="See how long the bot has been running for.")
async def get_uptime(interaction: discord.Interaction):
    epoch =round(dateInit.timestamp())
    
    await interaction.response.send_message(f"I've been running since <t:{epoch}:R>")
#TODO Command for adding images

def files_in_folder(folder_path): # Gives the number of files in a folder, and a list with all the files
    try:
        # List all files in the directory
        files = os.listdir(folder_path)
        
        # Use a list comprehension to filter out non-files
        files = [file for file in files if os.path.isfile(os.path.join(folder_path, file))]
        
        # Get the count of files
        file_count = len(files)
        
        return (file_count, files)
    except FileNotFoundError:
        print(f"The folder '{folder_path}' was not found.")
        return None
shrimpleFolder = files_in_folder("src/shrimple_gifs")
cars = files_in_folder("src/silly_cars")

# # Run the bot
bot.run(API_KEY)