#!/bin/python3

import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import logging

# Load environment variables from .env file
load_dotenv()

# Define constants
GUILD_ID = int(os.getenv("GUILD_ID"))
BOT_KEY = os.getenv("BOT_KEY")

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class Guideon(commands.Bot):
    def __init__(self, intents, *args, **kwargs):
        super().__init__(command_prefix="!", intents=intents, *args, **kwargs)
        self.guild = None

    async def on_ready(self):
        self.guild = discord.utils.get(self.guilds, id=GUILD_ID)
        if self.guild is None:
            logging.error(f"Guild with ID {GUILD_ID} not found.")
            return
        logging.info(f"Logged in as {self.user} (ID: {self.user.id})")
        logging.info(f"Connected to guild: {self.guild.name} (ID: {self.guild.id})")

    async def create_category(self, name):
        if self.guild is None:
            logging.error("Guild not found.")
            return
        category = await self.guild.create_category(name)
        return category

if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.guilds = True
    intents.members = True

    bot = Guideon(intents=intents)

    # run bots
    try:
        bot.run(BOT_KEY)
    except discord.LoginFailure:
        logging.error("Invalid token. Please check your BOT_KEY in the .env file.")
    except discord.HTTPException as e:
        logging.error(f"HTTP Exception: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
