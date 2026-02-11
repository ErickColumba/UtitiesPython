# ContractExtractor.py
import json
import ollama


class ContractExtractor:
    """Extrae información estructurada de contratos usando IA local"""

    def __init__(self, model_name="mistral:7b"):
        self.model_name = model_name

    def extract_contract_data(self, text):
        """Extrae campos importantes del contrato"""

        # Limita el texto si es muy largo
        text_sample = text[:6000] if len(text) > 6000 else text

        prompt = f"""Analiza el siguiente texto y extrae información del contrato en formato JSON.

IMPORTANTE: 
- Si NO encuentras información para un campo, NO lo incluyas en el JSON
- NO uses null, [] o {{}}
- Solo incluye campos con información real encontrada

TEXTO:
{text_sample}

Possible fields (only include those you find):
- contract_type: type (e.g., "sale", "lease", "service agreement")
- parties: ["Party 1 Name", "Party 2 Name"]
- signature_date: "YYYY-MM-DD"
- start_date: "YYYY-MM-DD"
- end_date: "YYYY-MM-DD"
- total_amount: number without symbols
- currency: "USD", "EUR", "GBP", etc.
- subject_matter: brief description
- key_clauses: ["FIRST CLAUSE", "Key Commercial Terms"]
- penalties: "description of penalties"

Responde SOLO con JSON válido:"""

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{
                    'role': 'user',
                    'content': prompt
                }],
                options={
                    'temperature': 0.1,
                }
            )

            content = response['message']['content']

            # Limpia markdown
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0]
            elif '```' in content:
                content = content.split('```')[1].split('```')[0]

            data = json.loads(content.strip())

            # Limpia el diccionario: elimina None, listas vacías, strings vacíos
            clean_data = {}
            for key, value in data.items():
                if value is None:
                    continue
                if isinstance(value, list) and len(value) == 0:
                    continue
                if isinstance(value, dict) and len(value) == 0:
                    continue
                if isinstance(value, str) and not value.strip():
                    continue
                clean_data[key] = value

            return clean_data

        except json.JSONDecodeError as e:
            print(f"⚠️ Error al parsear JSON: {e}")
            print(f"Respuesta del modelo: {content[:500]}")
            return {}
        except Exception as e:
            print(f"⚠️ Error en extracción: {e}")
            return {}