# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 16:09:11 2017

@author: cbothore
"""


import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pylab
import numpy as np
import pickle
from collections import Counter
import resource
import sys
############################## Rudresh ###############################################
def list_of_different_attribute_values(d):
    return set([v for values in d.values() for v in values])
    
def draw_graph(g, node_attribute=None, list_of_values_of_attributes=None):
    """
    Draw the graph g.

    Parameters
    ----------
    g : graph
       A networkx graph
    node_attribute : string 
       The name of the node attribute used to assign colors to the drawing
    list_of_values_of_attributes : list
        A list of all the potential values of node_attribute to assign one color
        per value.
    """
    #initialze Figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    
    pos = nx.spring_layout(g,iterations=50)

    
    if node_attribute and list_of_values_of_attributes: 
        # To associate colors to nodes according to an attribute, here college
        # build a color_map, one for each college
        color_map={}
        i=0.0
        for s in list_of_values_of_attributes:
            color_map[s]=i
            i+=1/len(list_of_values_of_attributes)
        color_map[None]=1 # for nodes without values for the attribute node_attribute
        
        # The values supplied to node_color should be in the same order as the nodes 
        # listed in G.nodes(). We take an arbitrary mapping of values color_map and 
        # generate the values list in the correct order
        #values = [color_map[G.node[node].get(node_attribute)] for node in G.nodes()] # for attributes encoded in the graph
        values=[]        
        for node in G.nodes():
            if node in node_attribute:
                if node_attribute[node]:
                    # we arbitrarily take the first value 
                    values.append(color_map[node_attribute[node][0]])
            else:
                values.append(1)
               
        nx.draw_networkx_nodes(g,pos, cmap=plt.get_cmap('jet'), node_color=values)
    else:
        nx.draw_networkx_nodes(g,pos)
    
    nx.draw_networkx_edges(g,pos)
    nx.draw_networkx_labels(g,pos)

    cut = 1.00
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)
    plt.show()
    pylab.close()
    del fig
############################## Rudresh ###############################################

def naive_method(graph, empty, attr):
    """   Predict the missing attribute with a simple but effective
    relational classifier. 
    
    The assumption is that two connected nodes are 
    likely to share the same attribute value. Here we chose the most frequently
    used attribute by the neighbors
    
    Parameters
    ----------
    graph : graph
       A networkx graph
    empty : list
       The nodes with empty attributes 
    attr : dict 
       A dict of attributes, either location, employer or college attributes. 
       key is a node, value is a list of attribute values.

    Returns
    -------
    predicted_values : dict 
       A dict of attributes, either location, employer or college attributes. 
       key is a node (from empty), value is a list of attribute values. Here 
       only 1 value in the list.
     """
    predicted_values={}
    for n in empty:
        nbrs_attr_values=[] 
        for nbr in graph.neighbors(n):
            if nbr in attr:
                for val in attr[nbr]:
                    nbrs_attr_values.append(val)
        predicted_values[n]=[]
        if nbrs_attr_values: # non empty list
            # count the number of occurrence each value and returns a dict
            cpt=Counter(nbrs_attr_values)
            # take the most represented attribute value among neighbors
            a,nb_occurrence=max(cpt.items(), key=lambda t: t[1])
            predicted_values[n].append(a)
    return predicted_values
    
 
def evaluation_accuracy(groundtruth, pred):
    """    Compute the accuracy of your model.

     The accuracy is the proportion of true results.

    Parameters
    ----------
    groundtruth :  : dict 
       A dict of attributes, either location, employer or college attributes. 
       key is a node, value is a list of attribute values.
    pred : dict 
       A dict of attributes, either location, employer or college attributes. 
       key is a node, value is a list of attribute values. 

    Returns
    -------
    out : float
       Accuracy.
    """
    true_positive_prediction=0   
    for p_key, p_value in pred.items():
        if p_key in groundtruth:
            # if prediction is no attribute values, e.g. [] and so is the groundtruth
            # May happen
            if not p_value and not groundtruth[p_key]:
                true_positive_prediction+=1
            # counts the number of good prediction for node p_key
            # here len(p_value)=1 but we could have tried to predict more values
            true_positive_prediction += len([c for c in p_value if c in groundtruth[p_key]])          
        # no else, should not happen: train and test datasets are consistent
    return true_positive_prediction*100/sum(len(v) for v in pred.values())
   

# load the graph
G = nx.read_gexf("mediumLinkedin.gexf")
print("Nb of users in our graph: %d" % len(G))

# load the profiles. 3 files for each type of attribute
# Some nodes in G have no attributes
# Some nodes may have 1 attribute 'location'
# Some nodes may have 1 or more 'colleges' or 'employers', so we
# use dictionaries to store the attributes
college={}
location={}
employer={}
# The dictionaries are loaded as dictionaries from the disk (see pickle in Python doc)
with open('mediumCollege_60percent_of_empty_profile.pickle', 'rb') as handle:
    college = pickle.load(handle)
with open('mediumLocation_60percent_of_empty_profile.pickle', 'rb') as handle:
    location = pickle.load(handle)
with open('mediumEmployer_60percent_of_empty_profile.pickle', 'rb') as handle:
    employer = pickle.load(handle)

print("Nb of users with one or more attribute college: %d" % len(college))
print("Nb of users with one or more attribute location: %d" % len(location))
print("Nb of users with one or more attribute employer: %d" % len(employer))

# here are the empty nodes for whom your challenge is to find the profiles
empty_nodes=[]
with open('mediumRemovedNodes_60percent_of_empty_profile.pickle', 'rb') as handle:
    empty_nodes = pickle.load(handle)
print("Your mission, find attributes to %d users with empty profile" % len(empty_nodes))


# --------------------- Baseline method -------------------------------------#
# Try a naive method to predict attribute
# This will be a baseline method for you, i.e. you will compare your performance
# with this method
# Let's try with the attribute 'employer'
employer_predictions=naive_method(G, empty_nodes, employer)
groundtruth_employer={}
with open('mediumEmployer.pickle', 'rb') as handle:
    groundtruth_employer = pickle.load(handle)
    
groundtruth_location={}
with open('mediumLocation.pickle', 'rb') as handle:
    groundtruth_location = pickle.load(handle)
    
groundtruth_college={}
with open('mediumCollege.pickle', 'rb') as handle:
    groundtruth_college = pickle.load(handle)
result=evaluation_accuracy(groundtruth_employer,employer_predictions)
print("%f%% of the predictions are true" % result)
print("Very poor result!!! Try to do better!!!!")

# --------------------- Now your turn -------------------------------------#
# Explore, implement your strategy to fill empty profiles of empty_nodes


# and compare with the ground truth (what you should have predicted)
# user precision and recall measures
"""
    empty_college: dict
        A dict containing all the nodes that don't have college data
        
    empty_location : dict
        A dict containing all the nodes that don't have location data
        
    empty_employer : dict
        A dict containing all the nodes that don't have employer data
        
    no_empty_college: dict
        A dict containing all the nodes that have college data
        
    no_empty_location : dict
        A dict containing all the nodes that have location data
        
    no_empty_employer : dict
        A dict containing all the nodes that have employer data
