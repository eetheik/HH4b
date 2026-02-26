Set up the `hh4b` virtual environment as follows. Consider doing this in your `/afs/cern.ch/work/{first_letter_of_username}/{username}` directory where you have more space.

```bash
# Download the micromamba setup script (change if needed for your machine https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html)
# Install: (the micromamba directory can end up taking O(1-10GB) so make sure the directory you're using allows that quota)
"${SHELL}" <(curl -L micro.mamba.pm/install.sh)
# You may need to restart your shell (exec bash)
micromamba create -n hh4b python=3.10 -c conda-forge
micromamba activate hh4b
```

Once the environment is set up, you should clone the git repository, set up an editable installation, and install the required packages to your environment:

```bash
# Clone the repository
git clone --single-branch --branch zbb https://github.com/eetheik/HH4b.git
cd HH4b
# Perform an editable installation
pip install -e .
# install requirements
pip3 install -r requirements.txt
```

Now the environment is set up and you have the HH4b repository to work in. The general workflow starting from zero is as follows:
1. Skim your data and MC files via HTCondor
    - I usually ran this overnight. Sometimes not all files ran so I sometimes sent MC first (since it was a lot quicker) and then data. I suspect the data to be slower just because the files are larger $\mathcal{O}(2-3\,\text{GB})$ compared to $\mathcal{O}(10-100\,\text{MB})$
2. Generate templates
3. Generate datacards
4. Run fits

### Some comments on the above:
- Naturally one needs to have initiated their grid proxy before step 1. I had a small shell script for this (which I ran in the home directory):
```bash
    # file init_grid_proxy.sh
    # usage: source init_grid_proxy.sh
    voms-proxy-init --voms cms
    cp /tmp/x509up_u$(id -u) .
    export X509_USER_PROXY=$(pwd)/x509up_u$(id -u)
    echo $X509_USER_PROXY
```
- In the above it is important that one exports the grid proxy to the X509_USER_PROXY variable, since the submission script will search for it there.
- Skimming and template generation are done in the `hh4b` environment we created earlier
- Datacard generation and fits are done in `cmsenv` in `CMSSW_14_1_0_pre4` paired with `rhalphalib` and `COMBINE`. Separate instructions for this are given later in the README. Perhaps importantly make sure to do all of the datacard and fitting steps in a clean environment (I had some conflicting dependencies which led to very mysterious segfaults, so I cleaned all of my `~/.local/lib/python3.*` directories and my pip cache which fixed it)
- The skimming step on condor works roughly as follows (`src/HH4b/condor/submit.templ.sh`): inside the job, it clones the git repo and downloads the file(s) from the T2, as well as a singularity image file for the correct coffea version, then processes the file(s) using `src/run.py` and `src/HH4b/processors/bbbbSkimmer.py`, and saves the output (wherever you configured it, ideally in your EOS directory). For this reason, if you have uncommited changes to the git repo (namely in any of the skimmer dependencies) you may not see the same results locally as you see when skimming the files on condor. This is bit of a funny setup, as **every time you make changes to the cuts etc. you also have to commit them to the repo if you want to skim via condor.** This is despite the fact that on lxplus with condor, you are able to tell the job to run code present in your private directories. The reason for the funny setup is the singularity image file for coffea, because coffea isn't available on the node where you send your job to be run, and so it needs to be sent in every time. One is free to change this setup (i.e. remove the repo cloning, as it would likely speed up the jobs), but currently it seems the limiting factor for processing the jobs quickly is actually the data files (they have lots of events and they go very slow)
- Warning: There are a fair few intermediate places in the code where files will be created and stored somewhere. Every time you run some step, make sure you have edited the file output location correctly, and then at the next step, make sure the input location is read in correctly. This just means going inside the script you are about to run, and checking the filepaths make sense. Once you run the full code cycle once you will not have to fiddle with the paths much more, but on first run you will.

### Considerations before sending skimmer jobs the first time:
The output directory for skimmer jobs is defined directly by taking `username = $(USER)$` from the `$(USER)$` shell variable, and is by default set to `eos/user/{username[0]}/{username}/bbbb/{args.processor}/`. This is the standard for CERN users, when using `--save-site cern`, which is the default flag in the code currently. If you want to change the default output directory for the skimmer outputs, you must edit this inside `src/condor/submit.py`: https://github.com/eetheik/HH4b/blob/5edd6b02e518ff398a7c1746b12fdddadb572aa1/src/condor/submit.py#L74.

