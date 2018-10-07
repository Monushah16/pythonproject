# for card shuffle
import random

#boolean is used to know if hand is in play
palying = False

chip_pool = 100 #could also make this a raw input

bet = 1

restart_phrase = "press 'd' to deal the cards again, or press 'q' to  quit"

#Hearts, diamonds , clubs, spades

suits = ('H','D','C','S')

#possible card ranks

ranking = ('a','2','3','4','5','6','7','8','9','10','J','Q','K')

#point valus dict
card_val = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}

#create a card class
class card:

     def __init__(self,suit,rank):
         self.suit = suit
         self.rank = rank

     def __str__(self):
         return self.suit + self.rank

     def grab_suit(self):
         return self.suit

     def grab_rank(self):
         return self.rank

     def draw(self):
         print(self.suit + self.rank)


# create a hand class
class Hand:

     def __init__(self):
         self.cards = []
         self.value = 0
         #aces can be 1 or 11 so need to define it here
         self.ace = False

     def __str__(self):
         ''' return a string of current hand composition'''
         hand_comp = " "

         for card in self.cards:
             card_name = card.__str__()
             hand_comp += " " + card_name

         return 'the hand has %s' %hand_comp

     def card_add(self,card):
         '''add another card to the hand'''
         self.cards.append(card)

         #check for aces
         if card.rank == 'A':
             self.ace = True
         self.value += card_val[card.rank]

     def calc_val(self):
         '''calculate the value of the hand , make aces an 11 if they dont bust the hand'''
         if(self.ace == True and self.value <12):
             return self.value +10
         else:
             return self.value

     def draw(self,hidden):
         if hidden == True and palying == True:
             starting_card = 1
         else:
             starting_card = 0
         for x in range(starting_card, len(self.cards)):
             self.cards[x].draw()


class deck:

    def __init__(self):
        '''create a deck in order'''
        self.deck= []
        for suit in suits:
            for rank in ranking:
                self.deck.append(card(suit, rank))

    def shuffle(self):
        '''shuffle the deck, python actually already have shufffle method in it lib'''
        random.shuffle(self.deck)

    def deal(self):
        '''grab the first item in a deck'''
        single_card = self.deck.pop()
        return single_card

    def __str__(self):
        deck_comp = " "
        for card in self.cards:
            deck_comp += " " + deck_comp.__str__()

        return "the deck has" + deck_comp


#first bet

def make_bet():
    '''ask the player for the bet amount and'''

    global bet
    bet = 0

    print ('what amount of cips would you like to bet? (enter the whole integer')

    #while loop to keep asking for the bet
    while bet ==0 :
        bet_comp = input() #use bet_comp as a checker
        bet_comp = int(bet_comp)

        #check to make sure the bet is within the remaining amount of chips left
        if bet_comp >=1 and bet_comp <= chip_pool:
            bet = bet_comp
        else:
            print("invalid bet, you only have "+ str(chip_pool)+ "remaining")




#make the function setting up the game and for dealing the cards.

def deal_cards():
    '''this function deal out cards and sets up round'''

    #set up all global variables
    global result,playing,deck,player_hand,dealer_hand,chip_pool,bet

    #create a deck
    deck = Deck()

    #shuffle it
    deck.shuffle()

    #set up bet
    make_bet()

    #set up both player and dealer hands
    player_hand = Hand()
    dealer_hand = Hand()

    #deal out initial cards
    player_hand.card_add(deck.deal())
    player_hand.card_add(deck.deal())

    dealer_hand.card_add(deck.deal())
    dealer_hand.card_add(deck.deal())

    result = "Hit or stand ? press either h or s:"

    if playing == True:
        print('fold,sorry')
        chip_pool -=bet

    #set up to know currrently playing hand
    playing = True
    game_step()


def hit():
    '''imlements the hit button '''
    global playing,chip_pool,deck,player_hand,dealer_hand,result,bet

    #if hand is in play add card
    if playing:
        if player_hand.calc_val()<= 21:
            player_hand.card_add(deck.deal())

        print("player hand is %s" %player_hand)

        if player_hand.calc_val() > 21:
            result = 'Busted!' + restart_phrase

            chip_pool -=bet
            playing = False

    else:
        result = "sorry, can't hit" + restart_phrase

    game_step()


#now make the stand function

def stand():
    global playing, chip_pool,deck,player_hand,dealer_hand,result,bet
    '''this fnctn will now play the dealers hand , since stand was choosen'''

    if playing== False:
        if player_hand.calc_val>0:
            result = "sorry , you can't stand!"

    # now go through all other possible options
    else:
        while dealer_hand.calc_val()<17:
            dealer_hand.card_add(deck.deal())

        if dealer_hand.calc_val()>21:
            result = 'dealer busts! you win!' + restart_phrase
            chip_pool += bet
            playing =False

        elif dealer_hand.calc_val() < player_hand.calc_val():
            result = 'you beat the dealer , you win!' + restart_phrase
            chip_pool += bet
            playing = False

        elif dealer_hand.calc_val() == player_hand.calc_val():
            result = ' Tied up, push!' + restart_phrase
            playing= False

        else:
            result = 'dealer wins!' + restart_phrase
            chip_pool -= bet
            playing = False

    game_step()


# function to print result and ask user for next step

def game_step():
    'function tp print game step/status on output'

    #dispplay player hand
    print("")
    print('player hand is: '),
    player_hand.draw(hidden=False)

    print('player hand total is: ' + str(player_hand.calc_val()))

    print('dealer hand is:'),
    dealer_hand.draw(hidden= True)

    if playing == False:
        print(" --- for a total of " + str(dealer_hand.calc_val()))
        print("chip total: "+ str(chip_pool))
    else:
        print("with another card hidden upside down")

    print(result)

    player_input()


#function for exiting the game

def game_exit():
    print("thanks for playing!")
    exit()


#function to read user input

def player_input():
    '''read user input, lower case it just to be safe'''

    plin = input().lower()


    if plin == 'h':
        hit()
    elif plin == 's':
        stand()
    elif plin=='d':
        deal_cards()
    elif plin=='q':
        game_exit()
    else:
        print("Invalid input...Enter h,s,d,or q:")
        player_input()



#make quick inntro of the game

def intro():
    statement = '''Welcome to BlackJack! Get as close to 21 as you can without going over!
        Dealer hits until she reaches 17. Aces count as 1 or 11.
        Card output goes a letter followed by a number of face notation'''
    print(statement)


#now to play game

deck = Deck()
deck.shuffle()
player_hand = Hand()
dealer_hand = Hand()
intro()
deal_cards()