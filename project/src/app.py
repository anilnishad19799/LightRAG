from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
from langchain.docstore.document import Document
from file_loader import FileLoader
from rag_manager import RAGManager
import asyncio

app = FastAPI(title="Advance RAG API")

# Path to templates
TEMPLATES_DIR = Path(__file__).parent / "templates"
INDEX_HTML = TEMPLATES_DIR / "index.html"

TEXT_DIR = Path.cwd() / "data" / "texts"
TEXT_DIR.mkdir(parents=True, exist_ok=True)

# Initialize RAG manager
rag_manager: RAGManager = RAGManager()


@app.on_event("startup")
async def startup_event():
    """Initialize RAGManager once when FastAPI starts."""
    await rag_manager.get_instance()


@app.get("/")
async def get_index():
    """Serve the index.html page."""
    return FileResponse(INDEX_HTML)


@app.post("/upload_and_index")
async def upload_and_index_file(file: UploadFile = File(...)):
    filename = Path(file.filename).name
    temp_path = Path.cwd() / "uploaded_files" / filename
    temp_path.parent.mkdir(parents=True, exist_ok=True)

    with temp_path.open("wb") as f:
        f.write(file.file.read())

    try:
        loader = FileLoader(str(temp_path))
        docs = loader.load()
    except Exception as e:
        return JSONResponse({"error": f"Failed to load file: {e}"}, status_code=400)

    full_text = "\n\n".join([d.page_content for d in docs])

    try:
        await rag_manager.index_text(full_text)
    except Exception as e:
        return JSONResponse({"error": f"Failed to index text: {e}"}, status_code=500)

    return {
        "status": "saved_and_indexed",
        "raw_path": str(temp_path),
        "text_preview": full_text[:200],
    }


@app.post("/query_rag")
async def query_rag(query: str = Form(...), mode: str = Form("hybrid")):
    result = await rag_manager.query_text(query, mode)
    return {"query": query, "mode": mode, "response": result}
