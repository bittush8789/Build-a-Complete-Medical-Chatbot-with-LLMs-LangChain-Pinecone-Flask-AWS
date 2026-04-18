# Enterprise Installation Guide

This guide provides step-by-step commands to set up the Medical Chatbot production environment on Ubuntu 22.04 LTS.

## 1. System Preparation
Update system packages and install essential build tools.
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3-pip python3-venv curl build-essential
```

## 2. Docker & Docker Compose
Used for containerization and local orchestration.
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose-v2 -y
```

## 3. Terraform (IaC)
Used for provisioning AWS infrastructure.
```bash
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

## 4. Kubernetes (kubectl & Helm)
Used for managing the production cluster.
```bash
# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

## 5. Monitoring (Prometheus & Grafana)
We use the Prometheus Operator (Loki/Grafana/Prometheus) for the K8s stack.
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install monitoring prometheus-community/kube-prometheus-stack
```

## 6. LLMOps Tools
- **MLflow**: `pip install mlflow`
- **LangChain**: `pip install langchain`
- **Pinecone SDK**: `pip install pinecone-client`
- **OpenTelemetry**: `pip install opentelemetry-api opentelemetry-sdk`
