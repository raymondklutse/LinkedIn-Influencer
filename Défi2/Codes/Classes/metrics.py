class metrics(object):
	"""docstring for Metrics"""
	def __init__(self, arg):
		super(metrics, self).__init__()
		self.arg = arg
	
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
	
	# --------------------- Now your turn -------------------------------------#
	# Explore, implement your strategy to fill empty profiles of empty_nodes

	# and compare with the ground truth (what you should have predicted)
	# user precision and recall measures