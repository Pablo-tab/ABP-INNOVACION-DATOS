# 📚 GUÍA PASO A PASO - PROYECTO ETL
## Manual Detallado para Replicar el Proyecto

**Para:** Paola, Julio, Elías
**De:** Pablo
**Fecha:** Octubre 2025

---

## 🎯 ¿QUÉ VAMOS A HACER?

Este proyecto consiste en:
1. **Extraer** datos de 2 archivos CSV
2. **Transformar** y limpiar esos datos
3. **Cargar** todo en una base de datos SQLite
4. **Analizar** y generar conclusiones estratégicas

**Resultado final:** Simular una consultoría para un banco que quiere digitalizar pagos.

---

## 📋 PASO 0: PREPARACIÓN INICIAL

### ¿Qué necesitamos instalado?

1. **Python 3.8 o superior**
   - Verificar: Abrir PowerShell y escribir `python --version`
   - Si no está: Descargar desde python.org

2. **Bibliotecas de Python**
   ```powershell
   pip install pandas numpy matplotlib jupyter sqlite3
   ```

3. **Editor de código** (ya tienes VS Code ✅)

4. **DB Browser for SQLite** (opcional, para ver la base de datos)
   - Descargar: https://sqlitebrowser.org/

---

## 📁 PASO 1: ENTENDER LA ESTRUCTURA

```
ABP INNOVACION/
│
├── customer_data.csv          👈 Datos de clientes
├── sales_data.csv             👈 Datos de ventas
│
├── notebooks/
│   └── analisis_etl.ipynb     👈 ARCHIVO PRINCIPAL (aquí trabajamos)
│
├── sql/
│   ├── schema.sql             👈 Estructura de la base de datos
│   └── consultas.sql          👈 17 consultas SQL
│
├── datos/
│   └── datos_limpios.csv      👈 (Se genera después)
│
└── visualizaciones/           👈 (Se generan gráficos aquí)
```

---

## 🔧 PASO 2: ABRIR Y ENTENDER EL NOTEBOOK

### 2.1 Abrir Jupyter Notebook

**Opción A - Desde VS Code:**
1. Abrir VS Code
2. Abrir la carpeta: `ABP INNOVACION`
3. Click derecho en `notebooks/analisis_etl.ipynb`
4. Click en "Open With" → "Jupyter Notebook"
5. Arriba a la derecha, seleccionar Kernel de Python

**Opción B - Desde terminal:**
```powershell
cd "C:\Users\PABLO\Desktop\TECNICATURA\ABP INNOVACION"
jupyter notebook
```
Luego ir a: `notebooks/analisis_etl.ipynb`

### 2.2 Estructura del Notebook

El notebook tiene **10 secciones**:

1️⃣ **Importar bibliotecas** (pandas, numpy, matplotlib)
2️⃣ **Cargar archivos CSV** → DataFrames
3️⃣ **Combinar datos** → Merge
4️⃣ **Limpiar datos** → Eliminar nulos, validar rangos
5️⃣ **Transformar datos** → Crear nuevas columnas
6️⃣ **Guardar CSV limpio** → `datos_limpios.csv`
7️⃣ **Análisis exploratorio** → Estadísticas
8️⃣ **Visualizaciones** → 10 gráficos PNG
9️⃣ **Resumen** → Tabla final
🔟 **Conclusiones** → Insights estratégicos

---

## ▶️ PASO 3: EJECUTAR EL NOTEBOOK (CELDA POR CELDA)

### ⚠️ IMPORTANTE: NO ejecutar todo de golpe. Ir celda por celda.

### Celda 1: Importar Bibliotecas
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

**Qué hace:** Carga las herramientas que vamos a usar.
**Si da error:** Instalar con `pip install pandas numpy matplotlib`

**Presionar:** `Shift + Enter` para ejecutar

---

### Celda 2: Cargar customer_data.csv
```python
df_customers = pd.read_csv('../customer_data.csv')
print(f"Clientes cargados: {len(df_customers)}")
df_customers.head()
```

**Qué hace:** Lee el archivo de clientes.
**Deberías ver:** "Clientes cargados: 99459" y una tabla con 5 filas.

**¿Qué es `df_customers`?**
- Es un **DataFrame** (como una tabla de Excel en Python)
- Tiene columnas: `customer_id`, `gender`, `age`, `payment_method`

