# What this repo is for

This repo aims to provide examples of what good code looks like vs. bad code. While both scripts contained in this repo _will_ run, one script is easier to understand and therefore easier to maintain and debug. One way to see this demonstrated is to try writing unit tests for them.

# This repo contains
This repo contains everything needed to run the scripts. The primary files of concern are:
```
code-quality-examples
├─── bad_quality_gate.py # Example of bad code.
├─── quality_gate.py # Example of good code.
└─── mock_reporting_server.py # Code to run a mock server locally.
```

# What this code does

The scripts `quality_gate.py` and `bad_quality_gate.py` execute an example quality gate check, the results of which are posted to a status endpoint. While the code doesn't _actually_ do anything, it embodies common programming patterns. 

# To run this example code

## Set up the environment

1. Start local server: `python3 mock_reporting_server.py` (leave this terminal window open and running)
2. Open new terminal window and `cd` to project directory
3. Generate virtual environment: `virtualenv venv`
4. Activate virtual environment: `source venv/bin/activate`
5. Install requirements: `pip install -r requirements.txt`

## Run the script

**Running the bad code**
1. Run the script: `python bad_quality_gate.py`

**Running the good code**
1. Add the API token to the environment variables: `export REPORTING_API_TOKEN=fake_token_for_testing`
1. Run the script: `python quality_gate.py` or `python bad_quality_gate.py`

**The output of either script should look like this**
```
Running quality checks against the local mock server (make sure it's running separately):
Status received successfully
------------------  --------------------------------------------------
Check type:         Combined Threshold Check
Check description:  Checking for errors above 10 and warnings above 5.
Status              Check failed: Exceeds error threshold
------------------  --------------------------------------------------
Main check result with code errors 15: Check failed: Exceeds error threshold
```