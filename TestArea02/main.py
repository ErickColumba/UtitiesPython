from contract_system import ContractSystem


def main():
    """
    Programa principal
    """

    # ==========================================
    # INICIALIZAR SISTEMA
    # ==========================================
    sistema = ContractSystem(
        db_path="./chroma_db",
        llm_model="mistral:7b",
        ocr_lang="en"
    )

    # ==========================================
    # OPCIÓN 1: PROCESAR CONTRATOS
    # ==========================================
    print("\n¿Quieres procesar contratos nuevos? (s/n)")
    respuesta = input("> ")

    if respuesta.lower() == 's':
        print("\nIngresa las rutas de los contratos (uno por línea, 'fin' para terminar):")

        while True:
            ruta = input("Ruta: ")
            if ruta.lower() == 'fin':
                break

            try:
                sistema.procesar_contrato(ruta)
            except Exception as e:
                print(f"❌ Error procesando {ruta}: {e}")

    # ==========================================
    # OPCIÓN 2: MODO CONSULTA
    # ==========================================
    sistema.modo_interactivo()


if __name__ == "__main__":
    main()