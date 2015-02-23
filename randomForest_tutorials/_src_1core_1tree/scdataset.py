"""
Created on Tue Oct 14 18:52:01 2014

@author: Wasit
"""
import numpy as np
class dataset:
    def __init__(self,clmax=5,spc=1000):
        self.clmax=clmax
        self.spc=spc
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
    def setL(self,x,L):
        self.samples[0,x]=L
    def getIs(self,thetas,x):
        #dataset.getParam() calls this
        return self.I[thetas[0,:],x] 
    def getI(self,theta,x):
        '''
        input:
            x: [1D ndarray dtype=np.uint32]\n
            thetas: [2D ndarray float]
        output: 
            [1D ndarray dtype=np.uint32]
        Description:
            In spiral case, it uses only first row of the thetas
        '''
        #engine.getQH() call this
        return self.I[theta[0],x]
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
        taus = self.getIs(thetas, x)
        return thetas,taus
    def show(self):
        import matplotlib.pyplot as plt
        #setup the new test-set
        d=0.01
        y, x = np.mgrid[slice(-1, 1+d, d), slice(-1, 1+d, d)]
        
#        #hack the dataset dont do this at home!        
#        dset2=dataset()      
#        #start labeling    
#        L=np.zeros(x.shape,dtype=int)
#        for r in xrange(x.shape[0]):
#            for c in xrange(x.shape[1]):
#                dset2.I[:,0]=np.array([ x[r,c],y[r,c] ])
#                L[r,c]=t.getL(0,dset2)
#        #plot the lalbel out put
#        plt.close('all')
#        plt.axis([-1,1,-1,1])
#        plt.pcolor(x,y,L)
#        plt.show()
#        plt.hold(True)
        
        #overlaying new input data        
        plt.set_cmap('jet')
        marker=['bo','co','go','ro','mo','yo','ko',
                'bs','cs','gs','rs','ms','ys','ks']
        marker_num=np.min((self.size,500))
        for i in self.getX()[:marker_num]:
            plt.plot(self.I[0,i],self.I[1,i],marker[self.samples[0,i]%14])
    
if __name__ == '__main__':
    from matplotlib import pyplot as plt    
    dset=dataset()
    plt.hold(True)
    marker=['rx','gx','bx','cx','mx','yx','kx']
    for i in xrange(dset.size):
        plt.plot(dset.I[0,i],dset.I[1,i],marker[dset.samples[0,i]])
    
    thetas,taus=dset.getParam(dset.getX())
    print("thetas:\n{}".format(thetas))
    print("taus:\n{}".format(taus))

