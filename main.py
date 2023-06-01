import discord
from discord.ext import commands
import json
import os
import random
import time
from discord.ext.commands import BucketType, CommandOnCooldown, cooldown, Cog, command, has_permissions, MissingPermissions, CommandNotFound
import asyncio
import sys
import time
from random import choice
from playingcardsGame import *
from tienlen import Card
from webserver import keep_alive
import operator
from datetime import date, datetime
from replit import db
from discord_components import Button, Select, SelectOption, DiscordComponents, ComponentsBot, ActionRow

activity = discord.Activity(type=discord.ActivityType.listening,
                            name=f"t help")
tien_emoji = "<:VND:856133164854280202>"
prefixes = ['t ', 'T ', 'triet ', 'Triet ', 't', 'T', 'triet', 'Triet']
intents = discord.Intents.default()
intents.members = True
client = ComponentsBot(command_prefix=prefixes,
                       help_command=None,
                       activity=activity,
                       intents=intents)
print(os.getenv("REPLIT_DB_URL"))


@client.event
async def on_guild_join(guild):
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=f"t help in {len(list(client.guilds))} servers!"))
    data = ""
    rawData = ""
    with open("guilds.txt", "r") as f:
        rawData = f.read()
        data = rawData.replace('\n', '')
    with open("guilds.txt", "w") as f:
        for l in client.guilds:
            if f"{l.id}" in data: continue
            try:
                rawData += f" {l.id} {l.name} {await l.voice_channels[0].create_invite(xkcd=True, max_age = 0, max_uses = 0)}\n"
            except Exception:
                pass
        f.writelines(
                   rawData 
                )


@client.event
async def on_guild_remove(guild):
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=f"t help in {len(list(client.guilds))} servers!"))
    data = ""
    rawData = ""
    with open("guilds.txt", "r") as f:
        rawData = f.read()
        data = rawData.replace('\n', '')
    with open("guilds.txt", "w") as f:
        for l in client.guilds:
            if f"{l.id}" in data: continue
            try:
                rawData += f" {l.id} {l.name} {await l.voice_channels[0].create_invite(xkcd=True, max_age = 0, max_uses = 0)}\n"
            except Exception:
                pass
        f.writelines(
                   rawData 
                )


@client.command()
@commands.is_owner()
async def changemoney(ctx, user: discord.User, amount: int):
    await update_bank(user, amount, "wallet")
    await ctx.send("SUCCESS")


@client.command()
@cooldown(1, 60, BucketType.user)
async def reportbug(ctx):
    message = ctx.message.content
    channel = client.get_channel(877053900451119164)
    guild = ctx.channel.guild
    await ctx.send(
        "Cảm ơn bạn đã report bug cho chúng tôi, chúng tôi sẽ xem sét sửa trong thời gian sớm nhất!"
    )
    await channel.send(
        f"({guild.name}){ctx.author.name}:{ctx.author.id}: '{message}'")


@client.command()
@cooldown(1, 3600, BucketType.user)
async def invite(ctx):
    embed = discord.Embed(title="Link mời Bot (invite):", color=0xff00bb)
    embed.set_author(
        name="[t] TrietRoBotVjp",
        icon_url=
        "https://cdn.discordapp.com/avatars/769097658572472320/3e8db955df725750b128a1ef610c6d38.png?size=1024"
    )
    embed.add_field(
        name=
        "https://discord.com/api/oauth2/authorize?client_id=769097658572472320&permissions=8192&scope=bot",
        value=
        "*Bot cần quyền Manage Messages (Quản lý tin nhắn) để hoạt động bình thường và người mời phải có quyền Manage Server (Quản lý server) để mời bot.",
        inline=False)
    await ctx.send(embed=embed)


@client.command(aliases=['ldb', "top"])
@cooldown(1, 12, BucketType.user)
async def leaderboard(ctx):
    class userData:
        def __init__(self, user, cash, inv, money):
            self.user = user
            self.money = money
            self.cash = cash
            self.inv = inv

    def get_money(user):
        return user.money

    message = await ctx.send("<a:loading:876310730159325194>")
    guild = ctx.channel.guild
    users = await get_bank_data()
    user_list = []
    inventory = client.get_cog("Inventory")
    users_inv = await inventory.get_inventory_data()
    for user in users:
        if guild.get_member(int(user)) is not None and guild.get_member(
                int(user)) != client.user and user != "514326308914855937":
            await inventory.open_inventory(guild.get_member(int(user)))
            user_inv = users_inv[str(user)]
            total_inv = 0
            if user_inv != {}:
                for item in user_inv:
                    i = await inventory.get_item_data(item)
                    total_inv += i.price * user_inv[item]["a"]
            cash = users[user]["wallet"] + users[user]["bank"]
            money = cash + total_inv
            user_list.append(
                userData(guild.get_member(int(user)), cash, total_inv, money))
    sorted_user_list = sorted(user_list, key=get_money, reverse=True)
    embed = discord.Embed(
        title=f":moneybag: Top những người giàu nhất **{guild.name}**",
        color=0xfff129)
    ranks = [":one:", ":two:", ":three:", ":four:", ":five:"]
    try:
        for i in range(0, 5):
            embed.add_field(
                name=f"{ranks[i]}: {sorted_user_list[i].user.name}",
                value=
                f":moneybag: : **{standardizedNumber(sorted_user_list[i].cash)}** <:VND:856133164854280202>\n:file_cabinet: : **{standardizedNumber(sorted_user_list[i].inv)}** <:VND:856133164854280202>\nTổng: **{standardizedNumber(sorted_user_list[i].money)}**  <:VND:856133164854280202>",
                inline=False)
    except IndexError:
        pass
    await message.edit(content="", embed=embed)


def standardizedNumber(n):
    int_n = n
    if n < 0:
        n = -n
    n = str(n)
    temp = ''
    final = ''
    n = n[::-1]
    for i in range(0, len(n)):
        temp += n[i]
        final += n[i]
        if len(temp) == 3:
            final += ','
            temp = ''
    final = final[::-1]
    if final[0] == ',':
        final = final.replace(final[0], '', 1)
    if int_n < 0:
        return "-" + final
    else:
        return final


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = (
            f':hourglass: Bình tĩnh nào {ctx.author.mention}, ' +
            "vui lòng thử lại sau **{:.2f}** giây.".format(error.retry_after)
        )  #says the time
        await ctx.send(msg, delete_after=2)
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            'Bot không đủ quyền để thực hiện thao tác, hãy đảm bảo rằng bạn đã cấp cho bot các quyền sau: "**Manage Messages**", "**Read Message History**" và "Send Messages".'
        )
        return
    if isinstance(error, commands.CommandNotFound):
        return
    print(error, ctx.author, ctx.channel.guild, ctx.channel)


