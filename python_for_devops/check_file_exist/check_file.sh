#!/bin/bash

path="$1"

if [ ! -e "$path" ]; then
    echo "Path does not exist"

elif [ -f "$path" ]; then
    echo "It is a file"

elif [ -d "$path" ]; then
    echo "It is a directory"

else
    echo "It exists, but it is neither a regular file nor a directory"
fi
