from LIBS.negocio import NegocioLayer

class PresentacionLayer:
    # Agregamos el parámetro modo_aislado (por defecto False para que el sistema normal funcione)
    def __init__(self, modo_aislado=False):
        self.negocio = NegocioLayer()
        self.modo_aislado = modo_aislado
        self.preguntas = {
            '1': '¿En qué estado ocurren más accidentes?',
            '2': '¿Cómo influye el día y la noche en los accidentes?',
            '3': '¿En qué horas del día ocurren más accidentes?',
            '4': '¿Qué día de la semana ocurren más accidentes?'
        }

    def mostrar_menu(self):
        print("\n" + "="*60)
        print("   ANÁLISIS DE ACCIDENTES EN EE.UU. (Impulsado por IA)")
        print("="*60)
        for key, pregunta in self.preguntas.items():
            print(f"{key}. {pregunta}")
        print("5. Escribir una pregunta libre en lenguaje natural")
        print("6. Salir")
        print("="*60)

    def iniciar_cli(self):
        while True:
            self.mostrar_menu()
            opcion = input("Ingresa el número de tu opción (1-6): ")

            if opcion == '6':
                print("Saliendo de la aplicación. ¡Hasta luego!")
                break
            
            # Variable para guardar el input final
            pregunta_texto = ""

            if opcion in self.preguntas:
                pregunta_texto = self.preguntas[opcion]
            
            elif opcion == '5':
                pregunta_texto = input("\nEscribe tu pregunta sobre los accidentes: ")
                if not pregunta_texto.strip():
                    print("[!] No escribiste nada. Intenta de nuevo.")
                    continue
            else:
                print("\n[!] Error: Opción no válida. Intenta de nuevo con un número del 1 al 6.")
                continue

            # =========================================================
            # LÓGICA DE AISLAMIENTO O FLUJO COMPLETO
            # =========================================================
            if self.modo_aislado:
                print("\n--- [PRUEBA AISLADA - CAPA DE PRESENTACIÓN] ---")
                print(f"Input capturado exitosamente: '{pregunta_texto}'")
                print("(El flujo se detiene aquí. No se conecta con Negocio, Persistencia ni BD).")
            else:
                print(f"\nPreguntándole a la IA: '{pregunta_texto}'...")
                print("Generando SQL y consultando la base de datos (~7.7M registros). Por favor espera...")
                respuesta = self.negocio.procesar_solicitud(pregunta_texto)
                print("\n>>> RESPUESTA DE LA IA:")
                print(respuesta)