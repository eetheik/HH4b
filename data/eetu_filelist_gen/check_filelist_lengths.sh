#!/usr/bin/env bash

echo "Checking file counts:"
echo

for FILE in *_filelist.txt; do
    # Skip if no matches
    [[ -e "$FILE" ]] || { echo "No filelists found."; exit 1; }

    COUNT=$(wc -l < "$FILE")
    echo "$FILE : $COUNT files"
done