"""
empty_college={}
empty_location={}
empty_employer={}

no_empty_college={}
no_empty_location={}
no_empty_employer={}

def emptydata(nodes, main_dictionary, empty_dictionary,no_empty_dictionary):
    """
    Find the nodes with missing data
    
    Parameters
    ----------
    nodes : dict
    main_dictionary: dict
    empty_dictionary : dict
    no_empty_dictionary : dict
    
    Returns
    ----------
    empty_dictionary : dict
        A dictory containing all the nodes with empty
    
    no_empty_dictionary : dict
        A dictory containing all the nodes non empty
    
    """
    for n in nodes:
        if n in main_dictionary:
            no_empty_dictionary[n] = main_dictionary[n]
            
        else:
             empty_dictionary[n] = None
             
    """
    full_data_info : dict
        A dict containing all the nodes that have full data , ie location, employer,college
    
    empty_full_data_info: dict
        A dict containing all the nodes that lack one or more of data , ie location, employer,college
    """            
full_data_info ={}
empty_full_data_info ={}
#
#def fulldata(dictionary_one,dictionary_two,dictionary_three):
#    """
#    Find the nodes that have full data , ie location, employer,college
#        
#    Parameters
#    ----------
#    dictionary_one: dict
#        A dict to compare with dictionary_two and dictionary_three
#        
#    dictionary_two: dict
#        A dict to compare with dictionary_one and dictionary_three
#         
#    dictionary_three : dict
#        A dict to compare with dictionary_one and dictionary_two
#        
#    Returns
#    ----------
#    full_data_info : dict
#        A dict containing all the nodes that have full data , ie location, employer,college
#    
#    empty_full_data_info: dict
#        A dict containing all the nodes that lack one or more of data , ie location, employer,college
#    """
#    for n in dictionary_one:
#        if n in dictionary_two and n in dictionary_three:
#          
#            full_data_info[n] = (n,dictionary_one[n],dictionary_two[n],dictionary_three[n])
#            
#        if dictionary_one[n] is None and dictionary_two[n] is None and dictionary_three[n] is None:
#                empty_full_data_info[n] = (n,None,None,None)
#                
#fulldata(employer,location,college)
#
#"""
#    empty_location_n_college_info: dict
#        A dict containing all the nodes that don't have location and college data
#        
#    empty_location_n_employer_info: dict
#        A dict containing all the nodes that don't have location and employer data
#        
#    empty_employer_n_college_info: dict
#        A dict containing all the nodes that don't have employer and college data
#        
#    empty_employer_n_location_info : dict
#        A dict containing all the nodes that don't have employer and location data
#        
#    empty_college_n_location_info: dict
#        A dict containing all the nodes that don't have college and location data
#        
#    empty_college_n_employer_info : dict
#        A dict containing all the nodes that don't have college and employer data
#              
#    location_n_college_info: dict
#        A dict containing all the nodes that have location and college data
#        
#    location_n_employer_info: dict
#        A dict containing all the nodes that have location and employer data
#        
#    employer_n_college_info: dict
#        A dict containing all the nodes that have employer and college data
#        
#    employer_n_location_info : dict
#        A dict containing all the nodes that have employer and location data
#        
#    college_n_location_info: dict
#        A dict containing all the nodes that have college and location data
#        
#    college_n_employer_info : dict
#        A dict containing all the nodes that have college and employer data
#        
#"""
#empty_location_n_college_info ={}
#location_n_college_info ={}
#
#empty_location_n_employer_info ={}
#location_n_employer_info ={}
#
#empty_employer_n_college_info ={}
#employer_n_college_info ={}
#
#empty_college_n_location_info ={}
#college_n_location_info ={}
#
#empty_employer_n_location_info ={}
#employer_n_location_info ={}
#
#empty_college_n_employer_info={}
#college_n_employer_info ={}
#
#def multipledata(dictionary_one,dictionary_two,no_empty_dictionary,empty_dictionary):
#    
#    """
#    Calculate the nodes that have a maximum of 2 values
#    
#    Parameters
#    ----------
#    dictionary_one:dict
#    dictionary_two:dict
#    no_empty_dictionary:dict
#    empty_dictionary : dict
#    Returns
#    ----------
#    no_empty_dictionary:dict
#    empty_dictionary : dict
#    
#    """
#  
#    for n in dictionary_one:
#        if n in dictionary_two:
#            no_empty_dictionary[n] = dictionary_one[n],dictionary_two[n]
#            #print(n,dictionary_one[n],dictionary_two[n])   
#        else:
#            #print(n,None,None)
#            empty_dictionary[n] = dictionary_one[n],None
#
#multipledata(location,college,location_n_college_info,empty_location_n_college_info)
#multipledata(location,employer,location_n_employer_info,empty_location_n_employer_info)
#multipledata(employer,college,employer_n_college_info,empty_employer_n_college_info)
#
#multipledata(college,location,college_n_location_info,empty_college_n_location_info)
#multipledata(employer,location,employer_n_location_info,empty_employer_n_location_info)
#multipledata(college,employer,college_n_employer_info,empty_college_n_employer_info)
#
#neighbours = {}
#neighboursofneighbour = {}
#
#"""
#    neighbours: dict
#    A dict to store neighbours of a given node
#    
#    neighboursofneighbour: dict
#    A dict to store neighbours of a given node in  neighbours
#"""
#
#def findneighbours(Graph):
#    """
#    Find the neighbours of nodes in a graph
#    
#    Parameters
#    ----------
#    Graph :  graph
#        A networkx graph
#        
#    Returns    
#    ----------
#    neighbours: dict
#    A dict to store neighbours of a given node
#    
#    neighboursofneighbour: dict
#    A dict to store neighbours of a given node in  neighbours
#    
#    """
#    for n in Graph.nodes() :
#       neighbours[n] = list(Graph.neighbors(n)), Graph.degree(n)
#       for node in neighbours[n][0]:
#             neighboursofneighbour[node] = list(Graph.neighbors(node)), Graph.degree(node)
#    
#findneighbours(G)
#
#def printneighbourskeys(neighbours):
#    """
#    Print the keys of neighbour dictionary
#    
#    Parameters
#    ----------
#    neighbours: dict
#        A dict to store neighbours of a given node
#    Returns    
#    ----------
#        A list of keys of neighbours
#    """
#    for n in neighbours:
#        print(n)
#
#def printneighbours(neighbours):
#    
#    """
#    Print the values of neighbour dictionary
#    
#    Parameters
#    ----------
#    neighbours: dict
#        A dict to store neighbours of a given node
#    Returns    
#    ----------
#        A list of values of neighbours
#    """
#    
#    for n in neighbours:
#        
#        print(neighbours[n][0])
#        
#def printneighboursdegree(neighbours):
#    """
#    Print the number of neighbours
#    
#    Parameters
#    ----------
#    neighbours: dict
#        A dict to store neighbours of a given node
#    Returns    
#    ----------
#        A list of the number of neighbours per node
#    """
#    for n in neighbours:
#        print(neighbours[n][1])
#
#nodepositions = dict()
#        
#def createnodepositions(Graph):
#    """
#    Create numerical positions for each node in Graph
#    
#    Parameters
#    ----------
#     Graph :  graph
#        A networkx graph
#    Returns    
#    ----------
#        A list of nodes in graph and their respective numerical position
#    """
#    
#    i = 0
#    for n in Graph.nodes() :
#        nodepositions[i] = n,i
#        i = i + 1
#        
#createnodepositions(G)   
#
#"""
#  commonneighbours: dict
#      A dict containing the common neighbours between two nodes. Key contains first node and second node
#"""
#commonneighbours = dict()
#
#def findcommonneighbours(Graph):
#    """`
#     Find the common neighbours of two nodes in a graph
#    
#    Parameters
#    ----------
#     Graph :  graph
#        A networkx graph
#    Returns    
#    ----------
#    commonneighbours: dict
#        A dict containing the common neighbours between two nodes. Key contains first node and second node. 
#        The values consist of the list of common neighbours and the number of common neighbours
#    """
#    G = Graph
#    i = 0
#    j = i+1
#    for i in range(len(nodepositions) - 1):
#        for j in range(len(nodepositions) - 1):
#             node1 = nodepositions[i][0]
#             node2 = nodepositions[j][0]
#             if(len(sorted(nx.common_neighbors(G, node1, node2))) != 0):
#                 commonneighbours[node1,node2] = sorted(nx.common_neighbors(G, node1, node2)),len(sorted(nx.common_neighbors(G, node1, node2)))
#             j = j + 1
#        i = i + 1
#         
#findcommonneighbours(G)    
#
#def findfirstkeycommonneighbors(commonneighbours):
#    """
#     Find the first key in common neighbours 
#    
#    Parameters
#    ----------
#     commonneighbours: dict
#        A dict containing the common neighbours between two nodes. Key contains first node and second node. 
#        The values consist of the list of common neighbours and the number of common neighbours
#        
#    Returns    
#    ----------
#   
#    """
#
#    for key, values in commonneighbours:
#        print(key[0])
#
#findfirstkeycommonneighbors(commonneighbours)
########################### RUdresh ###################################
#
#a = employer;
#draw_graph(G, node_attribute=a, list_of_values_of_attributes=list_of_different_attribute_values(a))
#
## print some properties to understand the type of graph
##properties(G)
## and compare with the ground truth (what you should have predicted)
## user precision and recall measures
#
#A = nx.k_nearest_neighbors(G,'in+out','in+out', nodes='U9128', weight=None)



