# Medical Chatbot with LLMs, LangChain, Pinecone, Flask, and AWS

[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Flask-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Vector Database](https://img.shields.io/badge/vector%20db-Pinecone-blueviolet.svg)](https://www.pinecone.io/)
[![LLM Orchestration](https://img.shields.io/badge/orchestrator-LangChain-brightgreen.svg)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

An end-to-end Medical Chatbot utilizing Retrieval-Augmented Generation (RAG). Developed by **Bittu Sharma**, this project leverages state-of-the-art LLMs (GPT-4o), LangChain, Hugging Face embeddings (`all-MiniLM-L6-v2`), and Pinecone serverless vector database to query medical documents and provide accurate, context-aware answers. The application is packaged using Docker and deployed via a fully automated CI/CD pipeline using GitHub Actions on AWS EC2.

---

## 🚀 Key Features

*   **Retrieval-Augmented Generation (RAG)**: Combines LLMs with a custom vector store to answer domain-specific questions accurately without hallucinations.
*   **Vector Database Integration**: Uses Pinecone Serverless Vector Store to index and query document embeddings efficiently.
*   **Interactive Web UI**: A clean, responsive chat interface built using Flask, HTML/CSS, and JavaScript.
*   **Hugging Face Embeddings**: Employs the `all-MiniLM-L6-v2` transformer model for generating 384-dimensional document embeddings.
*   **AWS CI/CD Pipeline**: Automated Docker build, push to AWS ECR, and deployment to AWS EC2 via GitHub Actions.

---

## 🛠️ Tech Stack

*   **Language**: Python 3.10
*   **Framework**: Flask
*   **RAG & Orchestration**: LangChain, LangChain-OpenAI, LangChain-Pinecone
*   **Embeddings**: Hugging Face (Sentence Transformers)
*   **Vector Store**: Pinecone (Serverless)
*   **Deployment**: Docker, AWS (EC2, ECR, IAM), GitHub Actions

---

## 📁 Project Structure

```text
├── .github/workflows/       # GitHub Actions workflow for CI/CD
├── data/                    # Directory for raw source documents (PDFs)
├── research/                # Jupyter Notebooks for experimentation
├── src/
│   ├── __init__.py
│   ├── helper.py            # PDF loader, splitter, and embedding helper functions
│   └── prompt.py            # System prompts and templates
├── static/                  # Static assets (CSS, JS, Images)
├── templates/               # Flask HTML templates (chat.html)
├── app.py                   # Main Flask application
├── store_index.py           # Script to parse PDFs, generate embeddings, and upsert to Pinecone
├── Dockerfile               # Container configuration
├── requirements.txt         # Project dependencies
├── setup.py                 # Package setup script
└── README.md                # Project documentation
```

---

## ⚙️ Installation & Setup

### Prerequisites

*   [Conda](https://docs.conda.io/en/latest/) (recommended) or Python 3.10+ installed
*   An active [Pinecone Account](https://www.pinecone.io/) and API Key
*   An active [OpenAI Account](https://platform.openai.com/) and API Key

### Step 1: Clone the Repository

```bash
git clone https://github.com/bittush8789/Build-a-Complete-Medical-Chatbot-with-LLMs-LangChain-Pinecone-Flask-AWS.git
cd Build-a-Complete-Medical-Chatbot-with-LLMs-LangChain-Pinecone-Flask-AWS
```

### Step 2: Create and Activate Environment

```bash
conda create -n medibot python=3.10 -y
conda activate medibot
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the root directory and add your credentials:

```env
PINECONE_API_KEY="your-pinecone-api-key"
OPENAI_API_KEY="your-openai-api-key"
```

---

## 🏃 Running the Application

### 1. Build and Store Index

Place your reference medical textbooks or PDF documents inside the `data/` directory. Then, run the following script to extract text, generate embeddings, and upsert them to Pinecone:

```bash
python store_index.py
```

### 2. Run the Flask Web Application

Once the database is indexed, start the local development server:

```bash
python app.py
```

Open your browser and navigate to `http://localhost:8080` (or `http://127.0.0.1:8080`) to interact with the medical chatbot.

---

## ☁️ AWS CI/CD Deployment with GitHub Actions

The repository is configured to build and deploy to AWS EC2 continuously upon pushing to the repository.

### Workflow Summary
1.  **Dockerization**: A Docker image is built from the source code.
2.  **AWS ECR**: The Docker image is pushed to Amazon Elastic Container Registry (ECR).
3.  **AWS EC2**: A self-hosted runner on EC2 pulls the latest image from ECR.
4.  **Deployment**: The runner launches the container on the EC2 instance.

### Step-by-Step Configuration

#### 1. Setup AWS IAM Roles & Credentials
Create an IAM user for deployment with the following policies:
*   `AmazonEC2ContainerRegistryFullAccess`
*   `AmazonEC2FullAccess`

#### 2. Create Amazon ECR Registry
*   Create a private repository to host your Docker image.
*   Save your ECR Repository URI (e.g., `315865595366.dkr.ecr.us-east-1.amazonaws.com/medicalbot`).

#### 3. Create and Prepare an EC2 Instance (Ubuntu)
*   Launch an EC2 Instance (Ubuntu 22.04 LTS or similar).
*   Install Docker on your EC2 instance:
    ```bash
    sudo apt-get update -y
    sudo apt-get upgrade -y
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker ubuntu
    newgrp docker
    ```

#### 4. Configure EC2 as a Self-Hosted GitHub Runner
*   Navigate to your GitHub repository -> **Settings** -> **Actions** -> **Runners**.
*   Click **New self-hosted runner**, select **Linux**, and execute the setup commands sequentially inside your EC2 terminal.

#### 5. Configure GitHub Secrets
Add the following secrets under **Settings** -> **Secrets and variables** -> **Actions**:
*   `AWS_ACCESS_KEY_ID`: Your IAM user access key
*   `AWS_SECRET_ACCESS_KEY`: Your IAM user secret key
*   `AWS_DEFAULT_REGION`: e.g., `us-east-1`
*   `ECR_REPO`: ECR repository name (e.g., `medicalbot`)
*   `PINECONE_API_KEY`: Pinecone API Key
*   `OPENAI_API_KEY`: OpenAI API Key

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
