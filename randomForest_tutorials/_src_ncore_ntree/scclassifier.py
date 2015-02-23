"""
Created on Fri Oct 17 23:10:18 2014

@author: Wasit
"""
import pickle
import numpy as np
from sctree import tree
class classifier:
    def __init__(self,ntrees=1,path='out'):
        self.trees=[]
        self.ntrees=ntrees
        for i in xrange(self.ntrees):
            filename=path+"/tree%02d.pickle"%(i)
            pickleFile = open(filename, 'rb')
            root = pickle.load(pickleFile)
            pickleFile.close()

            #init the test tree
            t=tree()
            t.settree(root)
            self.trees.append(t)
    def getP(self,Ix=np.arange(2)):
        P=[]
        for i in xrange(self.ntrees):
            P.append(self.trees[i].getP(Ix))
        P=np.sum(P,axis=0)
        P=P/np.sum(P)
        return P
    
    def getL(self,Ix=np.arange(2)):
        '''
        input:
            Ix is [2d ndarray]
        output:
            L [integer] label
        '''
        return np.argmax(self.getP(Ix))
            
if __name__ == '__main__':
    from matplotlib import pyplot as plt      
    from scdataset import dataset
    from scmaster import master
    import numpy as np
    import os
    #training
    m=master()
    ntrees=3
    path='out'
    if not os.path.exists(path):
        os.makedirs(path)
    for i in xrange(ntrees):
        m.reset()
        m.train()
        #recording the tree pickle file
        filename=path+"/tree%02d.pickle"%(i)
        pickleFile = open(filename, 'wb')
        pickle.dump(m.root, pickleFile, pickle.HIGHEST_PROTOCOL)
        pickleFile.close()
        
    #init the test tree
    cf=classifier(ntrees,path)
    #compute recall rate
    dset=dataset()
    correct=0;
    for i in xrange(dset.size):
        if dset.getL(i) == cf.getL(dset.I[:,i]):
            correct=correct+1
    print("recall rate: {}%".format(correct/float(dset.size)*100))
        
    #setup the new test-set
    d=0.01
    y, x = np.mgrid[slice(-1, 1+d, d), slice(-1, 1+d, d)]
    
    #start labeling
    L=np.zeros(x.shape,dtype=int)
    for r in xrange(x.shape[0]):
        for c in xrange(x.shape[1]):
            L[r,c]=cf.getL(np.array([ x[r,c],y[r,c] ]))
    
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
    for i in xrange(dset.size):
        plt.plot(dset.I[0,i],dset.I[1,i],marker[dset.samples[0,i]])