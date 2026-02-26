from __future__ import annotations

import contextlib
from pathlib import Path

from coffea.jetmet_tools import CorrectedJetsFactory, CorrectedMETFactory, JECStack
from coffea.lookup_tools import extractor

# This function builds the run3 JECs for scouting. Note that this is how you have to implement JECs in coffea.

jec_name_map = {
    "JetPt": "pt",
    "JetMass": "mass",
    "JetEta": "eta",
    "JetA": "area",
    "ptGenJet": "pt_gen",
    "ptRaw": "pt_raw",
    "massRaw": "mass_raw",
    "Rho": "event_rho",
    "METpt": "pt",
    "METphi": "phi",
    "JetPhi": "phi",
    "UnClusteredEnergyDeltaX": "MetUnclustEnUpDeltaX",
    "UnClusteredEnergyDeltaY": "MetUnclustEnUpDeltaY",
}


def jet_factory_factory(files):
    ext = extractor()
    with contextlib.ExitStack() as stack:
        real_files = [stack.enter_context(Path(f"data/jec/{f}")) for f in files]
        print(real_files)
        ext.add_weight_sets([f"* * {file}" for file in real_files])
        ext.finalize()

    jec_stack = JECStack(ext.make_evaluator())
    return CorrectedJetsFactory(jec_name_map, jec_stack)


