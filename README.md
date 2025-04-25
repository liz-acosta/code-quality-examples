# To run this example code

1. Generate virtual environment: `virtualenv venv`
2. Activate virtual environment: `source venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`
4. Start local server: `python mock_reporting_server.py` (leave this terminal window open and running)
5. Open new terminal window and `cd` to project directory
6. Activate virtual environment: `source venv/bin/activate`
7. Run the script: `python quality_gate.py` or `python bad_quality_gate.py`