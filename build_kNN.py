#!/usr/lib/python2.6
import math
import sys
from operator import itemgetter

def get_vectors(data_filename):
    data_file = open(data_filename, 'r')

    instances = {}
    labels = {}
    all_features = set()
    for line in data_file:
        line_array = line.split()
        instance_name = line_array[0]
        label = line_array[1]
    
        instances[instance_name] = {}
        instances[instance_name]['class_label'] = label
        if label in labels:
            labels[label] += 1
        else:
            labels[label] = 1
            
        features = line_array[2::2] # every other word in line starting with third
        values = line_array[3::2] # every other word in line starting with fourth
            
        for f, v in zip(features, values):
            all_features.add(f)
            if not (f in instances[instance_name]):
                instances[instance_name][f] = v
            else:
                instances[instance_name][f] += v
        
    data_file.close()
    return [instances, labels, len(all_features)]

# get euclidean distance between two vectors
def get_euclidean(instance_vector, neighbor_vector):
    sum = 0
    instance_set = set(instance_vector.keys())
    neighbor_set = set(neighbor_vector.keys())
    all_features = instance_set.union(neighbor_set)
    for feature in all_features:
        to_square = 0
        if feature == 'class_label':
            continue
        if (feature in neighbor_vector) and (feature in instance_vector):
            to_square = (int(instance_vector[feature]) -\
            int(neighbor_vector[feature]))
        elif (feature in instance_vector):
            to_square = int(instance_vector[feature])
        else:
            to_square = int(neighbor_vector[feature])
        sum += to_square * to_square
    return math.sqrt(sum)

def get_cosine(instance_vector, neighbor_vector):
    # get dot product (sum of products)
    # and square of the norm (distance)
    dot_product = 0
    norm_sq1 = 0
    norm_sq2 = 0
    for feature in instance_vector:
        if feature == 'class_label':
            continue
        # only get dot product if there is no 0
        if (feature in neighbor_vector):
            dot_product += int(instance_vector[feature])*\
            int(neighbor_vector[feature])
        norm_sq1 += int(instance_vector[feature]) *\
        int(instance_vector[feature])
    for feature in neighbor_vector:
        if feature == 'class_label':
            continue
        norm_sq2 += int(neighbor_vector[feature]) * \
        int(neighbor_vector[feature])
    return dot_product / (math.sqrt(norm_sq1)*math.sqrt(norm_sq2))

# return a list, same length as vector_list, with distance inserted
# in proper spot (so worst distance gets bumped off)
def insert_distance(vector_list, distance, name, dist_or_sim):
    new_list = []
    if (dist_or_sim == "dist"):
        for slot in range(len(vector_list)):
            if distance < vector_list[slot][1]:
                if slot == 0:
                    new_list = [[name, distance]]
                    new_list.extend(vector_list[0:len(vector_list)])
                else:
                    new_list = vector_list[0:slot]
                    new_list.append([name, distance])
                    new_list.extend(vector_list[slot:len(vector_list)])
                break
    else:
        for slot in range(len(vector_list)):
            if distance > vector_list[slot][1]:
                if slot == 0:
                    new_list = [[name, distance]]
                    new_list.extend(vector_list[0:len(vector_list)])
                else:
                    new_list = vector_list[0:slot]
                    new_list.append([name, distance])
                    new_list.extend(vector_list[slot:len(vector_list)])
                break

    return new_list[0:len(vector_list)]

# same as above, but checking for highest value, since we are looking
# at similarity
def insert_similarity(vector_list, similarity, name):
    new_list = []
    for slot in range(len(vector_list)):
        if similarity > vector_list[slot][1]:
            if slot == 0:
                new_list = [[name, similarity]]
                new_list.extend(vector_list[0:len(vector_list)])
            else:
                new_list = vector_list[0:slot]
                new_list.append([name, similarity])
                new_list.extend(vector_list[slot:len(vector_list)])
            break

    return new_list[0:len(vector_list)]

# return probabilities of each label based on the nearest neighbors
# specify the best prob in 'winner'
def vote(neighbors_list, all_vectors, labels):
    ranks = {}
    for label in labels:
        ranks[label] = 0
    for neighbor in neighbors_list:
        if neighbor[0] == ['']:
            continue
        #print all_vectors[neighbor[0]]
        label = all_vectors[neighbor[0]]['class_label']
        ranks[label] += 1

    for label in ranks:
        if ranks[label] > 0:
            ranks[label] = float(ranks[label]) / len(neighbors_list)

    best_label = ""
    best_prob = 0
    for label in ranks:
        if ranks[label] >= best_prob:
            best_label = label
            best_prob = ranks[label]

    ranks['winner'] = best_label
    return ranks

def print_sys(vector_guesses, sys_file, real_vectors):
    for instance in vector_guesses:
        real_class = real_vectors[instance]['class_label']
        sys_file.write(instance + " ")
        #sys.write(vector_guesses[instance]['winner'] + " ")
        temp = vector_guesses[instance].pop('winner')
        sys_file.write(real_class + " ")
        sorted_votes = sorted(vector_guesses[instance].iteritems()\
        , key=itemgetter(1), reverse=True)
        for tup in sorted_votes:
            sys_file.write(tup[0] + " ")
            sys_file.write(str(tup[1]) + " ")
        sys_file.write("\n")
        vector_guesses[instance]['winner'] = temp

