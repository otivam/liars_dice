import random
from itertools import count,dropwhile
from xml.etree.ElementTree import TreeBuilder


players_data = {}
random_computer_names = 'Dimo,Ivan,Georgi,Darth Vader,Jack Sparrow,Queen Elizabeth II,Bugs Bunny,Clyde,Lola,Elena,Dog,Cat,Kraken,Baba Yaga,Ra,Anubis,Angelica,Albena,Peter the Great'.split(',')
total_players = 0
bids_data = {}



def new_game_dices(all_players_dices):
    total_dices = len(all_players_dices)
    dices = []
    for x in range(total_dices):
        for y in range(1,7):
            dices.append(str(x+1)+str(y))
    return dices




def dices_generator():
    dices = []
    for x in range(0,5):
        dices.append(random.randint(1,6))
    return dices


def players_generator(total_players,computer_players):
    for x in range(total_players):
        #generating human players
        if x < int(total_players) - int(computer_players):
            print("Hello player {}, what is your name ?".format(x+1))
            name = input()
            players_data['player'+str(x+1)] = Player(name,dices_generator(),total_players,True,True)
        #generating computer players
        else:
            name = get_random_computer_name()
            print("Hello player {}, your name is {}.".format((x+1),name))
            players_data['player'+str(x+1)] = Player(name,dices_generator(),total_players,False,True)



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

    max_quantity_range = total_players*5
    print("How many '{}'s:".format(bid_number))
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
    return result


def display_dices_with_x(dice):
    return dice[:-1]+'x'+dice[-1]


def all_players_dices():
    all_players_dices = []
    for x in range(int(total_players)):
        all_players_dices.extend(players_data['player'+str(x+1)].dices)
    return all_players_dices



def all_players_dices_grouped(all_players_dices):
    all_players_dices_grouped = {}
    for x in all_players_dices:
        all_players_dices_grouped[x] = all_players_dices.count(x)
    return all_players_dices_grouped





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
            print("{}, it's your time to bid:".format(self.name))
            
            result = get_the_dice_combination(self.total_players)
            if ''.join(result[::-1]) not in current_round_dices:
                print("Your choise is not valid! Please enter new combination.")
                result = get_the_dice_combination(self.total_players)
        else:
            #TO DO -> bot logic
            pass

        return ''.join(result[::-1])

    def remove_dice(self):
        self.dices.pop()

    def __len__(self):
        return len(self.dices)



######################
#### GAME PLAY #######
######################
print("Welcome to Liars dice, let's begin...")
print("Please enter the total players:")
while True:
    total_players = input()
    if not total_players.isdigit():
        print("Please enter a digit")
    elif total_players.isdigit():
        if int(total_players) < 2:
            print("The game is played by two or more players.")
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



new_game = True

while new_game:
    current_round_dices = new_game_dices(all_players_dices())
    first_player = True
    last_player = {}
    new_round = True
    while new_round:
        #Checking for a winner
        active_players = []
        for x in range(int(total_players)):
            if players_data['player'+str(x+1)].isActive:
                active_players.append(players_data['player'+str(x+1)])
        #WINNER!
        if len(active_players) == 1:
            print("Great job, {}! YOU WIN!".format(active_players[0].name))
            print("You have {} dices left.".format(active_players[0].dices))
            print("Your reward is quarter piece of banana.")
            new_game = False
        #No winner
        else:
            #PLAY THE GAME
            for x in range(int(total_players)):
                player = players_data['player'+str(x+1)]
                print("Available dice combinations:")
                print(list(map(display_dices_with_x,current_round_dices)))
                print("Your dices:")
                print(player.dices)
                if first_player:
                    player_bid = player.play_bid(current_round_dices)
                    bids_data['bid_'+str(player.id)] = player_bid
                    last_player['bid'] = player_bid
                    last_player['attr'] = player
                    current_round_dices = game_dices_reducer(current_round_dices,player_bid)
                    first_player = False
                else:
                    print("Last player bid: "+display_dices_with_x(last_player['bid']))
                    print(player.name + ", it's your turn. 'liar' or 'bid' ?")
                    while True:
                        liar_or_bid = input()
                        if not liar_or_bid.isalpha():
                            print("Use only letters.")
                        elif liar_or_bid.isalpha():
                            if liar_or_bid.lower() == 'liar':
                                #Liar logic - challenger(current player) wins, bidder lose 1 dice
                                if all_players_dices_grouped(all_players_dices())[int(last_player['bid'][-1])] != int(last_player['bid'][:-1]):
                                    players_data['player'+str(last_player['attr'].id)].remove_dice()
                                    print("{}, you lost 1 dice! Time for a new round.".format(last_player['attr'].name))
                                    new_round = False
                                    break
                                #Liar logic - bidder(last player) wins, challenger lose 1 dice
                                else:
                                    print(all_players_dices())
                                    print("{}, you lost 1 dice! Time for a new round.".format(player.name))
                                    player.remove_dice()
                                    new_round = False
                                    break
                            elif liar_or_bid.lower() == 'bid':
                                player_bid = player.play_bid(current_round_dices)
                                bids_data['bid_'+str(player.id)] = player_bid
                                last_player['bid'] = player_bid
                                last_player['attr'] = player
                                current_round_dices = game_dices_reducer(current_round_dices,player_bid)
                                break
                            else:
                                print("Choose between 'liar' and 'bid'")
                        

                    
            


    







