import mysql.connector
import time

class DatabaseLayer:
    def __init__(self):
        # ¡RECUERDA PONER TU CONTRASEÑA REAL AQUÍ!
        self.config = {
            'host': '127.0.0.1',
            'user': 'TC3005B',
            'password': 'TEC2026', 
            'database': 'accidentes'
        }

    def execute_query(self, query):
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()
            return result
        except mysql.connector.Error as err:
            return f"Error en la base de datos: {err}"

    def test_connection(self):
        start_time = time.time()
        try:
            conn = mysql.connector.connect(**self.config)
            if conn.is_connected():
                conn.close()
                end_time = time.time()
                tiempo = round(end_time - start_time, 4)
                return True, f"[ÉXITO] Conexión a MySQL establecida en {tiempo} segundos."
        except mysql.connector.Error as err:
            return False, f"[FALLO] No se pudo conectar a MySQL: {err}"