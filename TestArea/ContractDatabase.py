# database_manager.py
import chromadb
from sentence_transformers import SentenceTransformer
import json
from datetime import datetime


class ContractDatabase:
    """Gestiona la base de datos de contratos"""

    def __init__(self, db_path="./chroma_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name="contratos",
            metadata={"hnsw:space": "cosine"}
        )
        self.embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    def add_contract(self, contract_id, text, metadata):
        """Agrega un contrato a la base de datos"""

        # Genera embedding del texto
        embedding = self.embedder.encode(text).tolist()

        # Almacena en ChromaDB
        self.collection.add(
            ids=[contract_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[{
                **metadata,
                'fecha_ingreso': datetime.now().isoformat()
            }]
        )

    def search_contracts(self, query, n_results=5):
        """Busca contratos relevantes a una consulta"""

        query_embedding = self.embedder.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        return results