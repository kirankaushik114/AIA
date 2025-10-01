# Robot Framework Project


This project contains sample Robot Framework tests plus CI configuration to run hourly and email results.


## Local run


1. Create a virtualenv: `python -m venv .venv && source .venv/bin/activate`
2. Install: `pip install -r requirements.txt`
3. Run tests: `./scripts/run_tests.sh`


## CI / GitHub Actions


The workflow `.github/workflows/ci.yml` will run every hour (see cron). Configure these repository secrets:
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASS`
- `EMAIL_TO`
- `EMAIL_FROM` (optional; defaults to SMTP_USER)


Push to GitHub and the schedule will run hourly.