Additionally, one also needs to define the git repository which is cloned by the condor skimmer jobs. This is handled inside the submitted script: `submit.templ.jdl`, which receives the `git_user` argument from the `src/condor/submit.py` script. I have set the default to my github username, which you may like to modify: https://github.com/eetheik/HH4b/blob/5edd6b02e518ff398a7c1746b12fdddadb572aa1/src/condor/submit.py#L206. Alternatively, you can always pass in the `--git-user {git_username}` flag when submitting jobs, but you must do this every time.

Make sure you are sending the correct/desired files to be skimmed. See the section on _Filelist and submission config_, you'll probably want to comment sections in or out inside the submission config. Similarly, make sure you are implementing the desired cuts in `src/HH4b/processors/bbbbSkimmer.py`. It is beneficial to check that the cuts which you have implemented work correctly locally. See the section on running skimmer locally.

# Skimmer
The skimmer is implemented in the ```src/HH4b/processors/bbbbSkimmer.py``` file. It contains the logic for loading in a dataset, calls the functions for grabbing the correct objects (electrons, muons, jets, fatjets) and applying the relevant corrections/selections to these. It makes use of the following files:
- ```src/HH4b/processors/utils.py```: assorted utilities e.g. for adding selections (wrapped for coffea)
- ```src/HH4b/processors/objects.py```: this file contains the object definitions, such as what columns are loaded for fatjets in `get_ak8jets()` (and the damn mappings between the NANO names as well as the ones used in the calibration/analysis: I have kept this mapping since it made rewriting the later template etc. scripts easier), jet ID criteria in `jetid_v14()` etc . Implemented are also the loose scouting muon and electron requirements, but these are not used for cuts in the ```src/HH4b/processors/bbbbSkimmer.py``` script right now.
- ```SkimmerABC.py```: implements the Skimmer class. Perhaps of importance here is just the weighting/normalisation functions like `get_dataset_norm()`. If you run locally, then the `dataset` string needs to be defined via the `--dataset {dataset}` flag when calling the `run.py` script, otherwise you will not see normalisation / weighting applied. When you send skimmer jobs they are applied as expected, and it grabs the dataset name, e.g. `Zto2Q-HT800...` from the YAML file specifying what files are sent to be skimmed. The cross-sections are looked up from `src/HH4b/xsecs.py`. We verified with Zihan that the ones here, and the ones used by her and Beatriz are in agreement for 2024 (up to some $\sim\mathcal{O}(10^{-4})$ differences)
- ```src/HH4b/corrections.py```: this implements the various corrections (JECs, jet veto maps), as well as adding systematic weights (like pileup and parton shower weights)
    - Currently Winter23 and Winter24 HLT JECs are implemented. These are applied as 2023pre-BPix: Winter23, 2023 and 2024: Winter24. 
    - Appropriate jet veto maps are used, supporting 2024 also
    - Pileup reweighting is not released yet for 2024, but Zichun implemented his own

## Notes on the above:
- In the current implementation the scouting and offline $Z \to bb$ cuts are intended to be almost identical:
    1. At least two AK8 jets
    2. pT lead. AK8 > 300 (450) GeV for scouting (offline), with an optional cut of TXbb > 0.3 (currently commented out)
    3. pT subl. AK8 > 200 GeV
    4. delta phi(lead. AK8, subl. AK8) >= pi/2 (back to back jets)
    5. HT > 600 (1000) GeV for scouting (offline)
- The topveto has been commented out from both scouting and offline for consistency
    - When AK4 jet tagging works in scouting again, it can be reimplemented
- The lepton veto has been commented out from both scouting and offline
    - I tried the lepton veto out once, and it didn't seem to work. In retrospect, perhaps it was just due to files going missing when skimming. It was never readded, since we figured TTbar processes weren't that dominant (although arguably they contribute unnecessarily to the tail, especially in the fail region at high pT)
- MET filters are toggled off in both scouting and offline currently.
    - Scouting does not have MET filters, but something similar might be possible to implement. In the code, I have implemented type I MET corrections for scouting.
- The cut on |eta| < 2.4 is implemented when selecting all fatjets. The basic fatjet selection also requires that all AK8 jets have pT > 200 GeV.

## Skimmer job submission
For sending all files to be skimmed, you will likely find it easiest to use the ```src/condor/submit_from_yaml.py``` script. I usually call it (from the root of the HH4b directory) as:

```bash
python src/condor/submit_from_yaml.py --processor skimmer --save-root --region "zbb" --yaml "src/condor/submit_configs/skimmer_zbb_HT-scouting.yaml" --nano-version "v15_scouting" --git-branch "zbb" --allow-diff-local-repo --txbb glopart-scouting --submit --use-scouting --save-systematics --tag {DATE}
```

