# LLMOps Best Practices & Implementation

Managing LLM applications in production requires specialized monitoring and versioning strategies.

## 1. Prompt Versioning
We use **LangSmith** or **MLflow Prompt Engineering** UI to version prompts.
- Avoid hardcoding prompts in `app.py`.
- Use a `prompts/` directory or a remote registry.

## 2. RAG Evaluation (RAGAS)
Evaluate the performance of the RAG pipeline using:
- **Faithfulness**: Is the answer derived from the context?
- **Answer Relevance**: Does the answer address the question?
- **Context Precision**: Is the retrieved context relevant?

## 3. Tracing & Latency
Integrated with **LangSmith**:
```python
from langsmith import Client
client = Client()
# Tracing is automatic when LANGCHAIN_TRACING_V2=true
```

## 4. Hallucination Detection
- Use a "Critic" model to verify the output against the retrieved documents.
- Implement confidence thresholds for Pinecone similarity scores.

## 5. Cost Monitoring
- Track token usage per request using LangChain's `get_openai_callback`.
- Export usage metrics to Prometheus for Grafana dashboarding.

## 6. Model Fallback Strategy
```python
try:
    response = openai_model.invoke(query)
except Exception:
    response = anthropic_model.invoke(query) # Fallback to secondary provider
```
