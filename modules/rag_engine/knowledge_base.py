import os
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

class CulturalIPKnowledgeBase:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        self.vector_store = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", "。", "，", " "]
        )
    
    def load_documents(self, file_path: str) -> List[Document]:
        loader = TextLoader(file_path, encoding='utf-8')
        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)
        return chunks
    
    def build_vector_store(self, documents: List[Document]):
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        return self.vector_store
    
    def save_store(self, path: str):
        if self.vector_store:
            self.vector_store.save_local(path)
    
    def load_store(self, path: str):
        self.vector_store = FAISS.load_local(
            path, 
            self.embeddings, 
            allow_dangerous_deserialization=True
        )
    
    def search(self, query: str, k: int = 3) -> List[Document]:
        if not self.vector_store:
            raise ValueError("请先构建或加载向量存储")
        docs = self.vector_store.similarity_search(query, k=k)
        return docs
    
    def get_context_with_gene(self, query: str, k: int = 3) -> str:
        docs = self.search(query, k)
        context_parts = []
        for i, doc in enumerate(docs):
            gene_marker = f"[白泽造物·在地文化基因片段 {i+1}]"
            context_parts.append(f"{gene_marker}\n{doc.page_content}")
        return "\n\n".join(context_parts)