def print_acc(vectors, guesses, labels):
    counts = {}
    num_right = 0
    for actuallabel in labels:
        sys.stdout.write("\t" + actuallabel)
        counts[actuallabel] = {}
        for expectedlabel in labels:
            counts[actuallabel][expectedlabel] = 0
    for instance in vectors:
        actual_label = vectors[instance]['class_label']
        expected_label = guesses[instance]['winner']
        counts[actual_label][expected_label] += 1
        if actual_label == expected_label:
            num_right += 1

    sys.stdout.write("\n")
    for actuallabel in labels:
        sys.stdout.write(actuallabel)
        for expectedlabel in labels:
            sys.stdout.write("\t" + str(counts[actuallabel][expectedlabel]))
        sys.stdout.write("\n")
    accuracy = float(num_right) / len(vectors)
    return accuracy

# main
if (len(sys.argv) < 6):
    print "Not enough args."
    sys.exit(1)

train_data_filename = sys.argv[1]
test_data_filename = sys.argv[2]
k = int(sys.argv[3])
similarity_func = int(sys.argv[4])
sys_filename = sys.argv[5]

vectors_labels = get_vectors(train_data_filename)
train_vectors = vectors_labels[0]
labels = vectors_labels[1]

vector_scores = {}
vector_guesses = {}
for instance_vector in train_vectors:
    if similarity_func == 1:
        vector_scores[instance_vector] = [[[""],[float("inf")]]]*k
    else:
        vector_scores[instance_vector] = [[[""],0.0]]*k
    #print vector_scores
    #for i in range(0,k-1):
    #    vector_scores[instance_vector][i][1] = float("inf")

    for neighbor_vector in train_vectors:
        # don't need distance between itself
        if train_vectors[neighbor_vector] == train_vectors[instance_vector]:
            continue
        # get euclidean distance
        if similarity_func == 1:
            distance = get_euclidean(train_vectors[instance_vector], \
            train_vectors[neighbor_vector])
            # if the distance is better than the last one of the sorted list
            if distance < vector_scores[instance_vector][k-1][1]:
                vector_scores[instance_vector] = \
                insert_distance(vector_scores[instance_vector], distance,\
                neighbor_vector, "dist")
        # get cosine similarity
        else:
            similarity = get_cosine(train_vectors[instance_vector],
            train_vectors[neighbor_vector])
            if similarity > vector_scores[instance_vector][k-1][1]:
                vector_scores[instance_vector] = \
                insert_distance(vector_scores[instance_vector], similarity,\
                neighbor_vector, "sim")

    # find the class based on the neighbors
    vector_guesses[instance_vector] = vote(vector_scores[instance_vector],\
    train_vectors, labels)

sys_file = open(sys_filename, 'w')
sys_file.write("%%%%% training data:\n")
print_sys(vector_guesses, sys_file, train_vectors)

test_vectors_labels = get_vectors(test_data_filename)
test_vectors = test_vectors_labels[0]

# process test vectors
test_scores = {}
test_guesses = {}
for instance_vector in test_vectors:
    if similarity_func == 1:
        test_scores[instance_vector] = [[[""],[float("inf")]]]*k
    else:
        test_scores[instance_vector] = [[[""],0.0]]*k
    #for i in range(0,k-1):
    #    test_scores[instance_vector][i][1] = float("inf")

    for neighbor_vector in train_vectors:
        # don't need distance between itself
        if train_vectors[neighbor_vector] == test_vectors[instance_vector]:
            continue
        # get euclidean distance
        if similarity_func == 1:
            distance = get_euclidean(test_vectors[instance_vector], \
            train_vectors[neighbor_vector])
            # if the distance is better than the last one of the sorted list

            print test_scores[instance_vector]
            if distance < test_scores[instance_vector][k-1][1]:
                print "here we are"
                print test_scores[instance_vector]
                test_scores[instance_vector] = \
                insert_distance(test_scores[instance_vector], distance,\
                neighbor_vector, "dist")
        # get cosine similarity
        else:
            similarity = get_cosine(test_vectors[instance_vector],\
            train_vectors[neighbor_vector])
            if similarity > test_scores[instance_vector][k-1][1]:
                test_scores[instance_vector] = \
                insert_distance(test_scores[instance_vector], similarity,\
                neighbor_vector, "sim")
        #print test_scores[instance_vector]

    # find the class based on the neighbors
    test_guesses[instance_vector] = vote(test_scores[instance_vector],\
    train_vectors, labels)

sys_file.write("\n%%%%% testing data:\n")
print_sys(test_guesses, sys_file, test_vectors)

# print confusion matrix
print "class_num=", len(labels), ", feat_num=", vectors_labels[2]

print "\nConfusion matrix for the training data:"
print "row is the truth, column is the system output\n"
#print vector_guesses
training_acc = print_acc(train_vectors, vector_guesses, labels)
print "Training accuracy:", training_acc

print "\nConfusion matrix for the testing data:"
print "row is the truth, column is the system output\n"
#print vector_guesses
testing_acc = print_acc(test_vectors, test_guesses, labels)
print "Testing accuracy:", testing_acc
