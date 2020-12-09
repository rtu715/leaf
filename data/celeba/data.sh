#!/usr/bin/env bash

if [ -d "data/rem_user_data" ]; then
	echo "removing processed data"
	rm -rf meta/ data/rem_user_data data/sampled_data data/test data/train
fi 

./preprocess.sh -s niid --sf 0.1 -k 5 -t sample 

