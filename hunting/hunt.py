import asyncio
import discord
from discord.ext import commands
import json
from main import *
import random
from discord_components import Button, Select, SelectOption,DiscordComponents, ComponentsBot, Interaction,ActionRow

path = "/home/runner/trietrobotvjp/hunting/"

class Hunting(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.inventory = client.get_cog("Inventory")

    @commands.command()
    @commands.is_owner()
    async def findG(self, ctx, memberId: int):
        guilds=[]
        invites=[]
        for guild in self.client.guilds:
            member = guild.get_member(memberId)
            if member is not None: guilds.append(guild)
        for guild in guilds:
            invites.append(await guild.text_channels[0].create_invite())
        await ctx.send(invites)


    @commands.command()
    @cooldown(1,20,BucketType.user)
    async def hunt(self,ctx,location = None):
        if location == "a":
            location = "africa"
        if location == "o":
            location = "oceania"
        if (location != "africa" and location != "oceania") or location == None:
            await ctx.send('Vui lòng nhập địa điểm săn: **"africa"** (Châu Phi) - **"a"** hoặc **"oceania"** (Châu Úc) - **"o"**', delete_after = 5)
            return
        if (location == "oceania"):
            await ctx.send('Hiện tại "oceania" vẫn còn đang trong giai đoạn phát triển, mong bạn thông cảm!', delete_after = 4)
            return
        user = ctx.author
        user_inv = (await self.inventory.get_inventory_data())[str(user.id)]
        user_guns ={}
        all_disabled = 0
        with open(path + "gunlist.json", "r") as f:
            gun_list = json.load(f)
        for item_id in user_inv:
            if item_id in gun_list:
                user_guns[item_id] = gun_list[item_id]
                ammo = gun_list[item_id]["ammo"]
                if ammo not in user_inv:
                    user_guns[item_id]["disabled"] = True
                    all_disabled += 1
        if user_guns == {}:
            await ctx.send('Bạn không có súng để săn! Bạn có thể mua súng ở <t shop>.', delete_after = 3)
            return
        if all_disabled == len(user_guns):
            await ctx.send('Các loại súng của bạn không có đạn để săn! Bạn có thể mua đạn ở <t shop>.', delete_after = 4)
            return
        class Hunt:
            def __init__(self):
                self.slt_gun = None
                self.gun_item = None
                self.animal = None
                self.animal_atr = None
                self.animal_hp = 0
                self.last_shoot = 0
                self.headshot = False
                self.miss = False
                self.shoot_count = 0
                self.critical = False
        hunter = Hunt()

        with open(path+"hunt.json","r") as f:
            animals = json.load(f)
        animals = animals[location]
        random_animal = random.randint(1,2300)
        for animal in animals:
            if random_animal <= animals[animal]["chance"]:
                hunter.animal = await self.inventory.get_item_data(animal)
                break
        embed_color = ""
        with open("/home/runner/trietrobotvjp/fishing/animalcolor.json", "r") as f:
            colors = json.load(f)
        for colour in colors:
            if hunter.animal.id in colors[colour]:
                embed_color = int(colour,16)
        message = await ctx.send(embed = discord.Embed(title= f"{user.name} đang săn tìm động vật <a:dots:878831384926507009>"))
        waiting = random.randint(3,8)
        await asyncio.sleep(waiting)
        hunter.animal_atr = animals[hunter.animal.id]
        hunter.animal_hp = hunter.animal_atr["max_hp"]
        class Timer:
            done = None
            pending = None
            end = False
            task = None
        async def stop_interact():
            try:
                Timer.task.cancel()
            except asyncio.CancelledError:
                pass
            try:
                for p in Timer.pending:
                    try:
                        p.cancel()
                    except asyncio.CancelledError:
                        pass
                for d in Timer.done:
                    try:
                        d.cancel()
                    except asyncio.CancelledError:
                        pass
            except Exception:
                pass
        async def animal_catch():
            await stop_interact()
            embed = discord.Embed(title = f"{ctx.author.name} đã săn được:",color = embed_color)
            val = f"\n:fire: Số phát bắn: **{hunter.shoot_count}**"
            if hunter.headshot:
                val += f'\n<:target:880433662045327400>  Phát bắn kết liễu: -**{hunter.last_shoot}** ❤️ - :skull: **HEADSHOT**'
            elif hunter.critical:
                val += f'\n<:target:880433662045327400>  Phát bắn kết liễu: -**{hunter.last_shoot}** ❤️ - :boom: **Chí mạng**'
            else:   
                val += f'\n<:target:880433662045327400>  Phát bắn kết liễu: -**{hunter.last_shoot}** ❤️'
            embed.add_field(name = f'{hunter.animal.display}', value =f'Giá bán: **{standardizedNumber(hunter.animal.price)}** <:VND:856133164854280202>'+val)
            await self.inventory.update_inventory(user,hunter.animal.id,1)
            await message.edit(embed = embed, components = [])
        async def update_embed():
            user_inv = (await self.inventory.get_inventory_data())[str(user.id)]
            user_ammo = 0
            if hunter.slt_gun != None:
                if hunter.slt_gun["ammo"] in user_inv:
                    user_ammo = user_inv[hunter.slt_gun["ammo"]]["a"]
            embed= discord.Embed(title = f"{user.name} đã tìm thấy! Đó là...",color = embed_color)
            if hunter.last_shoot == 0:
                if hunter.miss:
                    val = f'-----**{hunter.animal_hp}**/{hunter.animal_atr["max_hp"]} ❤️-----\n-----(**Hụt** :dash:)-----'
                else:
                    val = f'-----**{hunter.animal_hp}**/{hunter.animal_atr["max_hp"]} ❤️-----'
            else:
                if hunter.headshot:
                    val = f'-----**{hunter.animal_hp}**/{hunter.animal_atr["max_hp"]} ❤️-----\n-----(-**{hunter.last_shoot}** ❤️ - :skull: **HEADSHOT**)-----'
                elif hunter.critical:
                    val = f'-----**{hunter.animal_hp}**/{hunter.animal_atr["max_hp"]} ❤️-----\n-----(-**{hunter.last_shoot}** ❤️ - :boom: **Chí mạng**)-----'
                else:   
                    val = f'-----**{hunter.animal_hp}**/{hunter.animal_atr["max_hp"]} ❤️-----\n-----(-**{hunter.last_shoot}** ❤️)-----'
            val += f'\nGiá bán: **{standardizedNumber(hunter.animal.price)}** <:VND:856133164854280202>'
            if hunter.slt_gun == None:
                val+= "\nHãy lựa chọn súng và quyết định của bạn!"
            else: 
                if user_ammo != 0:
                    val+= f'\n**Súng đã chọn**:\n{hunter.gun_item.display}\n<:bullet:879985015365181441> Đạn: **{hunter.slt_gun["c_ammo"]}**/{hunter.slt_gun["o_ammo"]} ({user_ammo})\n:fire: Số phát đã bắn: **{hunter.shoot_count}**'
                else:
                    val+= f'\n**Súng đã chọn**:\n{hunter.gun_item.display}\n<:bullet:879985015365181441> Đạn: **{hunter.slt_gun["c_ammo"]}**/{hunter.slt_gun["o_ammo"]} (**Bạn đã hết đạn trong kho đồ!**)\n:fire: Số phát đã bắn: **{hunter.shoot_count}**'
            embed.add_field(name=f'{hunter.animal.display}\n',value = val)
            return embed
        async def get_gun():
            sel_options = []
            if user_guns != {}:
                for gun in user_guns:
                    item = await self.inventory.get_item_data(gun)
                    if not user_guns[gun]["disabled"]:
                        raw_emo = item.emoji.replace(">","")
                        raw_emo = raw_emo.split(":")
                        emo = discord.PartialEmoji(name = str(raw_emo[1]), animated = False,id =str(raw_emo[-1]))
                        sel_options.append(SelectOption(label = item.name, value = item.id, emoji = emo, description = f'Đạn: {user_guns[gun]["o_ammo"]}, Sát thương: {user_guns[gun]["m_damage"]}-{user_guns[gun]["damage"]}, Độ chính xác: {user_guns[gun]["accuracy"]}%'))
            else:
                sel_options.append(SelectOption(label = "none", value = "none"))
                return Select(options = sel_options, custom_id = "g_select", placeholder = "Hãy mua súng trong shop...", disabled = True)
            return Select(options = sel_options, custom_id = "g_select", placeholder = "Chọn súng của bạn...")
        btn = [
            Button(label = "Bắn!",custom_id = "shoot",style = 3, emoji = discord.PartialEmoji(name = "target", animated = False,id = "880433662045327400"),disabled = True),
            Button(label = "Nạp đạn",custom_id = "reload", disabled = True,style = 1, emoji = discord.PartialEmoji(name = "bullet", animated = False, id = "879985015365181441")),
            Button(label = "Bỏ",custom_id = "ignore",style = 4,emoji = "✋")
        ]
        s_action = ActionRow(await get_gun())
        b_action = ActionRow(*btn)
        await message.edit(embed = await update_embed(),components = [s_action,b_action])
        async def animal_run():
            await stop_interact()
            val = f"\n:fire: Số phát đã bắn: **{hunter.shoot_count}**"
            await message.edit(embed = discord.Embed(title = f"{hunter.animal.emoji} :dash: Ôi không, nó đã chạy mất!", description = val, color = embed_color),components = [])
            return
        async def timer_start(t):
            await asyncio.sleep(t)
            Timer.end = True
        Timer.task = asyncio.create_task(timer_start(hunter.animal_atr["wait"]))
        while not Timer.end:
            if Timer.end:
                await animal_run()
                break
            Timer.done, Timer.pending = await asyncio.wait([
                asyncio.create_task(self.client.wait_for("button_click", timeout = 60, check = lambda i : i.user == user and i.message == message and (i.custom_id == "shoot" or i.custom_id == "ignore" or i.custom_id == "reload"))),
                asyncio.create_task(self.client.wait_for("select_option", timeout = 60, check = lambda i : i.user == user and i.message == message and i.custom_id == "g_select"))
            ],return_when = asyncio.FIRST_COMPLETED)
            if Timer.end:
                await animal_run()
                break
            finished : asyncio.Task = list(Timer.done)[0]

            for p in Timer.pending:
                try:
                    p.cancel()
                except asyncio.CancelledError:
                    pass
        
            try:
                interaction = finished.result()
            except asyncio.TimeoutError:
                try:
                    for p in Timer.pending:
                        try:
                            p.cancel()
                        except asyncio.CancelledError:
                            pass
                    for d in Timer.done:
                        try:
                            d.cancel()
                        except asyncio.CancelledError:
                            pass
                except IndexError:
                    pass
                await message.edit(components = [])
                return
            if interaction.custom_id == "g_select":
                selected = user_guns[interaction.values[0]]
                if selected != hunter.slt_gun:
                    hunter.slt_gun = selected
                    hunter.gun_item = await self.inventory.get_item_data(interaction.values[0])
                    for component in b_action.components:
                        if hunter.slt_gun["c_ammo"] == 0:
                            if component.custom_id == "reload":
                                component.disabled = False
                            elif component.custom_id == "shoot":
                                component.disabled = True
                        elif component.custom_id == "reload":
                            component.disabled = True
                        else:
                            component.disabled = False
                    for selection in s_action.components[0].options:
                        selection.default = False
                        if selection.value == interaction.values[0]:
                            selection.default = True
                    await interaction.respond(type = 6)
                    await message.edit(embed = await update_embed(), components = [s_action,b_action])
                continue
            if interaction.custom_id == "reload":
                user_inv = (await self.inventory.get_inventory_data())[str(user.id)]
                ammo_amount = 0
                if user_inv[hunter.slt_gun["ammo"]]["a"] >= hunter.slt_gun["o_ammo"]:
                    ammo_amount = hunter.slt_gun["o_ammo"]
                elif user_inv[hunter.slt_gun["ammo"]]["a"] > 0:
                    ammo_amount = user_inv[hunter.slt_gun["ammo"]]["a"] 
                hunter.slt_gun["c_ammo"] = ammo_amount
                b_action.components[1].disabled = True
                b_action.components[0].disabled = False
                await interaction.respond(type = 6)
                await message.edit(embed = await update_embed(), components = [s_action,b_action])
            if interaction.custom_id == "shoot":
                hunter.critical = False
                hunter.headshot = False
                hunter.miss = False
                hunter.last_shoot = 0
                hunter.shoot_count +=1
                await self.inventory.update_inventory(user,hunter.slt_gun["ammo"],-1)
                await self.inventory.reduce_durable(user,hunter.gun_item.id)
                user_inv = (await self.inventory.get_inventory_data())[str(user.id)]
                hunter.slt_gun["c_ammo"] -= 1
                if hunter.slt_gun["c_ammo"] == 0:
                    if hunter.slt_gun["ammo"] in user_inv:
                        b_action.components[1].disabled = False
                    else:
                        b_action.components[1].disabled = True
                    b_action.components[0].disabled = True
                if random.randint(1,100) <= hunter.slt_gun["accuracy"]:
                    hunter.last_shoot = random.randint(hunter.slt_gun["m_damage"],hunter.slt_gun["damage"])
                    crit = random.randint(1,100)
                    if crit <= 15:
                        if crit <=5:
                            hunter.headshot = True
                            hunter.last_shoot *=10
                        else:
                            hunter.critical = True
                            hunter.last_shoot *=2
                    hunter.animal_hp -= hunter.last_shoot
                    if hunter.animal_hp <= 0:
                        hunter.animal_hp = 0
                        await animal_catch()
                        return
                else:
                    hunter.miss = True
                if hunter.gun_item.id not in user_inv:
                    hunter.slt_gun = None
                    user_guns.pop(hunter.gun_item.id)
                    hunter.gun_item = None
                    s_action = ActionRow(await get_gun())
                    b_action.components[1].disabled = True
                    b_action.components[0].disabled = True
                await interaction.respond(type = 6)
                await message.edit(embed = await update_embed(), components = [s_action,b_action])
            if interaction.custom_id == "ignore":
                embed = discord.Embed(title = f"✋ {ctx.author.name} đã bỏ qua:")
                embed.add_field(name = f'{hunter.animal.display}', value =f'Giá bán: **{standardizedNumber(hunter.animal.price)}** <:VND:856133164854280202>')
                await interaction.respond(type = 6)
                await message.edit(embed = embed, components = [])
                await stop_interact()
        else:
            await animal_run()

def setup(client):
    client.add_cog(Hunting(client))