import random
from itertools import count


players_data = {}
random_computer_names = 'Dimo,Ivan,Georgi,Darth Vader,Jack Sparrow,Bugs Bunny,Clyde,Lola,Elena,Dog,Cat,Kraken,Baba Yaga,Ra,Anubis,Angelica,Albena,Peter the Great'.split(',')
total_players = 0
bids_data = {}


def new_game_dices(all_players_dices):
    total_dices = len(all_players_dices)
    dices = []
    for x in range(total_dices):
        for y in range(1,7):
            dices.append(str(x+1)+str(y))
    return dices


def dices_generator(numOfDices):
    dices = []
    for x in range(0,numOfDices):
        dices.append(random.randint(1,6))
    return dices


def new_round_players_dices_generator():
    for x in range(int(total_players)):
        players_data['player'+str(x+1)].dices = dices_generator(
                                                len(players_data['player'+str(x+1)].dices))


def players_generator(total_players,computer_players):
    for x in range(total_players):
        #generating human players
        if x < int(total_players) - int(computer_players):
            print("Hello player {}, what is your name ?".format(x+1))
            pn_correct_inp = False
            while not pn_correct_inp:
                name = input()
                if not name:
                    print("Please enter your name")
                elif name:
                    players_data['player'+str(x+1)] = Player(name,dices_generator(5),
                                                      total_players,True,True)
                    pn_correct_inp = True
        #generating computer players
        else:
            name = get_random_computer_name()
            print("Hello player {}, your name is {}.".format((x+1),name))
            players_data['player'+str(x+1)] = Player(name,dices_generator(5),
                                              total_players,False,True)


def get_random_computer_name():
    if len(random_computer_names) >= 1:
        name = random.choice(random_computer_names)
        random_computer_names.remove(name)
    else:
        name = 'Unknown legend'
    return name


def game_dices_reducer(dices_arr,where_to_remover):
    idx = dices_arr.index(where_to_remover)
    new_list = dices_arr[idx+1:]
    return new_list


def get_the_dice_combination(total_players):
    result = []
    max_quantity_range = total_players*5
    print("Please choose your bid:")
    while True:
        bid_quantity = input()
        if not bid_quantity.isdigit():
            print("Please enter a digit")
        if bid_quantity.isdigit():
            if int(bid_quantity) not in range(1,max_quantity_range):
                print("Please choose a dice number from 1 to {}".format(max_quantity_range))
            else:
                result.append(bid_quantity)
                break

    print("Please choose a dice number from 1 to 6")
    while True:
        bid_number = input()
        if not bid_number.isdigit():
            print("Please enter a digit")
        elif bid_number.isdigit():
            if int(bid_number) not in range(1,7):
                print("Please choose a dice number from 1 to 6")
            else:
                result.append(bid_number)
                break
            
    return result


def display_dices_with_x(dice):
    return dice[:-1]+'x'+dice[-1]


def all_players_dices():
    all_players_dices = []
    for x in range(int(total_players)):
        all_players_dices.extend(players_data['player'+str(x+1)].dices)
    return all_players_dices


def all_players_dices_grouped(all_players_dices):
    all_players_dices_grouped = {
        1:0,
        2:0,
        3:0,
        4:0,
        5:0,
        6:0
    }
    for x in all_players_dices:
        all_players_dices_grouped[x] = all_players_dices.count(x)
    return all_players_dices_grouped


def players_order_generator(total_players):
    order_list = []
    for x in range(int(total_players)):
        order_list.append(players_data['player'+str(x+1)])
    return order_list


def new_players_order(isLoser,old_order_list):
    old_order_list.insert(0, old_order_list.pop(old_order_list.index(isLoser)))
    return old_order_list


def player_has_dices(dices):
    if len(dices) >= 1:
        return True


def check_winner():
    active_players = []
    for x in range(int(total_players)):
        if players_data['player'+str(x+1)].isActive:
            active_players.append(players_data['player'+str(x+1)])
            
    if len(active_players) == 1:
        print("Great job, {}! YOU WIN!".format(active_players[0].name))
        print("You have {} dices left.".format(len(active_players[0].dices)))
        print("Your reward is quarter piece of banana.")
        return True
      