jet_factory = {
    # "2022mc": jet_factory_factory(
    #     files=[
    #         "Summer2222Sep2023_V2_MC_L1FastJet_AK4PFPuppi.jec.txt.gz",
    #         "Summer2222Sep2023_V2_MC_L2Relative_AK4PFPuppi.jec.txt.gz",
    #         "Summer2222Sep2023_V2_MC_UncertaintySources_AK4PFPuppi.junc.txt.gz",
    #         "Summer2222Sep2023_V2_MC_Uncertainty_AK4PFPuppi.junc.txt.gz",
    #         "Summer2222Sep2023_JRV1_MC_PtResolution_AK4PFPuppi.jr.txt.gz",
    #         "Summer2222Sep2023_JRV1_MC_SF_AK4PFPuppi.jersf.txt.gz",
    #     ],
    # ),
    # "2022EEmc": jet_factory_factory(
    #     files=[
    #         "Summer22EE22Sep2023_V2_MC_L1FastJet_AK4PFPuppi.jec.txt.gz",
    #         "Summer22EE22Sep2023_V2_MC_L2Relative_AK4PFPuppi.jec.txt.gz",
    #         "Summer22EE22Sep2023_V2_MC_UncertaintySources_AK4PFPuppi.junc.txt.gz",
    #         "Summer22EE22Sep2023_V2_MC_Uncertainty_AK4PFPuppi.junc.txt.gz",
    #         "Summer22EE22Sep2023_JRV1_MC_PtResolution_AK4PFPuppi.jr.txt.gz",
    #         "Summer22EE22Sep2023_JRV1_MC_SF_AK4PFPuppi.jersf.txt.gz",
    #     ]
    # ),
    "2023mc": jet_factory_factory(
        files=[
            '2022_V1_MC_L1FastJet_AK4PFHLT.jec.txt',
            '2022_V1_MC_L2Relative_AK4PFHLT.jec.txt',
            '2022_V1_MC_L2L3Residual_AK4PFHLT.jec.txt',
            '2022_V1_MC_L3Absolute_AK4PFHLT.jec.txt'
            #'Summer23Prompt23_V3_MC_L1FastJet_AK4PFPuppi.jec.txt',
            #'Summer23Prompt23_V3_MC_L2Relative_AK4PFPuppi.jec.txt',
            #'Summer23Prompt23_V3_MC_UncertaintySources_AK4PFPuppi.junc.txt',
            #'Summer23Prompt23_V3_MC_Uncertainty_AK4PFPuppi.junc.txt',
            # 'Summer23Prompt23_RunCv1234_JRV1_MC_SF_AK4PFPuppi.jersf.txt',
            # 'Summer23Prompt23_RunCv1234_JRV1_MC_PtResolution_AK4PFPuppi.jr.txt'
        ],
    ),
    "2023BPixmc": jet_factory_factory(
        files=[
            'Winter24_V1_MC_L1FastJet_AK4PFHLT.jec.txt',
            'Winter24_V1_MC_L2Relative_AK4PFHLT.jec.txt',
            'Winter24_V1_MC_L2L3Residual_AK4PFHLT.jec.txt',
            'Winter24_V1_MC_L3Absolute_AK4PFHLT.jec.txt'

	    #'Summer23BPixPrompt23_V3_MC_L1FastJet_AK4PFPuppi.jec.txt',
            #'Summer23BPixPrompt23_V3_MC_L2Relative_AK4PFPuppi.jec.txt',
            #'Summer23BPixPrompt23_V3_MC_UncertaintySources_AK4PFPuppi.junc.txt',
            #'Summer23BPixPrompt23_V3_MC_Uncertainty_AK4PFPuppi.junc.txt',

	    # 'Summer23BPixPrompt23_RunD_JRV1_MC_SF_AK4PFPuppi.jersf.txt', 
            # 'Summer23BPixPrompt23_RunD_JRV1_MC_PtResolution_AK4PFPuppi.jr.txt'
        ],
    ),
    "2024mc": jet_factory_factory(
        files=[

            'Winter24_V1_MC_L1FastJet_AK4PFHLT.jec.txt',
            'Winter24_V1_MC_L2Relative_AK4PFHLT.jec.txt',
            'Winter24_V1_MC_L2L3Residual_AK4PFHLT.jec.txt',
            'Winter24_V1_MC_L3Absolute_AK4PFHLT.jec.txt'
        ],
    ),
    # # data
    # "2022_runCD": jet_factory_factory(
    #     files=[
    #         # "Summer2222Sep2023_RunCD_V2_DATA_L1FastJet_AK4PFPuppi.jec.txt.gz",
    #         "Summer2222Sep2023_RunCD_V2_DATA_L2Relative_AK4PFPuppi.jec.txt.gz",
    #         "Summer2222Sep2023_RunCD_V2_DATA_L2L3Residual_AK4PFPuppi.jec.txt.gz",
    #     ],
    # ),
    # "2022EE_runE": jet_factory_factory(
    #     files=[
    #         # "Summer22EE22Sep2023_RunE_V2_DATA_L1FastJet_AK4PFPuppi.jec.txt.gz",
    #         "Summer22EE22Sep2023_RunE_V2_DATA_L2Relative_AK4PFPuppi.jec.txt.gz",
    #         "Summer22EE22Sep2023_RunE_V2_DATA_L2L3Residual_AK4PFPuppi.jec.txt.gz",
    #     ],
    # ),
    # "2022EE_runF": jet_factory_factory(
    #     files=[
    #         # "Summer22EE22Sep2023_RunF_V2_DATA_L1FastJet_AK4PFPuppi.jec.txt.gz",
    #         "Summer22EE22Sep2023_RunF_V2_DATA_L2Relative_AK4PFPuppi.jec.txt.gz",
    #         "Summer22EE22Sep2023_RunF_V2_DATA_L2L3Residual_AK4PFPuppi.jec.txt.gz",
    #     ],
    # ),
    # "2022EE_runG": jet_factory_factory(
    #     files=[
    #         # "Summer22EE22Sep2023_RunG_V2_DATA_L1FastJet_AK4PFPuppi.jec.txt.gz",
    #         "Summer22EE22Sep2023_RunG_V2_DATA_L2Relative_AK4PFPuppi.jec.txt.gz",
    #         "Summer22EE22Sep2023_RunG_V2_DATA_L2L3Residual_AK4PFPuppi.jec.txt.gz",
    #     ],
    #),
    "2023_runCv123": jet_factory_factory(
        files=[ # For HLT jets we have no puppi, so we apply exactly same JECs to data and MC

            '2022_V1_MC_L1FastJet_AK4PFHLT.jec.txt',
            '2022_V1_MC_L2Relative_AK4PFHLT.jec.txt',
            '2022_V1_MC_L2L3Residual_AK4PFHLT.jec.txt',
            '2022_V1_MC_L3Absolute_AK4PFHLT.jec.txt'
            # "Summer23Prompt23_RunCv123_V1_DATA_L1FastJet_AK4PFPuppi.jec.txt.gz",
            #'Summer23Prompt23_RunCv123_V3_DATA_L2Relative_AK4PFPuppi.jec.txt', 
            #'Summer23Prompt23_RunCv123_V3_DATA_L2L3Residual_AK4PFPuppi.jec.txt'
        ],
    ),
    "2023_runCv4": jet_factory_factory(
        files=[

            '2022_V1_MC_L1FastJet_AK4PFHLT.jec.txt',
            '2022_V1_MC_L2Relative_AK4PFHLT.jec.txt',
            '2022_V1_MC_L2L3Residual_AK4PFHLT.jec.txt',
            '2022_V1_MC_L3Absolute_AK4PFHLT.jec.txt'

            # "Summer23Prompt23_RunCv4_V1_DATA_L1FastJet_AK4PFPuppi.jec.txt.gz",
            #'Summer23Prompt23_RunCv4_V3_DATA_L2Relative_AK4PFPuppi.jec.txt', 
            #'Summer23Prompt23_RunCv4_V3_DATA_L2L3Residual_AK4PFPuppi.jec.txt'
        ],
    ),
    "2023BPix_runD": jet_factory_factory(
        files=[

            'Winter24_V1_MC_L1FastJet_AK4PFHLT.jec.txt',
            'Winter24_V1_MC_L2Relative_AK4PFHLT.jec.txt',
            'Winter24_V1_MC_L2L3Residual_AK4PFHLT.jec.txt',
            'Winter24_V1_MC_L3Absolute_AK4PFHLT.jec.txt'

            # "Summer23BPixPrompt23_RunD_V1_DATA_L1FastJet_AK4PFPuppi.jec.txt.gz",
            #'Summer23BPixPrompt23_RunD_V3_DATA_L2Relative_AK4PFPuppi.jec.txt', 
            #'Summer23BPixPrompt23_RunD_V3_DATA_L2L3Residual_AK4PFPuppi.jec.txt'
        ],
    ),
    "2024": jet_factory_factory(
        files=[

            'Winter24_V1_MC_L1FastJet_AK4PFHLT.jec.txt',
            'Winter24_V1_MC_L2Relative_AK4PFHLT.jec.txt',
            'Winter24_V1_MC_L2L3Residual_AK4PFHLT.jec.txt',
            'Winter24_V1_MC_L3Absolute_AK4PFHLT.jec.txt'
        ],
    ),
}

