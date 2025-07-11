import boto3
import csv
import os
from datetime import datetime

# Constants
HOURS_IN_MONTH = 730  # Average number of hours in a month

# Setup clients
ec2 = boto3.client('ec2')
pricing = boto3.client('pricing', region_name='us-east-1')  # Pricing API is only available in us-east-1

def get_ec2_instances():
    instances = []
    paginator = ec2.get_paginator("describe_instances")
    for page in paginator.paginate():
        for reservation in page["Reservations"]:
            for instance in reservation["Instances"]:
                instances.append(instance)
    return instances

def get_price(instance_type, region):
    # AWS region name to pricing API location mapping
    region_mapping = {
        "us-east-1": "US East (N. Virginia)",
        "us-west-2": "US West (Oregon)",
        "us-east-2": "US East (Ohio)",
        "eu-west-1": "EU (Ireland)"
        # Add more if needed
    }

    location = region_mapping.get(region)
    if not location:
        print(f" Region {region} not supported for pricing lookup.")
        return None

    try:
        response = pricing.get_products(
            ServiceCode='AmazonEC2',
            Filters=[
                {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
                {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': location},
                {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': 'Linux'},
                {'Type': 'TERM_MATCH', 'Field': 'preInstalledSw', 'Value': 'NA'},
                {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': 'Shared'},
                {'Type': 'TERM_MATCH', 'Field': 'capacitystatus', 'Value': 'Used'}
            ],
            MaxResults=1
        )

        price_item = response['PriceList'][0]
        price_details = eval(price_item)
        on_demand = list(price_details['terms']['OnDemand'].values())[0]
        price_per_hour = list(on_demand['priceDimensions'].values())[0]['pricePerUnit']['USD']
        return float(price_per_hour)
    except Exception as e:
        print(f"️ Could not fetch price for {instance_type} in {region}: {str(e)}")
        return None

def write_cost_report(data, filename):
    os.makedirs("reports", exist_ok=True)
    with open(f"reports/{filename}", "w", newline="") as csvfile:
        fieldnames = ["InstanceId", "InstanceType", "Region", "HourlyCostUSD", "EstimatedMonthlyCostUSD"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    print(" Estimating EC2 instance costs...")
    instances = get_ec2_instances()
    cost_data = []

    for instance in instances:
        instance_id = instance["InstanceId"]
        instance_type = instance["InstanceType"]
        region = ec2.meta.region_name

        price_per_hour = get_price(instance_type, region)
        if price_per_hour is not None:
            monthly_cost = price_per_hour * HOURS_IN_MONTH
            cost_data.append({
                "InstanceId": instance_id,
                "InstanceType": instance_type,
                "Region": region,
                "HourlyCostUSD": round(price_per_hour, 4),
                "EstimatedMonthlyCostUSD": round(monthly_cost, 2)
            })

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"ec2_cost_estimate_{timestamp}.csv"
    write_cost_report(cost_data, filename)

    print(f" Cost report saved to reports/{filename}")

if __name__ == "__main__":
    main()
