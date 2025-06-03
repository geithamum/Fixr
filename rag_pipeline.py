from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from typing import List, Any
import logging
from config import CHUNK_SIZE, CHUNK_OVERLAP, TOP_K_CHUNKS

logger = logging.getLogger(__name__)

def build_vector_store(documents: List[str]) -> FAISS:
    """
    Build a FAISS vector store from the input documents.
    
    Args:
        documents: List of text documents to process
        
    Returns:
        FAISS vector store containing the document chunks
    """
    if not documents:
        logger.warning("No documents provided to build vector store")
        return None
        
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        
        chunks = []
        for doc in documents:
            chunks.extend(splitter.split_text(doc))
            
        if not chunks:
            logger.warning("No chunks created from documents")
            return None
            
        logger.info("Created %d chunks from %d documents", len(chunks), len(documents))
        
        embedder = OpenAIEmbeddings()
        vector_store = FAISS.from_texts(chunks, embedder)
        return vector_store
        
    except Exception as e:
        logger.error("Failed to build vector store: %s", str(e))
        raise

def retrieve_chunks(vector_store: FAISS, query: str, k: int = TOP_K_CHUNKS) -> List[Any]:
    """
    Retrieve the most relevant chunks for a query from the vector store.
    
    Args:
        vector_store: FAISS vector store to search
        query: Search query
        k: Number of chunks to retrieve
        
    Returns:
        List of relevant document chunks
    """
    if not vector_store:
        logger.error("No vector store provided")
        return []
        
    try:
        chunks = vector_store.similarity_search(query, k=k)
        logger.info("Retrieved %d chunks for query", len(chunks))
        return chunks
        
    except Exception as e:
        logger.error("Failed to retrieve chunks: %s", str(e))
        return []
