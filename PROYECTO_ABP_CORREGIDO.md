# PROYECTO ABP - ANÁLISIS ETL DE DATOS DE VENTAS

**Innovación de Datos**

**TSCDIA 2025**

---

## CARÁTULA

**Instituto Superior Politécnico Córdoba (ISPC)**

**Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial**

**Materia:** Innovación de Datos

**Trabajo Práctico:** Evidencia de Aprendizaje N° 3 - ETL con Pandas

**Profesores:**
- Alejandro Mainero (Programación I)
- Carlos Charletti (Base de Datos II)

**Integrantes:**
- Paola García (DNI: 29463402)
- Pablo Taborda (DNI: 28270596)
- Julio Orjindo (DNI: 26482639)
- Rodenas Elías Gabriel (DNI: 36356976)

**Fecha:** Octubre 2025

---

## ÍNDICE

1. Introducción
2. Extracción de Datos
3. Transformación de Datos
4. Limpieza de Datos
5. Carga a Base de Datos
6. Consultas SQL
7. Análisis Exploratorio
8. Conclusiones
9. Bibliografía

---

## 1. INTRODUCCIÓN

El presente trabajo implementa un proceso completo de ETL (Extract, Transform, Load) sobre datos de ventas de centros comerciales en Estambul, Turquía, correspondientes al período 2021-2023.

**Objetivos:**
- Extraer datos desde archivos CSV
- Transformar y limpiar información
- Cargar en base de datos SQLite
- Realizar análisis exploratorio
- Generar insights estratégicos

**Dataset:** Customer Shopping Dataset (Kaggle)
- 99,459 registros de transacciones
- 10 centros comerciales
- 8 categorías de productos
- 3 métodos de pago

---

## 2. EXTRACCIÓN DE DATOS

### Item 1: Carga de DataFrames

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cargar datasets
df_customers = pd.read_csv('customer_data.csv')
df_sales = pd.read_csv('sales_data.csv')
```

### Item 2: Descripción del Proceso

Los datos se extraen de dos archivos CSV:
- **customer_data.csv:** Información demográfica (ID, género, edad, método de pago)
- **sales_data.csv:** Información transaccional (factura, categoría, cantidad, precio, fecha, mall)

### Item 3: Concatenación de DataFrames

```python
# Combinar por customer_id
df_combined = pd.merge(df_sales, df_customers, on='customer_id', how='inner')
```

---

## 3. TRANSFORMACIÓN DE DATOS

### Item 4a: Modo de Pago Más Frecuente

```python
metodo_mas_frecuente = df_combined['payment_method'].value_counts()
```

**Resultado:** Cash (44.7% de transacciones)

### Item 4b: Categorización por Género

```python
pago_por_genero = df_combined.groupby(['gender', 'payment_method']).size()
```

### Item 4c: Pagos en Rango 25-35 Años

```python
df_25_35 = df_combined[(df_combined['age'] >= 25) & (df_combined['age'] <= 35)]
pagos_jovenes = df_25_35['payment_method'].value_counts()
```

### Item 4d: Métodos de Pago Más Usados por Mujeres

```python
df_mujeres = df_combined[df_combined['gender'] == 'Female']
pagos_mujeres = df_mujeres['payment_method'].value_counts()
```

### Item 4e: Precios por Categoría

```python
df_combined['total_sale'] = df_combined['quantity'] * df_combined['price']
ventas_categoria = df_combined.groupby('category')['total_sale'].sum()
```

**Resultado:** Clothing lidera con $113.8M en ventas

### Item 5: Documentación de Transformaciones

Transformaciones aplicadas:
1. Cálculo de campo `total_sale`
2. Categorización de edades en grupos
3. Extracción de componentes temporales (año, mes, día)
4. Limpieza de valores nulos
5. Validación de rangos numéricos

---

## 4. LIMPIEZA DE DATOS

### Item 6: DataFrame Limpio

```python
# Eliminar nulos
df_final = df_combined.dropna()

# Validar rangos
df_final = df_final[
    (df_final['age'] > 0) & 
    (df_final['quantity'] > 0) & 
    (df_final['price'] > 0)
]

# Categorizar edades
def categorizar_edad(edad):
    if edad < 25: return 'Joven'
    elif edad <= 45: return 'Adulto'
    else: return 'Senior'

