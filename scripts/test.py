import subprocess
import re

url = "https://tp1-massive-data.ew.r.appspot.com/api/timeline?user=user5"
runs = 3

for r in range(1, runs+1):
    print(f"Run {r}:")
    try:
        # Lancement de Apache Bench
        result = subprocess.run(
            ["ab", "-n", "100", "-c", "50", "-k", url],
            capture_output=True, text=True, check=True
        )
        # Extraction du "Time per request" moyen
        match = re.search(r"Time per request:\s+([\d\.]+) \[ms\]", result.stdout)
        if match:
            avg_time = float(match.group(1))
            print(f"Average time per request: {avg_time} ms")
        else:
            print("Error: could not parse time")
    except subprocess.CalledProcessError:
        print("Error: command failed")
