# Runbooks

   Runbook   | Description | CIS |     Prisma Cloud Id
:-----------:|:------------|-----|:-----------------------:
 **CloudFormation**
 AWS-CFM-003 | Enable CloudFormation Stack termination protection. | | n/a
 **CloudTrail**
 AWS-CLT-002 | Encrypt CloudTrail S3 logs with a KMS Customer Managed Key (CMK). | 2.7 | c2b84f89-7ec8-473e-a6af-404feeeb96c5
 AWS-CLT-004 | Integrate CloudTrail with CloudWatch Logs. Creates (if needed) the necessary IAM Policy and CloudWatch Logs group. | 2.4 | 962e0daa-3c2d-4d79-9a5f-e0bf8fd4bb3b
 AWS-CLT-005 | Enable CloudTrail log file validation. | 2.2 | 38e3d3cf-b694-46ec-8bd2-8f02194b5040
 AWS-CLT-006 | Remove CloudTrail S3 bucket ACL Public policy. | 2.3 | a5fe47e1-54f3-47e1-a2a3-deedfb2f70b2
 **Config**
 AWS-CONFIG-001 |  Enable Config. Creates (if needed) the necessary IAM Role and S3 Bucket/ Policy. | 2.5 | n/a
 **ELB**
 AWS-ELB-009 | Enable ELB (Classic) Connection Draining. | | 7eb7f61e-df59-42d4-8236-7d012f278fa6
 AWS-ELB-012 | Enable ELB (Classic) Cross-Zone Load Balancing. | | 551ee7ba-edb6-468e-a018-8774da9b1e85
 AWS-ELB-013 | Enable ELB (Classic) Access Logs. Creates (if needed) an ELB logs S3 bucket for the region. | | b675c604-e886-43aa-a60f-a9ad1f3742d3
 AWS-ELB-015 | Enable Application ELB (elbv2) Access Logs. Creates (if needed) an ELB logs S3 bucket for the region. | | f2a2bcf1-2966-4cb5-9230-bd39c9903a02
 **EC2**
 AWS-EC2-001 | Create an EBS snapshot if a snapshot doesn't exist, or is older than 15 days. | | n/a
 AWS-EC2-002 | Remove EC2 security group rules containing global access to TCP port 22 (SSH). | 4.1 | 617b9138-584b-4e8e-ad15-7fbabafbed1a
 AWS-EC2-003 | Remove EC2 security group rules containing global access to TCP port 23 (Telnet). | | 519456f2-f9eb-407b-b32d-064f1ac7f0ca
 AWS-EC2-004 | Remove EC2 security group rules containing global access to TCP port 3389 (RDP). | 4.2 | b82f90ce-ed8b-4b49-970c-2268b0a6c2e5
 AWS-EC2-009 | Remove EC2 security group rules containing global access to TCP port 3306 (MySQL). |  | 65daa6a0-e040-434e-aca3-9d5765c96e7c
 AWS-EC2-010 | Remove EC2 security group rules containing global access to TCP port 5432 (PostgreSQL). |  | 3b642d25-4534-487a-9399-c2622754ecb5
 AWS-EC2-011 | Remove EC2 security group rules containing global access to TCP port 1433 (SQLServer). |  | 760f2823-997e-495f-a538-5fb073c0ee78
 AWS-EC2-013 | Remove EC2 security group rules containing global access to TCP port 4333 (MYSQL). |  | ab7f8eda-18ab-457c-b5d3-fd4f53c722bc
 AWS-EC2-014 | Remove EC2 security group rules containing global access to TCP port 5500 (VNC Listener). |  | 8dd9e369-0c09-4477-97a2-ff0d50507fe2
 AWS-EC2-015 | Remove EC2 security group rules containing global access to TCP port 5900 (VNC Server). |  | 89cbc2f1-fcb0-48b9-be71-4cbe2d18a5f7
 AWS-EC2-019 | Remove EC2 security group rules containing global access to TCP port 21 (FTP). |  | 14d10ad2-51df-4b07-be69-e94951cc7067
 AWS-EC2-020 | Remove EC2 security group rules containing global access to TCP port 20 (FTP-Data). |  | cdcd663c-e9c9-4472-9779-e5f38751524a
 AWS-EC2-021 | Remove EC2 security group rules containing global access to TCP port 25 (SMTP). |  | c2074d5a-aa28-4dde-90c1-82f528cec55e
 AWS-EC2-024 | Remove EC2 security group rules containing global access to TCP port 53 (DNS). |  | 6eaf6455-1659-4c4b-bff5-c8c7b0fda201
 AWS-EC2-031 | Delete unused EC2 security groups. | | n/a
 AWS-EC2-036 | Set Public AMI to Private. | | 81a2200a-c63e-4860-85a0-b54eaa581135
 AWS-EC2-038 | Remove All rules from the **default** EC2 security group. | 4.3 | 2378dbf4-b104-4bda-9b05-7417affbba3f
 AWS-EC2-039 | Remove EC2 security group rules with Global access on all ports. | | 566686e8-0581-4df5-ae22-5a901ed37b58
 AWS-EC2-042 | Set Public EBS snapshot to Private. | | 7c714cb4-3d47-4c32-98d4-c13f92ce4ec5
 **IAM**
 AWS-IAM-002 | Enforce AWS account best practices password policy. | 1.5 - 1.11
 AWS-IAM-015 | Deactivate unused IAM access keys. | 1.3 | 7ca5af2c-d18d-4004-9ad4-9c1fbfcab218
 AWS-IAM-016 | Remove IAM policies that allow full administrative privileges. | 1.22 | d9b86448-11a2-f9d4-74a5-f6fc590caeef
 AWS-IAM-018 | Create an IAM Support Role to manage incidents with AWS Support. | 1.20 | n/a
 **KMS**
 AWS-KMS-001 | Enable KMS rotation of a Customer Master Key. | 2.8 | 497f7e2c-b702-47c7-9a07-f0f6404ac896
 **RDS**
 AWS-RDS-005 | Set Public RDS DB instance to Private. | | 1bb6005a-dca6-40e2-b0a6-24da968c0808
 AWS-RDS-007 | Set Public RDS snapshot to Private. | | a707de6a-11b7-478a-b636-5e21ee1f6162
 AWS-RDS-010 | Enable RDS DB instance Multi-AZ. | | c5305272-a732-4e8e-8427-6a9701cd2a6f
 AWS-RDS-011 | Enable RDS DB instance Auto Minor Version Upgrade. | | 9dd6cc35-1855-48c8-86ba-0e1818ce11e2
 **Redshift**
 AWS-REDSHIFT-001 | Set Public Redshift cluster to Private. | | d65fd313-1c5c-42a1-98b2-a73bdeda19a6
 **S3**
 AWS-SSS-001 | Enable S3 bucket Object versioning. | | 89ea62c1-3845-4134-b337-cc82203b8ff9
 AWS-SSS-008 | Remove S3 bucket ACL Global policy. | | 43c42760-5283-4bc4-ac43-a80e58c4139f
 AWS-SSS-009 | Enable S3 bucket logging. Creates (if needed) a target logging bucket for the region. | 2.6 | 4daa435b-fa46-457a-9359-6a4b4a43a442
 AWS-SSS-014 | Enable S3 Server Side Encryption. | | 7913fcbf-b679-5aac-d979-1b6817becb22
 **VPC**
 AWS-VPC-013 | Release unassociated (unused) Elastic IP addresses. | | n/a
 AWS-VPC-020 | Enable VPC flow logs. Creates (if needed) the necessary IAM Policy and CloudWatch Logs group. | 2.9 | 49f4760d-c951-40e4-bfe1-08acaa17672a
 AWS-VPC-Default | Delete the AWS default VPC. | | n/a

