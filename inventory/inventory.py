import asyncio
import discord
from discord.ext import commands
import json
from main import *
from discord_components import Button, Select, SelectOption,DiscordComponents, ComponentsBot, Interaction,ActionRow
from tienlen import Card
import random

path = "/home/runner/trietrobotvjp/inventory/"

class Inventory(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def itemchange(self,ctx,change, user:discord.User):
        if change =="add":
            with open("itemdata.json","r") as f:
                items = json.load(f)
            for item in items:
                await self.update_inventory(user,item,1)
            await ctx.send("Done!")
        elif change =="clear":
            users = await self.get_inventory_data()
            users[str(user.id)] = {}
            await ctx.send("Done!")

    @commands.command()
    @commands.is_owner()
    async def traogiai(self, ctx, target: discord.User = None):
        await self.update_inventory(target, "0061", 1)
        await ctx.send("Thành công")
        return


    @commands.command(aliases=["trd"])
    @cooldown(1,1,BucketType.user)
    async def trade(self, ctx, target : discord.User = None):
        await ctx.send("Lệnh trade đang đóng để nâng cấp!")
    #     if target == ctx.author:
    #         await ctx.send("Bạn không thể trao đổi với chính mình!")
    #         return
    #     class Trade:
    #         def __init__(self, user):
    #             self.user = user
    #             self.items = []
    #             self.message = None
    #             self.in_trade_inv = None
    #     class Item:
    #         def __init__(self,item,amount):
    #             self.item = str(item)
    #             self.amount = int(amount)     
    #     embed = discord.Embed(title = f':busts_in_silhouette: `{ctx.author.name}` muốn trao đổi với `{target.name}`!', color=0x00eeff)
    #     embed.add_field(name = f"{ctx.author.name}:", value = "Trống, chưa thêm vật phẩm nào.")
    #     embed.add_field(name = f"{target.name}:", value = "Trống, chưa thêm vật phẩm nào.")
    #     message = await ctx.send(":watch: Bạn có 30 giây để thêm vật phẩm và trao đổi! Bộ đếm thời gian sẽ khởi động lại khi bạn thêm vật phẩm.", embed = embed)
    #     trd_user = Trade(ctx.author)
    #     tgt_user = Trade(target)     
    #     confirm = False

    #     async def update_embed():
    #         embed = discord.Embed(title = f':busts_in_silhouette: `{ctx.author.name}` muốn trao đổi với `{target.name}`!', color=0x00eeff)
    #         trd_value = ""
    #         if trd_user.items != []:
    #             for item in trd_user.items:
    #                 item_name = await self.get_item_data(item.item,"name")
    #                 item_emoji = await self.get_item_data(item.item,"emoji")
    #                 trd_value+=f"x{item.amount} {item_emoji} **{item_name}#`{item.item}`**\n"
    #             embed.add_field(name = f"{ctx.author.name}:",value = trd_value)
    #         else:
    #             embed.add_field(name = f"{ctx.author.name}:", value = "Trống.")
    #         tgt_value = ""
    #         if tgt_user.items != []:
    #             for item in tgt_user.items:
    #                 item_name = await self.get_item_data(item.item,"name")
    #                 item_emoji = await self.get_item_data(item.item,"emoji")
    #                 tgt_value+=f"x{item.amount} {item_emoji} **{item_name}#`{item.item}`**\n"
    #             embed.add_field(name = f"{target.name}:",value = tgt_value)
    #         else:
    #             embed.add_field(name = f"{target.name}:", value = "Trống.")
    #         return embed

    #     def checkmsg(message):
    #         return message.author == ctx.author and (message.content.startswith("sadd ") or message.content.startswith("tadd ") or message.content.startswith("confirm")) and message.channel == ctx.message.channel
    #     while not confirm:
    #         try:
    #             msg = await self.client.wait_for('message',timeout = 30.0, check=checkmsg)
    #         except asyncio.TimeoutError:
    #             embed = discord.Embed(title = f"Lệnh trao đổi đã bị hủy do quá thời gian chờ!")
    #             await message.edit(embed=embed, delete_after = 5)
    #             return
    #         else:
    #             if msg.content.startswith("sadd "):
    #                 if "=" not in msg.content:
    #                     continue
    #                 items_raw = str(msg.content).replace("sadd ","")
    #                 items_raw = items_raw.replace(" ","")
    #                 items = items_raw.split("/")
    #                 inv = await self.get_inventory_data()
    #                 trd_inv = inv[str(ctx.author.id)]
    #                 trd_user.in_trade_inv = trd_inv
    #                 tgt_user.in_trade_inv = inv[str(target.id)]
    #                 for item in items:
    #                     if "=" not in item:
    #                         items.remove(item)
    #                 await msg.delete()
    #                 for item_raws in items:
    #                     if item_raws == None:
    #                         items.remove(item_raws)
    #                         continue
    #                     item_raw = item_raws.split("=")
    #                     if item_raw[1] == "all":
    #                         item_raw[1] = trd_inv[str(item_raw[0])]
    #                     if item_raw[1] == "-all":
    #                         item_raw[1] = -(trd_inv[str(item_raw[0])])
    #                     item = Item(str(item_raw[0]),int(item_raw[1]))
    #                     item_limit = await self.get_item_data(item.item,"max_amount")
    #                     if item.item not in trd_inv:
    #                         continue
    #                     if item_limit !=0 and item.amount >item_limit:
    #                         item.amount = item_limit
    #                     if item.amount > trd_inv[item.item]:
    #                         item.amount = trd_inv[item.item]
    #                     if trd_user.items != []:
    #                         for a_item in trd_user.items:
    #                             if a_item.item == item.item:
    #                                 if a_item.amount + item.amount <= trd_inv[item.item]:
    #                                     a_item.amount += item.amount
    #                                 else:
    #                                     a_item.amount = trd_inv[item.item]
    #                                 if a_item.amount <= 0:
    #                                     trd_user.items.remove(a_item)
    #                                 break
    #                         else:
    #                             if item.amount > 0:
    #                                 trd_user.items.append(item)
    #                     elif item.amount > 0:
    #                         trd_user.items.append(item)
    #                 await message.edit(embed = await update_embed())                   
    #             elif msg.content.startswith("tadd "):
    #                 if "=" not in msg.content:
    #                     continue
    #                 items_raw = str(msg.content).replace("tadd ","")
    #                 items_raw = items_raw.replace(" ","")
    #                 items = items_raw.split("/")
    #                 inv = await self.get_inventory_data()
    #                 tgt_inv = inv[str(target.id)]
    #                 trd_user.in_trade_inv = inv[str(ctx.author.id)]
    #                 tgt_user.in_trade_inv = tgt_inv
    #                 for item in items:
    #                     if "=" not in item:
    #                         items.remove(item)
    #                 await msg.delete()
    #                 for item_raws in items:
    #                     if item_raws == None:
    #                         items.remove(item_raws)
    #                         continue
    #                     item_raw = item_raws.split("=")
    #                     if item_raw[1] == "all":
    #                         item_raw[1] = tgt_inv[str(item_raw[0])]
    #                     if item_raw[1] == "-all":
    #                         item_raw[1] = -(tgt_inv[str(item_raw[0])])
    #                     item = Item(str(item_raw[0]),int(item_raw[1]))
    #                     item_limit = await self.get_item_data(item.item,"max_amount")
    #                     if item.item not in tgt_inv: 
    #                         continue
    #                     if item_limit !=0 and item.amount >item_limit:
    #                         item.amount = item_limit
    #                     if item.amount > tgt_inv[item.item]:
    #                         item.amount = tgt_inv[item.item]
    #                     if tgt_user.items != []:
    #                         for a_item in tgt_user.items:
    #                             if a_item.item == item.item:
    #                                 if a_item.amount + item.amount <= tgt_inv[item.item]:
    #                                     a_item.amount += item.amount
    #                                 else:
    #                                     a_item.amount = tgt_inv[item.item]
    #                                 if a_item.amount <= 0:
    #                                     tgt_user.items.remove(a_item)
    #                                 break
    #                         else:
    #                             if item.amount > 0:
    #                                 tgt_user.items.append(item)
    #                     elif item.amount > 0:
    #                         tgt_user.items.append(item)
    #                 await message.edit(embed = await update_embed())                  
    #             elif msg.content.startswith("confirm"):
    #                 if trd_user.items == [] and tgt_user.items == []:
    #                     await ctx.send("Không được bỏ trống cả hai ô vật phẩm!", delete_after = 2)
    #                     continue
    #                 confirm = True
    #                 await msg.delete()
    #                 await message.edit(content = "Đã gửi trao đổi!")
    #                 tgt_user.message = await tgt_user.user.send("Bạn có một trao đổi, react ✅ để chấp nhận. Trao đổi sẽ hết hạn sau **3** phút!",embed = await update_embed())
    #                 await tgt_user.message.add_reaction("✅")
    #                 trd_user.message = await trd_user.user.send("Bạn có một trao đổi đang chờ chấp nhận...",embed = await update_embed())
    #                 #wait for fix
    #                 def dmcheck(reaction,user):
    #                     return str(reaction.emoji) == "✅" and user != self.client.user and reaction.message.id == tgt_user.message.id
    #                 try:
    #                     reaction, user = await self.client.wait_for("reaction_add",timeout=180.0,check = dmcheck)
    #                 except asyncio.TimeoutError:
    #                     embed = discord.Embed(title = "Trao đổi đã hết hạn do quá thời gian chờ")
    #                     await tgt_user.message.edit(content ="", embed=embed)
    #                     await trd_user.message.edit(embed = embed)
    #                     await message.edit(content = "", embed = embed)
    #                     return
    #                 else:
    #                     async def cancel_embed():
    #                         embed = discord.Embed(title = "Trao đổi không hợp lệ do vật phẩm trong kho đồ của 1 trong 2 không trùng khớp với trao đổi")
    #                         await tgt_user.message.edit(embed = embed)
    #                         await trd_user.message.edit(embed = embed)
    #                     inv = await self.get_inventory_data()
    #                     tgt_inv = inv[str(tgt_user.user.id)]
    #                     trd_inv = inv[str(trd_user.user.id)]
    #                     if tgt_inv != tgt_user.in_trade_inv or trd_inv != trd_user.in_trade_inv:
    #                         await cancel_embed()
    #                         return
    #                     if trd_user.items != []:
    #                         for item in trd_user.items:
                                 
    #                             await self.update_inventory(trd_user.user,item.item,-item.amount)
    #                             await self.update_inventory(tgt_user.user,item.item,item.amount)
    #                     if tgt_user.items != []:
    #                         for item in tgt_user.items:
    #                                 await self.update_inventory(trd_user.user,item.item,item.amount)
    #                                 await self.update_inventory(tgt_user.user,item.item,-item.amount)  
                        
    #                     embed = discord.Embed(title = ":handshake: Trao đổi thành công!", color =0x3dff6e)
    #                     trd_value = ''
    #                     if trd_user.items != []:
    #                         for item in trd_user.items:
    #                             item_name = await self.get_item_data(item.item,"name")
    #                             item_emoji = await self.get_item_data(item.item,"emoji")
    #                             trd_value+= f"- x**{item.amount}** {item_emoji} **{item_name}#{item.item}**\n"
    #                     if tgt_user.items != []:
    #                         for item in tgt_user.items:
    #                             item_name = await self.get_item_data(item.item,"name")
    #                             item_emoji = await self.get_item_data(item.item,"emoji")
    #                             trd_value+= f"+ x**{item.amount}** {item_emoji} **{item_name}#{item.item}**\n"
    #                     embed.add_field(name = "Nội dung trao đổi:", value = trd_value)
    #                     await trd_user.message.edit(content="", embed=embed)

    #                     embed = discord.Embed(title = ":handshake: Trao đổi thành công!", color =0x3dff6e)
    #                     tgt_value = ''
    #                     if trd_user.items != []:
    #                         for item in trd_user.items:
    #                             item_name = await self.get_item_data(item.item,"name")
    #                             item_emoji = await self.get_item_data(item.item,"emoji")
    #                             tgt_value+= f"+ x**{item.amount}** {item_emoji} **{item_name}#`{item.item}`**\n"
    #                     if tgt_user.items != []:
    #                         for item in tgt_user.items:
    #                             item_name = await self.get_item_data(item.item,"name")
    #                             item_emoji = await self.get_item_data(item.item,"emoji")
    #                             tgt_value+= f"- x**{item.amount}** {item_emoji} **{item_name}#`{item.item}`**\n"
    #                     embed.add_field(name = "Nội dung trao đổi:", value = tgt_value)
    #                     await tgt_user.message.edit(content="", embed=embed)
    #                     embed = discord.Embed(title = ":handshake: Trao đổi thành công!", color =0x3dff6e)
    #                     trd_value = ""
    #                     if trd_user.items != []:
    #                         for item in trd_user.items:
    #                             item_name = await self.get_item_data(item.item,"name")
    #                             item_emoji = await self.get_item_data(item.item,"emoji")
    #                             trd_value+=f"x{item.amount} {item_emoji} **{item_name}#`{item.item}`**\n"
    #                         embed.add_field(name = f"{ctx.author.name}:",value = trd_value)
    #                     else:
    #                         embed.add_field(name = f"{ctx.author.name}:", value = "Trống.")
    #                     tgt_value = ""
    #                     if tgt_user.items != []:
    #                         for item in tgt_user.items:
    #                             item_name = await self.get_item_data(item.item,"name")
    #                             item_emoji = await self.get_item_data(item.item,"emoji")
    #                             tgt_value+=f"x{item.amount} {item_emoji} **{item_name}#`{item.item}`**\n"
    #                         embed.add_field(name = f"{target.name}:",value = tgt_value)
    #                     else:
    #                         embed.add_field(name = f"{target.name}:", value = "Trống.")
    #                     await message.edit(content = "", embed = embed)


    @commands.command(aliases=["mua"])
    @cooldown(1,4,BucketType.user)
    async def buy(self, ctx, item, amount : int = None):
        if item == None: 
           await ctx.send("Vui lòng nhập ID của vật phẩm cần mua, <t shop> để xem các vật phẩm có thể mua!", delete_after = 2)
           return 
        if amount == None: amount = 1
        if amount <=0:
           await ctx.send("Vui lòng nhập số lượng vật phẩm cần mua hợp lệ!", delete_after = 2)
           return 
        user = ctx.author
        await open_account(user)
        await self.open_inventory(user)
        users_money= await get_bank_data()    
        user_money = users_money[str(user.id)]["wallet"]
        with open(path+"shop.json","r") as f:
            shop_raw = json.load(f)
        shop_items = shop_raw["items"]
        if item not in shop_items:
            await ctx.send("Vật phẩm không tồn tại trong cửa hàng!", delete_after = 2)
            return
        item_max_allowed = (await self.get_item_data(item)).limit
        if amount > item_max_allowed and item_max_allowed > 0:
            await ctx.send(f'Vật phẩm bạn định mua chỉ cho phép mua tối đa {item_max_allowed} vật phẩm!', delete_after = 2)
            return
        users_inventory = await self.get_inventory_data()
        if item in users_inventory[str(user.id)]:
            if users_inventory[str(user.id)][item]["a"] == item_max_allowed:
                await ctx.send("Vật phẩm bạn mua đã đạt tới giới hạn số lượng trong kho đồ của bạn!", delete_after = 2)
                return
        item_price = shop_items[item]
        message = await ctx.send("<a:loading:876310730159325194>")
        if user_money >= (item_price*amount):
            await self.update_inventory(user,item,amount)
            await update_bank(user, -(item_price*amount),"wallet")
            item = await self.get_item_data(item)
            await message.edit(content = f'{user.mention} đã mua thành công **{amount}** {item.display} với giá **{standardizedNumber(item_price*amount)} **<:VND:856133164854280202>')
        else:
            await message.edit(content = f"{user.mention} không đủ tiền để mua!", delete_after = 3)
            return

    @commands.command(aliases=["ban"])
    @cooldown(1,4,BucketType.user)
    async def sell(self, ctx, item, amount = None):
        class ItemType:

            def __init__(self, item, amount, price):
                self.item = item
                self.amount = amount
                self.price = price
        
        all_type = await self.get_type_data()
        all_type_keys = list(all_type.keys())
        if item == None: 
           await ctx.send("Vui lòng nhập ID của vật phẩm hoặc loại vật phẩm cần bán, <t kho> để xem các vật phẩm trong kho đồ có thể bán!", delete_after = 2)
           return
        if amount == None: amount = 1
        user = ctx.author
        await open_account(user)
        await self.open_inventory(user)
        users_money= await get_bank_data()    
        user_money = users_money[str(user.id)]["wallet"]
        users_inventory = await self.get_inventory_data()
        user_inv = users_inventory[str(user.id)]
        if amount == "all" and item not in all_type_keys:
            amount = int(user_inv[item]["a"])
        amount = int(amount)
        if item not in all_type_keys:
            if item not in user_inv:
                await ctx.send("Vật phẩm không tồn tại trong kho đồ của bạn!", delete_after = 2)
                return
            if amount > user_inv[item]["a"]:
                await ctx.send(f'Vật phẩm trong kho đồ bạn chỉ tồn tại {user_inv[item]["a"]} vật phẩm!', delete_after = 2)
                return
        else:
            is_have_type = False
            for i in user_inv:
                if (await self.get_item_type(i)).name == item:
                    is_have_type = True
                    break
            if not is_have_type:
                await ctx.send("Loại vật phẩm cần bán không tồn tại trong kho đồ của bạn!", delete_after = 3)
                return 
        message = await ctx.send("<a:loading:876310730159325194>")  
        if item in all_type_keys:
            
            user_c_item = []
            for i in all_type[item]["items"]:
                if i in user_inv:
                    t_i = await self.get_item_data(i)
                    if t_i.durable != None:
                        t_i.price = int(float(t_i.price*(user_inv[t_i.id]["d"]/t_i.durable)))
                    user_c_item.append(ItemType(i,user_inv[i]["a"], t_i.price))
            total_price = 0
            for i in user_c_item:
               await self.update_inventory(user,i.item,-i.amount)
               await update_bank(user, i.price*i.amount,"wallet")
               total_price += (i.price*i.amount)
            await message.edit(content = f"{user.mention} đã bán thành công tất cả vật phẩm **'{item}'** với số tiền **{standardizedNumber(total_price)} <:VND:856133164854280202>**")

        else:     
            item = await self.get_item_data(item)
            if item.durable != None:
                item.price = int(float(item.price*(user_inv[item.id]["d"]/item.durable)))
            await self.update_inventory(user,item.id,-amount)
            await update_bank(user, item.price*amount,"wallet")
            await message.edit(content = f'{user.mention} đã bán thành công {amount} {item.display} với giá **{standardizedNumber(item.price*amount)}** <:VND:856133164854280202>')

    @commands.command(name = "inventory",aliases=["inv","kho"])
    @cooldown(1,10,BucketType.user)
    async def inventory(self, ctx, user : discord.User = None):
        if user == None: user = ctx.author
        await self.open_inventory(user)
        users_inv = await self.get_inventory_data()
        user_inv = users_inv[str(user.id)]
        now_time = datetime.utcnow()
        await open_account(user)       
        if user_inv == {}:
            embed = discord.Embed(title = f":file_cabinet: Kho đồ của **{user.name}**:", color = 0x85ffb4,timestamp=now_time)
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name = "Kho đồ rỗng", value ="Bạn hiện chưa có vật phẩm nào trong kho đồ!")
            await ctx.send(embed = embed)
            return
        message = await ctx.send("<a:loading:876310730159325194>")
        class inventory:
            def __init__(self):
                self.start =0
                self.end = 0
                self.current_page = 0
                self.end_page = 0
                self.user_inv_keys = []
                self.base_end = 0
                self.type_list = {}
                self.current_type = ""
        inventory = inventory()
        inventory.start = 0
        inventory.end = 5
        inventory.current_page = 1
        inventory.end_page = 0
        temp = len(user_inv)
        while temp > 0 or temp > 5:
            temp -=5
            inventory.end_page+=1
        inventory.user_inv_keys = list(user_inv.keys())
        inventory.base_end = inventory.end_page
        async def update_embed(itype):
            d_key = itype
            clr = int("0x85ffb4",16)
            if itype == "all": d_key = "Tất cả vật phẩm"
            else: clr = int((await self.get_type_data())[itype]["color"],16)
            total_price = 0
            for item in inventory.user_inv_keys:
                total_price += (await self.get_item_data(item)).price*user_inv[item]["a"]
            embed = discord.Embed(title = f":file_cabinet: Kho đồ của **{user.name}**:",description = f"Đang hiển thị: **{d_key}**\nTổng giá trị: **{standardizedNumber(total_price)}** {tien_emoji}", color = clr,timestamp=now_time)
            embed.set_thumbnail(url=user.avatar_url)
            embed.set_footer(text=f"Trang {inventory.current_page}/{inventory.end_page}")
            for i in range(inventory.start,inventory.end):
                try:
                    item = await self.get_item_data(inventory.user_inv_keys[i])
                    if item.durable != None:
                        item.price = int(float(item.price*(user_inv[item.id]["d"]/item.durable)))
                    e_value = f"Giá: **{standardizedNumber(item.price)}**  <:VND:856133164854280202>"
                    if itype == "all":
                        if item.limit !=0:
                            e_value+=f"\nLoại: **{item.type.name}** - Giới hạn : **{item.limit}**"
                        else:
                            e_value+=f"\nLoại: **{item.type.name}**"
                    else:
                        if item.limit !=0:
                            e_value+=f"\nGiới hạn : **{item.limit}**"
                    if item.durable != None:
                        e_value+=f'\nĐộ bền : **{user_inv[item.id]["d"]}**/{item.durable}'
                    embed.add_field(name = f'**{user_inv[item.id]["a"]}** {item.display}', value = e_value, inline= False)
                    
                except IndexError:
                    return embed          
            return embed
        inventory.current_type="all"
        await message.edit(content = "", embed = await update_embed(inventory.current_type))
        type_list = []
        for item_raw in user_inv:
            item = await self.get_item_data(item_raw)
            if item.type.name not in type_list:
                type_list.append(item.type.name)
        raw_type = await self.get_type_data()
        temp_list = []
        for t in raw_type:
            for ut in type_list:
                if t == ut:
                    temp_list.append(await self.convert_type(ut)) 
        inventory.type_list = temp_list
        select_options = [SelectOption(label = "Tất cả", value = "all", emoji = "🗄️")]
        for item_type in temp_list:
            select_options.append(SelectOption(label = item_type.name, value =item_type.name, description = item_type.description, emoji = item_type.emoji))
        buttons = [
            Button(label = "˂˂", custom_id = "first", style = 3, disabled = True),
            Button(label = "˂", custom_id = "left", style = 3,disabled = True),
            Button(label = "˃", custom_id = "right", style = 3),
            Button(label = "˃˃", custom_id = "last", style = 3)
        ]
        select =  Select(
                placeholder = "Bộ lọc",
                options = select_options,custom_id = "filter"
            )
        b_action = ActionRow(*buttons)
        s_action = ActionRow(select)
        if inventory.current_page != inventory.end_page:
            await message.edit(components = [s_action,b_action])
   
        def check(i):
            return (i.custom_id == "right" or i.custom_id == "left" or i.custom_id == "first" or i.custom_id == "last" or i.custom_id == "filter") and i.user != self.client.user and (i.user == user or i.user == ctx.author) and i.message.id == message.id

        while inventory.base_end!=1:
            done, pending = await asyncio.wait([
                asyncio.create_task(self.client.wait_for("button_click", timeout = 60, check = check), name = "button"),
                asyncio.create_task(self.client.wait_for("select_option", timeout = 60, check = check),name = "select")
            ],return_when = asyncio.FIRST_COMPLETED)

            finished : asyncio.Task = list(done)[0]

            for p in pending:
                try:
                    p.cancel()
                except asyncio.CancelledError:
                    pass
           
            try:
                interaction = finished.result()
            except asyncio.TimeoutError:
                for p in pending:
                    try:
                        p.cancel()
                    except asyncio.CancelledError:
                        pass
                for d in done:
                    try:
                        d.cancel()
                    except asyncio.CancelledError:
                        pass
                await message.edit(components = [])
                return      
            await interaction.respond(type =6)     
            if finished.get_name() == "button":
                if interaction.custom_id == "right" and inventory.current_page != inventory.end_page:
                    inventory.start += 5
                    inventory.end +=5
                    inventory.current_page+=1
                    if inventory.current_page != inventory.end_page:
                        for button in b_action.components:
                            button.disabled = False
                    else:
                        for button in b_action.components:
                            if button.custom_id =="right" or button.custom_id =="last":
                                button.disabled = True
                            else:
                                button.disabled = False
                    await message.edit(embed = await update_embed(inventory.current_type),components = [s_action,b_action])

                if interaction.custom_id == "left" and inventory.current_page != 1:
                    inventory.start -= 5
                    inventory.end -=5
                    inventory.current_page-=1
                    if inventory.current_page != 1:
                        for button in b_action.components:
                            button.disabled = False
                    else:
                        for button in b_action.components:
                            if button.custom_id =="left" or button.custom_id =="first":
                                button.disabled = True
                            else:
                                button.disabled = False
                    await message.edit(embed = await update_embed(inventory.current_type),components = [s_action,b_action])
                if interaction.custom_id =="first" and inventory.current_page != 1:
                    inventory.start =0
                    inventory.end =5
                    inventory.current_page=1              
                    for button in b_action.components:
                        if button.custom_id =="left" or button.custom_id =="first":
                            button.disabled = True
                        else:
                            button.disabled = False
                    await message.edit(embed = await update_embed(inventory.current_type),components = [s_action,b_action])
                if interaction.custom_id =="last" and inventory.current_page != inventory.end_page:
                    inventory.start = -5
                    inventory.end = 0
                    for i in range(0, inventory.end_page):
                        inventory.start += 5
                        inventory.end +=5
                    inventory.current_page= inventory.end_page
                    for button in b_action.components:
                        if button.custom_id =="right" or button.custom_id =="last":
                            button.disabled = True
                        else:
                            button.disabled = False
                    await message.edit(embed = await update_embed(inventory.current_type),components = [s_action,b_action])
            else:
                itype = str(interaction.values[0])
                inventory.current_type = itype
                if itype =="all":
                    inventory.start = 0
                    inventory.end = 5
                    inventory.current_page = 1
                    inventory.end_page = 0
                    temp = len(user_inv)
                    while temp > 0 or temp > 5:
                        temp -=5
                        inventory.end_page+=1
                    inventory.user_inv_keys = list(user_inv.keys())
                elif itype != None:
                    item_list = {}
                    for item_raw in user_inv:
                        item = await self.get_item_data(item_raw)
                        if item.type.name == itype:
                            item_list[item.id] = user_inv[item.id]
                    inventory.start = 0
                    inventory.end = 5
                    inventory.current_page = 1
                    inventory.end_page = 0
                    temp = len(item_list)
                    while temp > 0 or temp > 5:
                        temp -=5
                        inventory.end_page+=1
                    
                    inventory.user_inv_keys = list(item_list.keys())
                if inventory.end_page != 1:
                    for option in s_action.components[0].options:
                        option.default = False
                        if option.value == interaction.values[0]:
                            option.default = True
                    for button in b_action.components:
                        if button.custom_id =="left" or button.custom_id =="first":
                            button.disabled = True
                        else:
                            button.disabled = False
                    await message.edit(embed = await update_embed(inventory.current_type),components = [s_action,b_action])           
                else:
                    for option in s_action.components[0].options:
                        option.default = False
                        if option.value == interaction.values[0]:
                            option.default = True
                    for button in b_action.components:
                        button.disabled = True
                    await message.edit(embed = await update_embed(inventory.current_type),components = [s_action,b_action])    
                           
                    


    @commands.command()
    @cooldown(1,4,BucketType.user)
    async def shop(self,ctx):
        user = ctx.author
        now_time = datetime.utcnow()  
        message = await ctx.send("<a:loading:876310730159325194>")
        with open(path+"shop.json","r") as f:
            raw_shop = json.load(f)
        class shop:
            def __init__(self):
                self.items = None
                self.start =0
                self.end = 0
                self.current_page = 0
                self.end_page = 0
                self.current_keys = []
                self.type_list = {}
                self.current_type = ""
                self.current_stype = ""
        shop = shop()
        shop.start = 0
        shop.end = 5
        shop.current_page = 1
        shop.end_page = 0
        shop.items = raw_shop["items"]
        temp = len(shop.items)
        while temp > 0 or temp > 5:
            temp -=5
            shop.end_page+=1
        shop.current_keys = list(shop.items.keys())
        async def update_embed(itype):
            d_key = itype
            clr = int("0x6a87f0",16)
            if itype == "all": d_key = "Tất cả vật phẩm"
            else: clr = int((await self.get_type_data())[itype]["color"],16)
            embed = discord.Embed(title = f":shopping_cart: Shop",description = f"Đang hiển thị: **{d_key}**", color = clr,timestamp=now_time)
            embed.set_footer(text=f"Trang {shop.current_page}/{shop.end_page}")
            for i in range(shop.start,shop.end):
                try:
                    item = await self.get_item_data(shop.current_keys[i])
                    e_value = f"Giá: **{standardizedNumber(shop.items[item.id])}**  <:VND:856133164854280202>"
                    if itype == "all":
                        if item.limit !=0:
                            e_value+=f"\nLoại: **{item.type.name}** - Giới hạn : **{item.limit}**"
                        else:
                            e_value+=f"\nLoại: **{item.type.name}**"
                    else:
                        if item.limit !=0:
                            e_value+=f"\nGiới hạn : **{item.limit}**"
                    if item.durable != None:
                        e_value+=f'\nĐộ bền : **{item.durable}**'
                    embed.add_field(name = f'{item.display}', value = e_value, inline= False)
                    
                except IndexError:
                    return embed          
            return embed
        shop.current_type="all"
        await message.edit(content = "", embed = await update_embed(shop.current_type))
        type_list = []
        for item_raw in shop.items:
            item = await self.get_item_data(item_raw)
            if item.type.name not in type_list:
                type_list.append(item.type.name)
        raw_type = await self.get_type_data()
        temp_list = []
        for t in raw_type:
            for ut in type_list:
                if t == ut:
                    temp_list.append(await self.convert_type(ut)) 
        shop.type_list = temp_list
        select_options = [SelectOption(label = "Tất cả", value = "all", emoji = "🛒")]
        for item_type in temp_list:
            select_options.append(SelectOption(label = item_type.name, value =item_type.name, description = item_type.description, emoji = item_type.emoji))
        buttons = [
            Button(label = "˂˂", custom_id = "first", style = 1, disabled = True),
            Button(label = "˂", custom_id = "left", style = 1,disabled = True),
            Button(label = "˃", custom_id = "right", style = 1),
            Button(label = "˃˃", custom_id = "last", style = 1)
        ]
        select =  Select(
                placeholder = "Bộ lọc",
                options = select_options,custom_id = "filter"
            )
        b_action = ActionRow(*buttons)
        s_action = ActionRow(select)
        await message.edit(components = [s_action,b_action])
   
        def check(i):
            return (i.custom_id == "right" or i.custom_id == "left" or i.custom_id == "first" or i.custom_id == "last" or i.custom_id == "filter") and i.user != self.client.user and i.user == ctx.author and i.message.id == message.id

        while True:
            done, pending = await asyncio.wait([
                asyncio.create_task(self.client.wait_for("button_click", timeout = 60, check = check), name = "s_button"),
                asyncio.create_task(self.client.wait_for("select_option", timeout = 60, check = check),name = "s_select")
            ],return_when = asyncio.FIRST_COMPLETED)

            finished : asyncio.Task = list(done)[0]

            for p in pending:
                try:
                    p.cancel()
                except asyncio.CancelledError:
                    pass
           
            try:
                interaction = finished.result()
            except asyncio.TimeoutError:
                try:
                    for p in pending:
                        try:
                            p.cancel()
                        except asyncio.CancelledError:
                            pass
                    for d in done:
                        try:
                            d.cancel()
                        except asyncio.CancelledError:
                            pass
                except IndexError:
                    pass
                await message.edit(components = [])
                return      
            await interaction.respond(type =6)     
            if finished.get_name() == "s_button":
                if interaction.custom_id == "right" and shop.current_page != shop.end_page:
                    shop.start += 5
                    shop.end +=5
                    shop.current_page+=1
                    if shop.current_page != shop.end_page:
                        for button in b_action.components:
                            button.disabled = False
                    else:
                        for button in b_action.components:
                            if button.custom_id =="right" or button.custom_id =="last":
                                button.disabled = True
                            else:
                                button.disabled = False
                    await message.edit(embed = await update_embed(shop.current_type),components = [s_action,b_action])

                if interaction.custom_id == "left" and shop.current_page != 1:
                    shop.start -= 5
                    shop.end -=5
                    shop.current_page-=1
                    if shop.current_page != 1:
                        for button in b_action.components:
                            button.disabled = False
                    else:
                        for button in b_action.components:
                            if button.custom_id =="left" or button.custom_id =="first":
                                button.disabled = True
                            else:
                                button.disabled = False
                    await message.edit(embed = await update_embed(shop.current_type),components = [s_action,b_action])
                if interaction.custom_id =="first" and shop.current_page != 1:
                    shop.start =0
                    shop.end =5
                    shop.current_page=1              
                    for button in b_action.components:
                        if button.custom_id =="left" or button.custom_id =="first":
                            button.disabled = True
                        else:
                            button.disabled = False
                    await message.edit(embed = await update_embed(shop.current_type),components = [s_action,b_action])
                if interaction.custom_id =="last" and shop.current_page != shop.end_page:
                    shop.start = -5
                    shop.end = 0
                    for i in range(0, shop.end_page):
                        shop.start += 5
                        shop.end +=5
                    shop.current_page= shop.end_page
                    for button in b_action.components:
                        if button.custom_id =="right" or button.custom_id =="last":
                            button.disabled = True
                        else:
                            button.disabled = False
                    await message.edit(embed = await update_embed(shop.current_type),components = [s_action,b_action])
            elif interaction.custom_id == "filter":
                itype = str(interaction.values[0])
                shop.current_type = itype
                if itype =="all":
                    shop.start = 0
                    shop.end = 5
                    shop.current_page = 1
                    shop.end_page = 0
                    temp = len(shop.items)
                    while temp > 0 or temp > 5:
                        temp -=5
                        shop.end_page+=1
                    shop.current_keys = list(shop.items.keys())
                elif itype != None:
                    item_list = {}
                    for item_raw in shop.items:
                        item = await self.get_item_data(item_raw)
                        if item.type.name == itype:
                            item_list[item.id] = shop.items[item.id]
                    shop.start = 0
                    shop.end = 5
                    shop.current_page = 1
                    shop.end_page = 0
                    temp = len(item_list)
                    while temp > 0 or temp > 5:
                        temp -=5
                        shop.end_page+=1
                    
                    shop.current_keys = list(item_list.keys())
                if shop.end_page != 1:
                    for option in s_action.components[0].options:
                        option.default = False
                        if option.value == interaction.values[0]:
                            option.default = True
                    for button in b_action.components:
                        if button.custom_id =="left" or button.custom_id =="first":
                            button.disabled = True
                        else:
                            button.disabled = False
                    await message.edit(embed = await update_embed(shop.current_type),components = [s_action,b_action])           
                else:
                    for option in s_action.components[0].options:
                        option.default = False
                        if option.value == interaction.values[0]:
                            option.default = True
                    for button in b_action.components:
                        button.disabled = True
                    await message.edit(embed = await update_embed(shop.current_type),components = [s_action,b_action])
                
        
    async def get_inventory_data(self):
        
        return db["inventorydata"]

    async def open_inventory(self, user):

        if str(user.id) in db["inventorydata"]:
            return False
        else:
            db["inventorydata"][str(user.id)] = {}
        return True

    async def update_inventory(self, user : discord.User, item : str, amount : int):
        if item not in db["inventorydata"][str(user.id)]:
            db["inventorydata"][str(user.id)][item] = {}
            db["inventorydata"][str(user.id)][item]["a"] = 0
        db["inventorydata"][str(user.id)][item]["a"] += amount
        if db["inventorydata"][str(user.id)][item]["a"]<=0:
            db["inventorydata"][str(user.id)].pop(item)
        else:
            await self.generate_durable(user,item)
        

    async def get_item_data(self, item:str):
        with open("itemdata.json","r") as f:
            items = json.load(f)
        class Item:
            def __init__(self,id):
                self.id = id
                self.name = items[item]["name"]
                self.emoji = items[item]["emoji"]
                self.price = items[item]["price"]
                self.limit = items[item]["max_amount"]
                self.useable = items[item]["useable"]
                self.type = None
                self.display = f'{items[item]["emoji"]} **{items[item]["name"]}**#`{item}`'
                self.durable = None
                if "durable" in items[item]:
                    self.durable = items[item]["durable"]
        new_item = Item(item)
        new_item.type = await self.get_item_type(item)
        return new_item

    async def convert_type(self,itype):
        items_type = await self.get_type_data()
        class ItemType:
            def __init__(self,items_type,item_type):
                self.name = item_type
                self.subtypes = None
                if "subtypes" in items_type[item_type]:
                    self.subtypes = []
                self.description = items_type[item_type]["description"]
                self.emoji = None
                self.items = items_type[item_type]["items"]
        main_type = ItemType(items_type,itype)
        main_type.emoji = await self.get_type_emoji(itype)
        if main_type.subtypes ==[]:
            subtypes = items_type[itype]["subtypes"]
            for item_type in subtypes:
                main_type.subtypes.append(ItemType(items_type[itype]["subtypes"],item_type))
        return main_type

    async def get_item_type(self,item):
        items_type = await self.get_type_data()                
        for types in items_type:
            if item in items_type[types]["items"]:
                return await self.convert_type(types)
    
    async def get_type_data(self):
        with open("itemtype.json","r")as f:
            items_type = json.load(f)
        return items_type
    
    async def get_type_emoji(self, etype):
        with open("itemtype.json","r")as f:
            items_type = json.load(f)
        if type(items_type[etype]["emoji"]) is str:
            return items_type[etype]["emoji"]
        return discord.PartialEmoji(name = items_type[etype]["emoji"]["name"], animated = items_type[etype]["emoji"]["animated"], id = items_type[etype]["emoji"]["id"])

    async def generate_durable(self,user,item):
        i = await self.get_item_data(item)
        user_inv = db["inventorydata"][str(user.id)]
        user_item = user_inv[item]
        if (i.durable == None) or (item not in user_inv) or ("d" in user_item and user_inv[item]["d"]<=i.durable):
            return False
        db["inventorydata"][str(user.id)][item]["d"] = i.durable
        return True

    async def reduce_durable(self,user,item):
        await self.generate_durable(user,item)
        db["inventorydata"][str(user.id)][item]["d"] -= 1
        if db["inventorydata"][str(user.id)][item]["d"] == 0:
            await self.update_inventory(user,item,-1)

def setup(client):
    client.add_cog(Inventory(client))