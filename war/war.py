
import numpy as np
import pyprind
from stats import plot_war_stats

class Card:
    ''' simple class for playing cards. 
        suit and value are both strings; 
        rank is the numerical value of the card '''
    FaceRanks={'A':14,'K':13,'Q':12,'J':11}
    def __init__(self,suit,value):
        self.suit=suit
        self.value=value
        self.rank=None
        self._setRank()
    def _setRank(self):
        v=self.value
        if v in self.FaceRanks:
            self.rank=self.FaceRanks[v]
        elif v[0].isdigit():
            self.rank=int(v)
    def __str__(self):
        return f'{self.value}{self.suit}'
    def __gt__(self,other):
        return self.rank>other.rank
    def __eq__(self,other):
        return self.rank==other.rank
import random
class Deck:
    ''' simple class for a deck of Cards. '''
    def __init__(self,shuffle=False):
        self.D=[]
        for s in ['S','D','H','C']:
            for v in [str(x) for x in range(2,11)]+['J','Q','K','A']:
                self.D.append(Card(s,v))
        if shuffle:
            self.shuffle()
    def __str__(self):
        return ', '.join([str(x) for x in self.D])
    def __len__(self):
        return len(self.D)
    def pop(self):
        return self.D.pop()
    def shuffle(self):
        random.shuffle(self.D)
    def Reclaim(self,H):
        while len(H)>0:
            self.D.append(H.pop())

class War:
    ''' class for playing a game of War.  War begins with cards randomly
        assigned to both players; each has 26. Play proceeds by each player
        presenting a card for a "duel".  The winner of the duel is the card
        of higher rank, and the winner takes both duel cards and puts them 
        at the bottom of their hand. If the two duelling cards have the same
        rank, then war is declared.  Each duelling card becomes the first card
        it is respective player's Wall, and then each player adds at most
        three more cards to their Wall.  A final duel then decides the winner
        of the War, who takes all cards from both Walls.  Important edge cases:
        
        1. If a tie duel occurs when either player has played the only card in their
           hand, that player loses and the winner receives both cards.
        2. If either player has fewer than 4 cards in their hand when a tie duel
           occurs, then the number of Wall cards is temporarily adjusted down to 
           allow the minority player the chance at one final duel using their last card.
         '''
    def __init__(self):
        self.Wall=[]
        self.Duelers=[]
        self.HandWinners=[]
        self.Deck=Deck(shuffle=True)
        self.Hands=[[],[]]
    def _deal(self):
        assert len(self.Deck)==52, 'You are leaking cards before dealing!'
        assert len(self.Hands[0])==0, 'Gimme those cards back, Player 1!'
        assert len(self.Hands[1])==0, 'Gimme those cards back, Player 2!'
        self.Deck.shuffle()
        while len(self.Deck)>0:
            self.Hands[0].append(self.Deck.pop())
            self.Hands[1].append(self.Deck.pop())
    def _checkState(self):
        N=len(self.Hands[0])+len(self.Hands[1])+len(self.Wall)+len(self.Duelers)
        assert N==52, 'You are leaking cards after a game!'
    def _declareWinner(self):
        if len(self.Hands[0])==52:
            self.Winner=0
            self.Deck.Reclaim(self.Hands[0])
            assert len(self.Hands[0])==0, 'Gimme those cards!'
        elif len(self.Hands[1])==52:
            self.Winner=1
            self.Deck.Reclaim(self.Hands[1])
            assert len(self.Hands[0])==0, 'Gimme those cards!'
        else:
            self.Winner=None
    def _declareHandWinner(self,i):
        self.Hands[i].extend(self.Duelers)
        self.Hands[i].extend(self.Wall)
        self.Wall=[]
        self.Duelers=[]
        self.HandWinners.append(i)
    def _buildWall(self):
        nSoldiers=min([3,len(self.Hands[0])-1,len(self.Hands[1])-1])
        ''' To the ramparts!! '''
        self.Wall.extend(self.Duelers)
        self.Duelers=[]
        for i in range(nSoldiers):
            self.Wall.append(self.Hands[0].pop())
            self.Wall.append(self.Hands[1].pop())
    def Play(self):
        self.nTiebreaks=0
        self.nHands=0
        self._deal()
        while len(self.Hands[0])>0 and len(self.Hands[1])>0:
            ''' The duel begins! '''
            self.Duelers=[self.Hands[0].pop(),self.Hands[1].pop()]
            p1=self.Duelers[0]
            p2=self.Duelers[1]
            if p1>p2:
                ''' Player 1 wins! '''
                self._declareHandWinner(0)
            elif p2>p1:
                ''' Player 2 wins! '''
                self._declareHandWinner(1)
            else:
                ''' It's a tie! '''
                self.nTiebreaks+=1
                if len(self.Hands[0])==0:
                    ''' Player 1 is out of cards; Player 2 wins '''
                    self._declareHandWinner(1)
                elif len(self.Hands[1])==0:
                    ''' Player 2 is out of cards; Player 1 wins '''
                    self._declareHandWinner(0)
                else:
                    ''' The tie-break war is on!  
                        Build the wall, let the winner
                        of the next duel take it all! '''
                    self._buildWall()
            self.nHands+=1
        self._checkState()
        self._declareWinner()
        return self.nHands,self.nTiebreaks
if __name__=='__main__':
    N=100000
    HandsPerGame=[]
    TiebreaksPerGame=[]
    w=War()
    bar=pyprind.ProgBar(N)
    for i in range(N):
        h,t=w.Play()
        bar.update()
        HandsPerGame.append(h)
        TiebreaksPerGame.append(t)
    plot_war_stats(HandsPerGame,TiebreaksPerGame)
    