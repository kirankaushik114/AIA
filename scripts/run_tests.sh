#!/usr/bin/env bash
set -euo pipefail


# Create reports dir
mkdir -p reports


# Run Robot Framework with output files placed into reports/
robot --output reports/output.xml --log reports/log.html --report reports/report.html tests/


# Exit code from robot is propagated; CI will see test failure if non-zero