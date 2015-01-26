# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 10:58:54 2015

@author: Wasit
"""
import numpy as np
x=np.array([ [0,1,2] , [3,4,5] , [6,7,8 ] ])
print x
print "x[1,1] = %d"%x[1,1]
print "x[:,0]= " + str( x[:,0] )
print "x[:,1]= " + str( x[:,1] )

print "x[:,1:3]= " + str( x[:,1:3] )
print "x[:,-2:-1]= " + str( x[:,-2:-1] )

