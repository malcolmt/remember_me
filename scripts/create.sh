#!/bin/bash

if [ ! $# -eq 1 ]
then
	echo "Usage is $(basename $0) <dirname>"
	exit 1
fi

SCRIPT_DIR=$(dirname $0)

echo "Creating and populating virtual environment. Please wait..."
pip install -E $1 -r $SCRIPT_DIR/requirements.txt

