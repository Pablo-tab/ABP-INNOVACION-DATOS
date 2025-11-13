# 🎤 GUÍA DE PRESENTACIÓN ORAL - 15 MINUTOS (4 PERSONAS)

## ⏱️ DISTRIBUCIÓN DE TIEMPOS

**Total: 15 minutos = 4 personas × ~3.5 min c/u**

| Persona | Minutos | Tema | Diapositivas sugeridas |
|---------|---------|------|------------------------|
| **Persona 1** | 3-4 min | Introducción + ETL Extract | 3-4 slides |
| **Persona 2** | 3-4 min | ETL Transform + Librerías | 3-4 slides |
| **Persona 3** | 3-4 min | ETL Load + SQL | 3-4 slides |
| **Persona 4** | 3-4 min | Resultados + Conclusiones | 3-4 slides |

---

## 📊 ESTRUCTURA DE LA PRESENTACIÓN

### 🟦 **PERSONA 1: INTRODUCCIÓN + EXTRACT (3-4 min)**

#### **SLIDE 1: PORTADA (15 seg)**
```
┌─────────────────────────────────────────┐
│  ANÁLISIS ETL DE DATOS DE VENTAS       │
│  Centro Comercial - Estambul            │
│                                         │
│  Dataset: 99,459 transacciones         │
│  Período: 2021-2023                     │
│                                         │
│  Equipo: [Nombres]                      │
│  Profesores: Mainero & Charletti        │
└─────────────────────────────────────────┘
```

**Qué decir:**
> "Buenos días/tardes. Nuestro proyecto consiste en un análisis ETL completo de 99,459 transacciones de un centro comercial en Estambul entre 2021 y 2023. Aplicamos los conceptos de Programación I y Base de Datos II para extraer, transformar y cargar datos, generando insights estratégicos."

---

#### **SLIDE 2: ¿QUÉ ES ETL? (30 seg)**
```
┌─────────────────────────────────────────┐
│  ETL = Extract + Transform + Load      │
│                                         │
│  📥 EXTRACT                             │
│     └─ Obtener datos desde fuentes     │
│                                         │
│  🔄 TRANSFORM                           │
│     └─ Limpiar, calcular, validar      │
│                                         │
│  📤 LOAD                                │
│     └─ Cargar a base de datos          │
│                                         │
│  CONCEPTO TEÓRICO:                      │
│  ✅ Integración de datos (BD II)        │
│  ✅ Automatización (Prog I)             │
└─────────────────────────────────────────┘
```

**Qué decir:**
> "ETL es el proceso estándar en Data Engineering: Extract para obtener datos de fuentes, Transform para limpiar y enriquecer, y Load para cargar a un destino. Este concepto es fundamental en Data Warehousing, tema de Base de Datos II."

**⚠️ ANTICIPAR PREGUNTA:**
- **P: "¿Por qué no usar directamente SQL para todo?"**
- **R:** "SQL es excelente para consultas, pero Pandas ofrece 50+ funciones de transformación que serían complejas en SQL puro. Además, Python permite automatización completa del pipeline."

---

#### **SLIDE 3: FASE EXTRACT (1.5 min)**
```
┌─────────────────────────────────────────┐
│  📥 EXTRACT: Carga de datos            │
│                                         │
│  import pandas as pd                    │
│                                         │
│  df_sales = pd.read_csv(                │
│      'sales_data.csv'                   │
│  )  # 99,459 filas                      │
│                                         │
│  df_customers = pd.read_csv(            │
│      'customer_data.csv'                │
│  )  # Info demográfica                  │
│                                         │
│  RESULTADO:                             │
│  ✅ 2 DataFrames en memoria             │
│  ✅ ~12 MB de datos                     │
│  ✅ 3 segundos de carga                 │
└─────────────────────────────────────────┘
```

