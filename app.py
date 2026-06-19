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


app = Flask(__name__)


load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


# Prometheus Metrics Definition
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


embeddings = download_hugging_face_embeddings()

index_name = "medical-chatbot" 
# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)




retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

chatModel = ChatOpenAI(model="gpt-4o")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)



@app.route("/")
def index():
    REQUEST_COUNT.labels(method='GET', endpoint='/', http_status='200').inc()
    return render_template('chat.html')



@app.route("/get", methods=["GET", "POST"])
def chat():
    start_time = time.time()
    try:
        msg = request.form["msg"]
        input = msg
        print(input)
        response = rag_chain.invoke({"input": msg})
        print("Response : ", response["answer"])
        REQUEST_COUNT.labels(method=request.method, endpoint='/get', http_status='200').inc()
        REQUEST_LATENCY.labels(endpoint='/get').observe(time.time() - start_time)
        return str(response["answer"])
    except Exception as e:
        REQUEST_COUNT.labels(method=request.method, endpoint='/get', http_status='500').inc()
        raise e



@app.route("/health")
def health():
    if docsearch and embeddings:
        return jsonify({"status": "healthy", "timestamp": time.time()}), 200
    return jsonify({"status": "unhealthy"}), 500



@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}



if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)

