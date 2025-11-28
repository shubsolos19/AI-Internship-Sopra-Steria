# AI Document Summarizer - Architecture & Diagrams

Visual representation of the project structure, data flow, and components.

---

## 🏗️ Project Architecture

```
┌─────────────────────────────────────────────────────────────┐
│         AI Document Summarizer Project Structure            │
└─────────────────────────────────────────────────────────────┘

ai-document-summarizer/
│
├── 📄 app.py
│   └── Main Streamlit application
│       ├── UI Components
│       ├── PDF extraction
│       ├── Text chunking
│       └── AI summarization
│
├── 📦 requirements.txt
│   └── Dependencies:
│       ├── streamlit (UI framework)
│       ├── transformers (AI models)
│       ├── torch (ML backend)
│       └── PyPDF2 (PDF handling)
│
├── 📚 README.md (Full documentation)
├── ⚡ QUICKSTART.md (5-minute setup)
├── 📖 USAGE_GUIDE.md (How to use)
├── 📊 DIAGRAMS.md (This file)
└── 📋 AI_GUIDE.PDF (Complete guide)
```

---

## 🔄 Data Flow Diagram

```
                    ┌─────────────────────┐
                    │   User Interface    │
                    │   (Streamlit Web)   │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
        ┌───────▼────────┐          ┌────────▼─────────┐
        │  Plain Text    │          │  PDF File        │
        │  Input Area    │          │  Upload Button   │
        └───────┬────────┘          └────────┬─────────┘
                │                            │
                └──────────────┬─────────────┘
                               │
                       ┌───────▼────────┐
                       │ Text Extracted │
                       │ or Uploaded    │
                       └───────┬────────┘
                               │
              ┌────────────────▼────────────────┐
              │    Text Chunking Function       │
              │   (Split into 700-char chunks)  │
              └────────────────┬────────────────┘
                               │
        ┌──────────────────────┴──────────────────────┐
        │                                             │
   ┌────▼─────┐  ┌─────────┐  ┌────────┐  ┌────────┐│
   │ Chunk 1   │  │ Chunk 2 │  │ Chunk 3│  │ Chunk N││
   └────┬─────┘  └────┬────┘  └───┬────┘  └───┬────┘│
        │             │            │           │    │
        └─────────────┼────────────┼───────────┘    │
                      │            │                │
              ┌───────▼────────────▼────────┐       │
              │  t5-small Model Pipeline    │◄──────┘
              │  - Tokenization             │
              │  - Model Processing         │
              │  - Summary Generation       │
              └───────┬────────────┬────────┘
                      │            │
              ┌───────▼──┐  ┌────┬─▼─────┐
              │Summary 1 │  │ ... │Summary N│
              └──────────┘  └──────────────┘
                      │            │
              ┌───────▼────────────▼──────┐
              │ Combine All Summaries     │
              └───────────┬───────────────┘
                          │
                  ┌───────▼──────────┐
                  │ Final Summary    │
                  │ Display to User  │
                  └──────────────────┘
```

---

## 📋 Component Breakdown

### 1. User Interface (Streamlit)
```
┌────────────────────────────────────────┐
│  AI Document Summarizer (Title)        │
├────────────────────────────────────────┤
│                                        │
│  Instruction Text                      │
│                                        │
│  ┌──────────────────────────────────┐  │
│  │ Plain Text Input Label           │  │
│  ├──────────────────────────────────┤  │
│  │ [Text Area for User Input]       │  │
│  │                                  │  │
│  │ Paste or type your text here...  │  │
│  │                                  │  │
│  └──────────────────────────────────┘  │
│                                        │
│  ┌──────────────────────────────────┐  │
│  │ PDF Upload Label                 │  │
│  │ [Upload Button / File Selection] │  │
│  └──────────────────────────────────┘  │
│                                        │
│  ┌──────────────────────────────────┐  │
│  │ [ Summarize Button ]             │  │
│  └──────────────────────────────────┘  │
│                                        │
│  ┌──────────────────────────────────┐  │
│  │ Summary Output Box:              │  │
│  │ [Generated Summary Display]      │  │
│  │                                  │  │
│  └──────────────────────────────────┘  │
│                                        │
└────────────────────────────────────────┘
```

