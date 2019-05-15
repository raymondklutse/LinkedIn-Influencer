# -*- coding: utf-8 -*-
"""
Created on Tuesday 14 04 20:00:00 2019

@author: Rudresh Mishra
         Klutse Raymond
"""

import graph as g
import data as d
import algorithms as algo

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

commonneighbours = {}
nodepositions = g.graph.createnodepositions(G)

commonneighbours = g.graph.findcommonneighbours(G,nodepositions)

#markov_clustering
predicted_values_markov_location = algo.algorithms.markov_clustering(G,location,empty_nodes,groundtruth_location)

#louvain_clustering
predicted_values_louvain_location = algo.algorithms.louvain_clustering(G,location,empty_nodes,groundtruth_location)


bw_centrality = dict()
bw_centrality = algo.algorithms.centralitybetweeness(G)
bw_sorted = sorted(bw_centrality.items(), key=lambda x: x[1])


bayareadict_mark = dict()
print('Markov Clustering')
for node in bw_centrality:
   if node in predicted_values_markov_location:
        if predicted_values_markov_location[node] == ['urbana-champaign illinois area'] and bw_centrality[node] != 0:
           bayareadict_mark[node]= predicted_values_markov_location[node],bw_centrality[node]
        

bayareadict_bw_centrality_mark_sorted = sorted(bayareadict_mark.items(), key=lambda x: x[1],reverse = True)
print(len(bayareadict_bw_centrality_mark_sorted))

bayareadict_louv = dict()
print('Louvain Clustering')
for node in bw_centrality:
    if node in predicted_values_louvain_location:
        if predicted_values_louvain_location[node] == ['urbana-champaign illinois area'] and bw_centrality[node] != 0:
           bayareadict_louv[node]= predicted_values_louvain_location[node],bw_centrality[node]
        

bayareadict_bw_centrality_louv_sorted = sorted(bayareadict_louv.items(), key=lambda x: x[1],reverse = True)
print(len(bayareadict_bw_centrality_louv_sorted))

 #'U8828': 3036.2293413968355,
