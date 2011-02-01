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
	
	#is this now pointless?
	seen_in_doc = set() #features in this doc
	
	path = instance[0]
	classification = instance[1]
	features = instance[2::2]	
	if classification in classes:
		class_counts[classification] += 1
	else:
		classes.add(classification)
		total_in_class[classification] = 0
		class_counts[classification] = 1
	
	for f in features:
		total_in_class[classification] += 1
		if f not in global_features:
			global_features.add(f)
			features_in_classes[f] = {}
			features_in_classes[f]['__classes__'] = set()
		if classification in features_in_classes[f]['__classes__']:
			features_in_classes[f][classification] += 1
		else:
			features_in_classes[f]['__classes__'].add(classification)
			features_in_classes[f][classification] = 1
		
		if f not in seen_in_doc:  #this entire set seems pointless now, is that correct?
			seen_in_doc.add(f)
			try:					#ugly way of doing this... worse than passing around lots of sets?
				doc_freq[f]+=1
			except KeyError:
				doc_freq[f] = 1


#build table 3 per feature
for feature in global_features:
	#fill in missing features
	for missing_class in classes-features_in_classes[feature]['__classes__']:
		features_in_classes[feature][missing_class] = 0
	table_3[feature] = [] #list of tuples (top_row,bottom_row), all classes
	for classification in classes:
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
	#looping through table 3 will loop through all classifications
	index = -1 #just to initialize
	for classification in classes:
		index+=1
		class_count,not_feature = table_3[feature][index]
		try:
			expected = total_in_class[classification] / 2
			observed = class_count-not_feature
			to_sum.append(((observed-expected)**2)/expected)
		except ZeroDivisionError:  #i'm sure there are better ways to do this
			sys.stderr.write("ZeroDivisionError, no need for concern")
	chi_squared[feature] = sum(to_sum)

for key in sorted(chi_squared.keys(), key=chi_squared.get, reverse=True):
	print key +" "+ str(chi_squared[key]) + " " + str(doc_freq[key])