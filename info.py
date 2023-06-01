import asyncio
import discord
from discord.ext import commands
import json
from main import *
import random

class Info(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.inventory = client.get_cog("Inventory")

    @commands.command()
    async def info(self,ctx, user: discord.User):
       return
    

def setup(client):
    client.add_cog(Info(client))