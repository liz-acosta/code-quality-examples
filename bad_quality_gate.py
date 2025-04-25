import requests
import os

class QualityGateCheck:
    def __init__(self, error_threshold, warning_threshold):
        self.error_threshold = error_threshold
        self.warning_threshold = warning_threshold
        self.status = "Pending" 
        self.check_type = "Combined Threshold Check" 

    def run_check(self, code_errors):
        self.status = "Pending"
        if code_errors >= self.error_threshold:
            self.status = "Failed: Exceeds error threshold"
            result = self.status
            return result
        elif code_errors > self.warning_threshold:
            self.status = "Passed with errors"
            output = self.status
            return output
        else:
            self.status = "Passed"
            final_status = self.status
            return final_status
        return final_status

    def get_status(self):
        current_status = self.status 
        return current_status

    def describe_check(self): 
        description = f"Checking for errors above {self.error_threshold} and warnings above {self.warning_threshold}."
        return description

def report_quality_gate_status(gate_status, check_type):
    api_token = "A_HARDCODED_TOKEN_1234"
    headers = {"Authorization": f"Bearer {api_token}"}
    data = {"status": gate_status, "check_type": check_type}
    try:
        requests.post("http://localhost:8081/api/status", headers=headers, json=data)
        print("Status reported successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error reporting status: {e}")


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
        gate.status = final_status  # Update the gate's status

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

