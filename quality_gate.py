import requests
import os
from tabulate import tabulate


class QualityGateCheck:
    """Performs a quality check based on error and warning thresholds."""

    def __init__(self, error_threshold, warning_threshold):
        """Initializes the check with thresholds."""
        self.error_threshold = (
            error_threshold  # The number of errors at or above which the check fails.
        )
        self.warning_threshold = warning_threshold  # The number of errors above which the check passes with warnings.
        self.status = "Pending"
        self.check_type = "Code Error Threshold Check"

    def get_status(self):
        """Returns the current status."""
        return self.status

    def describe_check(self):
        """Returns a description of the check."""
        return f"Checking for errors above {self.error_threshold} and warnings above {self.warning_threshold}."

    def process_code_errors(self, code_errors):
        """Processes errors against thresholds."""
        if code_errors >= self.error_threshold:
            return "Check failed: Exceeds error threshold"
        elif code_errors > self.warning_threshold:
            return "Check passed with errors"
        else:
            return "Check passed"


def validate_code_errors(code_errors):
    """Validates the input for code errors."""
    if not code_errors:
        return "No code errors provided"
    if not isinstance(code_errors, int):
        return "Invalid code errors: Expected an integer."
    return None  # Input is valid


def report_quality_gate_status(gate_status, check_type, check_description):
    """Reports the status to an external service."""
    api_token = os.environ.get(
        "REPORTING_API_TOKEN"
    )  # API token for reporting retrieved from environment.
    if not api_token:
        print(
            "Warning: REPORTING_API_TOKEN environment variable not set (reporting skipped)."
        )
        return
    headers = {"Authorization": f"Bearer {api_token}"}
    data = {
        "status": gate_status,
        "check_type": check_type,
        "check_description": check_description,
    }
    try:
        response = requests.post(
            "http://localhost:8081/api/status", headers=headers, json=data
        )
        response.raise_for_status()  # Ensure successful request.
        final_ouput = [response.json()["message"], tabulate(response.json()["data"])]
        for output in final_ouput:
            print(output)
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

    final_status = gate.process_code_errors(errors)
    gate.status = final_status

    report_quality_gate_status(
        gate.get_status(), gate.check_type, gate.describe_check()
    )
    return gate.get_status()


if __name__ == "__main__":

    print(
        "\nRunning quality checks against the local mock server (make sure it's running separately):"
    )

    code_errors = [15, 3, None, "five"]

    for code_error in code_errors:
        result = main_quality_check(code_error)
        print(f"Main check result with code errors {code_error}: {result}")
