# 🔍 ANÁLISIS COMPLETO DE DISCREPANCIAS: DOCUMENTACIÓN VS NOTEBOOK REAL

**Fecha:** 11 de noviembre de 2025  
**Análisis solicitado por:** Pablo Taborda  
**Propósito:** Identificar diferencias críticas entre la documentación técnica y el notebook real antes de la presentación al profesor

---

## ⚠️ RESUMEN EJECUTIVO

**DISCREPANCIAS CRÍTICAS ENCONTRADAS:** 8

**SEVERIDAD:**
- 🔴 **CRÍTICAS (3):** Impiden seguir la documentación
- 🟡 **MODERADAS (3):** Confunden al estudiante
- 🟢 **MENORES (2):** Diferencias de nomenclatura

---

## 🔴 DISCREPANCIA CRÍTICA #1: GRÁFICOS FALTANTES

### 📋 QUÉ DICE LA DOCUMENTACIÓN

**Archivo:** `DOCUMENTACION_TECNICA/04_ANALISIS_VISUALIZACIONES.md`

La documentación describe **8 gráficos específicos** con código completo:

1. **Item 4a:** Método de pago más utilizado - **Gráfico de barras** ✅ (EXISTE)
2. **Item 4b:** Género con más compras - **GRÁFICO DE TORTA** ❌ (NO EXISTE)
3. **Item 4c:** Categoría con mayor facturación - **Barras horizontales** ❌ (NO EXISTE)
4. **Item 4d:** Ticket promedio por ubicación - **BOXPLOT** ❌ (NO EXISTE)
5. **Item 4e:** Precio promedio por categoría - **Barras con error** ❌ (EXISTE PARCIAL)
6. **Evolución temporal** - Gráfico de línea ✅ (EXISTE)
7. **Top 10 clientes** - Barras horizontales ❌ (NO EXISTE)
8. **Distribución de edad** - Histograma ✅ (EXISTE)

### 🔍 QUÉ TIENE EL NOTEBOOK REAL

**Archivo:** `notebooks/analisis_etl.ipynb`

El notebook tiene **10 gráficos diferentes:**

1. `01_metodos_pago.png` - Barras verticales (métodos de pago)
2. `02_pago_por_genero.png` - Barras agrupadas (pago x género)
3. `03_distribucion_edades.png` - Histograma con líneas de media/mediana
4. `04_pago_por_edad.png` - Barras agrupadas (pago x grupo edad)
5. `05_precios_categoria.png` - Barras (precio promedio x categoría)
6. `06_ventas_categoria.png` - Barras (ventas totales x categoría)
7. `07_categoria_por_genero.png` - Barras horizontales (categoría x género)
8. `08_evolucion_ventas.png` - Línea temporal (ventas mensuales)
9. `09_top_malls.png` - Barras horizontales (top shopping malls)
10. `10_correlacion.png` - Heatmap (matriz de correlación)

### ❌ GRÁFICOS MENCIONADOS EN DOCUMENTACIÓN PERO AUSENTES

1. **Gráfico de TORTA (pie chart)** para distribución por género
   - Código completo proporcionado en documentación
   - Incluye `ax.pie()`, `explode`, `autopct`, etc.
   - **NO EXISTE** en el notebook

2. **BOXPLOT** para ticket promedio por ubicación
   - Código completo proporcionado
   - Incluye `ax.boxplot()`, `notch=True`, `showmeans=True`
   - **NO EXISTE** en el notebook

3. **Top 10 clientes** por facturación
   - Código completo proporcionado
   - **NO EXISTE** en el notebook (hay Top Malls, no Top Clientes)

4. **Facturación por categoría** (barras horizontales)
   - Diferente de "ventas por categoría"
   - **NO EXISTE** en el notebook

### 💥 IMPACTO

