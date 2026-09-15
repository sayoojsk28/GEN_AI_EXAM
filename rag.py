from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)
from langchain_community.vectorstores import FAISS


VECTORSTORE_PATH = "vectorstore"


def load_vectorstore():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001"
    )

    return FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )


def generate_answer(question, vectorstore):
    results = vectorstore.similarity_search(
        question,
        k=3
    )

    context = "\n\n".join(
        document.page_content
        for document in results
    )

    prompt = f"""
You are a helpful RAG chatbot.

Answer the user's question ONLY using the context provided below.

If the answer cannot be found in the context, say:
"I couldn't find the answer in the provided document."

Do not use outside knowledge.
Do not make up information.

Context:
{context}

Question:
{question}

Answer:
"""

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    response = llm.invoke(prompt)

    return response.content, results


if __name__ == "__main__":
    load_dotenv()

    vectorstore = load_vectorstore()

    question = input("Ask a question: ")

    answer, results = generate_answer(
        question,
        vectorstore
    )

    print("\nAnswer:")
    print(answer)

    print("\nRetrieved Sources:")
    for i, document in enumerate(results):
        print(f"\n--- Source {i + 1} ---")
        print(document.page_content[:300])