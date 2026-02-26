# usage: source switch_template_to_fit_environment.sh
micromamba deactivate
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../../" && pwd)"
cd "$PROJECT_ROOT/CMSSW_14_1_0_pre4/src"
cmsenv
cd -
