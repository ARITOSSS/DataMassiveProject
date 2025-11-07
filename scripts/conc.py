import subprocess
import csv
import re

# Paramètres
url = "https://tp1-massive-data.ew.r.appspot.com/api/timeline?user=user1"
concurrences = [1, 10, 20, 50, 100, 1000]
runs = 3
csv_file = "conc.csv"

# Préparer le CSV
with open(csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["PARAM","AVG_TIME","RUN","FAILED"])

    for c in concurrences:
        for r in range(1, runs+1):
            print(f"Running: concurrency={c}, run={r}")
            try:
                result = subprocess.run(
                    ["ab", "-n", "100", "-c", str(c), url],
                    capture_output=True, text=True, check=True
                )
                match = re.search(r"Time per request:\s+([\d\.]+) \[ms\]", result.stdout)
                avg_time = float(match.group(1)) if match else -1
                failed = 0
            except subprocess.CalledProcessError:
                avg_time = -1
                failed = 1

            writer.writerow([c, f"{avg_time}ms", r, failed])