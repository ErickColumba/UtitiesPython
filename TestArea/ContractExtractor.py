# contract_extractor.py
import json
import ollama


class ContractExtractor:
    """Extrae información estructurada de contratos usando IA local"""

    def __init__(self, model_name="llama3.1:8b"):
        self.model_name = model_name

    def extract_contract_data(self, text):
        """Extrae campos importantes del contrato"""

        prompt = f"""Eres un asistente experto en análisis de contratos. 
Analiza el siguiente texto de contrato y extrae la información en formato JSON.

CAMPOS A EXTRAER:
- tipo_contrato: tipo de contrato (compraventa, arrendamiento, servicios, etc.)
- partes: array con nombres de las partes involucradas
- fecha_firma: fecha de firma del contrato
- fecha_inicio: fecha de inicio de vigencia
- fecha_termino: fecha de término (si aplica)
- monto_total: monto total del contrato
- moneda: moneda del monto
- objeto: descripción breve del objeto del contrato
- clausulas_importantes: array con cláusulas relevantes
- penalidades: penalidades o multas mencionadas

TEXTO DEL CONTRATO:
{text[:4000]}

Responde ÚNICAMENTE con un JSON válido, sin texto adicional."""

        response = ollama.chat(
            model=self.model_name,
            messages=[{'role': 'user', 'content': prompt}]
        )

        try:
            # Extrae el JSON de la respuesta
            content = response['message']['content']
            # Limpia markdown si existe
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0]
            elif '```' in content:
                content = content.split('```')[1].split('```')[0]

            return json.loads(content.strip())
        except:
            return {"error": "No se pudo extraer información estructurada"}