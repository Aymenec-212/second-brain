---
created_at: '2026-07-21T13:10:49.633658Z'
entities:
- AWS
- EC2
- ECS
- EKS
- Lambda
- IAM
- VPC
- CloudWatch
- CodePipeline
- GitHub Actions
id: 01KY2CSTH0N348751CFM874R1E
language: en
source:
  end_turn: 0
  session_id: 01KY2CRWDXEW7NWRH7HPKH2RVY
  start_turn: 0
tags:
- aws
- deployment
- cloud
- infrastructure
- ops
title: 'Decision: Use AWS for deployment'
type: decision
---

I decided to use AWS for deploying the project. Record this as the chosen cloud provider so future architecture and procurement decisions assume AWS unless explicitly changed. This decision affects account setup, service selection, security posture, cost estimates, and CI/CD choices.

Immediate implications and things to resolve: set up (or confirm) an AWS account and billing, choose a primary AWS region, configure IAM roles and policies for least privilege, and design the network (VPC, subnets, security groups). Decide whether to deploy using virtual machines (EC2), containers (ECS or EKS), or serverless (Lambda); each has different operational and cost trade-offs. Set up monitoring and logging (CloudWatch), backups, and alerting. Plan CI/CD (AWS CodePipeline or external tools such as GitHub Actions). Estimate monthly costs using the AWS Pricing Calculator and add billing alerts.

Open questions to answer next: which deployment model (EC2/ECS/EKS/Lambda) best fits expected load and team skills; target AWS region; initial sizing and autoscaling policy; security/compliance requirements and data residency; timeline for migration/first deployment; who needs AWS access and what IAM groups to create.

Next concrete steps: create/verify AWS account and billing alerts, pick a region, prototype a minimal environment, run a cost estimate, and schedule a short architecture decision meeting to choose the specific services and CI/CD approach.