# 🤖 RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built with **Python, LangChain, Google Gemini, Gemini Embeddings, FAISS, PyPDF, and Streamlit**.

The chatbot retrieves relevant information from a provided PDF document and uses Google Gemini to generate answers grounded only in the retrieved document context.

---

## 📌 Project Overview

This project demonstrates a complete **Retrieval-Augmented Generation (RAG) pipeline**.

Instead of asking the language model to answer using its general knowledge, the system first searches a knowledge base for relevant information. The retrieved content is then provided to the LLM as context so that the generated answer is based on the supplied document.

### Knowledge Source

The current knowledge base is:

**`data/logarithms_intuitive_guide.pdf`**

The document is an intuition-first guide to logarithms, including concepts such as:

* Exponents
* Logarithms
* Reverse questions
* Repeated multiplication
* Bacteria doubling example
* Relationship between exponents and logarithms

---

## 🧠 RAG Architecture

```text
                    ┌──────────────────────┐
                    │     PDF Document     │
                    │  Knowledge Source    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Document Loading    │
                    │      PyPDF            │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Text Chunking      │
                    │ RecursiveCharacter    │
                    │    Text Splitter     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Embeddings       │
                    │ Gemini Embeddings     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    FAISS Vector      │
                    │       Store          │
                    └──────────┬───────────┘
                               │
                         User Question
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Similarity Search    │
                    │    Top-K Retrieval   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Relevant Context     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Google Gemini     │
                    │       LLM            │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Grounded Answer    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Streamlit Chat UI    │
                    └──────────────────────┘
```

---

## 🛠️ Technologies Used

| Technology        | Purpose                                  |
| ----------------- | ---------------------------------------- |
| Python            | Core programming language                |
| LangChain         | RAG pipeline and LLM integration         |
| Google Gemini     | Large Language Model                     |
| Gemini Embeddings | Convert text into vector representations |
| FAISS             | Vector database / similarity search      |
| PyPDF             | PDF document loading                     |
| Streamlit         | Chatbot user interface                   |
| python-dotenv     | Environment variable management          |

---

## 📂 Project Structure

```text
rag-chatbot/
│
├── data/
│   └── logarithms_intuitive_guide.pdf
│
├── app.py
├── ingest.py
├── retrieve.py
├── rag.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### Generated Locally

```text
vectorstore/
```

The `vectorstore/` directory is generated automatically when the ingestion script is executed.

It is intentionally **not included in the GitHub repository** and is excluded through `.gitignore`.

---

## ⚙️ How the System Works

### 1. Document Ingestion

`ingest.py` loads the PDF using `PyPDFLoader`.

The extracted text is divided into smaller chunks using:

```text
RecursiveCharacterTextSplitter
```

Configuration:

```text
Chunk size: 500
Chunk overlap: 50
```

---

### 2. Embedding Generation

Each text chunk is converted into a numerical vector using:

```text
Gemini Embeddings
```

These vectors allow the system to compare the semantic similarity between a user's question and the document content.

---

### 3. Vector Storage

The generated embeddings are stored in a **FAISS vector store**.

FAISS is used to efficiently perform similarity searches over the document embeddings.

---

### 4. Retrieval

When a user asks a question, the question is converted into an embedding and compared against the stored document vectors.

The system retrieves the **top 3 most relevant chunks**.

---

### 5. Generation

The retrieved chunks are passed to **Google Gemini** as context.

The chatbot is instructed to:

* Answer only using the provided context
* Avoid outside knowledge
* Avoid making up information
* Clearly state when the answer cannot be found in the document

For questions outside the document, the chatbot responds:

> I couldn't find the answer in the provided document.

---

### 6. Chat Interface

The final chatbot is implemented using **Streamlit**.

Users can enter questions through a conversational chat interface and receive generated answers.

---

# 🚀 Setup and Installation

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd rag-chatbot
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\activate
```

---

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 4. Configure Google API Key

Create a file named:

```text
.env
```

in the project root.

Add:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

A template is provided in:

```text
.env.example
```

### Important

Do **not** commit your actual API key to GitHub.

The `.env` file is excluded using `.gitignore`.

---

# 📄 Document Ingestion

Before running the chatbot for the first time, create the FAISS vector store from the PDF.

Run:

```powershell
python ingest.py
```

Expected output:

```text
Total chunks: 10
Embeddings created successfully.
FAISS vector store saved successfully.
```

This creates:

```text
vectorstore/
├── index.faiss
└── index.pkl
```

The generated vector store remains local and is not committed to GitHub.

---

# 🔎 Testing Retrieval

The retrieval component can be tested independently using:

```powershell
python retrieve.py
```

This performs a similarity search and displays the most relevant document chunks for the test question.

Example question:

```text
What is the reverse question that logarithms help us answer?
```

The system retrieves relevant sections from the logarithms document.

---

# 💬 Running the Chatbot

Start the Streamlit application:

```powershell
streamlit run app.py
```

Streamlit will start the local web application.

The chatbot can then be used through the browser interface.

---

# 🧪 Testing

The chatbot was tested using both **document-related** and **out-of-document** questions.

### Document-related Questions

Examples:

```text
What is a logarithm?
```

```text
What question does a logarithm help us answer?
```

```text
If we have 16 bacteria after repeated doubling, how many doublings occurred?
```

```text
Explain the relationship between exponents and logarithms using the bacteria example.
```

These questions are answered using information retrieved from the PDF.

---

### Out-of-Document Questions

Examples:

```text
Who invented the computer?
```

```text
What is the capital of France?
```

Since these topics are not covered by the supplied document, the chatbot is designed to respond:

```text
I couldn't find the answer in the provided document.
```

This helps reduce unsupported or hallucinated answers.

---

# 🔐 Security

API credentials are managed through environment variables.

The following files and directories are excluded from Git:

```text
.env
venv/
vectorstore/
__pycache__/
*.pyc
```

The actual Google API key should **never** be committed to the repository.

Use `.env.example` as a template for configuring the application.

---

# 🎥 Demo

A demonstration video shows:

1. Starting the Streamlit application
2. Asking questions related to the PDF
3. Receiving grounded answers
4. Testing questions outside the document
5. Verifying the chatbot's fallback response

---


# 🧩 Main Files

### `ingest.py`

Loads the PDF, splits the document into chunks, generates embeddings, and creates the FAISS vector store.

### `retrieve.py`

Tests semantic similarity retrieval independently from the generation step.

### `rag.py`

Implements the core RAG pipeline:

```text
Question
   ↓
Similarity Search
   ↓
Relevant Chunks
   ↓
Context
   ↓
Google Gemini
   ↓
Answer
```

### `app.py`

Provides the Streamlit-based conversational chatbot interface.

---

# 🔄 Replacing the Knowledge Document

The chatbot can be adapted to other PDF-based knowledge sources.

To use another document:

1. Replace the PDF inside:

```text
data/
```

2. Update the PDF path in `ingest.py` if the filename changes.

3. Run:

```powershell
python ingest.py
```

4. Start the application:

```powershell
streamlit run app.py
```

The new document will then become the chatbot's knowledge base.

---

# 🎯 Project Goal

The goal of this project is to demonstrate how a Large Language Model can be combined with a custom knowledge base using **Retrieval-Augmented Generation**.

The system separates knowledge retrieval from language generation, allowing the chatbot to provide answers based on the supplied document rather than relying entirely on the model's general knowledge.

---



Built as part of a Generative AI / RAG practical assignment.
