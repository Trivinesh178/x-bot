import json
import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import db
from grok_client import GrokClient

load_dotenv()
logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


class GrokCord(commands.Bot):
    def __init__(self, grok):
        super().__init__(command_prefix="!", intents=intents)
        self.grok = grok

    async def setup_hook(self):
        db.init()
        await self.load_extension("cogs.chat")
        await self.load_extension("cogs.moderation")
        await self.tree.sync()

    async def on_ready(self):
        logging.info("Logged in as %s", self.user)

    async def close(self):
        await self.grok.close()
        await super().close()


def main():
    token = os.getenv("DISCORD_TOKEN")
    api_key = os.getenv("XAI_API_KEY")
    if not token or not api_key:
        raise SystemExit("Set DISCORD_TOKEN and XAI_API_KEY in your .env file")

    with open("config.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)

    grok = GrokClient(
        api_key=api_key,
        model=os.getenv("GROK_MODEL", "grok-4.6"),
        system_prompt=cfg["system_prompt"],
        max_tokens=cfg["max_output_tokens"],
    )
    GrokCord(grok).run(token)


if __name__ == "__main__":
    main()
