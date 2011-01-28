import math


if (len(sys.argv) < 6):
    print "Not enough args."
    sys.exit(1)

train_data_filename = sys.argv[1]
test_data_filename = sys.argv[2]
k = int(sys.argv[3])
similarity_func = int(sys.argv[4])
sys_filename = sys.argv[5]