**Qué decir:**
> "En la fase Extract, utilizamos Pandas para cargar dos archivos CSV: ventas y clientes. Pandas es una librería de Python especializada en manipulación de datos tabulares. En 3 segundos cargamos 99,459 transacciones en memoria como DataFrames, que son estructuras similares a tablas SQL pero en RAM."

**MOSTRAR EN PANTALLA:**
- Ejecutar celda de carga en Colab
- Mostrar `df_sales.head()` y `df_sales.info()`
- Destacar columnas clave: `invoice_no`, `customer_id`, `price`, `quantity`

**⚠️ ANTICIPAR PREGUNTAS:**
- **P: "¿Qué es un DataFrame?"**
- **R:** "Es una estructura de datos bidimensional de Pandas, similar a una tabla SQL o Excel. Cada columna tiene un tipo de dato y podemos aplicar operaciones vectorizadas muy rápidas."

- **P: "¿Por qué no usar listas de Python puro?"**
- **R:** "Pandas está optimizado en C. Un loop con 99,459 registros tomaría segundos, mientras Pandas procesa en milisegundos gracias a vectorización."

---

#### **SLIDE 4: MERGE - COMBINACIÓN (1 min)**
```
┌─────────────────────────────────────────┐
│  🔗 MERGE: Combinación de tablas       │
│                                         │
│  df_combined = pd.merge(                │
│      df_sales,                          │
│      df_customers,                      │
│      on='customer_id',                  │
│      how='left'                         │
│  )                                      │
│                                         │
│  EQUIVALENTE SQL:                       │
│  SELECT * FROM sales                    │
│  LEFT JOIN customers                    │
│    ON sales.customer_id =               │
│       customers.customer_id             │
│                                         │
│  CONCEPTO TEÓRICO: JOIN (BD II)         │
└─────────────────────────────────────────┘
```

**Qué decir:**
> "Utilizamos `pd.merge()` que es equivalente a un LEFT JOIN en SQL. Unimos las dos tablas por `customer_id`, preservando todas las ventas incluso si no tienen información demográfica. Esto nos da un DataFrame de 99,459 filas con 11 columnas combinadas."

**MOSTRAR EN PANTALLA:**
- `df_combined.shape` → (99459, 11)
- `df_combined.head()` mostrando columnas de ambos DataFrames

**⚠️ ANTICIPAR PREGUNTA:**
- **P: "¿Por qué LEFT JOIN y no INNER JOIN?"**
- **R:** "Porque queremos conservar TODAS las ventas. Un INNER JOIN eliminaría transacciones sin datos de cliente, perdiendo información de negocio crítica."

---

### 🟩 **PERSONA 2: TRANSFORM + LIBRERÍAS (3-4 min)**

#### **SLIDE 5: LIBRERÍAS UTILIZADAS (1 min)**
```
┌─────────────────────────────────────────┐
│  📚 LIBRERÍAS DEL PROYECTO              │
│                                         │
│  1. PANDAS (Transformación)             │
│     └─ Manipulación de datos           │
│     └─ Limpieza, cálculos, merge       │
│                                         │
│  2. NUMPY (Operaciones numéricas)       │
│     └─ Arrays multidimensionales       │
│     └─ Funciones matemáticas           │
│                                         │
│  3. SQLITE3 (Persistencia)              │
│     └─ Base de datos relacional        │
│     └─ Consultas SQL                    │
│                                         │
│  4. MATPLOTLIB (Visualización)          │
│     └─ Gráficos estadísticos           │
│     └─ Exportación PNG                  │
│                                         │
│  CONCEPTO TEÓRICO:                      │
│  ✅ Modularidad (Prog I - POO)          │
│  ✅ Abstracción de complejidad          │
└─────────────────────────────────────────┘
```

