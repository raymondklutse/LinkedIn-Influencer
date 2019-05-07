import markov_clustering as mc
import networkx as nx
import random

class Clustering(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg
	
	def performclustering:

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

	
########################### RUdresh ###################################

a = employer;
draw_graph(G, node_attribute=a, list_of_values_of_attributes=list_of_different_attribute_values(a))

print some properties to understand the type of graph
properties(G)
and compare with the ground truth (what you should have predicted)
user precision and recall measures

A = nx.k_nearest_neighbors(G,'in+out','in+out', nodes='U9128', weight=None)



#######################################################################



            
#use hamming distance on attributes to find the similarity between the attributes
#
 ###############################################################################       
# it has been notced that the certain area has been known with the different name as 
# synonym so the idea is to treat them same name  for eg greater chicago area comes near
#illinios  area or bloomington normal illinois area or urbana-champaign illinois area
# so idea is to treat them as common name as illinois area 
 ########################################################################       
