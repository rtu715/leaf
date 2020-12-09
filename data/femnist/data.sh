#!/usr/bin/env bash
split_seed="1549786796"
sampling_seed="1549786595"

rm -rf meta data/test data/train data/rem_user_data data/intermediate data/sampled_data

./preprocess.sh -s niid --sf 1 -k 100 -t sample --smplseed ${sampling_seed} --spltseed ${split_seed}