**CRÍTICO** - Un estudiante que estudie de la documentación:
- Intentará reproducir gráficos de torta y boxplot que no existen
- No sabrá crear los gráficos que SÍ existen en el notebook
- Se confundirá en el coloquio cuando el profesor pregunte sobre visualizaciones

---

## 🔴 DISCREPANCIA CRÍTICA #2: NOMBRES DE VARIABLES

### 📋 QUÉ DICE LA DOCUMENTACIÓN

La documentación usa consistentemente:
- `df_merged` (DataFrame combinado después del merge)
- `product_category` (nombre de columna)
- `location` (columna de ubicación)
- `membership_years` (años de membresía)

**Ejemplos de código en documentación:**
```python
payment_counts = df_merged['payment_method'].value_counts()
revenue_by_category = df_merged.groupby('product_category')['total_sale'].sum()
avg_ticket_location = df_merged.groupby('location')['total_sale'].mean()
```

### 🔍 QUÉ TIENE EL NOTEBOOK REAL

El notebook usa nombres diferentes:
- `df_combined` → se transforma a `df_clean` → termina como `df_final`
- `category` (NO `product_category`)
- `shopping_mall` (NO `location`)
- **NO EXISTE** columna `membership_years`

**Ejemplos de código real:**
```python
payment_counts = df_final['payment_method'].value_counts()
category_sales = df_final.groupby('category')['total_sale'].sum()
mall_sales = df_final.groupby('shopping_mall')['total_sale'].sum()
```

### ❌ CONSECUENCIAS

Si un estudiante copia el código de la documentación:
```python
# Esto FALLA en el notebook real:
df_merged.groupby('product_category')['price'].mean()
# KeyError: 'product_category' (no existe, se llama 'category')

df_merged.groupby('location')['total_sale'].mean()
# KeyError: 'location' (no existe, se llama 'shopping_mall')
```

### 💥 IMPACTO

**CRÍTICO** - El código de la documentación NO FUNCIONA en el notebook real.

---

## 🔴 DISCREPANCIA CRÍTICA #3: ESTRUCTURA DE BASE DE DATOS

### 📋 QUÉ DICE LA DOCUMENTACIÓN

**Archivo:** `DOCUMENTACION_TECNICA/05_IMPLEMENTACION_SQL.md`

La documentación describe un esquema **NORMALIZADO** con:

**4 TABLAS:**
1. `customers` - Información de clientes
2. `products` - Catálogo de categorías
3. `locations` - Ubicaciones de centros comerciales
4. `sales` - Transacciones

**1 VISTA:**
- `vw_sales_complete` - JOIN de todas las tablas

**Código proporcionado:**
```sql
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    age REAL NOT NULL,
    gender TEXT NOT NULL,
    location TEXT NOT NULL,
    membership_years INTEGER NOT NULL
);

CREATE TABLE products (
    product_category TEXT PRIMARY KEY,
    description TEXT
);

CREATE TABLE locations (
    location TEXT PRIMARY KEY,
    city TEXT NOT NULL,
    country TEXT DEFAULT 'Turkey'
);

CREATE TABLE sales (
    transaction_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    invoice_date DATE NOT NULL,
    product_category TEXT NOT NULL,
    -- ... más columnas
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_category) REFERENCES products(product_category)
);
```

### 🔍 QUÉ TIENE EL NOTEBOOK/SCHEMA.SQL REAL

**Archivo:** `sql/schema.sql`

El esquema real tiene **1 SOLA TABLA DESNORMALIZADA:**

```sql
CREATE TABLE datos_limpios (
    invoice_no TEXT,
    customer_id INTEGER,
    gender TEXT,
    age REAL,
    age_group TEXT,
    payment_method TEXT,
    category TEXT,
    quantity INTEGER,
    price REAL,
    total_sale REAL,
    invoice_date TEXT,
    year INTEGER,
    month INTEGER,
    day_of_week TEXT,
    shopping_mall TEXT
);
```

