# 🦖 Kaiju RAG API

Uma API RESTful desenvolvida com FastAPI e LangChain que implementa um pipeline RAG (Retrieval-Augmented Generation) para consultar e gerar respostas baseadas no universo de Kaijus (Toho & Monsterverse). 

O projeto foi construído com foco em boas práticas de engenharia de software, incluindo conteinerização, isolamento de dependências via ambientes virtuais e ingestão isolada de dados.

## 🛠️ Tecnologias Utilizadas

- **Framework API:** [FastAPI](https://fastapi.tiangolo.com/) com Uvicorn
- **Orquestração LLM:** [LangChain](https://www.langchain.com/)
- **Banco de Dados Vetorial:** [ChromaDB](https://www.trychroma.com/)
- **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`) processado localmente
- **LLM (Geração):** `qwen/qwen3.8-27b` via [Groq LPU Inference Engine](https://groq.com/)
- **Infraestrutura:** Docker, Docker Compose e Miniconda

## 📂 Estrutura do Projeto

```text
kaiju/
├── data/
│   ├── list_rag.md          # Base de conhecimento original (Documento fonte)
│   └── processed/           # Banco de dados vetorial ChromaDB (Gerado na ingestão)
├── src/
│   ├── app.py               # Lógica da API FastAPI e rotas
│   └── ingestao.py          # Pipeline de extração, chunking e vetorização (ETL)
├── .dockerignore            # Regras de exclusão de arquivos no build do container
├── .env                     # Variáveis de ambiente (Chaves de API)
├── docker-compose.yml       # Orquestração do container
├── Dockerfile               # Receita de infraestrutura do projeto
└── environment.yml          # Dependências do sistema e pacotes Python

```

## 🚀 Como Executar

### Pré-requisitos

* Uma conta na [Groq](https://console.groq.com/) para obter a API Key (Geração de texto ultrarrápida).
* Uma conta no [Hugging Face](https://huggingface.co/) para o Access Token (Download do modelo local de embeddings).

Crie um arquivo `.env` na raiz do projeto e adicione as suas chaves:

```env
HUGGINGFACEHUB_API_TOKEN=seu_token_hf_aqui
GROQ_API_KEY=gsk_sua_chave_groq_aqui

```

### Opção 1: Rodando Localmente 

1. **Crie e ative o ambiente virtual:**

```bash
conda env create -f environment.yml
conda activate kaiju

```

2. **Gere o Banco de Dados Vetorial:**

```bash
python src/ingestao.py

```

3. **Rode a Aplicaçao:**

```bash
python src/app.py

```

### Opção 2: Rodando via Docker

O Docker irá baixar as dependências, rodar o script de ingestão de dados (`src/ingestao.py`) para popular o banco vetorial na fase de build e, em seguida, subir a API.

```bash
docker compose up --build

```

A API estará disponível em `http://localhost:8000`. Acesse a documentação interativa em `http://localhost:8000/docs`.

## 🧪 Testando a Rota

**Endpoint:** `POST /query`

Pode testar a API diretamente pelo terminal utilizando o `curl`:

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "Quem é o maior inimigo do Godzilla?"}'

```

## ⚙️ Decisões de Arquitetura

1. **Separação de Preocupações:** O script `ingestao.py` atua como um job de ETL isolado, processando os dados brutos e construindo o banco ChromaDB de forma independente da lógica de roteamento da API (`app.py`).
2. **Embeddings Locais vs Geração Remota:** O modelo `all-MiniLM-L6-v2` roda nativamente para garantir buscas vetoriais rápidas e sem latência de rede. A carga pesada de inferência foi delegada para a Groq (LPUs), oferecendo latência ultrabaixa sem exigir configurações de hardware avançadas no ambiente host.
3. **Build Eficiente:** A ingestão do banco vetorial ocorre antes ou durante a construção do serviço, garantindo que o sistema suba com os dados já prontos para consulta em memória.