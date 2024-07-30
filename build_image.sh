#!/bin/bash

echo "requirements.txt file path: $1"
cp $1 ./tmp_build_requirements.txt

docker build --build-arg REQUIREMENTS_FILE=$1 -t naoinviabilize-dev .

rm ./tmp_build_requirements.txt
