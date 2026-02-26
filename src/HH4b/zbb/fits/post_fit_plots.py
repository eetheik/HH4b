from __future__ import annotations

from collections import OrderedDict
from pathlib import Path

import hist
import numpy as np
import uproot

from HH4b import plotting
from HH4b.hh_vars import data_key
from HH4b.utils import ShapeVar

MAIN_DIR = Path(".").resolve()

# (name in templates -> name in cards)
hist_label_map_inverse = OrderedDict(
    [
        ("Zto2Q_BB", "Zto2Q_BB"),
        ("Zto2Q_CC", "Zto2Q_CC"),
        ("Zto2Q_QQ", "Zto2Q_QQ"),
        # ("Zto2Q_unmatched", "Zto2Q_unmatched"),
        # ("hbb", "hbb"),
        ("Wto2Q", "Wto2Q"),
        ("ttbar", "ttbar"),
        ("qcd", "CMS_bbbb_hadronic_qcd_datadriven"),
        (data_key, "data_obs"),
    ]
)

hist_label_map = {val: key for key, val in hist_label_map_inverse.items()}
samples = list(hist_label_map.values())


m_low, m_high = 40, 180
bins = 5
n_mass_bins = int((m_high - m_low) / bins)

fit_shape_var_mreg = ShapeVar(
    "X2p", #"MSD", #"bbFatJetScoutParTX2pMass", #"bbFatJetScoutingX2pMass",#"FatJetGloParTMassVis", # ?
    r"$m_\mathrm{X2p}$ (GeV)",
    [n_mass_bins, m_low, m_high],
    reg=True,
)
shape_vars = [fit_shape_var_mreg]

shapes = {
    "prefit": "Pre-Fit",
    "postfit": "S+B Post-Fit",
}
samples = [
    "Zto2Q_BB", 
    "Zto2Q_CC", 
    "Zto2Q_QQ", 
    # "Zto2Q_unmatched", 
    "Wto2Q", 
    #"hbb", 
    "ttbar", 
    "qcd"]
all_categories = samples + ["data"]

cards_dir = "cards"
#TXbb_bins = ["0p95to0p975","0p975to0p99", "0p99to1p0"]
# pt_bins = ["350to450", "450to550", "550to10000"]
# pt_bins = ["350to450", "450to500", "500to550", "550to10000"]
#pt_bins = ["550to10000"]
pt_bins = [
"350to450",
 "450to550", 
"550to1800"
]
#pt_bins = ["550to1800"]
#pt_bins = ["350to450"]
#
TXbb_bins=[
#"0p94to0p96", 
#"0p96to0p98", 
"0p96to1p0"
#"0p96to1p0"
]
#TXbb_bins = ["0p9to0p95", "0p95to0p975", "0p975to1p0"]
# TXbb_bins = ["0p94to0p97", "0p97to0p98", "0p98to0p99", "0p99to1p0"]
# pt_bins = ["350to550", "550to10000"]
# years = ["2022", "2023"]
years = [
    # "2023BPix",
    "2023"
    ]

plot_ylims = {
    "2022": {
        # # "TXbb0p95to0p975pT350to550": 720,
        # "TXbb0p95to0p975pT350to450": 225,
        # "TXbb0p95to0p975pT450to550": 400,
        # "TXbb0p95to0p975pT550to10000": 300,
        # # "TXbb0p975to0p99pT350to550": 450,
        # "TXbb0p975to0p99pT350to450": 130,
        # "TXbb0p975to0p99pT450to550": 260,
        # "TXbb0p975to0p99pT550to10000": 225,
        # # "TXbb0p99to1p0pT350to550": 300,
        # "TXbb0p99to1p0pT350to450": 75,
        # "TXbb0p99to1p0pT450to550": 190,
        # "TXbb0p99to1p0pT550to10000": 225,
    },
    "2023": {
        # # "TXbb0p95to0p975pT350to550": 650,
        # "TXbb0p95to0p975pT350to450": 210,
        # "TXbb0p95to0p975pT450to550": 370,
        # "TXbb0p95to0p975pT550to10000": 275,
        # # "TXbb0p975to0p99pT350to550": 400,
        # "TXbb0p975to0p99pT350to450": 120,
        # "TXbb0p975to0p99pT450to550": 230,
        # "TXbb0p975to0p99pT550to10000": 200,
        # # "TXbb0p99to1p0pT350to550": 275,
        # "TXbb0p99to1p0pT450to550": 170,
        # "TXbb0p99to1p0pT550to10000": 225,
        # "TXbb0p99to1p0pT550to10000": 200,
    },
    "2023BPix": {

    },
    "2023C": {

    }
}