---

### Celda 3: Cargar sales_data.csv
```python
df_sales = pd.read_csv('../sales_data.csv')
print(f"Ventas cargadas: {len(df_sales)}")
df_sales.head()
```

**Qué hace:** Lee el archivo de ventas.
**Deberías ver:** "Ventas cargadas: 99459" y una tabla.

**¿Qué tiene `df_sales`?**
- Columnas: `invoice_no`, `customer_id`, `category`, `quantity`, `price`, `invoice_date`, `shopping_mall`

---

### Celda 4: Combinar (MERGE) ambos DataFrames
```python
df_combined = pd.merge(df_sales, df_customers, on='customer_id', how='inner')
print(f"Registros combinados: {len(df_combined)}")
df_combined.head()
```

**Qué hace:** Une las dos tablas por `customer_id`.

**Analogía:** Es como hacer un `JOIN` en SQL.
- Si un cliente ID=1001 compró 3 productos → aparecerán 3 filas
- Cada fila tiene TODA la info: venta + datos del cliente

**Deberías ver:** "Registros combinados: 99459"

---

### Celda 5: Revisar valores nulos
```python
print(df_combined.isnull().sum())
```

**Qué hace:** Cuenta cuántos valores vacíos hay en cada columna.

**Interpretación:**
- Si sale `age: 50` → Hay 50 clientes sin edad
- Si sale `price: 0` → Todas las ventas tienen precio ✅

---

### Celda 6: Limpiar valores nulos
```python
df_final = df_combined.dropna()
print(f"Registros antes: {len(df_combined)}")
print(f"Registros después: {len(df_final)}")
print(f"Eliminados: {len(df_combined) - len(df_final)}")
```

**Qué hace:** Elimina filas con datos vacíos.

**Deberías ver:**
```
Registros antes: 99459
Registros después: 99338
Eliminados: 121
```

**Explicación:** Perdimos solo 121 registros = 0.12% → Muy buena calidad de datos ✅

---

### Celda 7: Validar rangos numéricos
```python
df_final = df_final[
    (df_final['age'] > 0) & (df_final['age'] <= 120) &
    (df_final['quantity'] > 0) &
    (df_final['price'] > 0)
]
```

**Qué hace:** Filtra datos inválidos.

**Ejemplos de lo que elimina:**
- Edades negativas o mayores a 120 años
- Cantidades = 0 (imposible vender 0 unidades)
- Precios negativos o cero

---

### Celda 8: Crear columna `total_sale`
```python
df_final['total_sale'] = df_final['quantity'] * df_final['price']
df_final['total_sale'].describe()
```

**Qué hace:** Calcula el total de cada venta.

**Ejemplo:**
- Si compraste 2 zapatos a $150 c/u → `total_sale = 2 × 150 = $300`

**Deberías ver:** Estadísticas (media, mínimo, máximo, etc.)

---

### Celda 9: Categorizar edades
```python
def categorizar_edad(edad):
    if edad < 25:
        return 'Joven'
    elif edad <= 45:
        return 'Adulto'
    else:
        return 'Senior'

df_final['age_group'] = df_final['age'].apply(categorizar_edad)
df_final['age_group'].value_counts()
```

**Qué hace:** Crea grupos de edades.

**Deberías ver algo como:**
```
Adulto: 45000
Senior: 35000
Joven: 19338
```

---

### Celda 10: Extraer componentes de fecha
```python
df_final['invoice_date'] = pd.to_datetime(df_final['invoice_date'])
df_final['year'] = df_final['invoice_date'].dt.year
df_final['month'] = df_final['invoice_date'].dt.month
df_final['day_of_week'] = df_final['invoice_date'].dt.day_name()
```

**Qué hace:** De una fecha como "2023-05-15" extrae:
- `year` → 2023
- `month` → 5
- `day_of_week` → "Monday"

**¿Para qué?** Para analizar tendencias temporales.

---

### Celda 11: Guardar CSV limpio
```python
df_final.to_csv('../datos/datos_limpios.csv', index=False)
print("✅ Archivo guardado: datos/datos_limpios.csv")
```

**Qué hace:** Guarda el DataFrame limpio en un CSV.

