from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import hashlib
from typing import List

def smart_text_chunking(text: str, source_name: str) -> List[Document]:
    """
    Intelligent text chunking optimized for Bengali content
    """
    if not text.strip():
        return []
    
    separators = [
        "\n--- Page", "\n\n", "\n", "।।", "।", 
        ".", "?", "!", ";", ":", ",", " "
    ]
    
    chunk_size =   1500
    chunk_overlap = 300 #300
    
    text_splitter = RecursiveCharacterTextSplitter(
        separators=separators,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    
    chunks = text_splitter.split_text(text)
    documents = []
    
    for i, chunk in enumerate(chunks):
        cleaned_chunk = chunk.strip()
        if len(cleaned_chunk) < 40:
            continue
        
        chunk_id = hashlib.md5(f"{source_name}_{i}_{cleaned_chunk[:100]}".encode()).hexdigest()
        
        doc = Document(
            page_content=cleaned_chunk,
            metadata={
                "source": source_name,
                "chunk_id": chunk_id,
                "chunk_index": i,
                "chunk_length": len(cleaned_chunk)
            }
        )
        documents.append(doc)
    
    return documents