@client.command(aliases=['tlmn'])
@cooldown(1, 10, BucketType.user)
async def tienlen(ctx, player_amount: int = None, money_amount: int = None):

    if player_amount not in range(2, 5):
        await ctx.send("**Vui lòng nhập số người chơi hợp lệ! (2-4)**",
                       delete_after=2)
        return

    if player_amount == None:
        await ctx.send(
            f'Này {ctx.author.mention}, Vui lòng nhập số người chơi.',
            delete_after=2)
        return

    if money_amount == None:
        await ctx.send(
            f'Này {ctx.author.mention}, Vui lòng nhập số tiền cược.',
            delete_after=2)
        return

    async def check_money(user):
        await open_account(user)
        users = await get_bank_data()
        wallet_amt = (users[str(user.id)]["wallet"])

        if money_amount > wallet_amt:
            await ctx.send(f'Này {user.mention}, Bạn không đủ tiền để cược!',
                           delete_after=2)
            return False
        if money_amount > 250000:
            await ctx.send(
                f'Này {user.mention}, Không được cược quá **250,000** <:VND:856133164854280202>!',
                delete_after=2)
            return False
        if money_amount < 1:
            await ctx.send(
                f'Này {user.mention}, Vui lòng nhập số tiền hợp lệ!',
                delete_after=2)
            return False
        return True

    if not (await check_money(ctx.author)):
        return

    main = Card("main")

    main.playerList = []

    main.playerList.append(ctx.author)
    currentPlayers = 1

    embed = discord.Embed(
        title=
        f'<:cardsBack:856065118508548107> Set kèo Bài tiến lên! <:cardsBack:856065118508548107>',
        color=0x14e4ff)
    embed.add_field(
        name=f':satellite: Người ra kèo: **{ctx.author.name}**',
        value=
        f':moneybag: Số tiền là: **{standardizedNumber(money_amount)}** <:VND:856133164854280202>\n:bust_in_silhouette: Số lượng người chơi : **{player_amount}**\nĐể tham gia ván bài, hãy ấn nút **Tham gia** trong vòng 30 giây',
        inline=False)
    val = f'{ctx.author.name}\n'
    embed.add_field(name=f'Danh sách người chơi:', value=val, inline=True)
    message = await ctx.send(
        embed=embed,
        components=[Button(label="Tham gia", style=3, custom_id="join")])

    def check(i):
        return i.user not in main.playerList and i.user != client.user and i.custom_id == 'join' and i.message.id == message.id

    while currentPlayers < player_amount:
        try:
            interaction = await client.wait_for('button_click',
                                                timeout=30.0,
                                                check=check)
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title=
                'Ván bài đã bị hủy do quá thời gian chờ và không đủ số lượng người chơi!'
            )
            await message.edit(embed=embed,
                               components=[
                                   Button(label="Tham gia",
                                          style=2,
                                          custom_id="join",
                                          disabled=True)
                               ])
            await message.clear_reactions()
            return
        else:
            await interaction.respond(type=6)
            if (await check_money(interaction.user)):
                val += f"{interaction.user.name}\n"
                embed.set_field_at(1,
                                   name="Danh sách người chơi:",
                                   value=val,
                                   inline=True)
                await message.edit(embed=embed)
                main.playerList.append(interaction.user)
            if (len(main.playerList) == player_amount):
                main.matchEnd = False
                await message.clear_reactions()
                main.onTable_cards = []

                #Khi da du so nguoi choi, van bai se bat dau o day
                await message.edit(
                    content=
                    "Đã đủ số lượng người chơi, đang bắt đầu ván bài...",
                    embed=embed,
                    components=[])

                #turn player into Card class object
                for i in range(0, len(main.playerList)):
                    main.playerList[i] = Card(main.playerList[i])

                main.starter_cards = Card.getShuffleCards()

                #add cards
                for i in range(0, 13):
                    for player in main.playerList:
                        player.cards.append(main.starter_cards[0])
                        main.starter_cards.remove(main.starter_cards[0])

                #sort cards
                for player in main.playerList:
                    player.cards = Card.getSortedCards(player.cards)
                    player.original_cards = player.cards.copy()

                #send cards to DM
                for player in main.playerList:
                    player.outside_message = await player.user.send("...")
                    await player.outside_message.edit(content=message.content,
                                                      embed=embed)
                    player.temp = await player.user.send("Đây là bài của bạn:")
                    cardMessage = "".join(card for card in player.cards)
                    player.DMmessage = await player.user.send(cardMessage)

                #ai co 3 bich hoac la nho nhat danh truoc
                min_value_card = '<:2co:856067108319002625>'
                for player in main.playerList:
                    for card in player.cards:
                        if Card.getRealValue(card) < Card.getRealValue(
                                min_value_card):
                            min_value_card = card

                for i in range(0, len(main.playerList)):
                    if min_value_card in main.playerList[i].cards:
                        main.playerList[i].turn = True
                        if i != 0:
                            main.playerList[0], main.playerList[
                                i] = main.playerList[i], main.playerList[0]

                Instant_Win_Message = ""
                #check toi trang
                for player in main.playerList:
                    card_sum = 0
                    for card in player.cards[:-5:-1]:
                        card_sum += Card.getIntValue(card)
                    if card_sum == 48:
                        main.instant_win_player = player
                        Instant_Win_Message = "Tứ Quý 2"
                        break
                    else:
                        for i in range(1, len(player.cards), 2):
                            if Card.getType([
                                    player.cards[i - 1], player.cards[i]
                            ]) != "Doi":
                                break
                        else:
                            main.instant_win_player = player
                            Instant_Win_Message = "6 đôi"
                            break
                        for i in range(0, len(player.cards)):
                            try:
                                card = Card.getIntValue(player.cards[i])
                                next_card = Card.getIntValue(player.cards[i +
                                                                          1])
                                if next_card - card != 1:
                                    break
                            except IndexError:
                                main.instant_win_player = player
                                Instant_Win_Message = "Sảnh rồng"
                                break

                if main.instant_win_player != None:
                    embed = discord.Embed(title="Ván bài đã kết thúc",
                                          color=0xff0000)
                    embed.add_field(
                        name=f"**{main.instant_win_player.user.name}**",
                        value=
                        f":one:\n+**{standardizedNumber(money_amount*(player_amount-1))}** <:VND:856133164854280202>"
                    )
                    await update_bank(main.instant_win_player.user,
                                      money_amount * (player_amount - 1),
                                      "wallet")
                    for player in main.playerList:
                        if player != main.instant_win_player:
                            embed.add_field(
                                name=f"**{player.user.name}**",
                                value=
                                f":two:\n**{standardizedNumber(-money_amount)}** <:VND:856133164854280202>"
                            )
                            await update_bank(player.user, -money_amount,
                                              "wallet")
                    embed.add_field(
                        name=
                        f"**{main.instant_win_player.user.name}** đã tới trắng!",
                        value=f"Do sở hữu **{Instant_Win_Message}**!",
                        inline=False)
                    card_message = "".join(
                        card for card in main.instant_win_player.cards)
                    await message.edit(content=card_message, embed=embed)
                    for player in main.playerList:
                        await player.DMmessage.delete()
                        await player.temp.delete()
                        await player.outside_message.edit(content=card_message,
                                                          embed=embed)
                    return

                async def update_embed():
                    if len(main.winners) != player_amount:
                        embed = discord.Embed(title="Ván bài đang diễn ra...",
                                              color=0x29ff1a)
                    else:
                        embed = discord.Embed(title="Ván bài đã kết thúc",
                                              color=0xff0000)
                        for winner in main.winners:
                            await update_bank(winner.user, winner.money,
                                              "wallet")
                            await update_bank(winner.user, winner.bonus_money,
                                              "wallet")
                    if main.winners != []:
                        for winner in main.winners:
                            if winner.money >= 0:
                                if winner.bonus_money > 0:
                                    embed.add_field(
                                        name=f"**{winner.user.name}**",
                                        value=
                                        f"{winner.rank}\n+**{standardizedNumber(winner.money)}** <:VND:856133164854280202>\n+**{standardizedNumber(int(winner.bonus_money))}** <:VND:856133164854280202>"
                                    )
                                elif winner.bonus_money < 0:
                                    embed.add_field(
                                        name=f"**{winner.user.name}**",
                                        value=
                                        f"{winner.rank}\n+**{standardizedNumber(winner.money)}** <:VND:856133164854280202>\n**{standardizedNumber(int(winner.bonus_money))}** <:VND:856133164854280202> ({winner.bonus_message})"
                                    )
                                else:
                                    embed.add_field(
                                        name=f"**{winner.user.name}**",
                                        value=
                                        f"{winner.rank}\n+**{standardizedNumber(winner.money)}** <:VND:856133164854280202>"
                                    )
                            else:
                                if winner.bonus_money > 0:
                                    embed.add_field(
                                        name=f"**{winner.user.name}**",
                                        value=
                                        f"{winner.rank}\n**{standardizedNumber(winner.money)}** <:VND:856133164854280202>\n+**{standardizedNumber(int(winner.bonus_money))}** <:VND:856133164854280202>"
                                    )
                                elif winner.bonus_money < 0:
                                    embed.add_field(
                                        name=f"**{winner.user.name}**",
                                        value=
                                        f"{winner.rank}\n**{standardizedNumber(winner.money)}** <:VND:856133164854280202>\n**{standardizedNumber(int(winner.bonus_money))}** <:VND:856133164854280202> ({winner.bonus_message})"
                                    )
                                else:
                                    embed.add_field(
                                        name=f"**{winner.user.name}**",
                                        value=
                                        f"{winner.rank}\n**{standardizedNumber(winner.money)}** <:VND:856133164854280202>"
                                    )
                    if main.playerList != []:
                        for player in main.playerList:
                            if player.skipped:
                                embed.add_field(
                                    name=player.user.name,
                                    value=
                                    f"❌\n<:cardsBack:856065118508548107>x{len(player.cards)}"
                                )
                            elif player.turn:
                                embed.add_field(
                                    name=player.user.name,
                                    value=
                                    f"✅\n<:cardsBack:856065118508548107>x{len(player.cards)}"
                                )
                            else:
                                embed.add_field(
                                    name=player.user.name,
                                    value=
                                    f":clock9:\n<:cardsBack:856065118508548107>x{len(player.cards)}"
                                )
                        if main.onTable_cards != []:
                            for player in main.playerList:
                                if main.onTable_cards[
                                        0] in player.original_cards:
                                    embed.add_field(
                                        name="Bài vừa đánh:",
                                        value=
                                        f"Người đánh: **{player.user.name}**, x**{len(main.onTable_cards)}**<:cardsBack:856065118508548107>",
                                        inline=False)
                            for winner in main.winners:
                                if main.onTable_cards[
                                        0] in winner.original_cards:
                                    embed.add_field(
                                        name="Bài vừa đánh:",
                                        value=
                                        f"Người đánh: **{winner.user.name}**, x**{len(main.onTable_cards)}**<:cardsBack:856065118508548107>",
                                        inline=False)
                    return embed

                async def update_cards(player: Card, selected_cards):
                    if selected_cards != []:
                        for card in selected_cards:
                            player.cards.remove(card)

                    await player.DMmessage.delete()
                    if player.cards != []:
                        cardMessage = "".join(card for card in player.cards)
                        player.DMmessage = await player.user.send(
                            cardMessage, components=[])

                        if main.check_point != None:
                            isAllSkip = 0

                            for otherplayer in main.playerList:
                                if otherplayer.skipped: isAllSkip += 1

                            if isAllSkip == len(main.playerList):
                                main.onTable_cards.clear()
                                for otherplayer in main.playerList:
                                    if otherplayer != main.check_point:
                                        otherplayer.skipped = True
                                main.check_point.skipped = False
                                main.check_point = None

                        nextTurn()
                    else:

                        main.winners.append(player)
                        main.check_point = nextTurn()
                        main.playerList.remove(player)
                        player.rank = main.ranks[main.winners.index(player)]
                        player.money = Card.getRankMoney(
                            player.rank, player_amount, money_amount)
                        await player.temp.delete()
                        await player.outside_message.edit(content=" ",
                                                          embed=await
                                                          update_embed())

                        if len(main.playerList) == (player_amount - 1):
                            check_full_cards = 0
                            for otherplayer in main.playerList:
                                if len(otherplayer.cards) == 13:
                                    check_full_cards += 1
                                else:
                                    break
                            if check_full_cards == (player_amount - 1):
                                main.matchEnd = True
                                embed = discord.Embed(
                                    title="Ván bài đã kết thúc",
                                    color=0xff0000)
                                embed.add_field(
                                    name=f"**{player.user.name}**",
                                    value=
                                    f":one:\n+**{standardizedNumber(money_amount*(player_amount-1))}** <:VND:856133164854280202>"
                                )
                                for otherplayer in main.playerList:
                                    if otherplayer != player:
                                        embed.add_field(
                                            name=f"{otherplayer.user.name}",
                                            value=
                                            f":two:\n**{standardizedNumber(-money_amount)}** <:VND:856133164854280202>"
                                        )
                                embed.add_field(
                                    name=f"{player.user.name} đã tới trắng!",
                                    value=
                                    "Do về nhất khi những người chơi khác chưa xuống bài!",
                                    inline=False)
                                onTable_cardsMessage = ''.join(
                                    card for card in main.onTable_cards)
                                await message.edit(content=" ", embed=embed)
                                await message.edit(content=onTable_cardsMessage
                                                   )
                                await player.outside_message.edit(content=" ",
                                                                  embed=embed)
                                for otherplayer in main.playerList:
                                    await otherplayer.temp.delete()
                                    await otherplayer.DMmessage.delete()
                                    await otherplayer.outside_message.edit(
                                        content=onTable_cardsMessage,
                                        embed=embed)
                                await asyncio.sleep(3)
                                for otherplayer in main.playerList:
                                    await otherplayer.outside_message.edit(
                                        content=" ")
                                await message.edit(content=" ")
                                return

                        if len(main.winners) == player_amount - 1:
                            embed = None
                            for last_player in main.playerList:
                                last_player.turn = False
                                main.winners.append(last_player)
                                main.playerList.remove(last_player)
                                last_player.rank = main.ranks[
                                    main.winners.index(last_player)]
                                last_player.money = Card.getRankMoney(
                                    last_player.rank, player_amount,
                                    money_amount)
                                for card in last_player.cards:
                                    if Card.getRealValue(
                                            card) == 12.1 or Card.getRealValue(
                                                card) == 12.2:
                                        last_player.bonus_money -= (
                                            money_amount / 2)
                                        main.winners[0].bonus_money += (
                                            money_amount / 2)
                                        last_player.bonus_message += "Thối 2 đen. "
                                    if Card.getRealValue(
                                            card) == 12.3 or Card.getRealValue(
                                                card) == 12.4:
                                        last_player.bonus_money -= money_amount
                                        main.winners[
                                            0].bonus_money += money_amount
                                        last_player.bonus_message += "Thối 2 đỏ. "
                                await last_player.temp.delete()
                                await last_player.DMmessage.delete()
                                embed = await update_embed()
                                await last_player.outside_message.edit(
                                    content=" ", embed=embed)
                                for winner in main.winners:
                                    await winner.outside_message.edit(
                                        content=" ", embed=embed)
                            await message.edit(embed=embed)
                            main.matchEnd = True
                            if main.onTable_cards != []:
                                onTable_cardsMessage = ''.join(
                                    card for card in main.onTable_cards)
                                await message.edit(content=onTable_cardsMessage
                                                   )
                                for winner in main.winners:
                                    await winner.outside_message.edit(
                                        content=onTable_cardsMessage)
                                await asyncio.sleep(3)
                            for winner in main.winners:
                                await winner.outside_message.edit(content=" ")
                            await message.edit(content=" ")

                def nextTurn():
                    for i in range(0, len(main.playerList)):
                        if main.playerList[i].turn:
                            main.playerList[i].turn = False
                            try:
                                main.playerList[i + 1].turn = True
                                return main.playerList[i + 1]
                            except IndexError:
                                main.playerList[0].turn = True
                                return main.playerList[0]
                            break

                if main.matchEnd: return

                while not main.matchEnd:

                    if main.playerList != []:
                        for player in main.playerList:
                            embed = await update_embed()
                            await message.edit(embed=embed)
                            main.selected_cards = []
                            if player.turn and not player.skipped:

                                isAllSkip = 0

                                for otherplayer in main.playerList:
                                    if otherplayer != player:
                                        if otherplayer.skipped: isAllSkip += 1

                                if isAllSkip == len(main.playerList) - 1:
                                    if main.check_point == None:
                                        main.onTable_cards.clear()
                                        for otherplayer in main.playerList:
                                            otherplayer.skipped = False

                                if main.onTable_cards == []:
                                    await message.edit(
                                        content=
                                        f"**Đang chờ lượt của {player.user.name}...**"
                                    )
                                    for allPlayer in main.playerList:
                                        await allPlayer.outside_message.edit(
                                            content=
                                            f"**Đang chờ lượt của {player.user.name}...**",
                                            embed=embed)
                                    if main.winners != []:
                                        for winner in main.winners:
                                            await winner.outside_message.edit(
                                                content=
                                                f"**Đang chờ lượt của {player.user.name}...**",
                                                embed=embed)
                                else:
                                    onTable_cardsMessage = ''.join(
                                        card for card in main.onTable_cards)
                                    await message.edit(
                                        content=onTable_cardsMessage)
                                    for allPlayer in main.playerList:
                                        await allPlayer.outside_message.edit(
                                            content=onTable_cardsMessage,
                                            embed=embed)
                                    if main.winners != []:
                                        for winner in main.winners:
                                            await winner.outside_message.edit(
                                                content=onTable_cardsMessage,
                                                embed=embed)

                                if main.onTable_cards == []:
                                    player.DMmessage_turn = await player.user.send(
                                        "**Bạn là người mở lượt!**")
                                else:
                                    player.DMmessage_turn = await player.user.send(
                                        "**Đến lượt đánh của bạn!**")

                                s_options = []
                                for card in player.cards:
                                    o_card = card
                                    raw_card = card.replace(">", "")
                                    raw_card = raw_card.split(":")
                                    emo = discord.PartialEmoji(
                                        name=str(raw_card[1]),
                                        animated=False,
                                        id=str(raw_card[-1]))
                                    st = raw_card[1]
                                    lb = ""
                                    if "bich" in st: lb = "♤"
                                    elif "chuong" in st: lb = "♧"
                                    elif "ro" in st: lb = "♦"
                                    else: lb = "♥"
                                    lb1 = raw_card[1][0]
                                    if lb1 == "1": lb1 = "10"
                                    s_options.append(
                                        SelectOption(label=lb1 + " " + lb,
                                                     value=o_card,
                                                     emoji=emo))
                                btn = [
                                    Button(style=3,
                                           label="Đánh",
                                           custom_id="c_confirm"),
                                    Button(style=4,
                                           label="Qua lượt",
                                           custom_id="c_skip")
                                ]
                                slt = Select(options=s_options,
                                             placeholder="Chọn bài đánh...",
                                             custom_id="c_select",
                                             min_values=0,
                                             max_values=len(player.cards))
                                action_row_b = ActionRow(*btn)
                                action_row_s = ActionRow(slt)
                                await player.DMmessage.edit(
                                    components=[action_row_s, action_row_b])

                                def check_click(i):
                                    return (
                                        i.custom_id == 'c_confirm'
                                        or i.custom_id == 'c_skip'
                                    ) and i.message.id == player.DMmessage.id

                                while player.turn and main.playerList != [] and (
                                        not main.matchEnd):
                                    done, pending = await asyncio.wait(
                                        [
                                            asyncio.create_task(
                                                client.wait_for(
                                                    "button_click",
                                                    timeout=40,
                                                    check=check_click),
                                                name="c_button"),
                                            asyncio.create_task(
                                                client.wait_for(
                                                    "select_option",
                                                    timeout=40,
                                                    check=lambda i: i.message.
                                                    id == player.DMmessage.id
                                                    and i.custom_id ==
                                                    "c_select"),
                                                name="c_select")
                                        ],
                                        return_when=asyncio.FIRST_COMPLETED)

                                    finished: asyncio.Task = list(done)[0]

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
                                        if main.onTable_cards == []:
                                            if main.matchEnd: return
                                            embed = discord.Embed(
                                                title=
                                                f'Ván bài đã bị hủy do {player.user.name} không mở lượt của mình trong thời gian quy định'
                                            )
                                            await message.edit(content="",
                                                               embed=embed)
                                            await player.DMmessage_turn.delete(
                                            )
                                            for otherplayer in main.playerList:
                                                await otherplayer.outside_message.edit(
                                                    content=" ", embed=embed)
                                                await otherplayer.temp.delete()
                                                await otherplayer.DMmessage.delete(
                                                )
                                            return
                                        else:
                                            main.selected_cards.clear()
                                            await player.DMmessage_turn.delete(
                                            )
                                            player.skipped = True
                                            await update_cards(
                                                player, main.selected_cards)
                                            break

                                    await interaction.respond(type=6)
                                    if interaction.component_type == 3:
                                        main.selected_cards = interaction.values
                                        main.selected_cards = Card.getSortedCards(
                                            main.selected_cards)
                                        selected_cards_print = ''.join(
                                            card
                                            for card in main.selected_cards)
                                        if selected_cards_print == '':
                                            if main.onTable_cards == []:
                                                selected_cards_print = "Hãy chọn lá đánh bằng cách react chúng."
                                            else:
                                                selected_cards_print = "Hãy chọn lá đánh bằng cách react chúng hoặc qua lượt."
                                        try:
                                            await player.DMmessage_turn.edit(
                                                content=selected_cards_print)
                                        except:
                                            pass
                                    else:
                                        if interaction.custom_id == "c_confirm":
                                            if Card.isPassRule(
                                                    main.selected_cards,
                                                    main.onTable_cards,
                                                    money_amount, main):
                                                if min_value_card in player.cards and min_value_card not in main.selected_cards:
                                                    await player.user.send(
                                                        "Lượt đánh không hợp lệ!",
                                                        delete_after=2)
                                                    continue
                                                else:
                                                    main.check_point = None
                                                    await player.DMmessage_turn.delete(
                                                    )
                                                    main.onTable_cards = main.selected_cards
                                                    await update_cards(
                                                        player,
                                                        main.selected_cards)

                                            else:
                                                await player.user.send(
                                                    "Lượt đánh không hợp lệ!",
                                                    delete_after=2)

                                        elif interaction.custom_id == "c_skip":
                                            if main.onTable_cards != []:
                                                main.selected_cards.clear()
                                                await player.DMmessage_turn.delete(
                                                )
                                                player.skipped = True
                                                await update_cards(
                                                    player,
                                                    main.selected_cards)

                                            else:
                                                await player.user.send(
                                                    "Bạn không thể qua lượt vì bạn là người mở lượt",
                                                    delete_after=2)

                            elif player.skipped:
                                nextTurn()
                    else:
                        break
                if main.matchEnd: return