def total_active_players():
    active_players = 0
    for x in range(int(total_players)):
        if players_data['player'+str(x+1)].isActive:
            active_players += 1
    return active_players


def bot_odds(bot_dices_grouped, 
            current_round_dices, 
            total_players):
    poss = {}
    range_to_check = 0
    
    if len(current_round_dices) > 10:
        range_to_check = 10
    else:
        range_to_check = len(current_round_dices)

    for x in range(range_to_check):
        y = 1 if (int(current_round_dices[x][:-1])
                - bot_dices_grouped[int(current_round_dices[x][-1])]) == 0 else (int(current_round_dices[x][:-1])
                - bot_dices_grouped[int(current_round_dices[x][-1])])
        poss[current_round_dices[x]] = ((((int(total_players)-1)*5)*1/6)*100)/y

    smallest_val = dict(sorted(poss.items(), key=lambda item: item[1]))
    poss = sorted(poss, key=poss.get, reverse=True)
    poss.append(list(smallest_val.items())[-1][1])
    return poss

    
def bot_dices_grp(bot_dices):
    bot_dices_grouped = {
        1:0,
        2:0,
        3:0,
        4:0,
        5:0,
        6:0
    }
    for x in bot_dices:
        bot_dices_grouped[x] = bot_dices.count(x)
    bot_dices_grouped = dict(sorted(bot_dices_grouped.items(), key=lambda item: item[1]))
    return bot_dices_grouped

        
def bot_play_his_bid(bot_dices, 
                    current_round_dices, 
                    total_players):
    result = []
    bot_dices_grouped = bot_dices_grp(bot_dices)

    for x in current_round_dices:
        value = int(x[-1])
        quantity = int(x[:-1])

        if bot_dices_grouped[value] >= quantity:
            print("Please choose your bid:")
            print(str(quantity))
            bid_quantity = str(quantity)
            result.append(bid_quantity)

            print("Please choose a dice number from 1 to 6")
            print(str(value))
            bid_number = str(value)
            result.append(bid_number)
            break

    if len(result) == 0:
        value = bot_odds(bot_dices_grouped, 
                        current_round_dices, 
                        total_players)[0][-1]
        quantity = bot_odds(bot_dices_grouped, 
                            current_round_dices, 
                            total_players)[0][:-1]
        
        print("Please choose your bid:")
        print(str(quantity))
        bid_quantity = str(quantity)
        result.append(bid_quantity)

        print("Please choose a dice number from 1 to 6")
        print(str(value))
        bid_number = str(value)
        result.append(bid_number)
           
    return result


def bot_liar_or_bid(bot_dices, 
                    current_round_dices, 
                    total_players):
    bot_dices_grouped = bot_dices_grp(bot_dices)

    if int(bot_odds(bot_dices_grouped, 
                    current_round_dices, 
                    total_players)[-1]) < 60:
        print('liar')
        return 'liar'
    else:
        print('bid')
        return 'bid'

    
class Player:
    _ids = count(1)

    def __init__(self,name,dices,total_players,isHuman,isActive):
        self.name = name
        self.dices = dices
        self.total_players = total_players
        self.isHuman = isHuman
        self.isActive = isActive
        self.id = next(self._ids)

    def play_bid(self,current_round_dices):
        if self.isHuman:            
            result = get_the_dice_combination(self.total_players)
            if ''.join(result) not in current_round_dices:
                print("Your choise is not valid! Please enter new combination.")
                result = get_the_dice_combination(self.total_players)
        else:
            result = bot_play_his_bid(self.dices, 
                                    current_round_dices, 
                                    total_players)

        return ''.join(result)

    def remove_dice(self):
        self.dices.pop()

    def __len__(self):
        return len(self.dices)


######################
#### GAME PLAY #######
######################
print("Welcome to Liars dice, let's begin...")
print("Should we activate the 'wild ones' mode? (yes/no)")
wo_correct_inp = False
while not wo_correct_inp:
    wo_input = input()
    if not wo_input.isalpha():
        print("Use only letters.")
    elif wo_input.isalpha() and wo_input in ['yes','no']:
        wo_correct_inp = True
    else:
        print("Choose between 'yes' and 'no'")

