#!/bin/bash

JSON_FILE="nanoindex_v15_scouting.json"
total_size=0

# Extract all file paths from JSON (assumes leaf nodes are lists of XRootD file paths)
file_paths=$(jq -r '.. | arrays? | .[]? | select(test("^root://"))' "$JSON_FILE")

for file in $file_paths; do
    host=$(echo "$file" | cut -d/ -f3)
    remote_path=$(echo "$file" | cut -d/ -f4-)

    # Stat the file and extract the Size field
    size=$(xrdfs "$host" stat "$remote_path" 2>/dev/null | awk '/^Size:/ {print $2}')

    if [[ -n "$size" ]]; then
        total_size=$((total_size + size))
    else
        echo "Warning: Could not stat $file"
    fi
done

echo "Total size in bytes: $total_size"
echo -n "Total size in human-readable format: "
numfmt --to=iec-i --suffix=B "$total_size"
