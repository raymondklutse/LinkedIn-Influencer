import timeit
from collections import Counter

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