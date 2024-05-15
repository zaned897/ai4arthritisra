#%%
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.chat_models import ChatOllama as Ollama
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from pathlib import Path
from time import time

def get_pdf_files(path: str):
    return list(path.glob("*.pdf"))

def load_vector_store(base_dir:str, knowledge_base_files: List[Path]) -> FAISS:
    embeds_dir = base_dir / "embeds"
    embeds = OllamaEmbeddings(model='nomic-embed-text')
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=300,
        is_separator_regex=True,
        separators=[r"\n\n"]
    )
    database = []
    for file in knowledge_base_files:
        embed_base = embeds_dir / file.stem
        if embed_base.exists():
            print(f"Loading vector store from {embed_base}")
            vector_store = FAISS.load_local(
                base_dir=embed_base,
                embeddings=embeds,
                allow_dangerous_deserialization=True
                )
            database.append(vector_store)
        else:
            print(f"Creating vector store from {file}")
            loader = PyPDFLoader(file)
            documents = loader.load()
            chunks = splitter.split_documents(documents)
            vector_store = FAISS.from_documents(chunks, embeds)
            vector_store.save_local(embed_base)
            database.append(vector_store)
    for db in database[1:]:
        database[0].merge_from(db)
    return database[0]

knowledge_bas_path = Path("docs/resources")
embeds_path = knowledge_bas_path / "embeds"

knowledge_base_files = get_pdf_files(knowledge_bas_path)
vector_store = load_vector_store(embeds_path, knowledge_base_files)

inference_time = time()
llm = Ollama(model="mistral:latest")
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(), 
)

response = qa.run("Give me a very brief summary about the Phase 1 in the classification criteria topic")
print(response)
print(f"Inference time: {time() - inference_time:.2f} seconds")