#######################################################################

#import networkx as nx
#import timeit
#
#def getMean(values):
#    mean=0
#    numsum=0
#    for index in range(len(values)):
#        numsum=numsum+values[index]
#    mean=float(numsum)/float(len(values))
#    return mean
#
#def HeadTailCommunityDetection(G,finaledgelist):
#    H=nx.connected_component_subgraphs(G)
#    for subgraph in H:
#        result=nx.edge_betweenness(subgraph, False, None)
#        edges=list(result.keys())
#        values=list(result.values())
#        mean = getMean(values)
#        edgelist=[]
#        edgetemp=subgraph.edges();
#        if len(edgetemp)<=2:
#            for edge in edgetemp:
#                finaledgelist.append(edge)
#        else:
#            for index in range(len(values)):
#                    if values[index] <= mean:
#                        edgelist.append(edges[index])
#            if  (float(len(edgelist))/float(len(edges)))<=0.6: #change the head/tail division rule here, here is for tail percentage, so if the rule is 40/60, the value should be assigned 0.6 as in the code.
#                for edge in edgelist:
#                    finaledgelist.append(edge)
#            else:
#                Gsub= nx.Graph()
#                for edge in edgelist:
#                    Gsub.add_edge(edge[0],edge[1])
#                HeadTailCommunityDetection(Gsub,finaledgelist)
#
#def HeadTailInitiator():
#    G = nx.Graph()
#    ins = open("edge.txt", "r")  #input file path
#    for line in ins:
#            words = line.split(' ')
#            G.add_edge(int(words[0]), int(words[1]))
#    ins.close()
#    finaledgelist=[]
#    start = timeit.default_timer()
#    HeadTailCommunityDetection(G,finaledgelist)
#    print ("done!")
#    stop = (timeit.default_timer())
#    print ("Processing time(in second): ")
#    print (stop - start)
#    text_file = open("OutputEdge.txt", "w")    #output file path
#    for edge in finaledgelist:
#        text_file.write(str(edge[0])+" "+str(edge[1])+"\n")
#    text_file.close()

