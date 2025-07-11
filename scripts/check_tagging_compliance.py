
import boto3
import json
import csv
import os
from datetime import datetime

# === Load required tags ===
CONFIG_PATH = "config/required_tags.json"
with open(CONFIG_PATH) as f:
    config = json.load(f)
REQUIRED_TAGS = config["required_tags"]


# === Set up AWS clients ===
ec2 = boto3.client("ec2")

# === Get all EC2 instances ===
def get_all_instances():
    instances = []
    paginator = ec2.get_paginator("describe_instances")
    for page in paginator.paginate():
        for reservation in page["Reservations"]:
            for instance in reservation["Instances"]:
                instances.append(instance)
        return instances

# === Check for missing tags ===
# === Check for missing tags ===
def get_missing_tags(instance):
    found_tags = {tag["Key"]: tag["Value"] for tag in instance.get("Tags", [])}
    missing = []
    for tag in REQUIRED_TAGS:
        if tag not in found_tags:
            missing.append(tag)
    return missing

# === Write results to CSV ===
def write_csv_report(data, filename):
    os.makedirs("reports/", exist_ok=True)
    with open(f"reports/{filename}", "w", newline="") as csvfile:
        fieldnames = ["InstanceId", "InstanceType", "Region", "MissingTags"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# === Main Script Logic ===
def main():
    print("Checking EC2 instances for tagging compliance...")
    instances = get_all_instances()
    non_compliant = []

    for instance in instances:
        missing = get_missing_tags(instance)
        if missing:
            non_compliant.append({
                "InstanceId": instance["InstanceId"],
                "InstanceType": instance["InstanceType"],
                "Region": ec2.meta.region_name,
                "MissingTags": ", ".join(missing)
            })

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"tagging_compliance_{timestamp}.csv"
    write_csv_report(non_compliant, filename)

    print(f" Report saved to reports/{filename}")
    if non_compliant:
        print(f"Found {len(non_compliant)} non-compliant instances.")
    else:
        print("All instances are compliant!")


if __name__ == "__main__":
    main()