**Qué decir:**
> "Utilizamos cuatro librerías principales. **Pandas** para transformar datos con más de 50 funciones especializadas. **NumPy** para operaciones numéricas y arrays multidimensionales eficientes. **SQLite3** para persistir datos en una base relacional ACID-compliant. Y **Matplotlib** para visualización profesional. Cada librería abstrae complejidad: Pandas maneja optimización en C, NumPy usa vectorización SIMD, SQLite maneja transacciones, Matplotlib maneja renderizado de gráficos."

**⚠️ ANTICIPAR PREGUNTA:**
- **P: "¿Por qué no usar solo Python puro sin librerías?"**
- **R:** "Sería reinventar la rueda. Por ejemplo, un merge de 99,459 filas con loops anidados tomaría O(n²) = ~10 mil millones de comparaciones. Pandas lo hace en O(n log n) con hash tables, 1000x más rápido."

---

#### **SLIDE 6: TRANSFORM - CONVERSIÓN DE FECHAS (1.5 min)**
```
┌─────────────────────────────────────────┐
│  🔄 TRANSFORM: Conversión de fechas    │
│                                         │
│  # Original: dd-mm-yyyy                 │
│  '15-03-2023'                           │
│                                         │
│  # Código:                              │
│  df['invoice_date'] = pd.to_datetime(  │
│      df['invoice_date'],                │
│      format='%d-%m-%Y'                  │
│  )                                      │
│                                         │
│  df['invoice_date'] = (                 │
│      df['invoice_date'].dt             │
│      .strftime('%Y-%m-%d')             │
│  )                                      │
│                                         │
│  # Resultado: ISO 8601                  │
│  '2023-03-15'                           │
│                                         │
│  ✅ SQL reconoce automáticamente        │
│  ✅ Ordenamiento correcto               │
└─────────────────────────────────────────┘
```

**Qué decir:**
> "La transformación más crítica fue convertir fechas de formato dd-mm-yyyy a ISO 8601 (yyyy-mm-dd). Usamos `pd.to_datetime()` para parsear con formato específico, evitando ambigüedades. Luego `strftime()` para formatear al estándar internacional. Esto garantiza que SQLite reconozca las fechas automáticamente y que el ordenamiento sea correcto."

**MOSTRAR EN PANTALLA:**
- Mostrar fecha antes: `'15-03-2023'`
- Mostrar fecha después: `'2023-03-15'`
- Ejecutar `df['invoice_date'].dtype` → object (string)

**⚠️ ANTICIPAR PREGUNTAS:**
- **P: "¿Por qué no dejar las fechas como estaban?"**
- **R:** (Mostrar en pantalla)
```sql
-- Con dd-mm-yyyy (orden INCORRECTO):
'01-12-2023' < '15-01-2023'  -- ❌ Ordena alfabéticamente

-- Con yyyy-mm-dd (orden CORRECTO):
'2023-01-15' < '2023-12-01'  -- ✅ Orden cronológico
```

- **P: "¿Qué es ISO 8601?"**
- **R:** "Es el estándar internacional de fechas (yyyy-mm-dd). Usado por bases de datos, APIs REST, sistemas distribuidos. Evita ambigüedades entre 03/04/2023 (¿marzo 4 o abril 3?)."

---

#### **SLIDE 7: TRANSFORM - COLUMNAS CALCULADAS (1.5 min)**
```
┌─────────────────────────────────────────┐
│  🔄 TRANSFORM: Columnas derivadas      │
│                                         │
│  # 1. Total de venta                    │
│  df['total_sale'] = (                   │
│      df['quantity'] * df['price']       │
│  )                                      │
│                                         │
│  # 2. Extracción temporal               │
│  df['year'] = (                         │
│      df['invoice_date'].dt.year         │
│  )                                      │
│  df['month'] = (                        │
│      df['invoice_date'].dt.month        │
│  )                                      │
│                                         │
│  DECISIÓN: Persistir en DB              │
│  ✅ Calcular UNA VEZ                    │
│  ✅ Consultas SQL más rápidas           │
│                                         │
│  CONCEPTO TEÓRICO:                      │
│  Materialización de cálculos (BD II)    │
└─────────────────────────────────────────┘
```

