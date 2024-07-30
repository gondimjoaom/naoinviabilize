#!/bin/bash

echo "notebooks folder path: $1"
echo "datasets folder path: $2"

exec docker run --gpus all -p 4321:4321 -v "$1":/workspace/notebooks -v "$2":/workspace/datasets -t naoinviabilize-dev