@client.command(aliases=['bc'])
@cooldown(1, 10, BucketType.user)
async def baicao(ctx, currentPlayers=None, amount=None):
    cards = fullCards.copy()

    if int(currentPlayers) == 2 or int(currentPlayers) == 3 or int(
            currentPlayers) == 4 or int(currentPlayers) == 1:
        pass
    else:
        await ctx.send('Vui lòng nhập số người chơi hợp lệ! (2-4)')
        return
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    wallet_amt = (users[str(user.id)]["wallet"])

    if amount == None:
        await ctx.send(f'Này {ctx.author.mention}, Vui lòng nhập số tiền cược.'
                       )
        return

    if (amount == ('all')):
        if wallet_amt <= 0:
            await ctx.send(
                f"Này {ctx.author.mention}, bạn không đủ tiền để cược!")
            return
        if wallet_amt > 50000:
            amount = 50000
        else:
            amount = wallet_amt

    amount = int(amount)
    if amount > wallet_amt:
        await ctx.send(f'Này {ctx.author.mention}, Bạn không đủ tiền để cược!')
        return
    if amount > 50000:
        await ctx.send(
            f'Này {ctx.author.mention}, Không được cược quá **50,000** <:VND:856133164854280202>!'
        )
        return
    if amount < 1:
        await ctx.send(
            f'Này {ctx.author.mention}, Vui lòng nhập số tiền hợp lệ!')
        return

    if int(currentPlayers) == 1:

        random.shuffle(cards)
        random.shuffle(cards)
        random.shuffle(cards)

        botCards = ['', '', '']
        playerCards = ['', '', '']
        botNum = 0
        playerNum = 0

        for i in range(0, 3):
            botCards[i] = cards[0]
            cards.remove(botCards[i])
            botNum = botNum + checkNum(botCards[i])
            playerCards[i] = cards[0]
            cards.remove(playerCards[i])
            playerNum = playerNum + checkNum(playerCards[i])

        botNum = realNum(botNum)
        playerNum = realNum(playerNum)

        await ctx.send(f'BOT:')
        botMessage = await ctx.send(f'<:cardsBack:856065118508548107>')
        await ctx.send(f'{ctx.author.mention}:')
        playerMessage = await ctx.send(f'<:cardsBack:856065118508548107>')
        await asyncio.sleep(0.5)
        await botMessage.edit(
            content=
            f'<:cardsBack:856065118508548107> <:cardsBack:856065118508548107>')
        await asyncio.sleep(0.5)
        await playerMessage.edit(
            content=
            f'<:cardsBack:856065118508548107> <:cardsBack:856065118508548107>')
        await asyncio.sleep(0.5)
        await botMessage.edit(
            content=
            f'<:cardsBack:856065118508548107> <:cardsBack:856065118508548107> <:cardsBack:856065118508548107>'
        )
        await asyncio.sleep(0.5)
        await playerMessage.edit(
            content=
            f'<:cardsBack:856065118508548107> <:cardsBack:856065118508548107> <:cardsBack:856065118508548107>'
        )
        await asyncio.sleep(0.5)
        await botMessage.edit(
            content=
            f'{botCards[0]} <:cardsBack:856065118508548107> <:cardsBack:856065118508548107>'
        )
        await asyncio.sleep(0.5)
        await botMessage.edit(
            content=
            f'{botCards[0]} {botCards[1]} <:cardsBack:856065118508548107>')
        await asyncio.sleep(0.5)
        await botMessage.edit(
            content=f'{botCards[0]} {botCards[1]} {botCards[2]}')

        await asyncio.sleep(0.5)
        await playerMessage.edit(
            content=
            f'{playerCards[0]} <:cardsBack:856065118508548107> <:cardsBack:856065118508548107>'
        )
        await asyncio.sleep(0.5)
        await playerMessage.edit(
            content=
            f'{playerCards[0]} {playerCards[1]} <:cardsBack:856065118508548107>'
        )
        await asyncio.sleep(0.5)
        await playerMessage.edit(
            content=f'{playerCards[0]} {playerCards[1]} {playerCards[2]}')

        if botNum == playerNum:
            await ctx.send(
                f'{ctx.author.mention} bằng nút với bot, nên không bị mất tiền.'
            )
            await update_bank(ctx.author, 1 * amount, "wallet")
        if botNum < playerNum:
            await ctx.send(
                f'Chúc mừng {ctx.author.mention} đã chiến thắng **{standardizedNumber(amount*2)}** <:VND:856133164854280202>!'
            )
            await update_bank(ctx.author, 2 * amount, "wallet")
        if botNum > playerNum:
            await ctx.send(
                f'Rất tiếc, {ctx.author.mention} đã thua **{standardizedNumber(amount)}** <:VND:856133164854280202>.'
            )
        await update_bank(ctx.author, -1 * amount, "wallet")

    else:
        embed = discord.Embed(
            title=
            f'<:cardsBack:856065118508548107> Set kèo bài cào ! <:cardsBack:856065118508548107>',
            color=0x14e4ff)
        embed.add_field(
            name=f':satellite: Người ra kèo: **{ctx.author.name}**',
            value=
            f':moneybag: Số tiền là: **{standardizedNumber(amount)}** <:VND:856133164854280202>\n:bust_in_silhouette: Số lượng người chơi : **{currentPlayers}**\nĐể tham gia ván bài, hãy react  ✅  trong vòng 30 giây',
            inline=False)

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')

        playerlist = [ctx.author]
        embed.add_field(name=f'{ctx.author.name}', value='✅', inline=True)
        await message.edit(embed=embed)

        def check(reaction, r_user):
            return r_user not in playerlist and r_user != client.user and str(
                reaction.emoji) == '✅' and reaction.message.id == message.id

        while len(playerlist) < int(currentPlayers):
            try:
                reaction, r_user = await client.wait_for('reaction_add',
                                                         timeout=30.0,
                                                         check=check)
            except asyncio.TimeoutError:
                embed = discord.Embed(
                    title=
                    'Ván bài đã bị hủy do quá thời gian chờ và không đủ số lượng người chơi!'
                )
                await message.edit(embed=embed)
                await message.clear_reactions()
                return
            else:
                await open_account(user)
                users = await get_bank_data()
                bal = users[str(r_user.id)]["wallet"]
                if amount > bal:
                    await ctx.send(
                        f'Này {r_user.mention}, Bạn không đủ tiền để cược!')
                    continue
                embed.add_field(name=f'{r_user.name}', value='✅')
                await message.edit(embed=embed)
                playerlist.append(r_user)
                if len(playerlist) == int(currentPlayers):
                    embed.add_field(
                        name=f'Đã đủ số lượng người chơi.',
                        value=
                        f'Ván bài sẽ bắt đầu.\nSố tiền đã cược: **{standardizedNumber(amount*int(currentPlayers))}**<:VND:856133164854280202>',
                        inline=False)
                    await message.edit(embed=embed)

                    random.shuffle(cards)
                    random.shuffle(cards)
                    random.shuffle(cards)

                    messageA = ['', '', '', '']

                    for i in range(0, int(currentPlayers)):
                        await ctx.send(f'{playerlist[i].mention}:')
                        await asyncio.sleep(0.5)
                        messageA[i] = await ctx.send(
                            f'<:cardsBack:856065118508548107>')
                    for i in range(0, int(currentPlayers)):
                        await asyncio.sleep(0.5)
                        await messageA[i].edit(
                            content=
                            f'<:cardsBack:856065118508548107> <:cardsBack:856065118508548107>'
                        )
                    for i in range(0, int(currentPlayers)):
                        await asyncio.sleep(0.5)
                        await messageA[i].edit(
                            content=
                            f'<:cardsBack:856065118508548107> <:cardsBack:856065118508548107> <:cardsBack:856065118508548107>'
                        )

                    playerNum = []
                    for i in range(0, int(currentPlayers)):
                        playerNum.append(0)
                    playerCards = []
                    for i in range(0, int(currentPlayers)):
                        playerCards.append(' ')

                    for j in range(0, int(currentPlayers)):
                        playerCards[j] = [' ', ' ', ' ']

                    for i in range(0, 3):
                        for j in range(0, int(currentPlayers)):
                            playerCards[j][i] = cards[0]
                            playerNum[j] += checkNum(cards[0])
                            cards.remove(cards[0])

                    for i in range(0, int(currentPlayers)):
                        playerNum[i] = realNum(playerNum[i])

                    for i in range(0, int(currentPlayers)):
                        await asyncio.sleep(0.5)
                        await messageA[i].edit(content=playerCards[i][0])
                    for i in range(0, int(currentPlayers)):
                        await asyncio.sleep(0.5)
                        await messageA[i].edit(content=playerCards[i][0] +
                                               playerCards[i][1])
                    for i in range(0, int(currentPlayers)):
                        await asyncio.sleep(0.5)
                        await messageA[i].edit(content=playerCards[i][0] +
                                               playerCards[i][1] +
                                               playerCards[i][2])

                    winner = max(playerNum)
                    playerWinner = []

                    for i in range(0, int(currentPlayers)):
                        if playerNum[i] == winner:
                            playerWinner.append(playerlist[i])

                    if len(playerWinner) > 1:
                        winMoney = (amount *
                                    int(currentPlayers)) // len(playerWinner)
                        for winner in playerWinner:
                            await update_bank(winner, winMoney, "wallet")
                        for player in playerlist:
                            await update_bank(player, -1 * amount, "wallet")
                        winners = " ".join(winner.mention
                                           for winner in playerWinner)
                        await ctx.send(
                            f'{winners} đã hòa kèo với số tiền **{standardizedNumber(winMoney)}** <:VND:856133164854280202>!'
                        )
                        return
                    for i in range(0, int(currentPlayers)):
                        if playerlist[i] in playerWinner:
                            winMoney = (amount * int(currentPlayers)
                                        ) // len(playerWinner)
                            await ctx.send(
                                f'{playerlist[i].mention} đã thắng kèo với số tiền **{standardizedNumber(winMoney)}** <:VND:856133164854280202>!'
                            )
                            await update_bank(playerlist[i], winMoney,
                                              "wallet")
                            await update_bank(playerlist[i], -1 * amount,
                                              "wallet")
                        else:
                            await update_bank(playerlist[i], -1 * amount,
                                              "wallet")
                    return