**Qué decir:**
> "Creamos tres columnas derivadas. `total_sale` multiplica cantidad por precio. `year` y `month` extraen componentes temporales para análisis. La decisión clave fue PERSISTIR estos cálculos en la base de datos en lugar de recalcularlos en cada query. Esto es un trade-off consciente: gastamos espacio para ganar velocidad."

**MOSTRAR EN PANTALLA:**
- `df[['quantity', 'price', 'total_sale']].head()`
- Comparar tiempos:
```python
# Sin columna (recalcular):
%timeit -n 100 df['quantity'] * df['price']  # ~5ms

# Con columna (ya calculada):
%timeit -n 100 df['total_sale']  # ~0.5ms
```

**⚠️ ANTICIPAR PREGUNTA:**
- **P: "¿No es redundante guardar total_sale si ya tenemos quantity y price?"**
- **R:** "Sí, hay redundancia. Pero priorizamos OLAP (analítica) sobre OLTP (transacciones). En Data Warehouses, la desnormalización controlada es estándar para optimizar queries de lectura que se ejecutan miles de veces."

---

### 🟨 **PERSONA 3: LOAD + SQL (3-4 min)**

#### **SLIDE 8: LIMPIEZA DE NULOS (1 min)**
```
┌─────────────────────────────────────────┐
│  🧹 TRANSFORM: Limpieza de nulos       │
│                                         │
│  # Identificar nulos                    │
│  print(df.isnull().sum())               │
│                                         │
│  age            119                     │
│  price            0                     │
│  category         0                     │
│  ...                                    │
│                                         │
│  # Eliminar selectivamente              │
│  df_clean = df.dropna(                  │
│      subset=['age']                     │
│  )                                      │
│                                         │
│  RESULTADO:                             │
│  99,457 → 99,338 filas                  │
│  Tasa recuperación: 99.88%              │
│                                         │
│  CONCEPTO TEÓRICO:                      │
│  Calidad de datos (BD II)               │
└─────────────────────────────────────────┘
```

**Qué decir:**
> "Identificamos 119 registros con age nulo. Aplicamos `dropna()` selectivo solo en columnas críticas, preservando el 99.88% de los datos. Esta decisión se justifica porque age es esencial para el análisis demográfico y segmentación de clientes. La transparencia es clave: logueamos cuántos registros eliminamos."

**MOSTRAR EN PANTALLA:**
- `df.isnull().sum()` antes
- Mensaje: "Eliminando 119 registros con age nulo"
- `df_clean.shape` después

**⚠️ ANTICIPAR PREGUNTA:**
- **P: "¿Por qué no rellenar (fillna) en vez de eliminar?"**
- **R:** "Rellenar customer_id con 0 o 'desconocido' generaría datos falsos. En análisis, es preferible reconocer datos faltantes que inventar valores. Si tuviéramos más contexto de negocio, podríamos imputar inteligentemente, pero sin eso, eliminar es más honesto."

---

#### **SLIDE 9: LOAD - CARGA A SQLITE (1.5 min)**
```
┌─────────────────────────────────────────┐
│  📤 LOAD: Carga a base de datos        │
│                                         │
│  import sqlite3                         │
│                                         │
│  conn = sqlite3.connect(                │
│      'sql/ventas.db'                    │
│  )                                      │
│                                         │
│  df_clean.to_sql(                       │
│      'datos_limpios',                   │
│      conn,                              │
│      if_exists='replace',               │
│      index=False                        │
│  )                                      │
│                                         │
│  RESULTADO:                             │
│  ✅ 99,338 filas cargadas               │
│  ✅ Base de datos: 15 MB                │
│  ✅ Tiempo: ~5 segundos                 │
│                                         │
│  CONCEPTO TEÓRICO:                      │
│  Persistencia relacional (BD II)        │
└─────────────────────────────────────────┘
```

