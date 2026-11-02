import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

app = FastAPI(title="RAG API - Kaiju Context")

# 1. Configuração do LLM 
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="qwen/qwen3.8-27b", 
    temperature=0.1,
    max_tokens=500
)

# 2. Embeddings locais
modelo_embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 3. Conexão com o banco vetorial populado pelo ingestao.py
banco_vetorial = Chroma(
    persist_directory="data/processed",
    embedding_function=modelo_embedding
)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def query_rag(request: QueryRequest):
    try:
        # Extrai a representação vetorial matemática da pergunta
        query_embedding = modelo_embedding.embed_query(request.query)
        
        # Busca os 5 fragmentos mais relevantes no banco
        resultados = banco_vetorial.similarity_search_by_vector(
            embedding=query_embedding, 
            k=5 
        )
        
        # Consolida o contexto recuperado em um único bloco de texto
        contexto_limpo = "\n\n".join([doc.page_content for doc in resultados])

        # Constrói o prompt garantindo a restrição de escopo e alinhamento de idioma
        prompt = (
            f"You are an AI assistant. Answer based ONLY on the document below.\n"
            f"IMPORTANT: You MUST reply in the exact same language as the user's query (e.g., if the user asks in Portuguese, answer in Portuguese).\n\n"
            f"Document:\n{contexto_limpo}\n\n"
            f"User: {request.query}\nAssistant:"
        )

        # Injeção do contexto no LLM via Groq
        resposta = llm.invoke(prompt)

        return {
            "pergunta": request.query,
            "resposta": resposta.content.strip(),
            "contexto_utilizado": contexto_limpo
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)