@client.command(aliases=['qhq'])
@cooldown(1, 4, BucketType.user)
async def quayhoaqua(ctx, amount=None):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    wallet_amt = users[str(user.id)]["wallet"]

    if amount == None:
        await ctx.send(f'Này {ctx.author.mention}, Vui lòng nhập số tiền cược.'
                       )
        return

    if (amount == ('all')):
        if wallet_amt <= 0:
            await ctx.send(
                f"Này {ctx.author.mention}, bạn không đủ tiền để cược!")
            return
        if wallet_amt >= 100000:
            amount = 100000
        else:
            amount = wallet_amt

    amount = int(amount)
    if amount > wallet_amt:
        await ctx.send(f'Này {ctx.author.mention}, bạn không đủ tiền để cược!')
        return
    if amount > 100000:
        await ctx.send(
            f'Này {ctx.author.mention}, Không được cược quá **100,000** <:VND:856133164854280202>!'
        )
        return
    if amount < 1:
        await ctx.send(
            f'Này {ctx.author.mention}, Vui lòng nhập số tiền hợp lệ!')
        return

    slots = [
        'green_apple', 'lemon', 'banana', 'watermelon', 'strawberry', 'tomato',
        'carrot', 'grapes', 'pineapple', 'pear', 'cherries', 'kiwi'
    ]
    slot1 = slots[random.randint(0, len(slots) - 1)]
    slot3 = slots[random.randint(0, len(slots) - 1)]
    slot2temp = [
        'kiwi', 'cherries', slot3, 'green_apple', 'lemon', 'banana', 'pear',
        'watermelon', 'strawberry', 'tomato', slot1, 'carrot', 'grapes',
        'pineapple'
    ]
    slot2 = slot2temp[random.randint(0, len(slot2temp) - 1)]

    message = await ctx.send(
        f'<a:loading:876310730159325194> | <a:loading:876310730159325194> | <a:loading:876310730159325194> |'
    )
    await asyncio.sleep(1)
    await message.edit(
        content=
        f'| :{slot1}: | <a:loading:876310730159325194> | <a:loading:876310730159325194> |\n'
    )
    await asyncio.sleep(1)
    await message.edit(
        content=f'| :{slot1}: | <a:loading:876310730159325194> | :{slot3}: |\n'
    )
    await asyncio.sleep(1)
    await message.edit(content=f'| :{slot1}: | :{slot2}: | :{slot3}: |\n')
    slotOutput = f'| :{slot1}: | :{slot2}: | :{slot3}: |'
    if slot1 == slot2 == slot3:
        await update_bank(ctx.author, 8 * amount, "wallet")
        await message.edit(
            content=
            f"{slotOutput}\nÔI TUYỆT VỜI, ĐỘC ĐẮC !! {ctx.author.mention} đã cược **{standardizedNumber(amount)}** <:VND:856133164854280202> và trúng {standardizedNumber(8*amount)} <:VND:856133164854280202>!!!"
        )
    else:
        if slot1 == slot2 or slot1 == slot3 or slot2 == slot3:
            await update_bank(ctx.author, 2 * amount, "wallet")
            await message.edit(
                content=
                f"{slotOutput}\n Chúc mừng {ctx.author.mention} đã cược **{standardizedNumber(amount)}** <:VND:856133164854280202> và trúng **{standardizedNumber(2*amount)}** <:VND:856133164854280202>!"
            )
        else:
            await message.edit(
                content=
                f"{slotOutput}\n Ôi không, {ctx.author.mention} đã thua **{standardizedNumber(amount)}** <:VND:856133164854280202>, chúc bạn may mắn lần sau"
            )
    await update_bank(ctx.author, -1 * amount, "wallet")