**Qué decir:**
> "En la fase Load, usamos SQLite para persistir los datos transformados. `to_sql()` crea automáticamente la tabla, infiere tipos de datos, y ejecuta INSERTs en batches de 1000 filas. El parámetro `if_exists='replace'` permite reejecutar el ETL en desarrollo. En producción, usaríamos 'append' para cargas incrementales."

**MOSTRAR EN PANTALLA:**
- Ejecutar celda de carga
- Mostrar archivo `ventas.db` en explorador (15 MB)
- Ejecutar en Colab:
```python
cursor.execute('SELECT COUNT(*) FROM datos_limpios')
print(f"✅ {cursor.fetchone()[0]} registros")
```

**⚠️ ANTICIPAR PREGUNTAS:**
- **P: "¿Por qué SQLite y no MySQL/PostgreSQL?"**
- **R:** "SQLite es perfecto para análisis local: sin servidor, archivo único, portable, ACID-compliant. Para este volumen (15 MB), no necesitamos la complejidad de un servidor. En producción con múltiples usuarios concurrentes, sí usaríamos PostgreSQL."

- **P: "¿Qué significa ACID?"**
- **R:** "Atomicity, Consistency, Isolation, Durability. Garantías de integridad transaccional. Si falla la carga a mitad, SQLite hace rollback automático, no quedamos con datos parciales."

---

#### **SLIDE 10: CONSULTAS SQL (1.5 min)**
```
┌─────────────────────────────────────────┐
│  🔍 CONSULTAS SQL - Ejemplos           │
│                                         │
│  -- Item 5a: Ventas mensuales           │
│  SELECT                                 │
│      STRFTIME('%Y-%m', invoice_date)    │
│          AS mes,                        │
│      SUM(total_sale) AS ventas          │
│  FROM datos_limpios                     │
│  GROUP BY mes                           │
│  ORDER BY mes;                          │
│                                         │
│  -- Item 5b: Top 5 categorías           │
│  SELECT category,                       │
│      SUM(quantity) AS unidades          │
│  FROM datos_limpios                     │
│  GROUP BY category                      │
│  ORDER BY unidades DESC                 │
│  LIMIT 5;                               │
│                                         │
│  CONCEPTOS TEÓRICOS:                    │
│  ✅ Agregación (SUM, COUNT)             │
│  ✅ Agrupamiento (GROUP BY)             │
│  ✅ Ordenamiento (ORDER BY)             │
└─────────────────────────────────────────┘
```

**Qué decir:**
> "Ejecutamos 4 consultas SQL para responder los Items del TP. Primera consulta: ventas mensuales usando STRFTIME para formatear fechas y SUM para agregar. Segunda: Top 5 categorías con GROUP BY y ORDER BY. Estas son consultas estándar de Business Intelligence."

**MOSTRAR EN PANTALLA:**
- Ejecutar queries en notebook
- Mostrar resultados en formato tabla
- Destacar: "Clothing: 24,685 unidades vendidas"

**⚠️ ANTICIPAR PREGUNTA:**
- **P: "¿Cuál es la diferencia entre WHERE y HAVING?"**
- **R:** "WHERE filtra filas ANTES de agrupar. HAVING filtra grupos DESPUÉS de agrupar. Ejemplo: WHERE para 'ventas del 2023', HAVING para 'categorías con más de 1000 ventas'."

---

### 🟥 **PERSONA 4: RESULTADOS + CONCLUSIONES (3-4 min)**

