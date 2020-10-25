# encoding: utf-8
import os
import socket
import sys
import random
from threading import Thread, Lock, enumerate
import time
import select

cards = [[], []]
cardchoices = [0, 0]
cardnum = 7
ind = -1

def CardAvailable(cards, card):
    for i in cards:
        if (card == i):
            return True
    return False

def GetNumber(cards, str, apd = None):
    if (str == 'keyboard'):
        readstr = input('input card:')
        while not (readstr.isdigit() and CardAvailable(cards, int(readstr))):
            readstr = input('Error!input card:')
        return int(readstr)
    if (str == 'random'):
        return random.choice(cards)
    if (str == 'min'):
        return min(cards)
    if (str == 'max'):
        return max(cards)

def GetPlayNumber(str, apd = None):
    num = GetNumber(cards[apd], str, apd)
    cardchoices[apd] = num
    cards[apd].remove(num)



if __name__=="__main__":

    
    for i in range(1, cardnum+1):
        cards[0].append(i);
        cards[1].append(i);
    
    clientsocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

    host = sys.argv[1]

    port = 2257

    clientsocket.connect((host, port))
    print ('Connected')
    hello = clientsocket.recv(1024).decode('utf-8')
    print ('The server says %s to you!' % (hello))
    print ('Waiting for the game to start!\n')
    
    ind = int(clientsocket.recv(1024).decode('utf-8'))
    print ('Game Starts!')
    print ('You are Player %d\n' % (ind + 1))
    
    print ('Player 1\'s cards: ', cards[0], ' Player 2\'s cards: ', cards[1])
    while len(cards[0]) > 0 and len(cards[1]) > 0:
        GetPlayNumber('keyboard', ind)
        clientsocket.send(str(cardchoices[ind]).encode('utf-8'))
        cardchoices[1-ind] = int(clientsocket.recv(1024).decode('utf-8'))
        if (cardchoices[1-ind] < 0):
            print ('\nDisconnect from the other player.You are now playing with an AI.\n')
            cardchoices[1-ind] = -cardchoices[1-ind]
        cards[1-ind].remove(cardchoices[1-ind])
        print ('Player 1 selects %d;Player 2 selects %d' % (cardchoices[0], cardchoices[1]))
        if (cardchoices[0] > cardchoices[1]):
            cards[0].append(cardchoices[1])
        elif (cardchoices[0] < cardchoices[1]):
            cards[1].append(cardchoices[0])
        cards[0].sort()
        cards[1].sort()
        print ('Player 1\'s cards: ', cards[0], ' Player 2\'s cards: ', cards[1], '\n')
    
    if len(cards[0]) == 0 and len(cards[1]) == 0:
        print('Draw!\n')
    elif len(cards[0]) == 0 ^ ind == 0:
        print('You lose!')
    else:
        print('You win!')
    
    clientsocket.close()
    input('Press \"enter\" to end the game.')
