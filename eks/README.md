# AWS EKS & GitOps Deployment Documentation

This directory contains the Kubernetes manifests, cluster provisioning configuration, and GitOps application resources required to deploy the Medical Chatbot to a production-grade **Amazon Elastic Kubernetes Service (EKS)** cluster managed via **ArgoCD** (GitOps).

---

## 🏗️ 1. GitOps & EKS Architecture

In this deployment strategy, the active configuration is driven entirely by Git. 

```text
[Developer]
    │
    ├─► Push Code (app.py, src/, etc.)
    ▼
[GitHub Actions (CI)]
    │
    ├─► Build & Test Docker Image
    ├─► Push Image to Amazon ECR (tagged with Git SHA)
    ├─► Modify 'eks/deployment.yaml' image tag to match Git SHA
    ├─► Commit & Push updated manifest back to GitHub Repository
    ▼
[GitHub Repository] (State Changed)
    ▲
    │ Polls Git repository for changes / Webhook
[ArgoCD Controller (on EKS)]
    │
    ├─► Detects diff between Git and EKS cluster state
    ├─► Synchronizes changes automatically
    ▼
[AWS EKS Cluster]
    │
    └─► Spawns updated chatbot pods and configures AWS ALB Ingress
```

---

## 🛠️ 2. Prerequisites & CLI Installation

Ensure you have the following installed on your management machine or EC2 bastion:
*   [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) configured with Administrator permissions (`aws configure`).
*   [eksctl](https://eksctl.io/introduction/#installation) (EKS Cluster CLI tool).
*   [kubectl](https://kubernetes.io/docs/tasks/tools/) matching your cluster version.

---

## 🚀 3. Step-by-Step EKS Deployment Guide

### Step 1: Provision the EKS Cluster
Deploy the cluster utilizing the managed node group configuration template `eksctl-config.yaml`:
```bash
eksctl create cluster -f eks/eksctl-config.yaml
```
*This command creates an EKS cluster named `medical-chatbot-eks` in region `us-east-1` with 2 private worker nodes.*

### Step 2: Install AWS Load Balancer Controller
AWS EKS requires the Application Load Balancer (ALB) Controller to route traffic via the Ingress resource:

```bash
# 1. Create IAM OIDC provider
eksctl utils associate-iam-oidc-provider --cluster=medical-chatbot-eks --approve

# 2. Download IAM Policy
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.5.4/docs/install/iam_policy.json

# 3. Create IAM Policy in AWS
aws iam create-policy \
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://iam_policy.json

# 4. Create IAM Service Account
eksctl create iamserviceaccount \
  --cluster=medical-chatbot-eks \
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --role-name AmazonEKSLoadBalancerControllerRole \
  --attach-policy-arn=arn:aws:iam::<AWS_ACCOUNT_ID>:policy/AWSLoadBalancerControllerIAMPolicy \
  --approve

# 5. Install Controller via Helm
helm repo add eks https://aws.github.io/eks-charts
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=medical-chatbot-eks \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller
```

### Step 3: Install ArgoCD on the EKS Cluster
Install ArgoCD in a dedicated `argocd` namespace:
```bash
# Create Namespace
kubectl create namespace argocd

# Apply ArgoCD installation manifests
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

To access the ArgoCD dashboard externally, patch the server service to a LoadBalancer type:
```bash
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
```
Get the LoadBalancer hostname and default admin password:
```bash
# Get Dashboard URL
kubectl get svc argocd-server -n argocd

# Get Admin Password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### Step 4: Deploy the ArgoCD Application
Run the following to bootstrap the GitOps controller to watch your repository:
```bash
kubectl apply -f eks/argocd-app.yaml
```
ArgoCD will automatically create the `medical-chatbot-eks` namespace and deploy the secret, configmap, deployment, service, ingress, and HPA resources.

---

## ⚙️ 4. Secret Configuration on EKS

In GitOps, you should not save plain-text passwords on GitHub. Before synching:
1. Base64-encode your secrets:
   ```bash
   echo -n "your-openai-api-key" | base64
   ```
2. Update the encoded values locally in `eks/secret.yaml` or inject them directly into EKS:
   ```bash
   kubectl edit secret medical-chatbot-secrets -n medical-chatbot-eks
   ```

---

## 🔍 5. Verification & Troubleshooting

### Check Pods and Services
```bash
# Verify pods are running
kubectl get pods -n medical-chatbot-eks

# Verify AWS ALB has been provisioned
kubectl get ingress -n medical-chatbot-eks
```

### Troubleshoot Ingress / LoadBalancer
If Ingress has no Address assigned:
*   Inspect AWS Load Balancer Controller logs:
    ```bash
    kubectl logs -n kube-system -l app.kubernetes.io/name=aws-load-balancer-controller
    ```
*   Ensure EKS Subnets are tagged correctly for public ingress:
    *   `kubernetes.io/role/elb` = `1` (for public subnets)
    *   `kubernetes.io/role/internal-elb` = `1` (for private subnets)
