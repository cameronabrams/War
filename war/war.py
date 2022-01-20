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
            random.shuffle(self.D)
    def __str__(self):
        return ', '.join([str(x) for x in self.D])
    def __len__(self):
        return len(self.D)
    def pop(self):
        return self.D.pop()

class Game:
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
        self.D=Deck(shuffle=True)
        self.Deal()
        self.Play()
        self._checkState()
    def Deal(self):
        self.Hands=[[],[]]
        while len(self.D)>0:
            self.Hands[0].append(self.D.pop())
            self.Hands[1].append(self.D.pop())
    def _checkState(self):
        N=len(self.Hands[0])+len(self.Hands[1])+len(self.Wall)+len(self.Duelers)
        if N!=52:
            print('Error: Card leakage!')
            exit()
    def _declareWinner(self,i):
        self.Hands[i].extend(self.Duelers)
        self.Hands[i].extend(self.Wall)
        self.Wall=[]
        self.Duelers=[]
    def _buildWall(self):
        nSoldiers=min([3,len(self.Hands[0])-1,len(self.Hands[1])-1])
        # man the wall!
        self.Wall.extend(self.Duelers)
        self.Duelers=[]
        for i in range(nSoldiers):
            self.Wall.append(self.Hands[0].pop())
            self.Wall.append(self.Hands[1].pop())
    def Play(self):
        self.nWars=0
        self.nDuels=0
        while len(self.Hands[0])>0 and len(self.Hands[1])>0:
            ''' The duel begins! '''
            self.Duelers=[self.Hands[0].pop(),self.Hands[1].pop()]
            p1=self.Duelers[0]
            p2=self.Duelers[1]
            if p1>p2:
                ''' Player 1 wins! '''
                self._declareWinner(0)
            elif p2>p1:
                ''' Player 2 wins! '''
                self._declareWinner(1)
            else:
                ''' It's a tie! '''
                self.nWars+=1
                if len(self.Hands[0])==0:
                    ''' Player 1 is out of cards; Player 2 wins '''
                    self._declareWinner(1)
                elif len(self.Hands[1])==0:
                    ''' Player 2 is out of cards; Player 1 wins '''
                    self._declareWinner(0)
                else:
                    ''' War is on!  Build the wall, and go to next duel! '''
                    self._buildWall()
            self.nDuels+=1

if __name__=='__main__':
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    import numpy as np
    mycmap=cm.get_cmap('plasma')
    prism=cm.get_cmap('prism')
    Duels=[]
    Wars=[]
    for i in range(100000):
        g=Game()
        if i%100==0:
            print('.',end='',flush=True)
        if i>0 and i%8000==0:
            print(flush=True)
        Duels.append(g.nDuels)
        Wars.append(g.nWars)
    Duels=np.array(Duels,dtype=int)
    X=np.linspace(min(Duels),max(Duels)*10,10000)
    Wars=np.array(Wars,dtype=int)
    maxWars=max(Wars)
    fig,ax=plt.subplots(1,2,figsize=(10,6))
    plt.subplots_adjust(hspace=0.3)
    ax[0].hist(Duels,bins=100,range=(0,2000),density=True,histtype='step',label='Duels per game',color=mycmap(0.3))
    ax[0].hist(Wars,bins=100,range=(0,2000),density=True,histtype='step',label='Wars per game',color=mycmap(0.8))
    ax[0].legend()
    ax[0].set_xlabel('Duels, Wars')
    ax[0].set_ylabel('Frequency')
    ax[0].set_yscale('log')
    ax[0].set_xlim((0,ax[0].get_xlim()[1]))
    ax[1].scatter(Duels,Wars/Duels,s=1,c=[prism(x) for x in Wars/maxWars])
    ax[1].set_ylim(0,0.5)
    for x in list(range(0,20))+list(range(21,max(Wars),10)):
        ax[1].plot(X,x/X,alpha=0.2,color=prism(x/max(Wars)))
    ax[1].set_xlabel('Duels')
    ax[1].set_ylabel('Wars per Duel')
    ax[1].set_xscale('log')
    plt.savefig('warishell.png')
    plt.show()