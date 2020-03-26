import random
#step 1
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}
playing = True

#step 2
class Card:
    def __init__(self,rank, suit):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank+' of '+self.suit

cardtest = Card(random.choice(ranks),random.choice(suits))

#step 3
class Deck:
    def __init__(self):
        self.deck = [] #empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(rank,suit))
    def __str__(self):
        deckcomp = ''
        for card in self.deck:
            deckcomp += '\n'+card.__str__()
        return 'the deck has:'+deckcomp
    def shuffle(self):
        random.shuffle(self.deck)
    def deal(self):
        single_card = self.deck.pop()
        return single_card


#step 4
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    def add_card(self,card):
        #card passed in from deck.deal
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

class Chips:
    def __init__(self,total=100):
        #hardcode total to always be the same
        self.total = total
        self.bet = 0
    def win_bet(self):
        self.total += self.bet
    def lose_bet(self):
        self.total -= self.bet

chip_amount = Chips()
#chip_amount.win_bet()

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('how much are you betting?'))
        except:
            print('sorry. please type a number')
        else:
            if chips.bet > chips.total:
                print('cant bet that. you only have {}'.format(chips.total))
            else:
                break

def hit(deck,hand): #dealer must stay at 17 or higher
    pulled_card = deck.deal()
    hand.add_card(pulled_card)
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing # to control while loop
    while True:
        x = input('hit or stand? pick H or S:  ')
        if x == 'H':
            hit(deck,hand)
        elif x == 'S':
            print('player stands; dealers turn')
            playing = False
        else:
            print('try again. pick H or S')
            continue
        break

def show_some(player,dealer):
    print('dealers hand:')
    print('one card hidden.')
    print(dealer.cards[1])
    print('\n')
    print('players hand:')
    for card in player.cards:
        print(card)

def show_all(player,dealer):
    print('dealers hand:')
    for card in dealer.cards:
        print(card)
    print('\n')
    print('players hand:')
    for card in player.cards:
        print(card)


def player_busts(player,dealer,chips):
    print('bust! sorry')
    chips.lose_bet()
def player_wins(player,dealer,chips):
    print('nice job. you win!')
    chips.win_bet()
def dealer_busts(player,dealer,chips):
    print('dealer busts. you win!')
    chips.win_bet()
def dealer_wins(player,dealer,chips):
    print('dealer wins. sorry.')
    chips.lose_bet()
def push(player,dealer):
    print('dealer and player tied')

while True:
    print('welcome to blackjack.')
    #create and shuffle deck
    deck = Deck()
    deck.shuffle()
    #create players hand
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    BlackJackCheck = player_hand.value()
    #create dealers hand
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    #set up players chips
    player_chips = Chips()
    #prompt player for bet
    take_bet(player_chips)
    #show cards (but keep dealers hidden
    show_some(player_hand,dealer_hand)
                #if blackjackcheck = 21
                #print(Blackjack! player wins!)
                #player_wins(player_hand,dealer_hand,player_chips)
                #playing = False
    while playing:
        #prompt player to hit or stand
        hit_or_stand(deck,player_hand)
        #show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)
        #if player hands exceeds 21, run player_busts() and break out of while loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
        break

    #if player hasn't busted, play Dealer's hand until dealer reaches 17
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)
        #show all cards
        show_all(player_hand,dealer_hand)
        #run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)

    #inform player of chips total
    print('\n Player total chips are at: {}'.format(player_chips.total))
    #ask to play again
    new_game = input('play again? Y or N: ')
    if new_game == 'Y':
        playing = True
        continue
    else:
        print('Thanks for playing')
        break

# add blackjack win functionality
# if value of first two player cards = 21, they instantly win