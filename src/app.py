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

if __name__ == "__main__":
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)
