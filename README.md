# LightRAG 🚀

**LightRAG** is an advanced Retrieval-Augmented Generation (RAG) framework that allows indexing and querying PDF or TXT documents using a combination of vector and graph databases.

## Features
- Upload PDF or TXT documents and automatically extract text.
- Hybrid retrieval using vector database (Faiss/Chroma/Milvus) and graph database (Neo4j) storage.
- Optional reranking with Cohere or custom models.
- Web UI for querying documents easily.
- Fully Dockerized for easy deployment.

## Project Structure
```
LightRAG/
├── notebook/
│   ├── neo4j.ipynb          Graph database exploration example
│   └── sample_demo.ipynb    Simple LightRAG usage demo
├── project/
│   ├── rag_storage/         Storage for indexed documents
│   ├── data/                Original PDFs/TXT and extracted text
│   │   ├── raw/             Original PDFs
│   │   └── texts/           Extracted text files
│   ├── src/
│   │   ├── templates/
│   │   │   └── index.html   Web interface
│   │   ├── app.py           FastAPI application
│   │   ├── .env             Environment variables
│   │   ├── Dockerfile       Docker image for API
│   │   ├── file_loader.py   File loader and text extraction
│   │   ├── rag_manager.py   RAG manager for indexing/querying
│   │   ├── rag_setup.py     LightRAG initialization
│   │   └── requirements.txt Python dependencies
│   ├── uploaded_files/      Uploaded files for indexing
│   └── docker-compose.yml   Docker Compose configuration
```

## 1. Prerequisites
- Python 3.10+
- Docker & Docker Compose 
- Neo4j instance for graph storage
- OpenAI API key for embeddings and LLM
- Cohere API key (optional) for reranking

## 2. Installation (Local Python)
- Clone the repository:
- git clone https://github.com/anilnishad19799/LightRAG.git
- cd LightRAG/project/src

## 3. Create and activate a virtual environment:
- python -m venv venv
- source venv/bin/activate   # Linux/Mac
- venv\Scripts\activate      # Windows

## 4. Install dependencies:
- pip install -r requirements.txt

`This step is important to run code`
## 5. Neo4j Setup using Docker
- Open Docker Desktop (Windows) or terminal (Linux/Ubuntu) and run:
- change below LOCAL_PATH with your PATH and then run below command 
- `docker run --publish=7474:7474 --publish=7687:7687 --volume="YOUR_LOCAL_PATH:/data" neo4j`
- Go to [http://localhost:7474/](http://localhost:7474/), login with username `neo4j` and password `neo4j`, then change the password.  
- Use this new password in your `.env` file as `NEO4J_PASSWORD`.  
- In `.env`, set `NEO4J_URI=bolt://neo4j:7687` and `NEO4J_USERNAME=neo4j`.  
- Give the same `YOUR_LOCAL_PATH` as Neo4j volume path in Docker Compose to persist data.  

   
## 6. Make `.env` file at src/ folder lcoation and add environment variables in `.env`:
- NEO4J_URI=bolt://localhost:7687
- NEO4J_USERNAME=neo4j
- NEO4J_PASSWORD=your_password
- RERANK_MODEL=cohere_model
- RERANK_BINDING_API_KEY=cohere_api_key
- RERANK_BINDING_HOST=cohere_host_api

## Running the Application (Local) 
- cd LightRAG/project/src
- uvicorn app:app --host 0.0.0.0 --port 8000
- Open your browser at http://127.0.0.1:8000 to upload PDFs/TXT files and query documents.

## Running with Docker
- Build and start containers:
- cd LightRAG/project
- docker-compose build
- docker-compose up
- Access the app at http://127.0.0.1:8000

## File Loading & Indexing
- `file_loader.py` handles PDF/TXT loading and text extraction.
- Extracted text is saved in `data/texts/`.
- Raw PDFs are saved in `data/raw/`.

## RAG Manager
- `rag_manager.py` initializes a singleton RAG instance.
- Supports hybrid retrieval: vector + graph.
- Use `index_text()` to index documents and `query_text()` to perform queries.

## LightRAG Setup
- `rag_setup.py` initializes LightRAG with vector storage, graph storage, and optional reranking.
- Works with OpenAI embeddings and optional Cohere reranker.

## Notes
- `.env` should never be pushed to GitHub.
- Use `uploaded_files/` to store documents for indexing.
- Docker ensures environment consistency and isolates dependencies.

## References
- [LangChain](https://www.langchain.com/)
- [Neo4j](https://neo4j.com/)
- [OpenAI](https://openai.com/)

## Contributing
- Fork the repo, make changes, and open a pull request.
- Ensure large database files (`.db`) are never committed.

## License
MIT License
