import sys
classes = set()
global_features = set()
class_counts = {}
features_in_classes = {} # class : {feature: count}
doc_freq = {} #feature: number of documents it appears in
contingency_table = {} #feature : (top,bottom)
chi_squared = {}

for instance in sys.stdin.readlines():
	instance = instance.split()
	seen_in_doc = set() #features in this doc
	
	# instance_count += 1
	path = instance[0]
	classification = instance[1]
	features = instance[2::2]
	# values = instance[3::2]
	
	if classification in classes:
		class_counts[classification] +=1
	else:
		classes.add(classification)
		class_counts[classification] = 1
		features_in_classes[classification] = {}
		features_in_classes[classification]['__features__'] = set()
	
	for f in features:
		if f not in seen_in_doc:
			seen_in_doc.add(f)
			try:					#ugly way of doing this... worse than passing around lots of sets?
				doc_freq[f]+=1
			except KeyError:
				doc_freq[f] = 1
		if f not in global_features:
			global_features.add(f)
		if f in features_in_classes[classification]['__features__']:
			features_in_classes[classification][f] += 1
		else:
			features_in_classes[classification]['__features__'].add(f)
			features_in_classes[classification][f] = 1

#build contingency table per feature

for feature in global_features:
	contingency_table[feature] = [] #list of tuples (top_row,bottom_row), all classes
	for classification in classes:
		#fill in missing features
		for missing_feature in global_features-features_in_classes[classification]['__features__']:
			features_in_classes[classification][missing_feature] = 0
			
		contingency_table[feature].append((class_counts[classification],\
		class_counts[classification]-features_in_classes[classification][feature]))
		
#compute chi square
for feature in global_features:
	to_sum = []
	for top,bottom in contingency_table[feature]: #observed-expected/expected
		try:
			to_sum.append((top**2)/bottom)
		except ZeroDivisionError:  #i'm sure there are better ways to do this
			sys.stderr.write("ZeroDivisionError, no need for concern")
		
	chi_squared[feature] = sum(to_sum)

for key in sorted(chi_squared.keys(), key=chi_squared.get, reverse=True):
	print key +" "+ str(chi_squared[key]) + " " + str(doc_freq[key])