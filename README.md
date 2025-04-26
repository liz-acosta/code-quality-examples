# To run this example code

1. Generate virtual environment: `virtualenv venv`
2. Activate virtual environment: `source venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`
4. Start local server: `python mock_reporting_server.py` (leave this terminal window open and running)
5. Open new terminal window and `cd` to project directory
6. Activate virtual environment: `source venv/bin/activate`
7. Run the script: `python quality_gate.py` or `python bad_quality_gate.py`

The output of either script should look like this:
```
Running quality checks against the local mock server (make sure it's running separately):
Status 'Check failed: Exceeds error threshold' for 'Combined Threshold Check' reported successfully.
Main Check Result (15 errors): Check failed: Exceeds error threshold
Status 'Check passed' for 'Combined Threshold Check' reported successfully.
Main Check Result (3 errors): Check passed
Main Check Result (No errors): No code errors provided
```