#!/bin/bash

# === CONFIG ===
REPORT_DIR="reports"
REPORT_FILE=$(ls -t $REPORT_DIR/ec2_cost_estimate_*.csv | head -n 1)
RECIPIENT="vmuyengw@gmail.com"

# === CHECK FILE EXISTS ===
if [ ! -f "$REPORT_FILE" ]; then
  echo " No report file found!"
  exit 1
fi

# === SEND EMAIL ===
echo "Attached is the latest EC2 Cost Estimate Report: $(basename "$REPORT_FILE")" | \
mail -s " New EC2 Cost Estimate Report" -a "$REPORT_FILE" "$RECIPIENT"

echo " Email sent to $RECIPIENT for $REPORT_FILE"

