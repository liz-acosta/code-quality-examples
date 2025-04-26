import requests
import os

# An example of redundant code and redundant comments.
# Definition of the QualityGateCheck class.
class QualityGateCheck:
     # Constructor for the QualityGateCheck class. It initializes the error and warning thresholds, the initial status, and the check type.
    def __init__(self, error_threshold, warning_threshold):
        # Store the error threshold provided during initialization. This threshold determines when the check fails.
        self.error_threshold = error_threshold
         # Store the warning threshold provided during initialization. This threshold determines when the check passes with errors.
        self.warning_threshold = warning_threshold
        # Initialize the status of the quality gate to 'Pending'. This will be updated after the check is run.
        self.status = "Pending" 
        # Define the type of check this instance performs.
        self.check_type = "Combined Threshold Check" 

    # Function to process the 'code_errors' against the defined thresholds.
    def run_check(self, code_errors):
        self.status = "Pending"
         # Check if the number of 'code_errors' is greater than or equal to the 'error_threshold'. If it is, return a 'failed' status message.
        if code_errors >= self.error_threshold:
            self.status = "Failed: Exceeds error threshold"
            result = self.status
            return result
        # Otherwise, check if the number of 'code_errors' is greater than the 'warning_threshold'. If it is, return a 'passed with errors' status message.
        elif code_errors > self.warning_threshold:
            self.status = "Passed with errors"
            output = self.status
            return output
        # If neither of the above conditions is met, it means the number of errors is within the acceptable range, so return a 'passed' status message.
        else:
            self.status = "Passed"
            final_status = self.status
            return final_status
        return final_status

     # Method to retrieve the current status of the quality gate.
    def get_status(self):
        current_status = self.status 
        # Return the current status. This could be 'Pending', 'Passed', 'Passed with errors', or 'Failed: Exceeds error threshold'.
        return current_status

    # Method to describe the check.
    def describe_check(self): 
        description = f"Checking for errors above {self.error_threshold} and warnings above {self.warning_threshold}."
        # Return the description of the check.
        return description

REPORTING_API_TOKEN = "A_HARDCODED_TOKEN_1234" # A hardcoded secret.

def report_quality_gate_status(gate_status, check_type):    
    headers = {"Authorization": f"Bearer {REPORTING_API_TOKEN}"}
    data = {"status": gate_status, "check_type": check_type}
    try:
        requests.post("http://localhost:8081/api/status", headers=headers, json=data)
        print("Status reported successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error reporting status: {e}")


# This does not make use of the QualityGateCheck class, instead it performs all of the tasks in one function.
def main_quality_check(errors):
    error_threshold = 10
    warning_threshold =  5
    gate = QualityGateCheck(error_threshold, warning_threshold)
    final_status = None

    if not errors:
        final_status = "No code errors provided"
    elif not isinstance(errors, int):
        final_status = "Invalid code errors"
    else:
        if errors >= gate.error_threshold:
            final_status = "Check failed: Exceeds error threshold"
        elif errors > gate.warning_threshold:
            final_status = "Check passed with errors"
        else:
            final_status = "Check passed"
        gate.status = final_status  # Update the gate's status.

        api_token = "A_HARDCODED_TOKEN_1234"
        if not api_token:
            print("Warning: REPORTING_API_TOKEN environment variable not set (reporting skipped).")
        else:
            headers = {"Authorization": f"Bearer {api_token}"}
            data = {"status": gate.get_status(), "check_type": gate.check_type}
            try:
                response = requests.post("http://localhost:8081/api/status", headers=headers, json=data)
                print(f"Status '{gate.get_status()}' for '{gate.check_type}' reported successfully.")
            except requests.exceptions.RequestException as e:
                print(f"Error reporting status: {e}")
    return final_status

if __name__ == "__main__":

    print("\nRunning quality checks against the local mock server (make sure it's running separately):")
    result1 = main_quality_check(15)
    print(f"Main Check Result (15 errors): {result1}")

    result2 = main_quality_check(3)
    print(f"Main Check Result (3 errors): {result2}")

    result3 = main_quality_check(None)
    print(f"Main Check Result (No errors): {result3}")

