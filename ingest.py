from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS


PDF_PATH = "data/logarithms_intuitive_guide.pdf"
VECTORSTORE_PATH = "vectorstore"


def load_and_split_document():
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    return splitter.split_documents(documents)


def create_vectorstore(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001"
    )

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    vectorstore.save_local(VECTORSTORE_PATH)

    return vectorstore


if __name__ == "__main__":
    load_dotenv()

    chunks = load_and_split_document()

    print(f"Total chunks: {len(chunks)}")

    vectorstore = create_vectorstore(chunks)

    print("Embeddings created successfully.")
    print("FAISS vector store saved successfully.")