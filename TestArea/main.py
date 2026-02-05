# main.py - Ejemplo de uso

import uuid

from TestArea.ContractChatbot import ContractChatbot
from TestArea.ContractDatabase import ContractDatabase
from TestArea.ContractExtractor import ContractExtractor
from TestArea.DocumentProcessor import DocumentProcessor


def process_and_store_contract(file_path):
    """Procesa un contrato y lo almacena en la BD"""

    # 1. Extrae texto
    processor = DocumentProcessor()
    text = processor.extract_text(file_path)
    print(f"✓ Texto extraído: {len(text)} caracteres")

    # 2. Extrae datos estructurados con IA
    extractor = ContractExtractor()
    metadata = extractor.extract_contract_data(text)
    print(f"✓ Datos extraídos: {metadata}")

    # 3. Almacena en base de datos
    db = ContractDatabase()
    contract_id = str(uuid.uuid4())
    db.add_contract(contract_id, text, metadata)
    print(f"✓ Contrato almacenado con ID: {contract_id}")

    return contract_id


def chat_with_contracts():
    """Inicia el chatbot para consultar contratos"""

    db = ContractDatabase()
    chatbot = ContractChatbot(db)

    print("\n🤖 Chatbot de Contratos Iniciado")
    print("Escribe 'salir' para terminar\n")

    while True:
        question = input("Tú: ")
        if question.lower() in ['salir', 'exit', 'quit']:
            break

        answer = chatbot.ask(question)
        print(f"\n🤖 Asistente: {answer}\n")


# Ejemplo de uso
if __name__ == "__main__":
    # Procesa un contrato
    contract_id = process_and_store_contract("test02.pdf")

    # Inicia el chat
    #chat_with_contracts()