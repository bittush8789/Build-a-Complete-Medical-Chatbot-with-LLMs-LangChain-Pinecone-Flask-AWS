# Enterprise Deployment Guide

This guide covers the end-to-end deployment process from Infrastructure provisioning to CI/CD.

## 1. Infrastructure Provisioning (Terraform)
Navigate to the `terraform/` directory:
```bash
terraform init
terraform plan
terraform apply -auto-approve
```
This will create:
- VPC with Public/Private subnets.
- EKS Cluster (Elastic Kubernetes Service).
- ECR Repository (Elastic Container Registry).

## 2. Production Server Hardening (Jumpbox/Deployer)
Commands for setting up a secure Linux server:
```bash
# Create deploy user
sudo adduser deploy
sudo usermod -aG sudo deploy

# Firewall setup (UFW)
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable

# Fail2Ban for SSH protection
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

## 3. Reverse Proxy & SSL (Nginx + Certbot)
```bash
sudo apt install nginx -y
sudo apt install certbot python3-certbot-nginx -y

# Configure Nginx for the domain
sudo certbot --nginx -d yourdomain.com
```

## 4. CI/CD Strategy
- **Branching Strategy**: GitFlow (main, staging, feature/*).
- **Deployment Strategy**: Rolling Update (Kubernetes Default).
- **Rollback**: `kubectl rollout undo deployment/medical-chatbot-deploy`

## 5. Scaling Strategy
- **Horizontal Pod Autoscaling (HPA)**: Configured in `kubernetes/hpa.yml` (to be created) to scale based on CPU/Memory.
- **Cluster Autoscaler**: Enabled on EKS via Terraform.