Notable flags for the script are:
1. `--use-scouting` which switches between using scouting variables and offline variables (also toggles the correct JEC, and is intended to toggle correct lepton vetos etc. if used).
2. `--save-root` which saves root files (usually just pickle and parquet files are saved)
3. `--save-systematics` does as it says
4. `--txbb` defines the AK8 jet tagger to be used. If you use `--no-use-scouting` then make sure that you use `--txbb glopart-v3`
    - One should also make sure that if they use `--use-scouting` or `--no-use-scouting` flags, that the `.yaml` file contains the correct data files.
5. `--processor` should be set to `skimmer`
6. `--nano-version` should be set to `v15_scouting`, this ensures you look up the correct filelist (`data/nanoindex_v15_scouting.json`)
    - I have included my script for generating the filelist under `data/eetu_filelist_gen/`. There is another implementation also available from the HH4b folk in `data/make_filelists.py` but this isn't up to date
7. `--region` should be set to `zbb`
8. `--git-branch` should be set to `zbb`
8. `--allow-diff-local-repo` is useful if you have changes locally which aren't present on github
9. `--tag {DATE}` I usually put the date as the tag. This dictates the name of the output directory
10. `--git-user` (optional) defines the username from who the git repo is cloned during skimmer job: `https://github.com/{git_user}/HH4b`
11. `--yaml` specifies the config YAML file

As it may be helpful to you, an example command to submit only QCD for the year 2023BPix would be:
```bash
python src/condor/submit.py --processor skimmer --save-root --region "zbb" --nano-version "v15_scouting" --git-branch "zbb" --allow-diff-local-repo --txbb glopart-scouting --samples QCD --year 2023BPix --submit --use-scouting --save-systematics --tag TAG
```

## Filelist and submission config
The filelist for scouting is defined in `data/nanoindex_v15_scouting.json`. The `src/condor/submit_from_yaml.py` submission script, paired with a `.yaml` config, together parse this filelist correctly, so that you end up with individual directories with the sample names in the end, and so that the `--samples` and `--subsamples` flags is set correctly for normalization etc. The up to date submission config for scouting files is `src/condor/submit_configs/skimmer_zbb_HT-scouting.yaml`. Note that it includes all MC and scouting data. Realistically, you usually do not want to process QCD, so I suggest commenting that out for both the years 2023 and 2023BPix. Additionally, included are also all the MC and data samples for 2024 (but commented out). If you want to process using `--no-use-scouting` for a scouting-offline comparison, I have included also a config file for that: `src/condor/submit_configs/skimmer_zbb_HT-offlinevars-scouting.yaml`, which is essentially equivalent to the scouting one, but with the scouting data switched for offline JetMET.

There also exists a config for the NLO Vjets samples, called `src/condor/submit_configs/skimmer_zbb_PT-scouting.yaml`. There was some bug with the NLO samples, so this shouldn't be used, and hasn't been updated either so may be out of date.

### NOTE: Currently Scouting 2023BPix uses 2023 TTto4Q samples, since we never got the BPix samples. When these samples are finally available, it would be wise to change them out inside the filelist: `data/nanoindex_v15_scouting.json`.

## Skimming locally
The submission scripts in `/src/condor/` send the jobs, which all end up calling the `src/run.py/` script inside the jobs, which is essentially a wrapper for the skimmer script.

So to run locally, you just work with the `src/run.py` script, which may be worthwhile for you to briefly read through to understand the arguments and how it works. If you have some file locally, you can call the script (inside the `hh4b` environment) via 

```bash
python src/run.py --processor skimmer --region zbb --nano-version v15_scouting --use-scouting --txbb glopart-scouting --files {filepath} --year YEAR
``` 

One may alternatively want to process some file from the filelist locally (note that you will need to have your grid proxy activated, as it will fetch the file from the T2), in which case they can use the `--sample {sample}` and `--subsample {subsample}` flags in place of the `--files` flag. An example could be:

```bash
python src/run.py --processor skimmer --region zbb --nano-version v15_scouting --use-scouting --txbb glopart-scouting --sample QCD --subsample QCD_PT-600to800 --starti 0 --endi 1 --year 2023
``` 

Check the sample and subsample naming from the filelist or the submission config.

### Mass decorrelation
I produce the mass decorrelation TXbb quantile maps using the `src/HH4b/zbb/decorrelation/ScoutGloParT_decorrelation.py` script. 

The configuration of the script is done at the very top, where one can define the following:

