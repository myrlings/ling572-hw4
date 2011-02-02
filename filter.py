#!/usr/lib/python2.6
import sys

if (len(sys.argv) < 4):
    print "Not enough args."
    sys.exit(1)

flist_file = open(sys.argv[1], 'r')
in_file = open(sys.argv[2], 'r')
out_file = open(sys.argv[3], 'w')

threshhold = 7.378

related_features = set()
for line in flist_file:
    parts = line.split()
    f = parts[0]
    score = int(parts[1])
    if (score > threshhold):
        related_features.add(f)

for line in in_file:
    line_array = line.split()
    instance_name = line_array[0]
    label = line_array[1]
    features = line_array[2::2] # every other word in line starting with third
    values = line_array[3::2] # every other word in line starting with fourth
    out_line = instance_name + " " + label
    for f, v in zip(features, values):
        if f in related_features:
            out_line += " " + f + " " + v
    out_file.write(out_line + "\n")
