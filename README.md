#  FinOps Scripting Lab

This project demonstrates hands-on FinOps practices using Python and Bash scripting to automate AWS cost visibility and tagging governance. It’s designed to showcase scripting proficiency, cloud cost management, and Infrastructure-as-Code best practices.

---

##  Objectives

- Enforce AWS **tagging compliance** for EC2 resources
-  Estimate EC2 **monthly costs** using the AWS Pricing API
-  Send cost reports via **Slack or email** (configurable)
-  *(Optional)* Clean up or auto-tag uncompliant resources

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

2. Set Up Your Environment

Install Python dependencies:

``
pip install -r requirements.txt
```

Configure AWS credentials:
aws configure
Update the required tags list in config/required_tags.json:

```

{
  "required_tags": ["Owner", "CostCenter", "Environment"]
}
```


How to Use

Check Tagging Compliance
```
python3 scripts/check_tagging_compliance.py
Outputs: reports/tagging_compliance_<timestamp>.csv
```

Estimate EC2 Costs

`
python3 scripts/estimate_ec2_costs.py
Outputs: reports/ec2_cost_estimate_<timestamp>.csv

Send Report Notification (Optional)
Option A: Slack
Edit scripts/notify.sh and add your Slack webhook URL, then run:

```bash
scripts/notify.sh
```

Option B: Email via Python + Gmail
Make sure to use an App Password, not your Gmail login

python3 scripts/send_email.py

Key Concepts Demonstrated

Python automation with boto3

EC2 pricing via AWS Pricing API

Tag compliance enforcement logic

CSV generation and reporting

Bash scripting for alerting

FinOps and cloud cost governance

Security & Git Best Practices

Do not hard-code secrets (use .env or app passwords)

Add .env, credentials, and reports/ to .gitignore

Use IAM least privilege policies (e.g., pricing:GetProducts, ec2:DescribeInstances)

Author
Vimbai Muyengwa
Cloud FinOps | AWS | Python | Carnegie Mellon University
