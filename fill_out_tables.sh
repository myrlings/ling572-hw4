#!/bin/bash

# The format is: build_kNN.sh training_data test_data k_val similarity_func sys_output > acc_file


#q2
python build_KNN.py examples/train.vectors.txt examples/test.vectors.txt 1 1 q2/sys1_1 > q2/acc1_1
python build_KNN.py examples/train.vectors.txt examples/test.vectors.txt 1 5 q2/sys1_5 > q2/acc1_5
python build_KNN.py examples/train.vectors.txt examples/test.vectors.txt 1 10 q2/sys1_10 > q2/acc1_10
python build_KNN.py examples/train.vectors.txt examples/test.vectors.txt 2 1 q2/sys2_1 > q2/acc2_1
python build_KNN.py examples/train.vectors.txt examples/test.vectors.txt 2 5 q2/sys2_5 > q2/acc2_5
python build_KNN.py examples/train.vectors.txt examples/test.vectors.txt 2 10 q2/sys2_10 > q2/acc2_10


#q3
python build_KNN.py examples/train2.vectors.txt examples/test2.vectors.txt 1 1 q3/sys1_1_bin > q3/acc1_1_bin
python build_KNN.py examples/train2.vectors.txt examples/test2.vectors.txt 1 5 q3/sys1_5_bin > q3/acc1_5_bin
python build_KNN.py examples/train2.vectors.txt examples/test2.vectors.txt 1 10 q3/sys1_10_bin > q3/acc1_10_bin
python build_KNN.py examples/train2.vectors.txt examples/test2.vectors.txt 2 1 q3/sys2_1_bin > q3/acc2_1_bin
python build_KNN.py examples/train2.vectors.txt examples/test2.vectors.txt 2 5 q3/sys2_1_bin > q3/acc2_5_bin
python build_KNN.py examples/train2.vectors.txt examples/test2.vectors.txt 2 1 q3/sys2_1_bin > q3/acc2_10_bin

#q5
cat examples/train2.vectors.txt | python rank_feat_by_chi_square.py > train.ranked
###STOPPED WRITING HERE
python filter.py train.ranked
cat examples/test2.vectors.txt | python rank_feat_by_chi_square.py > test.filtered.vectors.txt
python build_KNN.py examples/train.vectors.txt examples/test.vectors.txt 1 2 sys1_2_filtered > acc1_2_filtered

#q6
cat examples/train.vectors.txt | python rank_feat_by_chi_square.py > train.filtered.vectors.txt
cat examples/test.vectors.txt | python rank_feat_by_chi_square.py > test.filtered.vectors.txt
python build_KNN.py examples/train.vectors.txt examples/test.vectors.txt 1 2 sys1_2_filtered > acc1_2_filtered