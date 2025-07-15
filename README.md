#  FinOps Scripting Lab

This project demonstrates hands-on FinOps practices using Python and Bash scripting to automate AWS cost visibility and tagging governance. It’s designed to showcase scripting proficiency, cloud cost management, and Infrastructure-as-Code best practices.

---

##  Objectives

- Enforce AWS **tagging compliance** for EC2 resources
-  Estimate EC2 **monthly costs** using the AWS Pricing API
-  Send cost reports via **email** (configurable)


---

## Project Structure

```
finops-scripting-lab/
├── config/
│ └── required_tags.json # Required tag keys (e.g., CostCenter, Owner)
├── reports/ # Output CSV reports
├── scripts/
│ ├── check_tagging_compliance.py # Tagging enforcement script
│ ├── estimate_ec2_costs.py # EC2 cost estimation
│ ├── notify.sh # Optional notification via Slack/email
│ └── send_email.py # Optional Gmail-based notification
├── .gitignore
├── requirements.txt
└── README.md

```

---

## Prerequisites:

Install boto3

Configure AWS credentials (aws configure)

Define required tags in a config file

---

##  Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/vimmuyengwa/finops-scripting-lab.git
cd finops-scripting-lab
```

## 2. Set Up Your Environment

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Configure AWS credentials:
```bash
aws configure
```

Update the required tags list in config/required_tags.json:

```bash
{
  "required_tags": ["Owner", "CostCenter", "Environment"]
}
```

### 1. Tagging Compliance Checker (`check_tagging_compliance.py`)

- Scans all EC2 instances in the configured AWS region
- Reads required tag keys from `config/required_tags.json`
- Identifies resources that are missing any required tags
- Outputs a detailed CSV report in the `reports/` directory

### 2. EC2 Cost Estimator (estimate_ec2_costs.py)

Uses the AWS Pricing API to fetch current hourly prices
Calculates estimated monthly cost per instance based on 730 hours/month
Supports multiple instance types and AWS regions (mapped to pricing terms)
Saves the cost summary to a CSV file for reporting and audits


---

## How to Run
Tag Compliance Checker
```bash
python3 scripts/check_tagging_compliance.py
```

Generates:
```bash
reports/tagging_compliance_<timestamp>.csv
```

EC2 Cost Estimator
```bash
python3 scripts/estimate_ec2_costs.py
```

Generates:
```bash
reports/ec2_cost_estimate_<timestamp>.csv
```

Email:
```bash
python3 scripts/send_email.py
```

Author
Vimbai Muyengwa
Cloud FinOps | AWS | Python | Carnegie Mellon University