#### **SLIDE 11: VISUALIZACIONES (1.5 min)**
```
┌─────────────────────────────────────────┐
│  📊 VISUALIZACIONES - Matplotlib        │
│                                         │
│  import matplotlib.pyplot as plt        │
│                                         │
│  plt.figure(figsize=(12, 6))            │
│  plt.plot(meses, ventas, marker='o')    │
│  plt.title('Ventas Mensuales')          │
│  plt.xlabel('Mes')                      │
│  plt.ylabel('Ventas ($)')               │
│  plt.grid(True, alpha=0.3)              │
│  plt.savefig('ventas.png', dpi=300)     │
│                                         │
│  GENERAMOS:                             │
│  ✅ 8 gráficos profesionales            │
│  ✅ Resolución 300 DPI                  │
│  ✅ Formato PNG portable                │
│                                         │
│  CONCEPTO TEÓRICO:                      │
│  Comunicación de insights (Prog I)      │
└─────────────────────────────────────────┘
```

**Qué decir:**
> "Usamos Matplotlib para generar 8 visualizaciones profesionales. Cada gráfico usa 300 DPI para calidad impresa, grids para legibilidad, y colores consistentes. Los gráficos transforman tablas numéricas en insights visuales: tendencias, patrones, outliers. Este es el último paso del pipeline: comunicar hallazgos."

**MOSTRAR EN PANTALLA:**
- Gráfico de evolución temporal (línea)
- Gráfico de categorías (barras)
- Gráfico de métodos de pago (torta)

**⚠️ ANTICIPAR PREGUNTA:**
- **P: "¿Por qué Matplotlib y no Seaborn o Plotly?"**
- **R:** "Matplotlib es la base de visualización en Python, ofrece control granular. Seaborn es más alto nivel pero menos flexible. Plotly genera gráficos interactivos, pero el TP requería imágenes estáticas. Matplotlib es la herramienta correcta para nuestro caso."

---

#### **SLIDE 12: HALLAZGOS CLAVE (1.5 min)**
```
┌─────────────────────────────────────────┐
│  🎯 HALLAZGOS ESTRATÉGICOS              │
│                                         │
│  1. SEGMENTO FEMENINO DOMINANTE         │
│     59.8% de transacciones              │
│     → Ampliar secciones Clothing        │
│                                         │
│  2. EFECTIVO SIGUE SIENDO REY           │
│     44.7% usan cash                     │
│     → Mantener cajeros ATM              │
│                                         │
│  3. CLOTHING = CATEGORÍA ESTRELLA       │
│     24,685 unidades vendidas            │
│     → Expandir marcas internacionales   │
│                                         │
│  4. TECNOLOGÍA: ALTO VALOR, BAJA VOL.   │
│     Precio promedio: $850               │
│     → Financiación 0% interés           │
│                                         │
│  5. MILLENNIALS = 28% DEL MERCADO       │
│     Edad 25-35: mayor spending          │
│     → Programas de fidelización         │
└─────────────────────────────────────────┘
```

**Qué decir:**
> "Del análisis de 99,459 transacciones, extraemos 5 insights estratégicos. Primero: el segmento femenino genera 59.8% de las transacciones, indica dónde invertir en expansión. Segundo: el efectivo sigue siendo el método preferido, eliminar ATMs sería un error. Tercero: Clothing es la categoría líder con 24,685 unidades. Cuarto: Technology tiene alto ticket promedio pero bajo volumen, oportunidad para financiación. Quinto: millennials 25-35 años son el 28% y tienen alto spending power."

**MOSTRAR EN PANTALLA:**
- Gráfico de distribución por género
- Gráfico de métodos de pago
- Tabla de Top 5 categorías

**⚠️ ANTICIPAR PREGUNTA:**
- **P: "¿Cómo calcularon estos porcentajes?"**
- **R:** (Mostrar código)
```python
# Distribución por género
df.groupby('gender').size() / len(df) * 100

# Resultado:
# Female: 59.8%
# Male:   40.2%
```

---