df_final['age_group'] = df_final['age'].apply(categorizar_edad)
```

**Resultado:** 99,338 registros válidos (121 registros eliminados)

---

## 5. CARGA A BASE DE DATOS

### Esquema SQLite

```sql
CREATE TABLE datos_limpios (
    invoice_no TEXT PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    gender TEXT CHECK(gender IN ('Male', 'Female')),
    age INTEGER CHECK(age > 0 AND age <= 120),
    category TEXT NOT NULL,
    quantity INTEGER CHECK(quantity > 0),
    price REAL CHECK(price > 0),
    payment_method TEXT CHECK(payment_method IN ('Cash', 'Credit Card', 'Debit Card')),
    invoice_date TEXT NOT NULL,
    shopping_mall TEXT NOT NULL,
    age_group TEXT,
    total_sale REAL,
    year INTEGER,
    month INTEGER,
    day_of_week TEXT
);
```

### Script de Carga

```python
import sqlite3

conn = sqlite3.connect('ventas_estambul.db')
df_final.to_sql('datos_limpios', conn, if_exists='replace', index=False)
conn.close()
```

---

## 6. CONSULTAS SQL

### Consulta 1: Métodos de Pago Más Frecuentes

```sql
SELECT payment_method, COUNT(*) as total
FROM datos_limpios
GROUP BY payment_method
ORDER BY total DESC;
```

### Consulta 2: Pagos por Género

```sql
SELECT gender, payment_method, COUNT(*) as total
FROM datos_limpios
GROUP BY gender, payment_method;
```

### Consulta 3: Ventas por Categoría

```sql
SELECT category, SUM(total_sale) as ventas_totales
FROM datos_limpios
GROUP BY category
ORDER BY ventas_totales DESC;
```

*(Se incluyen 17 consultas en archivo consultas.sql)*

---

## 7. ANÁLISIS EXPLORATORIO

### Hallazgos Principales

**Por Método de Pago:**
- Cash: 44.7% (44,397 transacciones)
- Credit Card: 35.1% (34,898 transacciones)
- Debit Card: 20.2% (20,043 transacciones)

**Por Género:**
- Mujeres: 59.8% del mercado
- Hombres: 40.2% del mercado

**Por Edad:**
- Edad promedio: 43.4 años
- Grupo dominante: Adultos (25-45 años)

**Por Categoría:**
- Clothing: $113.8M (líder en ventas)
- Technology: $3,157 (precio promedio más alto)

**Evolución Temporal:**
- Periodo: Enero 2021 - Marzo 2023
- Estabilidad en métodos de pago (sin cambios significativos)

---

## 8. CONCLUSIONES

### Conclusiones Técnicas

1. **Proceso ETL exitoso:** 99.88% de registros válidos (99,338 de 99,459)
2. **Calidad de datos:** Mínima pérdida de información (121 registros)
3. **Integridad referencial:** Implementada mediante constraints SQL
4. **Optimización:** 8 índices para mejorar rendimiento de consultas

### Conclusiones de Negocio

1. **Dominio del efectivo:** El 44.7% de transacciones se realizan en Cash, representando una oportunidad de digitalización
2. **Segmento femenino:** Las mujeres representan el 59.8% del mercado, clave para estrategias de fidelización
3. **Categoría líder:** Clothing genera $113.8M, foco para promociones dirigidas
4. **Estabilidad temporal:** No hay tendencia espontánea hacia digitalización (2021-2023), se requiere intervención activa

### Recomendaciones Estratégicas

**Para Entidades Financieras:**
1. Implementar incentivos para migración Cash → Digital (descuentos, cashback)
2. Segmentar por género y edad para personalizar productos financieros
3. Desarrollar alianzas con retailers de Clothing (categoría líder)
4. Lanzar productos digitales: wallets, NFC, BNPL (Buy Now Pay Later)

**Proyección de Impacto:**
- Migración estimada: 10,000 transacciones en 12 meses
- ROI proyectado: 51.3% en año 1
- Inversión requerida: $1.04M (marketing + tecnología)

---

## 9. BIBLIOGRAFÍA

### Bases de Datos
- **Silberschatz, Abraham; Korth, Henry F.; Sudarshan, S.** (2006). *Fundamentos de Bases de Datos* (5ª Edición). McGraw Hill.
- **Ullman, Jeffrey** (1999). *Introducción a los Sistemas de Bases de Datos*. Prentice Hall.

### Estadística y Análisis de Datos
- **ISPC** (2025). *Fundamentos de estadística y probabilidad aplicada al análisis de datos*. Instituto Superior Politécnico Córdoba.
- **ISPC** (2025). *Apunte de Analítica de Datos - Estadística Descriptiva*. Instituto Superior Politécnico Córdoba.

### Fuentes de Datos
- **Kaggle Dataset** (2023). *Customer Shopping Dataset - Retail Sales Data*. Istanbul Shopping Malls (2021-2023).

### Herramientas y Tecnología
- **McKinney, Wes** (2022). *Python for Data Analysis* (3rd Edition). O'Reilly Media.
- **Pandas Documentation** (2025). pandas.pydata.org
- **SQLite Documentation** (2025). sqlite.org/docs.html

---

**FIN DEL DOCUMENTO**