### 2. File Processing Pipeline
```
Input File
    │
    ├─► IF PDF:
    │   └─► PyPDF2.PdfReader()
    │       └─► Extract text from each page
    │           └─► Combine all text
    │
    └─► IF Plain Text:
        └─► Use directly


Combined Text
    │
    └─► chunk_text() function
        │
        ├─► Split by '\n' (newlines)
        ├─► Group into 700-char chunks
        └─► Return list of chunks


Chunks List
    │
    └─► FOR EACH chunk:
        │
        ├─► Tokenize
        ├─► Pass to t5-small model
        ├─► Generate summary
        └─► Append to output


Final Output
    │
    └─► Display in Summary Box
```

### 3. AI Model Processing
```
┌─────────────────────────────────────┐
│      t5-small Model Pipeline        │
└─────────────────────────────────────┘

Input Text Chunk
    │
    └─► Tokenizer
        └─► Convert text to tokens
            └─► [Token1, Token2, ...]
                │
                └─► t5-small Encoder
                    └─► Create embeddings
                        │
                        └─► t5-small Decoder
                            └─► Generate summary tokens
                                │
                                └─► Detokenizer
                                    └─► Convert tokens to text
                                        │
                                        └─► Output Summary
```

---

## 🔧 Function Architecture

```
app.py Structure:

┌──────────────────────────────────────┐
│ Imports & Configuration              │
│ (streamlit, transformers, PyPDF2)   │
└──────────────────────────────────────┘
           │
           ├─► get_summarizer()
           │   └─► Loads t5-small model
           │       └─► Cached for performance
           │
           ├─► extract_text_from_pdf()
           │   └─► Takes: pdf_file
           │   └─► Returns: extracted_text
           │
           ├─► chunk_text()
           │   └─► Takes: text, max_chars
           │   └─► Returns: list of chunks
           │
           └─► Main UI Loop
               └─► File uploader widget
               └─► Text area widget
               └─► Summarize button
               └─► Output display


Function Calls Flow:

User clicks Summarize
    │
    ├─► IF uploaded_file:
    │   └─► extract_text_from_pdf(pdf)
    │       └─► document_text
    │
    ├─► ELSE IF text_input:
    │   └─► use text_input directly
    │
    └─► IF document_text exists:
        └─► chunk_text(document_text)
            └─► For each chunk:
                └─► summarizer(chunk)
                    └─► Append to summary
```

---

## 📊 Data Types & Transformations

```
1. Input Stage:
   ┌────────────┐
   │ Raw Text   │  (string)
   │ -or-       │
   │ PDF File   │  (file object)
   └────┬───────┘
        │

2. Extraction Stage:
   ┌─────────────────┐
   │ Extracted Text  │  (string)
   └────┬────────────┘
        │

3. Chunking Stage:
   ┌──────────────────┐
   │ Chunks List      │  (list of strings)
   │ [chunk1, chunk2] │
   └────┬─────────────┘
        │

4. Processing Stage:
   ┌──────────────────┐
   │ Model Output     │  (list of dicts)
   │ [{summary_text}, │
   │  {summary_text}] │
   └────┬─────────────┘
        │

5. Output Stage:
   ┌──────────────────┐
   │ Final Summary    │  (string)
   │ Combined result  │
   └──────────────────┘
```

---

## 🔌 Dependencies Relationship

```
                    ┌──────────┐
                    │ Python   │
                    │ 3.11.9   │
                    └────┬─────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼────┐    ┌────▼────┐    ┌────▼───────┐
    │Streamlit│    │ PyPDF2  │    │Transformers│
    │ 1.33.0  │    │ 3.0.1   │    │ 4.39.3     │
    └────┬────┘    └────┬────┘    └────┬───────┘
         │              │               │
         │              │          ┌────▼──────┐
         │              │          │ PyTorch   │
         │              │          │ 2.2.2     │
         │              │          └───────────┘
         │              │
    ┌────┴──────────────┴──────────────────────┐
    │                                           │
    │    app.py (Your Application)             │
    │                                           │
    └───────────────────────────────────────────┘
```

---

## ⏱️ Processing Timeline

```
User Action: Click Summarize

T = 0ms
    │
    ├─► Get input (Text or PDF)
    │
T = 10-50ms
    │
    ├─► If PDF: Extract text from all pages
    │
T = 50-100ms
    │
    ├─► Chunk text (split into parts)
    │
T = 100-120ms
    │
    ├─► First chunk to t5-small model
    │
T = 120-500ms (per chunk)
    │
    ├─► Model processes → Summary generated
    ├─► If multiple chunks → repeat
    │
T = 500-3000ms (total, depends on text size)
    │
    ├─► Combine all summaries
    │
T = 3000-3100ms
    │
    └─► Display final summary

TOTAL TIME: 3-10 seconds (depending on text length)
```

