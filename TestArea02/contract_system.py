import json


class ContractSystem:
    """
    RESPONSABILIDAD: Coordinar todas las clases

    ¿Qué hace?
    - Usa OCRProcessor para extraer texto
    - Usa LLMExtractor para obtener datos estructurados
    - Usa DatabaseManager para guardar y buscar
    - Proporciona interfaz simple para el usuario
    """

    def __init__(self, db_path="./chroma_db", llm_model="mistral:7b", ocr_lang="en"):
        """
        Inicializa el sistema completo

        Args:
            db_path: Ruta de la base de datos
            llm_model: Modelo de Ollama a usar
            ocr_lang: Idioma para OCR
        """
        print("🚀 Inicializando sistema de contratos...")
        print()

        # Importar las clases
        from ocr_processor import OCRProcessor
        from llm_extractor import LLMExtractor
        from database_manager import DatabaseManager

        # Inicializar componentes
        self.ocr = OCRProcessor(lang=ocr_lang)
        self.llm = LLMExtractor(model_name=llm_model)
        self.db = DatabaseManager(db_path=db_path)

        print()
        print("✅ Sistema listo para usar")
        print("=" * 60)

    def procesar_contrato(self, ruta_imagen):
        """
        FLUJO COMPLETO: Imagen → Texto → Datos → Base de datos

        Args:
            ruta_imagen: Ruta al archivo de imagen

        Returns:
            str: ID del contrato guardado
        """
        print("\n" + "=" * 60)
        print(f"📄 PROCESANDO CONTRATO: {ruta_imagen}")
        print("=" * 60)

        # ==========================================
        # PASO 1: OCR - Extraer texto
        # ==========================================
        resultado_ocr = self.ocr.extraer_texto(ruta_imagen)
        texto_completo = resultado_ocr['texto_completo']
        confianza = resultado_ocr['confianza']

        # ==========================================
        # PASO 2: LLM - Extraer datos estructurados
        # ==========================================
        datos_estructurados = self.llm.extract_contract_data(texto_completo)

        # ==========================================
        # PASO 3: BD - Guardar todo
        # ==========================================
        contrato_id = self.db.guardar_contrato(
            archivo=ruta_imagen,
            texto_ocr=texto_completo,
            datos_estructurados=datos_estructurados,
            confianza_ocr=confianza
        )

        print("=" * 60)
        print(f"✅ CONTRATO PROCESADO: {contrato_id}")
        print("=" * 60)

        return contrato_id

    def responder_pregunta(self, pregunta):
        """
        FLUJO COMPLETO: Pregunta → Buscar → Contexto → Respuesta

        Args:
            pregunta: Pregunta del usuario

        Returns:
            str: Respuesta del LLM
        """
        print("\n" + "=" * 60)
        print(f"❓ PREGUNTA: {pregunta}")
        print("=" * 60)

        # ==========================================
        # PASO 1: Buscar contratos relevantes
        # ==========================================
        resultados = self.db.buscar_contratos(pregunta, n_results=3)

        if not resultados['ids'][0]:
            return "❌ No encontré contratos relacionados con tu pregunta."

        # ==========================================
        # PASO 2: Construir contexto
        # ==========================================
        contexto = self._construir_contexto(resultados)

        # ==========================================
        # PASO 3: LLM genera respuesta
        # ==========================================
        respuesta = self.llm.responder_pregunta(pregunta, contexto)

        return respuesta

    def _construir_contexto(self, resultados):
        """
        Construye contexto rico para el LLM

        Args:
            resultados: Resultados de ChromaDB

        Returns:
            str: Contexto formateado
        """
        contexto = ""

        ids = resultados['ids'][0]
        documentos = resultados['documents'][0]
        metadatas = resultados['metadatas'][0]
        distancias = resultados['distances'][0]

        for i, doc_id in enumerate(ids):
            metadata = metadatas[i]
            texto_ocr = documentos[i]
            relevancia = 1 - distancias[i]

            # Deserializar listas JSON
            parties = json.loads(metadata.get('parties', '[]')) if isinstance(metadata.get('parties'),
                                                                              str) else metadata.get('parties', [])
            key_clauses = json.loads(metadata.get('key_clauses', '[]')) if isinstance(metadata.get('key_clauses'),
                                                                                      str) else metadata.get(
                'key_clauses', [])

            contexto += f"""
{'=' * 60}
CONTRACT ID: {doc_id}
RELEVANCE: {relevancia:.2%}
{'=' * 60}

STRUCTURED DATA:
- File: {metadata.get('archivo_original', 'N/A')}
- Type: {metadata.get('contract_type', 'N/A')}
- Parties: {', '.join(parties) if parties else 'N/A'}
- Signature: {metadata.get('signature_date', 'N/A')}
- Start: {metadata.get('start_date', 'N/A')}
- End: {metadata.get('end_date', 'N/A')}
- Amount: {metadata.get('total_amount', 'N/A')} {metadata.get('currency', '')}
- Subject: {metadata.get('subject_matter', 'N/A')}
- Clauses: {', '.join(key_clauses) if key_clauses else 'N/A'}

FULL TEXT (first 2000 chars):
{texto_ocr[:2000]}...

"""

        return contexto

    def listar_contratos(self):
        """Muestra todos los contratos en la BD"""
        resultado = self.db.listar_todos()

        print("\n" + "=" * 60)
        print("📋 CONTRATOS EN LA BASE DE DATOS")
        print("=" * 60)

        if not resultado['ids']:
            print("No hay contratos guardados aún.")
            return

        for i, doc_id in enumerate(resultado['ids']):
            metadata = resultado['metadatas'][i]
            parties = json.loads(metadata.get('parties', '[]')) if isinstance(metadata.get('parties'), str) else []

            print(f"\n{i + 1}. {doc_id}")
            print(f"   Archivo: {metadata.get('archivo_original', 'N/A')}")
            print(f"   Tipo: {metadata.get('contract_type', 'N/A')}")
            print(f"   Partes: {', '.join(parties) if parties else 'N/A'}")
            print(f"   Monto: {metadata.get('total_amount', 'N/A')} {metadata.get('currency', '')}")
            print(f"   Vence: {metadata.get('end_date', 'N/A')}")

        print("=" * 60)

    def modo_interactivo(self):
        """Modo interactivo para consultas"""
        print("\n" + "=" * 60)
        print("🤖 SISTEMA DE CONSULTA DE CONTRATOS")
        print("=" * 60)
        print("\nComandos:")
        print("  - Escribe una pregunta sobre tus contratos")
        print("  - 'listar' para ver todos los contratos")
        print("  - 'stats' para ver estadísticas")
        print("  - 'salir' para terminar")
        print("=" * 60)

        while True:
            comando = input("\n💬 > ")

            if comando.lower() == 'salir':
                print("👋 ¡Hasta luego!")
                break

            elif comando.lower() == 'listar':
                self.listar_contratos()

            elif comando.lower() == 'stats':
                total = self.db.contar_contratos()
                print(f"\n📊 Total de contratos: {total}")

            else:
                # Es una pregunta
                respuesta = self.responder_pregunta(comando)
                print("\n💬 Respuesta:")
                print("-" * 60)
                print(respuesta)
                print("-" * 60)