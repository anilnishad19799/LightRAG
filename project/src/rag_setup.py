import os
from lightrag.lightrag import LightRAG
from lightrag.llm.openai import gpt_4o_mini_complete, openai_embed
from lightrag.kg.shared_storage import initialize_pipeline_status
from dotenv import load_dotenv
from functools import partial
from lightrag.rerank import cohere_rerank


load_dotenv()
os.environ["NEO4J_URI"] = os.getenv("NEO4J_URI")
os.environ["NEO4J_USERNAME"] = os.getenv("NEO4J_USERNAME")
os.environ["NEO4J_PASSWORD"] = os.getenv("NEO4J_PASSWORD")

WORKING_DIR = "./rag_storage"
if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

rerank_model_func = partial(
    cohere_rerank,
    model=os.getenv("RERANK_MODEL"),
    api_key=os.getenv("RERANK_BINDING_API_KEY"),
    base_url=os.getenv("RERANK_BINDING_HOST"),
)


async def initialize_rag(
    graph_storage=None,
    vector_storage=None,
    chunk_token_size=1000,
    chunk_overlap_token_size=200,
):
    """
    Initialize LightRAG with vector and optional graph storage
    """
    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=gpt_4o_mini_complete,
        embedding_func=openai_embed,
        graph_storage=graph_storage,  # e.g., "Neo4JStorage" or None
        vector_storage=vector_storage,
        chunk_token_size=chunk_token_size,
        chunk_overlap_token_size=chunk_overlap_token_size,
        rerank_model_func=rerank_model_func,
    )
    
    await rag.initialize_storages()
    await initialize_pipeline_status()
    return rag
