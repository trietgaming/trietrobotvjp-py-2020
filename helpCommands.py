import discord
from discord.ext import commands
from main import *

class Help(commands.Cog):
    def __init__(self,client):
        self.client = client

    change =  """
    - Cân bằng <fishing>
    - THÊM LỆNH : <hunt> - <t help hunt> để biết thêm chi tiết
"""
    date_change = "28/8/2021" 

    @commands.command()
    @cooldown(1,5,BucketType.user)
    async def help(self, ctx, command = None):
        if command == None:
            await ctx.send(embed = Help.main_embed(), components = [[Button(emoji = "🤖" ,style = 5, label = "Invite bot", url = "https://discord.com/api/oauth2/authorize?client_id=769097658572472320&permissions=8192&scope=bot"),Button(emoji = "🔔",style = 5, label = "Subscribe us", url = "https://www.youtube.com/channel/UC-MDrlf-82aWwipeBsE_zXQ"),Button(emoji = "❤️",style = 5, label = "Donation", url = "https://playerduo.com/trietgaming")]])
        else:
            command = command.lower()
            if command =="lastchange":
                embed = Help.get_embed("Lastchange","t lastchange","Hiển thị những thay đổi gần nhất của bot.",0)
                await ctx.send(embed = embed)
            help_method = getattr(Help, str(command), "invalid")
            if help_method != "invalid":
                await ctx.send(embed = help_method())
            else:
                await ctx.send("**Lệnh không hợp lệ!**", delete_after = 3)

    @commands.command(aliases = ["changelog"])
    @cooldown(1,15,BucketType.user)
    async def lastchange(self, ctx):
        await ctx.send(f"`* Những thay đổi gần nhất:{Help.change}* Ngày thay đổi: {Help.date_change}`")

    @staticmethod
    def main_embed():
        embed=discord.Embed(title=":flag_vn:  **Danh sách các lệnh hiện có **", description=':brain: Các câu lệnh có thể bắt đầu bằng **"t"**, **"T"** hoặc **"triet"**\n:thinking: Gõ **"t help <lệnh muốn trợ giúp>"** để biết thông tin chi tiết của lệnh cũng như cách sử dụng.', color=0x75ddff)
        embed.set_author(name="TrietRobotVjp", icon_url="https://cdn.discordapp.com/avatars/769097658572472320/3e8db955df725750b128a1ef610c6d38.png?size=1024")
        embed.add_field(name=":robot:  Lệnh về bot:", value="**`ping`** **`invite`** **`lastchange`** **`reportbug`**", inline=False)
        embed.add_field(name="<:cardsBack:856065118508548107>  Cờ bạc:", value="**`quayhoaqua`** **`somayman`** **`baicao`** **`tienlen`**", inline=False)
        embed.add_field(name=":moneybag:  Tiền:", value="**`tien`** **`chuyen`** **`gui`** **`rut`**", inline=False)
        embed.add_field(name=":gem:  Vật phẩm:", value="**`kho`** **`shop`** **`mua`** **`ban`** **`trade`**", inline=False)
        embed.add_field(name=":pick:  Kiếm tiền:", value="**`free`** **`bankearn`** **`fishing`** **`hunt`** - MỚI!", inline=False)
        embed.add_field(name=":signal_strength:  Dữ liệu:", value="**`leaderboard`**", inline=False)
        embed.set_footer(text=""" Hãy report lỗi cho chúng tôi bằng "t reportbug <lỗi>" để chúng tôi xem xét và sửa trong thời gian sớm nhất.\nLiên hệ với chúng tôi qua Discord: "Triết#6102" - Bạn có thể invite vào server của bạn để cùng giải đáp thắc mắc hoặc góp ý...""")
        return embed
    
    @staticmethod
    def get_embed(title, cp, cp_value, type):
        types=[
            ":electric_plug: Lệnh cơ bản",
            "<:cardsBack:856065118508548107>  Cờ bạc",
            ":moneybag:  Tiền",
            ":pick: Kiếm tiền",
            ":signal_strength: Dữ liệu",
            ":gem: Vật phẩm"
        ]
        embed=discord.Embed(title=f":book: Lệnh: {title}", color=0xc2dcff)
        embed.add_field(name=f':brain: Cú pháp: "{cp}"', value=cp_value, inline=False)
        embed.add_field(name=":radio: Loại:", value=types[type], inline=False)
        return embed
    @staticmethod
    def ping():
        embed = Help.get_embed("Ping", "t ping", "Hiển thị độ trễ (ms) của bot.",0)
        return embed
    
    @staticmethod
    def free():
        embed = Help.get_embed("Free", "t free", "Nhận một số tiền ngẫu nhiên trong khoảng 1000-3000 <:VND:856133164854280202>, có thể nhận lại sau 2 tiếng.", 3)
        return embed

    @staticmethod
    def tien():
        embed = Help.get_embed("Tien", "t tien <@Người dùng Discord>", "Nếu bỏ trống <@Người dùng Discord> thì Bot sẽ hiển thị ra số tiền hiện tại của bạn (bao gồm ví tiền và tài khoản ngân hàng), còn không thì Bot sẽ hiển thị của người mà bạn nhắc đến.", 2)
        return embed

    @staticmethod
    def chuyen():
        return Help.get_embed("Chuyen", "t chuyen <@Người dùng Discord> <Số tiền cần chuyển>", "Chuyển số tiền bằng với <Số tiền cần chuyển> từ ví của bạn sang ví của <@Người dùng Discord>, không giới hạn số tiền chuyển được.",2)

    @staticmethod
    def gui():
        return Help.get_embed("Gui", "t gui <Số tiền cần gửi>", "Gửi số tiền bằng <Số tiền cần gửi> từ ví tiền vào ngân hàng của bạn.", 2)

    @staticmethod
    def rut():
        return Help.get_embed("Rut", "t rut <Số tiền cần rút>", "Rút số tiền bằng <Số tiền cần rút> từ ngân hàng vào ví tiền của bạn.", 2)

    @staticmethod
    def quayhoaqua():
        return Help.get_embed("Quayhoaqua (Viết tắt: qhq)", "t quayhoaqua <Số tiền cược (tối đa 50000)>", "Quay ngẫu nhiên 3 trái cây, có 2/3 quả trùng thì sẽ thắng gấp đôi số tiền đã cược, nếu trùng cả 3 quả thì thắng gấp 8 lần số tiền đã cược (đặc biệt), còn không thì sẽ thua số tiền đã cược từ ví tiền của bạn.", 1)
    
    @staticmethod
    def somayman():
        return Help.get_embed("Somayman (Viết tắt: smm)", "t somayman <Số tiền cược (tối đa 50000)> <Số từ 1-5>","Bot sẽ quay số ngẫu nhiên trong khoảng 1-5, nếu trùng số của bạn thì thắng gấp 4 lần số tiền đã cược từ ví tiền của bạn, còn không thì sẽ thua số tiền đã cược từ ví tiền của bạn.", 1)
    
    @staticmethod
    def baicao():
        embed = Help.get_embed("Baicao (Viết tắt: bc)","t baicao <Số lượng người chơi (tối đa 4, tối thiểu 1)> <Số tiền cược (tối đa 25000)>",'Nếu nhập số lượng người chơi bằng 1, bạn sẽ chơi với bot.\n Nếu không, bot sẽ hiển thị ra một bảng kèm nút ✅, những người chơi khác sẽ phải react vào nếu muốn tham gia ván bài và phải có đủ tiền cược mới có thể tham gia.\nChơi tương tự như bài cào thông thường.',1)
        embed.add_field(name = "Luật chơi cho ai chưa biết:", value = "Bot sẽ chia bài cho những người chơi tham gia, mỗi người ba lá. Cách tính điểm như sau: Các lá: 2, 3, 4, 5, 6, 7, 8, 9, 10 mỗi lá có số điểm tương ứng con số đó. Các lá: J, Q, K mỗi lá tính mười điểm. Điểm của người chơi trong mỗi ván là số lẻ 10 của tổng điểm ba lá bài. Ví dụ, tổng ba lá là 27 điểm thì được 7 điểm (hay gọi là nút), 10 điểm thì được 0 điểm (gọi là bù). Trường hợp đặc biệt là ai sở hữu được cả ba lá bài J, Q, K bất kỳ thì thắng ngay ván đó không cần tính điểm gọi là ba cào hoặc ba tiên (nếu không ai khác sở hữu ba cào). Bài cào không quan tâm đến chất (cơ ♥, rô ♦, chuồng ♣, bích ♠) của mỗi lá bài. Ví dụ bộ ♥ 3, ♣ 4, ♠ 2 (9 nút) vẫn hòa với bộ ♦ 3, ♠ 4, ♣ 2 (Nguồn: Wikipedia).\nNgười thắng là người có số nút lớn nhất, sẽ thắng tất cả số tiền của những người chơi khác, nếu có người trùng nút thì sẽ chia tiền. ")
        return embed
    
    @staticmethod
    def tienlen():
        embed = Help.get_embed("Tienlen (Viết tắt: tlmn)","t tienlen <Số lượng người chơi (tối đa 4, tối thiểu 2)> <Số tiền cược (tối đa 200000)>",'Bot sẽ hiển thị ra một bảng kèm nút **Tham gia**, những người chơi khác sẽ phải ấn vào nếu muốn tham gia ván bài và phải có đủ tiền cược mới có thể tham gia.\nKhi đã đủ số lượng người chơi, Bot sẽ gửi tin nhắn riêng cho từng người chơi tham gia, người chơi cần vào phần tin nhắn riêng tư ấy để tương tác với trò chơi.\n**Cách chơi:** Nếu tới lượt bạn, chọn lá bài trong bảng lựa chọn ngay dưới phần bài của bạn, khi chọn thì sẽ hiện lên những lá bài bạn chọn, bạn có thể hủy chọn. Ấn nút **Đánh** để đánh những lá bài bạn chọn, **Qua lượt** để qua lượt **(Lưu ý: lượt đánh phải tuân thủ luật, nếu không sẽ được đánh lại và người mở lượt không thể qua luợt, thời gian chờ tương tác là 40 giây)**. Còn nếu bạn không có lượt thì phải đợi đến lượt của bạn mới có thể đánh. Khi quá thời gian chờ tương tác, nếu người có lượt là người mở lượt thì ván bài sẽ bị hủy, còn không thì sẽ tự động qua lượt.',1)
        embed.add_field(name = ":face_with_raised_eyebrow: **Luật chơi cơ bản:**", value = "Game tiến lên Nam sử dụng cả bộ bài tú lơ khơ gồm 52 lá. Độ lớn các là bài được sắp xếp theo thứ tự 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A, 2. Trong đó nhỏ nhất là 3 và lớn nhất là 2. Độ lớn được sắp xếp như sau: Bích ♠ < Chuồn ♣ < Rô ♦ < Cơ ♥. Số lượng người chơi tối đa là 4 người, tối thiểu là 2 người. Khi bắt đầu chơi, mỗi người chơi được chia 13 lá bài. Lượt chơi đánh bài từ trái qua phải. Lượt đầu tiên người chơi có lá bài 3♠ (hoặc lá nhỏ nhất) được đi trước và bắt buộc phải đánh ra lá đó (có thể theo đôi hoặc sảnh). Mỗi lượt chơi người chơi cần đánh ra lá bài (hoặc bộ bài) có thể chặt được lá bài (hoặc bộ bài) của người chơi trước vừa đánh ra, nếu không thể chặt thì phải qua lượt. Khi không có người chơi chặt được lá bài vừa đánh thì lượt chơi kết thúc, người vừa đánh có thể tiếp tục đánh ra quân bài tùy ý (quân bài phải hợp lệ). Ván bài kết thúc khi tất cả người chơi đã đánh hết bài trên tay.")
        embed.add_field(name =":thinking: **Luật chặt 2, chặt hàng và tới trắng:**", value="Khác với tiến lên miền nam thông thường một chút, chúng tôi đã chỉnh sửa một số luật như sau:\n**Tứ quý**: chặt được 2, đôi 2.\n**Ba đôi thông**: chặt 2\n**Bốn đôi thông**: chặt 2, đôi 2\n**Năm đôi thông**: chặt 2, đôi 2 và tam 2.\nHàng lớn hơn có thể chặt hàng nhỏ hơn, không thể chặt hàng khác loại.\n**Luật tới trắng**: sở hữu Tứ quý 2, 6 đôi, sảnh rồng (từ 3 đến 2) và đánh hết bài khi tất cả những người chơi khác còn nguyên 13 lá.\n**Những luật từ tiến lên miền Nam đã bị lược bỏ như:** chết 13 cây, tới cóng, chết hàng (thối hàng), các trường hợp tới trắng khác.")
        return embed
    
    @staticmethod
    def invite():
        return Help.get_embed("Invite","t invite","Hiển thị link mời (invite) bot vào server của bạn.",0)

    @staticmethod
    def leaderboard():
        return Help.get_embed("Leaderboard (Viết tắt: ldb, top)", "t leaderboard", "Hiển thị danh sách 10 người giàu nhất trong server, nếu số những người có tài khoản tiền mặt nhỏ hơn 10 thì hiện tất cả trong số đó.",4)


    @staticmethod
    def bankearn():
        return Help.get_embed("Bankearn (Viết tắt: bnke)","t bankearn","Nhận tiền lãi từ lãi suất ngân hàng (1.5%) tính bằng tài khoản ngân hàng của bạn. Mỗi lần nhận cách nhau 2 tiếng.",3)
    
    @staticmethod
    def inventory():
        return Help.get_embed("Kho (Viết tắt: inv, inventory)","t kho <@Người dùng Discord>","Hiển thị ra kho đồ của bạn nếu bỏ trống <@Người dùng Discord>, còn không hiển thị kho đồ của người đó.",5)

    @staticmethod
    def shop():
        return Help.get_embed("Shop","t shop","Hiển thị ra các vật phẩm có thể mua.",5)

    @staticmethod
    def mua():
        return Help.get_embed("Mua (hoặc buy)", "t mua <ID vật phẩm> <Số lượng (mặc định là 1)>","Mua vật phẩm với ID đã nhập, chỉ có thể mua vật phẩm hiện có ở shop.",5)

    @staticmethod
    def ban():
        return Help.get_embed("Ban (hoặc sell)","t ban <ID vật phẩm hoặc loại vật phẩm> <Số lượng (mặc định là 1)>",'Bán vật phẩm trong kho đồ của bạn với ID đã nhập, xem giá bán trong kho đồ của bạn. Nếu nhập số lượng bằng "all" thì bán tất cả vật phẩm đó. Nếu nhập vào loại vật phẩm thì bán tất cả những vật phẩm cùng loại trong kho đồ.',5)

    @staticmethod
    def reportbug():
        return Help.get_embed("Reportbug","t reportbug <Lỗi bạn gặp phải>","Gửi tin nhắn đến chúng tôi về lỗi của bạn gặp phải, chúng tôi luôn xem xét chúng để sửa.",0)

    @staticmethod
    def gofish():
        return Help.get_embed("Fishing (Hoặc: gf, gofish, gofishing)","t fishing <Địa điểm>",'Hiện có 2 địa điểm: "river" (r) và "sea" (s). Để câu cá, bạn cần có **<:cancauthuong:876424458154418186> Cần câu cá#`0000`** và **<:moicau:877132339585626132> Mồi câu cá#`0034`** (xem trong "t shop" và dùng lệnh "t mua" để mua), để câu ở "river" bạn cần có **<:thuyennho:877131605674717195> Thuyền đánh cá nhỏ#`0035`**, còn ở "sea" thì bạn cần **<:taucalon:877133054991278140> Tàu đánh cá lớn#`0036`** để câu. Mỗi lần câu tốn 1 **<:moicau:877132339585626132> Mồi câu cá#`0034`** và giảm 1 độ bền của cần câu và thuyền. Khi câu, bot sẽ đợi đến khi cá đớp mồi. Khi cá đã đớp mồi, bạn cần ấn nhanh nút "CÂU!" để câu cá trong khoảng 1 giây. Nếu không câu, bạn sẽ không câu được cá và vẫn sẽ mất mồi. Cá sau khi câu sẽ được lưu trong kho đồ (dùng "t kho" để xem).',3)
    @staticmethod
    def trade():
        embed = Help.get_embed("Trade","t trade <@Người dùng Discord>","Dùng để trao đổi vật phẩm giữa người với người.\n**Cách dùng:** nhập lệnh đúng cú pháp, sau đó bot sẽ hiển thị ra một bảng thông tin.\nNhập **sadd <ID vật phẩm 1>=<số lượng>/<ID vật phẩm 2>=<số lượng>/...<ID vật phẩm N>=<số lượng>** để thêm vật phẩm của bạn vào bảng trao đổi.\n**tadd <ID vật phẩm 1>=<số lượng>/<ID vật phẩm 2>=<số lượng>/...<ID vật phẩm N>=<số lượng>** để thêm vật phẩm của người bạn muốn trao đổi để trao đổi. **Bạn có thể nhập số lượng là âm để rút ra khỏi ô trao đổi một số lượng bạn nhập, nếu nhỏ hơn hoặc bằng 0 thì loại vật phẩm ra khỏi ô**. **Bạn có thể thêm vật phẩm nhiều lần**. **Bạn có thể bỏ trống phần vật phẩm của bạn hoặc của người bạn cần trao đổi** (dùng để xin đồ hoặc tặng vật phẩm, không được bỏ trống cả hai)\n**Khi đã chắc chắn về lựa chọn của mình**, gõ '**confirm**' để gửi đi lời mời trao đổi. Người được yêu cầu trao đổi cần phải react ✅ để thực hiện trao đổi (bot sẽ gửi tin nhắn riêng cho người đó). Trao đổi có hiệu lực trong 3 phút. ",5)
        embed.add_field(name ="Những lưu ý khi sử dụng:",value = "Vật phẩm bạn thêm phải có trong kho đồ của bạn hoặc của người muốn trao đổi, tùy trường hợp bạn thêm ô nào. Số lượng vật phẩm phải nhỏ hơn hoặc bằng trong kho đồ. Có thể sử dụng **'all'** trong phần số lượng vật phẩm cần thêm để thêm hết số lượng vật phẩm đó có trong kho đồ, sử dụng **'-all'** để rút vật phẩm ra khỏi ô. Lệnh thêm vật phẩm phải có '=' ở trong cú pháp (<ID vật phẩm>=<số lượng>/...). Trao đổi sẽ bị hủy khi bạn không 'confirm' trong thời gian quy định. **Kho đồ của một trong 2 người không được thay đổi để trao đổi được chấp nhận**.")
        return embed

    @staticmethod
    def hunt():
        return Help.get_embed("Hunt","t hunt <Địa điểm>",'Có 2 địa điểm: "**africa**" (a) và "**oceania**" (o). Tuy nhiên hiện chỉ có thể săn ở "**africa**". Để đi săn, bạn cần có súng và đạn tương ứng (Xem ở <t shop>). Khi sử dụng, bot sẽ đợi cho đến khi bạn tìm được thú ngẫu nhiên. Khi đã tìm được, bot sẽ hiện lên một bảng gồm: **Con vật tìm được**, **Máu**, **Bảng chọn súng** và **Nút tương tác**.\nMỗi con vật đều có lượng **máu** và **thời gian chiến đấu nhất định**. Khi bạn đã chọn súng và nạp đạn, bạn có thể bắn. Khi bắn, con vật sẽ mất máu tương ứng với **sát thương vũ khí** của bạn (xem được trong lúc chọn súng), phát bắn có thể **Chí mạng** (15% - x2 sát thuơng) hoặc **HEADSHOT** (5% - x10 sát thương), mỗi lần bắn tốn 1 viên đạn và 1 độ bền của súng. Mỗi loại súng đều có **độ chính xác** riêng nên phát bắn có thể bị hụt.\nKhi con vật hết máu, bạn sẽ săn được nó. **Nếu quá thời gian chiến đấu của con vật**, nó sẽ bỏ chạy và bạn sẽ không nhận được gì nên bạn cần chọn loại súng phù hợp. Thú sau khi săn được lưu trong kho đồ của bạn (dùng <t kho> để xem)',3)

    sell = ban
    buy = mua
    kho = inventory
    inv = inventory
    ldb = leaderboard
    smm = somayman
    qhq = quayhoaqua
    bc = baicao
    tlmn = tienlen
    bnke = bankearn
    gf = gofish
    fishing = gofish
    gofishing = gofish
    top = ldb

def setup(client):
    client.add_cog(Help(client))