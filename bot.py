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
        self.categories = {}

    async def on_ready(self):
        self.guild = discord.utils.get(self.guilds, id=GUILD_ID)
        if self.guild is None:
            logging.error(f"Guild with ID {GUILD_ID} not found.")
            return
        logging.info(f"Logged in as {self.user} (ID: {self.user.id})")
        logging.info(f"Connected to guild: {self.guild.name} (ID: {self.guild.id})")

    async def send_embed_message(self, channel, title, description):
        embed = discord.Embed(title=title, description=description, color=discord.Color.blue())
        await channel.send(embed=embed)

    async def delete_category(self, category):
        if category is None:
            logging.error("Category not found.")
            return
        await category.delete()
        if category.name in self.categories:
            del self.categories[category.name]
        logging.info(f"Deleted category: {category.name} (ID: {category.id})")

    async def delete_channel(self, channel):
        if channel is None:
            logging.error("Channel not found.")
            return
        await channel.delete()
        category_name = next((name for name, channels in self.categories.items() if any(c["id"] == channel.id for c in channels)), None)
        if category_name:
            self.categories[category_name] = [c for c in self.categories[category_name] if c["id"] != channel.id]
            if not self.categories[category_name]:
                del self.categories[category_name]
        logging.info(f"Deleted channel: {channel.name} (ID: {channel.id})")

    async def create_category(self, name):
        if self.guild is None:
            logging.error("Guild not found.")
            return
        category = await self.guild.create_category(name)
        self.categories[name] = []
        return category

    async def create_channel(self, name, category):
        if self.guild is None:
            logging.error("Guild not found.")
            return
        channel = await self.guild.create_text_channel(name, category=category)
        self.categories[category.name].append({"id": channel.id, "name": channel.name})
        return channel

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
