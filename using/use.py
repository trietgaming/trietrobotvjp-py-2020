import asyncio
import discord
from discord.ext import commands
import json
from main import *
import random
from discord_components import Button, Select, SelectOption,DiscordComponents, ComponentsBot, Interaction,ActionRow

path = "/home/runner/trietrobotvjp/fishing/"

class Use(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.inventory = client.get_cog("Inventory")

    @commands.command()
    @cooldown(1,4,BucketType.user)
    async def use(self,ctx,item):
        await self.inventory.open_inventory(ctx.author)
        user_inv = (await self.inventory.get_inventory_data())[str(ctx.author.id)]
        if item not in user_inv:
            await ctx.send("Vật phẩm bạn chọn **không có trong kho đồ của bạn** hoặc **không tồn tại**!", delete_after = 4)
            return
        if not await self.is_useable(item):
            await ctx.send("Vật phẩm bạn chọn **không thể dùng được**!", delete_after = 3)
            return
        await ctx.send("Dùng")

    async def is_useable(self,item):
        return await self.inventory.get_item_data(item,"useable")
    
def setup(client):
    client.add_cog(Use(client))