```python
REPROCESS = True # Whether to reprocess the data. This is necessary when increasing the PT_LIMS, RHO_LIMS, making binning smaller etc. Notably one can change the quantiles (alphas) which are calculated without reprocessing

SKIMMER_DIR = "/eos/user/e/eheikkil/bbbb/skimmer" # Directory for skimmer outputs
YEARS = ["2023", "2023BPix"] # Years which are aggregated and used for producing the QCD quantile
TAG = "13Feb2026_Data_Standard_Cuts_QCD_Inclusive_v15_scouting_zbb" # Tag indicating directory inside skimmer directory which contains the skimmer outputs

OUTDIR = "/eos/user/e/eheikkil/MASS_DECORRELATION_EFFORTS/Smoothing/outputs" # Output directory
FILENAME = f"{OUTDIR}/second_bins_TXBBPRECUT0p3.pkl" # Filename for saving the QCD binning. If you set REPROCESS = False then this is loaded

ALPHAS = [0.95, 0.995] # quantiles to be used (alpha gives the fraction of QCD rejected)
extra_txbb_cut = 0.3 # an additional cut on QCD TXbb, before any alpha calculation. This is mainly here because my skimmed QCD was fully inclusive in TXbb, but my data had a cut on TXbb > 0.3, so I had to implement this into the QCD as well so that I decorrelated the same effective sample. Ideally this would be set to 0.0, and the data wouldnt have such a TXbb cut.

USE_SMOOTHING = True # Whether to smooth the quantile surface (uses Gaussian filter smoothing right now, one of the papers uses some nearest neighbors based smoothing which might be considered). In all honesty it might also work to just not use any smoothing
SMOOTH_SIGMA = (1.0, 1.0) # Standard deviation for Gaussian filter smoothing along (rho, pT)

# Binning
PT_LIMS  = (300, 1800)
RHO_LIMS = (-7.0, -1.0) # -2

N_PT   = 50 # Number of pT bins inside PT_LIMS
N_RHO  = 50 # Number of rho = ln(m^2/pT^2) bins inside RHO_LIMS
N_TXBB = 400 # Number of TXbb bins (from 0 to 1)
```

This is a minimally working script, it can (should) be cleaned up and edited. The smoothing is somewhat arbitrary. In its current state, when you run the script it will probably run for around 20ish minutes, if not longer. It's not very optimized (doesn't really need to be, you run it once for your desired working point alpha), but it also does the QCD efficiency map computation as well as plotting, which are both unnecessary for the fits. The main output from the script are `.pkl` files for the quantile surfaces (output file name and location defined at the very end in the main() function).

For the script, you should use QCD files which have undergone very minimal cuts. I skimmed the QCD files using just the following cuts:
1. pT leading AK8 jet > 300 GeV,
2. HT > 600 GeV,

and then worked with the skimmed QCD files. Read: You will comment out almost every cut inside the `src/HH4b/processors/bbbbSkimmer.py` script, commit this to the git repo, then inside the submit config you will only include the QCD samples and subsamples / use the `--sample QCD` flag, and submit jobs as usual.

If you are happy with the configuration in the script, you just run it (inside the `hh4b` environment) using
```bash
python ScoutGloParT_decorrelation.py
```

Included in the same directory (`src/HH4b/zbb/decorrelation/`) are also some plotting scripts which may be of use to you.

### Template generation
There are three separate template generation scripts, which really all do the same thing. However there are some caveats which I felt warranted writing three separate scripts rather than inflating one script with extra features.
1. `src/HH4b/zbb/decorrelated_scouting_templates.py`
    - This script has one very dangerous function, which is `apply_jmsr_smearing_in_templates()`, which retroactively applies JMS/R and creates the up and down variations just from the standard mass branch. Because the nominal value for JMR is set to 1.05, and JMS to 1.0, if you run the templates multiple times without reprocessing you are going to drift the nominal value away from what it should be by 5% each iteration. This function was useful to me, because I could check the effect of different initial guesses for JMS/R in the fits (no real effect) without re-running the skimmer, but one needs to be very aware of what they are doing with this function. For your safety, I have commented out the line that uses this function. The skimmer scripts should by default apply the JMS/R correctly.
    - Additionally, this script applies the tagger mass decorrelation. 
        - This is handled by the `load_qsurf()` function, which loads in the quantile surface `.pkl` file created in the quantile surface derivation using QCD MC above.
        - It then uses this quantile surface to create the decorrelated tagger score `TXbb_DDT0 = TXbb - quantile_map`, which one uses to define the pass region as `TXbb_DDT0 > 0` and `TXbb_DDT0 < 0` for the fail region. The decorrelated tagger score is saved to a new branch with the name `TXbb_DDT0`.
