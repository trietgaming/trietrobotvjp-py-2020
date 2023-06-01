import asyncio
import discord
from discord.ext import commands
import json
from main import *
import random
from discord_components import Button, Select, SelectOption,DiscordComponents, ComponentsBot, Interaction,ActionRow

path = "/home/runner/trietrobotvjp/fishing/"

class Fishing(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.inventory = client.get_cog("Inventory")

    @commands.command(aliases=["gf","gofish","gofishing"])
    @cooldown(1,18,BucketType.user)
    async def fishing(self, ctx, location = None):
        await self.inventory.open_inventory(ctx.author)
        if location == "r":
            location = "river"
        if location == "s":
            location = "sea"
        if (location != "sea" and location != "river") or location == None:
            await ctx.send('Vui lòng nhập địa điểm câu cá: **"sea"** (biển) hoặc **"river"** (sông)', delete_after = 5)
            return      
        users_inv = await self.inventory.get_inventory_data()
        if "0000" not in users_inv[str(ctx.author.id)]:
            await ctx.send(f"Bạn phải có **<:cancauthuong:876424458154418186> Cần câu cá#`0000`** mới có thể câu cá!")
            return
        if "0034" not in users_inv[str(ctx.author.id)]:
            await ctx.send(f"Bạn phải có **<:moicau:877132339585626132> Mồi câu cá#`0034`** mới có thể câu cá!")
            return
        if location == "river" and "0035" not in users_inv[str(ctx.author.id)]:
            await ctx.send(f"Bạn phải có **<:thuyennho:877131605674717195> Thuyền đánh cá nhỏ#`0035`** mới có thể câu cá ở river!")
            return
        if location == "sea" and "0036" not in users_inv[str(ctx.author.id)]:
            await ctx.send(f"Bạn phải có **<:taucalon:877133054991278140> Tàu đánh cá lớn#`0036`** mới có thể câu cá ở sea!")
            return
        with open(path+"animalcolor.json","r") as f:
            colors = json.load(f)
        current_boat = ""
        if location == "sea":
            current_boat = "0036"
        else:
            current_boat = "0035"
        button = [Button(label = "Chưa câu được", style = 2, custom_id = "catch", disabled = True)]
        b_action = ActionRow(*button)       
        embed = discord.Embed(title = f"<a:fishingmanfishing2018:876766462335922196> {ctx.author.name} đang chờ cá cắn câu <a:dots:878831384926507009>")
        embed.set_thumbnail(url = "https://media.giphy.com/media/tIk1NLkHzKYBboNhnO/giphy.gif?cid=790b7611be729d3c938ba7fa51a21b24921e5e6337fb8539&rid=giphy.gif&ct=g")
        await self.inventory.update_inventory(ctx.author, "0034", -1)
        message = await ctx.send(embed = embed, components = [b_action])
        waiting = random.randint(2,6)
        await asyncio.sleep(waiting)
        embed = discord.Embed(title = f"🐟 {ctx.author.name} nhanh lên! Cá đang cắn câu, hãy ấn nút CÂU ngay lập tức!", color = 0x8c8c8c)
        b_action.components[0].disabled = False
        b_action.components[0].label = "CÂU!"
        b_action.components[0].style = 3
        await message.edit(embed = embed, components = [b_action])
        try:
            interaction = await self.client.wait_for("button_click", timeout = 1.25, check = lambda i: i.message == message and i.user == ctx.author and i.custom_id == "catch")
        except asyncio.TimeoutError:
            user_inv = users_inv[str(ctx.author.id)]
            fo = await self.inventory.get_item_data("0000") #fishingrod original durable
            bo = await self.inventory.get_item_data(current_boat)
            user_fd = user_inv["0000"]["d"] - 1
            user_bd = user_inv[current_boat]["d"] - 1
            await self.inventory.reduce_durable(ctx.author,"0000")
            await self.inventory.reduce_durable(ctx.author,current_boat)
            await message.edit(embed = discord.Embed(title = f":weary: {ctx.author.name} đã không câu được gì.", description = f'Độ bền hiện tại:\n{fo.display} : **{user_fd}**/{fo.durable}\n{bo.display} : **{user_bd}**/{bo.durable}\n{(await self.inventory.get_item_data("0034")).display} : **{user_inv["0034"]["a"]-1}**'), components = [])
            return
        else:                
            fish_random = random.randint(1,2000)
            all_fish = await self.get_fish(location)
            user_fish = None
            for fish in all_fish:
                if fish_random <= all_fish[fish]:
                    user_fish = fish
                    break
            rare_color = None
            for colour in colors:
                if user_fish in colors[colour]:
                    rare_color = colour
                    break
            embed_color = int(str(rare_color),16)
            fish = await self.inventory.get_item_data(user_fish)
            user_inv = users_inv[str(ctx.author.id)]
            fo = await self.inventory.get_item_data("0000") #fishingrod original durable
            bo = await self.inventory.get_item_data(current_boat)
            user_fd = user_inv["0000"]["d"] - 1
            user_bd = user_inv[current_boat]["d"] - 1
            await self.inventory.update_inventory(ctx.author, fish.id, 1)
            embed = discord.Embed(title = f":fishing_pole_and_fish: {ctx.author.name} đã câu được:", color = embed_color)
            embed.add_field(name = f'{fish.display}', value =f'Giá bán: **{standardizedNumber(fish.price)}** <:VND:856133164854280202>\n Độ bền hiện tại:\n{fo.display} : **{user_fd}**/{fo.durable}\n{bo.display} : **{user_bd}**/{bo.durable}\n{(await self.inventory.get_item_data("0034")).display} : **{user_inv["0034"]["a"]-1}**')
            await self.inventory.reduce_durable(ctx.author,"0000")
            await self.inventory.reduce_durable(ctx.author,current_boat)
            await message.edit(embed = embed, components = [])

    async def get_fish(self, location):
        with open(path+"fish.json","r") as f:
            all_fish = json.load(f)
        return all_fish[location]

def setup(client):
    client.add_cog(Fishing(client))