print("Please enter the total players:")
while True:
    total_players = input()
    if not total_players.isdigit():
        print("Please enter a digit")
    elif total_players.isdigit():
        if int(total_players) < 2:
            print("The game is played by two or more players.")
        elif int(total_players) > 8:
            print("Max 8 players.")
        else:
            break

print("And how many of them will be computer players?")
while True:
    computer_players = input()
    if not computer_players.isdigit():
        print("Please enter a digit")
    elif total_players.isdigit():
        if int(total_players) < int(computer_players):
            print("Computer players cannot be more than total players!")
        else:
            break

print("Very well! We will asign {} random computer players!".format(computer_players))
players_generator(int(total_players),int(computer_players))

new_players = players_order_generator(total_players)
new_game = True
first_round = True
last_player = {}

while new_game:
    current_round_dices = new_game_dices(all_players_dices())
    new_round = True
    while new_round:
        #PLAY THE GAME -> new player start his turn
        x = 0
        while x <= len(new_players):
            player = new_players[x]
            x += 1
            print("{}: Available dice combinations:".format(player.name.upper()))
            print(list(map(display_dices_with_x,current_round_dices)))
            print("Your dices:")
            print(player.dices)
            if first_round:
                player_bid = player.play_bid(current_round_dices)
                bids_data['bid_'+str(player.id)] = player_bid
                last_player['bid'] = player_bid
                last_player['attr'] = player
                current_round_dices = game_dices_reducer(current_round_dices,
                                                        player_bid)
                first_round = False
            else:
                correct_inp = False
                print("Last player bid: "+display_dices_with_x(last_player['bid']))
                print(player.name + ", it's your turn. 'liar' or 'bid' ?")
                while not correct_inp:
                    if not player.isHuman:
                        liar_or_bid = bot_liar_or_bid(player.dices, 
                                                    current_round_dices, 
                                                    total_active_players())
                    else:
                        liar_or_bid = input()

                    if not liar_or_bid.isalpha():
                        print("Use only letters.")
                    elif liar_or_bid.isalpha():
                        #LIAR
                        if liar_or_bid.lower() == 'liar':
                            bidder = players_data['player'+str(last_player['attr'].id)]
                            print(all_players_dices())
                            wo_yes = ((all_players_dices_grouped(all_players_dices())[int(last_player['bid'][-1])] 
                                    + all_players_dices_grouped(all_players_dices())[int(1)] 
                                    >= int(last_player['bid'][:-1])) 
                                    and wo_input == 'yes')
                            wo_no = ((int(all_players_dices_grouped(all_players_dices())[int(last_player['bid'][-1])]) 
                                    >= int(last_player['bid'][:-1])) 
                                    and wo_input == 'no')

                            if wo_no or wo_yes:
                                #IF ONE OF THESE IS TRUE
                                new_players = new_players_order(player,new_players)
                                print("{}, you lost 1 dice! Time for a new round.".format(player.name))
                                player.remove_dice()
                                if not player_has_dices(player.dices):
                                    player.isActive = False
                                    new_players.remove(player)
                                    print('{} is out of the game!'.format(player.name))
                            else:
                                new_players = new_players_order(bidder,new_players)
                                print("{}, you lost 1 dice! Time for a new round.".format(last_player['attr'].name))
                                bidder.remove_dice()
                                if not player_has_dices(bidder.dices):
                                    bidder.isActive = False
                                    new_players.remove(bidder)
                                    print('{} is out of the game!'.format(bidder.name))

                            x = 0
                            new_round_players_dices_generator()
                            current_round_dices = new_game_dices(all_players_dices())
                            new_round = False
                            first_round = True
                            if check_winner(): 
                                new_game = False
                                x = len(new_players) + 1
                        #BID
                        elif liar_or_bid.lower() == 'bid' and current_round_dices:
                            player_bid = player.play_bid(current_round_dices)
                            bids_data['bid_'+str(player.id)] = player_bid
                            last_player['bid'] = player_bid
                            last_player['attr'] = player
                            current_round_dices = game_dices_reducer(current_round_dices,
                                                                    player_bid)
                        else:
                            print("Choose between 'liar' and 'bid'")

                        correct_inp = True
            if x == len(new_players):x = 0
                
                        

                        

                    
            


    