**Verificar:** Debería aparecer el archivo en la carpeta `datos/`

---

### Celdas 12-21: Visualizaciones (10 gráficos)

Cada celda genera un gráfico PNG y lo guarda en `visualizaciones/`

**Ejemplo - Gráfico 1: Métodos de Pago**
```python
plt.figure(figsize=(10, 6))
df_final['payment_method'].value_counts().plot(kind='bar', color='steelblue')
plt.title('Distribución de Métodos de Pago')
plt.xlabel('Método de Pago')
plt.ylabel('Cantidad de Transacciones')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('../visualizaciones/01_metodos_pago.png', dpi=300)
plt.show()
```

**Qué hace:**
1. Crea una figura de 10x6 pulgadas
2. Cuenta cuántas veces aparece cada método de pago
3. Genera un gráfico de barras
4. Guarda como PNG de alta calidad (300 DPI)
5. Muestra el gráfico

**Repetir esto para los 10 gráficos** (ya están en el notebook).

---

### Celda 22: Resumen Estadístico
```python
print("=== RESUMEN GENERAL ===")
print(f"Total registros: {len(df_final)}")
print(f"Ventas totales: ${df_final['total_sale'].sum():,.2f}")
print(f"Ticket promedio: ${df_final['total_sale'].mean():,.2f}")
```

**Qué hace:** Muestra números clave del negocio.

---

### Celda 23: Conclusiones
```python
# Análisis de métodos de pago
metodos = df_final['payment_method'].value_counts()
print("\n=== MÉTODOS DE PAGO ===")
for metodo, cantidad in metodos.items():
    porcentaje = (cantidad / len(df_final)) * 100
    print(f"{metodo}: {cantidad:,} ({porcentaje:.1f}%)")
```

**Deberías ver:**
```
Cash: 44,397 (44.7%)
Credit Card: 34,898 (35.1%)
Debit Card: 20,043 (20.2%)
```

---

## 💾 PASO 4: CREAR LA BASE DE DATOS

### 4.1 Ejecutar el script de carga

```powershell
python cargar_a_sqlite.py
```

**Qué hace el script:**
1. Lee `datos/datos_limpios.csv`
2. Crea la base de datos `ventas_estambul.db`
3. Ejecuta `sql/schema.sql` (crea la tabla)
4. Inserta los 99,338 registros
5. Crea 8 índices para optimizar consultas
6. Valida que todo esté correcto

**Deberías ver:**
```
✅ Base de datos creada: ventas_estambul.db
✅ Tabla creada con 99338 registros
✅ 8 índices creados
✅ Validación exitosa
```

---

### 4.2 Verificar la base de datos

**Opción A - DB Browser for SQLite:**
1. Abrir DB Browser
2. File → Open Database
3. Seleccionar `ventas_estambul.db`
4. Ver tabla `datos_limpios`

**Opción B - Python:**
```python
import sqlite3
conn = sqlite3.connect('ventas_estambul.db')
df_test = pd.read_sql("SELECT * FROM datos_limpios LIMIT 5", conn)
print(df_test)
conn.close()
```

---

## 🔍 PASO 5: EJECUTAR CONSULTAS SQL

### 5.1 Abrir el archivo `sql/consultas.sql`

Contiene 17 consultas. Ejemplos:

**Consulta 1: Métodos de pago más frecuentes**
```sql
SELECT payment_method, COUNT(*) as total
FROM datos_limpios
GROUP BY payment_method
ORDER BY total DESC;
```

**Consulta 4: Top 5 categorías por ventas**
```sql
SELECT category, SUM(total_sale) as ventas_totales
FROM datos_limpios
GROUP BY category
ORDER BY ventas_totales DESC
LIMIT 5;
```

### 5.2 Ejecutar consultas

**Opción A - DB Browser:**
1. Pestaña "Execute SQL"
2. Copiar consulta
3. Click en "Play" (▶️)

**Opción B - Python:**
```python
import sqlite3
conn = sqlite3.connect('ventas_estambul.db')

# Copiar consulta aquí
query = """
SELECT payment_method, COUNT(*) as total
FROM datos_limpios
GROUP BY payment_method
ORDER BY total DESC;
"""

resultado = pd.read_sql(query, conn)
print(resultado)
conn.close()
```

