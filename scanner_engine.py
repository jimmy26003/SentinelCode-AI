import subprocess
import json
import os

def run_security_scan(file_path):
    try:
        # Running Bandit security linter
        result = subprocess.run(
            ['py', '-m', 'bandit', '-r', file_path, '-f', 'json', '-q'],
            capture_output=True,
            text=True
        )
        
        if not result.stdout.strip():
            return {"results": []}
            
        return json.loads(result.stdout)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Create a dummy file for testing
    sample_code = "import os\nos.system('rm -rf /')"
    with open("test_sample.py", "w") as f:
        f.write(sample_code)

    print("--- Starting Scan ---")
    report = run_security_scan("test_sample.py")
    
    if "results" in report:
        print(f"Found {len(report['results'])} security issues.")
        for issue in report['results']:
            print(f"Issue: {issue['issue_text']} at line {issue['line_number']}")