# test_complete.py

import uuid

from TestArea.ContractDatabase import ContractDatabase
from TestArea.ContractExtractor import ContractExtractor
from TestArea.DocumentProcessor import DocumentProcessor


def test_full_pipeline():
    """Prueba el pipeline completo"""

    print("=" * 60)
    print("PRUEBA DEL SISTEMA COMPLETO")
    print("=" * 60)

    # 1. Procesar documento
    print("\n1. Procesando documento...")
    processor = DocumentProcessor()
    text = processor.extract_text("test.pdf")
    print(f"✓ Texto extraído: {len(text)} caracteres")
    print(f"\nPrimeros 300 caracteres:\n{text[:300]}\n")

    # 2. Extraer datos con IA
    print("2. Extrayendo datos con IA...")
    extractor = ContractExtractor()
    metadata = extractor.extract_contract_data(text)
    print(f"✓ Datos extraídos:")
    for key, value in metadata.items():
        print(f"  - {key}: {value}")

    # 3. Guardar en BD
    print("\n3. Guardando en base de datos...")
    db = ContractDatabase()
    contract_id = str(uuid.uuid4())
    db.add_contract(contract_id, text, metadata)

    # 4. Verificar guardado
    print("\n4. Verificando almacenamiento...")
    saved_contract = db.get_contract(contract_id)
    if saved_contract:
        print(f"✓ Contrato recuperado exitosamente")
        print(f"  ID: {saved_contract['id']}")
        print(f"  Metadatos: {saved_contract['metadata']}")

    # 5. Probar búsqueda
    print("\n5. Probando búsqueda semántica...")
    results = db.search_contracts("¿Cuáles son las partes del contrato?", n_results=1)
    print(f"✓ Resultados encontrados: {len(results['ids'][0])}")

    print("\n" + "=" * 60)
    print("✓ PRUEBA COMPLETADA EXITOSAMENTE")
    print("=" * 60)

    return contract_id


if __name__ == "__main__":
    test_full_pipeline()