---

## 📊 PASO 6: ANÁLISIS PROFUNDO (Scripts Adicionales)

### 6.1 Análisis rápido de datos reales
```powershell
python analizar_datos_reales.py
```

**Qué hace:** Muestra estadísticas clave en consola.

**Output esperado:**
```
=== MÉTODOS DE PAGO ===
Cash: 44,397 (44.7%)
Credit Card: 34,898 (35.1%)
Debit Card: 20,043 (20.2%)

=== GÉNERO ===
Female: 59,415 (59.8%)
Male: 39,923 (40.2%)

=== CATEGORÍAS TOP 5 ===
Clothing: $113,826,140
Technology: $75,156,280
...
```

---

### 6.2 Análisis evolutivo de medios de pago
```powershell
python analisis_profundo_pagos.py
```

**Qué hace:** Analiza cómo evolucionaron los medios de pago 2021-2023.

**Genera 3 gráficos:**
1. `evolucion_mensual_pagos.png` - Tendencia mes a mes
2. `comparacion_anual_pagos.png` - Comparación por año
3. `pago_por_rango_precio.png` - Métodos según monto

**Hallazgo clave:** El efectivo se mantiene estable ~44.7% (no hay digitalización espontánea).

---

## 📄 PASO 7: DOCUMENTACIÓN ESTRATÉGICA

### 7.1 Leer el informe estratégico

Abrir: `informe/INFORME_ESTRATEGICO_ENTIDAD_FINANCIERA.txt`

**Contiene:**
1. Contexto del mercado
2. Hallazgos del análisis
3. Estrategia CVL (Customer Value Lifecycle)
4. Calendario de promociones
5. ROI proyectado (51.3%)
6. Productos futuros (NFC, Wallets, BNPL)

**¿Por qué es importante?**
- Diferencia nuestro proyecto de otros grupos
- Muestra visión de negocio, no solo técnica
- Simula una consultoría real

---

### 7.2 Investigar datos externos

Abrir: `CHECKLIST_DATOS_EXTERNOS.txt`

**Categorías:**
- Demografía de Estambul
- Sistema financiero de Turquía
- Retail (centros comerciales)
- Economía (inflación, tipo de cambio)
- Tecnología (bancarización, smartphones)
- Competencia (otros bancos)
- Cultura (preferencias de pago)
- Legal (regulaciones)

**Tarea:** Buscar datos reales en Google para enriquecer el análisis.

**Ejemplo:**
- Buscar "Turkey bancarization rate 2023"
- Agregar al documento: "Turquía tiene 67% de bancarización vs 44.7% uso efectivo en nuestro dataset"

---

## 📝 PASO 8: COMPLETAR EL DOCUMENTO FINAL

### 8.1 Usar el PROYECTO_ABP_CORREGIDO.md como base

Ya tiene:
- ✅ Nombres correctos
- ✅ Profesores correctos
- ✅ Materia correcta ("Innovación de Datos")
- ✅ Bibliografía completa

### 8.2 Agregar capturas de pantalla

**Qué capturar:**
1. Notebook ejecutado (cada celda con su output)
2. Gráficos generados
3. Consultas SQL ejecutadas
4. Resultado de scripts

**Cómo:**
1. Ejecutar celda
2. `Windows + Shift + S` (captura de pantalla)
3. Recortar el área
4. Pegar en Word

**Orden:**
- Código de la celda
- Output de la celda
- Gráfico (si lo genera)

---

## 🎯 PASO 9: ENTREGABLES FINALES

### Checklist de archivos a entregar:

- [ ] `PROYECTO ABP.docx` - Documento principal con capturas
- [ ] `notebooks/analisis_etl.ipynb` - Notebook ejecutado
- [ ] `ventas_estambul.db` - Base de datos SQLite
- [ ] `sql/schema.sql` - Esquema de BD
- [ ] `sql/consultas.sql` - 17 consultas SQL
- [ ] `datos/datos_limpios.csv` - Dataset procesado
- [ ] `visualizaciones/` - Carpeta con 13 PNGs
- [ ] `informe/INFORME_ESTRATEGICO_ENTIDAD_FINANCIERA.txt`
- [ ] `README.md` - Documentación del proyecto

---

