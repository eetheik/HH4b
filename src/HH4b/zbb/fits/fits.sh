#!/bin/bash

#TXbb_bins=(
#	 0p94to0p96
#	 0p96to0p98
#	 0p98to1p0
#)
#TXbb_bins=(0p99to1p0 0p975to0p99 0p95to0p975)
#TXbb_bins=(0p9to0p95 0p975to1p0 0p95to0p975)
# pt_bins=(350to450 450to550 550to10000)
#TXbb_bins=(0p94to0p97 0p97to0p98 0p98to0p99 0p99to1p0)
TXbb_bins=(0p96to1p0)
pt_bins=(
  350to450 
  #450to550 
  #550to1800
  #450to10000
  #450to1200
)
years=(2023All)
fit_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )


for year in "${years[@]}"; do
  for txbb in "${TXbb_bins[@]}"; do
    for pt in "${pt_bins[@]}"; do
        echo "Processing year: ${year}, TXbb: ${txbb}, pT: ${pt}"
        passbin="TXbb${txbb}pT${pt}"
        failbin="failpT${pt}"
        cards_dir="${fit_dir}/cards/${year}" # removed All
        passbin_dir="${cards_dir}/${passbin}"
        mkdir -p "${passbin_dir}"
        echo "Passbin: ${passbin}"
        cd "${passbin_dir}" || exit
        "${fit_dir}"/fit_zbb.sh --workspace --bfit --dfit --impacts --gofdata --passbin "${passbin}" --failbin "${failbin}" --cards_dir "${cards_dir}" 2>&1 | tee fit.log
        rm -rf "${passbin_dir}/outs"
        mv "${cards_dir}/outs" "${passbin_dir}"
    done
  done
done