#HeadTailInitiator()

###############################################################################
#markovs cluster formation of the graphs
#reference https://github.com/GuyAllard/markov_clustering

import markov_clustering as mc
import networkx as nx
import random

# perform clustering using different inflation values from 1.5 and 2.5
# for each clustering run, calculate the modularity

for inflation in [i / 10 for i in range(15, 26)]:
    result = mc.run_mcl(matrix, inflation=inflation)
    clusters = mc.get_clusters(result)
    Q = mc.modularity(matrix=result, clusters=clusters)
    print("inflation:", inflation, "modularity:", Q)
    
# cluster using the optimized cluster inflation value
matrix = nx.to_scipy_sparse_matrix(G)
result = mc.run_mcl(matrix, inflation=1.5)
clusters = mc.get_clusters(result)  

# to obrain the list of the nodes in the list
x = list(G.nodes())

# to find the cordinates of the nodes
pos = nx.spring_layout(G,iterations=50)

dicts= {}

for i in range(len(pos)):
    dicts[i]=pos[x[i]]

# draw the clustered graph
mc.draw_graph(matrix, clusters, pos=dicts, node_size=50, with_labels=False, edge_color="silver")
 ################################################################################


# to obtain the details regarding the employer,location college of particular node in dictionary
del dict_details
dict_details = {}

