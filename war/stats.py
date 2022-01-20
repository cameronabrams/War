import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
def plot_war_stats(hpg=[],tpg=[],**kwargs):
    mycmap=cm.get_cmap('plasma')
    prism=cm.get_cmap('prism')
    HPG=np.array(hpg,dtype=int)
    TPG=np.array(tpg,dtype=int)
    X=np.linspace(min(HPG),max(HPG)*10,10000)
    maxTPG=max(TPG)
    fig,ax=plt.subplots(1,2,figsize=(10,6))
    plt.subplots_adjust(hspace=0.3)
    ax[0].hist(HPG,bins=100,range=(0,2000),density=True,histtype='step',label='Hands per game',color=mycmap(0.3))
    ax[0].hist(TPG,bins=100,range=(0,2000),density=True,histtype='step',label='Tibreaks per game',color=mycmap(0.8))
    ax[0].legend()
    ax[0].set_xlabel('Hands, Tiebreaks')
    ax[0].set_ylabel('Frequency')
    ax[0].set_yscale('log')
    ax[0].set_xlim((0,ax[0].get_xlim()[1]))
    ax[1].scatter(HPG,TPG/HPG,s=1,c=[prism(x) for x in TPG/maxTPG])
    ax[1].set_ylim(0,0.5)
    for x in list(range(0,20))+list(range(21,maxTPG,10)):
        ax[1].plot(X,x/X,alpha=0.2,color=prism(x/maxTPG))
    ax[1].set_xlabel('Hands')
    ax[1].set_ylabel('Tiebreaks per Hand')
    ax[1].set_xscale('log')
    if 'fn' in kwargs:
        plt.savefig(kwargs['fn'])
    else:
        plt.savefig('warishell.png')
    plt.show()