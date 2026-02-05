# chatbot.py
import ollama


class ContractChatbot:
    """Chatbot para consultar contratos usando RAG"""

    def __init__(self, database, model_name="llama3.1:8b"):
        self.db = database
        self.model_name = model_name
        self.conversation_history = []

    def ask(self, question):
        """Responde preguntas sobre los contratos"""

        # Busca contratos relevantes
        results = self.db.search_contracts(question, n_results=3)

        # Construye contexto
        context = "\n\n".join([
            f"CONTRATO {i + 1}:\n{doc}\nMETADATOS: {json.dumps(meta, ensure_ascii=False)}"
            for i, (doc, meta) in enumerate(zip(
                results['documents'][0],
                results['metadatas'][0]
            ))
        ])

        # Construye el prompt con contexto
        prompt = f"""Eres un asistente experto en contratos. Responde la pregunta basándote ÚNICAMENTE en la información de los contratos proporcionados.

CONTEXTO (Contratos relevantes):
{context}

PREGUNTA: {question}

Responde de forma clara y concisa. Si la información no está en los contratos, indica que no tienes esa información."""

        # Genera respuesta
        response = ollama.chat(
            model=self.model_name,
            messages=[
                {'role': 'system', 'content': 'Eres un asistente experto en análisis de contratos.'},
                {'role': 'user', 'content': prompt}
            ]
        )

        answer = response['message']['content']

        # Guarda en historial
        self.conversation_history.append({
            'question': question,
            'answer': answer
        })

        return answer