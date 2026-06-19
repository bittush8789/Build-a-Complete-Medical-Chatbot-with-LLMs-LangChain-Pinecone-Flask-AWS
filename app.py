# Import necessary modules for the Flask web application, LangChain pipeline, and Prometheus monitoring
from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Initialize the Flask application
app = Flask(__name__)

# Load environment variables from the local .env file (used in local development)
load_dotenv()

# Retrieve API keys from system environment variables
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Ensure the keys are set back into environment variables so LangChain integrations can automatically pick them up
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Define Prometheus Metrics for tracking request volumes and processing latencies
REQUEST_COUNT = Counter(
    'medical_chatbot_requests_total',
    'Total number of requests to the chatbot',
    ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'medical_chatbot_request_latency_seconds',
    'Request latency in seconds',
    ['endpoint']
)

# Download the HuggingFace word embeddings model (all-MiniLM-L6-v2) for querying similarity
embeddings = download_hugging_face_embeddings()

# Define the target Pinecone index name
index_name = "medical-chatbot" 

# Load the existing vector database index from Pinecone using the embedding model
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

# Convert the vector database into a retriever object returning the top 3 most similar document chunks
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

# Initialize the OpenAI Chat Model (GPT-4o) for generating user answers
chatModel = ChatOpenAI(model="gpt-4o")

# Create the conversational prompt template using the predefined system template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# Combine the LLM and system prompt template into a Q&A document processing chain
question_answer_chain = create_stuff_documents_chain(chatModel, prompt)

# Construct the final Retrieval-Augmented Generation (RAG) chain by binding the retriever and Q&A chain
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


# Web Route: Serves the front-end chat interface (HTML page)
@app.route("/")
def index():
    # Increment Prometheus request counter
    REQUEST_COUNT.labels(method='GET', endpoint='/', http_status='200').inc()
    return render_template('chat.html')


# Web Route: Accepts user messages and returns the generated LLM response
@app.route("/get", methods=["GET", "POST"])
def chat():
    start_time = time.time()
    try:
        # Extract user message from post request body
        msg = request.form["msg"]
        input = msg
        print(input)
        
        # Invoke the LangChain RAG pipeline with user's question
        response = rag_chain.invoke({"input": msg})
        print("Response : ", response["answer"])
        
        # Log successful metrics
        REQUEST_COUNT.labels(method=request.method, endpoint='/get', http_status='200').inc()
        REQUEST_LATENCY.labels(endpoint='/get').observe(time.time() - start_time)
        return str(response["answer"])
        
    except Exception as e:
        # Increment request counter with 500 status on failure
        REQUEST_COUNT.labels(method=request.method, endpoint='/get', http_status='500').inc()
        raise e


# Web Route: Health Check endpoint used by Kubernetes Liveness/Readiness probes and Docker HEALTHCHECK
@app.route("/health")
def health():
    # Check if necessary Pinecone and embedding components are active and loaded
    if docsearch and embeddings:
        return jsonify({"status": "healthy", "timestamp": time.time()}), 200
    return jsonify({"status": "unhealthy"}), 500


# Web Route: Prometheus metrics scraping endpoint
@app.route("/metrics")
def metrics():
    # Generate and return latest Prometheus metrics
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


# Application runner
if __name__ == '__main__':
    # Start the Flask web application on port 8080
    app.run(host="0.0.0.0", port= 8080, debug= True)