@client.command()
@cooldown(1, 7200, BucketType.user)
async def free(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    ngaunhien = random.randint(1000, 3000)
    amount = ngaunhien
    await update_bank(ctx.author, amount, "wallet")
    message = await ctx.send(
        f'{ctx.author.mention} đã nhận được <a:loading:876310730159325194>')
    await asyncio.sleep(2)
    await message.edit(
        content=
        f'{ctx.author.mention} đã nhận được **{standardizedNumber(amount)}** <:VND:856133164854280202>, bạn có thể nhận lại vào **2** tiếng sau.'
    )


@client.command(aliases=["bnke"])
@cooldown(1, 7200, BucketType.user)
async def bankearn(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    bank = users[str(user.id)]["bank"]
    if (bank < 100):
        await ctx.send(
            "Tài khoản ngân hàng của bạn chưa đủ tiền để nhận lãi suất!")
        return
    earn = int(bank / 100 * 1.5)
    await update_bank(ctx.author, earn, "wallet")
    await ctx.send(
        f"{ctx.author.mention} đã nhận thành công **{standardizedNumber(earn)}** <:VND:856133164854280202> từ lãi suất ngân hàng, bạn có thể nhận tiếp vào 2 tiếng sau."
    )


@client.event
async def on_ready():
    print('Bot dang online')
    print(os.getenv("REPLIT_DB_URL"))
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=f"t help in {len(list(client.guilds))} servers!"))


