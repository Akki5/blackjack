# CodeSkulptor runs Python programs in your browser.
# Click the upper left button to run this simple demo.

# CodeSkulptor runs in Chrome 18+, Firefox 11+, and Safari 6+.
# Some features may work in other browsers, but do not expect
# full functionality.  It does NOT run in Internet Explorer.

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ['C', 'S', 'H', 'D']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank
    
    def __str__(self):
        return self.suit + self.rank
    
    def get_suit(self):
        return self.suit
    
    def get_rank(self):
        return self.rank
    
    def draw(self, canvas, pos):
        i = RANKS.index(self.rank)
        j = SUITS.index(self.suit)
        card_loc=[CARD_CENTER[0] + i * CARD_SIZE[0],
                  CARD_CENTER[1] + j * CARD_SIZE[1]]
        if pos==[108,256] and in_play==True:
            card_loc = [108, 48]
            canvas.draw_image(card_back, card_loc, CARD_SIZE, pos, CARD_SIZE)
        else:
            canvas.draw_image(card_images, card_loc, CARD_SIZE, pos, CARD_SIZE)
    
    
# define hand class
class Hand:
    def __init__(self):
        self.cards_list=[]
        
    def __str__(self):
        res="Hand contains"
        for card in self.cards_list:
            res = res + " " + str(card)
        return res
            
    def add_card(self,card):
        self.cards_list.append(card)
    
    def get_value(self):
        value = 0
        for card in self.cards_list:
            value = value + VALUES[card.get_rank()]
        return value
    
    def draw(self, canvas, pos):
        for card in self.cards_list:
            card.draw(canvas, pos)
            pos[0] = pos[0] + 100
    
# define deck class
class Deck:
    def __init__(self):
        self.cards_list=[]
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit,rank)
                self.cards_list.append(card)
        self.shuffle()
        
    def shuffle(self):
        random.shuffle(self.cards_list)
    
    def deal_card(self):
        return self.cards_list.pop()
    
    def __str__(self):
        res="Deck contains"
        for card in self.cards_list:
            res = res + " " + str(card)
        return res
            

# event handlers
def deal():
    global in_play,deck,player_hand,dealer_hand
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    in_play = True

def hit():
    global outcome,in_play,score
    if in_play:
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = "You busted and lost."
            in_play=False
            score = score - 1

def stand():    
    global outcome,in_play,score
    if in_play == True:
        while dealer_hand.get_value()<17:
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.get_value() > 21:
            outcome = "Dealer busted and lost."
            in_play = False
            score = score + 1
        else:
            if dealer_hand.get_value() >= player_hand.get_value():
                outcome = "Dealer won."
                in_play = False
                score = score - 1 
            else:
                outcome = "You won."
                in_play = False
                score = score + 1
    
# Handler to draw on canvas
def draw(canvas):
    # write blackjack and score
    canvas.draw_text("Blackjack",[100,100],50,"Cyan")
    canvas.draw_text("Score " + str(score),[400,100],30,"Black")
    
    # dealer's hand
    canvas.draw_text("Dealer",[72,170],30,"Black")
    canvas.draw_text(outcome,[230,170],30,"Black")
    dealer_hand.draw(canvas,[108,256])
    
    # playes's hand
    canvas.draw_text("Player",[72,366],30,"Black")
    if in_play:
        canvas.draw_text("Hit or stand?",[230,366],30,"Black")
    else:
        canvas.draw_text("New deal?",[230,366],30,"Black")
    player_hand.draw(canvas,[108,452])

deck = Deck()
dealer_hand = Hand()
player_hand = Hand()
deal()


# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal",deal,200)
frame.add_button("Hit",hit,200)
frame.add_button("Stand",stand,200)
frame.set_draw_handler(draw)

# Start the frame animation
frame.start()
