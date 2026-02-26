import os
import subprocess
import json


def get_all_files_in_T2_directory(T2_REDIRECTOR: str, REMOTE_PATH: str) -> list[str]:
    """
    Get all files in a T2 directory and its subdirectories using ls recursively.
    
    Args:
        T2_REDIRECTOR (str): The redirector for the T2 storage site (e.g., "root://hip-cms-se.csc.fi").
        REMOTE_PATH (str): The directory on the T2 machine to search in
        
    Returns:
        list[str]: A list of file paths.
    """

    CMD = ["xrdfs", T2_REDIRECTOR, "ls", "-R", REMOTE_PATH]

    try:
        FILES = subprocess.check_output(CMD, text=True).split("\n")
        return [f"{T2_REDIRECTOR}://{file}" for file in FILES if file and file.endswith(".root")] # file exists and ends with .root, perhaps just ends with .root is sufficient
    
    except Exception as e:
        print(f"Error executing command: {' '.join(CMD)}. Error: {e}")
        return []


def get_all_files_in_EOS_directory(EOS_DIR: str) -> list[str]:
    root_files = []
    for root, dirs, files in os.walk(EOS_DIR):
        for f in files:
            if f.endswith(".root"):
                root_files.append(os.path.join(root, f))
    return root_files

    
def pick_files_with_substring(files: list[str], substring: str) -> list[str]:
    """
    Pick files matching a specific substring from a list of files.
    
    Args:
        files (list[str]): List of file paths.
        substring: substring to match in file names.
        
    Returns:
        list[str]: Subset of files that contain the substring.
    """
    return [file for file in files if substring in file]
    
       
def get_all_files_from_dasgoclient_output(T2_REDIRECTOR: str, filepath: str) -> list[str]:
    """
    Intended to be used after running something to the effect of

    dasgoclient --query="file dataset={REMOTE_PATH}"=file.txt

    2023D = /ScoutingPFRun3/Run2023D-ScoutNano-v1/NANOAOD
    2023C = /ScoutingPFRun3/Run2023C-ScoutNano-v1/NANOAOD
    """
    try:
        with open(filepath, "r") as f:
            lines = f.read().splitlines()
        return [f"{T2_REDIRECTOR}://{line}" for line in lines if line.endswith(".root")]
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return []