for a in clusters[3]:
    if x[a] not in groundtruth_employer:
        y = None
    else:
        y = groundtruth_employer[x[a]]
    if x[a] not in groundtruth_location:
        z = None
    else:
       z = groundtruth_location[x[a]]
    if x[a] not in groundtruth_college:
        w = None
    else:
       w = groundtruth_college[x[a]]
    dict_details[a]= (y,z,w)
           
for a in G.neighbors('U27494'):
    for b in clusters[0]:
        if (x[b] == a):
            print(b)
            print('yes')  
            
###############################################################################
            
#use hamming distance on attributes to find the similarity between the attributes
#
 ###############################################################################       
# it has been notced that the certain area has been known with the different name as 
# synonym so the idea is to treat them same name  for eg greater chicago area comes near
#illinios  area or bloomington normal illinois area or urbana-champaign illinois area
# so idea is to treat them as common name as illinois area 
 ########################################################################       
from multiprocessing import Pool
import itertools

def partitions(nodes, n):
    "Partitions the nodes into n subsets"
    nodes_iter = iter(nodes)
    while True:
        partition = tuple(itertools.islice(nodes_iter,n))
        if not partition:
            return
        yield partition
        

def btwn_pool(G_tuple):
    return nx.betweenness_centrality_source(*G_tuple)

def between_parallel(G, processes = None):
    p = Pool(processes=processes)
    part_generator = 4*len(p._pool)
    node_partitions = list(partitions(G.nodes(), int(len(G)/part_generator)))
    num_partitions = len(node_partitions)
 
    bet_map = p.map(btwn_pool,
                        zip([G]*num_partitions,
                        [True]*num_partitions,
                        [None]*num_partitions,
                        node_partitions))
 
    bt_c = bet_map[0]
    for bt in bet_map[1:]:
        for n in bt:
            bt_c[n] += bt[n]
    return bt_c

G_fb = G
spring_pos = nx.spring_layout(G_fb)
bt = between_parallel(G_fb)
top = 10

max_nodes =  sorted(bt.items(), key = lambda v: -v[1])[:top]
bt_values = [5]*len(G_fb.nodes())
bt_colors = [0]*len(G_fb.nodes())
for max_key, max_val in max_nodes:
    bt_values[max_key] = 150
    bt_colors[max_key] = 2
 
plt.axis("off")
nx.draw_networkx(G_fb, pos = spring_pos, cmap = plt.get_cmap("rainbow"), node_color = bt_colors, node_size = bt_values, with_labels = False)