## ❓ PREGUNTAS FRECUENTES

### P1: ¿Por qué usamos SQLite y no MariaDB?
**R:** Para simplificar. SQLite no requiere instalación de servidor, es un solo archivo `.db`.

### P2: ¿Qué es un DataFrame?
**R:** Es como una tabla de Excel en Python. Tiene filas, columnas y podés hacer operaciones.

### P3: ¿Qué significa "inner join"?
**R:** En el merge, solo conserva registros que existen en AMBAS tablas.

### P4: ¿Por qué tantas visualizaciones?
**R:** Porque "una imagen vale más que mil palabras". Los gráficos comunican mejor que tablas.

### P5: ¿Qué es ETL?
**R:**
- **E**xtract: Sacar datos de CSVs
- **T**ransform: Limpiar y procesar
- **L**oad: Cargar en base de datos

### P6: ¿Qué es el ROI?
**R:** Return On Investment. Si invertís $100 y ganás $151, el ROI es 51%.

### P7: ¿Qué es CVL?
**R:** Customer Value Lifecycle. Estrategia para acompañar al cliente en 4 fases:
1. Adquisición
2. Activación
3. Retención
4. Monetización

---

## 🚨 ERRORES COMUNES Y SOLUCIONES

### Error: "ModuleNotFoundError: No module named 'pandas'"
**Solución:**
```powershell
pip install pandas
```

### Error: "FileNotFoundError: customer_data.csv not found"
**Solución:** Verificar que estás en la carpeta correcta:
```powershell
cd "C:\Users\PABLO\Desktop\TECNICATURA\ABP INNOVACION"
```

### Error: "OperationalError: no such table: datos_limpios"
**Solución:** Ejecutar primero `cargar_a_sqlite.py` para crear la BD.

### Error: Las visualizaciones no se guardan
**Solución:** Crear la carpeta manualmente:
```powershell
mkdir visualizaciones
```

### Error: "KeyError: 'payment_method'"
**Solución:** El DataFrame no tiene esa columna. Verificar que ejecutaste el merge primero.

---

## 🎓 CONCEPTOS CLAVE PARA EL EXAMEN

### Pandas
- `read_csv()` - Leer archivos
- `merge()` - Combinar DataFrames
- `dropna()` - Eliminar nulos
- `groupby()` - Agrupar datos
- `apply()` - Aplicar funciones
- `to_csv()` / `to_sql()` - Exportar

### SQL
- `SELECT` - Consultar
- `WHERE` - Filtrar
- `GROUP BY` - Agrupar
- `ORDER BY` - Ordenar
- `JOIN` - Combinar tablas
- `COUNT()`, `SUM()`, `AVG()` - Agregaciones

### Estadística
- Media (promedio)
- Mediana (valor central)
- Moda (más frecuente)
- Desviación estándar (dispersión)
- Percentiles (cuartiles)

---

## 📞 SI NECESITAN AYUDA

**Pablo Taborda**
- WhatsApp: [Tu número]
- Email: [Tu email]

**Horarios disponibles:**
- Lunes a Viernes: 18:00 - 22:00 hs
- Sábados: 10:00 - 18:00 hs

---

## ✅ RESUMEN DE 5 MINUTOS

1. **Instalar:** Python, pandas, numpy, matplotlib, jupyter
2. **Abrir:** `notebooks/analisis_etl.ipynb`
3. **Ejecutar:** Todas las celdas con `Shift + Enter`
4. **Resultado:** 10 gráficos PNG + datos_limpios.csv
5. **Cargar BD:** `python cargar_a_sqlite.py`
6. **Consultas:** Ejecutar `sql/consultas.sql`
7. **Documentar:** Tomar capturas y armar Word
8. **Diferenciarse:** Leer informe estratégico, investigar datos externos

---

**¡ÉXITO EN EL PROYECTO! 🚀**

**Recordá:** Este trabajo simula una consultoría real. No es solo un TP técnico, es una propuesta de negocio para un banco. Eso nos diferencia del resto.

**Pregunta clave del profesor:** "¿Qué recomendarían a la entidad financiera?"
**Nuestra respuesta:** "Estrategia CVL con ROI 51.3% y migración de 10,000 transacciones en 12 meses"

💪 ¡Nos vemos en la presentación!
