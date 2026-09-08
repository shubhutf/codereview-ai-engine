import json

def save_report_json(report, filename="pr_report.json"):

    with open(filename, "w") as f:
        json.dump(report, f, indent=4)

    print(f"Report saved to {filename}")