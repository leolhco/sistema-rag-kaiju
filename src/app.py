import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

app = FastAPI(title="RAG API - Kaiju Context")

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    huggingfacehub_api_token=hf_token,
    temperature=0.1, 
    max_new_tokens=512 
)

modelo_embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

banco_vetorial = Chroma(
    persist_directory="./data/processed",
    embedding_function=modelo_embedding
)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def query_rag(request: QueryRequest):
    try:
        query_embedding = modelo_embedding.embed_query(request.query)

        resultados = banco_vetorial.similarity_search_by_vector(
            embedding=query_embedding, 
            k=1
        )
        contexto_limpo = resultados[0].page_content

        prompt = (
            f"You are an AI assistant. Answer based ONLY on this document:\n"
            f"{contexto_limpo}\n\n"
            f"User: {request.query}\nAssistant:"
        )

        resposta = llm.invoke(prompt)

        return {
            "pergunta": request.query,
            "resposta": resposta.strip(),
            "contexto_utilizado": contexto_limpo
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)