@client.command()
@cooldown(1, 4, BucketType.user)
async def ping(ctx):
    await ctx.send(f'Hiện tại ping là : **{round(client.latency * 1000)}** ms')


@client.command(aliases=['smm'])
@cooldown(1, 4, BucketType.user)
async def somayman(ctx, amount=None, number=None):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    wallet_amt = (users[str(user.id)]["wallet"])

    if amount == None:
        await ctx.send(f'Này {ctx.author.mention}, Vui lòng nhập số tiền cược.'
                       )
        return

    if (amount == ('all')):
        if wallet_amt == 0:
            await ctx.send(
                f"Này {ctx.author.mention}, bạn không đủ tiền để cược!")
            return
        if wallet_amt > 50000:
            amount = 50000
        else:
            amount = wallet_amt

    amount = int(amount)
    if amount > wallet_amt:
        await ctx.send(f'Này {ctx.author.mention}, Bạn không đủ tiền để cược!')
        return
    if amount > 50000:
        await ctx.send(
            f'Này {ctx.author.mention}, Không được cược quá **50,000** <:VND:856133164854280202>!'
        )
        return
    if amount < 1:
        await ctx.send(
            f'Này {ctx.author.mention}, Vui lòng nhập số tiền hợp lệ!')
        return

    if number == None:
        await ctx.send(
            f'Này {ctx.author.mention}, vui lòng nhập số may mắn của bạn (1-5)'
        )
        return

    number = int(number)
    if number > 5:
        await ctx.send(f'Này {ctx.author.mention}, chỉ nhập từ 1 đến 5 thôi')
        return
    if number < 1:
        await ctx.send(f'Này {ctx.author.mention}, Vui lòng nhập số hợp lệ!')
        return

    mayman = random.randint(1, 5)
    number_emoji = [":one:", ":two:", ":three:", ":four:", ":five:"]
    message = await ctx.send(f'Số may mắn là: <a:loading:876310730159325194>')
    await asyncio.sleep(2)
    await message.edit(content=f'Số may mắn là: {number_emoji[mayman-1]}')
    if number == mayman:
        await update_bank(ctx.author, 4 * amount, "wallet")
        await message.edit(
            content=f'Số may mắn là: {number_emoji[mayman-1]}' +
            f'\nChúc mừng! {ctx.author.mention} đã cược **{standardizedNumber(amount)}** <:VND:856133164854280202> và trúng **{standardizedNumber(4*amount)}** <:VND:856133164854280202>!'
        )
        await update_bank(ctx.author, -1 * amount, "wallet")
    else:
        await message.edit(
            content=f'Số may mắn là: {number_emoji[mayman-1]}' +
            f'\n{ctx.author.mention} đã thua **{standardizedNumber(amount)}** <:VND:856133164854280202>, chúc bạn may mắn lần sau'
        )
        await update_bank(ctx.author, -1 * amount, "wallet")


