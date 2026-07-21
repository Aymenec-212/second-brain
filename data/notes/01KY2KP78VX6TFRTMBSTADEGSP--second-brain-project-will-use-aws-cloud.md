---
created_at: '2026-07-21T15:11:11.643464Z'
entities:
- Second Brain
- AWS
id: 01KY2KP78VX6TFRTMBSTADEGSP
language: en
source:
  end_turn: 0
  session_id: 01KY2KKX71474CWZQXF3NEHD2G
  start_turn: 0
tags:
- second brain
- aws
- deployment
- infrastructure
title: Second Brain project will use AWS cloud
type: fact
---

I will deploy the Second Brain project to the AWS cloud. This is a current, concrete constraint for the project: the chosen cloud provider is Amazon Web Services (AWS). Treat this as a baseline decision that affects tooling, account setup, cost model, available managed services, and security/compliance requirements. Key immediate implications to track: I need an AWS account (or accounts) and IAM structure, an agreed AWS region or regions for deployment, an initial estimate of monthly budget and cost controls, and a plan for backups and recovery that align with AWS services (S3, EBS snapshots, RDS snapshots, etc.). Open questions to resolve soon: which AWS services will host the application (EC2, ECS/EKS, Lambda, Elastic Beanstalk, managed databases, etc.), whether to use a single account or multiple accounts (per environment or per team), and what the target availability/SLAs should be. Things to check first: current AWS account limits and permissions, compliance or data residency constraints in the intended region, and any existing organizational policies for tagging, billing, and VPC networking. Capture this fact now so all later deployment decisions assume AWS as the provider unless I explicitly change it.