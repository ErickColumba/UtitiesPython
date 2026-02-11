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
    contract_id = process_and_store_contract("Cardow, Inc dba Cardow Airport Store Lease and Amend No. 1 10.2014.pdf")

    # Inicia el chat
    chat_with_contracts()

#TODO
"""     ################################ IMPORTANTEEEEE  ###########################################################
        - Toca espesificar bien las etiquetas que se van a manejar por que si no el modelo se confunde (Base da datos)
        Expreciones de las tablas y labesl de documento, se pued armar o extraer del entrenamiento del modelo de IA
        Ejemplo : ZONAS --- Contexo  puesto de venta de comidas(Se puede clasificar como una ZONA), TOCA VERIFICAR EL CONEXTO PARA ENCONTRAR PALABRAS CLAVE 
        ##############################################################################################################   
        
        - Cambiar el fitz (Lecatura de PDF) por temas de licencias 
        - Cambiar el Poppler (Transfirmacion de PDF escaneado a Image para procesmiento de OCR )por temas de licencias 
        - Entrenamiento de Lora,RAG, para especiliar el modelo para utlizacion del modelo , Mistral 7B  
        - Integrar api para conexion ah internet  """