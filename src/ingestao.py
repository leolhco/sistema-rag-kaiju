import os
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Carrega o documento base de conhecimento
with open('data/list_rag.md', 'r', encoding='utf-8') as arquivo:
    dados = arquivo.read()

# 2. Fatiamento semântico: divide o texto respeitando as seções do Markdown
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
]
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
md_header_splits = markdown_splitter.split_text(dados)

# 3. Fatiamento físico: garante que os blocos não excedam o limite de tokens do modelo
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks_finais = text_splitter.split_documents(md_header_splits)

# 4. Geração de Embeddings
modelo_embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 5. Persistência
banco_vetorial = Chroma.from_documents(
    documents=chunks_finais,
    embedding=modelo_embedding,
    persist_directory="data/processed"
)

print("Ingestão concluída com sucesso! Banco salvo na pasta data/processed")