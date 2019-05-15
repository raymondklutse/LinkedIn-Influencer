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
   
    
    def fulldata(dictionary_one,dictionary_two,dictionary_three):
        """
        Find the nodes that have full data , ie location, employer,college
            
        Parameters
        ----------
        dictionary_one: dict
            A dict to compare with dictionary_two and dictionary_three
            
        dictionary_two: dict
            A dict to compare with dictionary_one and dictionary_three
             
        dictionary_three : dict
            A dict to compare with dictionary_one and dictionary_two
            
        Returns
        ----------
        full_data_info : dict
            A dict containing all the nodes that have full data , ie location, employer,college
        
        empty_full_data_info: dict
            A dict containing all the nodes that lack one or more of data , ie location, employer,college
        """
        for n in dictionary_one:
            if n in dictionary_two and n in dictionary_three:
              
                full_data_info[n] = (n,dictionary_one[n],dictionary_two[n],dictionary_three[n])
                
            if dictionary_one[n] is None and dictionary_two[n] is None and dictionary_three[n] is None:
                    empty_full_data_info[n] = (n,None,None,None)
                    
    #fulldata(employer,location,college)
    
    """
        empty_location_n_college_info: dict
            A dict containing all the nodes that don't have location and college data
            
        empty_location_n_employer_info: dict
            A dict containing all the nodes that don't have location and employer data
            
        empty_employer_n_college_info: dict
            A dict containing all the nodes that don't have employer and college data
            
        empty_employer_n_location_info : dict
            A dict containing all the nodes that don't have employer and location data
            
        empty_college_n_location_info: dict
            A dict containing all the nodes that don't have college and location data
            
        empty_college_n_employer_info : dict
            A dict containing all the nodes that don't have college and employer data
                  
        location_n_college_info: dict
            A dict containing all the nodes that have location and college data
            
        location_n_employer_info: dict
            A dict containing all the nodes that have location and employer data
            
        employer_n_college_info: dict
            A dict containing all the nodes that have employer and college data
            
        employer_n_location_info : dict
            A dict containing all the nodes that have employer and location data
            
        college_n_location_info: dict
            A dict containing all the nodes that have college and location data
            
        college_n_employer_info : dict
            A dict containing all the nodes that have college and employer data
            
    """
    
    def multipledata(dictionary_one,dictionary_two,no_empty_dictionary,empty_dictionary):
        
        """
        Calculate the nodes that have a maximum of 2 values
        
        Parameters
        ----------
        dictionary_one:dict
        dictionary_two:dict
        no_empty_dictionary:dict
        empty_dictionary : dict
        Returns
        ----------
        no_empty_dictionary:dict
        empty_dictionary : dict
        
        """
      
        for n in dictionary_one:
            if n in dictionary_two:
                no_empty_dictionary[n] = dictionary_one[n],dictionary_two[n]
                print(n,dictionary_one[n],dictionary_two[n])   
            else:
                print(n,None,None)
                empty_dictionary[n] = dictionary_one[n],None
    
    #multipledata(location,college,location_n_college_info,empty_location_n_college_info)
    #multipledata(location,employer,location_n_employer_info,empty_location_n_employer_info)
    #multipledata(employer,college,employer_n_college_info,empty_employer_n_college_info)
    
    #multipledata(college,location,college_n_location_info,empty_college_n_location_info)
    #multipledata(employer,location,employer_n_location_info,empty_employer_n_location_info)
    #multipledata(college,employer,college_n_employer_info,empty_college_n_employer_info)
    

    
    
