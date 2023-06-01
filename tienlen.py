import random

class Card:

    def __init__(self, user):
        if user == "main":
            self.instant_win_player = None
            self.check_point = None
            self.matchEnd = False
            self.starter_cards = []
            self.playerList = []
            self.onTable_cards = []
            self.selected_cards = []
            self.winners = []
            self.ranks = [":one:", ":two:", ":three:", ":four:"]
            self.btn = []
        else:
            self.outside_message = None
            self.original_cards = []
            self.user = user
            self.cards = []
            self.turn = False
            self.DMmessage = None
            self.DMmessage_turn = None
            self.skipped = False
            self.temp = None
            self.rank = ""
            self.money = 0
            self.bonus_money = int(0)
            self.bonus_message = " "

    fullCards = ['<:3bich:856077372993175552>', '<:3chuong:856067108768448512>','<:3ro:856067108681416744>','<:3co:856067108362256415>','<:4bich:856067108449288234>','<:4chuong:856067108705533972>',
            '<:4ro:856067108751802368>','<:4co:856067108647731240>','<:5bich:856067108420714527>','<:5chuong:856067108776181760>','<:5ro:856067108353474571>',
            '<:5co:856067108751671316>','<:6bich:856067108756258846>','<:6chuong:856067108751540234>','<:6ro:856067108763729920>','<:6co:856079612014493696>',
            '<:7bich:856067108760584223>','<:7chuong:856067108773560340>','<:7ro:856067108760846336>','<:7co:856080166786957313>','<:8bich:856067108463312908>',
            '<:8chuong:856067110454427658>','<:8ro:856067108764778546>','<:8co:856080754147983360>','<:9bich:856080960859930644>','<:9chuong:856067108868980746>',
            '<:9ro:856067108857577492>','<:9co:856081329795891240>','<:10bich:856067108789551104>','<:10chuong:856067108767793182>','<:10ro:856067108773429258>',
            '<:10co:856067108395417621>','<:Jbich:856081880659132416>','<:Jchuong:856067108764516392>','<:Jro:856067108773298206>','<:Jco:856082311778402304>',
            '<:Qbich:856067108769497088>','<:Qchuong:856067108776181790>','<:Qro:856067108765302814>','<:Qco:856067108780376084>','<:Kbich:856067108332765215>',
            '<:Kchuong:856067108759928852>','<:Kro:856067108814716938>','<:Kco:856067108793876490>','<:Abich:856065246510186537>','<:Achuong:856065246573756426>',
            '<:Aro:856065246531813386>','<:Aco:856065246548590592>','<:2bich:856067108618108959>','<:2chuong:856067108756652052>','<:2ro:856067108752588840>','<:2co:856067108319002625>']

    @staticmethod
    def getRankMoney(rank : str, player_amount : int, money_amount : int):
        switcher = {
        2:{
            ":one:": money_amount,
            ":two:": -money_amount
            },
        3:{
            ":one:": money_amount,
            ":two:": 0,
            ":three:": -money_amount,
            },
        4:{
            ":one:": money_amount,
            ":two:": money_amount/2,
            ":three:": -money_amount/2,
            ":four:": -money_amount,
            }
        }
        return int(switcher[player_amount][rank])


    @staticmethod
    def getSortedCards(cards):
        RealValueList = []
        for card in cards:
            RealValueList.append(Card.getRealValue(card))

        RealValueList.sort()
        SortedCards = []

        for cardValue in RealValueList:
            for card in cards:
                if Card.getRealValue(card) == cardValue: SortedCards.append(card)

        return SortedCards



    @staticmethod
    def getShuffleCards():
        cards = Card.fullCards.copy()
        for i in range(0,7):
            random.shuffle(cards)
        return cards

    @staticmethod
    def getIntValue(card):
        if card[3] == '0': return 7
        switcher = {
        "3" : 0,
        "4" : 1,
        "5" : 2,
        "6" : 3,
        "7" : 4,
        "8" : 5,
        "9" : 6,
        "J" : 8,
        "Q" : 9,
        "K" : 10,
        "A" : 11,
        "2" : 12,
        }
        return switcher[card[2]]

    @staticmethod
    def getRealValue(card):
        if "bich" in card: return float(Card.getIntValue(card)) + 0.1
        if "chuong" in card: return float(Card.getIntValue(card)) + 0.2
        if "ro" in card: return float(Card.getIntValue(card)) + 0.3
        if "co" in card: return float(Card.getIntValue(card)) + 0.4

    @staticmethod
    def getType(cards):
        int_cards = []
        for card in cards:
            int_cards.append(Card.getIntValue(card))

        def isAllCardSameInt(cards):
            base_check = cards[0]
            for card in cards:
                if card != base_check:
                    return False
            return True

        def isIncreasingOne(cards):
            for i in range(0, len(cards)):
                try:
                    card = cards[i]
                    next_card = cards[i+1]
                    if next_card - card != 1:
                        return False
                except IndexError:
                    return True

        def isDoiThong(cards):
            if len(cards) < 6: return False
            for i in range(1, len(cards),2):
                try:
                    if not ( isIncreasingOne([cards[i],cards[i+1]]) and isAllCardSameInt([cards[i-1],cards[i]]) ):
                        return False
                except IndexError:
                    return True

        if 12 in int_cards:
            switcher = {
            12:"Heo1",
            24:"Heo2",
            36:"Heo3"
            }
            if sum(int_cards) != 12 and sum(int_cards) != 24 and sum(int_cards) != 36:
                return "invalid"
            return switcher[sum(int_cards)]

        if isIncreasingOne(int_cards) and len(int_cards)>=3 and 12 not in int_cards:
            return "Sanh"
        if isAllCardSameInt(int_cards) and len(int_cards) in range(2,5):
            switcher = {
            4:"TuQuy",
            3:"BaLa",
            2:"Doi"
            }
            return switcher[len(int_cards)]
        if isDoiThong(int_cards) and 12 not in int_cards:
            switcher = {
            6:"BaDoiThong",
            8:"BonDoiThong",
            10:"NamDoiThong"
            }
            return switcher[len(int_cards)]
        if len(cards)==1:
            return "Mua"
        return "invalid"

    @staticmethod
    def isPassRule(cards, onTable_cards, money_amount, main):
        if cards == [] : return False
        cards = Card.getSortedCards(cards)
        #check selectedCards
        if len(cards) > 1:
            if len(cards) == 2 and Card.getIntValue(cards[0]) != Card.getIntValue(cards[1]):
                return False
            for i in range(0, len(cards)):
                if (i==len(cards)-1): break

                if Card.getRealValue(cards[i+1]) - Card.getRealValue(cards[i]) > 1.4: return False

        def check_bonus_plus(message):
            money_add = 0
            for player in main.playerList:
                if onTable_cards[0] in player.original_cards:
                    player.bonus_money -= money_amount
                    money_add = money_amount
                    player.bonus_message += message
            for player in main.playerList:
                if cards[0] in player.original_cards:
                    player.bonus_money += money_add

        def check_bonus(message):
            money_add = 0
            for player in main.playerList:
                if onTable_cards[0] in player.original_cards:
                    for card in onTable_cards:
                        if Card.getRealValue(card) == 12.1 or Card.getRealValue(card) == 12.2:
                            player.bonus_money -= (money_amount/2)
                            money_add = money_amount/2
                            player.bonus_message += message
                        if Card.getRealValue(card) == 12.3 or Card.getRealValue(card) == 12.4:
                            player.bonus_money -= money_amount
                            money_add = money_amount
                            player.bonus_message += message
            for player in main.playerList:
                if cards[0] in player.original_cards:
                    player.bonus_money += money_add

        #compare selected cards with on table cards
        def sumCardsValue(cards):
            sum_value = 0.0
            for card in cards:
                sum_value += Card.getRealValue(card)
            return sum_value
        if Card.getType(cards) == "invalid":
            return False
        if onTable_cards != []:
            if Card.getType(cards) == "BaDoiThong" and Card.getType(onTable_cards) == "Heo1":
                check_bonus("Bị chặt 2.")                           
                return True
            if Card.getType(cards) == "TuQuy" and (Card.getType(onTable_cards) == "Heo1" or Card.getType(onTable_cards) == "Heo2"):
                check_bonus("Bị chặt 2. ")                           
                return True
            if Card.getType(cards) == "BonDoiThong" and (Card.getType(onTable_cards) == "Heo1" or Card.getType(onTable_cards) == "Heo2"):
                check_bonus("Bị chặt 2. ") 
                return True
            if Card.getType(cards) == "NamDoiThong" and (Card.getType(onTable_cards) == "Heo1" or Card.getType(onTable_cards) == "Heo2" or Card.getType(onTable_cards) == "Heo3"):
                check_bonus("Bị chặt 2. ") 
                return True
            if Card.getType(cards) == "BaDoiThong" and Card.getType(cards) == Card.getType(onTable_cards):
                if Card.getRealValue(cards[-1]) < Card.getRealValue(onTable_cards[-1]):
                    return False
                check_bonus_plus("Bị chặt hàng. ")
                return True
            if Card.getType(cards) == "TuQuy" and Card.getType(cards) == Card.getType(onTable_cards):
                if Card.getRealValue(cards[-1]) < Card.getRealValue(onTable_cards[-1]):
                    return False
                check_bonus_plus("Bị chặt hàng. ")
                return True
            if Card.getType(cards) == "BonDoiThong" and Card.getType(cards) == Card.getType(onTable_cards):
                if Card.getRealValue(cards[-1]) < Card.getRealValue(onTable_cards[-1]):
                    return False
                check_bonus_plus("Bị chặt hàng. ")
                return True
            if Card.getType(cards) == "NamDoiThong" and Card.getType(cards) == Card.getType(onTable_cards):
                if Card.getRealValue(cards[-1]) < Card.getRealValue(onTable_cards[-1]):
                    return False
                check_bonus_plus("Bị chặt hàng. ")
                return True

            if Card.getType(cards) == Card.getType(onTable_cards) or ((Card.getType(cards) == "Heo1" or Card.getType(cards) == "Heo2" or Card.getType(cards) == "Heo3") and Card.getType(onTable_cards) != "Sanh"):
                if len(cards) != len(onTable_cards):
                    return False
                if len(cards) >= 2 and Card.getRealValue(cards[-1]) > Card.getRealValue(onTable_cards[-1]):
                    return True
                elif sumCardsValue(cards) > sumCardsValue(onTable_cards) and len(cards) == 1:
                    return True
                else: return False
            
        else:
            return True