---

## 🎯 Key Concepts Visualized

### Text Chunking Example
```
Original Text (2100 characters):
┌──────────────────────────────────────────┐
│ AI is transforming... [2100 chars total] │
└──────────────────────────────────────────┘
                    │
                    ▼
        Chunk into 700-char segments:
    
    ┌─────────────────────┐
    │ Chunk 1 (700 chars) │
    └─────────────────────┘
            │
            └─► Summarize → Summary 1
    
    ┌─────────────────────┐
    │ Chunk 2 (700 chars) │
    └─────────────────────┘
            │
            └─► Summarize → Summary 2
    
    ┌──────────────────┐
    │ Chunk 3 (700 ch) │
    └──────────────────┘
            │
            └─► Summarize → Summary 3
    
                    │
                    ▼
    
    ┌────────────────────────────┐
    │ Final Summary (Summaries   │
    │ 1 + 2 + 3 combined)        │
    └────────────────────────────┘
```

### PDF Processing Example
```
Sample.pdf (25 pages)
    │
    ├─► Page 1 ─► Extract text ─┐
    ├─► Page 2 ─► Extract text ─┼─► Combine
    ├─► Page 3 ─► Extract text ─┤
    ├─► ...                      │
    └─► Page 25 ─► Extract text ─┘
                    │
                    ▼
            Combined Full Text
                    │
                    ▼
            Chunk & Summarize
                    │
                    ▼
            Display Summary
```

---

## 📈 Model Specifications

### t5-small Architecture
```
Input Text
    │
    ├─► Tokenizer (sentencepiece)
    │   └─► 32,000 token vocabulary
    │
    ├─► Encoder (12 layers)
    │   └─► Self-attention mechanism
    │   └─► Feed-forward networks
    │
    ├─► Decoder (12 layers)
    │   └─► Self-attention mechanism
    │   └─► Cross-attention (encoder-decoder)
    │
    └─► Output Layer
        └─► Softmax over vocabulary
            └─► Next token prediction
```

### Model Parameters
```
Parameter         Value
──────────────────────────
Model Size        60M parameters
Vocabulary        32,000 tokens
Max Sequence Len  512 tokens
Hidden Size       512 dimensions
Num Layers        12 (encoder/decoder)
Attention Heads   8
Feed-forward Dim  2048
Download Size     ~900 MB
Memory Required   ~1.5 GB
```

---

## 🚀 Performance Metrics

```
Text Length    Processing Time    Memory Used
────────────────────────────────────────────
100 words      0.5 - 1 sec        ~500 MB
500 words      2 - 3 sec          ~800 MB
1000 words     4 - 6 sec          ~1 GB
2000 words     8 - 12 sec         ~1.2 GB
5000 words     15 - 25 sec        ~1.5 GB
```

---

## 📚 Reference Diagrams

### Streamlit App Lifecycle
```
1. User loads http://localhost:8501
         │
         ▼
2. app.py runs top to bottom
         │
         ▼
3. UI rendered (title, inputs, button)
         │
         ▼
4. Wait for user interaction
         │
         ▼
5. User uploads file or enters text
         │
         ▼
6. User clicks Summarize button
         │
         ▼
7. Python code executes (chunking, AI)
         │
         ▼
8. Summary displayed in UI
         │
         ▼
9. Back to step 4 (wait for interaction)
```

---

## 🎓 Learning Diagram

```
What You Learn:

Streamlit Framework
    ├─► st.title()
    ├─► st.text_area()
    ├─► st.file_uploader()
    ├─► st.button()
    ├─► st.write()
    └─► st.cache_resource()

Natural Language Processing
    ├─► Text extraction
    ├─► Tokenization
    ├─► Text chunking
    └─► Summarization

Python Skills
    ├─► Functions
    ├─► List/string operations
    ├─► File handling
    └─► Error handling

AI/ML Concepts
    ├─► Transformer models
    ├─► Pre-trained models
    ├─► Transfer learning
    └─► Model pipelines
```

---

Enjoy exploring the architecture! 🏗️✨