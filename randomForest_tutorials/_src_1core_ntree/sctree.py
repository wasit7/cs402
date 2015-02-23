"""
Created on Thu Oct 16 17:33:47 2014

@author: Wasit
"""
from scmaster import mnode
import numpy as np

class tree(mnode):    
    def settree(self,root=mnode(0,0,0)):
        self.theta=root.theta  #vector array
        self.tau=root.tau  #scalar
        self.H=root.H  #scalar
        self.P=root.P  #vector array
        self.parent=root.parent  #mnode
        self.depth=root.depth  #int
        self.char=root.char
        self.Q=root.Q
        if root.L is not None:
            self.L=tree()  #mnode
            self.L.settree(root.L)
            self.R=tree()  #mnode
            self.R.settree(root.R)
    def getP(self,Ix=np.arange(2)):
        '''
        input:
            Ix is [1d ndarray]
        output:
            P [1d ndarray] probability P(L|Ix)
        '''
#        print("tree>>mnode:{}".format(self))
#        print("tree>>type(Ix[0]):{}".format(type(Ix[0])))
#        print("tree>>type(tau):{}".format(type(self.tau)))
        if self.tau is None:
            return self.P
        elif (self.L is not None and Ix[self.theta[0]]<self.tau) :
            return self.L.getP(Ix)
        else:
            return self.R.getP(Ix)
    
    def getL(self,Ix=np.arange(2)):
        '''
        input:
            Ix is [2d ndarray]
        output:
            L [integer] label
        '''
        return np.argmax(self.getP(Ix))

if __name__ == '__main__':
    import pickle
    from matplotlib import pyplot as plt      
    from scdataset import dataset
    from scmaster import master
    #training
    m=master()
    m.reset()
    m.train()    
    print m.root.table()
    #recording the tree pickle file
    pickleFile = open('root.pickle', 'wb')
    pickle.dump(m.root, pickleFile, pickle.HIGHEST_PROTOCOL)
    pickleFile.close()
    
    #reading the tree pickle file    
    pickleFile = open('root.pickle', 'rb')
    root = pickle.load(pickleFile)
    pickleFile.close()
    
    #init the test tree
    t=tree()
    t.settree(root)
    
    #compute recall rate
    dset=dataset()
    correct=0;
    for i in xrange(dset.size):
        if dset.getL(i) == t.getL(dset.I[:,i]):
            correct=correct+1
    print("recall rate: {}%".format(correct/float(dset.size)*100))
        
    #setup the new test-set
    d=0.01
    y, x = np.mgrid[slice(-1, 1+d, d), slice(-1, 1+d, d)]
    
    #start labeling
    L=np.zeros(x.shape,dtype=int)
    for r in xrange(x.shape[0]):
        for c in xrange(x.shape[1]):
            L[r,c]=t.getL(np.array([ x[r,c],y[r,c] ]))
    
    #plot the lalbel out put
    plt.close('all')
    plt.axis([-1,1,-1,1])
    plt.pcolor(x,y,L)
    plt.show()
    
    #overlaying new input data
    plt.hold(True)
    
    plt.hold(True)
    marker=['bo','co','go','ro','mo','yo','ko',
            'bs','cs','gs','rs','ms','ys','ks']
    for i in dset.getX()[0:min(dset.size,1000)]:
        plt.plot(dset.I[0,i],dset.I[1,i],marker[dset.samples[0,i]])