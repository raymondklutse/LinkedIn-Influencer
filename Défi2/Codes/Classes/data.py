import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pylab
import numpy as np
import pickle
from collections import Counter
import resource
import sys
import algorithms as a
import metrics as m

class data(object):
    # load the profiles. 3 files for each type of attribute
    # Some nodes in G have no attributes
    # Some nodes may have 1 attribute 'location'
    # Some nodes may have 1 or more 'colleges' or 'employers', so we
    # use dictionaries to store the attributes
    def __init__(self, arg):
        super(data, self).__init__()
        self.arg = arg   
        
            
    def loaddata(college,location,employer,empty_nodes):
        """
        Load  dictionary
    
        Parameters
        ----------
        college : dictionary
            A dictionary to store location data
        """
        with open('../Data/mediumLocation_60percent_of_empty_profile.pickle', 'rb') as handle:
            location = pickle.load(handle)
            print("Nb of users with one or more attribute employer: %d" % len(location))
            
        with open('../Data/mediumEmployer_60percent_of_empty_profile.pickle', 'rb') as handle:
            employer = pickle.load(handle)
            print("Nb of users with one or more attribute location: %d" % len(employer))
            
        with open('../Data/mediumCollege_60percent_of_empty_profile.pickle', 'rb') as handle:
            college = pickle.load(handle)
            print("Nb of users with one or more attribute college: %d" % len(college))
            
        with open('../Data/mediumRemovedNodes_60percent_of_empty_profile.pickle', 'rb') as handle:
            empty_nodes = pickle.load(handle)
            print("Your mission, find attributes to %d users with empty profile" % len(empty_nodes))
        
        return college,location,employer,empty_nodes
   
    def groundtruth(G,empty_nodes,employer):
        employer_predictions=a.algorithms.naive_method(G, empty_nodes, employer)
        groundtruth_employer={}
        with open('../Data/mediumEmployer.pickle', 'rb') as handle:
            groundtruth_employer = pickle.load(handle)
            
        groundtruth_location={}
        with open('../Data/mediumLocation.pickle', 'rb') as handle:
            groundtruth_location = pickle.load(handle)
            
        groundtruth_college={}
        with open('../Data/mediumCollege.pickle', 'rb') as handle:
            groundtruth_college = pickle.load(handle)
            
        result=m.metrics.evaluation_accuracy(groundtruth_employer,employer_predictions)
        print("%f%% of the predictions are true" % result)
        print("Very poor result!!! Try to do better!!!!")
        
        return groundtruth_college, groundtruth_location, groundtruth_employer
        
       

    
    
