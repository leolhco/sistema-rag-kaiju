FROM continuumio/miniconda3:latest

WORKDIR /app

COPY environment.yml .

RUN conda env create -f environment.yml

COPY src/ ./src/
COPY data/ ./data/

EXPOSE 8000

CMD ["conda", "run", "-n", "kaiju", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