if __name__ == "__main__":
    T2_REDIRECTOR_HELSINKI = "root://hip-cms-se.csc.fi"
    T2_REDIRECTOR_CMS_XRD = "root://cms-xrd-global.cern.ch"

    # ScoutingPFMonitor_2024_REMOTE_PATH = "/store/user/pinkaew/scouting_nano_dev_v0p6_golden/ScoutingPFMonitor" # Won't use these
    ScoutingMC_2023_REMOTE_PATH = "/store/user/pinkaew/scouting_hbb/samples/scouting_nano_v02_mc" # On Helsinki T2
    # ScoutingData_2023D_12p5_REMOTE_PATH = "/store/user/pinkaew/scouting_hbb/samples/ScoutingNano/Data2023/V02/Golden/ScoutingPFRun3" # On Helsinki T2
    
    # ScoutingData_2023D_REMOTE_PATH = "/store/data/Run2023D/ScoutingPFRun3/NANOAOD/ScoutNano-v1/" # On CERN T2
    # ScoutingData_2023C_REMOTE_PATH = "/store/data/Run2023C/ScoutingPFRun3/NANOAOD/ScoutNano-v1/" # On CERN T2

    ScoutingMC_2024_EOS_PATH = "/eos/cms/store/cmst3/group/vhcc/ScoutingNanoAOD/2024/mc"
    ScoutingData_2024_EOS_PATH = "/eos/cms/store/cmst3/group/vhcc/ScoutingNanoAOD/2024/data"

    # Is it /ScoutingPFRun3/Run2023C-ScoutNano-v1/NANOAOD?

    # TOOD: Write cleaner and more modular code to generate the filelist
    filelist = {
        "2023": {
            "VJetsLO": {

            },
            "VJets": {
                
            },
            "Data": {

            },
            "JetMET": {

            },
            "QCD": {

            },
            "TT": {

            }
        },
        "2023BPix": {
            "VJetsLO": {

            },
            "VJets": {

            },
            "Data": {

            },
            "JetMET": {

            },
            "QCD": {

            },
            "TT": {

            }
        },
        "2024": {
            "VJetsLO": {

            },
            "VJets": {
                
            },
            "Data": {

            },
            "JetMET": {

            },
            "QCD": {

            },
            "TT": {

            }
        }
    }

    #JetMet files from Zichun

    with open("../nanoindex_v14_25v2.json", "r") as f:
        ZichunFileList = json.load(f)

    Run2023C_JetMET_list = []

    filelist["2023BPix"]["JetMET"] = ZichunFileList["2023BPix"]["JetMET"]
    filelist["2023"]["JetMET"] = ZichunFileList["2023"]["JetMET"]
    # Could add 2024 here from Zichun

    Zto2Q_2Jets_subsamples_list = [
        "Zto2Q-2Jets_PTQQ-100to200_1J",
        "Zto2Q-2Jets_PTQQ-100to200_2J",
        "Zto2Q-2Jets_PTQQ-200to400_1J",
        "Zto2Q-2Jets_PTQQ-200to400_2J",
        "Zto2Q-2Jets_PTQQ-400to600_1J",
        "Zto2Q-2Jets_PTQQ-400to600_2J",
        "Zto2Q-2Jets_PTQQ-600_1J",
        "Zto2Q-2Jets_PTQQ-600_2J",
    ]

    Wto2Q_2Jets_subsamples_list = [
        "Wto2Q-2Jets_PTQQ-100to200_1J",
        "Wto2Q-2Jets_PTQQ-100to200_2J",
        "Wto2Q-2Jets_PTQQ-200to400_1J",
        "Wto2Q-2Jets_PTQQ-200to400_2J",
        "Wto2Q-2Jets_PTQQ-400to600_1J",
        "Wto2Q-2Jets_PTQQ-400to600_2J",
        "Wto2Q-2Jets_PTQQ-600_1J",
        "Wto2Q-2Jets_PTQQ-600_2J",
    ]

    Zto2Q_4Jets_HT_subsamples_list = [
        "Zto2Q-4Jets_HT-200to400",
        "Zto2Q-4Jets_HT-400to600",
        "Zto2Q-4Jets_HT-600to800",
        "Zto2Q-4Jets_HT-800"
    ]

    Wto2Q_3Jets_HT_subsamples_list = [
        "Wto2Q-3Jets_HT-200to400",
        "Wto2Q-3Jets_HT-400to600",
        "Wto2Q-3Jets_HT-600to800",
        "Wto2Q-3Jets_HT-800"
    ]

    TT_subsamples_list = [ 
        "TTto2L2Nu",
        "TTto4Q", # Was missing for BPix (check)
        "TTtoLNu2Q"
    ]

    QCD_subsamples_list = [
        "QCD_PT-170to300",
        "QCD_PT-300to470",
        "QCD_PT-470to600",
        "QCD_PT-600to800",
        "QCD_PT-800to1000",
        "QCD_PT-1000to1400",
        "QCD_PT-1800to2400",
        "QCD_PT-1400to1800",
        "QCD_PT-2400to3200",
        "QCD_PT-3200",
    ]

    Beatriz_2024MC_samples = { # Compare to Zichun's sample for the naming scheme
        "VJetsLO": [
            "Wto2Q-3Jets_Bin-HT-100to400",
            "Wto2Q-3Jets_Bin-HT-1500to2500",
            "Wto2Q-3Jets_Bin-HT-2500",
            "Wto2Q-3Jets_Bin-HT-400to800",
            "Wto2Q-3Jets_Bin-HT-800to1500",
            "Zto2Q-4Jets_Bin-HT-100to400",
            "Zto2Q-4Jets_Bin-HT-1500to2500",
            "Zto2Q-4Jets_Bin-HT-2500",
            "Zto2Q-4Jets_Bin-HT-400to800",
            "Zto2Q-4Jets_Bin-HT-800to1500",
        ],
        "TT": [ 
            "TTto2L2Nu",
            "TTto4Q", 
            "TTtoLNu2Q"
        ],
        "QCD": [ # TuneCP5_13p6TeV_madgraphMLM-pythia8
            "QCD-4Jets_Bin-HT-100to200",
            "QCD-4Jets_Bin-HT-200to400",
            "QCD-4Jets_Bin-HT-400to600",
            "QCD-4Jets_Bin-HT-600to800",
            "QCD-4Jets_Bin-HT-800to1000",
            "QCD-4Jets_Bin-HT-1000to1200",
            "QCD-4Jets_Bin-HT-1200to1500",
            "QCD-4Jets_Bin-HT-1500to2000",
            "QCD-4Jets_Bin-HT-2000"
        ]
        # No VJets NLO samples
    }
    
    ScoutingData2023BPix_runs_list = [ 
        "Run2023D",
    ]

    ScoutingData2023_runs_list = [
        "Run2023C"
    ]

    ScoutingData2024_runs_list = [ 
        "Run2024B",
        "Run2024C", 
        "Run2024D",
        "Run2024E",
        "Run2024F",
        "Run2024G",
        "Run2024H",
        "Run2024I"
    ]

    # All MC files (2023)
    ScoutingMC2023_all_files_list = get_all_files_in_T2_directory(
        T2_REDIRECTOR_HELSINKI, 
        ScoutingMC_2023_REMOTE_PATH
    )

    # All MC files (2024)
    ScoutingMC2024_all_files_list = get_all_files_in_EOS_directory(
        ScoutingMC_2024_EOS_PATH
    )

    # MC files subsampled by year
    ScoutingMC_2023BPix_all_files_list = pick_files_with_substring(
        ScoutingMC2023_all_files_list,
        "Run3Summer23BPixDRPremix_AODSIM"
    )
    ScoutingMC_2023C_all_files_list = pick_files_with_substring(
        ScoutingMC2023_all_files_list,
        "Run3Summer23DRPremix_AODSIM"
    ) 

    ScoutingMC_2024_all_files_list = pick_files_with_substring(
        ScoutingMC2024_all_files_list,
        "RunIII2024Summer24MiniAOD"
    ) 



    # Data files
    ScoutingData2023D_all_files_list = get_all_files_from_dasgoclient_output(
        T2_REDIRECTOR_CMS_XRD,
        "2023D_filelist.txt"
    )
    ScoutingData2023C_all_files_list = get_all_files_from_dasgoclient_output(
        T2_REDIRECTOR_CMS_XRD,
        "2023C_filelist.txt"
    )

    # ScoutingDataFull2024_all_files_list = get_all_files_in_EOS_directory(
    #     ScoutingData_2024_EOS_PATH
    # )

    for run in ScoutingData2024_runs_list:
        filelist["2024"]["Data"][run] = get_all_files_from_dasgoclient_output(
            T2_REDIRECTOR_CMS_XRD,
            f"{run[3:]}_filelist.txt" # Run is first three characters, then 2023D etc. 
        )
    
    for sample, subsamples in Beatriz_2024MC_samples.items():
        for subsample in subsamples:
            filelist["2024"][sample][subsample] = pick_files_with_substring(
                ScoutingMC_2024_all_files_list, 
                subsample
            )


    for subsample in Zto2Q_4Jets_HT_subsamples_list + Wto2Q_3Jets_HT_subsamples_list:
        filelist["2023BPix"]["VJetsLO"][subsample] = pick_files_with_substring(
            ScoutingMC_2023BPix_all_files_list, 
            subsample
        )

        filelist["2023"]["VJetsLO"][subsample] = pick_files_with_substring(
            ScoutingMC_2023C_all_files_list,
            subsample
        )

    for subsample in Zto2Q_2Jets_subsamples_list + Wto2Q_2Jets_subsamples_list:
        filelist["2023BPix"]["VJets"][subsample] = pick_files_with_substring(
            ScoutingMC_2023BPix_all_files_list, 
            subsample
        )

        filelist["2023"]["VJets"][subsample] = pick_files_with_substring(
            ScoutingMC_2023C_all_files_list,
            subsample
        )
    
    for subsample in QCD_subsamples_list:
        filelist["2023BPix"]["QCD"][subsample] = pick_files_with_substring(
            ScoutingMC_2023BPix_all_files_list,
            subsample
        )

        filelist["2023"]["QCD"][subsample] = pick_files_with_substring(
            ScoutingMC_2023C_all_files_list,
            subsample
        )
    
    for subsample in TT_subsamples_list:
        filelist["2023"]["TT"][subsample] = pick_files_with_substring(
            ScoutingMC_2023C_all_files_list,
            subsample
        )

        if subsample != "TTto4Q":
            filelist["2023BPix"]["TT"][subsample] = pick_files_with_substring(
                ScoutingMC_2023BPix_all_files_list,
                subsample
            )
        else:
            filelist["2023BPix"]["TT"]["TTto4Q"] = pick_files_with_substring(
                ScoutingMC_2023C_all_files_list,
                subsample
            )

    for run in ScoutingData2023BPix_runs_list:
        filelist["2023BPix"]["Data"][run] = pick_files_with_substring(
            ScoutingData2023D_all_files_list, 
            run
        )

    for run in ScoutingData2023_runs_list:
        filelist["2023"]["Data"][run] = pick_files_with_substring(
            ScoutingData2023C_all_files_list, 
            run
        )

    # for run in ScoutingData2024_runs_list:
    #     filelist["2024"]["Data"][run] = pick_files_with_substring(
    #         ScoutingData2024_all_files_list,
    #         run
    #     )

    

    with open("nanoindex_v15_scouting.json", "w") as f:
        json.dump(filelist, f, indent=4)
    print("Copy the output file into the ../ directory")
