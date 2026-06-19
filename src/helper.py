# Import Document loader modules from LangChain community
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
# Import text splitter utility
from langchain.text_splitter import RecursiveCharacterTextSplitter
# Import HuggingFace Embeddings interface
from langchain.embeddings import HuggingFaceEmbeddings
# Import type hints
from typing import List
# Import standard Document schema
from langchain.schema import Document


# Extract Data From all PDF Files in the target directory
def load_pdf_file(data):
    # Initialize the DirectoryLoader targeting only .pdf files using PyPDFLoader
    loader= DirectoryLoader(data,
                            glob="*.pdf",
                            loader_cls=PyPDFLoader)

    # Load and parse the documents
    documents=loader.load()

    return documents



# Filter the metadata of each document to reduce size and payload overhead before indexing
def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    """
    Given a list of Document objects, return a new list of Document objects
    containing only 'source' in metadata and the original page_content.
    """
    minimal_docs: List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source")
        # Strip other default file metadata leaving only 'source'
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": src}
            )
        )
    return minimal_docs



# Split the loaded document data into smaller text chunks for vector indexing
def text_split(extracted_data):
    # Setup chunk size of 500 characters and small overlap of 20 characters to preserve boundaries
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks=text_splitter.split_documents(extracted_data)
    return text_chunks



# Download the Sentence Transformers word embeddings model from HuggingFace
def download_hugging_face_embeddings():
    # Instantiate HuggingFaceEmbeddings model (all-MiniLM-L6-v2) returning 384 dimensions
    embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    return embeddings