from Types.types import *
from game import *

import random
import numpy as np

"""
Spades:
    Ace
    King
    Jack
    6
    2
Hearts:
    Ace
    Queen
Clubs:
    King
    9
    5
    4
    3
Diamonds
    Queen
"""
# TODO: try to recreate betting scheme from paper
n = [Card(Suit.spade, 14),
     Card(Suit.spade, 13),
     Card(Suit.spade, 11),
     Card(Suit.spade, 6),
     Card(Suit.spade, 2),
     Card(Suit.heart, 14),
     Card(Suit.heart, 12),
     Card(Suit.club, 13),
     Card(Suit.club, 9),
     Card(Suit.club, 5),
     Card(Suit.club, 4),
     Card(Suit.club, 3),
     Card(Suit.diamond, 12)]

hands = {p: [] for p in Player}

hands[Player.north] = n

deck = SpadesState(Player.north).GetCardDeck()

deck = [card for card in deck if card not in n]
random.shuffle(deck)
for p in Player:
    if p != Player.north:
        hands[p] = deck[:13]
        deck = deck[13:]

print(hands)

table_1 = [[0.997, 0.966, 0.817],  # 0
           [0.994, 0.942, 0.733],  # 1
           [0.990, 0.907, 0.624],  # 2
           [0.983, 0.855, 0.489],  # 3
           [0.970, 0.779, 0.350],  # 4
           [0.948, 0.678, 0.212],  # 5
           [0.915, 0.544, 0.095],  # 6
           [0.857, 0.381, 0.025],  # 7
           [0.774, 0.214, 0],  # 8
           [0.646, 0.074, 0],  # 9
           [0.462, 0, 0],  # 10
           [0.227, 0, 0]]  # 11

# rows is the number of cards the player has of a given suit
table_1_mod = [[0, 0, 0],  # 0
               [0.994, 0, 0],  # 1
               [0.990, 0.907, 0],  # 2
               [0.983, 0.855, 0.489],  # 3
               [0.970, 0.779, 0.350],  # 4
               [0.948, 0.678, 0.212],  # 5
               [0.915, 0.544, 0.095],  # 6
               [0.857, 0.381, 0.025],  # 7
               [0.774, 0.214, 0],  # 8
               [0.646, 0.074, 0],  # 9
               [0.462, 0, 0],  # 10
               [0.227, 0, 0]]  # 11

a = np.asarray(table_1_mod)


def side_suit_high(table, suitHand):
    ret = []
    for card in suitHand:
        if card.val in [12, 13, 14]:
            num_of_suit = len(suitHand)
            ret.append(table[num_of_suit][14 - card.val])
    return ret


ssh = []
for suit in Suit:
    if suit != Suit.spade:
        sub = list(filter(lambda x: x.suit == suit, hands[Player.north]))
        ssh.extend(side_suit_high(a, sub))

ssh = np.asarray(ssh)
print(ssh.sum())