#### **SLIDE 13: DECISIONES TÉCNICAS CLAVE (1 min)**
```
┌─────────────────────────────────────────┐
│  ⚙️ DECISIONES DIFERENCIADORAS          │
│                                         │
│  1. FECHAS ISO 8601                     │
│     → SQL compatibility + ordenamiento  │
│                                         │
│  2. TABLA DESNORMALIZADA                │
│     → Velocidad de consulta (OLAP)      │
│                                         │
│  3. COLUMNAS CALCULADAS PERSISTIDAS     │
│     → Performance (calcular 1 vez)      │
│                                         │
│  4. CONFIGURACIÓN COLAB AUTOMÁTICA      │
│     → Reproducibilidad garantizada      │
│                                         │
│  5. MANEJO SELECTIVO DE NULOS           │
│     → Transparencia + calidad           │
│                                         │
│  CONCEPTO TEÓRICO:                      │
│  Trade-offs conscientes (Ingeniería)    │
└─────────────────────────────────────────┘
```

**Qué decir:**
> "Nuestro proyecto se diferencia por cinco decisiones técnicas conscientes. Uno: conversión a ISO 8601 para compatibilidad SQL. Dos: tabla desnormalizada priorizando OLAP sobre OLTP. Tres: persistir columnas calculadas para performance. Cuatro: auto-configuración de Colab garantizando reproducibilidad. Cinco: manejo selectivo de nulos con logging transparente. Cada decisión tiene trade-offs que documentamos y justificamos."

**⚠️ ANTICIPAR PREGUNTA:**
- **P: "¿No es mejor normalizar la base de datos?"**
- **R:** "Depende del caso de uso. Para sistemas transaccionales (OLTP) con inserts/updates frecuentes, sí normalizamos. Pero para Data Warehouses analíticos (OLAP) con queries de lectura intensiva, la desnormalización controlada es estándar. Priorizamos velocidad de lectura sobre redundancia."

---

#### **SLIDE 14: CIERRE + CONCEPTOS TEÓRICOS (1 min)**
```
┌─────────────────────────────────────────┐
│  🎓 MAPEO TEORÍA-PRÁCTICA               │
│                                         │
│  PROGRAMACIÓN I:                        │
│  ✅ Estructuras de datos (DataFrames)   │
│  ✅ Funciones y modularidad              │
│  ✅ Manejo de archivos                   │
│  ✅ Librerías externas (import)          │
│  ✅ Visualización de datos               │
│                                         │
│  BASE DE DATOS II:                      │
│  ✅ Modelo relacional                    │
│  ✅ SQL: SELECT, GROUP BY, JOINS         │
│  ✅ Normalización vs Desnormalización    │
│  ✅ Data Warehousing (OLAP)              │
│  ✅ Integridad y calidad de datos        │
│                                         │
│  RESULTADO:                             │
│  ETL completo, reproducible, escalable   │
│                                         │
│  ¿PREGUNTAS? 🤔                         │
└─────────────────────────────────────────┘
```

**Qué decir:**
> "En conclusión, aplicamos conceptos de ambas materias. De Programación I: estructuras de datos con Pandas, modularidad, manejo de archivos, librerías especializadas. De Base de Datos II: modelo relacional, SQL avanzado, normalización, Data Warehousing, calidad de datos. El resultado es un pipeline ETL completo, reproducible en Colab, y escalable a datasets más grandes. Estamos preparados para responder cualquier consulta técnica."

---

## 🎬 RECOMENDACIONES DE PRESENTACIÓN

### ✅ **ANTES DE PRESENTAR:**

1. **Ensayar con cronómetro:** Cada persona debe cumplir su tiempo (3.5 min)
2. **Tener Colab abierto:** Notebook ya ejecutado con todos los outputs visibles
3. **Preparar transiciones:** "Ahora [Nombre] continuará con Transform..."
4. **Backup de pantalla:** Si falla proyector, tener diapositivas en PDF

### 🎤 **DURANTE LA PRESENTACIÓN:**

