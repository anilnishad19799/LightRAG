# rag_manager.py
from rag_setup import initialize_rag
from lightrag import LightRAG, QueryParam
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["NEO4J_URI"] = os.getenv("NEO4J_URI")
os.environ["NEO4J_USERNAME"] = os.getenv("NEO4J_USERNAME")
os.environ["NEO4J_PASSWORD"] = os.getenv("NEO4J_PASSWORD")


class RAGManager:
    """Singleton manager for a single RAG instance reused for indexing and querying."""

    _instance = None

    def __init__(
        self,
        graph_storage="Neo4JStorage",
        vector_storage="FaissVectorDBStorage",
        chunk_token_size=1500,
        chunk_overlap_token_size=200,
    ):
        if RAGManager._instance is not None:
            raise Exception("RAGManager is a singleton! Use get_instance()")

        self.rag = None
        self.graph_storage = graph_storage
        self.vector_storage = vector_storage
        self.chunk_token_size = chunk_token_size
        self.chunk_overlap_token_size = chunk_overlap_token_size

        RAGManager._instance = self

    @classmethod
    async def get_instance(
        cls,
        graph_storage="Neo4JStorage",
        vector_storage="ChromaVectorDBStorage",
        chunk_token_size=1500,
        chunk_overlap_token_size=200,
    ):
        if cls._instance is None:
            cls(
                graph_storage=graph_storage,
                vector_storage=vector_storage,
                chunk_token_size=chunk_token_size,
                chunk_overlap_token_size=chunk_overlap_token_size,
            )
        if cls._instance.rag is None:
            # pass storage types to initialize_rag
            cls._instance.rag = await initialize_rag(
                graph_storage=cls._instance.graph_storage,
                vector_storage=cls._instance.vector_storage,
                chunk_token_size=cls._instance.chunk_token_size,
                chunk_overlap_token_size=cls._instance.chunk_overlap_token_size,
            )
        return cls._instance

    async def index_text(self, text: str):
        await self.rag.ainsert(text)
        await self.rag.finalize_storages()

    async def query_text(self, user_query: str, mode: str = "hybrid"):
        try:
            return await self.rag.aquery(user_query, param=QueryParam(mode=mode))
        except Exception as e:
            return {"error": str(e)}
