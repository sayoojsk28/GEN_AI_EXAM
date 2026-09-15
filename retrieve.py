from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS


VECTORSTORE_PATH = "vectorstore"


def load_vectorstore():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001"
    )

    vectorstore = FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore


if __name__ == "__main__":
    load_dotenv()

    vectorstore = load_vectorstore()

    question = "What is the reverse question that logarithms help us answer?"

    results = vectorstore.similarity_search(
        question,
        k=3
    )

    print(f"Retrieved {len(results)} chunks:\n")

    for i, document in enumerate(results):
        print(f"--- Retrieved Chunk {i + 1} ---")
        print(document.page_content)
        print()