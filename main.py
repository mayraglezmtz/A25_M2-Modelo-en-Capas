import argparse
from LIBS.presentacion import PresentacionLayer
from LIBS.negocio import NegocioLayer
from LIBS.persistencia import PersistenciaLayer
from LIBS.data import DatabaseLayer

def main():
    parser = argparse.ArgumentParser(description="Aplicación de análisis de accidentes.")
    parser.add_argument(
        '--layer', 
        type=str, 
        choices=['all', 'data', 'persistencia', 'negocio', 'presentacion'],
        default='all',
        help="Especifica qué capa deseas ejecutar o probar."
    )
    # Argumento para meter un query por terminal (solo para capa data)
    parser.add_argument(
        '--query', 
        type=str, 
        default="SELECT City, State FROM accidentes_data LIMIT 5;",
        help="Query SQL manual para probar la capa de data directamente."
    )
    
    args = parser.parse_args()

    print(f"\n{'='*50}\n INICIANDO EJECUCIÓN EN MODO: {args.layer.upper()} \n{'='*50}")

    if args.layer == 'data':
        print("\n--- [1] PROBANDO CAPA DATA (Aislada) ---")
        db = DatabaseLayer()
        print(f"Ejecutando query manual desde el parser: \n> {args.query}")
        resultado = db.execute_query(args.query)
        print("Resultado obtenido:")
        for fila in resultado:
            print(f"  {fila}")

    elif args.layer == 'persistencia':
        print("\n--- [2] PROBANDO CAPA PERSISTENCIA (Aislada) ---")
        # Usamos negocio para generar el query, pero NO llamamos a la base de datos
        negocio = NegocioLayer()
        pregunta_prueba = "¿Qué día de la semana ocurren más accidentes?"
        
        print(f"Pregunta enviada a la IA: '{pregunta_prueba}'")
        print("Generando el query SQL con Gemini...")
        query_ia = negocio.generar_sql(pregunta_prueba)
        
        print(f"\n[QUERY GENERADO POR IA]:\n> {query_ia}\n")
        print("(El flujo se detiene aquí. No se conecta con la base de datos ni procesa la respuesta final).")

    elif args.layer == 'negocio':
        print("\n--- [3] PROBANDO CAPA NEGOCIO (Aislada) ---")
        negocio = NegocioLayer()
        status, msg = negocio.test_layer()
        print(f"\n{msg}")

    elif args.layer == 'presentacion':
        print("\n--- [4] PROBANDO CAPA PRESENTACION (Aislada) ---")
        # Le pasamos modo_aislado=True para que atrape el input pero NO llame a la IA ni a la BD
        app = PresentacionLayer(modo_aislado=True)
        app.iniciar_cli()

    elif args.layer == 'all':
        print("\n--- [ALL] EJECUTANDO FLUJO COMPLETO INTEGRADO ---")
        # Le pasamos modo_aislado=False (o vacío) para que corra normal y responda las dudas del usuario
        app = PresentacionLayer(modo_aislado=False)
        app.iniciar_cli()

if __name__ == "__main__":
    main()