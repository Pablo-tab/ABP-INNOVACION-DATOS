"""
Script para generar la base de datos SQLite con datos limpios
Ejecuta el proceso ETL completo: Extract → Transform → Load
"""

import pandas as pd
import numpy as np
import sqlite3
import os

print("=" * 80)
print("PROCESO ETL AUTOMATICO - GENERACION DE BASE DE DATOS")
print("=" * 80)

# ============================================================================
# FASE 1: EXTRACCION (EXTRACT)
# ============================================================================
print("\n[1/4] EXTRACCION DE DATOS...")

# Cargar datos
df_sales = pd.read_csv('sales_data.csv')
df_customers = pd.read_csv('customer_data.csv')

print(f"✅ sales_data.csv cargado: {len(df_sales):,} registros")
print(f"✅ customer_data.csv cargado: {len(df_customers):,} registros")

# Merge (JOIN)
df_combined = pd.merge(df_sales, df_customers, on='customer_id', how='left')
print(f"✅ DataFrames combinados: {len(df_combined):,} registros")

# ============================================================================
# FASE 2: TRANSFORMACION (TRANSFORM)
# ============================================================================
print("\n[2/4] TRANSFORMACION DE DATOS...")

# Crear copia para transformaciones
df_clean = df_combined.copy()

# Convertir fechas a datetime
df_clean['invoice_date'] = pd.to_datetime(df_clean['invoice_date'], format='%d-%m-%Y')

# Crear columnas derivadas
df_clean['year'] = df_clean['invoice_date'].dt.year
df_clean['month'] = df_clean['invoice_date'].dt.month
df_clean['day_of_week'] = df_clean['invoice_date'].dt.day_name()

# Calcular total de venta
df_clean['total_sale'] = df_clean['quantity'] * df_clean['price']

# Categorizar edad
def categorize_age(age):
    if pd.isna(age):
        return None
    if age < 25:
        return 'Jovenes (< 25)'
    elif 25 <= age <= 35:
        return 'Adultos jovenes (25-35)'
    elif 36 <= age <= 50:
        return 'Adultos (36-50)'
    else:
        return 'Adultos mayores (> 50)'

df_clean['age_group'] = df_clean['age'].apply(categorize_age)

print(f"✅ Columnas derivadas creadas: year, month, day_of_week, total_sale, age_group")

# ============================================================================
# FASE 3: LIMPIEZA (CLEAN)
# ============================================================================
print("\n[3/4] LIMPIEZA DE DATOS...")

# Identificar nulos
print(f"\nNulos antes de limpieza:")
nulos_antes = df_clean.isnull().sum()
for col, count in nulos_antes[nulos_antes > 0].items():
    print(f"  - {col}: {count} nulos")

# Eliminar registros con age nulo
registros_antes = len(df_clean)
df_clean = df_clean.dropna(subset=['age'])
registros_eliminados = registros_antes - len(df_clean)

print(f"\n✅ Registros eliminados: {registros_eliminados}")
print(f"✅ Registros finales: {len(df_clean):,}")
print(f"✅ Tasa de recuperación: {(len(df_clean)/registros_antes)*100:.2f}%")

# Convertir fecha a formato ISO 8601 (string) para SQLite
df_clean['invoice_date'] = df_clean['invoice_date'].dt.strftime('%Y-%m-%d')

# Seleccionar columnas finales
columns_final = [
    'invoice_no', 'customer_id', 'gender', 'age', 'age_group',
    'payment_method', 'category', 'quantity', 'price', 'total_sale',
    'invoice_date', 'year', 'month', 'day_of_week', 'shopping_mall'
]

df_final = df_clean[columns_final].copy()

# ============================================================================
# FASE 4: CARGA (LOAD)
# ============================================================================
print("\n[4/4] CARGA A BASE DE DATOS SQLITE...")

# Crear directorio sql si no existe
os.makedirs('sql', exist_ok=True)

# Conectar a SQLite
db_path = 'sql/ventas.db'
conn = sqlite3.connect(db_path)

# Cargar datos a tabla
df_final.to_sql('datos_limpios', conn, if_exists='replace', index=False)

print(f"✅ Tabla 'datos_limpios' creada en: {db_path}")

# Verificar carga
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM datos_limpios')
count = cursor.fetchone()[0]
print(f"✅ Registros en base de datos: {count:,}")

# Verificar estructura
cursor.execute("PRAGMA table_info(datos_limpios)")
columns = cursor.fetchall()
print(f"\n✅ Columnas en tabla 'datos_limpios': {len(columns)}")
for col in columns:
    print(f"   - {col[1]} ({col[2]})")

# Estadísticas finales
cursor.execute("SELECT MIN(invoice_date), MAX(invoice_date) FROM datos_limpios")
date_range = cursor.fetchone()
print(f"\n📅 Rango de fechas: {date_range[0]} a {date_range[1]}")

cursor.execute("SELECT SUM(total_sale) FROM datos_limpios")
total_ventas = cursor.fetchone()[0]
print(f"💰 Ventas totales: ${total_ventas:,.2f}")

cursor.execute("SELECT COUNT(DISTINCT customer_id) FROM datos_limpios")
clientes = cursor.fetchone()[0]
print(f"👥 Clientes únicos: {clientes:,}")

conn.close()

print("\n" + "=" * 80)
print("✅ PROCESO ETL COMPLETADO EXITOSAMENTE")
print("=" * 80)
print(f"\n📂 Base de datos generada: {db_path}")
print(f"🔧 Herramienta recomendada: DB Browser for SQLite")
print(f"📊 Tabla disponible: datos_limpios ({count:,} registros)")
print("\n💡 Ahora puedes abrir el archivo con DB Browser for SQLite para explorar los datos.")
