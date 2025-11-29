# AI Document Summarizer using Streamlit, PyPDF2, HuggingFace Transformers
# Student-friendly | t5-small model | Python 3.11.9

import streamlit as st
from transformers import pipeline
import PyPDF2

# Title
st.set_page_config(page_title="AI Document Summarizer", layout="centered")

# Custom CSS for aesthetic UI
st.markdown("""
    <style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    /* Main App Background - Gradient */
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #2d2b42 100%);
        color: #ffffff;
    }
    
    /* Title Styling */
    h1 {
        color: #ffffff;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Glassmorphism for Containers */
    .stTextArea, .stFileUploader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 10px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Input Fields Text Color */
    .stTextArea textarea {
        color: #ffffff !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #ff8a00 0%, #e52e71 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-size: 16px;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(229, 46, 113, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(229, 46, 113, 0.6);
    }
    
    /* Success/Info Messages */
    .stAlert {
        background-color: rgba(255, 255, 255, 0.1);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    ::-webkit-scrollbar-track {
        background: #1e1e2f; 
    }
    ::-webkit-scrollbar-thumb {
        background: #555; 
        border-radius: 5px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #888; 
    }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ AI Document Summarizer")
st.markdown("<p style='text-align: center; color: #b0b0c0;'>Summarize plain text or PDF documents instantly using AI.</p>", unsafe_allow_html=True)

# Load the easiest HuggingFace summarizer (t5-small)
@st.cache_resource
def get_summarizer():
    return pipeline("summarization", model="t5-small")

summarizer = get_summarizer()

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

# Function to chunk long text (t5-small works best with <= 400 tokens)
def chunk_text(text, max_chars=700):
    # Split text into chunks of max_chars length
    chunks = []
    paragraphs = text.split('\n')
    temp = ""
    for para in paragraphs:
        if len(temp) + len(para) + 1 < max_chars:
            temp += para + "\n"
        else:
            chunks.append(temp.strip())
            temp = para + "\n"
    if temp.strip():
        chunks.append(temp.strip())
    return [c for c in chunks if c.strip()]

# Streamlit UI
uploaded_file = st.file_uploader("Upload PDF document (optional)", type=["pdf"])
text_input = st.text_area("Or paste/type your plain text here (optional)", height=150)
summarize_button = st.button("Summarize")

if summarize_button:
    document_text = ""
    if uploaded_file:
        document_text = extract_text_from_pdf(uploaded_file)
    elif text_input.strip():
        document_text = text_input
    else:
        st.info("Please upload a PDF or enter some text above.")
    
    if document_text.strip():
        loading_placeholder = st.empty()
        loading_placeholder.write("🍳👨‍🍳 please wait... 🥘🍲")
        chunks = chunk_text(document_text)
        summary = ""
        for chunk in chunks:
            try:
                result = summarizer(chunk, max_length=70, min_length=20, do_sample=False)
                summary += result[0]['summary_text'].strip() + "\n"
            except Exception as e:
                summary += "[Error in summarization]\n"
        
        loading_placeholder.empty()
        st.markdown("### Summary:")
        st.text_area("", summary.strip(), height=140)
    else:
        st.warning("No text found to summarize.")
