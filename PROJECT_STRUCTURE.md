# Enterprise Project Structure

This project has been transformed from a basic Flask app into a production-grade LLMOps architecture.

## Folder Hierarchy

- `app/`: Core application logic (Flask, LangChain, src).
- `docker/`: Dockerfiles for production and staging.
- `infra/`: Generic infrastructure scripts.
- `terraform/`: Infrastructure as Code (AWS VPC, EKS, ECR).
- `kubernetes/`: K8s manifests (Deployment, Service, HPA, ConfigMaps).
- `monitoring/`: Prometheus, Grafana, and Loki configurations.
- `docs/`: Comprehensive documentation (Installation, Deployment, Security, LLMOps).
- `scripts/`: Utility scripts for database migration and indexing.
- `tests/`: Unit and integration tests.
- `.github/workflows/`: CI/CD automation pipelines.

## Key Files
- `docker-compose.yml`: For local staging and development.
- `requirements.txt`: Moved to `app/requirements.txt`.
- `.env.example`: Template for environment variables.