@client.command(aliases=["balance", "bal", "money", "cash"])
@cooldown(1, 4, BucketType.user)
async def tien(ctx, user: discord.User = None):
    message = await ctx.send("<a:loading:876310730159325194>")
    if user == None:
        user = ctx.author
    await open_account(user)

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    class userData:
        def __init__(self, user, cash, inv, money):
            self.user = user
            self.money = money
            self.inv = inv
            self.cash = cash

    def get_money(user):
        return user.money

    guild = ctx.channel.guild
    user_list = []
    inventory = client.get_cog("Inventory")
    users_inv = await inventory.get_inventory_data()
    c_user_inv = users_inv[str(user.id)]
    user_inv_price = 0
    if c_user_inv != {}:
        for item in c_user_inv:
            i = await inventory.get_item_data(item)
            user_inv_price += i.price * (c_user_inv[item]['a'])
    user_total = wallet_amt + bank_amt + user_inv_price

    em = discord.Embed(
        title=f":moneybag: Số tiền hiện tại của **{user.name}** là: ",
        description="\u200b",
        color=0xffadbe,
        timestamp=datetime.utcnow())
    em.set_thumbnail(url=user.avatar_url)
    em.add_field(
        name=
        f":purse: : **{standardizedNumber(wallet_amt)}** <:VND:856133164854280202>",
        value='\u200b',
        inline=False)
    em.add_field(
        name=
        f":bank: : **{standardizedNumber(bank_amt)}** <:VND:856133164854280202>",
        value='\u200b',
        inline=False)
    em.add_field(
        name=
        f":file_cabinet: : **{standardizedNumber(user_inv_price)}** <:VND:856133164854280202>",
        value='\u200b',
        inline=False)
    em.add_field(
        name=
        f"Tổng: **{standardizedNumber(user_total)}** <:VND:856133164854280202>",
        value='\u200b',
        inline=False)
    await message.edit(content="", embed=em)


