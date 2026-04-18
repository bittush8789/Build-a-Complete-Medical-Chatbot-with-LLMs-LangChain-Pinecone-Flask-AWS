# Security & Compliance Guide (Healthcare Focused)

This project follows HIPAA-compliant architectural patterns for handling medical data.

## 1. Secrets Management
- **DO NOT** commit `.env` files.
- Use **AWS Secrets Manager** or **HashiCorp Vault**.
- Kubernetes: Use `ExternalSecrets` to sync AWS secrets to K8s secrets.

## 2. Data Encryption
- **At Rest**: AES-256 encryption on RDS/Pinecone.
- **In Transit**: TLS 1.3 for all API communication.

## 3. IAM Least Privilege
- EKS Nodes should use OIDC roles (IRSA) to access S3/Pinecone.
- Use separate IAM users for CI/CD with restricted policies.

## 4. API Security
- **Rate Limiting**: Implemented via Nginx or API Gateway.
- **WAF**: AWS WAF to protect against SQLi and XSS.
- **Authentication**: JWT-based auth or API Keys.

## 5. Audit Logging
- Enable AWS CloudTrail.
- Log all LLM inputs/outputs to a secure, tamper-proof S3 bucket for compliance auditing.

## 6. DDoS Protection
- Use AWS Shield (Standard) and CloudFront for edge protection.
