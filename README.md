# 🚀 FAISS-Powered Bengali PDF Chat

## 📖 Table of Contents
- [Project Overview](#project-overview)
- [Installation](#installation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Q&A of 10-Minute School](#qa-of-10-minute-school)
- [Screenshot Demo](#screenshot-demo)
- [Video Demo](#video-demo)

## 🌍 Project Overview
A Retrieval-Augmented Generation (RAG) system for querying Bengali PDFs (e.g., "HSC26-Bangla1st-Paper-1-9.pdf" containing "অপরিচিতা"). Upload documents, ask questions, and get answers with source references and evaluation metrics (groundedness, relevance) via a Streamlit UI. Powered by LangChain, FAISS, and Azure OpenAI.

## 📦 Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/bengali-pdf-chat.git
   cd bengali-pdf-chat
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   **requirements.txt**:
   ```
   streamlit==1.38.0
   python-dotenv==1.0.1
   PyPDF2==3.0.1
   pdf2image==1.17.0
   Pillow==10.4.0
   pytesseract==0.3.13
   langchain==0.2.16
   langchain-openai==0.1.23
   faiss-cpu==1.8.0
   PyMuPDF==1.24.10
   opencv-python==4.10.0.84
   numpy==1.26.4
   nltk==3.9.1
   scikit-learn==1.5.2
   ```

4. **Install Tesseract OCR**:
   - **Ubuntu**: `sudo apt-get install tesseract-ocr tesseract-ocr-ben`
   - **Windows**: Download from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki) and add to PATH.
   - **Mac**: `brew install tesseract`
   - Ensure the Bengali language model (`ben`) is installed.

5. **Download NLTK Data**:
   ```python
   import nltk
   nltk.download('punkt')
   ```

## 🔧 Configuration
Create a `.env` file in the project root:
```
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_DEPLOYMENT_NAME=your_chat_deployment_name
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME=your_embedding_deployment_name
OPENAI_API_VERSION=2023-05-15
OPENAI_EMBEDDING_API_VERSION=2023-05-15
```
Update `config/config.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()

CONFIG = {
    "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT"),
    "AZURE_OPENAI_API_KEY": os.getenv("AZURE_OPENAI_API_KEY"),
    "AZURE_OPENAI_DEPLOYMENT_NAME": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME": os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"),
    "OPENAI_API_VERSION": os.getenv("OPENAI_API_VERSION"),
    "OPENAI_EMBEDDING_API_VERSION": os.getenv("OPENAI_EMBEDDING_API_VERSION")
}
```

## 📂 Project Structure
```
bengali-pdf-chat/
├── config/
│   └── config.py               # Azure OpenAI configuration
├── conversation/
│   └── conversation_chain.py   # ConversationalRetrievalChain setup
├── evaluation/
│   ├── __init__.py
│   └── evaluation.py          # Groundedness and relevance metrics
├── pdf_processing/
│   ├── extraction.py          # Text and OCR extraction
│   └── chunking.py            # Text chunking
├── query/
│   ├── __init__.py
│   └── query_handler.py       # Query processing and RAG evaluation
├── templates/
│   └── htmlTemplates.py       # Streamlit HTML/CSS templates
├── vectorstore/
│   └── faiss_vectorstore.py   # FAISS vector store setup
├── main.py                    # Streamlit app
├── requirements.txt           # Dependencies
├── .env                       # Environment variables
└── faiss_index/               # FAISS index storage
```

## ❓ Q&A of 10-Minute School
This section provides a quick guide inspired by 10-Minute School’s concise Q&A format, explaining the project’s core functionality for Bengali PDF querying. Answers are highlighted with different background colors for clarity.

- **Q: What does this project do?**  
  <div style="background-color: #e6f3ff; padding: 10px; border-radius: 5px;">  
  A: It lets you upload Bengali PDFs, ask questions (e.g., "What is Anupam’s father’s occupation in অপরিচিতা?"), and get answers with source references and evaluation metrics (groundedness, relevance) using a Streamlit interface.  
  </div>

- **Q: How does it process PDFs?**  
  <div style="background-color: #e6ffe6; padding: 10px; border-radius: 5px;">  
  A: It extracts text using PyMuPDF for text-based PDFs or Tesseract OCR for image-based PDFs, chunks the text into 1000-character segments with 150-character overlap, and indexes them in a FAISS vector store.  
  </div>

- **Q: How are answers generated?**  
  <div style="background-color: #fff7e6; padding: 10px; border-radius: 5px;">  
  A: The system uses LangChain’s `ConversationalRetrievalChain` with Azure OpenAI’s chat model (e.g., `gpt-3.5-turbo`) to generate answers based on retrieved document chunks.  
  </div>

- **Q: What are the evaluation metrics?**  
  <div style="background-color: #ffe6e6; padding: 10px; border-radius: 5px;">  
  A: Groundedness (trigram overlap between answer and chunks) and relevance (cosine similarity between query and chunks) measure answer quality and chunk accuracy.  
  </div>

- **Q: Why are retrieved chunks sometimes incorrect?**  
  <div style="background-color: #f0e6ff; padding: 10px; border-radius: 5px;">  
  A: Large chunks or retriever caching may cause irrelevant retrieval. Use `chunk_size=1000`, `search_type="similarity"`, and reinitialize the retriever per query to fix this.  
  </div>

- **Q: How do I check if it’s working?**  
  <div style="background-color: #e6fff0; padding: 10px; border-radius: 5px;">  
  A: Upload a PDF, ask a specific question, and verify that "Source References" shows relevant chunks and "RAG Evaluation Results" displays non-zero metrics.  
  </div>

## 📸 Screenshot Demo
Below are placeholder images demonstrating the Streamlit UI (to be replaced with actual screenshots, sized equally at 600x400 pixels for consistency):

| **Upload Interface** | **Query Interface** | **Source References** | **Evaluation Metrics** |
|----------------------|---------------------|-----------------------|-----------------------|
| ![Upload Interface](https://via.placeholder.com/600x400.png?text=Upload+Interface) | ![Query Interface](https://via.placeholder.com/600x400.png?text=Query+Interface) | ![Source References](https://via.placeholder.com/600x400.png?text=Source+References) | ![Evaluation Metrics](https://via.placeholder.com/600x400.png?text=Evaluation+Metrics) |

- **Upload Interface**: Shows the sidebar for uploading PDFs and selecting processing options.
- **Query Interface**: Displays the input field for asking questions (e.g., "What is Anupam’s father’s occupation?").
- **Source References**: Shows retrieved document chunks for the query.
- **Evaluation Metrics**: Displays groundedness and relevance scores.

## 🎥 Video Demo
A video walkthrough is available to demonstrate the project in action.  
[Watch the Video Demo](https://via.placeholder.com/video.mp4)  
*Note*: Replace the placeholder link with an actual video hosted on YouTube, Vimeo, or a similar platform.

---

**Built with ❤️ for Bengali language processing!**
