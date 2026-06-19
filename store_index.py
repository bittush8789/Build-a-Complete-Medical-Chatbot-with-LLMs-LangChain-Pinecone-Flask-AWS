# Import dotenv to load secret keys
from dotenv import load_dotenv
import os
# Import helper functions from custom src directory
from src.helper import load_pdf_file, filter_to_minimal_docs, text_split, download_hugging_face_embeddings
# Import Pinecone client SDK components
from pinecone import Pinecone
from pinecone import ServerlessSpec 
# Import LangChain-Pinecone vector database connector
from langchain_pinecone import PineconeVectorStore

# Load environment configuration variables
load_dotenv()

# Extract keys
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Propagate environment settings
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# 1. Load PDFs from the source folder
extracted_data = load_pdf_file(data='data/')

# 2. Filter document metadata to keep only source names to minimize payload sizing
filter_data = filter_to_minimal_docs(extracted_data)

# 3. Segment source texts into split chunks
text_chunks = text_split(filter_data)

# 4. Download word embedding vectorizer
embeddings = download_hugging_face_embeddings()

# 5. Initialize base Pinecone SDK client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Define vector index name inside database
index_name = "medical-chatbot"

# 6. Check if target index exists; if not, create it as a Serverless AWS Index with 384 dimensions
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

# Retrieve reference connection to target index
index = pc.Index(index_name)

# 7. Convert text chunks to vector embeddings and upsert them to Pinecone database
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings, 
)