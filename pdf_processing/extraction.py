import streamlit as st
from pdf2image import convert_from_bytes
from PIL import Image
import fitz  # PyMuPDF
import re
from .preprocessing import preprocess_image_advanced
from .bengali_text_fixes import clean_bengali_text, apply_bengali_fixes
import pytesseract

def clean_extracted_text(text: str) -> str:
    """
    Advanced text cleaning for Bengali OCR output using external fixes
    """
    # Use the comprehensive Bengali text cleaning function
    return clean_bengali_text(text)

def enhanced_ocr_extraction(pdf_bytes: bytes, pdf_name: str) -> str:
    """
    Enhanced OCR extraction with multiple strategies for Bengali text
    """
    text = ""
    
    try:
        # Convert to high-quality images
        images = convert_from_bytes(
            pdf_bytes, 
            dpi=400,
            fmt='png',
            thread_count=2
        )
        
        total_pages = len(images)
        st.info(f"Processing {total_pages} pages from {pdf_name}")
        
        progress_bar = st.progress(0)
        page_texts = []
        
        ocr_configs = [
            r'--oem 3 --psm 6 -l ben',
        ]
        
        for i, image in enumerate(images):
            progress_bar.progress((i + 1) / total_pages)
            
            # Preprocess image for better OCR
            processed_image = preprocess_image_advanced(image)
            
            page_text = ""
            best_result = ""
            max_length = 0
            
            # Try multiple OCR configurations
            for config in ocr_configs:
                try:
                    result = pytesseract.image_to_string(processed_image, config=config)
                    if len(result.strip()) > max_length:
                        max_length = len(result.strip())
                        best_result = result
                except:
                    continue
            
            # Fallback to original image if needed
            if max_length < 50:
                try:
                    best_result = pytesseract.image_to_string(
                        image, config=r'--oem 3 --psm 6 -l ben'
                    )
                except:
                    best_result = ""
            
            # Apply Bengali fixes immediately after OCR for each page
            best_result = apply_bengali_fixes(best_result)
            page_texts.append(best_result)
            
            if i % 2 == 0 or i == total_pages - 1:
                st.info(f"Processed page {i + 1}/{total_pages}")
        
        progress_bar.empty()
        
        text = "\n\n".join(page_texts)
        return clean_extracted_text(text)
        
    except Exception as e:
        st.error(f"OCR extraction failed for {pdf_name}: {str(e)}")
        return ""

def extract_direct_text_advanced(pdf_bytes: bytes) -> str:
    """
    Advanced direct text extraction with metadata preservation and Bengali fixes
    """
    text = ""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_text = page.get_text("text")
            
            if len(page_text.strip()) < 50:
                continue
                
            # Apply Bengali fixes to directly extracted text as well
            page_text = apply_bengali_fixes(page_text)
            
            text += f"\n--- Page {page_num + 1} ---\n"
            text += page_text + "\n"
        
        doc.close()
        return clean_extracted_text(text)
        
    except Exception as e:
        st.warning(f"Direct text extraction failed: {str(e)}")
        return ""