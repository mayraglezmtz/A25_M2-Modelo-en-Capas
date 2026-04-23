from google import genai
from LIBS.persistencia import PersistenciaLayer
import time

class NegocioLayer:
    def __init__(self):
        self.persistencia = PersistenciaLayer()
        self.client = genai.Client(api_key="LA_API_KEY_VA_AQUI_PROFE") 
        self.modelo = 'gemini-2.5-flash-lite'
        
        self.db_specs = """
        Contexto de la BD MySQL:
        - Tabla: 'accidentes_data'
        - Total de registros: ~7.7 millones.
        - Esquema relevante para las preguntas:
          * State (varchar): Estado de USA.
          * City (varchar): Ciudad.
          * Sunrise_Sunset (varchar): 'Day' o 'Night'.
          * Start_Time (datetime): Fecha y hora del accidente.
        INSTRUCCIÓN VITAL: Usa GROUP BY, ORDER BY DESC y LIMIT 5. No devuelvas markdown, solo el SQL puro.
        """

    def generar_sql(self, pregunta):
        prompt = f"""
        {self.db_specs}
        Escribe ÚNICAMENTE la consulta SQL válida en MySQL para responder: "{pregunta}".
        IMPORTANTE: Devuelve solo el código SQL sin comillas invertidas.
        """
        respuesta = self.client.models.generate_content(model=self.modelo, contents=prompt)
        return respuesta.text.strip()

    def procesar_solicitud(self, pregunta_texto):
        try:
            sql_query = self.generar_sql(pregunta_texto)
            datos_crudos = self.persistencia.ejecutar_query(sql_query)

            if isinstance(datos_crudos, str) and "Error" in datos_crudos:
                return f"Hubo un problema con la base de datos: {datos_crudos}"

            prompt_explicacion = f"La pregunta fue: '{pregunta_texto}'. Datos de MySQL: {datos_crudos}. Redacta una respuesta clara mostrando los resultados."
            explicacion = self.client.models.generate_content(model=self.modelo, contents=prompt_explicacion)
            
            return explicacion.text

        except Exception as e:
            return f"Error en la capa de negocio/IA: {e}"

    def test_layer(self):
        # 1. Imprimir la tabla de especificaciones
        print("\n" + "="*60)
        print(f"{'ESPECIFICACIONES DE LA BASE DE DATOS (accidentes_data)':^60}")
        print("="*60)
        print(f"{'Campo (Field)':<25} | {'Tipo (Type)':<20} | {'Nulo'}")
        print("-" * 60)
        
        campos = [
            ("ID", "varchar(50)", "YES"), ("Source", "varchar(50)", "YES"),
            ("Severity", "int", "YES"), ("Start_Time", "datetime", "YES"),
            ("End_Time", "datetime", "YES"), ("Start_Lat", "double", "YES"),
            ("Start_Lng", "double", "YES"), ("End_Lat", "double", "YES"),
            ("End_Lng", "double", "YES"), ("Distance(mi)", "double", "YES"),
            ("Description", "text", "YES"), ("Street", "varchar(255)", "YES"),
            ("City", "varchar(100)", "YES"), ("County", "varchar(100)", "YES"),
            ("State", "varchar(10)", "YES"), ("Zipcode", "varchar(20)", "YES"),
            ("Country", "varchar(10)", "YES"), ("Timezone", "varchar(100)", "YES"),
            ("Airport_Code", "varchar(20)", "YES"), ("Weather_Timestamp", "datetime", "YES"),
            ("Temperature(F)", "double", "YES"), ("Wind_Chill(F)", "double", "YES"),
            ("Humidity(%)", "double", "YES"), ("Pressure(in)", "double", "YES"),
            ("Visibility(mi)", "double", "YES"), ("Wind_Direction", "varchar(20)", "YES"),
            ("Wind_Speed(mph)", "double", "YES"), ("Precipitation(in)", "double", "YES"),
            ("Weather_Condition", "varchar(100)", "YES"), ("Amenity", "tinyint(1)", "YES"),
            ("Bump", "tinyint(1)", "YES"), ("Crossing", "tinyint(1)", "YES"),
            ("Give_Way", "tinyint(1)", "YES"), ("Junction", "tinyint(1)", "YES"),
            ("No_Exit", "tinyint(1)", "YES"), ("Railway", "tinyint(1)", "YES"),
            ("Roundabout", "tinyint(1)", "YES"), ("Station", "tinyint(1)", "YES"),
            ("Stop", "tinyint(1)", "YES"), ("Traffic_Calming", "tinyint(1)", "YES"),
            ("Traffic_Signal", "tinyint(1)", "YES"), ("Turning_Loop", "tinyint(1)", "YES"),
            ("Sunrise_Sunset", "varchar(10)", "YES"), ("Civil_Twilight", "varchar(10)", "YES"),
            ("Nautical_Twilight", "varchar(10)", "YES"), ("Astronomical_Twilight", "varchar(10)", "YES")
        ]
        
        for c in campos:
            print(f"{c[0]:<25} | {c[1]:<20} | {c[2]}")
        print("="*60)

        # 2. Probar la conexión a la API
        print("\nVerificando conexión con Gemini (Ping)...")
        start_time = time.time()
        try:
            respuesta = self.client.models.generate_content(
                model=self.modelo,
                contents="Responde únicamente con la palabra: OK"
            )
            if "OK" in respuesta.text.upper():
                tiempo = round(time.time() - start_time, 4)
                return True, f"[ÉXITO] Conexión con IA establecida en {tiempo} segundos."
            else:
                return False, "[FALLO] La IA no respondió correctamente."
        except Exception as e:
            return False, f"[FALLO] Error de API: {e}"