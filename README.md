# Prisma Enhanced Remediation

Create custom auto-remediation solutions for Prisma Cloud using serverless functions in the cloud.

## Summary

- [Summary](#summary)
- [What are Serverless Functions?](#what-are-serverless-functions)
- [Why Remediate Using Serverless?](#why-remediate-using-serverless)
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Support](#support)
- [Built With](#built-with)
- [Contributing](#contributing)
- [Maintainers](#maintainers)
- [Acknowledgments](#acknowledgments)

## What are Serverless Functions?

Serverless functions is a service offered by Cloud Service Providers (CSPs) that let you run code (e.g. Python scripts) without provisioning or managing servers. You pay only for the compute time you consume. Serverless has the benefit of letting you focus more on the code itself; the infrastructure, scaling, and availability factors are all taken care of automatically by the CSP.

## Why Remediate Using Serverless?

Serverless functions are a simple way to create custom auto-remediation solutions based on Prisma Cloud alerts. Using Prisma Cloud's built-in integrations to CSPs (e.g. AWS SQS), you can quickly and easily remediate misconfigurations in your cloud environment with the flexibility of a full-fledged coding environment.

For example, instead of automatically deleting an insecure AWS S3 bucket, you could create a backup of it before deletion; perhaps you want to send a Slack notification after enabling VPC flow logs. Both of these are possible using serverless auto-remediation. This repo gives you the starting point to build your own specific auto-remediation capabilities.

## Getting Started

There are different setup instructions depending on your CSP (Cloud Service Provider):

- [Amazon Web Services (AWS) Setup Guide](AWS/docs/setup.md)
  - [Out-of-the-box runbooks and associated Prisma Cloud policies](AWS/lambda_package/README.md)

## Prerequisites

Using our out-of-the-box runbooks takes minimal programming knowledge and can be set up by following our step-by-step instructions. Developing your own runbooks will require familiarity with your CSP's relevant SDK.

## Support

This template/solution are released under an as-is, best effort, support policy. These scripts should be seen as community supported and Palo Alto Networks will contribute our expertise as and when possible. Please read [SUPPORT.md](SUPPORT.md) for more details on this project's support policy.

## Built With

- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - The AWS SDK

## Contributing

We value your contributions! Please read
[CONTRIBUTING.md](CONTRIBUTING.md)
for details on how to contribute, and the process for submitting pull requests
to us. If you have a custom runbook you would like to contribute, feel free to make a pull request and it'll be reviewed for future releases.

## Maintainers

- Todd Murchison - [toddm92](https://github.com/toddm92)
- Young Lee - [youngleepanw](https://github.com/youngleepanw)

Thank you to all the
[contributors](https://github.com/PaloAltoNetworks/Prisma-Enhanced-Remediation/contributors)
who participated in this project.

## Acknowledgments

- Kasi Annamalai
- Antony Setiawan
