#!/usr/bin/env bash
# Everything that runs without a model. No dependencies beyond python3.
#
#   ./evals/run.sh                      static checks + offline trip-wires
#   ./evals/run.sh --base-ref origin/main   ... plus the version-bump check
#
# The live trip-wires are opt-in and cost tokens:
#   python3 evals/tripwires.py --mode live --runs 3
#   python3 evals/interview_tripwires.py --mode live --runs 3
set -uo pipefail
cd "$(dirname "$0")/.."

status=0
python3 evals/static_checks.py "$@" || status=1
echo
python3 evals/tripwires.py || status=1
echo
python3 evals/interview_tripwires.py || status=1
echo
python3 evals/application_checks.py || status=1

echo
if [ $status -eq 0 ]; then
  echo "evals: PASS"
else
  echo "evals: FAIL"
fi
exit $status
