from LIBS.data import DatabaseLayer
import time

class PersistenciaLayer:
    def __init__(self):
        self.db = DatabaseLayer()

    def ejecutar_query(self, query_generado_por_ia):
        return self.db.execute_query(query_generado_por_ia)

    def test_layer(self):
        print("Enviando query de prueba a la base de datos...")
        start_time = time.time()
        # Un query sencillo para validar que podemos leer los datos
        resultado = self.db.execute_query("SELECT COUNT(*) as Total FROM accidentes_data;")
        end_time = time.time()
        
        if isinstance(resultado, str) and "Error" in resultado:
            return False, f"[FALLO] La persistencia falló: {resultado}"
            
        tiempo = round(end_time - start_time, 4)
        total_filas = resultado[0]['Total']
        return True, f"[ÉXITO] Persistencia OK. Tiempo de query: {tiempo} segs. Total de registros leídos: {total_filas}."