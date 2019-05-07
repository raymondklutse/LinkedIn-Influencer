# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 16:09:11 2017

@author: Rudresh
         Klutse Raymond
"""

import graph as g
import data as d

#Load Graph Data
G = g.graph.loadgraph()

#create dictionaries to store college, location and employer data
college = {}
location= {}
employer= {}
empty_nodes = []

#load college, location and employer data into dictionaries 
college,location,employer,empty_nodes = d.data.loaddata(college,location,employer,empty_nodes)

#create dictionaries to store college, location and employer data
groundtruth_college={}
groundtruth_location={}
groundtruth_employer={}

#load college, location and employer data into dictionaries 
groundtruth_college, groundtruth_location, groundtruth_employer = d.data.groundtruth(G,empty_nodes,employer)



   









