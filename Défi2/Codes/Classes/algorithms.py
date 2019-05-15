import timeit
from collections import Counter
import markov_clustering as mc
import community
import networkx as nx
import matplotlib.pyplot as plt
import random
import metrics as met

class algorithms(object):
    """docstring for Algorithms"""
    def __init__(self, arg):
        super(algorithms, self).__init__()
        self.arg = arg
    import networkx as nx


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
    def dijstrashortestpath(Graph):
        shortestpaths = dict()
        G = Graph
    
        i = 0
        j = i+1
        for i in range(len(nodepositions)):
            for j in range(len(nodepositions)):
                 node1 = nodepositions[i][0]
                 node2 = nodepositions[j][0]
                 if(len(sorted(nx.common_neighbors(G, node1, node2))) != 0):
                     shortestpaths[node1,node2] = sorted(nx.common_neighbors(G, node1, node2)),len(sorted(nx.common_neighbors(G, node1, node2)))
                 j = j + 1
            i = i + 1
        return  commonneighbours
    
    def centralitybetweeness(Graph):
        G = Graph
        bw_centrality = dict()
        bw_centrality = nx.betweenness_centrality(G, normalized=False)
        
        return bw_centrality
    
    def markov_clustering(G,location,empty_nodes,groundtruth_location):
        
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
        ### to predict the location
        x = list(G.nodes())
        predicted_values={}
        for i in clusters:
            dict_details = {}
            for a in i:
                if x[a] not in location:
                    w = None
                else:
                    w = location[x[a]]
                dict_details[a]= (w)
           
            for a in dict_details:
                if dict_details[a] is None and x[a] in empty_nodes:
                    nbrs_attr_values=[] 
                    for b in G.neighbors(x[a]):
                        node = x.index(b)
                        if node in i and dict_details[node] is not None and b in location:
                            for val in location[b]:
                                nbrs_attr_values.append(val)                    
                                predicted_values[x[a]]=[]
                                if nbrs_attr_values: # non empty list
                                    # count the number of occurrence each value and returns a dict
                                    cpt=Counter(nbrs_attr_values)
                                    # take the most represented attribute value among neighbors
                                    b,nb_occurrence=max(cpt.items(), key=lambda t: t[1])
                                    predicted_values[x[a]].append(b)
        
        #print("Print predicted value",predicted_values)
        result = met.metrics.evaluation_accuracy(groundtruth_location,predicted_values)
        print("%f%% of the predictions are true" % result)
        return predicted_values
        #return predicted_values
    def louvain_clustering(G,location,empty_nodes,groundtruth_location):
        partition = community.best_partition(G)

        size = float(len(set(partition.values())))
        pos = nx.spring_layout(G)
        count = 0.
        clusters=[]
        for com in set(partition.values()) :
            count = count + 1.
            list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
            clusters.append(list_nodes)
            nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,node_color = str(count / size))
        nx.draw_networkx_edges(G, pos, alpha=0.5)
        plt.show()
        predicted_values={}
        for i in clusters:
            dict_details = {}
            for a in i:
                if a not in location:
                    w = None
                else:
                    w = location[a]
                dict_details[a]= (w)
            for a in dict_details:
                if dict_details[a] is None and a in empty_nodes:
                    nbrs_attr_values=[] 
                    for b in G.neighbors(a):
                        if b in i and dict_details[b] is not None and b in location:
                            for val in location[b]:
                                nbrs_attr_values.append(val)                    
                                predicted_values[a]=[]
                                if nbrs_attr_values: # non empty list
                                    # count the number of occurrence each value and returns a dict
                                    cpt=Counter(nbrs_attr_values)
                                    # take the most represented attribute value among neighbors
                                    b,nb_occurrence=max(cpt.items(), key=lambda t: t[1])
                                    predicted_values[a].append(b)
        return predicted_values
                 
    def getMean(values):
        mean=0
        numsum=0
        for index in range(len(values)):
            numsum=numsum+values[index]
        mean=float(numsum)/float(len(values))
        return mean
    
    def HeadTailCommunityDetection(G,finaledgelist):
       """ H=nx.connected_component_subgraphs(G)
        for subgraph in H:
            result=nx.edge_betweenness(subgraph, False, None)
            edges=list(result.keys())
            values=list(result.values())
            mean = getMean(values)
            edgelist=[]
            edgetemp=subgraph.edges();
            if len(edgetemp)<=2:
                for edge in edgetemp:
                    finaledgelist.append(edge)
            else:
                for index in range(len(values)):
                        if values[index] <= mean:
                            edgelist.append(edges[index])
                if  (float(len(edgelist))/float(len(edges)))<=0.6: change the head/tail division rule here, here is for tail percentage, so if the rule is 40/60, the value should be assigned 0.6 as in the code.
                    for edge in edgelist:
                        finaledgelist.append(edge)
                else:
                    Gsub= nx.Graph()
                    for edge in edgelist:
                        Gsub.add_edge(edge[0],edge[1])
                    HeadTailCommunityDetection(Gsub,finaledgelist)
                    """
    
    def HeadTailInitiator():
       """ G = nx.Graph()
        ins = open("edge.txt", "r")  input file path
        for line in ins:
                words = line.split(' ')
                G.add_edge(int(words[0]), int(words[1]))
        ins.close()
        finaledgelist=[]
        start = timeit.default_timer()
        HeadTailCommunityDetection(G,finaledgelist)
        print ("done!")
        stop = (timeit.default_timer())
        print ("Processing time(in second): ")
        print (stop - start)
        text_file = open("OutputEdge.txt", "w")    output file path
        for edge in finaledgelist:
            text_file.write(str(edge[0])+" "+str(edge[1])+"\n")
        text_file.close()  """
    
    HeadTailInitiator()
    
    
    ##markovs cluster formation of the graphs
    ##reference https://github.com/GuyAllard/markov_clustering"""