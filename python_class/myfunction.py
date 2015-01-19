# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 11:47:11 2015

@author: Wasit
"""

def print_height(mylist):
    x=max(mylist)
    y=min(mylist)
    print "maximum height %.2f \nminimum height: %.2f" % (x,y)
    return (x,y)    
if __name__ == "__main__":
    mylist=[158,171,158,167,180]
    x,y = print_height(mylist)
    