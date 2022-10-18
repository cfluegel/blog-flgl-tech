#!/bin/bash
# 

# Only allow this script to run after all changes have been checked in 

if [ -n "$(git status -s pelican)" ]; then 
  echo "Unchecked modifications have been found!"
  echo 
  exit 1 
fi 

# Generate the website 
(
cd pelican/
make clean publish 
)

# Prepare some tests 

# Generate the docker image 
#VERSION=$(git log -1 --pretty=%h)
#VERSION=$(date +%Y.%m.%d-%H%M)
VERSION=$(date +%s)
REPO="cfluegel/blog-flgl-tech"
TAG="$REPO:$VERSION"
LATEST="${REPO}:latest"

# docker build -t "$TAG" -t "$LATEST" --build-arg VERSION="$VERSION" .
docker build  -t "$LATEST" --build-arg VERSION="$VERSION" .

docker push -a $REPO
