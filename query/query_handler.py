import streamlit as st
from templates.htmlTemplates import user_template, bot_template

def handle_user_query(user_question: str):
 
    if not st.session_state.conversation:
        st.error("❌ Please process documents first!")
        return
    
    try:
        with st.spinner("🔍 Searching"):
            processed_query = user_question.strip()
            response = st.session_state.conversation({
                'question': processed_query
            })
            st.session_state.chat_history = response['chat_history']
        
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        
        if 'source_documents' in response and response['source_documents']:
            with st.expander(f"📚 Source References ({len(response['source_documents'])} chunks found)"):
                sources_by_file = {}
                for doc in response['source_documents']:
                    source_file = doc.metadata.get('source', 'Unknown')
                    if source_file not in sources_by_file:
                        sources_by_file[source_file] = []
                    sources_by_file[source_file].append(doc)
                
                for source_file, docs in sources_by_file.items():
                    st.write(f"**📄 From: {source_file}** ({len(docs)} chunks)")
                    for i, doc in enumerate(docs):
                        st.write(f"*Chunk {i+1}:*")
                        st.write(doc.page_content[:400] + ("..." if len(doc.page_content) > 400 else ""))
                        st.write("---")
        
    except Exception as e:
        st.error(f"❌ Query processing failed: {str(e)}")
        st.error("Please try rephrasing your question or reprocess the documents.")
        st.exception(e)