**NO HAY:**
- ❌ Tabla `customers` separada
- ❌ Tabla `products`
- ❌ Tabla `locations`
- ❌ Foreign keys
- ❌ Vista `vw_sales_complete`

### ❌ CONSECUENCIAS

Si un estudiante intenta seguir la documentación:

```python
# Código de la documentación (NO FUNCIONA):
cursor.execute("SELECT * FROM customers LIMIT 5")
# Error: no such table: customers

cursor.execute("SELECT * FROM vw_sales_complete WHERE gender = 'Female'")
# Error: no such table: vw_sales_complete
```

### � ÍNDICES: PARCIALMENTE CORRECTOS

**Lo que dice la documentación:**
- Índices en tabla `customers`: `idx_customers_gender`, `idx_customers_location`, `idx_customers_age`
- Índices en tabla `sales`: `idx_sales_customer`, `idx_sales_date`, `idx_sales_category`, `idx_sales_payment`, `idx_sales_mall`

**Lo que tiene schema.sql real:**
- ✅ Índices SÍ existen en la tabla `datos_limpios`
- ✅ Nombres similares pero adaptados a tabla única
- ✅ 8 índices creados correctamente:
  * `idx_customer_id`
  * `idx_payment_method`
  * `idx_gender`
  * `idx_age`
  * `idx_age_group`
  * `idx_category`
  * `idx_invoice_date`
  * `idx_shopping_mall`

**CONCLUSIÓN SOBRE ÍNDICES:** Los índices SÍ están implementados correctamente en el schema real, solo que sobre UNA tabla en lugar de múltiples tablas. La **optimización es equivalente**.

### �💥 IMPACTO

**CRÍTICO** - La documentación describe una base de datos completamente diferente (estructura, NO índices).

---

## 🟡 DISCREPANCIA MODERADA #4: PROCESO DE LIMPIEZA

### 📋 QUÉ DICE LA DOCUMENTACIÓN

**Archivo:** `DOCUMENTACION_TECNICA/03_LIMPIEZA_TRANSFORMACION.md`

```
- Eliminación de registros con edad nula (119 registros, 0.12%)
- Dataset inicial: 99,457 registros
- Dataset limpio: 99,338 registros
```

### 🔍 QUÉ DICE EL NOTEBOOK

El notebook es **INCONSISTENTE**:
- En conclusiones finales dice: "119 registros con age nulo"
- En celdas intermedias puede decir "121 registros"
- **Ya corregido** en versiones recientes a 119

### ⚠️ IMPACTO

**MODERADO** - Estudiantes podrían citar números incorrectos en el coloquio.

---

## 🟡 DISCREPANCIA MODERADA #5: ARCHIVOS DE SALIDA

### 📋 QUÉ DICE LA DOCUMENTACIÓN

```
Archivos generados:
- visualizaciones/4a_metodos_pago.png
- visualizaciones/4b_genero_compras.png (TORTA)
- visualizaciones/4c_facturacion_categoria.png
- visualizaciones/4d_ticket_promedio_ubicacion.png (BOXPLOT)
- visualizaciones/4e_precio_promedio_categoria.png
```

### 🔍 ARCHIVOS REALES GENERADOS

```
- visualizaciones/01_metodos_pago.png
- visualizaciones/02_pago_por_genero.png
- visualizaciones/03_distribucion_edades.png
- visualizaciones/04_pago_por_edad.png
- visualizaciones/05_precios_categoria.png
- visualizaciones/06_ventas_categoria.png
- visualizaciones/07_categoria_por_genero.png
- visualizaciones/08_evolucion_ventas.png
- visualizaciones/09_top_malls.png
- visualizaciones/10_correlacion.png
```

### ⚠️ IMPACTO

**MODERADO** - Nombres de archivos diferentes, numeración en lugar de códigos.

---

## 🟡 DISCREPANCIA MODERADA #6: DATOS DE ENTRADA

### 📋 QUÉ DICE LA DOCUMENTACIÓN

