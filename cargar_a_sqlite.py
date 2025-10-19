"""
============================================================================
SCRIPT DE CARGA A SQLITE - TRABAJO PRACTICO ETL
TSCDIA 2025

Integrantes:
- Paola Garcia (DNI: 29463402)
- Pablo Taborda (DNI: 28270596)
- Julio Orjindo (DNI: 26482639)
- Rodenas Elias Gabriel (DNI: 36356976)

Asignatura: Innovacion de Datos
Profesores: Alejandro Mainero, Carlos Charletti

Descripcion:
Este script automatiza la carga de datos limpios del proceso ETL
a una base de datos SQLite, creando el esquema y ejecutando las consultas.
============================================================================
"""

import pandas as pd
import sqlite3
import os
from datetime import datetime

# Configuracion de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'datos')
SQL_DIR = os.path.join(BASE_DIR, 'sql')
DB_PATH = os.path.join(BASE_DIR, 'ventas_estambul.db')

# Archivos necesarios
CSV_FILE = os.path.join(DATA_DIR, 'datos_limpios.csv')
SCHEMA_FILE = os.path.join(SQL_DIR, 'schema.sql')
QUERIES_FILE = os.path.join(SQL_DIR, 'consultas.sql')

print('=' * 80)
print('CARGA DE DATOS A SQLITE - PROCESO ETL')
print('=' * 80)
print(f'Fecha de ejecucion: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print()

# Paso 1: Verificar existencia de archivos necesarios
print('PASO 1: Verificando archivos necesarios...')
archivos_faltantes = []

if not os.path.exists(CSV_FILE):
    archivos_faltantes.append(CSV_FILE)
    print(f'  [ERROR] No se encuentra: {CSV_FILE}')
else:
    print(f'  [OK] Encontrado: datos_limpios.csv')

if not os.path.exists(SCHEMA_FILE):
    archivos_faltantes.append(SCHEMA_FILE)
    print(f'  [ERROR] No se encuentra: {SCHEMA_FILE}')
else:
    print(f'  [OK] Encontrado: schema.sql')

if not os.path.exists(QUERIES_FILE):
    archivos_faltantes.append(QUERIES_FILE)
    print(f'  [ERROR] No se encuentra: {QUERIES_FILE}')
else:
    print(f'  [OK] Encontrado: consultas.sql')

if archivos_faltantes:
    print()
    print('[ERROR] Faltan archivos necesarios. Por favor ejecuta primero el notebook analisis_etl.ipynb')
    print('El notebook debe generar el archivo datos_limpios.csv en la carpeta datos/')
    exit(1)

print()

# Paso 2: Cargar datos del CSV
print('PASO 2: Cargando datos del CSV...')
try:
    df = pd.read_csv(CSV_FILE)
    print(f'  [OK] Datos cargados: {len(df)} registros')
    print(f'  [OK] Columnas: {len(df.columns)}')
    print(f'  Columnas: {", ".join(df.columns[:5])}...')
except Exception as e:
    print(f'  [ERROR] Error al cargar CSV: {e}')
    exit(1)

print()

# Paso 3: Conectar a SQLite y crear base de datos
print('PASO 3: Conectando a SQLite...')
try:
    # Eliminar base de datos existente si existe
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f'  [OK] Base de datos anterior eliminada')
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print(f'  [OK] Conexion establecida: {DB_PATH}')
except Exception as e:
    print(f'  [ERROR] Error al conectar: {e}')
    exit(1)

print()

# Paso 4: Crear esquema de base de datos
print('PASO 4: Creando esquema de base de datos...')
try:
    with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    # Ejecutar comandos SQL del esquema
    # SQLite no soporta multiples comandos en execute(), asi que los separamos
    comandos = schema_sql.split(';')
    for comando in comandos:
        comando = comando.strip()
        if comando and not comando.startswith('--'):
            # Saltar comentarios de linea completa
            lineas_limpias = [linea for linea in comando.split('\n') 
                            if not linea.strip().startswith('--')]
            comando_limpio = '\n'.join(lineas_limpias).strip()
            if comando_limpio:
                cursor.execute(comando_limpio)
    
    conn.commit()
    print('  [OK] Esquema creado exitosamente')
    print('  [OK] Tabla datos_limpios creada con restricciones')
    print('  [OK] Indices creados para optimizacion')
except Exception as e:
    print(f'  [ERROR] Error al crear esquema: {e}')
    conn.close()
    exit(1)

print()

