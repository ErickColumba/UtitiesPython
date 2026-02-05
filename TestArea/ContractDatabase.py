# ContractDatabase.py
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

    def _sanitize_metadata(self, metadata):
        """
        Convierte los metadatos a tipos aceptados por ChromaDB.
        ChromaDB solo acepta: str, int, float, bool (NO None, NO listas vacías)
        """
        sanitized = {}

        for key, value in metadata.items():
            # SKIP valores None
            if value is None:
                continue

            # Valores simples aceptados
            if isinstance(value, (str, int, float, bool)):
                # Solo agrega strings no vacíos
                if isinstance(value, str) and value.strip():
                    sanitized[key] = value
                elif not isinstance(value, str):
                    sanitized[key] = value

            # Convierte listas a JSON string (solo si no están vacías)
            elif isinstance(value, list):
                if len(value) > 0:
                    sanitized[key] = json.dumps(value, ensure_ascii=False)

            # Convierte diccionarios a JSON string (solo si no están vacíos)
            elif isinstance(value, dict):
                if len(value) > 0:
                    sanitized[key] = json.dumps(value, ensure_ascii=False)

            # Otros tipos: convierte a string
            else:
                str_value = str(value)
                if str_value.strip():
                    sanitized[key] = str_value

        return sanitized

    def add_contract(self, contract_id, text, metadata):
        """Agrega un contrato a la base de datos"""

        # Genera embedding del texto
        embedding = self.embedder.encode(text).tolist()

        # Sanitiza los metadatos (elimina None y listas vacías)
        clean_metadata = self._sanitize_metadata(metadata)

        # Agrega fecha de ingreso (siempre presente)
        clean_metadata['fecha_ingreso'] = datetime.now().isoformat()

        # Agrega el texto original como metadato para búsquedas
        clean_metadata['texto_length'] = len(text)

        # Si no hay metadatos útiles, agrega al menos uno
        if len(clean_metadata) == 2:  # Solo fecha_ingreso y texto_length
            clean_metadata['sin_datos_extraidos'] = True

        print(f"\n📊 Metadatos a guardar: {clean_metadata}")

        # Almacena en ChromaDB
        self.collection.add(
            ids=[contract_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[clean_metadata]
        )

        print(f"✓ Contrato almacenado con ID: {contract_id}")

    def search_contracts(self, query, n_results=5):
        """Busca contratos relevantes a una consulta"""

        query_embedding = self.embedder.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        # Deserializa los metadatos que son JSON strings
        if results['metadatas']:
            for metadata_list in results['metadatas']:
                for metadata in metadata_list:
                    for key, value in list(metadata.items()):
                        if isinstance(value, str) and (value.startswith('[') or value.startswith('{')):
                            # Intenta parsear como JSON
                            try:
                                metadata[key] = json.loads(value)
                            except:
                                pass

        return results

    def get_contract(self, contract_id):
        """Obtiene un contrato específico por ID"""
        try:
            result = self.collection.get(
                ids=[contract_id],
                include=['documents', 'metadatas']
            )

            if result['ids']:
                # Deserializa metadatos
                metadata = result['metadatas'][0]
                for key, value in list(metadata.items()):
                    if isinstance(value, str) and (value.startswith('[') or value.startswith('{')):
                        try:
                            metadata[key] = json.loads(value)
                        except:
                            pass

                return {
                    'id': result['ids'][0],
                    'text': result['documents'][0],
                    'metadata': metadata
                }
            return None
        except Exception as e:
            print(f"Error obteniendo contrato: {e}")
            return None

    def list_all_contracts(self):
        """Lista todos los contratos almacenados"""
        try:
            result = self.collection.get(
                include=['documents', 'metadatas']
            )

            contracts = []
            for i, contract_id in enumerate(result['ids']):
                metadata = result['metadatas'][i]

                # Deserializa metadatos JSON
                for key, value in list(metadata.items()):
                    if isinstance(value, str) and (value.startswith('[') or value.startswith('{')):
                        try:
                            metadata[key] = json.loads(value)
                        except:
                            pass

                contracts.append({
                    'id': contract_id,
                    'metadata': metadata,
                    'text_preview': result['documents'][i][:200] + '...'
                })

            return contracts
        except Exception as e:
            print(f"Error listando contratos: {e}")
            return []

    def delete_contract(self, contract_id):
        """Elimina un contrato de la base de datos"""
        try:
            self.collection.delete(ids=[contract_id])
            print(f"✓ Contrato {contract_id} eliminado")
            return True
        except Exception as e:
            print(f"Error eliminando contrato: {e}")
            return False

    def count_contracts(self):
        """Cuenta total de contratos en la BD"""
        try:
            result = self.collection.count()
            return result
        except Exception as e:
            print(f"Error contando contratos: {e}")
            return 0