fatjet_factory = {
    # "2022mc": jet_factory_factory(
    #     files=[
    #         "Summer2222Sep2023_V2_MC_L1FastJet_AK8PFPuppi.jec.txt.gz",
    #         "Summer2222Sep2023_V2_MC_L2Relative_AK8PFPuppi.jec.txt.gz",
    #         "Summer2222Sep2023_V2_MC_UncertaintySources_AK8PFPuppi.junc.txt.gz",
    #         "Summer2222Sep2023_V2_MC_Uncertainty_AK8PFPuppi.junc.txt.gz",
    #         "Summer2222Sep2023_JRV1_MC_PtResolution_AK8PFPuppi.jr.txt.gz",
    #         "Summer2222Sep2023_JRV1_MC_SF_AK8PFPuppi.jersf.txt.gz",
    #     ],
    # ),
    # "2022EEmc": jet_factory_factory(
    #     files=[
    #         "Summer22EE22Sep2023_V2_MC_L1FastJet_AK8PFPuppi.jec.txt.gz",
    #         "Summer22EE22Sep2023_V2_MC_L2Relative_AK8PFPuppi.jec.txt.gz",
    #         "Summer22EE22Sep2023_V2_MC_UncertaintySources_AK8PFPuppi.junc.txt.gz",
    #         "Summer22EE22Sep2023_V2_MC_Uncertainty_AK8PFPuppi.junc.txt.gz",
    #         "Summer22EE22Sep2023_JRV1_MC_PtResolution_AK8PFPuppi.jr.txt.gz",
    #         "Summer22EE22Sep2023_JRV1_MC_SF_AK8PFPuppi.jersf.txt.gz",
    #     ]
    # ),
    "2023mc": jet_factory_factory(
        files=[

            '2022_V1_MC_L1FastJet_AK8PFHLT.jec.txt',
            '2022_V1_MC_L2Relative_AK8PFHLT.jec.txt',
            '2022_V1_MC_L2L3Residual_AK8PFHLT.jec.txt',
            '2022_V1_MC_L3Absolute_AK8PFHLT.jec.txt'

            #'Summer23Prompt23_V3_MC_L1FastJet_AK8PFPuppi.jec.txt', 
            #'Summer23Prompt23_V3_MC_L2Relative_AK8PFPuppi.jec.txt', 
            #'Summer23Prompt23_V3_MC_UncertaintySources_AK8PFPuppi.junc.txt', 
            #'Summer23Prompt23_V3_MC_Uncertainty_AK8PFPuppi.junc.txt',
            
            # 'Summer23Prompt23_RunCv1234_JRV1_MC_PtResolution_AK8PFPuppi.jr.txt',
            # 'Summer23Prompt23_RunCv1234_JRV1_MC_SF_AK8PFPuppi.jersf.txt' 
        ],
    ),
    "2023BPixmc": jet_factory_factory(
        files=[

            'Winter24_V1_MC_L1FastJet_AK8PFHLT.jec.txt',
            'Winter24_V1_MC_L2Relative_AK8PFHLT.jec.txt',
            'Winter24_V1_MC_L2L3Residual_AK8PFHLT.jec.txt',
            'Winter24_V1_MC_L3Absolute_AK8PFHLT.jec.txt'

            #'Summer23BPixPrompt23_V3_MC_L1FastJet_AK8PFPuppi.jec.txt', 
            #'Summer23BPixPrompt23_V3_MC_L2Relative_AK8PFPuppi.jec.txt', 
            #'Summer23BPixPrompt23_V3_MC_UncertaintySources_AK8PFPuppi.junc.txt', 
            #'Summer23BPixPrompt23_V3_MC_Uncertainty_AK8PFPuppi.junc.txt',

            # 'Summer23BPixPrompt23_RunD_JRV1_MC_PtResolution_AK8PFPuppi.jr.txt',
            # 'Summer23BPixPrompt23_RunD_JRV1_MC_SF_AK8PFPuppi.jersf.txt'
        ],
    ),
    "2024mc": jet_factory_factory(
        files=[

            'Winter24_V1_MC_L1FastJet_AK8PFHLT.jec.txt',
            'Winter24_V1_MC_L2Relative_AK8PFHLT.jec.txt',
            'Winter24_V1_MC_L2L3Residual_AK8PFHLT.jec.txt',
            'Winter24_V1_MC_L3Absolute_AK8PFHLT.jec.txt'

        ],
    ),
    # "2022_runCD": jet_factory_factory(
    #     files=[
    #         # "Summer2222Sep2023_RunCD_V2_DATA_L1FastJet_AK8PFPuppi.jec.txt.gz",
    #         "Summer2222Sep2023_RunCD_V2_DATA_L2Relative_AK8PFPuppi.jec.txt.gz",
    #         "Summer2222Sep2023_RunCD_V2_DATA_L2L3Residual_AK8PFPuppi.jec.txt.gz",
    #     ],
    # ),
    # "2022EE_runE": jet_factory_factory(
    #     files=[
    #         # "Summer22EE22Sep2023_RunE_V2_DATA_L1FastJet_AK8PFPuppi.jec.txt.gz",
    #         "Summer22EE22Sep2023_RunE_V2_DATA_L2Relative_AK8PFPuppi.jec.txt.gz",
    #         "Summer22EE22Sep2023_RunE_V2_DATA_L2L3Residual_AK8PFPuppi.jec.txt.gz",
    #     ],
    # ),
    # "2022EE_runF": jet_factory_factory(
    #     files=[
    #         # "Summer22EE22Sep2023_RunF_V2_DATA_L1FastJet_AK8PFPuppi.jec.txt.gz",
    #         "Summer22EE22Sep2023_RunF_V2_DATA_L2Relative_AK8PFPuppi.jec.txt.gz",
    #         "Summer22EE22Sep2023_RunF_V2_DATA_L2L3Residual_AK8PFPuppi.jec.txt.gz",
    #     ],
    # ),
    # "2022EE_runG": jet_factory_factory(
    #     files=[
    #         # "Summer22EE22Sep2023_RunG_V2_DATA_L1FastJet_AK8PFPuppi.jec.txt.gz",
    #         "Summer22EE22Sep2023_RunG_V2_DATA_L2Relative_AK8PFPuppi.jec.txt.gz",
    #         "Summer22EE22Sep2023_RunG_V2_DATA_L2L3Residual_AK8PFPuppi.jec.txt.gz",
    #     ],
    # ),
    "2023_runCv123": jet_factory_factory(
        files=[

            '2022_V1_MC_L1FastJet_AK8PFHLT.jec.txt',
            '2022_V1_MC_L2Relative_AK8PFHLT.jec.txt',
            '2022_V1_MC_L2L3Residual_AK8PFHLT.jec.txt',
            '2022_V1_MC_L3Absolute_AK8PFHLT.jec.txt'

            # "Summer23Prompt23RunCv123_V1_DATA_L1FastJet_AK8PFPuppi.jec.txt.gz",

#            'Summer23Prompt23_RunCv123_V3_DATA_L2Relative_AK8PFPuppi.jec.txt', 
#            'Summer23Prompt23_RunCv123_V3_DATA_L2L3Residual_AK8PFPuppi.jec.txt'
        ],
    ),
    "2023_runCv4": jet_factory_factory(
        files=[

            '2022_V1_MC_L1FastJet_AK8PFHLT.jec.txt',
            '2022_V1_MC_L2Relative_AK8PFHLT.jec.txt',
            '2022_V1_MC_L2L3Residual_AK8PFHLT.jec.txt',
            '2022_V1_MC_L3Absolute_AK8PFHLT.jec.txt'

            # "Summer23Prompt23_RunCv4_V1_DATA_L1FastJet_AK8PFPuppi.jec.txt.gz",

            #'Summer23Prompt23_RunCv4_V3_DATA_L2Relative_AK8PFPuppi.jec.txt', 
            #'Summer23Prompt23_RunCv4_V3_DATA_L2L3Residual_AK8PFPuppi.jec.txt'
        ],
    ),
    "2023BPix_runD": jet_factory_factory(
        files=[

            'Winter24_V1_MC_L1FastJet_AK8PFHLT.jec.txt',
            'Winter24_V1_MC_L2Relative_AK8PFHLT.jec.txt',
            'Winter24_V1_MC_L2L3Residual_AK8PFHLT.jec.txt',
            'Winter24_V1_MC_L3Absolute_AK8PFHLT.jec.txt'

            # "Summer23BPixPrompt23_RunD_V1_DATA_L1FastJet_AK8PFPuppi.jec.txt.gz",

#            'Summer23BPixPrompt23_RunD_V3_DATA_L2Relative_AK8PFPuppi.jec.txt', 
 #           'Summer23BPixPrompt23_RunD_V3_DATA_L2L3Residual_AK8PFPuppi.jec.txt'
        ],
    ),
    "2024": jet_factory_factory(
        files=[
            # Can these be updated to Summer24 like is done in offline analysis currently?
            'Winter24_V1_MC_L1FastJet_AK8PFHLT.jec.txt',
            'Winter24_V1_MC_L2Relative_AK8PFHLT.jec.txt',
            'Winter24_V1_MC_L2L3Residual_AK8PFHLT.jec.txt',
            'Winter24_V1_MC_L3Absolute_AK8PFHLT.jec.txt'

        ],
    ),
}

met_factory = CorrectedMETFactory(jec_name_map)

if __name__ == "__main__":
    import argparse
    import gzip

    import cloudpickle

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--output", default="jec_compiled_scouting2023_2024.pkl.gz", type=str)
    args = parser.parse_args()

    with gzip.open(args.output, "wb") as fout:
        cloudpickle.dump(
            {
                "jet_factory": jet_factory,
                "fatjet_factory": fatjet_factory,
                "met_factory": met_factory,
            },
            fout,
        )
