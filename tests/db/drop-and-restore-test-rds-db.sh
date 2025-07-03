#!/bin/bash

# This script is intended for use on AWS Texas non-prod environment.
# To run this script, first sign in to AWS Console and export your AWS access keys or configure AWS credentials using `aws configure`.
export AWS_REGION="eu-west-2"

db_instance_identifier="bcss-oracle-bcss-bcss-18000"
db_snapshot_identifier="bcss-18000-snapshot-with-notify-messaging-test-data-arthur"
option_group_name="bcss-oracle-bcss-dev-option-grp"
db_instance_class="db.t3.small"
db_subnet_group_name="bcss-oracle-bcss-cloud-subnet-grp"
db_parameter_group_name="default.oracle-se2-19"
vpc_security_group_id="sg-09164a04f68c35f26"

db_instance_status="$(aws rds describe-db-instances --db-instance-identifier $db_instance_identifier --query 'DBInstances[0].DBInstanceStatus' --output text)"

if [ "$db_instance_status" = "available" ] || [ "$db_instance_status" = "stopped" ]; then
    # Delete existing database
    echo "Deleting existing RDS DB instance bcss-oracle-bcss-bcss-18000..."
    aws rds delete-db-instance \
        --db-instance-identifier $db_instance_identifier \
        --skip-final-snapshot \
        --delete-automated-backups > /dev/null

    while [ "$(aws rds describe-db-instances --db-instance-identifier $db_instance_identifier --query 'DBInstances[0].DBInstanceStatus' --output text)" == "deleting" ]; do
        echo "Waiting for DB instance to be deleted..."
        sleep 10
    done

    echo "DB instance bcss-oracle-bcss-bcss-18000 deleted successfully."
fi

echo "Restoring snapshot $db_snapshot_identifier to database $db_instance_identifier..."
# Restore snapshot
aws rds restore-db-instance-from-db-snapshot \
    --db-instance-identifier $db_instance_identifier \
    --db-snapshot-identifier $db_snapshot_identifier \
    --option-group-name $option_group_name \
    --vpc-security-group-ids $vpc_security_group_id \
    --db-instance-class $db_instance_class \
    --db-subnet-group-name $db_subnet_group_name \
    --db-parameter-group-name $db_parameter_group_name \
    --db-subnet-group-name $db_subnet_group_name > /dev/null

while [ "$(aws rds describe-db-instances --db-instance-identifier $db_instance_identifier --query 'DBInstances[0].DBInstanceStatus' --output text)" != "available" ]; do
    echo "Waiting for DB instance to be available..."
    sleep 10
done

echo "DB instance $db_instance_identifier restored successfully from snapshot."
