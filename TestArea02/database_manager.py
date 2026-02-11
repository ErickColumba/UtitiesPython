import chromadb
from sentence_transformers import SentenceTransformer
import json
from datetime import datetime


class DatabaseManager:
    """
    RESPONSABILIDAD: Guardar y buscar contratos en ChromaDB

    ¿Qué hace?
    - Guarda contratos con embeddings vectoriales
    - Busca contratos por similitud semántica
    - Gestiona metadata estructurada
    """

    def __init__(self, db_path="./chroma_db"):
        """
        Inicializa ChromaDB y modelo de embeddings

        Args:
            db_path: Ruta donde guardar la base de datos
        """
        print("💾 Inicializando base de datos...")

        # Cliente de ChromaDB
        self.client = chromadb.PersistentClient(path=db_path)

        # Colección para contratos
        self.collection = self.client.get_or_create_collection(
            name="contratos",
            metadata={"hnsw:space": "cosine"}
        )

        # Modelo para convertir texto a vectores
        self.embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

        print(f"✅ Base de datos lista en: {db_path}")

    def _sanitize_metadata(self, metadata):
        """
        ChromaDB solo acepta: str, int, float, bool
        Esta función convierte tipos complejos a strings

        Args:
            metadata: dict con metadata del contrato

        Returns:
            dict con metadata sanitizada
        """
        sanitized = {}

        for key, value in metadata.items():
            if value is None:
                continue  # Omitir None

            if isinstance(value, (str, int, float, bool)):
                # Tipos permitidos directamente
                sanitized[key] = value

            elif isinstance(value, list):
                # Listas → JSON string
                sanitized[key] = json.dumps(value, ensure_ascii=False)

            elif isinstance(value, dict):
                # Diccionarios → JSON string
                sanitized[key] = json.dumps(value, ensure_ascii=False)

            else:
                # Cualquier otro tipo → string
                sanitized[key] = str(value)

        return sanitized

    def guardar_contrato(self, archivo, texto_ocr, datos_estructurados, confianza_ocr):
        """
        Guarda un contrato en ChromaDB

        Args:
            archivo: Nombre del archivo original
            texto_ocr: Texto completo extraído por OCR
            datos_estructurados: dict con campos extraídos por LLM
            confianza_ocr: Score de confianza del OCR (0-1)

        Returns:
            str: ID del contrato guardado
        """
        print("💾 Guardando contrato en base de datos...")

        # ==========================================
        # PASO 1: Generar embedding (vector semántico)
        # ==========================================
        # Combinar info importante para el embedding
        texto_para_embedding = f"""
        Tipo: {datos_estructurados.get('contract_type', '')}
        Partes: {', '.join(datos_estructurados.get('parties', []))}
        Objeto: {datos_estructurados.get('subject_matter', '')}
        Contenido: {texto_ocr[:1000]}
        """

        embedding = self.embedder.encode(texto_para_embedding).tolist()

        # ==========================================
        # PASO 2: Preparar metadata
        # ==========================================
        metadata = {
            "archivo_original": archivo,
            "fecha_procesamiento": datetime.now().isoformat(),
            "contract_type": datos_estructurados.get('contract_type', ''),
            "signature_date": datos_estructurados.get('signature_date', ''),
            "start_date": datos_estructurados.get('start_date', ''),
            "end_date": datos_estructurados.get('end_date', ''),
            "total_amount": datos_estructurados.get('total_amount', 0),
            "currency": datos_estructurados.get('currency', ''),
            "subject_matter": datos_estructurados.get('subject_matter', ''),
            "parties": datos_estructurados.get('parties', []),
            "key_clauses": datos_estructurados.get('key_clauses', []),
            "confianza_ocr": float(confianza_ocr)
        }

        # Sanitizar metadata
        metadata_limpio = self._sanitize_metadata(metadata)

        # ==========================================
        # PASO 3: Generar ID único
        # ==========================================
        doc_id = f"contrato_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

        # ==========================================
        # PASO 4: Guardar en ChromaDB
        # ==========================================
        self.collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[texto_ocr],  # Texto completo
            metadatas=[metadata_limpio]
        )

        print(f"✅ Contrato guardado: {doc_id}")
        return doc_id

    def buscar_contratos(self, consulta, n_results=3):
        """
        Busca contratos por similitud semántica

        ¿Cómo funciona?
        1. Convierte la consulta en un vector
        2. Busca los vectores más similares en la BD
        3. Devuelve los contratos más relevantes

        Args:
            consulta: Texto de búsqueda (ej: "contratos sobre cloud")
            n_results: Cuántos resultados devolver

        Returns:
            dict con ids, documents, metadatas, distances
        """
        print(f"🔍 Buscando: '{consulta}'")

        # Convertir consulta a vector
        query_embedding = self.embedder.encode(consulta).tolist()

        # Buscar en ChromaDB
        resultados = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )

        num_encontrados = len(resultados['ids'][0])
        print(f"✅ Encontrados {num_encontrados} contratos relevantes")

        return resultados

    def listar_todos(self):
        """
        Lista todos los contratos en la base de datos

        Returns:
            dict con ids, documents, metadatas
        """
        return self.collection.get()

    def contar_contratos(self):
        """
        Cuenta cuántos contratos hay en la BD

        Returns:
            int: Número de contratos
        """
        return self.collection.count()