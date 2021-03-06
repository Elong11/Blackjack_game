import random

# global variables to be accessed
# suits tuples
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')

ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

# values is very important as you can lookup the rank and see its value and add the sum of the persons hand
# dictionary for values rank of card to get the value
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}

# if the game is over this will be changed to false
playing = True


class Card():

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))  # build Card objects and add them to the list

    def __str__(self):
        deck_comp = ''  # start with an empty string
        for card in self.deck:
            deck_comp += '\n ' + card.__str__()  # add each Card object's print string
        return 'The deck has:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


# test_deck = Deck()
# test_deck.shuffle()
# print(test_deck)


# The HAND CLASS is where these can be used
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        # card passed in from Deck.deal() -> 1 card
        self.cards.append(card)
        self.value += values[card.rank]

        # track aces
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):

        # when you first get an ace it will count as 11
        # this will check if the self.value is over 21 and I have an ace
        # will be changed to a 1
        # the self.aces = 0 is being used as a boolean
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


# TESTING TESTING TESTING TESTING TESTING TESTING TESTING TESTING

test_deck = Deck()
test_deck.shuffle()


# print(test_deck)

# PLAYER
# test_player = Hand()

# Deal 1 card from the deck CARD(suit,rank)
# pulled_card = test_deck.deal()
# print(pulled_card)
# test_player.add_card(pulled_card)
# print(test_player.value)

# TESTING TESTING TESTING TESTING TESTING TESTING TESTING TESTING
# ALL OF THE ABOVE TESTING COULD BE WRITTEN
# test_player.add_card(test_deck.deal())
# print(test_player.value)


class Chips():

    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_best(self):
        self.total -= self.bet


def take_bet(chips):
    while True:

        try:
            chips.bet = int(input('How many chips would you like to bet?'))
        except ValueError:
            print('Sorry please provide an integer')
        else:
            if chips.bet > chips.total:
                print('Sorry you have insufficient chips! You have: {}'.format(chips.total))
            else:
                break


# takes the deck and a hand (deck,hand)
def hit(deck, hand):
    # deals a single card from the deck
    single_card = deck.deal()
    # adds that card dealt to the hand
    hand.add_card(single_card)
    # checks for an ace adjustment
    hand.adjust_for_ace()


#
def hit_or_stand(deck, hand):
    global playing  # to control an upcoming while loops3

    while True:
        x = input('Hit or Stand?  Enter h or s ')

        if x[0].lower() == 'h':
            hit(deck, hand)

        elif x[0].lower() == 's':
            print("Player Stands Dealer's Turn")
            playing = False

        else:
            print('Sorry, I did not understand that, Please enter h for Hit or s for stand')
            continue

        break


def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')


def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)


def player_busts(player, dealer, chips):
    print('PLAYER BUSTS!')
    chips.lose_best()
    pass


def dealer_busts(player, dealer, chips):
    print('DEALER BUSTS!  PLAYER WINS! ')
    chips.win_bet()
    pass


def player_wins(player, dealer, chips):
    print('PLAYER WINS!')
    chips.win_bet()
    pass


def dealer_wins(player, dealer, chips):
    print('PLAYER BUSTS!')
    chips.lose_best()
    pass


# this means tie, no need for chips
def push(player, dealer):
    print('DEALER AND PLAYER TIE!  ITS A PUSH!')


while True:
    # Print an opening statement
    print('Welcome to BLACKJACK')

    # Create and shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    # Deal cards to the Player   two of them
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    # Deal cards to the Dealer   two of them
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Setup the Players Chips

    players_chips = Chips()

    # Prompt the Player for their bet
    take_bet(players_chips)

    # Show cards (but keep one dealer card hidden)

    show_some(player_hand, dealer_hand)

    # recall this variable from the hit_or_stand function
    while playing:

        # Prompt player to hit or stand
        hit_or_stand(deck, player_hand)

        # Show cards (but hide one of the dealers)
        show_some(player_hand, dealer_hand)

        # If player's hand exceeds 21, run player_buists() and break out of the loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, players_chips)

            break

    # If the player hasn't busted, player dealers hand until dealer reaches 17
    if player_hand.value <= 21:

        while dealer_hand.value < player_hand.value:
            hit(deck, dealer_hand)

            # Show all cards
            show_all(player_hand, dealer_hand)

            # Run different winning scenarios
            if dealer_hand > 21:
                dealer_busts(player_hand, dealer_hand, players_chips)
            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand, dealer_hand, players_chips)
            elif dealer_hand.value < player_hand.value:
                player_wins(player_hand, dealer_hand, players_chips)
            else:
                push(player_hand, dealer_hand)

    print("\n Player's total chips are at : {}".format(players_chips.total))

    # Ask to play again
    new_game = input('Would you liek to play another hand? y/n')

    if new_game[0].lower == 'y':
        playing = True
        continue
    else:
        print('Thank you for playing!')
        break