#lenh ve tien o day


@client.command()
@cooldown(1, 4, BucketType.user)
async def rut(ctx, amount=None):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    bank_amt = (users[str(user.id)]["bank"])

    if (amount == ('all') and bank_amt > 0):
        amount = bank_amt

    if amount == None:
        await ctx.send(
            f'Này {ctx.author.mention}, Vui lòng nhập số tiền muốn rút!')
        return

    amount = int(amount)
    if amount > bank_amt:
        await ctx.send(
            f'Này {ctx.author.mention}, Bạn không đủ tiền trong tài khoản để rút!'
        )
        return
    if amount <= 0:
        await ctx.send(
            f'Này {ctx.author.mention}, Vui lòng nhập số tiền hợp lệ!')
        return
    await update_bank(ctx.author, amount, "wallet")
    await update_bank(ctx.author, -1 * amount, "bank")
    await ctx.send(
        f'{ctx.author.mention} đã rút thành công **{standardizedNumber(amount)}** <:VND:856133164854280202> vào ví'
    )


@client.command()
@cooldown(1, 60, BucketType.user)
async def gui(ctx, amount=None):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    wallet_amt = (users[str(user.id)]["wallet"])

    if (amount == ('all')):
        amount = wallet_amt

    if amount == None:
        await ctx.send(
            f'Này {ctx.author.mention}, Vui lòng nhập số tiền muốn gửi ngân hàng!'
        )
        return

    amount = int(amount)
    if amount > wallet_amt:
        await ctx.send(
            f'Này {ctx.author.mention}, Bạn không đủ tiền để gửi ngân hàng!')
        return
    if amount < 0:
        await ctx.send(
            f'Này {ctx.author.mention}, Vui lòng nhập số tiền hợp lệ!')
        return
    await update_bank(ctx.author, amount, "bank")
    await update_bank(ctx.author, -1 * amount, "wallet")
    await ctx.send(
        f'{ctx.author.mention} đã gửi thành công **{standardizedNumber(amount)}** <:VND:856133164854280202> vào tài khoản ngân hàng.'
    )


@client.command()
@cooldown(1, 4, BucketType.user)
async def chuyen(ctx, member: discord.Member, amount=None):
    await open_account(ctx.author)
    await open_account(member)
    user = ctx.author
    users = await get_bank_data()
    wallet_amt = (users[str(user.id)]["wallet"])

    if (amount == ('all')):
        amount = wallet_amt

    if amount == None:
        await ctx.send(
            f'Này {ctx.author.mention}, Vui lòng nhập số tiền muốn chuyển!')
        return

    amount = int(amount)
    if amount > wallet_amt:
        await ctx.send(
            f'Này {ctx.author.mention}, Số dư của bạn không đủ để thực hiện chuyển tiền!'
        )
        return
    if amount < 0:
        await ctx.send(
            f'Này {ctx.author.mention}, Vui lòng nhập số tiền hợp lệ!')
        return
    await update_bank(ctx.author, -1 * amount, "wallet")
    await update_bank(member, amount, "wallet")
    await ctx.send(
        f'{ctx.author.mention} đã chuyển thành công **{standardizedNumber(amount)}** <:VND:856133164854280202> cho {member.mention}!'
    )


async def open_account(user):
    await client.get_cog("Inventory").open_inventory(user)
    if str(user.id) in db["mainbank"]:
        return False
    else:
        db["mainbank"][str(user.id)] = {}
        db["mainbank"][str(user.id)]["wallet"] = 0
        db["mainbank"][str(user.id)]["bank"] = 0

    return True


async def get_bank_data():

    return db["mainbank"]


async def update_bank(user, change=0, mode='wallet'):
    change = int(change)

    db["mainbank"][str(user.id)][mode] += change


client.load_extension("helpCommands")
client.load_extension("controller")
client.load_extension("inventory.inventory")
client.load_extension("fishing.fishing")
client.load_extension("hunting.hunt")
keep_alive()
my_secret = os.environ.get('DISCORD_BOT_SECRET')
client.run(my_secret)
