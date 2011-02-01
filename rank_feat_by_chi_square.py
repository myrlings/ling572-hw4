import sys
classes = set()
global_features = set()
class_counts = {}
features_in_classes = {} # class : {feature: count}
doc_freq = {} #feature: number of documents it appears in
table_3 = {} #feature : (top,bottom)
chi_squared = {}
instance_count = 0
total_in_class = {}

for instance in sys.stdin.readlines():
	instance_count +=1
	instance = instance.split()
	seen_in_doc = set() #features in this doc
	path = instance[0]
	classification = instance[1]
	features = instance[2::2]	
	if classification in classes:
		class_counts[classification] +=1
	else:
		classes.add(classification)
		total_in_class[classification] = 0
		class_counts[classification] = 1
		# features_in_classes[classification] = {}
		# features_in_classes[classification]['__features__'] = set()
	
	for f in features:
		if f not in global_features:
			global_features.add(f)
			features_in_classes[f] = {}
			features_in_classes[f]['__classes__'] = set()
		if classification in features_in_classes[f]['__classes__']:
			features_in_classes[f][classification] += 1
		else:
			features_in_classes[classification]['__features__'].add(f)
			features_in_classes[classification][f] = 1
		
		if f not in seen_in_doc:  #this entire set seems pointless now, is that correct?
			seen_in_doc.add(f)
			total_in_class[classification] += 1
			try:					#ugly way of doing this... worse than passing around lots of sets?
				doc_freq[f]+=1
			except KeyError:
				doc_freq[f] = 1

#build table 3 per feature
for feature in global_features:
	table_3[feature] = [] #list of tuples (top_row,bottom_row), all classes
	for classification in classes:
		#fill in missing features
		for missing_class in classes-features_in_classes[feature]['__classes__']:
			features_in_classes[f][classification] = 0
		table_3[feature].append((class_counts[classification],\
		class_counts[classification]-features_in_classes[feature][classification]))
# 
#compute chi square
#Chad's algo:
# -For each feature:
#   score <- 0
#   for each class that feature had a count for:
#     expected <- cnt(class)/2.0
#     withF <- cnt(class, feature)
#     withoutF <- cnt(class) - cnt(class, feature)
#     score <- score + [withF-expected]^2/expected
#     score <- score + [withoutF-expected]^2/expected //edit: line added - I accidentally left it out of my original post


for feature in global_features:
	to_sum = []
	for class_count,not_feature in table_3[feature]: #observed-expected/expected
		try:
			expected = total_in_class[feature] / 2
			observed = class_count-not_feature
			to_sum.append(((observed-expected)**2)/expected)
		except ZeroDivisionError:  #i'm sure there are better ways to do this
			sys.stderr.write("ZeroDivisionError, no need for concern")
	chi_squared[feature] = sum(to_sum)


# #fill in missing features
# for feature in global_features:
# 	for classification in classes:
# 		for missing_class in classes-features_in_classes[f]['__classes__']:
# 			features_in_classes[f][classification] = 0
# 			
# 
# # 			compute chi square
# for feature in global_features:
# 	for classification in classes:
		

# #build E table from O table  (features_in_classes)
# E_table = {}
# for feature in global_features:
# 	E_table[feature] = {} #just initializing it
# 	row_total = 0
# 	for classification in classes: # get row total
# 		E_table[feature][classificaAtion] = 0
# 		row_total += features_in_classes[classification][feature]	
# 	for classification in classes: # get row total	
# 		e_value = row_total / len(classes)
# 		E_table[feature][classification] = e_value
# 		# if e_value != 0:
# 		# 	print feature,classification,e_value
# 	
# 		
# 
# # compute chi square
# for feature in global_features:
# 	to_sum = []
# 	for classification in classes:
# 		E = E_table[feature][classification]
# 		O = features_in_classes[classification][feature]
# 		try:
# 			to_sum.append((((O-E)**2)/E))		
# 		except ZeroDivisionError:  #i'm sure there are better ways to do this
# 			sys.stderr.write("ZeroDivisionError, no need for concern")
# 	chi_squared[feature] = sum(to_sum)

for key in sorted(chi_squared.keys(), key=chi_squared.get, reverse=True):
	print key +" "+ str(chi_squared[key]) + " " + str(doc_freq[key])