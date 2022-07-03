import random


my_data = {
    'random_computer_names': 'Dimo,Ivan,Georgi,Darth Vader,Jack Sparrow,Queen Elizabeth II,Bugs Bunny,Clyde,Lola,Elena,Dog,Cat,Kraken,Baba Yaga,Ra,Anubis,Angelica,Albena,Peter the Great'.split(','),
}
total_players = 0


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
            my_data['player'+str(x+1)] = Player(name,dices_generator(),total_players,True,True)
        #generating computer players
        else:
            name = get_random_computer_name()
            print("Hello player {}, your name is {}.".format((x+1),name))
            my_data['player'+str(x+1)] = Player(name,dices_generator(),total_players,False,True)


def get_random_computer_name():
    name = random.choice(my_data['random_computer_names'])
    my_data['random_computer_names'].remove(name)
    return name


class Player:
    def __init__(self,name,dices,total_players,isHuman,isActive):
        self.name = name
        self.dices = dices
        self.total_players = total_players
        self.isHuman = isHuman
        self.isActive = isActive

    def play(self):
        result = []
        print("{}, it's your time to bid:".format(self.name))
        print("Please choose a dice number from 1 to 6")
        while True:
            bid_number = input()
            if not bid_number.isdigit():
                print("Please enter a digit")
            elif bid_number.isdigit():
                if int(bid_number) not in range(1,7):
                    print("Please choose a dice number from 1 to 6 asdas")
                else:
                    result.append(bid_number)
                    break

        max_quantity_range = self.total_players*5
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



while True:
    #Checking for a winner
    active_players = []
    for x in range(total_players):
        if my_data['player'+str(x+1)].isActive:
            active_players.append(my_data['player'+str(x+1)])
    #WINNER!
    if len(active_players) == 1:
        print("Great job, {}! YOU WIN!".format(active_players[0].name))
        print("You have {} dices left.".format(active_players[0].dices))
        print("Your reward is 1 banana.")
        break
    #No winner
    else:
        #PLAY THE GAME


    







'''
print(my_data['player1'].name)
print(my_data['player1'].dices)
print(my_data['player1'].total_players)
print(my_data['player2'].name)
print(my_data['player2'].dices)
print(my_data['player2'].total_players)
'''