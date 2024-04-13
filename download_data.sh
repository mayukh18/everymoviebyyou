#! /bin/sh

mkdir ml-25m
wget --show-progress "http://movierecobucket.s3.amazonaws.com/ml-25m/ratings.csv" -P ml-25m
wget --show-progress "http://movierecobucket.s3.amazonaws.com/ml-25m/movies_data_v2.csv" -P ml-25m