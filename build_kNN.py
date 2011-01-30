#!/usr/lib/python2.6
import math
import sys
from operator import itemgetter

def get_vectors(data_filename):
    data_file = open(train_data_filename, 'r')

    instances = {}
    labels = {}
    for line in data_file:
        line_array = line.split()
        instance_name = line_array[0]
        label = line_array[1]
    
        instances[instance_name] = {}
        instances[instance_name]['class_label'] = label
        labels[label] += 1
            
        features = line_array[2::2] # every other word in line starting with third
        values = line_array[3::2] # every other word in line starting with fourth
            
        for f, v in zip(features, values):
            if not (f in instances[instance_name]):
                instances[instance_name][f] = v
            else:
                instances[instance_name][f] += v
        
    data_file.close()
    return [instances, labels]

def get_euclidean(instance_vector, neighbor_vector):
    sum = 0
    for feature in instance_vector:
        if feature == 'class_label':
            continue
        if feature in neighbor_vector:
            sum += (int(instance_vector[feature]) -\
            int(neighbor_vector[feature]))**2
        else:
            sum += (int(instance_vector[feature]))**2
    return math.sqrt(sum)

def get_cosine(train_vectors, instance_vector, neighbor_vector):
    return 0

# return a list, same length as vector_list, with distance inserted
# in proper spot (so worst distance gets bumped off)
def insert_distance(vector_list, distance, name):
    new_list = []
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

def vote(neighbors_list, all_vectors, labels):
    ranks = {}
    for neighbor in neighbors_list:
        label = all_vectors[neighbor[0]]['class_label']
        if label in ranks:
            ranks[label] += 1
        else:
            ranks[label] = 1

    for label in ranks:
        ranks[label] = ranks[label] / len(neighbors_list)

    best_label = ""
    best_prob = 0
    for label in ranks:
        if ranks[label] > best_prob:
            best_label = label
            best_prob = ranks[label]

    ranks['winner'] = best_label
    return ranks

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
    vector_scores[instance_vector] = [[[""],[float("inf")]]]*k
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
                neighbor_vector)
        # get cosine similarity
        else:
            similarity = get_cosine(instance_vector, neighbor_vector)
            vector_scores[instance_vector][neighbor_vector] = distance

    # find the class based on the neighbors
    vector_guess[instance_vector] = vote(vector_scores[instance_vector],\
    train_vectors, labels)

## write print_sys method
print_sys(vector_guess)
