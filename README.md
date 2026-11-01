# 🦖 Kaiju RAG API

Uma API RESTful desenvolvida com FastAPI e LangChain que implementa um pipeline RAG (Retrieval-Augmented Generation) para consultar e gerar respostas baseadas no universo de Kaijus (Toho & Monsterverse). 

O projeto foi construído com foco em boas práticas de engenharia de software, incluindo conteinerização (Docker/Docker Compose), isolamento de dependências (Conda) e ingestão automática de dados em tempo de build.

## 🛠️ Tecnologias Utilizadas

* **Framework API:** [FastAPI](https://fastapi.tiangolo.com/) com Uvicorn
* **Orquestração LLM:** [LangChain](https://www.langchain.com/)
* **Banco de Dados Vetorial:** [ChromaDB](https://www.trychroma.com/)
* **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`) processado localmente
* **LLM (Geração):** Mistral-7B-Instruct-v0.3 via HuggingFace Hub API
* **Infraestrutura:** Docker, Docker Compose e Miniconda

## 📂 Estrutura do Projeto

```text
kaiju/
├── data/
│   ├── list_rag.md          # Base de conhecimento original (Documento fonte)
│   └── processed/           # Banco de dados vetorial ChromaDB (Gerado no build)
├── src/
│   ├── app.py               # Lógica da API FastAPI e rotas
│   └── ingest.py            # Pipeline de extração, chunking e vetorização (ETL)
├── .dockerignore            # Regras de exclusão de ficheiros no build do container
├── .env                     # Variáveis de ambiente (Chave da API Hugging Face)
├── docker-compose.yml       # Orquestração do container
├── Dockerfile               # Receita de infraestrutura do projeto
└── environment.yml          # Dependências do sistema e pacotes Python exportados pelo Conda

```

## 🚀 Como Executar (Plug & Play)

Este projeto foi desenhado para rodar com um único comando, gerando o seu próprio banco de dados vetorial durante a construção da imagem.

### Pré-requisitos

* [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/install/) instalados.
* Uma conta no [Hugging Face](https://huggingface.co/) para obter um Access Token.

### Passo a Passo

1. **Clone o repositório:**
```bash
git clone https://github.com/leolhco/sistema-rag-kaiju.git
cd kaiju-rag-api

```


2. **Configure as Variáveis de Ambiente:**
Crie um ficheiro `.env` na raiz do projeto e adicione o seu token do Hugging Face:
```env
HUGGINGFACEHUB_API_TOKEN=seu_token_aqui

```


3. **Suba a aplicação:**
Execute o comando abaixo. O Docker irá baixar as dependências, rodar o script de ingestão de dados (`src/ingest.py`) para popular o banco vetorial e, em seguida, subir a API.
```bash
docker compose up --build

```



A API estará disponível em `http://localhost:8000`. Você pode aceder à documentação interativa do Swagger em `http://localhost:8000/docs`.

## 🧪 Testando a Rota

**Endpoint:** `POST /query`

Pode testar a API diretamente pelo terminal utilizando o `curl`:

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "Quais são os poderes do King Ghidorah no Monsterverse?"}'

```

**Exemplo de Resposta:**

```json
{
  "pergunta": "Quais são os poderes do King Ghidorah no Monsterverse?",
  "resposta": "King Ghidorah absorbs most energy attacks, has regenerative abilities, brings destructive bioelectric storms, generates hurricane-force winds with its wings, and fires gravity blasts from all three of its heads.",
  "contexto_utilizado": "King Ghidorah is massive, with its three-headed form..."
}

```

## ⚙️ Decisões de Arquitetura

1. **Separação de Preocupações:** O script `ingest.py` atua como um job de ETL isolado, processando os dados brutos e construindo o banco ChromaDB de forma independente da lógica da API (`app.py`).
2. **Embeddings Locais vs Geração Remota:** O modelo `all-MiniLM-L6-v2` roda nativamente no container para garantir buscas vetoriais rápidas e sem latência de rede, enquanto a carga pesada de geração de texto (Mistral-7B) é delegada à API da Hugging Face, permitindo que a aplicação rode em máquinas com recursos computacionais limitados (sem a necessidade de GPUs pesadas no host).
3. **Build Eficiente:** A ingestão do banco vetorial ocorre na etapa de `build` do Dockerfile, garantindo que a imagem final seja totalmente auto-contida e imutável, o que facilita o deploy em ambientes Cloud.

---
