import networkx as nx


class graph(object):
    """
    Graph Class
    
    """
    def __init__(self, arg):
        super(graph, self).__init__()
        self.arg = arg
        
    def loadgraph():
        G = nx.read_gexf("../Data/mediumLinkedin.gexf")
        print("Nb of users in our graph: %d" % len(G))
        return G
    
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
             #To associate colors to nodes according to an attribute, here college
            # build a color_map, one for each college
            color_map={}
            i=0.0
            for s in list_of_values_of_attributes:
                color_map[s]=i
                i+=1/len(list_of_values_of_attributes)
            #color_map[None]=1  for nodes without values for the attribute node_attribute
            
             #The values supplied to node_color should be in the same order as the nodes 
             #listed in G.nodes(). We take an arbitrary mapping of values color_map and 
             #generate the values list in the correct order"""
            #values = [color_map[G.node[node].get(node_attribute)] for node in G.nodes()]  for attributes encoded in the graph
            values=[]        
            for node in G.nodes():
                if node in node_attribute:
                    if node_attribute[node]:
                       #  we arbitrarily take the first value 
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


    """
        neighbours: dict
        A dict to store neighbours of a given node
        
        neighboursofneighbour: dict
        A dict to store neighbours of a given node in  neighbours
    """
    
    def findneighbours(Graph,neighbours,neighboursofneighbour):
        """
        Find the neighbours of nodes in a graph
        
        Parameters
        ----------
        Graph :  graph
            A networkx graph
            
        Returns    
        ----------
        neighbours: dict
        A dict to store neighbours of a given node
        
        neighboursofneighbour: dict
        A dict to store neighbours of a given node in  neighbours
        
        """
        for n in Graph.nodes() :
           neighbours[n] = list(Graph.neighbors(n)), Graph.degree(n)
           for node in neighbours[n][0]:
                 neighboursofneighbour[node] = list(Graph.neighbors(node)), Graph.degree(node)
        
    #findneighbours(G)
    
    def printneighbourskeys(neighbours):
        """
        Print the keys of neighbour dictionary
        
        Parameters
        ----------
        neighbours: dict
            A dict to store neighbours of a given node
        Returns    
        ----------
            A list of keys of neighbours
        """
        for n in neighbours:
            print(n)
    
    def printneighbours(neighbours):
        
        """
        Print the values of neighbour dictionary
        
        Parameters
        ----------
        neighbours: dict
            A dict to store neighbours of a given node
        Returns    
        ----------
            A list of values of neighbours
        """
        
        for n in neighbours:
            
            print(neighbours[n][0])
            
    def printneighboursdegree(neighbours):
        """
        Print the number of neighbours
        
        Parameters
        ----------
        neighbours: dict
            A dict to store neighbours of a given node
        Returns    
        ----------
            A list of the number of neighbours per node
        """
        for n in neighbours:
            print(neighbours[n][1])
    
    nodepositions = dict()
            
    def createnodepositions(Graph):
        """
        Create numerical positions for each node in Graph
        
        Parameters
        ----------
         Graph :  graph
            A networkx graph
        Returns    
        ----------
            A list of nodes in graph and their respective numerical position
        """
        nodepositions = {}
        i = 0
        for n in Graph.nodes() :
            nodepositions[i] = n,i
            i = i + 1
        return nodepositions
    #createnodepositions(G)   
    
    """
      commonneighbours: dict
          A dict containing the common neighbours between two nodes. Key contains first node and second node
    """
   
    
    def findcommonneighbours(Graph,nodepositions):
        """`
         Find the common neighbours of two nodes in a graph
        
        Parameters
        ----------
         Graph :  graph
            A networkx graph
        Returns    
        ----------
        commonneighbours: dict
            A dict containing the common neighbours between two nodes. Key contains first node and second node. 
            The values consist of the list of common neighbours and the number of common neighbours
        """
        G = Graph
        commonneighbours = dict()
        i = 0
        j = i+1
        for i in range(len(nodepositions)):
            for j in range(len(nodepositions)):
                 node1 = nodepositions[i][0]
                 node2 = nodepositions[j][0]
                 if(len(sorted(nx.common_neighbors(G, node1, node2))) != 0):
                     commonneighbours[node1,node2] = sorted(nx.common_neighbors(G, node1, node2)),len(sorted(nx.common_neighbors(G, node1, node2)))
                 j = j + 1
            i = i + 1
        return  commonneighbours
    #findcommonneighbours(G)    
    
    def findfirstkeycommonneighbors(commonneighbours):
        """
         Find the first key in common neighbours 
        
        Parameters
        ----------
         commonneighbours: dict
            A dict containing the common neighbours between two nodes. Key contains first node and second node. 
            The values consist of the list of common neighbours and the number of common neighbours
            
        Returns    
        ----------
       
        """
    
        for key, values in commonneighbours:
            print(key[0])
    
    #findfirstkeycommonneighbors(commonneighbours)
    empty_location_n_college_info ={}
    location_n_college_info ={}
    
    empty_location_n_employer_info ={}
    location_n_employer_info ={}
    
    empty_employer_n_college_info ={}
    employer_n_college_info ={}
    
    empty_college_n_location_info ={}
    college_n_location_info ={}
    
    empty_employer_n_location_info ={}
    employer_n_location_info ={}
    
    empty_college_n_employer_info={}
    college_n_employer_info ={}
    
    neighbours = {}
    neighboursofneighbour = {}