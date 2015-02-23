"""
Created on Mon Oct 13 18:50:34 2014

@author: Wasit
"""
#scmaster.py

import numpy as np
from scengine import engine
class master:
    def __init__(self):
        self.minbagsize=2
        self.maxdepth=30
        self.eng=engine()
        self.queue=None
        self.root=None
        self.node=None
    def __del__(self):
        pass
    def reset(self):
        H,Q = self.eng.reset()
        print("master>>H: {:.4f}".format(H))
        print("master>>Q: {:05d}".format(Q))
        del self.root
        del self.queue
        del self.node
        self.root=mnode(self.maxdepth,H,Q)
        self.queue=[self.root]
        self.node=[]
    def pop(self):
        self.eng.pop()
        self.node=self.queue.pop()
    def train(self):
        while 0<len(self.queue):
            self.pop()
            self.search()
            print self.node
            
    def search(self):        
        #check depth
        if self.node.depth<=1:
            self.terminate('D')                
            return
        #collect_thetas_taus
        thetas,taus=self.eng.getParam()
        #mearge_thetas_taus
        all_thetas=thetas
        all_taus=taus
        #compute ensemble entropy
        QH,Q=self.eng.getQH(all_thetas,all_taus)
        #check bag size Q
        if np.min(Q)<self.minbagsize:
            self.terminate('Q')                
            return
        #compute the entropy gain
        gain=self.node.H-QH/Q
        #find best gain index
        bgi = np.argmax(gain)
        #check gain
        if gain[bgi]<np.finfo(np.float32).tiny:
            self.terminate('G')                
            return
        #split
        HL,QL,HR,QR = self.eng.split(all_thetas[:,bgi],all_taus[bgi])

        self.node.L=mnode(self.node.depth-1,HL,QL,'L',self.node)
        self.node.R=mnode(self.node.depth-1,HR,QR,'R',self.node)
        self.queue.append(self.node.L)        
        self.queue.append(self.node.R)
        
        self.node.theta=all_thetas[:,bgi]
        self.node.tau=all_taus[bgi]
        self.node.char=self.node.char+'-'        
        
    def terminate(self, code):
        self.node.char=self.node.char+code
        P=self.eng.getHist()#+np.finfo(np.float32).tiny
        self.node.P=P/np.sum(P)

class mnode:
    def __init__(self,depth=0,H=0,Q=0,char='*',parent=None):
        self.theta=None  #vector array
        self.tau=None  #scalar
        self.H=H  #scalar
        self.P=None  #vector array
        self.parent=parent  #mnode
        self.depth=depth  #int
        self.L=None  #mnode
        self.R=None  #mnode
        self.char=char
        self.Q=Q
    def __del__(self):
        del self.theta
        del self.tau
        del self.H
        del self.P
        del self.parent
        del self.depth
        del self.L
        del self.R
        del self.char
    def table(self):
        text = self.__repr__()+'\n'
        if self.L is not None:
            text=text+self.L.table()
        if self.R is not None:
            text=text+self.R.table()
 
        return text
    
    def __repr__(self):
        #np.set_printoptions(formatter={'float': '{: 0.2f}'.format})
        if self.tau is None:
            ids = self.P.argsort()[::-1][:3]
            string='%s %02d H:%.3e,Q:%06d (cl,P):(%03d,%.2f) (%03d,%.2f) (%03d,%.2f)' % (
            self.char,self.depth,self.H,self.Q,ids[0],self.P[ids[0]],ids[1],self.P[ids[1]],ids[2],self.P[ids[2]])
        else:
            string='%s %02d H:%.3e,Q:%06d tau:%s' % (self.char,self.depth,self.H,self.Q,self.tau)
        return string

if __name__ == '__main__':
    m=master()
    m.reset()
    m.train()
    
    import pickle
    pickleFile = open('root.pickle', 'wb')
    pickle.dump(m.root, pickleFile, pickle.HIGHEST_PROTOCOL)
    pickleFile.close()



