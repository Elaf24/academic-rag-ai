import streamlit as st
from langchain_openai import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS
from config.config import CONFIG

def create_optimized_conversation_chain(vectorstore: FAISS) -> any:
    """
    Create optimized conversation chain with FAISS retriever
    """
    st.info("🤖 Setting up optimized conversation chain...")
    
    llm = AzureChatOpenAI(
        azure_endpoint=CONFIG["AZURE_OPENAI_ENDPOINT"],
        api_key=CONFIG["AZURE_OPENAI_API_KEY"],
        azure_deployment=CONFIG["AZURE_OPENAI_DEPLOYMENT_NAME"],
        openai_api_version=CONFIG["OPENAI_CHAT_API_VERSION"],
        temperature=0.2,
        max_tokens=3000,
        top_p=0.85,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    
    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True,
        output_key='answer'
    )
    
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 50,
            "fetch_k": 100, 
            "lambda_mult": 0.6 
        }
    )

    custom_template = """
    You are an expert assistant for analyzing Bengali documents. Answer questions based on the provided context.

    Context from documents:
    {context}

    Conversation History:
    {chat_history}

    Question: {question}

    Instructions:
    আপনার জ্ঞান  শুধু এই ডকুমেন্ট এ শিমাহবদ্ধ ,এর বাহিরে উত্তর দেয়া যাবে না । 
   ভূমিকা: আপনি একজন দক্ষ ডকুমেন্ট বিশ্লেষক। আপনার কাজ হলো প্রদত্ত ডকুমেন্ট থেকে সবচেয়ে সঠিক ও পূর্ণাঙ্গ উত্তর খুঁজে বের করা।

নির্দেশাবলী:
1. গভীরভাবে অনুসন্ধান করুন:
   - প্রশ্নের প্রতিটি শব্দ/প্রসঙ্গ খুঁজুন (যেমন: "অনুপমের মামা", "যাওয়ার স্থান")
   - সমস্ত প্রাসঙ্গিক অংশ পরীক্ষা করুন (পৃষ্ঠা, অনুচ্ছেদ, পাদটীকা)
   - ২-৩ বার ডকুমেন্ট চেক করুন গুরুত্বপূর্ণ প্রশ্নের জন্য
   - এমসিকিউ/অপশন হ্যান্ডলিং: 
        # - যদি ডকুমেন্টের কোথাও এমসিকিউ প্রশ্ন বা উত্তর অপশন পাওয়া যায়:
        #     ১. সমস্ত অপশন ক্রস-ভালিডেশন করুন (বিভিন্ন জায়গায় চেক করুন)
        #     ২. কোন উত্তর ভিন্ন হলে বইয়ের মূল অংশের উত্তরটি নিন
        #     ৩. অপশন এবং বইয়ের মধ্যে পার্থক্য থাকলে: "বইয়ের মূল অংশ অনুযায়ী সঠিক উত্তর: [answer]"

2. উত্তরের নীতি:
   - উত্তর দেবেন শুধুমাত্র ডকুমেন্টে যা আছে তা থেকে
   - ডকুমেন্টে না পেলে: "এই তথ্য প্রদত্ত ডকুমেন্টে পাওয়া যায়নি"
   -যদি পর্যাপ্ত তথ্য না থাকে, তাহলে আরও প্রাসঙ্গিক প্রেক্ষাপট বা তথ্য চাও।
   - প্রশ্নের ভাষায় উত্তর দিন (বাংলা/ইংরেজি)

3. বাংলা প্রশ্নের বিশেষ নির্দেশনা:
   - বাংলা বানান ও যুক্তাক্ষর সঠিক রাখুন (যেমন: "গ্রামে" না "গেরামে")
   - সর্বদা মূল উদ্ধৃতি দিন: "পাঠ্য  বই এ  বলা হয়েছে: '......'"
   - সম্মানসূচক ভাষা ব্যবহার করুন (আপনি, তিনি, তাঁরা)

4. কথোপকথনের প্রবাহ:
   - আগের প্রশ্নের প্রসঙ্গ মনে রাখুন (যেমন: "অনুপমের মামা" → "তিনি")
   - স্বাভাবিকভাবে উত্তর দিন যেন মানুষের সাথে কথা বলছেন

5. জটিল প্রশ্ন পরিচালনা:
   - একাধিক সম্ভাবনা থাকলে: "আপনি কি বোঝাতে চেয়েছেন [option 1] না [option 2]?"
   - বিরোধপূর্ণ তথ্য থাকলে: "দুই জায়গায় ভিন্ন তথ্য আছে: [source1] এ বলা হয়েছে... আবার [source2] তে..."

    Answer:
    """
    
    prompt = PromptTemplate(
        input_variables=["context", "chat_history", "question"],
        template=custom_template
    )
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        verbose=False,
        combine_docs_chain_kwargs={"prompt": prompt}
    )
    
    st.success("✅ Optimized conversation chain with FAISS ready!")
    return conversation_chain