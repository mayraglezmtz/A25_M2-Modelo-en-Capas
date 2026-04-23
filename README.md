# Sistema de Análisis de Accidentes con IA (TC3005B) 🚗📊

Este proyecto es una herramienta inteligente de análisis de datos que permite consultar una base de datos masiva de accidentes de tráfico en EE. UU. (7.7 millones de registros) utilizando **lenguaje natural**. 

El sistema utiliza **Inteligencia Artificial (Gemini 2.5 Flash Lite)** para traducir preguntas cotidianas en sentencias SQL precisas, las ejecuta en un servidor MySQL y devuelve una interpretación narrativa de los resultados.

## 🏗️ Arquitectura del Proyecto

El software implementa un **Patrón de Arquitectura por Capas**, lo que permite una alta cohesión y un bajo acoplamiento.

### Descripción de las Capas:
1.  **Capa de Presentación (`LIBS/presentacion.py`):** Gestiona la interfaz de usuario (CLI) y la captura de datos.
2.  **Capa de Negocio (`LIBS/negocio.py`):** Orquestador principal. Maneja la comunicación con la API de Gemini y la interpretación de resultados.
3.  **Capa de Persistencia (`LIBS/persistencia.py`):** Gestiona la limpieza y extracción del SQL generado por la IA.
4.  **Capa de Datos (`LIBS/data.py`):** Responsable de la conexión física y ejecución de queries en MySQL.

---

## 📂 Estructura de Archivos

```text
/CohesionLeyva
├── main.py                # Punto de entrada y Parser de comandos
├── LIBS/
│   ├── data.py            # Capa de Datos
│   ├── negocio.py         # Capa de Negocio (IA)
│   ├── persistencia.py    # Capa de Persistencia
│   └── presentacion.py    # Capa de Presentación
└── US_Accidents_data.csv  # Dataset de referencia
```

## 🚀 Pruebas y Ejecución
El proyecto incluye un Parser que permite probar cada capa de manera aislada para verificar su funcionamiento:

1. Probar Capa de Datos (Aislada)
Ejecuta un query SQL directo a la base de datos:

Bash
python main.py --layer data --query "SELECT State, COUNT(*) FROM accidentes_data GROUP BY State LIMIT 3;"
2. Probar Capa de Persistencia (Generación SQL)
Verifica que la IA genere el código SQL correctamente sin tocar la base de datos:

Bash
python main.py --layer persistencia
3. Probar Capa de Negocio (Health Check IA)
Verifica la conexión y cuotas con la API de Gemini:

Bash
python main.py --layer negocio
4. Probar Capa de Presentación
Inicia el menú interactivo sin procesar lógica de fondo:

Bash
python main.py --layer presentacion
5. Flujo Completo
Ejecuta la aplicación completa (entrada de usuario -> IA -> DB -> Respuesta final):

Bash
python main.py --layer all

🛠️ Tecnologías Utilizadas
Lenguaje: Python 3.13
IA: Google Gemini API (google-genai)
Base de Datos: MySQL
Arquitectura: Diseño por Capas (Cohesión y Desacoplamiento)

## 👤 Autor
Mayra Gonzalez Martinez - a01769543@tec.mx

Tecnológico de Monterrey
