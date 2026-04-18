# Enterprise Operations Runbook

This document provides commands for daily administration, debugging, and maintenance.

## 1. Daily Admin Commands
```bash
# Check application status in K8s
kubectl get pods -n production
kubectl get services -n production

# View application logs
kubectl logs -f deployment/medical-chatbot-deploy -n production

# Check resource usage
kubectl top pods -n production
```

## 2. Debugging & Troubleshooting
```bash
# Describe a failing pod
kubectl describe pod <pod-name> -n production

# Execute a shell in a running container
kubectl exec -it <pod-name> -n production -- /bin/bash

# View events in the namespace
kubectl get events -n production --sort-by='.lastTimestamp'
```

## 3. Logs & Monitoring
- **Grafana**: Access at `http://grafana.yourdomain.com` to view system metrics.
- **Prometheus**: Access at `http://prometheus.yourdomain.com` for ad-hoc queries.
- **Loki**: Use Grafana Explore to search through application logs.

## 4. Scaling & Restarts
```bash
# Manual Scaling
kubectl scale deployment/medical-chatbot-deploy --replicas=5 -n production

# Rolling Restart
kubectl rollout restart deployment/medical-chatbot-deploy -n production
```

## 5. Maintenance & Upgrades
```bash
# Upgrade Helm charts
helm upgrade monitoring prometheus-community/kube-prometheus-stack

# Update Terraform Infrastructure
cd terraform/
terraform apply -auto-approve
```

## 6. Database (Pinecone) Maintenance
- **Upserting Data**: Run `python app/store_index.py` (ensure env vars are set).
- **Clearing Index**: Use the Pinecone Python SDK to delete all vectors if needed.