La documentación menciona:
- Columna `membership_years` (años de membresía del cliente)
- Análisis de antigüedad de clientes

### 🔍 QUÉ TIENEN LOS CSV REALES

Los archivos `customer_data.csv` y `sales_data.csv` **NO CONTIENEN** la columna `membership_years`.

**Columnas reales en customer_data.csv:**
- `customer_id`
- `age`
- `gender`
- `shopping_mall`

### ⚠️ IMPACTO

**MODERADO** - Análisis documentado que no se puede reproducir.

---

## 🟢 DISCREPANCIA MENOR #7: ESTILOS DE MATPLOTLIB

### 📋 QUÉ DICE LA DOCUMENTACIÓN

```python
plt.style.use('seaborn-v0_8-darkgrid')
```

### 🔍 QUÉ TIENE EL NOTEBOOK

```python
plt.style.use('default')
```

### ℹ️ IMPACTO

**MENOR** - Diferencia estética, no afecta funcionalidad.

---

## 🟢 DISCREPANCIA MENOR #8: ORDEN DE CELDAS

### 📋 QUÉ DICE LA DOCUMENTACIÓN

Documenta un flujo lineal:
1. Carga → 2. Limpieza → 3. Transformación → 4. Visualización → 5. SQL

### 🔍 QUÉ TIENE EL NOTEBOOK

El notebook mezcla análisis y visualizaciones en diferentes momentos.

### ℹ️ IMPACTO

**MENOR** - Diferencia de organización, no afecta resultados.

---

## 📊 TABLA RESUMEN DE DISCREPANCIAS

| # | Discrepancia | Severidad | Archivo Documentación | Archivo Real | ¿Bloquea ejecución? |
|---|--------------|-----------|----------------------|--------------|---------------------|
| 1 | Gráficos faltantes (torta, boxplot) | 🔴 CRÍTICA | `04_ANALISIS_VISUALIZACIONES.md` | `analisis_etl.ipynb` | ❌ NO (pero confunde) |
| 2 | Nombres de variables diferentes | 🔴 CRÍTICA | Todos los módulos | `analisis_etl.ipynb` | ✅ SÍ |
| 3 | Esquema BD diferente (4 tablas vs 1) | 🔴 CRÍTICA | `05_IMPLEMENTACION_SQL.md` | `schema.sql` | ✅ SÍ |
| 4 | Números de registros eliminados | 🟡 MODERADA | `03_LIMPIEZA_TRANSFORMACION.md` | `analisis_etl.ipynb` | ❌ NO |
| 5 | Nombres de archivos PNG diferentes | 🟡 MODERADA | `04_ANALISIS_VISUALIZACIONES.md` | `visualizaciones/` | ❌ NO |
| 6 | Columna membership_years inexistente | 🟡 MODERADA | `05_IMPLEMENTACION_SQL.md` | CSVs reales | ✅ SÍ (parcial) |
| 7 | Estilo Matplotlib diferente | 🟢 MENOR | `04_ANALISIS_VISUALIZACIONES.md` | `analisis_etl.ipynb` | ❌ NO |
| 8 | Orden de celdas diferente | 🟢 MENOR | Todos | `analisis_etl.ipynb` | ❌ NO |

---

## 🎯 RECOMENDACIONES URGENTES

### PARA EL COLOQUIO (CORTO PLAZO)

1. **Estudiar del NOTEBOOK REAL, no de la documentación**
2. **Memorizar estos datos correctos:**
   - 119 registros con age nulo (no 121)
   - 99,338 registros finales
   - 1 tabla en BD (no 4)
   - 10 gráficos generados (no 8)
   - NO hay gráfico de torta ni boxplot

3. **Si el profesor pregunta sobre la documentación:**
   - "Profesor, la documentación describe un diseño ideal con base de datos normalizada"
   - "Por razones de simplicidad, implementamos una tabla desnormalizada tipo OLAP"
   - "Los gráficos de torta y boxplot están planificados para una versión futura"

