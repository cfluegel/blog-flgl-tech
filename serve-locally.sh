#!/bin/bash
# 

cd pelican
make clean 
echo 

make devserver
echo $? 