2. `src/HH4b/zbb/scouting_templates.py`
    - Implements the standard template generation, but using scouting variables, and ignoring all the trigger scale factors and PNet work necessary in the offline template generation. If you want to derive SFs without decorrelating the tagger, you use this script.
3. `src/HH4b/zbb/offline_templates.py`
    - Zichun's script for offline

Inside the template generation script you can specify the TXbb working points (in the mass decorrelated case this is just a dummy entry used by the filenames so that the processing doesn't have to be changed), as well as the pT bins. You must specify the used tag so that the data can be loaded from the correct place. The directory to which files is also specified. All configuration happens near the top of the file and is rather self-explanatory (filepaths, TXbb binning, pT binning, mass binning, and file containing quantile surface in case of decorrelated templates)

Note: In the case of the DDT-decorrelated tagger, you may wish to move the DDT transformation and cut from the template generation step to the skimmer step.

### Setting up the datacard and fitting environment for the first time
Inside the root of the HH4b directory (but not inside the `hh4b` mamba/micromamba environment), do the following
```bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsrel CMSSW_14_1_0_pre4
cd CMSSW_14_1_0_pre4/src
cmsenv
scram-venv
cmsenv
git clone -b v10.1.0 https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
git clone -b v3.0.0-pre1 https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
# Important: this scram has to be run from src dir
scramv1 b clean; scramv1 b
pip3 install --upgrade rhalphalib
```
If you run into mysterious crashes / segfaults during the datacard or fitting processes, this is likely due to mismatching dependencies. To fix it, delete everything that was downloaded in the above step, and clear `~/.local/lib/python3.*`, as well as your pip cache. Then you should rerun the above steps, and afterwards be able to cleanly run the datacards and fits.

In the future whenever you run datacards and fits, you need to use the `cmsenv` environment, which should be activated inside the `CMSSW_14_1_0_pre4/src` directory. If you placed `CMSSW_14_1_0_pre4` inside the HH4b root directory and you are using the `hh4b` micromamba environment, you can use the `switch_template_to_fit_environment.sh` script inside `src/HH4b/zbb/fits` to quickly switch to the correct environment after generating templates:
```bash
# usage: source switch_template_to_fit_environment.sh
micromamba deactivate
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../../" && pwd)"
cd "$PROJECT_ROOT/CMSSW_14_1_0_pre4/src" 
cmsenv
cd -
```

### Running datacards and fits
Before running the fits you must create the corresponding datacard which is consumed by the COMBINE fit. For this, there is the `datacard.sh` bash script, which specifies the standard arguments to call the `CreateDatacard.py` python script. Inside the `datacard.sh` script you only ever need to change the directory where the templates are located, `templates_dir`, as well as the order of the transfer factor `--nTF`.

If you change the working points or pT bining in the templates, you must also modify them inside the `CreateDatacard.py` script. This is done at the very top of the file with the WPS and PTS lists.

The datacards are by default output to the `src/HH4b/zbb/fits/cards/{YEAR}` directory.

The inclusion/exclusion of certain systematics can rather easily be done inside the `CreateDatacard.py` script by commenting them in or out, like
```python
    "PDF_gg": Syst(name = "ggPDF", prior="lnN", samples=["ttbar"], value=1.042), 
    # "QCD_scale_ttbar": Syst(
    #     name= r"QCD_scale_ttbar",
    #     prior="lnN",
    #     samples=["ttbar"],
    #     value=1.024,
    #     value_down=0.965,
    # ),
```

After creating the datacards, the fits can be run using the `fits.sh` bash script, which calls the `fit_zbb.sh` script with the appropriate arguments. Inside of the `fits.sh` script one needs to specify the used pT binning and working points, if these are changed.

If no changes are made, the workflow is simply
1. Activate cmsenv (inside the `CMSSW_14_1_0_pre4/src` directory)
2. Run `./datacard.sh` (inside the `src/HH4b/zbb/fits` directory)
3. Run `./fits.sh` (inside the `src/HH4b/zbb/fits` directory)

Cards as well as fit results (impacts, dNLL scans, root files etc.) are output to the `src/HH4b/zbb/fits/cards/{YEAR}/{passbin}` directory.

If you want to plot the fit results, you can call the `post_fit_plots.py` script. Use the same mass binning as in the template generation step, otherwise this will crash. Plots are output to the `src/HH4b/zbb/fits/postfit_plots` directory. 

