import streamlit as st
from langchain.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
import os
import time
from config.config import CONFIG
from typing import List
from langchain.schema import Document

def create_faiss_vectorstore(documents: List[Document]) -> FAISS:
    """
    Create FAISS vector store
    """
    if not documents:
        raise ValueError("No documents to process")
    
    st.info("🔄 Initializing Azure OpenAI embeddings for FAISS...")
    
    embeddings = AzureOpenAIEmbeddings(
        azure_endpoint=CONFIG["AZURE_OPENAI_ENDPOINT"],
        api_key=CONFIG["AZURE_OPENAI_API_KEY"],
        azure_deployment=CONFIG["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"],
        openai_api_version=CONFIG["OPENAI_EMBEDDING_API_VERSION"],
        chunk_size=50
    )
    
    try:
        test_embedding = embeddings.embed_query("Test sentence for Bengali embedding বাংলা পরীক্ষা")
        embedding_dim = len(test_embedding)
        st.success(f"✅ Embeddings working! Dimension: {embedding_dim}")
    except Exception as e:
        st.error(f"❌ Embedding test failed: {str(e)}")
        raise e
    
    total_docs = len(documents)
    st.info(f"📊 Creating FAISS index for {total_docs} documents...")
    
    batch_size = 100
    
    if total_docs <= batch_size:
        vectorstore = FAISS.from_documents(documents, embeddings)
        st.success(f"✅ FAISS vector store created with {total_docs} documents!")
    else:
        st.info(f"Processing large dataset in batches of {batch_size}...")
        first_batch = documents[:batch_size]
        vectorstore = FAISS.from_documents(first_batch, embeddings)
        
        for i in range(batch_size, total_docs, batch_size):
            batch_end = min(i + batch_size, total_docs)
            batch = documents[i:batch_end]
            
            progress = batch_end / total_docs
            st.progress(progress)
            st.info(f"Processing batch: {batch_end}/{total_docs}")
            
            try:
                batch_vectorstore = FAISS.from_documents(batch, embeddings)
                vectorstore.merge_from(batch_vectorstore)
                time.sleep(0.1)
            except Exception as e:
                st.warning(f"Failed to process batch {i//batch_size + 1}: {str(e)}")
                continue
        
        st.success(f"✅ FAISS vector store created with {total_docs} documents!")
    
    try:
        test_results = vectorstore.similarity_search("test বাংলা", k=5)
        st.success(f"✅ FAISS retrieval test successful! Found {len(test_results)} results")
        
        with st.expander("🔍 FAISS Retrieval Test Results"):
            for i, doc in enumerate(test_results):
                st.write(f"**Result {i+1}:** {doc.page_content[:150]}...")
                st.write(f"*Source: {doc.metadata.get('source', 'Unknown')}*")
                st.write("---")
    except Exception as e:
        st.warning(f"⚠️ FAISS retrieval test failed: {str(e)}")
    
    try:
        vectorstore.save_local("faiss_index")
        st.info("💾 FAISS index saved locally")
    except Exception as e:
        st.warning(f"Could not save FAISS index: {str(e)}")
    
    return vectorstore

def load_existing_faiss_index() -> FAISS:
    """
    Load existing FAISS index if available
    """
    try:
        if os.path.exists("faiss_index"):
            embeddings = AzureOpenAIEmbeddings(
                azure_endpoint=CONFIG["AZURE_OPENAI_ENDPOINT"],
                api_key=CONFIG["AZURE_OPENAI_API_KEY"],
                azure_deployment=CONFIG["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"],
                openai_api_version=CONFIG["OPENAI_EMBEDDING_API_VERSION"],
            )
            vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
            st.info("📂 Loaded existing FAISS index")
            return vectorstore
    except Exception as e:
        st.warning(f"Could not load existing FAISS index: {str(e)}")
    return None