1. **Mirar a los profesores:** No leer las diapositivas
2. **Señalar outputs:** "Como ven aquí en pantalla, tenemos 99,338 filas..."
3. **Usar terminología técnica:** DataFrame (no "tabla de Pandas"), persistence (no "guardar")
4. **Anticipar:** "Podríamos preguntarnos por qué no usar MySQL..."

### ⚠️ **PREGUNTAS DIFÍCILES Y RESPUESTAS:**

**P: "¿Qué harían si el dataset fuera de 100 GB?"**
**R:** "Pandas no escala a ese tamaño. Usaríamos Apache Spark con PySpark para procesamiento distribuido, o Dask para paralelización en múltiples cores. Otra alternativa es chunking: procesar el CSV en bloques de 1 GB con `pd.read_csv(chunksize=100000)`."

**P: "¿Cómo garantizan que no hay duplicados?"**
**R:** "Validamos con `df.duplicated().sum()` en Transform. Si hubiera duplicados, usaríamos `df.drop_duplicates(subset=['invoice_no'])`. En SQL, podríamos agregar constraint UNIQUE en invoice_no para prevención a nivel de base de datos."

**P: "¿Por qué no usar ORM como SQLAlchemy?"**
**R:** "Para este proyecto educativo, SQLite con conexión directa es suficiente. SQLAlchemy agrega abstracción útil para múltiples motores de DB (Postgres, MySQL, Oracle), pero introduce overhead. Para 99,338 registros en SQLite, la conexión nativa es más simple y directa."

**P: "¿Qué pasa si cambian las columnas del CSV?"**
**R:** "El ETL fallaría en Extract. Para producción, implementaríamos schema validation con Pandera o Great Expectations: definir schema esperado (tipos, rangos, constraints) y validar antes de procesar. Si falla, alertar y detener el pipeline."

**P: "¿Pueden explicar el concepto de idempotencia en ETL?"**
**R:** "Idempotencia significa que ejecutar el ETL N veces produce el mismo resultado. Nuestro `if_exists='replace'` lo garantiza: cada ejecución recrea la tabla completa. En producción con `append`, necesitaríamos deduplicación basada en invoice_no para mantener idempotencia."

**P: "¿Qué métricas usarían para monitorear este ETL en producción?"**
**R:** 
```
1. Row count source vs destination (reconciliación)
2. Null percentage por columna (calidad)
3. Tiempo de ejecución (performance)
4. Failed rows (errores)
5. Freshness (últimos datos cuándo llegaron)
```

---

## 📋 CHECKLIST FINAL

**1 HORA ANTES:**
- [ ] Notebook ejecutado completamente en Colab
- [ ] Todas las visualizaciones generadas
- [ ] Base de datos ventas.db creada (15 MB)
- [ ] Diapositivas cargadas en computadora de presentación
- [ ] Cronómetro configurado
- [ ] Ensayo completo realizado (15 min)

**5 MINUTOS ANTES:**
- [ ] Colab abierto en pestaña del navegador
- [ ] Zoom configurado (si es virtual)
- [ ] Proyector conectado
- [ ] Agua disponible
- [ ] Respirar profundo 😌

---

## 💡 FRASE DE APERTURA POTENTE

> "Implementamos un pipeline ETL completo que procesa 99,459 transacciones en menos de 20 segundos, aplicando principios de Data Engineering: extracción automatizada, transformación con validación de calidad, y carga a base de datos relacional. Generamos insights estratégicos que identifican oportunidades de negocio por $2.5 millones en el segmento femenino. Todo el proceso es reproducible con un clic en Google Colab."

---

## 🎯 FRASE DE CIERRE POTENTE

> "Este proyecto demuestra que dominamos el ciclo completo de datos: desde archivos CSV hasta insights accionables, pasando por transformación, persistencia y visualización. Aplicamos conceptos teóricos de ambas materias en un caso real de Business Intelligence. Estamos preparados para responder cualquier aspecto técnico del pipeline."

---

**¡ÉXITO EN LA PRESENTACIÓN! 🚀**