# Paso 5: Insertar datos en la tabla
print('PASO 5: Insertando datos en la base de datos...')
try:
    # Convertir fecha a formato correcto
    df['invoice_date'] = pd.to_datetime(df['invoice_date']).dt.strftime('%Y-%m-%d')
    
    # Insertar datos usando to_sql
    df.to_sql('datos_limpios', conn, if_exists='append', index=False)
    
    # Verificar insercion
    cursor.execute('SELECT COUNT(*) FROM datos_limpios')
    count = cursor.fetchone()[0]
    print(f'  [OK] {count} registros insertados correctamente')
    
    # Estadisticas basicas
    cursor.execute('SELECT MIN(invoice_date), MAX(invoice_date) FROM datos_limpios')
    fecha_min, fecha_max = cursor.fetchone()
    print(f'  [OK] Rango de fechas: {fecha_min} a {fecha_max}')
    
    cursor.execute('SELECT COUNT(DISTINCT customer_id) FROM datos_limpios')
    clientes = cursor.fetchone()[0]
    print(f'  [OK] Clientes unicos: {clientes}')
    
    conn.commit()
except Exception as e:
    print(f'  [ERROR] Error al insertar datos: {e}')
    conn.close()
    exit(1)

print()

# Paso 6: Ejecutar consultas de validacion
print('PASO 6: Ejecutando consultas de validacion...')
try:
    # Consulta 1: Verificar metodos de pago
    cursor.execute('''
        SELECT payment_method, COUNT(*) as cantidad
        FROM datos_limpios
        GROUP BY payment_method
        ORDER BY cantidad DESC
    ''')
    print('  Metodos de pago:')
    for row in cursor.fetchall():
        print(f'    - {row[0]}: {row[1]} transacciones')
    
    # Consulta 2: Verificar distribucion por genero
    cursor.execute('''
        SELECT gender, COUNT(*) as cantidad
        FROM datos_limpios
        GROUP BY gender
    ''')
    print('  Distribucion por genero:')
    for row in cursor.fetchall():
        print(f'    - {row[0]}: {row[1]} transacciones')
    
    # Consulta 3: Verificar categorias
    cursor.execute('''
        SELECT COUNT(DISTINCT category) as categorias
        FROM datos_limpios
    ''')
    categorias = cursor.fetchone()[0]
    print(f'  Total de categorias: {categorias}')
    
    print('  [OK] Validaciones completadas exitosamente')
except Exception as e:
    print(f'  [ERROR] Error en validaciones: {e}')

print()

# Paso 7: Mostrar ejemplo de consulta compleja
print('PASO 7: Ejecutando consulta de ejemplo...')
print('  Consulta: Top 5 categorias por ventas totales')
try:
    cursor.execute('''
        SELECT 
            category,
            COUNT(*) as transacciones,
            ROUND(SUM(total_sale), 2) as ventas_totales,
            ROUND(AVG(total_sale), 2) as ticket_promedio
        FROM datos_limpios
        GROUP BY category
        ORDER BY ventas_totales DESC
        LIMIT 5
    ''')
    
    resultados = cursor.fetchall()
    print()
    print('  Resultado:')
    print('  ' + '-' * 70)
    print(f'  {"Categoria":<20} {"Trans.":<10} {"Ventas Totales":<20} {"Ticket Prom.":<15}')
    print('  ' + '-' * 70)
    for row in resultados:
        print(f'  {row[0]:<20} {row[1]:<10} ${row[2]:>18,.2f} ${row[3]:>13,.2f}')
    print('  ' + '-' * 70)
except Exception as e:
    print(f'  [ERROR] Error en consulta: {e}')

print()

# Paso 8: Cerrar conexion
print('PASO 8: Finalizando...')
conn.close()
print('  [OK] Conexion cerrada')
print()

# Resumen final
print('=' * 80)
print('PROCESO COMPLETADO EXITOSAMENTE')
print('=' * 80)
print(f'Base de datos creada: {DB_PATH}')
print(f'Registros totales: {len(df)}')
print()
print('Para ejecutar las consultas SQL manualmente:')
print('  1. Abre una herramienta de SQLite (DB Browser, DBeaver, etc.)')
print(f'  2. Conecta a: {DB_PATH}')
print(f'  3. Ejecuta las consultas de: {QUERIES_FILE}')
print()
print('O puedes ejecutar consultas desde Python:')
print('  import sqlite3')
print(f'  conn = sqlite3.connect("{DB_PATH}")')
print('  cursor = conn.cursor()')
print('  cursor.execute("SELECT * FROM datos_limpios LIMIT 5")')
print('  print(cursor.fetchall())')
print()
print('Trabajo realizado por:')
print('  - Paola Garcia, Pablo Taborda, Julio Orjindo, Rodenas Elias Gabriel')
print('  TSCDIA 2025 - Innovacion de Datos')
print('=' * 80)
