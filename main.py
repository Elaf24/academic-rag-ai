import streamlit as st
import os
import shutil
from pdf_processing.extraction import extract_direct_text_advanced, enhanced_ocr_extraction
from pdf_processing.chunking import smart_text_chunking
from vectorstore.faiss_vectorstore import create_faiss_vectorstore, load_existing_faiss_index
from conversation.conversation_chain import create_optimized_conversation_chain
from query.query_handler import handle_user_query
from templates.htmlTemplates import css, bot_template, user_template
from config.config import CONFIG

def process_pdf_intelligently(pdf_file, processing_method: str) -> str:
    """
    Intelligent PDF processing with fallback strategies
    """
    pdf_name = pdf_file.name
    pdf_file.seek(0)
    pdf_bytes = pdf_file.read()
    
    st.info(f"🔍 Analyzing {pdf_name}...")
    
    direct_text = extract_direct_text_advanced(pdf_bytes)
    
    if processing_method == "Direct + OCR Fallback":
        if len(direct_text.strip()) > 200:
            st.success(f"✅ Using direct text extraction for {pdf_name}")
            return direct_text
        else:
            st.info(f"📸 Falling back to OCR for {pdf_name}")
            return enhanced_ocr_extraction(pdf_bytes, pdf_name)
    else:
        st.info(f"📸 Using OCR extraction for {pdf_name}")
        return enhanced_ocr_extraction(pdf_bytes, pdf_name)

def main():
    st.set_page_config(
        page_title="FAISS Bengali PDF Chat", 
        page_icon="🚀",
        layout="centered"
    )
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "processed_docs" not in st.session_state:
        st.session_state.processed_docs = 0
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None

    st.header("🚀 10MS ChatBot")
    st.markdown("*Ultra-fast retrieval for large Bengali documents*")

    with st.container():
        input_col, button_col = st.columns([0.85, 0.15])
        with input_col:
            user_question = st.text_input(
                "প্রশ্ন করুন / Ask your question:",
                key="user_input",
                placeholder="এই ডকুমেন্টে কী আছে?",
                label_visibility="collapsed"
            )
        with button_col:
            if st.button("🔍 Search", type="primary", use_container_width=True):
                if user_question:
                    if st.session_state.conversation:
                        handle_user_query(user_question)
                        st.rerun()
                    else:
                        st.warning("Please process documents first!")
                else:
                    st.warning("Please enter a question")

    if st.session_state.chat_history:
        st.divider()
        for message in reversed(st.session_state.chat_history):
            if message.type == "human":
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

    with st.sidebar:
        st.subheader("🔧 System Status")
        
        config_items = [
            ("Azure Endpoint", CONFIG["AZURE_OPENAI_ENDPOINT"]),
            ("API Key", CONFIG["AZURE_OPENAI_API_KEY"]),
            ("Chat Model", CONFIG["AZURE_OPENAI_DEPLOYMENT_NAME"]),
            ("Embedding Model", CONFIG["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"])
        ]
        
        all_configured = True
        for name, value in config_items:
            status = "✅" if value else "❌"
            if not value:
                all_configured = False
            st.write(f"{status} {name}")
        
        if st.session_state.processed_docs > 0:
            st.write(f"📊 Processed: {st.session_state.processed_docs} documents")
            st.write("🗃️ Vector Store: FAISS")
        
        if os.path.exists("faiss_index") and not st.session_state.conversation:
            if st.button("📂 Load Existing Index", help="Load previously created FAISS index"):
                try:
                    vectorstore = load_existing_faiss_index()
                    if vectorstore:
                        st.session_state.vectorstore = vectorstore
                        st.session_state.conversation = create_optimized_conversation_chain(vectorstore)
                        st.success("✅ Existing FAISS index loaded!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Failed to load existing index: {str(e)}")
        
        st.divider()
        
        st.subheader("📁 Document Upload")
        
        pdf_files = st.file_uploader(
            "Upload Bengali PDF files",
            accept_multiple_files=True,
            type=['pdf'],
            help="Upload Bengali PDFs (text or image-based)"
        )
        
        if pdf_files:
            total_size = sum(len(pdf.getvalue()) for pdf in pdf_files) / 1024 / 1024
            st.info(f"📄 {len(pdf_files)} files ({total_size:.1f} MB total)")
            
            for pdf in pdf_files:
                size_mb = len(pdf.getvalue()) / 1024 / 1024
                st.write(f"• {pdf.name} ({size_mb:.1f} MB)")
        
        st.subheader("⚙️ Processing Options")
        
        processing_method = st.selectbox(
            label="",
            options=["OCR Only", "Direct + OCR Fallback"],
            help="Direct: Try text extraction first. OCR: Process as images."
        )
        
        process_button_disabled = not pdf_files or not all_configured
        
        if st.button("🚀 START PROCESS", type="primary", disabled=process_button_disabled):
            if not all_configured:
                st.error("❌ Please configure all Azure OpenAI settings!")
                return
            
            st.session_state.conversation = None
            st.session_state.chat_history = []
            st.session_state.processed_docs = 0
            st.session_state.vectorstore = None
            
            if os.path.exists("faiss_index"):
                try:
                    shutil.rmtree("faiss_index")
                    st.info("🗑️ Cleared existing FAISS index")
                except:
                    pass
            
            with st.spinner("🔄 Processing "):
                try:
                    all_documents = []
                    
                    for pdf_file in pdf_files:
                        st.info(f"📖 Processing: {pdf_file.name}")
                        
                        extracted_text = process_pdf_intelligently(pdf_file, processing_method)
                        st.write(extracted_text,height=500)
                        
                        if not extracted_text.strip():
                            st.warning(f"⚠️ No text extracted from {pdf_file.name}")
                            continue
                        
                        documents = smart_text_chunking(extracted_text, pdf_file.name)
                        all_documents.extend(documents)
                    
                    if not all_documents:
                        st.error("❌ No processable content found!")
                        return
                    
                    vectorstore = create_faiss_vectorstore(all_documents)
                    st.session_state.vectorstore = vectorstore
                    st.session_state.conversation = create_optimized_conversation_chain(vectorstore)
                    st.session_state.processed_docs = len(pdf_files)
                    
                    st.success("🎉 Processing complete!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Processing failed: {str(e)}")
        
        with st.expander("❓ Usage Guide"):
            st.markdown("""
            **How to use:**
            1. Upload PDF files
            2. Click "Process with FAISS"
            3. Ask questions about the documents
            
            **Example Questions:**
            - এই ডকুমেন্টের মূল বিষয় কী?
            - What are the main points?
            - Summarize the findings
            """)

if __name__ == '__main__':
    main()