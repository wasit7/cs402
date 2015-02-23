"""
Created on Tue Oct 14 18:52:01 2014

@author: Wasit
"""
import numpy as np
class dataset:
    def __init__(self):
        self.clmax=5
        self.spc=10000
        self.dim_theta=2
        self.size=self.clmax*self.spc
        #list of np.array
        self.I=np.zeros((2,self.size))
        #samples first row is the label
        #samples 2nd row is sample index
        self.samples=np.zeros((2,self.size),dtype=np.uint32)
        for cl in xrange(self.clmax):
                xo=cl*self.spc
                #define label
                self.samples[0,xo:xo+self.spc]=cl    
                #define sample index.
                self.samples[1,xo:xo+self.spc]=np.arange(xo,xo+self.spc)   
                
                phi = np.linspace(0, 2*np.pi, self.spc) + \
                np.random.randn(self.spc)*0.4*np.pi/self.clmax + \
                2*np.pi*cl/self.clmax
                r = np.linspace(0.1, 1, self.spc)
                
                self.I[:,xo:xo+self.spc]=np.array([r*np.cos(phi), r*np.sin(phi)])
                
                
    def __del__(self):
        del self.clmax
        del self.spc
        del self.size
        del self.I
        del self.samples
    def getX(self):
        '''
        input: 
            void
        output: 
            [1D ndarray dtype=np.uint32]
        '''
#        return np.arange(0, self.size, dtype=np.uint32)
#        return np.random.randint(0,self.size,size=self.size)
        return np.random.permutation(self.size)
    def getL(self,x):
        '''
        input: 
            [1D ndarray dtype=np.uint32]
        output: 
            [1D ndarray dtype=np.uint32]
        '''
        return self.samples[0,x]
    def getI(self,thetas,x):
        '''
        input:
            x: [1D ndarray dtype=np.uint32]\n
            thetas: [2D ndarray float]
        output: 
            [1D ndarray dtype=np.uint32]
        Description:
            In spiral case, it uses only first row of the thetas
        '''
        if thetas.ndim==2:
            #dataset.getParam() calls this
            return self.I[thetas[0,:],x] 
        else:
            #engine.getQH() call this
            return self.I[thetas[0],x]
    def getParam(self,x):
        '''
        input:
            x: [1D ndarray dtype=np.uint32]
        output:
            thetas: [2D ndarray float] rmax=dim_theta, cmax=len(x)
            taus: [1D ndarray dtype=np.uint32]
        Description:
            In spiral case, it uses only first row of the thetas
        '''
        rmax=self.dim_theta
        cmax=len(x)
        thetas = np.random.randint(2, size=(rmax,cmax))
        taus = self.getI(thetas, x)
        return thetas,taus
    
    
if __name__ == '__main__':
    from matplotlib import pyplot as plt    
    dset=dataset()
    plt.hold(True)
    marker=['bo','co','go','ro','mo','yo','ko',
            'bs','cs','gs','rs','ms','ys','ks']
    for i in xrange(dset.size):
        plt.plot(dset.I[0,i],dset.I[1,i],marker[dset.samples[0,i]])
    
    thetas,taus=dset.getParam(dset.getX())
    print("thetas:\n{}".format(thetas))
    print("taus:\n{}".format(taus))

