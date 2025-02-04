import sys
classes = set()
global_features = set()
class_counts = {}
features_in_classes = {} # class : {feature: count}
doc_freq = {} #feature: number of documents it appears in
table_3 = {} #feature : (top,bottom)
chi_squared = {}
instance_count = 0
total_in_class = {} # total number of features that appear in a certain class
N = 0

for instance in sys.stdin.readlines():
	instance_count +=1
	instance = instance.split()
	classification = instance[1]
	features = instance[2::2]	
	
	if classification in classes:
		class_counts[classification] += 1.0
	else:
		classes.add(classification)
		total_in_class[classification] = 0
		class_counts[classification] = 1.0
	
	for f in features:
		N += 1.0
		total_in_class[classification] += 1.0
		if f not in global_features:
			doc_freq[f] = 1.0
			global_features.add(f)
			features_in_classes[f] = {}
			features_in_classes[f]['__classes__'] = set()
		else:
			doc_freq[f] += 1.0
		if classification in features_in_classes[f]['__classes__']:
			features_in_classes[f][classification] += 1.0
		else:
			features_in_classes[f]['__classes__'].add(classification)
			features_in_classes[f][classification] = 1.0


#build table 3 per feature
for feature in global_features:
	# #fill in missing features
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
#     score <- score + [withoutF-expected]^2/expected


for feature in global_features:
	to_sum = []
	index = -1 #just to initialize
	
	#row total is the total number of documents of any class that had the feature
	row_total = doc_freq[feature]
	
	for classification in classes:
		index+=1
		class_count,not_feature = table_3[feature][index]
		try:
			column_total = total_in_class[classification]
			expected = row_total * column_total / N
			observed = features_in_classes[feature][classification]
			to_sum.append(((observed-expected)**2)/expected)
			# withF = features_in_classes[feature][classification]
			# withoutF = table_3[feature][index][1]
			# to_sum.append(((withF-expected)**2)/expected)
			# to_sum.append(((withoutF-expected)**2)/expected)
			
		except ZeroDivisionError:  #i'm sure there are better ways to do this
			sys.stderr.write("ZeroDivisionError, no need for concern")
	chi_squared[feature] = sum(to_sum)

for key in sorted(chi_squared.keys(), key=chi_squared.get, reverse=True):
	print key +" "+ str(chi_squared[key]) + " " + str(int(doc_freq[key]))