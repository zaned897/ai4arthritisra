# src/query.py

from langchain.chains import create_retrieval_chain
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate
from .pdf_utils import load_pdfs_from_directory

def setup_chain(llm_model: str, embed_model: str, pdf_directory: str):
    """Setup the LangChain and FAISS chain."""
    print("Loading PDF documents from directory...")
    pdf_docs = load_pdfs_from_directory(pdf_directory)
    print(f"Loaded {len(pdf_docs)} documents.")
    
    print("Creating embeddings...")
    embeds = OllamaEmbeddings(model=embed_model)
    vectors = FAISS.from_texts([pdf.content for pdf in pdf_docs], embeds)
    print("Embeddings created.")
    
    print("Initializing LLM...")
    llm = Ollama(model=llm_model)
    
    print("Setting up RetrievalQA chain...")
    retriever = vectors.as_retriever()
    
    system_prompt = (
        "Use the given context to answer the question. "
        "If you don't know the answer, say you don't know. "
        "Use three sentence maximum and keep the answer concise. "
        "Context: {context}"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(retriever, question_answer_chain)
    print("Chain setup complete.")
    return chain

def interact_with_pdfs(chain, query: str) -> str:
    """Interact with the PDFs using the chain."""
    print(f"Query received: {query}")
    response = chain.invoke({"input": query})
    print(f"Response generated: {response}")
    return response
