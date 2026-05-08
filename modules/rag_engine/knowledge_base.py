import os
import re
from typing import List


class SimpleTextSplitter:
    """纯Python文本分割器，替代 langchain.text_splitter.RecursiveCharacterTextSplitter"""

    def __init__(self, chunk_size=500, chunk_overlap=50, separators=None):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", "。", "，", " "]

    def split_text(self, text: str) -> List[str]:
        chunks = []
        for sep in self.separators:
            if sep in text:
                parts = text.split(sep)
                current = ""
                for part in parts:
                    if len(current) + len(part) + len(sep) > self.chunk_size and current:
                        chunks.append(current.strip())
                        # overlap: keep tail
                        overlap_len = min(self.chunk_overlap, len(current))
                        current = current[-overlap_len:] if overlap_len else ""
                    current += (sep if current else "") + part
                if current.strip():
                    chunks.append(current.strip())
                break
        else:
            # No separator found, just chunk by size
            for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
                chunks.append(text[i:i + self.chunk_size].strip())

        return chunks if chunks else [text.strip()]

    def split_documents(self, documents: List[dict]) -> List[dict]:
        """兼容 langchain Document 风格"""
        all_chunks = []
        for doc in documents:
            texts = self.split_text(doc.get("page_content", doc) if isinstance(doc, dict) else doc)
            for t in texts:
                all_chunks.append({"page_content": t, "metadata": doc.get("metadata", {}) if isinstance(doc, dict) else {}})
        return all_chunks


# 简单文档模拟
class SimpleDocument:
    def __init__(self, page_content="", metadata=None):
        self.page_content = page_content
        self.metadata = metadata or {}

    def __repr__(self):
        return f"SimpleDocument(page_content='{self.page_content[:50]}...')"


class CulturalIPKnowledgeBase:
    """在地文化IP知识库（纯Python版，无torch无langchain依赖）"""

    def __init__(self):
        self.embeddings = None
        self.vector_store = None
        self.documents = []  # 存储原始文档
        self.text_splitter = SimpleTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

    def load_documents(self, file_path: str) -> List[SimpleDocument]:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        raw_doc = SimpleDocument(page_content=text)
        chunks = self.text_splitter.split_text(text)
        return [SimpleDocument(page_content=c) for c in chunks]

    def build_vector_store(self, documents: List[SimpleDocument]):
        """知识库功能需要安装完整依赖才能使用"""
        raise NotImplementedError(
            "知识库（RAG）功能需要额外安装依赖：\n"
            "  pip install langchain-huggingface langchain-community sentence-transformers faiss-cpu\n"
            "当前精简版仅支持 AIGC管线 和 商业决策Agent 两个页面。"
        )

    def save_store(self, path: str):
        pass

    def load_store(self, path: str):
        """跳过加载——精简版不使用RAG"""
        pass

    def search(self, query: str, k: int = 3) -> List[SimpleDocument]:
        raise NotImplementedError("知识库搜索需要完整安装")

    def get_context_with_gene(self, query: str, k: int = 3) -> str:
        return ""