for year in years:
    for TXbb_bin in TXbb_bins:
        for pt_bin in pt_bins:
            # define the pass bin
            pass_bin = f"TXbb{TXbb_bin}pT{pt_bin}"
            plot_dir = MAIN_DIR / f"postfit_plots/{year}All/{pass_bin}"
            plot_dir.mkdir(exist_ok=True, parents=True)
            file = uproot.open(f"cards/{year}All/{pass_bin}/FitShapes.root") # Removed All from after {year} since I'm not merging years rn
            print(f"Opened file for {year}, {pass_bin}")

            # regions
            selection_regions_labels = {
                f"passbin{pass_bin}": "Pass",
                "fail": "Fail",
            }
            signal_regions = [f"passbin{pass_bin}"]

            bins = list(selection_regions_labels.keys())
            selection_regions = {key: selection_regions_labels[key] for key in bins}

            # load the histograms
            hists = {}
            for shape in shapes:
                hists[shape] = {
                    region: hist.Hist(
                        hist.axis.StrCategory(all_categories, name="Sample"),
                        *[shape_var.axis for shape_var in shape_vars],
                        storage="double",
                    )
                    for region in selection_regions
                }

                for region in selection_regions:
                    h = hists[shape][region]
                    try:
                        templates = file[f"{region}_{shape}"]
                    except KeyError as e:
                        print(f"KeyError for {year}, {region}, {shape}")
                        continue
                    # print(templates)
                    for key, file_key in hist_label_map_inverse.items():
                        if key != data_key:
                            if file_key not in templates:
                                print(f"No {key} in {region}")
                                continue

                            data_key_index = np.where(np.array(list(h.axes[0])) == key)[0][0]
                            h.view(flow=False)[data_key_index, :] = templates[file_key].values()

                    data_key_index = np.where(np.array(list(h.axes[0])) == data_key)[0][0]
                    h.view(flow=False)[data_key_index, :] = np.nan_to_num(
                        templates[hist_label_map_inverse[data_key]].values()
                    )

            # plotting
            pass_ratio_ylims = [0.5, 1.5]
            # fail_ratio_ylims = [0.5, 1.5]
            fail_ratio_ylims = [0.5, 1.5]

            for shape, shape_label in shapes.items():
                for region, region_label in selection_regions.items():
                    pass_region = region.startswith("pass")
                    for shape_var in shape_vars:
                        if pass_region and pass_bin in plot_ylims[year]:
                            ymax = plot_ylims[year][pass_bin]
                        else:
                            ymax = None

                        # print(hists[shape][region])
                        plot_params = {
                            "hists": hists[shape][region],
                            "sig_keys": [],
                            "sig_scale_dict": None,
                            "bg_keys": samples,
                            "show": True,
                            "year": "2023All",
                            "xlim": m_high,
                            "xlim_low": m_low,
                            "ylim": ymax,
                            "ratio_ylims": pass_ratio_ylims if pass_region else fail_ratio_ylims,
                            "title": f"{shape_label} {region_label} Region",
                            "name": f"{plot_dir}/{shape}_{region}_{shape_var.var}.pdf",
                            "bg_order": reversed(samples),
                            "energy": 13.6,
                            "show": False,
                        }

                        plotting.ratioHistPlot(**plot_params)

                        # if pass_region and "fail" in selection_regions:
                        #     hists_pass = hists[shape].get(region)   # pass hist
                        #     hists_fail = hists[shape].get("fail")   # fail hist

                        #     if hists_pass is None:
                        #         print(f"No pass hist for {region} ({shape}) — skipping subtracted plot.")
                        #     elif hists_fail is None:
                        #         print(f"No fail hist for {region} ({shape}) — skipping subtracted plot.")
                        #     else:
                        #         sub_name = f"{plot_dir}/{shape}_{pass_bin}_{shape_var.var}_subtracted.pdf"
                        #         sub_title = f"Subtracted ({region_label} - Fail) {shape_label} {shape_var.var}"

                        #         # bg_order: keep same ordering as in ratio plot (you used reversed(samples))
                        #         bg_order_for_sub = plot_params.get("bg_order", None)

                                
                        #         plotting.subtractedHistPlot(
                        #             hists=hists_pass,
                        #             hists_fail=hists_fail,
                        #             year=f"{year}",
                        #             bg_keys=samples,
                        #             bg_err=None,
                        #             sortyield=False,
                        #             title=sub_title,
                        #             name=sub_name,
                        #             xlim=m_high,
                        #             xlim_low=m_low,
                        #             ylim=ymax,
                        #             ylim_low=None,
                                #     show=False,
                                #     bg_err_type="shaded",
                                #     plot_data=True,
                                #     bg_order=bg_order_for_sub,
                                #     log=False,
                                #     logx=False,
                                #     ratio_ylims=plot_params["ratio_ylims"],
                                #     energy=plot_params.get("energy", "13.6"),
                                # )
                        
