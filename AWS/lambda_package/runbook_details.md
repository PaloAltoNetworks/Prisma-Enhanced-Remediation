# Runbook Details

Click on a runbook to see the code as well as the IAM permissions required to run it.

## Table of Contents

- [CloudFormation Runbooks](#cloudformation-runbooks)
  - [Enable CloudFormation Stack termination protection](#enable-cloudformation-stack-termination-protection)
- [CloudTrail Runbooks](#cloudtrail-runbooks)
  - [AWS CloudTrail logs are not encrypted using Customer Master Keys (CMKs)](#aws-cloudtrail-logs-are-not-encrypted-using-customer-master-keys-cmks)
  - [CloudTrail trail is not integrated with CloudWatch Logs](#cloudtrail-trail-is-not-integrated-with-cloudwatch-logs)
  - [AWS CloudTrail log validation is not enabled in all regions](#aws-cloudtrail-log-validation-is-not-enabled-in-all-regions)
  - [AWS CloudTrail bucket is publicly accessible](#aws-cloudtrail-bucket-is-publicly-accessible)
- [Config Runbooks](#config-runbooks)
  - [AWS Config disabled](#aws-config-disabled)
- [EC2 Runbooks](#ec2-runbooks)
  - [EBS snapshot doesn't exist or older than 15 days](#ebs-snapshot-doesnt-exist-or-older-than-15-days)
  - [AWS Security Groups allow internet traffic to SSH port (22)](#aws-security-groups-allow-internet-traffic-to-ssh-port-22)
  - [AWS Security Groups allow internet traffic from internet to Telnet port (23)](#aws-security-groups-allow-internet-traffic-from-internet-to-telnet-port-23)
  - [AWS Security Groups allow internet traffic from internet to RDP port (3389)](#aws-security-groups-allow-internet-traffic-from-internet-to-rdp-port-3389)
  - [AWS Security Groups allow internet traffic from internet to MYSQL port (3306)](#aws-security-groups-allow-internet-traffic-from-internet-to-mysql-port-3306)
  - [AWS Security Groups allow internet traffic from internet to PostgreSQL port (5432)](#aws-security-groups-allow-internet-traffic-from-internet-to-postgresql-port-5432)
  - [AWS Security Groups allow internet traffic from internet to SQLServer port (1433)](#aws-security-groups-allow-internet-traffic-from-internet-to-sqlserver-port-1433)
  - [AWS Security Groups allow internet traffic from internet to MSQL port (4333)](#aws-security-groups-allow-internet-traffic-from-internet-to-msql-port-4333)
  - [AWS Security Groups allow internet traffic from internet to VNC Listener port (5500)](#aws-security-groups-allow-internet-traffic-from-internet-to-vnc-listener-port-5500)
  - [AWS Security Groups allow internet traffic from internet to VNC Server port (5900)](#aws-security-groups-allow-internet-traffic-from-internet-to-vnc-server-port-5900)
  - [AWS Security Groups allow internet traffic from internet to FTP port (21)](#aws-security-groups-allow-internet-traffic-from-internet-to-ftp-port-21)
  - [AWS Security Groups allow internet traffic from internet to FTP-Data port (20)](#aws-security-groups-allow-internet-traffic-from-internet-to-ftp-data-port-20)
  - [AWS Security Groups allow internet traffic from internet to SMTP port (25)](#aws-security-groups-allow-internet-traffic-from-internet-to-smtp-port-25)
  - [AWS Security Groups allow internet traffic from internet to DNS port (53)](#aws-security-groups-allow-internet-traffic-from-internet-to-dns-port-53)
  - [AWS delete unused EC2 Security Groups](#aws-delete-unused-ec2-security-groups)
  - [AWS Amazon Machine Image (AMI) is publicly accessible](#aws-amazon-machine-image-ami-is-publicly-accessible)
  - [AWS Default Security Group does not restrict all traffic](#aws-default-security-group-does-not-restrict-all-traffic)
  - [AWS Security Groups with Inbound rule overly permissive to All Traffic](#aws-security-groups-with-inbound-rule-overly-permissive-to-all-traffic)
  - [AWS EBS snapshots are accessible to public](#aws-ebs-snapshots-are-accessible-to-public)
- [ELB Runbooks](#elb-runbooks)
  - [AWS Elastic Load Balancer (Classic) with connection draining disabled](#aws-elastic-load-balancer-classic-with-connection-draining-disabled)
  - [AWS Elastic Load Balancer (Classic) with cross-zone load balancing disabled](#aws-elastic-load-balancer-classic-with-cross-zone-load-balancing-disabled)
  - [AWS Elastic Load Balancer (Classic) with access log disabled](#aws-elastic-load-balancer-classic-with-access-log-disabled)
  - [AWS Elastic Load Balancer v2 (ELBv2) Application Load Balancer (ALB) with access log disabled](#aws-elastic-load-balancer-v2-elbv2-application-load-balancer-alb-with-access-log-disabled)
- [IAM Runbooks](#iam-runbooks)
  - [Enforce AWS account best practices password policy](#enforce-aws-account-best-practices-password-policy)
  - [AWS access keys not used for more than 90 days](#aws-access-keys-not-used-for-more-than-90-days)
  - [AWS IAM policy allows full administrative privileges](#aws-iam-policy-allows-full-administrative-privileges)
  - [Create an IAM Support Role to manage incidents with AWS Support](#create-an-iam-support-role-to-manage-incidents-with-aws-support)
- [KMS Runbooks](#kms-runbooks)
  - [AWS Customer Master Key (CMK) rotation is not enabled](#aws-customer-master-key-cmk-rotation-is-not-enabled)
- [RDS Runbooks](#rds-runbooks)
  - [AWS RDS database instance is publicly accessible](#aws-rds-database-instance-is-publicly-accessible)
  - [AWS RDS snapshots are accessible to public](#aws-rds-snapshots-are-accessible-to-public)
  - [AWS RDS instance with Multi-Availability Zone disabled](#aws-rds-instance-with-multi-availability-zone-disabled)
  - [AWS RDS minor upgrades not enabled](#aws-rds-minor-upgrades-not-enabled)
- [Redshift Runbooks](#redshift-runbooks)
  - [AWS Redshift clusters should not be publicly accessible](#aws-redshift-clusters-should-not-be-publicly-accessible)
- [S3 Runbooks](#s3-runbooks)
  - [AWS S3 Object Versioning is disabled](#aws-s3-object-versioning-is-disabled)
  - [AWS S3 bucket has global view ACL permissions enabled](#aws-s3-bucket-has-global-view-acl-permissions-enabled)
  - [AWS Access logging not enabled on S3 buckets](#aws-access-logging-not-enabled-on-s3-buckets)
  - [AWS S3 buckets do not have server side encryption](#aws-s3-buckets-do-not-have-server-side-encryption)
  - [AWS S3 buckets are accessible to public](#aws-s3-buckets-are-accessible-to-public)
- [VPC Runbooks](#vpc-runbooks)
  - [Release unassociated (unused) Elastic IP addresses](#release-unassociated-unused-elastic-ip-addresses)
  - [AWS VPC has flow logs disabled](#aws-vpc-has-flow-logs-disabled)
  - [Delete AWS default VPC](#delete-aws-default-vpc)
- [Misc Runbooks](#misc-runbooks)
  - [Example Runbook](#example-runbook)

## CloudFormation Runbooks

### Enable CloudFormation Stack termination protection

- Script name: [`AWS-CFM-003.py`](runbooks/AWS-CFM-003.py)
- Prisma Cloud policy descriptor: N/A
- Runbook summary: Enables CloudFormation Stack termination protection.
- Required IAM permissions:
  - `cloudformation:DescribeStacks`
  - `cloudformation:UpdateTerminationProtection`
- CIS section: N/A
- Caveats: N/A

## CloudTrail Runbooks

### AWS CloudTrail logs are not encrypted using Customer Master Keys (CMKs)

- Script name: [`AWS-CLT-002.py`](runbooks/AWS-CLT-002.py)
- Prisma Cloud policy descriptor: `PC-AWS-CT-5`
- Runbook summary: Encrypts CloudTrail S3 logs with a KMS Customer Managed Key (CMK).
- Required IAM permissions:
  - `cloudtrail:DescribeTrails`
  - `cloudtrail:UpdateTrail`
  - `s3:GetBucketLocation`
  - `kms:CreateAlias`
  - `kms:CreateKey`
- CIS section: 2.7
- Caveats: N/A

### CloudTrail trail is not integrated with CloudWatch Logs

- Script name: [`AWS-CLT-004.py`](runbooks/AWS-CLT-004.py)
- Prisma Cloud policy descriptor: `PC-AWS-CT-50`
- Runbook summary: Integrates CloudTrail with CloudWatch Logs. Creates (if needed) the necessary IAM Policy and CloudWatch Logs group.
- Required IAM permissions:
  - `iam:CreateRole`
  - `iam:GetRole`
  - `iam:PutRolePolicy`
  - `logs:CreateLogGroup`
  - `logs:DescribeLogGroups`
  - `logs:PutRetentionPolicy`
  - `cloudtrail:UpdateTrail`
- CIS section: 2.4
- Caveats: N/A

### AWS CloudTrail log validation is not enabled in all regions

- Script name: [`AWS-CLT-005.py`](runbooks/AWS-CLT-005.py)
- Prisma Cloud policy descriptor: `PC-AWS-CT-4`
- Runbook summary: Enables CloudTrail log file validation.
- Required IAM permissions:
  - `cloudtrail:DescribeTrails`
  - `cloudtrail:UpdateTrail`
- CIS section: 2.2
- Caveats: N/A

### AWS CloudTrail bucket is publicly accessible

- Script name: [`AWS-CLT-006.py`](runbooks/AWS-CLT-006.py)
- Prisma Cloud policy descriptor: `PC-AWS-S3-1`
- Runbook summary: Removes CloudTrail S3 bucket ACL Public policy.
- Required IAM permissions:
  - `s3:GetBucketAcl`
  - `s3:PutBucketAcl`
- CIS section: 2.3
- Caveats: N/A

## Config Runbooks

### AWS Config disabled

- Script name: [`AWS-CONFIG-001.py`](runbooks/AWS-CONFIG-001.py)
- Prisma Cloud policy descriptor: N/A
- Runbook summary: Enables AWS Config. Creates (if needed) the necessary IAM Role and S3 bucket/policy.
- Required IAM permissions:
  - `iam:AttachRolePolicy`
  - `iam:CreateRole`
  - `iam:GetRole`
  - `s3:CreateBucket`
  - `s3:PutBucketPolicy`
  - `config:PutConfigurationRecorder`
  - `config:PutDeliveryChannel`
  - `config:StartConfigurationRecorder`
- CIS section: 2.5
- Caveats: N/A

## EC2 Runbooks

### EBS snapshot doesn't exist or older than 15 days

- Script name: [`AWS-EC2-001.py`](runbooks/AWS-EC2-001.py)
- Prisma Cloud policy descriptor: N/A
- Runbook summary: Creates an EBS snapshot if a snapshot doesn't exist, or is older than 15 days.
- Required IAM permissions:
  - `ec2:CreateSnapshot`
  - `ec2:DescribeSnapshots`
- CIS section: N/A
- Caveats: N/A

### AWS Security Groups allow internet traffic to SSH port (22)

- Script name: [`AWS-EC2-002.py`](runbooks/AWS-EC2-002.py)
- Prisma Cloud policy descriptor: `PC-AWS-VPC-23`
- Runbook summary: Removes EC2 security group rules containing global access to TCP port 22 (SSH).
- Required IAM permissions:
  - `ec2:DescribeSecurityGroups`
  - `ec2:RevokeSecurityGroupIngress`
- CIS section: 4.1
- Caveats: N/A

### AWS Security Groups allow internet traffic from internet to Telnet port (23)

- Script name: [`AWS-EC2-003.py`](runbooks/AWS-EC2-003.py)
- Prisma Cloud policy descriptor: `PC-AWS-VPC-236`
- Runbook summary: Removes EC2 security group rules containing global access to TCP port 23 (Telnet).
- Required IAM permissions:
  - `ec2:DescribeSecurityGroups`
  - `ec2:RevokeSecurityGroupIngress`
- CIS section: N/A
- Caveats: N/A

### AWS Security Groups allow internet traffic from internet to RDP port (3389)

- Script name: [`AWS-EC2-004.py`](runbooks/AWS-EC2-004.py)
- Prisma Cloud policy descriptor: `PC-AWS-VPC-24`
- Runbook summary: Removes EC2 security group rules containing global access to TCP port 3389 (RDP).
- Required IAM permissions:
  - `ec2:DescribeSecurityGroups`
  - `ec2:RevokeSecurityGroupIngress`
- CIS section: 4.2
- Caveats: N/A

### AWS Security Groups allow internet traffic from internet to MYSQL port (3306)

- Script name: [`AWS-EC2-010.py`](runbooks/AWS-EC2-010.py)
- Prisma Cloud policy descriptor: `PC-AWS-VPC-229`
- Runbook summary: Removes EC2 security group rules containing global access to TCP port 3306 (MySQL).
- Required IAM permissions:
  - `ec2:DescribeSecurityGroups`
  - `ec2:RevokeSecurityGroupIngress`
- CIS section: N/A
- Caveats: N/A

### AWS Security Groups allow internet traffic from internet to PostgreSQL port (5432)

- Script name: [`AWS-EC2-010.py`](runbooks/AWS-EC2-010.py)
- Prisma Cloud policy descriptor: `PC-AWS-VPC-230`
- Runbook summary: Removes EC2 security group rules containing global access to TCP port 5432 (PostgreSQL).
- Required IAM permissions:
  - `ec2:DescribeSecurityGroups`
  - `ec2:RevokeSecurityGroupIngress`
- CIS section: N/A
- Caveats: N/A

### AWS Security Groups allow internet traffic from internet to SQLServer port (1433)

- Script name: [`AWS-EC2-010.py`](runbooks/AWS-EC2-010.py)
- Prisma Cloud policy descriptor: `PC-AWS-VPC-233`
- Runbook summary: Removes EC2 security group rules containing global access to TCP port 1433 (SQLServer).
- Required IAM permissions:
  - `ec2:DescribeSecurityGroups`
  - `ec2:RevokeSecurityGroupIngress`
- CIS section: N/A
- Caveats: N/A

### AWS Security Groups allow internet traffic from internet to MSQL port (4333)

- Script name: [`AWS-EC2-010.py`](runbooks/AWS-EC2-010.py)
- Prisma Cloud policy descriptor: `PC-AWS-VPC-247`
- Runbook summary: Removes EC2 security group rules containing global access to TCP port 4333 (MYSQL).
- Required IAM permissions:
  - `ec2:DescribeSecurityGroups`
  - `ec2:RevokeSecurityGroupIngress`
- CIS section: N/A
- Caveats: N/A

### AWS Security Groups allow internet traffic from internet to VNC Listener port (5500)

- Script name: [`AWS-EC2-010.py`](runbooks/AWS-EC2-010.py)
- Prisma Cloud policy descriptor: `PC-AWS-VPC-238`
- Runbook summary: Removes EC2 security group rules containing global access to TCP port 5500 (VNC Listener).
- Required IAM permissions:
  - `ec2:DescribeSecurityGroups`
  - `ec2:RevokeSecurityGroupIngress`
- CIS section: N/A
- Caveats: N/A

### AWS Security Groups allow internet traffic from internet to VNC Server port (5900)

- Script name: [`AWS-EC2-010.py`](runbooks/AWS-EC2-010.py)
- Prisma Cloud policy descriptor: `PC-AWS-VPC-232`
- Runbook summary: Removes EC2 security group rules containing global access to TCP port 5900 (VNC Server).
- Required IAM permissions:
  - `ec2:DescribeSecurityGroups`
  - `ec2:RevokeSecurityGroupIngress`
- CIS section: N/A
- Caveats: N/A

### AWS Security Groups allow internet traffic from internet to FTP port (21)

- Script name: [`AWS-EC2-010.py`](runbooks/AWS-EC2-010.py)
- Prisma Cloud policy descriptor: `PC-AWS-VPC-245`
- Runbook summary: Removes EC2 security group rules containing global access to TCP port 21 (FTP).
- Required IAM permissions:
  - `ec2:DescribeSecurityGroups`
  - `ec2:RevokeSecurityGroupIngress`
- CIS section: N/A
- Caveats: N/A

### AWS Security Groups allow internet traffic from internet to FTP-Data port (20)

- Script name: [`AWS-EC2-010.py`](runbooks/AWS-EC2-010.py)
- Prisma Cloud policy descriptor: `PC-AWS-VPC-248`
- Runbook summary: Removes EC2 security group rules containing global access to TCP port 20 (FTP-Data).
- Required IAM permissions:
  - `ec2:DescribeSecurityGroups`
  - `ec2:RevokeSecurityGroupIngress`
- CIS section: N/A
- Caveats: N/A

### AWS Security Groups allow internet traffic from internet to SMTP port (25)

- Script name: [`AWS-EC2-010.py`](runbooks/AWS-EC2-010.py)
- Prisma Cloud policy descriptor: `PC-AWS-VPC-227`
- Runbook summary: Removes EC2 security group rules containing global access to TCP port 25 (SMTP).
- Required IAM permissions:
  - `ec2:DescribeSecurityGroups`
  - `ec2:RevokeSecurityGroupIngress`
- CIS section: N/A
- Caveats: N/A

### AWS Security Groups allow internet traffic from internet to DNS port (53)

- Script name: [`AWS-EC2-010.py`](runbooks/AWS-EC2-010.py)
- Prisma Cloud policy descriptor: `PC-AWS-VPC-228`
- Runbook summary: Removes EC2 security group rules containing global access to TCP port 53 (DNS).
- Required IAM permissions:
  - `ec2:DescribeSecurityGroups`
  - `ec2:RevokeSecurityGroupIngress`
- CIS section: N/A
- Caveats: N/A

### AWS delete unused EC2 Security Groups

- Script name: [`AWS-EC2-031.py`](runbooks/AWS-EC2-031.py)
- Prisma Cloud policy descriptor: `N/A`
- Runbook summary: Deletes unused EC2 security groups.
- Required IAM permissions:
  - `ec2:DeleteSecurityGroup`
  - `ec2:DescribeSecurityGroups`
  - `lambda:ListFunctions`
- CIS section: N/A
- Caveats: N/A

### AWS Amazon Machine Image (AMI) is publicly accessible

- Script name: [`AWS-EC2-036.py`](runbooks/AWS-EC2-036.py)
- Prisma Cloud policy descriptor: `PC-AWS-EC2-35`
- Runbook summary: Sets Public AMIs to Private.
- Required IAM permissions:
  - `ec2:DescribeImageAttribute`
  - `ec2:ModifyImageAttribute`
- CIS section: N/A
- Caveats: N/A

### AWS Default Security Group does not restrict all traffic

- Script name: [`AWS-EC2-038.py`](runbooks/AWS-EC2-038.py)
- Prisma Cloud policy descriptor: `PC-AWS-VPC-22`
- Runbook summary: Removes all rules from the **default** EC2 security group.
- Required IAM permissions:
  - `ec2:DescribeSecurityGroups`
  - `ec2:RevokeSecurityGroupIngress`
  - `ec2:RevokeSecurityGroupEgress`
- CIS section: 4.3
- Caveats: N/A

### AWS Security Groups with Inbound rule overly permissive to All Traffic

- Script name: [`AWS-EC2-039.py`](runbooks/AWS-EC2-039.py)
- Prisma Cloud policy descriptor: `PC-AWS-VPC-222`
- Runbook summary: Removes EC2 security group rules with Global access on all ports.
- Required IAM permissions:
  - `ec2:DescribeSecurityGroups`
  - `ec2:RevokeSecurityGroupIngress`
- CIS section: N/A
- Caveats: N/A

### AWS EBS snapshots are accessible to public

- Script name: [`AWS-EC2-042.py`](runbooks/AWS-EC2-042.py)
- Prisma Cloud policy descriptor: `PC-AWS-EC2-31`
- Runbook summary: Sets Public EBS snapshots to Private.
- Required IAM permissions:
  - `ec2:DescribeSnapshotAttribute`
  - `ec2:ModifySnapshotAttribute`
- CIS section: N/A
- Caveats: N/A

## ELB Runbooks

### AWS Elastic Load Balancer (Classic) with connection draining disabled

- Script name: [`AWS-ELB-009.py`](runbooks/AWS-ELB-009.py)
- Prisma Cloud policy descriptor: `PC-AWS-ELB-267`
- Runbook summary: Enables ELB (Classic) Connection Draining.
- Required IAM permissions:
  - `elasticloadbalancing:DescribeLoadBalancerAttributes`
  - `elasticloadbalancing:ModifyLoadBalancerAttributes`
- CIS section: N/A
- Caveats: N/A

### AWS Elastic Load Balancer (Classic) with cross-zone load balancing disabled

- Script name: [`AWS-ELB-012.py`](runbooks/AWS-ELB-012.py)
- Prisma Cloud policy descriptor: `PC-AWS-ELB-266`
- Runbook summary: Enables ELB (Classic) Cross-Zone Load Balancing.
- Required IAM permissions:
  - `elasticloadbalancing:DescribeLoadBalancerAttributes`
  - `elasticloadbalancing:ModifyLoadBalancerAttributes`
- CIS section: N/A
- Caveats: N/A

### AWS Elastic Load Balancer (Classic) with access log disabled

- Script name: [`AWS-ELB-013.py`](runbooks/AWS-ELB-013.py)
- Prisma Cloud policy descriptor: `PC-AWS-ELB-265`
- Runbook summary: Enables ELB (Classic) Access Logs. Creates (if needed) an ELB logs S3 bucket for the region.
- Required IAM permissions:
  - `elasticloadbalancing:DescribeLoadBalancerAttributes`
  - `elasticloadbalancing:ModifyLoadBalancerAttributes`
  - `s3:CreateBucket`
  - `s3:PutBucketPolicy`
  - `s3:PutObject`
  - `sts:GetCallerIdentity`
- CIS section: N/A
- Caveats: N/A

### AWS Elastic Load Balancer v2 (ELBv2) Application Load Balancer (ALB) with access log disabled

- Script name: [`AWS-ELB-015.py`](runbooks/AWS-ELB-015.py)
- Prisma Cloud policy descriptor: `PC-AWS-ELB-242`
- Runbook summary: Enables Application ELB (elbv2) Access Logs. Creates (if needed) an ELB logs S3 bucket for the region.
- Required IAM permissions:
  - `elasticloadbalancing:DescribeLoadBalancerAttributes`
  - `elasticloadbalancing:DescribeLoadBalancers`
  - `elasticloadbalancing:ModifyLoadBalancerAttributes`
  - `s3:CreateBucket`
  - `s3:PutBucketPolicy`
  - `s3:PutObject`
- CIS section: N/A
- Caveats: N/A

## IAM Runbooks

### Enforce AWS account best practices password policy

- Script name: [`AWS-IAM-002.py`](runbooks/AWS-IAM-002.py)
- Prisma Cloud policy descriptor: N/A
- Runbook summary: Enforces AWS account best practices password policy.
- Required IAM permissions:
  - `iam:UpdateAccountPasswordPolicy`
- CIS section: 1.5 - 1.11
- Caveats: N/A

### AWS access keys not used for more than 90 days

- Script name: [`AWS-IAM-015.py`](runbooks/AWS-IAM-015.py)
- Prisma Cloud policy descriptor: `PC-AWS-IAM-48`
- Runbook summary: Deactivates unused IAM access keys.
- Required IAM permissions:
  - `iam:GetAccessKeyLastUsed`
  - `iam:UpdateAccessKey`
- CIS section: 1.3
- Caveats: N/A

### AWS IAM policy allows full administrative privileges

- Script name: [`AWS-IAM-016.py`](runbooks/AWS-IAM-016.py)
- Prisma Cloud policy descriptor: `PC-AWS-IAM-46`
- Runbook summary: Removes IAM policies that allow full administrative privileges.
- Required IAM permissions:
  - `iam:CreatePolicyVersion`
- CIS section: 1.22
- Caveats: N/A

### Create an IAM Support Role to manage incidents with AWS Support

- Script name: [`AWS-IAM-018.py`](runbooks/AWS-IAM-018.py)
- Prisma Cloud policy descriptor: N/A
- Runbook summary: Creates an IAM Support Role to manage incidents with AWS Support.
- Required IAM permissions:
  - `iam:AttachRolePolicy`
  - `iam:CreateRole`
  - `iam:CreateUser`
  - `iam:GetPolicy`
- CIS section: 1.20
- Caveats: N/A

## KMS Runbooks

### AWS Customer Master Key (CMK) rotation is not enabled

- Script name: [`AWS-KMS-001.py`](runbooks/AWS-KMS-001.py)
- Prisma Cloud policy descriptor: `PC-AWS-KMS-20`
- Runbook summary: Enables KMS rotation of a Customer Master Key (CMK).
- Required IAM permissions:
  - `kms:EnableKeyRotation`
- CIS section: 2.8
- Caveats: N/A

## RDS Runbooks

### AWS RDS database instance is publicly accessible

- Script name: [`AWS-RDS-005.py`](runbooks/AWS-RDS-005.py)
- Prisma Cloud policy descriptor: `PC-AWS-RDS-99`
- Runbook summary: Sets Public RDS DB instances to Private.
- Required IAM permissions:
  - `rds:DescribeDBInstances`
  - `rds:ModifyDBInstance`
- CIS section: N/A
- Caveats: N/A

### AWS RDS snapshots are accessible to public

- Script name: [`AWS-RDS-007.py`](runbooks/AWS-RDS-007.py)
- Prisma Cloud policy descriptor: `PC-AWS-RDS-32`
- Runbook summary: Sets Public RDS snapshots to Private.
- Required IAM permissions:
  - `rds:DescribeDBSnapshotAttributes`
  - `rds:ModifyDBSnapshotAttribute`
- CIS section: N/A
- Caveats: N/A

### AWS RDS instance with Multi-Availability Zone disabled

- Script name: [`AWS-RDS-010.py`](runbooks/AWS-RDS-010.py)
- Prisma Cloud policy descriptor: `PC-AWS-RDS-218`
- Runbook summary: Enables RDS DB instance Multi-AZ.
- Required IAM permissions:
  - `rds:DescribeDBInstances`
  - `rds:ModifyDBInstance`
- CIS section: N/A
- Caveats: N/A

### AWS RDS minor upgrades not enabled

- Script name: [`AWS-RDS-011.py`](runbooks/AWS-RDS-011.py)
- Prisma Cloud policy descriptor: `PC-AWS-RDS-260`
- Runbook summary: Enables RDS DB instance Auto Minor Version Upgrade.
- Required IAM permissions:
  - `rds:DescribeDBInstances`
  - `rds:ModifyDBInstance`
- CIS section: N/A
- Caveats: N/A

## Redshift Runbooks

### AWS Redshift clusters should not be publicly accessible

- Script name: [`AWS-REDSHIFT-001.py`](runbooks/AWS-REDSHIFT-001.py)
- Prisma Cloud policy descriptor: `PC-AWS-RED-79`
- Runbook summary: Sets Public Redshift clusters to Private.
- Required IAM permissions:
  - `redshift:DescribeClusters`
  - `redshift:ModifyCluster`
- CIS section: N/A
- Caveats: N/A

## S3 Runbooks

### AWS S3 Object Versioning is disabled

- Script name: [`AWS-SSS-001.py`](runbooks/AWS-SSS-001.py)
- Prisma Cloud policy descriptor: `PC-AWS-S3-259`
- Runbook summary: Enables S3 bucket Object Versioning.
- Required IAM permissions:
  - `s3:PutBucketVersioning`
- CIS section: N/A
- Caveats: N/A

### AWS S3 bucket has global view ACL permissions enabled

- Script name: [`AWS-SSS-008.py`](runbooks/AWS-SSS-008.py)
- Prisma Cloud policy descriptor: `PC-AWS-S3-251`
- Runbook summary: Removes S3 bucket ACL Global policy.
- Required IAM permissions:
  - `s3:GetBucketAcl`
  - `s3:PutBucketAcl`
- CIS section: N/A
- Caveats: N/A

### AWS Access logging not enabled on S3 buckets

- Script name: [`AWS-SSS-009.py`](runbooks/AWS-SSS-009.py)
- Prisma Cloud policy descriptor: `PC-AWS-S3-30`
- Runbook summary: Enables S3 bucket logging. Creates (if needed) a target logging bucket for the region.
- Required IAM permissions:
  - `sts:GetCallerIdentity`
  - `s3:CreateBucket`
  - `s3:GetBucketLogging`
  - `s3:PutBucketLogging`
- CIS section: 2.6
- Caveats: N/A

### AWS S3 buckets do not have server side encryption

- Script name: [`AWS-SSS-014.py`](runbooks/AWS-SSS-014.py)
- Prisma Cloud policy descriptor: `PC-AWS-S3-64`
- Runbook summary: Enables S3 Server-Side Encryption.
- Required IAM permissions:
  - `s3:PutEncryptionConfiguration`
- CIS section: N/A
- Caveats: N/A

### AWS S3 buckets are accessible to public

- Script name: [`PC-AWS-S3-29.py`](runbooks/PC-AWS-S3-29.py)
- Prisma Cloud policy descriptor: `PC-AWS-S3-29`
- Runbook summary: Removes S3 bucket public access at the bucket level.
- Required IAM permissions:
  - `s3:PutBucketPublicAccessBlock`
- CIS section: N/A
- Caveats: N/A

## VPC Runbooks

### Release unassociated (unused) Elastic IP addresses

- Script name: [`AWS-VPC-013.py`](runbooks/AWS-VPC-013.py)
- Prisma Cloud policy descriptor: N/A
- Runbook summary: Releases unassociated (unused) Elastic IP addresses.
- Required IAM permissions:
  - `ec2:DescribeAddresses`
  - `ec2:ReleaseAddress`
- CIS section: N/A
- Caveats: N/A

### AWS VPC has flow logs disabled

- Script name: [`AWS-VPC-020.py`](runbooks/AWS-VPC-020.py)
- Prisma Cloud policy descriptor: `PC-AWS-VPC-25`
- Runbook summary: Enables VPC flow logs. Creates (if needed) the necessary IAM Policy and CloudWatch Logs group.
- Required IAM permissions:
  - `iam:PutRolePolicy`
  - `iam:CreateRole`
  - `iam:GetRole`
  - `iam:PassRole`
  - `logs:CreateLogGroup`
  - `logs:PutRetentionPolicy`
  - `ec2:CreateFlowLogs`
- CIS section: 2.9
- Caveats: N/A

### Delete AWS default VPC

- Script name: [`AWS-VPC-Default.py`](runbooks/AWS-VPC-Default.py)
- Prisma Cloud policy descriptor: N/A
- Runbook summary: Deletes the AWS default VPC.
- Required IAM permissions:
  - `ec2:DeleteInternetGateway`
  - `ec2:DeleteNetworkAcl`
  - `ec2:DeleteRouteTable`
  - `ec2:DeleteSecurityGroup`
  - `ec2:DeleteSubnet`
  - `ec2:DeleteVpc`
  - `ec2:DescribeInternetGateways`
  - `ec2:DescribeNetworkAcls`
  - `ec2:DescribeNetworkInterfaces`
  - `ec2:DescribeRouteTables`
  - `ec2:DescribeSecurityGroups`
  - `ec2:DescribeSubnets`
  - `ec2:DescribeVpcs`
  - `ec2:DetachInternetGateway`
- CIS section: N/A
- Caveats: N/A

## Misc Runbooks

### Example Runbook

- Script name: [`AWS-TEST-001.py`](runbooks/AWS-TEST-001.py)
- Prisma Cloud policy descriptor: N/A
- Runbook summary: Example runbook which can be used to test your Lambda. Check out the [setup guide](../docs/setup.md) for more info.
- Required IAM permissions: N/A
- CIS section: N/A
- Caveats: N/A
