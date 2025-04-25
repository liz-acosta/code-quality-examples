import requests
import os

class QualityGateCheck:
    """Performs a quality check based on error and warning thresholds."""
    def __init__(self, error_threshold, warning_threshold):
        """Initializes the check with thresholds."""
        self.error_threshold = error_threshold  # The number of errors at or above which the check fails.
        self.warning_threshold = warning_threshold  # The number of errors above which the check passes with warnings.
        self.status = "Pending"
        self.check_type = "Code Error Threshold Check"

    def get_status(self):
        """Returns the current status."""
        return self.status

    def describe_check(self):
        """Returns a description of the check."""
        return f"Checking for errors above {self.error_threshold} and warnings above {self.warning_threshold}."

def validate_code_errors(code_errors):
    """Validates the input for code errors."""
    if not code_errors:
        return "No code errors provided"
    if not isinstance(code_errors, int):
        return "Invalid code errors: Expected an integer."
    return None  # Input is valid

def process_code_errors(code_errors, error_threshold, warning_threshold):
    """Processes errors against thresholds."""
    if code_errors >= error_threshold:
        return "Check failed: Exceeds error threshold"
    elif code_errors > warning_threshold:
        return "Check passed with errors"
    else:
        return "Check passed"

def report_quality_gate_status(gate_status, check_type):
    """Reports the status to an external service."""
    api_token = os.environ.get("REPORTING_API_TOKEN")  # API token for reporting.
    if not api_token:
        print("Warning: REPORTING_API_TOKEN environment variable not set (reporting skipped).")
        return
    headers = {"Authorization": f"Bearer {api_token}"}
    data = {"status": gate_status, "check_type": check_type}
    try:
        response = requests.post("http://localhost:8081/api/status", headers=headers, json=data)
        response.raise_for_status()  # Ensure successful request.
        print(f"Status '{gate_status}' for '{check_type}' reported successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error reporting status: {e}")

def main_quality_check(errors):
    """Orchestrates the quality check process."""
    error_threshold = 10
    warning_threshold = 5
    gate = QualityGateCheck(error_threshold, warning_threshold)

    validation_result = validate_code_errors(errors)
    if validation_result:
        return validation_result

    final_status = process_code_errors(errors, gate.error_threshold, gate.warning_threshold)
    gate.status = final_status

    report_quality_gate_status(gate.get_status(), gate.check_type)
    return gate.get_status()

if __name__ == "__main__":
    # Set a dummy API token
    os.environ['REPORTING_API_TOKEN'] = 'fake_token_for_testing'


    print("\nRunning quality checks against the local mock server (make sure it's running separately):")
    result1 = main_quality_check(15)
    print(f"Main Check Result (15 errors): {result1}")

    result2 = main_quality_check(3)
    print(f"Main Check Result (3 errors): {result2}")

    result3 = main_quality_check(None)
    print(f"Main Check Result (No errors): {result3}")