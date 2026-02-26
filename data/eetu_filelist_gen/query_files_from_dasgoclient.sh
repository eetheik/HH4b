#!/usr/bin/env bash

# List of run eras
ERAS=(
    "2024B"
    "2024C"
    "2024D"
    "2024E"
    "2024F"
    "2024G"
    "2024H"
    "2024I"
)

# DBS instance if needed:
# INSTANCE="instance=prod/phys03"
INSTANCE=""

for ERA in "${ERAS[@]}"; do
    DATASET="/ScoutingPFRun3/Run${ERA}-ScoutNano-v1/NANOAOD"
    OUTFILE="${ERA}_filelist.txt"

    echo "Querying dataset: $DATASET"
    echo "Writing to: $OUTFILE"

    dasgoclient \
        -query="file dataset=${DATASET} ${INSTANCE}" \
        --limit=0 \
        > "${OUTFILE}"

    if [[ $? -eq 0 ]]; then
        echo "Done: ${OUTFILE}"
    else
        echo "ERROR querying ${DATASET}"
    fi

    echo
done
