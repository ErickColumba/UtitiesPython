import json
import requests


class LLMExtractor:
    """
    RESPONSABILIDAD: Extraer datos estructurados de texto usando LLM

    ¿Qué hace?
    - Recibe texto (del OCR)
    - Le pide al LLM que identifique: tipo, partes, fechas, montos, etc.
    - Devuelve datos en formato JSON
    """

    def __init__(self, model_name="mistral:7b", base_url="http://localhost:11434"):
        """
        Inicializa conexión con Ollama

        Args:
            model_name: Modelo a usar (ej: "mistral:7b", "llama2")
            base_url: URL de Ollama
        """
        self.model_name = model_name
        self.base_url = base_url

    def extract_contract_data(self, texto):
        """
        Extrae campos estructurados del texto del contrato

        Args:
            texto: Texto completo del contrato (del OCR)

        Returns:
            dict con campos como: contract_type, parties, dates, amount, etc.
        """
        print("🤖 Extrayendo datos estructurados con LLM...")

        # Limitar texto si es muy largo (para no exceder tokens)
        texto_sample = texto[:6000] if len(texto) > 6000 else texto

        # Construir prompt
        prompt = f"""Extract contract information in JSON format.

TEXT:
{texto_sample}

Extract these fields (only include if found):
- contract_type: string (e.g., "service agreement", "lease", "sale")
- parties: array of party names
- signature_date: "YYYY-MM-DD"
- start_date: "YYYY-MM-DD"
- end_date: "YYYY-MM-DD"
- total_amount: number (without symbols)
- currency: string (e.g., "USD", "EUR")
- subject_matter: brief description
- key_clauses: array of clause titles
- penalties: description of penalties

IMPORTANT:
- Only include fields you actually find in the text
- Do NOT use null, [], or {{}}
- Respond ONLY with valid JSON, no explanations

JSON:"""

        # Llamar a Ollama
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
        )

        if response.status_code != 200:
            print(f"❌ Error llamando a Ollama: {response.status_code}")
            return {}

        # Obtener respuesta
        llm_response = response.json()['response']

        # Parsear JSON
        try:
            # Limpiar posibles markdown code blocks
            llm_response = llm_response.strip()
            if llm_response.startswith("```json"):
                llm_response = llm_response[7:]
            if llm_response.startswith("```"):
                llm_response = llm_response[3:]
            if llm_response.endswith("```"):
                llm_response = llm_response[:-3]

            datos = json.loads(llm_response.strip())
            print(f"✅ Extraídos {len(datos)} campos")
            return datos

        except json.JSONDecodeError as e:
            print(f"⚠️ Error parseando JSON: {e}")
            print(f"Respuesta del LLM: {llm_response[:200]}...")
            return {}

    def responder_pregunta(self, pregunta, contexto):
        """
        Responde una pregunta del usuario usando contexto de contratos

        Args:
            pregunta: Pregunta del usuario
            contexto: Información de contratos relevantes

        Returns:
            str: Respuesta del LLM
        """
        print("🤖 Generando respuesta...")

        prompt = f"""You are a contract analysis assistant. Answer the user's question using the provided contract information.

QUESTION:
{pregunta}

AVAILABLE CONTRACTS:
{contexto}

Instructions:
- Provide a clear, direct answer
- Reference specific contract IDs when relevant
- If you need information from the full contract text, use it
- Be concise but complete

Answer:"""

        # Llamar a Ollama
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
        )

        if response.status_code != 200:
            return f"❌ Error generando respuesta: {response.status_code}"

        return response.json()['response']