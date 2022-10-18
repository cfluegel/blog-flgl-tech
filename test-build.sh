#!/bin/bash
# 

cd pelican
make clean 
echo 

make publish 
echo $? 