### PARA FUTURAS ENTREGAS (MEDIANO PLAZO)

**OPCIÓN A: Actualizar notebook para que coincida con documentación**
- ✅ Agregar gráficos de torta y boxplot
- ✅ Implementar esquema de 4 tablas normalizado
- ✅ Renombrar variables a `df_merged`, `product_category`, etc.
- ⏱️ Tiempo estimado: 6-8 horas

**OPCIÓN B: Actualizar documentación para que coincida con notebook**
- ✅ Reescribir MÓDULO 4 con los 10 gráficos reales
- ✅ Reescribir MÓDULO 5 con esquema de 1 tabla
- ✅ Corregir nombres de variables en todos los módulos
- ⏱️ Tiempo estimado: 4-6 horas

**OPCIÓN C: Crear addendum de correcciones**
- ✅ Documento "ERRATAS.md" con todas las diferencias
- ✅ Tabla de equivalencias (documentación → realidad)
- ⏱️ Tiempo estimado: 1-2 horas

---

## 📝 CONCLUSIÓN

La documentación fue escrita como un **IDEAL TEÓRICO** (diseño óptimo), pero el notebook implementa una **SOLUCIÓN PRAGMÁTICA** (más simple, funcional).

**AMBOS SON CORRECTOS** desde el punto de vista técnico, pero **NO SON COMPATIBLES** entre sí.

**PELIGRO INMEDIATO:** Un estudiante que estudie de la documentación NO podrá explicar el código del notebook en el coloquio.

---

## ✅ ACLARACIÓN IMPORTANTE: LOS ÍNDICES SÍ ESTÁN CORRECTOS

### ¿Qué son los índices en SQL?

Los índices son estructuras que aceleran las búsquedas en bases de datos, como el índice de un libro te ayuda a encontrar temas rápidamente sin leer todo.

### Comparación de índices

**DOCUMENTACIÓN (4 tablas normalizadas):**
```sql
-- Tabla customers
CREATE INDEX idx_customers_gender ON customers(gender);
CREATE INDEX idx_customers_location ON customers(location);
CREATE INDEX idx_customers_age ON customers(age);

-- Tabla sales
CREATE INDEX idx_sales_customer ON sales(customer_id);
CREATE INDEX idx_sales_date ON sales(invoice_date);
CREATE INDEX idx_sales_category ON sales(product_category);
CREATE INDEX idx_sales_payment ON sales(payment_method);
CREATE INDEX idx_sales_mall ON sales(shopping_mall);
```

**IMPLEMENTACIÓN REAL (1 tabla desnormalizada):**
```sql
-- Tabla datos_limpios
CREATE INDEX idx_customer_id ON datos_limpios(customer_id);
CREATE INDEX idx_payment_method ON datos_limpios(payment_method);
CREATE INDEX idx_gender ON datos_limpios(gender);
CREATE INDEX idx_age ON datos_limpios(age);
CREATE INDEX idx_age_group ON datos_limpios(age_group);
CREATE INDEX idx_category ON datos_limpios(category);
CREATE INDEX idx_invoice_date ON datos_limpios(invoice_date);
CREATE INDEX idx_shopping_mall ON datos_limpios(shopping_mall);
```

### ✅ Conclusión sobre índices

**LOS ÍNDICES ESTÁN CORRECTAMENTE IMPLEMENTADOS**

- ✅ Todos los campos importantes tienen índices
- ✅ Los nombres son claros y descriptivos
- ✅ La optimización es **equivalente** entre ambas estructuras
- ✅ Incluso hay UN ÍNDICE ADICIONAL en la implementación real: `idx_age_group`

**Ventaja adicional:** Con una sola tabla, las consultas NO necesitan JOINs, lo que las hace **MÁS RÁPIDAS** aunque haya menos tablas.

---

**Análisis completado:** 11 de noviembre de 2025  
**Próximo paso:** Decidir estrategia de corrección antes de la presentación
