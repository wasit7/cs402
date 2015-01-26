# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 11:22:15 2015

@author: Wasit
"""
import os
#file
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('py') or f.endswith('txt'):
            print f
        #for f in files:
                #if f.endswith('jpg') or f.endswith('JPG'):