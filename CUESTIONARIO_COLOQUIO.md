# 📝 CUESTIONARIO DE COLOQUIO - PROYECTO ETL (20 PREGUNTAS ESENCIALES)

**Asignatura:** Innovación de Datos (Programación I + Base de Datos II)  
**Modalidad:** Coloquio oral individual  
**Objetivo:** Validar conocimientos técnicos del trabajo práctico entregado

**📌 Versión optimizada:** 20 preguntas estratégicas que cubren todos los temas fundamentales

---

## 👨‍🏫 PROFESOR ALEJANDRO MAINERO (PROGRAMACIÓN I)

### 🎯 **PREGUNTAS 1-8: Fundamentos de Python, Pandas y Análisis**

---

**1. ¿Por qué eligieron usar Pandas en lugar de leer los CSV con Python puro?**

**RESPUESTA:**

Elegimos Pandas por 4 razones técnicas fundamentales:

1. **Rendimiento:** `pd.read_csv()` está implementado en C, entre 10-100x más rápido que Python puro con `open()` y `readlines()`

2. **Inferencia automática de tipos:** Pandas detecta automáticamente si una columna es int, float, string o datetime. Con Python puro todo se lee como string.

3. **Operaciones vectoriales:** Permite hacer `df['total'] = df['quantity'] * df['price']` en una sola línea para 99,459 registros. Con Python puro necesitaríamos un bucle for que sería mucho más lento.

4. **Integración con ecosistema:** Se conecta nativamente con NumPy para cálculos, Matplotlib para gráficos, y SQLite con `.to_sql()`.

**Ejemplo comparativo:**
```python
# Python puro (complejo y lento)
with open('sales_data.csv', 'r') as f:
    lines = f.readlines()
    for line in lines[1:]:
        fields = line.strip().split(',')
        # Convertir tipos manualmente...

# Pandas (simple y rápido)
df = pd.read_csv('sales_data.csv')
```

---

**2. Explícame la diferencia entre `pd.merge()` y `pd.concat()`. ¿Por qué usaron merge en el Item 3?**

**RESPUESTA:**

**`pd.merge()`** - Operación tipo JOIN de SQL:
- Combina DataFrames **basándose en una columna común** (clave)
- Busca coincidencias entre las claves y combina las filas que coinciden
- Puede hacer INNER JOIN, LEFT JOIN, RIGHT JOIN, OUTER JOIN

**`pd.concat()`** - Concatenación simple:
- **Apila** DataFrames uno después del otro (vertical u horizontal)
- NO busca relaciones entre datos
- No requiere columnas comunes

**¿Por qué usamos merge?**

Teníamos dos datasets relacionados por `customer_id`:
- `df_sales`: transacciones (invoice_no, quantity, price, customer_id)
- `df_customers`: datos demográficos (customer_id, age, gender)

Necesitábamos combinar información de ambas tablas para cada cliente:

```python
# Correcto - merge (lo que hicimos)
df_combined = pd.merge(df_sales, df_customers, on='customer_id', how='left')
# Resultado: cada venta tiene edad y género del cliente

# Incorrecto - concat
df_wrong = pd.concat([df_sales, df_customers])
# ¡Apila filas sin relacionarlas!
```

---

**3. Veo que usan `.copy()` para crear df_clean. ¿Qué pasaría si no usaran .copy()?**

**RESPUESTA:**

Sin `.copy()`, estaríamos creando una **vista (view)** en lugar de una **copia independiente**. Problemas:

1. **SettingWithCopyWarning:**
```python
df_clean = df_combined  # ¡Solo una referencia!
df_clean['total_sale'] = df_clean['quantity'] * df_clean['price']
# ⚠️ WARNING: A value is trying to be set on a copy...
```

2. **Modificaciones afectan el original:**
```python
df_clean = df_combined  # referencia
df_clean.dropna(inplace=True)  # ¡También borra en df_combined!
```

**Con `.copy()` (correcto):**
```python
df_clean = df_combined.copy()  # Copia independiente
df_clean.drop(columns=['age'])  # df_combined intacto
```

**Importancia en nuestro proyecto:** La consigna del Item 3 dice *"Se mantienen los DataFrames originales sin modificar"*. Sin `.copy()`, al transformar `df_clean` alteraríamos `df_combined`, violando este requisito.

---

**4. En la conversión de fechas, ¿por qué especifican `format='%d-%m-%Y'`?**

**RESPUESTA:**

Especificar el formato tiene 3 ventajas críticas:

**1. RENDIMIENTO (10-20x más rápido)**
```python
# Con formato explícito
pd.to_datetime(df['date'], format='%d-%m-%Y')  # Pandas sabe cómo parsear

# Sin formato
pd.to_datetime(df['date'])  # Debe "adivinar" probando múltiples patrones
```

**2. EVITA AMBIGÜEDAD (dd/mm vs mm/dd)**
```
Fecha: "01-02-2023"

Sin format: ¿Es 1 de febrero o 2 de enero? 
           Depende de la configuración del sistema

Con format='%d-%m-%Y': Siempre 1 de febrero de 2023
```

**3. CONTROL Y VALIDACIÓN**
- Si el CSV tiene formato inconsistente, Pandas lanza error inmediatamente
- Sin format, podría convertir mal sin avisar

**En nuestro proyecto:** Los CSV tienen formato `15-03-2023` (dd-mm-yyyy turco). Especificar `format='%d-%m-%Y'` garantiza interpretación correcta en Colab (servidor USA) y laptops locales (Argentina).

---

**5. ¿Qué diferencia hay entre `mean()`, `median()` y `mode()`? ¿Cuándo usarías cada una?**

**RESPUESTA:**

**MEAN (Media) - `.mean()`**
- Suma de valores / cantidad
- **MUY sensible a outliers**
```python
precios = [10, 15, 20, 25, 1000]  # ← outlier
media = 214  # ¡Engañosa!
```
**Cuándo:** Datos sin outliers, distribución simétrica

**MEDIAN (Mediana) - `.median()`**
- Valor central al ordenar datos
- **ROBUSTA contra outliers**
```python
precios = [10, 15, 20, 25, 1000]
mediana = 20  # ¡Representativa!
```
**Cuándo:** Datos con outliers, salarios, precios de vivienda

**MODE (Moda) - `.mode()`**
- Valor MÁS FRECUENTE
- **ÚNICA medida para datos categóricos**
```python
payment_methods = ['Cash', 'Cash', 'Credit', 'Cash']
moda = 'Cash'
```
**Cuándo:** Datos categóricos (género, método de pago)

**Ejemplo con salarios:**
```
[30k, 32k, 35k, 38k, 40k, 500k]  ← CEO

Media:    106k  ❌ Engañosa
Mediana:  36.5k ✅ Representativa
```

**En nuestro proyecto:**
```python
# Item 4: Análisis de precios
df.groupby('category')['price'].agg(['mean', 'median'])  # Ambas

# Item 4a: Método más frecuente
df['payment_method'].mode()[0]  # Moda (no tiene sentido media de texto)
```

---

**6. ¿Qué biblioteca usaron para generar los gráficos y por qué?**

**RESPUESTA:**

Usamos **Matplotlib** (módulo `pyplot`), la biblioteca estándar de visualización en Python.

**¿Por qué Matplotlib?**

1. **Estándar de la industria:** Más madura (desde 2003), ampliamente documentada

2. **Integración con Pandas:**
```python
df.plot()  # Usa Matplotlib internamente
df['price'].hist()  # Matplotlib
```

3. **Control granular:** Personalización extrema de cada elemento

4. **Múltiples backends:** Funciona en Jupyter, Colab, scripts, guarda PNG/PDF/SVG

**Alternativas consideradas:**

| Biblioteca | Ventaja | Por qué NO la usamos |
|------------|---------|---------------------|
| Seaborn | Gráficos estadísticos bellos | Más configuración inicial |
| Plotly | Interactivos (zoom, hover) | Interactividad no necesaria para PDF |
| Bokeh | Escalable a millones de puntos | Complejidad innecesaria |

**En el proyecto:**
```python
# Configuración global
import matplotlib.pyplot as plt
plt.style.use('default')
plt.rcParams['figure.figsize'] = (12, 6)

# Gráfico de líneas (tendencias)
ventas_mensuales.plot(kind='line', marker='o')
plt.title('Evolución de Ventas')
plt.grid(True, alpha=0.3)
plt.savefig('visualizaciones/ventas.png', dpi=300)
```

**Conclusión:** Matplotlib es ideal para nuestro caso: gráficos estáticos de alta calidad para reportes PDF/presentaciones, integración perfecta con Pandas.

---

**7. En el código, ¿identificás algún uso de POO (Programación Orientada a Objetos)?**

**RESPUESTA:**

Sí, usamos POO **intensivamente a través de Pandas**. Los DataFrames SON objetos con:

**ATRIBUTOS (propiedades):**
```python
print(df.shape)      # (99459, 11) - atributo
print(df.columns)    # Index(['invoice_no', ...]) - atributo
print(df.dtypes)     # Series con tipos - atributo
```

**MÉTODOS (funciones del objeto):**
```python
df.head()            # Devuelve primeras 5 filas
df.describe()        # Estadísticas descriptivas
df.dropna()          # Retorna nuevo DataFrame sin nulos
df.groupby('gender') # Retorna GroupBy object
```

**ENCAPSULAMIENTO:**
Los datos internos están protegidos, accedemos via métodos:
```python
df['age']  # Usa __getitem__ internamente
```

**Ejemplo explícito (si tuviéramos que crear una clase):**
```python
class AnalizadorVentas:
    def __init__(self, dataframe):
        self.df = dataframe  # Atributo
        self.total_registros = len(dataframe)
    
    def calcular_ingresos_totales(self):  # Método
        return self.df['total_sale'].sum()
    
    def top_categorias(self, n=5):  # Método
        return self.df.groupby('category')['total_sale'].sum().nlargest(n)

# Uso
analizador = AnalizadorVentas(df_clean)  # Instanciar objeto
print(analizador.calcular_ingresos_totales())  # Llamar método
```

**Conexión con teoría:**
- DataFrame hereda de NDFrame
- Series hereda de NDFrame
- Métodos encadenados: `df.dropna().groupby('x').sum()`
- Todo el proyecto usa objetos de librerías (Pandas, Matplotlib)

---

**8. ¿Cómo se relaciona su trabajo con el temario de Programación I?**

**RESPUESTA EJECUTIVA:**

Nuestro proyecto aplica **8 temas del programa**:

| Tema | Aplicación en el proyecto |
|------|--------------------------|
| **1. Tipos de datos** | Conversión int/float/datetime: `df['customer_id'].astype(int)` |
| **2. Operadores** | Filtrado: `df[(df['age'] >= 25) & (df['age'] <= 35)]`, cálculos: `quantity * price` |
| **3. If/else** | Detección Colab: `if 'google.colab' in sys.modules:`, validaciones de nulos |
| **4. Ciclos for** | Iteración sobre grupos: `for gender in df['gender'].unique():` |
| **5. Funciones** | Categorización: `def categorize_age(age): if age < 25: return 'Joven'...` |
| **6. POO** | DataFrames como objetos con atributos (`.shape`) y métodos (`.dropna()`) |
| **7. Análisis exploratorio** | `.describe()`, `.mean()`, `.median()`, `.value_counts()` |
| **8. Visualización** | Matplotlib: histogramas, barras, líneas, boxplots |

**Ejemplo integrador:**
```python
# Combina 5 conceptos de Programación I
def analizar_ventas_por_edad(df):  # ← Función
    """Calcula estadísticas por grupo etario"""  # ← Docstring
    
    # Operadores de comparación + if/else
    if df['age'].isnull().sum() > 0:
        df = df.dropna(subset=['age'])  # POO: método
    
    # Ciclo for + estructuras de control
    for edad_min, edad_max in [(18,25), (26,35), (36,50)]:
        grupo = df[(df['age'] >= edad_min) & (df['age'] <= edad_max)]
        
        # Análisis estadístico
        promedio = grupo['total_sale'].mean()
        
        # Visualización
        grupo['total_sale'].hist(bins=20)
        plt.title(f'Ventas grupo {edad_min}-{edad_max}')
        plt.show()
```

Este código usa: funciones, docstrings, if/else, ciclos, operadores, POO (DataFrame), análisis estadístico y visualización. **Es una aplicación práctica directa del programa de Programación I.**

---

1. **¿Por qué eligieron usar Pandas en lugar de leer los CSV con Python puro (open/readlines)?**
   
   **RESPUESTA COMPLETA:**
   
   Elegimos Pandas por varias razones técnicas fundamentales:
   
   - **Optimización de lectura:** `pd.read_csv()` está implementado en C (bajo nivel), lo que hace la lectura entre 10-100x más rápida que Python puro con `open()` y `readlines()`.
   
   - **Inferencia automática de tipos:** Pandas detecta automáticamente si una columna es int, float, string o datetime, mientras que con Python puro todo se lee como string y habría que convertir manualmente cada campo.
   
   - **Operaciones vectoriales:** Pandas permite hacer `df['total'] = df['quantity'] * df['price']` en una sola línea para 99,459 registros. Con Python puro necesitaríamos un bucle for que sería mucho más lento.
   
   - **Estructura de datos potente:** El DataFrame es bidimensional con etiquetas de columnas, índices, y métodos como `.groupby()`, `.merge()`, `.pivot_table()` que no existen en listas de Python.
   
   - **Integración con ecosistema:** Se conecta nativamente con NumPy para cálculos numéricos, Matplotlib para gráficos, y SQLite con `.to_sql()`.
   
   - **Manejo robusto de datos faltantes:** Pandas maneja `NaN` de forma inteligente, mientras que con listas necesitaríamos lógica manual para cada caso.
   
   **Ejemplo comparativo:**
   ```python
   # Python puro (complejo y lento)
   with open('sales_data.csv', 'r') as f:
       lines = f.readlines()
       for line in lines[1:]:  # saltar header
           fields = line.strip().split(',')
           # Convertir tipos manualmente...
   
   # Pandas (simple y rápido)
   df = pd.read_csv('sales_data.csv')
   ```

---

2. **Explícame la diferencia entre `pd.merge()` y `pd.concat()`. ¿Por qué usaron merge en el Item 3?**
   
   **RESPUESTA COMPLETA:**
   
   Son funciones con propósitos completamente diferentes:
   
   **`pd.merge()`** - Operación tipo JOIN de SQL:
   - Combina DataFrames **basándose en una columna común** (clave)
   - Similar a hacer un `JOIN` en SQL
   - Busca coincidencias entre las claves y combina las filas que coinciden
   - Puede hacer INNER JOIN, LEFT JOIN, RIGHT JOIN, OUTER JOIN
   
   **`pd.concat()`** - Concatenación simple:
   - **Apila** DataFrames uno después del otro (vertical u horizontal)
   - NO busca relaciones entre datos
   - Es como "pegar" tablas una debajo de otra o al lado
   - No requiere columnas comunes
   
   **¿Por qué usamos merge en Item 3?**
   
   Porque teníamos dos datasets relacionados por `customer_id`:
   - `df_sales`: transacciones de ventas (invoice_no, quantity, price, customer_id)
   - `df_customers`: información demográfica (customer_id, age, gender)
   
   Necesitábamos **combinar la información de ambas tablas** para cada cliente. Ejemplo:
   
   ```python
   # Correcto - merge (lo que hicimos)
   df_combined = pd.merge(df_sales, df_customers, on='customer_id', how='left')
   # Resultado: cada venta tiene edad y género del cliente
   
   # Incorrecto - concat
   df_wrong = pd.concat([df_sales, df_customers])
   # Resultado: ¡apila filas sin relacionarlas! DataFrames incompatibles
   ```
   
   **Analogía:** Merge es como buscar en la guía telefónica (clave: nombre), concat es como apilar dos directorios completos uno después del otro sin orden.

---

3. **¿Qué significa el parámetro `how='left'` en el merge? ¿Qué otros valores puede tomar?**
   
   **RESPUESTA COMPLETA:**
   
   El parámetro `how` define **qué registros se mantienen** cuando las claves no coinciden en ambos DataFrames.
   
   **Valores posibles:**
   
   **a) `how='left'` (LEFT JOIN)** - Lo que usamos:
   - Mantiene **TODAS las filas del DataFrame izquierdo** (df_sales)
   - Agrega datos del derecho (df_customers) donde hay coincidencia
   - Si un customer_id de ventas NO existe en clientes → columnas de clientes quedan `NaN`
   - **Usamos esto porque:** No queremos perder transacciones, incluso si falta info del cliente
   
   **b) `how='right'` (RIGHT JOIN)**:
   - Mantiene **TODAS las filas del DataFrame derecho** (df_customers)
   - Agrega datos del izquierdo donde coincide
   - Útil si priorizamos tener todos los clientes, aunque no hayan comprado
   
   **c) `how='inner'` (INNER JOIN)**:
   - Mantiene **SOLO las filas que coinciden en AMBOS** DataFrames
   - Descarta transacciones sin cliente Y clientes sin transacciones
   - Más restrictivo, dataset resultante más pequeño
   
   **d) `how='outer'` (FULL OUTER JOIN)**:
   - Mantiene **TODAS las filas de AMBOS** DataFrames
   - Rellena con `NaN` donde no hay coincidencia
   - Dataset resultante más grande
   
   **Ejemplo visual con datos ficticios:**
   ```
   df_sales:              df_customers:
   customer_id | amount   customer_id | age
   ------------|------    ------------|----
   1           | 100      1           | 25
   2           | 200      3           | 30
   4           | 150
   
   LEFT:   3 filas (IDs: 1,2,4) → cliente 4 tendrá age=NaN
   RIGHT:  2 filas (IDs: 1,3) → pierde venta del cliente 2 y 4
   INNER:  1 fila  (ID: 1) → solo donde coincide
   OUTER:  4 filas (IDs: 1,2,3,4) → todos con NaN donde faltan
   ```

---

4. **Veo que usan `.copy()` para crear df_clean. ¿Qué pasaría si no usaran .copy()?**
   
   **RESPUESTA COMPLETA:**
   
   Sin `.copy()`, estaríamos creando una **vista (view)** del DataFrame original en lugar de una **copia independiente**. Esto causa problemas graves:
   
   **Problema 1: SettingWithCopyWarning**
   ```python
   # Sin copy
   df_clean = df_combined  # ¡Solo una referencia!
   df_clean['total_sale'] = df_clean['quantity'] * df_clean['price']
   # ⚠️ WARNING: A value is trying to be set on a copy of a slice...
   ```
   
   **Problema 2: Modificaciones afectan el original**
   ```python
   df_clean = df_combined  # referencia
   df_clean.dropna(inplace=True)  # ¡También borra en df_combined!
   
   print(len(df_combined))  # ¡Cambió! No esperábamos esto
   ```
   
   **Problema 3: Comportamiento impredecible**
   - A veces Pandas hace copia implícita, a veces no
   - Depende de la operación específica
   - Código se vuelve frágil y difícil de debuggear
   
   **Con `.copy()` (correcto):**
   ```python
   df_clean = df_combined.copy()  # Copia profunda independiente
   df_clean['nueva_col'] = 0       # Solo afecta df_clean
   df_clean.drop(columns=['age'])  # df_combined intacto
   ```
   
   **¿Por qué es importante en nuestro proyecto?**
   
   La consigna del Item 3 dice explícitamente: *"Se mantienen los DataFrames originales df_customers y df_sales sin modificar"*. Si no usáramos `.copy()`, al hacer transformaciones en `df_clean` podríamos alterar `df_combined`, violando este requisito.
   
   **Regla práctica:** Siempre usar `.copy()` cuando vas a modificar un DataFrame derivado y necesitas preservar el original.

---

## 👨‍🏫 PROFESOR CARLOS CHARLETTI (BASE DE DATOS II)

### 🎯 **PREGUNTAS 9-14: SQL, Bases de Datos y ETL**

---

**9. ¿Por qué eligieron SQLite en lugar de MySQL o PostgreSQL?**

**RESPUESTA:**

Elegimos SQLite por 5 razones técnicas específicas para este proyecto:

**1. ARQUITECTURA SERVERLESS**
```
SQLite: Python → archivo .db ¡Listo!

MySQL: Python → servidor corriendo → base de datos
        ↑ Requiere instalación, puerto 3306, usuario, contraseña
```

**2. ARCHIVO ÚNICO PORTÁTIL**
```python
ventas.db  # 15 MB, contiene las 99,459 transacciones
# Ventajas:
# - Fácil compartir (GitHub)
# - Backup = copiar archivo
# - Profesor puede abrir sin configurar nada
```

**3. CERO CONFIGURACIÓN**
```python
# SQLite (2 líneas)
import sqlite3
conn = sqlite3.connect('ventas.db')  # ¡Listo!

# MySQL (complejo)
import mysql.connector
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='tu_password',
    database='ventas'
)
# + Instalar MySQL Server (500MB+)
# + Configurar seguridad, puerto, usuario
```

**4. INTEGRACIÓN NATIVA CON PYTHON**
```python
import sqlite3  # Incluido en Python estándar
df.to_sql('datos', conn, if_exists='replace')  # ¡Una línea!
```

**5. RENDIMIENTO SUFICIENTE**
```
Nuestro dataset: 99,459 registros, ~15 MB
Capacidad SQLite: Hasta 281 TB teóricos
Consultas del proyecto: < 100ms todas
```

**CUÁNDO SÍ USAR MySQL/PostgreSQL:**

| Situación | Requiere MySQL/PostgreSQL |
|-----------|-------------------------|
| Múltiples usuarios concurrentes (>100) | ✅ Sí |
| Aplicación web en producción | ✅ Sí |
| Datos > 100 GB | ✅ Sí |
| Proyecto educativo individual | ❌ No (SQLite suficiente) |
| Análisis de datos local | ❌ No (SQLite suficiente) |

**Conclusión:** SQLite es ideal para proyectos educativos donde no necesitamos usuarios concurrentes. Para aplicación web en producción con cientos de usuarios simultáneos, sí migraríamos a PostgreSQL.

---

**10. ¿Qué es normalización? ¿Sus datos están normalizados?**

**RESPUESTA:**

**Normalización:** Organizar datos en múltiples tablas relacionadas para eliminar redundancia y mejorar integridad.

**¿NUESTROS DATOS ESTÁN NORMALIZADOS? NO - Intencionalmente**

**Estructura actual (tabla única desnormalizada):**
```sql
CREATE TABLE datos_limpios (
    invoice_no TEXT,
    customer_id INTEGER,
    gender TEXT,        -- ← Redundancia
    age INTEGER,        -- ← Redundancia
    category TEXT,
    quantity INTEGER,
    price REAL,
    payment_method TEXT -- ← Redundancia
);
```

**Problema de desnormalización:**
```
invoice | customer_id | gender | age | payment_method
I001    | 1001        | Female | 25  | Cash
I002    | 1001        | Female | 25  | Cash  ← Repite gender, age
I003    | 1001        | Female | 25  | Credit ← Repite gender, age

¡Gender y age del cliente 1001 replicados en cada compra!
```

**DISEÑO NORMALIZADO (3FN) - Cómo DEBERÍA ser en producción:**
```sql
-- Tabla 1: Clientes (sin redundancia)
CREATE TABLE clientes (
    customer_id INTEGER PRIMARY KEY,
    gender TEXT,
    age INTEGER,
    payment_method TEXT
);  -- Solo 1,000 filas únicas

-- Tabla 2: Ventas
CREATE TABLE ventas (
    invoice_no TEXT PRIMARY KEY,
    customer_id INTEGER,  -- ← Foreign Key
    category TEXT,
    quantity INTEGER,
    price REAL,
    total_sale REAL,
    FOREIGN KEY (customer_id) REFERENCES clientes(customer_id)
);  -- 99,459 filas

-- Para consultar: JOIN
SELECT v.invoice_no, v.total_sale, c.gender, c.age
FROM ventas v
JOIN clientes c ON v.customer_id = c.customer_id;
```

**¿POR QUÉ ELEGIMOS DESNORMALIZACIÓN?**

**Razones válidas:**

1. **Optimización para análisis (Data Warehouse pattern)**
```
Normalizado:  SELECT requiere JOIN constante → Más lento
Desnormalizado: SELECT * FROM datos_limpios → Más rápido
```

2. **Dataset estático:** No hay inserciones/actualizaciones frecuentes

3. **Estándar en analítica:** Data Warehouses usan Star Schema (parcialmente desnormalizado)

**TRADE-OFFS:**

| Aspecto | Normalizado 3FN | Desnormalizado (nuestro) |
|---------|-----------------|-------------------------|
| Redundancia | ✅ Mínima | ❌ Alta |
| Velocidad lectura | ❌ Requiere JOINs | ✅ Directa |
| Integridad | ✅ Alta | ❌ Dependiente de ETL |
| Ideal para | OLTP (transaccional) | OLAP (analítica) |

**Conclusión:** Desnormalizamos porque priorizamos velocidad de consulta para análisis. Para sistema transaccional (e-commerce en tiempo real), SÍ normalizaríamos con FK y constraints.

---

**11. Explícame qué hace `df.to_sql()` y qué parámetros clave acepta.**

**RESPUESTA:**

`df.to_sql()` **escribe un DataFrame completo a una tabla SQL**.

**Funcionamiento interno:**
1. Crea tabla si no existe (CREATE TABLE)
2. Infiere tipos SQL desde tipos Pandas
3. Genera statements INSERT por batch (1000 filas por defecto)
4. Ejecuta y hace commit

**PARÁMETROS CLAVE:**

**1. `if_exists` (CRÍTICO):**
```python
# 'fail' (default): Error si tabla existe ← Seguro
df.to_sql('datos', conn, if_exists='fail')

# 'replace': BORRA tabla y crea nueva ← PELIGROSO
df.to_sql('datos', conn, if_exists='replace')
# DROP TABLE datos; CREATE TABLE datos...

# 'append': AGREGA filas a tabla existente ← Updates incrementales
df.to_sql('datos', conn, if_exists='append')
```

**En nuestro proyecto:**
```python
df.to_sql(
    'datos_limpios',
    conn,
    if_exists='replace',  # ← Borra y recrea (desarrollo)
    index=False           # ← No guardar índice Pandas
)
```

**¿Por qué `if_exists='replace'`?**
- Script ETL se ejecuta múltiples veces en desarrollo
- Queremos versión más reciente siempre
- No es producción, no hay riesgo de perder datos críticos

**⚠️ CUIDADO EN PRODUCCIÓN:**
```python
# ❌ PELIGROSO
df.to_sql('usuarios', conn, if_exists='replace')
# ¡Borra TODOS los usuarios!

# ✅ SEGURO
df.to_sql('usuarios', conn, if_exists='append')
# Solo agrega nuevos registros
```

**2. `index=False` (importante):**
```python
# Con index=True (default)
df.to_sql('datos', conn)
# Resultado: index | invoice_no | price
#              0   | I001       | 25
# ← Columna "index" innecesaria

# Con index=False (lo que usamos)
df.to_sql('datos', conn, index=False)
# Resultado: invoice_no | price
#            I001       | 25
# ← Limpio
```

**MAPEO TIPOS Pandas → SQL:**

| Pandas | SQLite |
|--------|--------|
| int64 | INTEGER |
| float64 | REAL |
| object (string) | TEXT |
| datetime64 | TEXT (ISO8601) |

**VERIFICACIÓN POST-CARGA:**
```python
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM datos_limpios')
count = cursor.fetchone()[0]
print(f'✅ {count} registros cargados')
```

---

**12. En el Item 5, ¿cómo harías el total de ventas por mes? Explica la consulta SQL.**

**RESPUESTA:**

**Consulta SQL del proyecto:**
```sql
SELECT 
    STRFTIME('%Y-%m', invoice_date) AS mes,
    SUM(total_sale) AS ventas_totales,
    COUNT(*) AS num_transacciones,
    AVG(total_sale) AS ticket_promedio
FROM datos_limpios
GROUP BY mes
ORDER BY mes;
```

**EXPLICACIÓN PASO A PASO:**

**1. `STRFTIME('%Y-%m', invoice_date)`**
- Función de fecha en SQLite
- Extrae año-mes de la fecha: `2023-03-15` → `2023-03`
- `%Y` = año 4 dígitos, `%m` = mes 2 dígitos

**2. `SUM(total_sale)`**
- Función de agregación
- Suma todos los `total_sale` de cada mes
- Resultado: ingresos totales mensuales

**3. `COUNT(*)`**
- Cuenta número de transacciones por mes
- Útil para identificar meses con más actividad

**4. `AVG(total_sale)`**
- Promedio del monto por transacción
- Identifica ticket promedio por mes

**5. `GROUP BY mes`**
- Agrupa resultados por el alias `mes` (año-mes)
- Todas las funciones agregadas (SUM, COUNT, AVG) operan dentro de cada grupo

**6. `ORDER BY mes`**
- Ordena cronológicamente (2023-01, 2023-02, 2023-03...)

**RESULTADO EJEMPLO:**
```
mes     | ventas_totales | num_transacciones | ticket_promedio
2021-01 | 1,250,430.50  | 8,234             | 151.89
2021-02 | 1,180,290.25  | 7,891             | 149.55
2021-03 | 1,420,850.75  | 9,456             | 150.25
...
```

**ALTERNATIVAS EN OTROS MOTORES:**

```sql
-- PostgreSQL
SELECT DATE_TRUNC('month', invoice_date) AS mes, SUM(total_sale)
FROM datos_limpios
GROUP BY DATE_TRUNC('month', invoice_date);

-- MySQL
SELECT DATE_FORMAT(invoice_date, '%Y-%m') AS mes, SUM(total_sale)
FROM datos_limpios
GROUP BY DATE_FORMAT(invoice_date, '%Y-%m');
```

**¿Por qué funciona sin JOIN?**
Porque desnormalizamos: `total_sale` ya está en la tabla. En modelo normalizado necesitaríamos:
```sql
SELECT STRFTIME('%Y-%m', v.invoice_date), SUM(v.quantity * p.price)
FROM ventas v
JOIN productos p ON v.product_id = p.id
GROUP BY ...
```

---

**13. ¿Qué diferencia hay entre WHERE y HAVING en SQL?**

**RESPUESTA:**

**WHERE:** Filtra **filas ANTES** de agrupar  
**HAVING:** Filtra **grupos DESPUÉS** de agrupar

**REGLA CLAVE:** WHERE no puede usar funciones agregadas, HAVING sí.

**EJEMPLO PRÁCTICO DEL PROYECTO:**

```sql
-- Queremos: Categorías con más de $1,000,000 en ventas,
-- solo considerando transacciones > $100

SELECT 
    category,
    SUM(total_sale) AS ventas_totales,
    COUNT(*) AS transacciones
FROM datos_limpios
WHERE total_sale > 100        -- ← Filtra FILAS (antes de agrupar)
GROUP BY category
HAVING SUM(total_sale) > 1000000  -- ← Filtra GRUPOS (después de agrupar)
ORDER BY ventas_totales DESC;
```

**FLUJO DE EJECUCIÓN:**

```
1. FROM datos_limpios          (99,459 filas)
       ↓
2. WHERE total_sale > 100       (85,230 filas después del filtro)
       ↓
3. GROUP BY category            (8 grupos: Clothing, Technology, etc.)
       ↓
4. SUM(total_sale) por grupo    (calcula agregaciones)
       ↓
5. HAVING SUM(...) > 1M         (solo 5 de 8 grupos pasan)
       ↓
6. ORDER BY ventas DESC         (ordena los 5 grupos)
```

**ERRORES COMUNES:**

```sql
-- ❌ ERROR: WHERE no puede usar funciones agregadas
SELECT category, SUM(total_sale)
FROM datos_limpios
WHERE SUM(total_sale) > 1000000  -- ¡FALLA!
GROUP BY category;

-- ✅ CORRECTO: HAVING usa funciones agregadas
SELECT category, SUM(total_sale)
FROM datos_limpios
GROUP BY category
HAVING SUM(total_sale) > 1000000;  -- ✅ OK

-- ❌ ERROR: HAVING filtra columnas individuales (usar WHERE)
SELECT category, total_sale
FROM datos_limpios
HAVING total_sale > 100;  -- ¡Ineficiente!

-- ✅ CORRECTO: WHERE filtra filas individuales
SELECT category, total_sale
FROM datos_limpios
WHERE total_sale > 100;  -- ✅ Más eficiente
```

**TABLA RESUMEN:**

| Cláusula | ¿Cuándo se aplica? | Puede usar agregaciones | Ejemplo |
|----------|-------------------|------------------------|---------|
| WHERE | ANTES de GROUP BY | ❌ NO | `WHERE age > 25` |
| HAVING | DESPUÉS de GROUP BY | ✅ SÍ | `HAVING SUM(sale) > 1000` |

**En nuestro proyecto:**
```sql
-- Item 5: Top 5 categorías más vendidas
SELECT category, SUM(quantity) AS total
FROM datos_limpios
-- No necesitamos WHERE (procesamos todo)
GROUP BY category
-- No necesitamos HAVING (queremos todas, luego limitamos con LIMIT)
ORDER BY total DESC
LIMIT 5;
```

---

**14. ¿Cómo se relaciona su trabajo con el temario de Base de Datos II?**

**RESPUESTA EJECUTIVA:**

Nuestro proyecto cubre **7 temas del programa**:

| Tema | Aplicación en el proyecto |
|------|--------------------------|
| **1. Bases relacionales** | Tabla SQLite con 99,459 tuplas, tipos INTEGER/REAL/TEXT |
| **2. Normalización** | Análisis 3FN, decisión consciente de desnormalizar para OLAP |
| **3. SQL (SELECT)** | Consultas con GROUP BY, ORDER BY, LIMIT, funciones agregadas (SUM, COUNT, AVG) |
| **4. JOINs** | `pd.merge()` en Pandas equivalente a LEFT JOIN SQL |
| **5. Importar CSV** | `pd.read_csv()` → `.to_sql()` (proceso ETL completo) |
| **6. Integridad** | Validaciones: `.dropna()`, assertions, verificación post-carga |
| **7. NoSQL** | Análisis teórico: cuándo usar MongoDB vs SQL |

**EJEMPLO INTEGRADOR:**

```python
# EXTRACT (importar CSV - Tema 5)
df = pd.read_csv('sales_data.csv')

# TRANSFORM (validar integridad - Tema 6)
df = df.dropna(subset=['customer_id', 'price'])
assert (df['price'] > 0).all()

# JOIN (Tema 4)
df_combined = pd.merge(df_sales, df_customers, on='customer_id', how='left')

# LOAD (base relacional - Tema 1)
conn = sqlite3.connect('ventas.db')
df.to_sql('datos_limpios', conn, if_exists='replace')

# QUERY (SQL - Tema 3)
cursor.execute('''
    SELECT category, SUM(total_sale) AS ventas
    FROM datos_limpios
    GROUP BY category
    ORDER BY ventas DESC
    LIMIT 5
''')
```

**Este código integra 5 temas de Base de Datos II en un pipeline ETL real.**

---

5. **En la conversión de fechas, ¿por qué especifican `format='%d-%m-%Y'`? ¿Qué pasa si lo omiten?**
   
   **RESPUESTA COMPLETA:**
   
   Especificar el formato tiene **tres ventajas críticas**:
   
   **1. RENDIMIENTO (10-20x más rápido)**
   ```python
   # Con formato explícito (rápido)
   df['invoice_date'] = pd.to_datetime(df['invoice_date'], format='%d-%m-%Y')
   # Pandas sabe exactamente cómo parsear: día-mes-año
   
   # Sin formato (lento)
   df['invoice_date'] = pd.to_datetime(df['invoice_date'])
   # Pandas debe "adivinar" el formato, probando múltiples patrones
   ```
   
   **2. EVITA AMBIGÜEDAD (dd/mm vs mm/dd)**
   
   Ejemplo del problema:
   ```
   Fecha en CSV: "01-02-2023"
   
   Sin format:
   - ¿Es 1 de febrero o 2 de enero?
   - Pandas usa convención de tu sistema (en USA: mm-dd, en Argentina: dd-mm)
   - ¡El mismo código da resultados diferentes en distintas computadoras!
   
   Con format='%d-%m-%Y':
   - Siempre interpreta como 1 de febrero de 2023
   - Comportamiento consistente en cualquier máquina
   ```
   
   **3. CONTROL Y VALIDACIÓN**
   - Si el CSV tiene formato inconsistente, Pandas lanza error inmediatamente
   - Sin format, podría convertir mal sin avisar
   - Detecta errores temprano en el pipeline ETL
   
   **Códigos de formato importantes:**
   - `%d`: día (01-31)
   - `%m`: mes (01-12)
   - `%Y`: año 4 dígitos (2023)
   - `%y`: año 2 dígitos (23)
   - `%H`: hora 24h (00-23)
   - `%M`: minutos (00-59)
   
   **En nuestro proyecto:**
   Los CSV de Kaggle tienen formato `15-03-2023` (dd-mm-yyyy turco), especificar `format='%d-%m-%Y'` garantiza que se interprete correctamente en Colab (servidor en USA) y en laptops locales (Argentina).

---

6. **¿Qué diferencia hay entre `.dt.strftime('%Y-%m-%d')` y `.astype(str)`?**
   
   **RESPUESTA COMPLETA:**
   
   Ambas convierten a string, pero con **control y resultado muy diferentes**:
   
   **`.dt.strftime('%Y-%m-%d')` - Formato controlado**
   
   Características:
   - Solo funciona con columnas datetime64
   - Requiere el accessor `.dt` (similar a `.str` para strings)
   - Permite **formato personalizado** con códigos de formato
   - Salida consistente y predecible
   
   ```python
   # Entrada: datetime64
   df['invoice_date'] = pd.to_datetime(['2023-03-15', '2023-12-01'])
   
   # Con strftime (control total)
   df['fecha_str'] = df['invoice_date'].dt.strftime('%Y-%m-%d')
   # Resultado: ['2023-03-15', '2023-12-01']
   
   df['fecha_formateada'] = df['invoice_date'].dt.strftime('%d/%m/%Y')
   # Resultado: ['15/03/2023', '01/12/2023']
   
   df['mes_año'] = df['invoice_date'].dt.strftime('%B %Y')
   # Resultado: ['March 2023', 'December 2023']
   ```
   
   **`.astype(str)` - Conversión directa sin control**
   
   Características:
   - Funciona con cualquier tipo de dato
   - Convierte "como venga" sin formato específico
   - Incluye información de hora si existe (aunque sea 00:00:00)
   - No permite personalización
   
   ```python
   # Con astype(str) (sin control)
   df['fecha_str'] = df['invoice_date'].astype(str)
   # Resultado: ['2023-03-15 00:00:00', '2023-12-01 00:00:00']
   # ¡Agrega hora innecesaria!
   ```
   
   **¿Cuándo usar cada una?**
   
   | Situación | Usar |
   |-----------|------|
   | Guardar en SQLite con formato específico | `.dt.strftime()` |
   | Formatear para visualización (reportes) | `.dt.strftime()` |
   | Conversión rápida sin requisitos | `.astype(str)` |
   | Crear columnas como "2023-Q1" | `.dt.strftime()` |
   
   **En nuestro proyecto (cargar_a_sqlite.py línea 137):**
   ```python
   df['invoice_date'] = pd.to_datetime(df['invoice_date']).dt.strftime('%Y-%m-%d')
   ```
   Usamos `.dt.strftime()` porque SQLite espera fechas en formato ISO 8601 estricto (`YYYY-MM-DD`) sin componente de hora.

---

7. **Usan `.dropna(subset=['customer_id'])`. ¿Qué otras estrategias existen para manejar nulos?**
   
   **RESPUESTA COMPLETA:**
   
   Existen **5 estrategias principales** para manejar valores nulos, cada una con casos de uso específicos:
   
   **1. ELIMINAR (lo que usamos) - `.dropna()`**
   
   ```python
   # Eliminar filas con nulos en columnas críticas
   df_clean = df.dropna(subset=['customer_id', 'price'])
   
   # Eliminar filas con cualquier nulo
   df_clean = df.dropna()
   
   # Eliminar columnas con muchos nulos
   df_clean = df.dropna(axis=1, thresh=1000)  # mantener columnas con ≥1000 no-nulos
   ```
   
   **Cuándo usar:** Columnas críticas (IDs, precios), pocos nulos (<5%), datos no recuperables
   
   **2. RELLENAR CON VALOR CONSTANTE - `.fillna()`**
   
   ```python
   # Rellenar con cero
   df['quantity'].fillna(0, inplace=True)
   
   # Rellenar con string
   df['payment_method'].fillna('Unknown', inplace=True)
   
   # Rellenar con diccionario (diferentes valores por columna)
   df.fillna({'age': 0, 'gender': 'Not specified'}, inplace=True)
   ```
   
   **Cuándo usar:** Valores default razonables, datos categóricos, análisis que tolera "Unknown"
   
   **3. IMPUTACIÓN ESTADÍSTICA - fillna con agregaciones**
   
   ```python
   # Rellenar con media (datos numéricos)
   df['age'].fillna(df['age'].mean(), inplace=True)
   
   # Rellenar con mediana (más robusta contra outliers)
   df['price'].fillna(df['price'].median(), inplace=True)
   
   # Rellenar con moda (más frecuente)
   df['category'].fillna(df['category'].mode()[0], inplace=True)
   ```
   
   **Cuándo usar:** Datos numéricos con distribución normal, mantener estadísticas del dataset
   
   **4. INTERPOLACIÓN - `.interpolate()`**
   
   ```python
   # Interpolar linealmente (series temporales)
   df['temperatura'] = df['temperatura'].interpolate(method='linear')
   
   # Interpolación por fecha
   df['ventas_diarias'] = df['ventas_diarias'].interpolate(method='time')
   ```
   
   **Cuándo usar:** Series temporales, datos secuenciales, tendencias continuas
   
   **5. FORWARD FILL / BACKWARD FILL - `.ffill()` / `.bfill()`**
   
   ```python
   # Forward fill: propagar último valor válido hacia adelante
   df['estado'] = df['estado'].ffill()
   
   # Backward fill: propagar siguiente valor válido hacia atrás
   df['categoria'] = df['categoria'].bfill()
   ```
   
   **Cuándo usar:** Datos que "persisten" (ej: estado de máquina), registros cronológicos
   
   **¿Por qué elegimos `.dropna()` en nuestro proyecto?**
   
   Decisiones específicas:
   1. **customer_id:** Campo clave para merge, sin él el registro no tiene sentido → ELIMINAR
   2. **price:** Valor crítico para análisis de ingresos, no podemos "inventar" precios → ELIMINAR
   3. **Cantidad de nulos:** Muy baja (<0.1% del dataset), eliminar no afecta análisis
   4. **Integridad:** Preferimos dataset más pequeño pero 100% confiable que rellenar con valores artificiales
   
   **Estrategia alternativa que podríamos haber usado:**
   ```python
   # Imputar age con mediana por género
   df.loc[df['gender']=='Female', 'age'] = df.loc[df['gender']=='Female', 'age'].fillna(
       df.loc[df['gender']=='Female', 'age'].median()
   )
   ```

---

8. **¿Por qué crearon la columna `total_sale` multiplicando quantity * price? ¿No estaba ya en el CSV?**
   
   **RESPUESTA COMPLETA:**
   
   **Respuesta directa:** NO, el CSV original no incluía el monto total de cada transacción. Solo tenía `quantity` (cantidad de artículos) y `price` (precio unitario).
   
   **¿Por qué es necesaria esta columna calculada?**
   
   **1. ANÁLISIS DE INGRESOS**
   ```python
   # Sin total_sale (incorrecto)
   total_ingresos = df['price'].sum()  
   # ¡ERROR! Suma precios unitarios, no ventas reales
   # Si alguien compró 5 camisas a $50 → cuenta $50 en vez de $250
   
   # Con total_sale (correcto)
   df['total_sale'] = df['quantity'] * df['price']
   total_ingresos = df['total_sale'].sum()  
   # Correcto: 5 × $50 = $250 por transacción
   ```
   
   **2. REQUERIMIENTOS DEL ANÁLISIS**
   
   El Item 5 pide "total de ventas por mes" y "categoría con más ingresos":
   ```python
   # Ventas totales por mes
   ventas_mensuales = df.groupby('month')['total_sale'].sum()
   
   # Top categorías por ingresos
   top_categorias = df.groupby('category')['total_sale'].sum().sort_values(ascending=False)
   ```
   Sin `total_sale`, estos análisis serían imposibles o incorrectos.
   
   **3. PRINCIPIO DE DATOS DERIVADOS**
   
   En ETL es común crear **columnas calculadas** durante Transform:
   - **Datos atómicos (CSV):** quantity=5, price=50
   - **Datos derivados (calculados):** total_sale=250
   - **Ventaja:** Cálculo una sola vez, consultas posteriores más rápidas
   
   **4. EJEMPLO REAL DEL DATASET**
   ```
   CSV original:
   invoice_no | quantity | price | category
   I001       | 3        | 25.50 | Clothing
   I002       | 1        | 149.99| Technology
   
   Después de transformación:
   invoice_no | quantity | price | category   | total_sale
   I001       | 3        | 25.50 | Clothing   | 76.50
   I002       | 1        | 149.99| Technology | 149.99
   
   Ahora podemos: sum(total_sale) = $226.49 (correcto)
   ```
   
   **5. PERSISTENCIA EN BASE DE DATOS**
   
   Guardamos `total_sale` en SQLite (schema.sql):
   ```sql
   CREATE TABLE datos_limpios (
       ...
       quantity INTEGER,
       price REAL,
       total_sale REAL,  -- Columna calculada persistida
       ...
   );
   ```
   
   **Alternativa (menos eficiente):** Calcular en cada consulta SQL
   ```sql
   -- Sin columna total_sale (repetir cálculo siempre)
   SELECT SUM(quantity * price) FROM datos_limpios;  -- Más lento
   
   -- Con columna total_sale (pre-calculado)
   SELECT SUM(total_sale) FROM datos_limpios;  -- Más rápido
   ```
   
   **Conclusión:** `total_sale` es una **feature engineering básica** necesaria para análisis de ingresos, no venía en los datos originales y debíamos calcularla en la fase Transform del ETL.

---

9. **Explícame qué hace `.dt.day_name()` y qué tipo de dato devuelve.**
   
   **RESPUESTA COMPLETA:**
   
   `.dt.day_name()` es un **método del accessor .dt** que extrae el nombre del día de la semana de una columna datetime.
   
   **Funcionamiento técnico:**
   
   ```python
   # Columna datetime64
   df['invoice_date'] = pd.to_datetime(['2023-03-15', '2023-03-17', '2023-03-20'])
   
   # Extraer nombre del día
   df['day_of_week'] = df['invoice_date'].dt.day_name()
   
   # Resultado
   print(df['day_of_week'])
   # 0    Wednesday
   # 1    Friday
   # 2    Monday
   # dtype: object  ← Tipo de dato: string (object en Pandas)
   ```
   
   **Tipo de dato devuelto:** `object` (que en Pandas significa **string/texto**)
   
   **Otros métodos similares del accessor `.dt`:**
   
   ```python
   df['year'] = df['invoice_date'].dt.year           # int64: 2023
   df['month'] = df['invoice_date'].dt.month         # int64: 3
   df['day'] = df['invoice_date'].dt.day             # int64: 15
   df['dayofweek'] = df['invoice_date'].dt.dayofweek # int64: 2 (lunes=0)
   df['quarter'] = df['invoice_date'].dt.quarter     # int64: 1
   df['weekday'] = df['invoice_date'].dt.weekday     # int64: 2
   
   # Métodos que devuelven string
   df['day_name'] = df['invoice_date'].dt.day_name()     # object: "Wednesday"
   df['month_name'] = df['invoice_date'].dt.month_name() # object: "March"
   ```
   
   **¿Para qué lo usamos en el proyecto?**
   
   **1. ANÁLISIS DE PATRONES DE COMPRA POR DÍA**
   ```python
   # Ventas por día de la semana
   ventas_por_dia = df.groupby('day_of_week')['total_sale'].sum()
   
   # Resultado (ejemplo):
   # Friday       $1,250,000
   # Monday       $980,000
   # Saturday     $1,500,000  ← Más ventas el fin de semana
   # Sunday       $1,450,000
   # ...
   ```
   
   **2. VISUALIZACIONES**
   ```python
   # Gráfico de ventas por día de semana
   df.groupby('day_of_week')['total_sale'].sum().plot(kind='bar')
   plt.title('Ventas por Día de la Semana')
   plt.xlabel('Día')
   plt.ylabel('Ventas Totales ($)')
   ```
   
   **3. SEGMENTACIÓN DE ESTRATEGIAS**
   - Identificar días pico de ventas
   - Planificar personal en tienda
   - Optimizar campañas de marketing (enviar emails viernes para compras de fin de semana)
   
   **Localización (importante):**
   ```python
   # Cambiar idioma de nombres de días
   import locale
   locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Español
   df['dia_semana'] = df['invoice_date'].dt.day_name()
   # Resultado: "miércoles", "viernes", "lunes"
   ```
   
   **Orden correcto para visualización:**
   ```python
   # Problema: orden alfabético
   df.groupby('day_of_week')['total_sale'].sum().plot()
   # Friday, Monday, Saturday... ¡mal orden!
   
   # Solución: usar Categorical con orden
   dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                 'Friday', 'Saturday', 'Sunday']
   df['day_of_week'] = pd.Categorical(df['day_of_week'], 
                                       categories=dias_orden, 
                                       ordered=True)
   df.groupby('day_of_week')['total_sale'].sum().plot()
   # Ahora sí: lunes a domingo en orden correcto
   ```

---

### 🟣 **BLOQUE 3: ANÁLISIS ESTADÍSTICO Y VISUALIZACIÓN**

10. **¿Qué diferencia hay entre `mean()`, `median()` y `mode()`? ¿Cuándo usarías cada una?**
    
    **RESPUESTA COMPLETA:**
    
    Son tres **medidas de tendencia central** que resumen datos de forma diferente:
    
    **MEAN (Media aritmética) - `.mean()`**
    
    **Definición:** Suma de todos los valores dividido por la cantidad
    ```python
    # Ejemplo
    precios = [10, 15, 20, 25, 1000]  # ← outlier
    media = sum(precios) / len(precios) = 1070 / 5 = 214
    
    df['price'].mean()  # Pandas
    ```
    
    **Características:**
    - ✅ Usa TODOS los valores
    - ❌ **MUY sensible a outliers** (valores extremos)
    - ✅ Útil para distribuciones normales (campana de Gauss)
    - ✅ Permite operaciones algebraicas
    
    **Cuándo usar:** Datos sin outliers, distribución simétrica, cuando necesitas sumar/restar medias
    
    ---
    
    **MEDIAN (Mediana) - `.median()`**
    
    **Definición:** Valor central cuando ordenas los datos
    ```python
    # Mismo ejemplo
    precios = [10, 15, 20, 25, 1000]
    ordenados = [10, 15, 20, 25, 1000]
                        ↑
                   valor central
    mediana = 20  # ¡Mucho más representativa!
    
    df['price'].median()  # Pandas
    ```
    
    **Características:**
    - ✅ **ROBUSTA contra outliers** (ignora valores extremos)
    - ✅ Representa el "dato típico" mejor que la media
    - ❌ No usa todos los valores (solo posición central)
    - ✅ Divide el dataset en dos mitades iguales (50% arriba, 50% abajo)
    
    **Cuándo usar:** Datos con outliers, salarios, precios de vivienda, distribuciones asimétricas
    
    ---
    
    **MODE (Moda) - `.mode()`**
    
    **Definición:** Valor MÁS FRECUENTE
    ```python
    # Ejemplo
    payment_methods = ['Cash', 'Cash', 'Credit Card', 'Cash', 'Debit Card']
    moda = 'Cash'  # Aparece 3 veces
    
    df['payment_method'].mode()[0]  # Pandas (devuelve Series, tomamos primer elemento)
    ```
    
    **Características:**
    - ✅ **ÚNICA medida para datos categóricos** (texto)
    - ✅ Identifica el valor "más popular"
    - ❌ Puede no existir (todos diferentes) o ser múltiple (varios empates)
    - ✅ No afectada por outliers
    
    **Cuándo usar:** Datos categóricos (género, método de pago, categoría), identificar tendencias de preferencia
    
    ---
    
    **COMPARACIÓN VISUAL (Ejemplo con salarios):**
    ```
    Salarios en una empresa:
    [30k, 32k, 35k, 38k, 40k, 45k, 50k, 500k]  ← CEO
                              ↑
    Media:    96.25k  ❌ Engañosa (nadie gana eso)
    Mediana:  39k     ✅ Representativa del empleado típico
    Moda:     No hay  ⚠️ Todos diferentes
    ```
    
    **EN NUESTRO PROYECTO:**
    
    ```python
    # Item 4: Análisis de precios por categoría
    df.groupby('category')['price'].agg([
        ('Precio_Minimo', 'min'),
        ('Precio_Maximo', 'max'),
        ('Precio_Promedio', 'mean'),    # ← Media
        ('Precio_Mediana', 'median'),   # ← Mediana
    ])
    
    # Item 4a: Método de pago más frecuente
    metodo_mas_comun = df['payment_method'].mode()[0]  # ← Moda
    # Resultado: "Cash" (no tiene sentido calcular media de texto)
    ```
    
    **CUÁNDO USAR CADA UNA (Decisión rápida):**
    
    | Tipo de dato | Distribución | Medida recomendada |
    |--------------|--------------|-------------------|
    | Numérico simétrico sin outliers | Normal | **Mean** |
    | Numérico con outliers | Asimétrica | **Median** |
    | Categórico (texto) | Cualquiera | **Mode** |
    | Salarios, precios vivienda | Asimétrica | **Median** |
    | Edad en población equilibrada | Normal | **Mean** |
    | Método de pago preferido | Categórica | **Mode** |

---

11. **En el Item 4, calculan el método de pago más frecuente. ¿Qué función de Pandas usan?**
    
    **RESPUESTA COMPLETA:**
    
    Usamos **`.value_counts()`**, una de las funciones más útiles de Pandas para análisis exploratorio.
    
    **FUNCIONAMIENTO:**
    
    ```python
    # Sintaxis básica
    df['payment_method'].value_counts()
    
    # Resultado (Series ordenado por frecuencia):
    Cash           44397
    Credit Card    34898
    Debit Card     20043
    Name: payment_method, dtype: int64
    ```
    
    **LO QUE HACE INTERNAMENTE:**
    1. Agrupa valores únicos de la columna
    2. Cuenta cuántas veces aparece cada uno
    3. Ordena de mayor a menor (por defecto)
    4. Devuelve un Series con índice=valores y valores=conteos
    
    **PARÁMETROS ÚTILES:**
    
    ```python
    # Normalizar (porcentajes en lugar de conteos)
    df['payment_method'].value_counts(normalize=True)
    # Resultado:
    # Cash           0.446  (44.6%)
    # Credit Card    0.351  (35.1%)
    # Debit Card     0.202  (20.2%)
    
    # Incluir valores nulos en el conteo
    df['payment_method'].value_counts(dropna=False)
    
    # Orden ascendente (menos a más frecuente)
    df['payment_method'].value_counts(ascending=True)
    
    # Solo top N más frecuentes
    df['category'].value_counts().head(3)
    ```
    
    **OPERACIONES COMUNES CON value_counts():**
    
    ```python
    # 1. Obtener el más frecuente (moda)
    metodo_mas_frecuente = df['payment_method'].value_counts().idxmax()
    # o más simple:
    metodo_mas_frecuente = df['payment_method'].mode()[0]
    
    # 2. Obtener la frecuencia del más frecuente
    frecuencia_max = df['payment_method'].value_counts().max()
    
    # 3. Porcentaje del más frecuente
    porcentaje = (frecuencia_max / len(df)) * 100
    
    # 4. Crear diccionario
    dict_conteos = df['payment_method'].value_counts().to_dict()
    # {'Cash': 44397, 'Credit Card': 34898, 'Debit Card': 20043}
    ```
    
    **EN NUESTRO PROYECTO (Item 4):**
    
    ```python
    # Item 4a: Método de pago más frecuente (todos los clientes)
    print('=== ANÁLISIS DE MÉTODOS DE PAGO ===')
    payment_counts = df_clean['payment_method'].value_counts()
    print(payment_counts)
    print(f'\nEl método de pago más utilizado es: {payment_counts.idxmax()}')
    print(f'Cantidad: {payment_counts.max()} transacciones')
    print(f'Porcentaje: {(payment_counts.max() / len(df_clean) * 100):.2f}%')
    
    # Item 4c: Métodos de pago rango 25-35 años
    df_age_25_35 = df_clean[(df_clean['age'] >= 25) & (df_clean['age'] <= 35)]
    payment_25_35 = df_age_25_35['payment_method'].value_counts()
    print((payment_25_35 / len(df_age_25_35) * 100).round(2))
    ```
    
    **ALTERNATIVAS (menos eficientes):**
    
    ```python
    # Opción 1: groupby + count (más verboso)
    df.groupby('payment_method').size().sort_values(ascending=False)
    
    # Opción 2: groupby + count de columna
    df.groupby('payment_method')['invoice_no'].count().sort_values(ascending=False)
    
    # Opción 3: Python puro (LENTO para datasets grandes)
    from collections import Counter
    Counter(df['payment_method']).most_common()
    ```
    
    **VENTAJA DE value_counts():** Más rápida, sintaxis más limpia, optimizada en C (bajo nivel)
    
    **VISUALIZACIÓN:**
    ```python
    # Gráfico de barras directamente desde value_counts
    df['payment_method'].value_counts().plot(kind='bar')
    plt.title('Frecuencia de Métodos de Pago')
    plt.ylabel('Cantidad de Transacciones')
    plt.show()
    
    # Gráfico de torta
    df['payment_method'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    ```

---

12. **¿Cómo interpretarías un coeficiente de correlación de 0.95 entre dos variables?**
    
    **RESPUESTA COMPLETA:**
    
    Un coeficiente de correlación de **0.95** indica una **correlación positiva muy fuerte** entre dos variables.
    
    **INTERPRETACIÓN TÉCNICA:**
    
    **Escala del coeficiente de correlación (Pearson):**
    ```
    -1.0 ← Correlación negativa perfecta
    -0.9 ← Correlación negativa muy fuerte
    -0.7 ← Correlación negativa fuerte
    -0.5 ← Correlación negativa moderada
    -0.3 ← Correlación negativa débil
     0.0 ← Sin correlación
    +0.3 ← Correlación positiva débil
    +0.5 ← Correlación positiva moderada
    +0.7 ← Correlación positiva fuerte
    +0.9 ← Correlación positiva muy fuerte
    +0.95 ← ¡TU CASO! Correlación positiva muy fuerte
    +1.0 ← Correlación positiva perfecta
    ```
    
    **¿Qué significa 0.95?**
    
    1. **Relación lineal muy fuerte:** Cuando una variable aumenta, la otra también aumenta de forma casi proporcional
    2. **Predictibilidad alta:** Conociendo el valor de X, puedes predecir Y con ~90% de precisión (R² = 0.95² = 0.90)
    3. **Movimiento conjunto:** Las variables "se mueven juntas" casi siempre
    
    **EJEMPLO PRÁCTICO:**
    
    ```python
    # Supongamos correlación 0.95 entre quantity y total_sale
    import numpy as np
    import pandas as pd
    
    # Crear datos correlacionados
    quantity = np.array([1, 2, 3, 4, 5, 10, 15, 20])
    total_sale = quantity * 25 + np.random.normal(0, 2, len(quantity))  # Casi lineal con ruido mínimo
    
    df = pd.DataFrame({'quantity': quantity, 'total_sale': total_sale})
    correlacion = df['quantity'].corr(df['total_sale'])
    print(f'Correlación: {correlacion:.2f}')  # ~0.95
    
    # Visualizar
    import matplotlib.pyplot as plt
    plt.scatter(df['quantity'], df['total_sale'])
    plt.xlabel('Quantity')
    plt.ylabel('Total Sale')
    plt.title('Correlación 0.95 (Muy Fuerte)')
    # Los puntos forman una línea casi perfecta con ligera dispersión
    ```
    
    **⚠️ ADVERTENCIA CRÍTICA: CORRELACIÓN ≠ CAUSALIDAD**
    
    **Ejemplo clásico del error:**
    ```
    Correlación 0.95 entre:
    - Ventas de helado
    - Ahogamientos en piscinas
    
    ❌ INTERPRETACIÓN INCORRECTA: "Los helados causan ahogamientos"
    ✅ INTERPRETACIÓN CORRECTA: "Ambos aumentan en verano" (variable oculta: temperatura)
    ```
    
    **MÁS EJEMPLOS DE CORRELACIONES ESPURIAS (falsas):**
    - Número de piratas vs temperatura global (correlación negativa fuerte, ¡pero sin relación!)
    - Consumo de queso per cápita vs muertes por estrangulamiento con sábanas
    
    **EN NUESTRO PROYECTO:**
    
    ```python
    # Matriz de correlación
    correlacion_matrix = df_clean[['quantity', 'price', 'total_sale', 'age']].corr()
    print(correlacion_matrix)
    
    # Visualizar con heatmap
    import seaborn as sns
    sns.heatmap(correlacion_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Matriz de Correlación')
    ```
    
    **Correlaciones esperadas en nuestro dataset:**
    - `quantity` vs `total_sale`: **~0.85-0.95** (fuerte positiva) - ¡obvio! total = quantity × price
    - `age` vs `total_sale`: **~0.1-0.3** (débil/moderada) - edades mayores podrían gastar más
    - `price` vs `quantity`: **~-0.2-0.0** (débil negativa/nula) - productos caros se compran en menor cantidad
    
    **CONCLUSIÓN PARA EL COLOQUIO:**
    
    "Un coeficiente de 0.95 indica que las variables tienen una relación lineal muy fuerte y positiva. Cuando una aumenta, la otra también lo hace de forma casi proporcional. Sin embargo, esto NO implica causalidad: debemos analizar el contexto para determinar si hay una relación causa-efecto o si ambas están influidas por una tercera variable. En nuestro proyecto, encontramos correlaciones fuertes esperadas, como entre quantity y total_sale, que son consistentes con la lógica del negocio."

---

13. **En los gráficos, ¿por qué usan `plt.figure(figsize=(12,6))`? ¿Qué pasa si lo omiten?**
    
    **RESPUESTA COMPLETA:**
    
    `plt.figure(figsize=(12,6))` configura el **tamaño físico del gráfico** antes de dibujar.
    
    **PARÁMETROS:**
    - `figsize=(ancho, alto)` en **pulgadas** (inches)
    - `(12, 6)` = 12 pulgadas de ancho × 6 de alto
    - Matplotlib usa DPI (dots per inch) para convertir a píxeles: 12"×100 DPI = 1200px ancho
    
    **¿QUÉ PASA SI LO OMITES?**
    
    ```python
    # Sin especificar tamaño (usa default)
    plt.plot(x, y)
    plt.show()
    # Tamaño default: figsize=(6.4, 4.8) - muy pequeño para presentaciones
    ```
    
    **Resultado:** Gráfico pequeño, difícil de leer, etiquetas comprimidas, no apto para reportes/presentaciones
    
    **CON figsize (correcto):**
    
    ```python
    # Especificar tamaño apropiado
    plt.figure(figsize=(12, 6))  # Panorámico, ideal para dashboards
    plt.plot(x, y)
    plt.title('Ventas Mensuales')
    plt.show()
    ```
    
    **TAMAÑOS COMUNES Y SUS USOS:**
    
    ```python
    # Cuadrado (análisis exploratorio)
    plt.figure(figsize=(8, 8))  # Matrices de correlación, scatter plots
    
    # Panorámico horizontal (series temporales)
    plt.figure(figsize=(12, 6))  # ← LO QUE USAMOS
    # Ideal para: líneas de tiempo, barras horizontales, múltiples categorías
    
    # Panorámico ancho (muchas categorías)
    plt.figure(figsize=(15, 5))  # Gráficos con 20+ barras
    
    # Vertical (rankings)
    plt.figure(figsize=(6, 10))  # Top 20 productos (barras horizontales)
    
    # Presentación (PowerPoint)
    plt.figure(figsize=(10, 5.625))  # Ratio 16:9 para slides
    
    # Publicación científica
    plt.figure(figsize=(7, 5))  # Estándar para papers
    ```
    
    **EN NUESTRO PROYECTO:**
    
    ```python
    # Item 6: Gráfico de ventas mensuales
    plt.figure(figsize=(12, 6))  # ← Panorámico para ver tendencia temporal
    ventas_por_mes.plot(kind='line', marker='o')
    plt.title('Evolución de Ventas Mensuales (2021-2023)')
    plt.xlabel('Mes')
    plt.ylabel('Ventas Totales ($)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()  # Ajusta automáticamente para que no se corten labels
    plt.savefig('visualizaciones/ventas_mensuales.png', dpi=300, bbox_inches='tight')
    plt.show()
    ```
    
    **¿POR QUÉ (12, 6) ESPECÍFICAMENTE?**
    
    1. **Ratio 2:1 (panorámico):** Ideal para series temporales, data que crece horizontalmente
    2. **Compatible con notebooks:** Se ve bien en Jupyter/Colab sin scroll
    3. **Profesional:** Tamaño apropiado para reportes Word/PDF
    4. **Legible:** Suficiente espacio para etiquetas de eje X con muchas categorías
    
    **OTROS PARÁMETROS DE figure():**
    
    ```python
    plt.figure(
        figsize=(12, 6),      # Tamaño
        dpi=100,              # Resolución (default: 100, para guardar: 300)
        facecolor='white',    # Color de fondo
        edgecolor='black',    # Borde
        tight_layout=True     # Auto-ajuste de márgenes
    )
    ```
    
    **COMPARACIÓN VISUAL:**
    ```
    Default (6.4, 4.8):
    ┌─────────┐  ← Muy pequeño, difícil de leer
    │  📊     │
    └─────────┘
    
    Nuestro (12, 6):
    ┌──────────────────────┐  ← Panorámico, ideal para presentar
    │      📊📊📊          │
    └──────────────────────┘
    ```
    
    **CONFIGURACIÓN GLOBAL (alternativa):**
    
    ```python
    # Configurar tamaño default para toda la sesión
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['figure.dpi'] = 100
    
    # Ahora todos los gráficos usan este tamaño sin especificarlo
    plt.plot(x, y)  # Ya es (12,6) automáticamente
    ```

---

14. **¿Qué biblioteca usaron para generar los gráficos y por qué?**
    
    **RESPUESTA COMPLETA:**
    
    Usamos **Matplotlib** (específicamente el módulo `pyplot`), la biblioteca estándar de visualización en Python.
    
    **IMPORT EN NUESTRO CÓDIGO:**
    ```python
    import matplotlib.pyplot as plt
    
    # Configuración adicional
    plt.style.use('default')  # Estilo visual
    plt.rcParams['figure.figsize'] = (12, 6)  # Tamaño default
    plt.rcParams['font.size'] = 10  # Tamaño de fuente
    ```
    
    **¿POR QUÉ MATPLOTLIB?**
    
    **1. ESTÁNDAR DE LA INDUSTRIA**
    - Biblioteca más madura (desde 2003, ~20 años)
    - Usada en investigación científica, finanzas, ingeniería
    - Documentación extensa y comunidad gigante
    
    **2. INTEGRACIÓN CON PANDAS**
    ```python
    # Pandas usa Matplotlib internamente
    df.plot()  # ← Llama a matplotlib por detrás
    df['price'].hist()  # ← Matplotlib
    df.groupby('category')['total_sale'].sum().plot(kind='bar')  # ← Matplotlib
    ```
    
    **3. CONTROL GRANULAR**
    - Personalización extrema de cada elemento
    - Desde colores hasta posición exacta de etiquetas
    - Ideal para publicaciones científicas con requisitos específicos
    
    **4. MÚLTIPLES BACKENDS**
    - Funciona en Jupyter, Colab, scripts, aplicaciones web
    - Guarda en PNG, PDF, SVG, JPG
    - Compatible con diferentes entornos sin cambios
    
    **5. BASE PARA OTRAS BIBLIOTECAS**
    - Seaborn (gráficos estadísticos) usa Matplotlib
    - Pandas .plot() usa Matplotlib
    - Muchas librerías se construyen sobre ella
    
    **ALTERNATIVAS QUE CONSIDERAMOS:**
    
    | Biblioteca | Ventajas | Por qué NO la usamos |
    |------------|----------|---------------------|
    | **Seaborn** | Gráficos estadísticos bellos, menos código | Requiere más configuración inicial |
    | **Plotly** | Interactivos (zoom, hover), dashboards web | Más pesado, interactividad no necesaria para entrega PDF |
    | **Bokeh** | Interactivos, escalable a millones de puntos | Complejidad innecesaria para este proyecto |
    | **ggplot** | Sintaxis declarativa (estilo R) | Menos mantenida, comunidad más pequeña |
    | **Altair** | Declarativa, JSON specs | Curva de aprendizaje, menos flexible |
    
    **TIPOS DE GRÁFICOS QUE GENERAMOS:**
    
    ```python
    # 1. Gráfico de líneas (tendencias temporales)
    plt.figure(figsize=(12, 6))
    ventas_mensuales.plot(kind='line', marker='o')
    plt.title('Ventas Mensuales')
    plt.grid(True)
    
    # 2. Gráfico de barras (categorías)
    df.groupby('category')['total_sale'].sum().plot(kind='bar', color='steelblue')
    plt.ylabel('Ventas Totales ($)')
    plt.xticks(rotation=45)
    
    # 3. Histograma (distribución)
    plt.hist(df['age'], bins=20, edgecolor='black', alpha=0.7)
    plt.xlabel('Edad')
    plt.ylabel('Frecuencia')
    
    # 4. Gráfico de torta (proporciones)
    df['payment_method'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    
    # 5. Boxplot (distribución con outliers)
    df.boxplot(column='price', by='category', figsize=(12,6))
    ```
    
    **MEJORES PRÁCTICAS QUE APLICAMOS:**
    
    ```python
    # ✅ Buenas prácticas en nuestro código
    plt.figure(figsize=(12, 6))          # Tamaño apropiado
    plt.title('Título Descriptivo')     # Título claro
    plt.xlabel('Eje X')                  # Etiquetar ejes
    plt.ylabel('Ventas ($)')             # Incluir unidades
    plt.grid(True, alpha=0.3)            # Grid sutil para lectura
    plt.tight_layout()                   # Evitar recortes
    plt.savefig('output.png', dpi=300)   # Guardar alta resolución
    plt.show()                           # Mostrar en notebook
    ```
    
    **CONFIGURACIÓN GLOBAL DEL PROYECTO:**
    
    ```python
    # Al inicio del notebook
    import matplotlib.pyplot as plt
    import warnings
    warnings.filterwarnings('ignore')  # Ocultar warnings de visualización
    
    # Estilo y configuración
    plt.style.use('default')  # Otros: 'ggplot', 'seaborn', 'bmh'
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3
    ```
    
    **CONCLUSIÓN PARA EL COLOQUIO:**
    
    "Elegimos Matplotlib porque es el estándar de la industria para visualización en Python, tiene integración nativa con Pandas (que usamos extensivamente), ofrece control granular sobre cada aspecto del gráfico, y es ampliamente documentada. Además, genera gráficos estáticos de alta calidad apropiados para reportes PDF y presentaciones, que era nuestro objetivo de entrega."

---

### 🔴 **BLOQUE 4: PROGRAMACIÓN ORIENTADA A OBJETOS (POO)**

15. **En el código, ¿identificás algún uso de POO? ¿Dónde?**
    - *Esperan:* DataFrames son objetos, métodos como .head(), .groupby(), .plot(), atributos como .columns, .shape

16. **¿Qué es un método en POO? Dame un ejemplo del código.**
    - *Esperan:* Función dentro de una clase, ejemplo: df.dropna(), df.merge(), df.to_sql()

17. **¿Podrías crear una clase `AnalizadorVentas` que encapsule las operaciones del ETL?**
    - *Esperan:* Estructura básica: class AnalizadorVentas, __init__, métodos extraer(), transformar(), cargar()

---

### 🟡 **BLOQUE 5: BUENAS PRÁCTICAS Y DOCUMENTACIÓN**

18. **Veo que usan `warnings.filterwarnings('ignore')`. ¿Es una buena práctica? ¿Por qué?**
    - *Esperan:* NO es ideal en producción, útil para presentación, puede ocultar problemas reales

19. **¿Qué son las docstrings y por qué son importantes?**
    - *Esperan:* Documentación dentro del código con """, accesible con help(), mejora mantenibilidad

20. **Si tuvieras que refactorizar el código, ¿qué mejorarías?**
    - *Esperan:* Modularizar en funciones, agregar try-except, validaciones de entrada, logging, tests unitarios

---

## 👨‍🏫 PROFESOR CARLOS CHARLETTI (BASE DE DATOS II)

### 🔵 **BLOQUE 6: FUNDAMENTOS DE BASES DE DATOS**

21. **¿Por qué eligieron SQLite en lugar de MySQL o PostgreSQL?**
    
    **RESPUESTA COMPLETA:**
    
    Elegimos **SQLite** por razones técnicas y prácticas específicas para este proyecto educativo:
    
    **VENTAJAS DE SQLite PARA NUESTRO CASO:**
    
    **1. ARQUITECTURA SERVERLESS (sin servidor)**
    ```
    SQLite:
    Python → archivo .db (¡listo!)
    
    MySQL/PostgreSQL:
    Python → servidor corriendo → base de datos
              ↑ Requiere instalación, configuración, puerto, usuario, contraseña
    ```
    - No requiere proceso separado corriendo
    - No necesita configurar puertos ni credenciales
    - No hay riesgo de que el servidor "se caiga"
    
    **2. ARCHIVO ÚNICO PORTÁTIL**
    ```python
    # Todo el database en un solo archivo
    ventas.db  # 15 MB, contiene las 99,459 transacciones
    
    # Ventajas:
    - Fácil de compartir (subirlo a GitHub)
    - Backup = copiar un archivo
    - Mover entre computadoras: copy/paste
    - Profesor puede abrir con DB Browser sin configurar nada
    ```
    
    **3. CERO CONFIGURACIÓN**
    ```python
    # SQLite (2 líneas)
    import sqlite3
    conn = sqlite3.connect('ventas.db')  # ¡Listo!
    
    # MySQL (complejo)
    import mysql.connector
    conn = mysql.connector.connect(
        host='localhost',       # ¿Está corriendo el servidor?
        user='root',           # ¿Cuál es el usuario?
        password='tu_password', # ¿Cuál es la contraseña?
        database='ventas'      # ¿Ya creaste la DB?
    )
    # + Instalar MySQL Server (500MB+)
    # + Configurar seguridad
    # + Abrir puerto 3306
    ```
    
    **4. INTEGRACIÓN NATIVA CON PYTHON**
    ```python
    import sqlite3  # ← Incluido en Python estándar, no requiere pip install
    
    # Pandas tiene integración directa
    df.to_sql('datos_limpios', conn, if_exists='replace')  # ¡Una línea!
    ```
    
    **5. IDEAL PARA DESARROLLO Y EDUCACIÓN**
    - Usado en apps móviles (Android/iOS)
    - Prototipos rápidos
    - Pruebas unitarias (databases en memoria)
    - Enseñanza de SQL sin complejidad de servidor
    
    **6. RENDIMIENTO SUFICIENTE PARA NUESTRO CASO**
    ```
    Nuestro dataset: 99,459 registros, ~15 MB
    Capacidad SQLite: Hasta 281 TB teóricos, millones de registros prácticos
    
    Consultas SQL del proyecto: < 100ms todas
    ```
    
    **CUÁNDO SÍ USAR MySQL/PostgreSQL:**
    
    | Situación | Requiere MySQL/PostgreSQL |
    |-----------|-------------------------|
    | Múltiples usuarios concurrentes (>100) | ✅ Sí |
    | Aplicación web en producción | ✅ Sí |
    | Datos > 100 GB | ✅ Sí |
    | Transacciones complejas con rollback | ✅ Sí (mejor ACID) |
    | Replicación maestro-esclavo | ✅ Sí |
    | Proyecto educativo individual | ❌ No (SQLite suficiente) |
    | Análisis de datos local | ❌ No (SQLite suficiente) |
    | Prototipo / MVP | ❌ No (SQLite más rápido) |
    
    **LIMITACIONES DE SQLite (por qué en producción NO):**
    
    ```
    ❌ No soporta múltiples escritores simultáneos (lock de archivo)
    ❌ No tiene usuarios/permisos granulares (solo filesystem)
    ❌ No permite conexiones remotas por red
    ❌ Funciones limitadas vs PostgreSQL (no tiene arrays, JSON avanzado, etc.)
    ❌ No es ideal para datasets > 100 GB
    ```
    
    **COMPARACIÓN RÁPIDA:**
    
    | Característica | SQLite | MySQL | PostgreSQL |
    |----------------|--------|-------|------------|
    | Instalación | ✅ Ninguna | ❌ Compleja | ❌ Compleja |
    | Servidor | ✅ No requiere | ❌ Sí | ❌ Sí |
    | Portabilidad | ✅ Un archivo | ❌ Dump SQL | ❌ Dump SQL |
    | Concurrencia | ❌ Limitada | ✅ Alta | ✅ Muy alta |
    | Funciones SQL | 🟨 Básicas | ✅ Completas | ✅ Avanzadas |
    | Ideal para | Desarrollo, apps móviles, análisis local | Web apps, SaaS | Data warehouses, analítica compleja |
    
    **EN NUESTRO PROYECTO:**
    
    ```python
    # Conexión (cargar_a_sqlite.py línea 42)
    conn = sqlite3.connect('sql/ventas.db')
    
    # Carga de datos
    df_clean.to_sql('datos_limpios', conn, if_exists='replace', index=False)
    
    # Ventajas logradas:
    # ✅ Profesor ejecuta notebook sin instalar servidor
    # ✅ GitHub almacena el .db directamente
    # ✅ Google Colab puede usar SQLite sin configuración
    # ✅ Consultas SQL funcionan igual que en MySQL (estándar SQL)
    ```
    
    **CONCLUSIÓN PARA COLOQUIO:**
    
    "Elegimos SQLite porque es ideal para proyectos educativos y análisis de datos donde no necesitamos múltiples usuarios concurrentes. Nos permitió enfocarnos en aprender SQL y ETL sin perder tiempo en configuración de servidores. El archivo .db es portátil, fácil de compartir en GitHub, y suficientemente potente para nuestros 99,459 registros. Para una aplicación web en producción con cientos de usuarios simultáneos, sí migrar íamos a PostgreSQL o MySQL."

---

22. **¿Qué es normalización? ¿Sus datos están normalizados?**
    
    **RESPUESTA COMPLETA:**
    
    **NORMALIZACIÓN:** Proceso de organizar datos en múltiples tablas relacionadas para eliminar redundancia y mejorar integridad.
    
    **FORMAS NORMALES (progresivas):**
    
    **1FN (Primera Forma Normal):**
    - ✅ Cada celda contiene un solo valor (no listas)
    - ✅ Cada columna tiene tipo de dato único
    - ✅ Cada fila es única (tiene identificador)
    - ✅ No hay grupos repetidos
    
    **2FN (Segunda Forma Normal):**
    - ✅ Cumple 1FN
    - ✅ Todos los atributos dependen completamente de la clave primaria
    - ❌ No hay dependencias parciales
    
    **3FN (Tercera Forma Normal):**
    - ✅ Cumple 2FN
    - ❌ No hay dependencias transitivas (campo→campo→PK)
    - ✅ Atributos no-clave dependen SOLO de la clave primaria
    
    **¿NUESTROS DATOS ESTÁN NORMALIZADOS?**
    
    **RESPUESTA: NO - Tenemos una tabla DESNORMALIZADA (por diseño)**
    
    **Estructura actual (tabla única `datos_limpios`):**
    ```sql
    CREATE TABLE datos_limpios (
        invoice_no TEXT,
        customer_id INTEGER,
        gender TEXT,              -- ← Redundancia
        age INTEGER,              -- ← Redundancia
        category TEXT,
        quantity INTEGER,
        price REAL,
        payment_method TEXT,      -- ← Redundancia
        invoice_date TEXT,
        shopping_mall TEXT,
        total_sale REAL
    );
    ```
    
    **Problema de desnormalización:**
    ```
    invoice_no | customer_id | gender | age | payment_method
    I001       | 1001        | Female | 25  | Cash
    I002       | 1001        | Female | 25  | Cash          ← Repite gender, age
    I003       | 1001        | Female | 25  | Credit Card   ← Repite gender, age
    
    ¡El gender y age del cliente 1001 están replicados en cada compra!
    ```
    
    **Consecuencias de la redundancia:**
    - ❌ Desperdicio de espacio (age, gender repetidos 99,459 veces)
    - ❌ Riesgo de inconsistencia (¿qué pasa si el cliente cambia de edad?)
    - ❌ Anomalías de actualización (cambiar edad requiere UPDATE en miles de filas)
    
    **DISEÑO NORMALIZADO (3FN) - Cómo DEBERÍA ser:**
    
    ```sql
    -- Tabla 1: Clientes (sin redundancia)
    CREATE TABLE clientes (
        customer_id INTEGER PRIMARY KEY,
        gender TEXT,
        age INTEGER,
        payment_method TEXT
    );
    -- Solo 1,000 filas (clientes únicos)
    
    -- Tabla 2: Ventas (sin info demográfica)
    CREATE TABLE ventas (
        invoice_no TEXT PRIMARY KEY,
        customer_id INTEGER,              -- ← Foreign Key
        category TEXT,
        quantity INTEGER,
        price REAL,
        invoice_date TEXT,
        shopping_mall TEXT,
        total_sale REAL,
        FOREIGN KEY (customer_id) REFERENCES clientes(customer_id)
    );
    -- 99,459 filas (transacciones)
    
    -- Para consultar: hacer JOIN
    SELECT v.invoice_no, v.total_sale, c.gender, c.age
    FROM ventas v
    JOIN clientes c ON v.customer_id = c.customer_id;
    ```
    
    **¿POR QUÉ ELEGIMOS DESNORMALIZACIÓN?**
    
    **Razones técnicas válidas:**
    
    **1. OPTIMIZACIÓN PARA ANÁLISIS (Data Warehouse pattern)**
    ```
    Normalizado:
    - Consultas requieren JOIN constante
    - SELECT ventas JOIN clientes JOIN categorías... ← Más lento
    
    Desnormalizado:
    - Todo en una tabla
    - SELECT * FROM datos_limpios WHERE... ← Más rápido
    ```
    
    **2. SIMPLICIDAD DEL PROYECTO**
    - Dataset estático (no cambia)
    - No hay inserciones/actualizaciones frecuentes
    - Foco en análisis, no en CRUD operations
    
    **3. FACILIDAD DE CONSULTA**
    ```sql
    -- Desnormalizado (simple)
    SELECT category, AVG(age), SUM(total_sale)
    FROM datos_limpios
    GROUP BY category;
    
    -- Normalizado (complejo)
    SELECT c.category, AVG(cl.age), SUM(v.total_sale)
    FROM ventas v
    JOIN clientes cl ON v.customer_id = cl.customer_id
    JOIN categorias c ON v.category_id = c.category_id
    GROUP BY c.category;
    ```
    
    **4. ESTÁNDAR EN ANALÍTICA**
    - Data Warehouses (Snowflake, Redshift) usan Star Schema (parcialmente desnormalizado)
    - OLAP (Online Analytical Processing) prioriza lectura sobre escritura
    - BI tools (Tableau, Power BI) funcionan mejor con tablas anchas
    
    **TRADE-OFFS:**
    
    | Aspecto | Normalizado (3FN) | Desnormalizado (nuestro caso) |
    |---------|-------------------|------------------------------|
    | Redundancia de datos | ✅ Mínima | ❌ Alta |
    | Velocidad de lectura | ❌ Requiere JOINs | ✅ Directa |
    | Integridad de datos | ✅ Alta | ❌ Dependiente de ETL |
    | Facilidad de actualización | ✅ Un solo lugar | ❌ Múltiples filas |
    | Espacio en disco | ✅ Menor | ❌ Mayor |
    | Ideal para | Sistemas transaccionales (OLTP) | Sistemas analíticos (OLAP) |
    
    **CONCLUSIÓN PARA COLOQUIO:**
    
    "Nuestros datos NO están normalizados - intencionalmente. Tenemos una tabla desnormalizada tipo Data Warehouse, optimizada para análisis y consultas rápidas. Esto genera redundancia (gender/age repetidos por cada venta), pero es aceptable porque: (1) El dataset es estático, no hay actualizaciones frecuentes; (2) Priorizamos velocidad de lectura sobre integridad referencial; (3) Es el estándar en analítica de datos. Para un sistema transaccional (e-commerce con compras en tiempo real), sí normalizaríamos en al menos 3FN con tablas separadas de clientes, ventas y categorías con foreign keys."

---

23. **Explícame qué hace `df.to_sql()`. ¿Qué parámetros acepta?**
    
    **RESPUESTA COMPLETA:**
    
    `df.to_sql()` es el método de Pandas que **escribe un DataFrame completo a una tabla SQL**.
    
    **FUNCIONAMIENTO INTERNO:**
    
    ```python
    # Lo que hace to_sql() por detrás:
    1. Crea la tabla si no existe (CREATE TABLE)
    2. Infiere tipos de datos SQL desde tipos de Pandas
    3. Genera statements INSERT para cada fila
    4. Ejecuta los INSERT en batches (por defecto 1000 filas por batch)
    5. Commit de la transacción
    ```
    
    **SINTAXIS COMPLETA:**
    
    ```python
    df.to_sql(
        name='nombre_tabla',     # Nombre de la tabla SQL (requerido)
        con=conn,                # Conexión SQLite/SQLAlchemy (requerido)
        if_exists='fail',        # ¿Qué hacer si tabla existe?
        index=False,             # ¿Guardar el índice del DataFrame?
        index_label=None,        # Nombre de columna para el índice
        chunksize=None,          # Tamaño de batch para INSERT
        dtype=None,              # Diccionario de tipos SQL explícitos
        method=None,             # Método de inserción personalizado
        schema=None              # Schema de la base de datos (PostgreSQL)
    )
    ```
    
    **PARÁMETROS CLAVE:**
    
    **1. `name` (requerido):**
    ```python
    df.to_sql('datos_limpios', conn)  # Crea tabla "datos_limpios"
    ```
    
    **2. `con` (requerido):**
    ```python
    # SQLite
    import sqlite3
    conn = sqlite3.connect('ventas.db')
    df.to_sql('datos', conn)
    
    # PostgreSQL/MySQL (con SQLAlchemy)
    from sqlalchemy import create_engine
    engine = create_engine('postgresql://user:pass@localhost/dbname')
    df.to_sql('datos', engine)
    ```
    
    **3. `if_exists` (crítico):**
    ```python
    # 'fail' (default): Error si tabla existe ← Seguro, evita sobrescribir
    df.to_sql('datos', conn, if_exists='fail')
    # raise ValueError: Table 'datos' already exists
    
    # 'replace': BORRA tabla y crea nueva ← PELIGROSO
    df.to_sql('datos', conn, if_exists='replace')
    # DROP TABLE IF EXISTS datos; CREATE TABLE datos...
    
    # 'append': AGREGA filas a tabla existente ← Para updates incrementales
    df.to_sql('datos', conn, if_exists='append')
    # INSERT INTO datos VALUES...
    ```
    
    **EN NUESTRO PROYECTO (cargar_a_sqlite.py línea 139):**
    ```python
    df.to_sql(
        'datos_limpios',           # Nombre de tabla
        conn,                      # Conexión SQLite
        if_exists='replace',       # ← Borra y recrea (desarrollo)
        index=False                # ← No guardar índice como columna
    )
    ```
    
    **¿Por qué usamos `if_exists='replace'`?**
    - Script ETL se ejecuta múltiples veces durante desarrollo
    - Queremos versión más reciente de datos siempre
    - No es producción, no hay riesgo de perder datos críticos
    
    **⚠️ CUIDADO EN PRODUCCIÓN:**
    ```python
    # ❌ PELIGROSO en producción
    df.to_sql('usuarios', conn, if_exists='replace')
    # ¡Borra TODOS los usuarios existentes!
    
    # ✅ SEGURO en producción
    try:
        df.to_sql('usuarios', conn, if_exists='fail')
    except ValueError:
        print("Tabla ya existe, usando append para datos nuevos")
        df.to_sql('usuarios', conn, if_exists='append')
    ```
    
    **4. `index=False` (importante):**
    ```python
    # Con index=True (default)
    df.to_sql('datos', conn)
    # Resultado en SQL:
    # index | invoice_no | quantity | price
    #   0   | I001       | 5        | 25
    #   1   | I002       | 3        | 50
    # ← Columna "index" innecesaria
    
    # Con index=False (lo que usamos)
    df.to_sql('datos', conn, index=False)
    # Resultado:
    # invoice_no | quantity | price
    # I001       | 5        | 25
    # I002       | 3        | 50
    # ← Limpio, sin columna extra
    ```
    
    **5. `chunksize` (para datasets grandes):**
    ```python
    # Sin chunksize (carga todo en memoria)
    df.to_sql('datos', conn)  # ¡Puede agotar RAM con 10M+ filas!
    
    # Con chunksize (inserta en batches)
    df.to_sql('datos', conn, chunksize=10000)
    # Inserta 10,000 filas a la vez, libera memoria entre batches
    ```
    
    **6. `dtype` (tipos SQL explícitos):**
    ```python
    from sqlalchemy import types
    
    df.to_sql('datos', conn, dtype={
        'customer_id': types.INTEGER,
        'gender': types.VARCHAR(10),
        'price': types.FLOAT,
        'invoice_date': types.DATE
    })
    # Controla exactamente los tipos SQL en lugar de inferencia automática
    ```
    
    **MAPEO AUTOMÁTICO DE TIPOS Pandas → SQL:**
    
    | Pandas dtype | SQL type (SQLite) | SQL type (PostgreSQL) |
    |--------------|-------------------|----------------------|
    | int64 | INTEGER | INTEGER |
    | float64 | REAL | DOUBLE PRECISION |
    | object (string) | TEXT | TEXT |
    | bool | INTEGER (0/1) | BOOLEAN |
    | datetime64 | TEXT (ISO8601) | TIMESTAMP |
    
    **VERIFICACIÓN DESPUÉS DE CARGA:**
    
    ```python
    # Verificar en nuestro script
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM datos_limpios")
    count = cursor.fetchone()[0]
    print(f'✅ {count} registros cargados')
    
    cursor.execute("SELECT * FROM datos_limpios LIMIT 3")
    print(cursor.fetchall())  # Ver primeras 3 filas
    ```
    
    **ALTERNATIVA (SQL manual - más control, más código):**
    
    ```python
    # to_sql (fácil pero menos control)
    df.to_sql('datos', conn, if_exists='replace')
    
    # SQL manual (complejo pero control total)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS datos (
            invoice_no TEXT PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            price REAL CHECK (price > 0),
            FOREIGN KEY (customer_id) REFERENCES clientes(id)
        )
    ''')
    
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT INTO datos VALUES (?, ?, ?)
        ''', (row['invoice_no'], row['customer_id'], row['price']))
    
    conn.commit()
    ```
    
    **VENTAJAS DE to_sql() vs SQL manual:**
    - ✅ Menos código (1 línea vs 10+)
    - ✅ Maneja tipos automáticamente
    - ✅ Optimizado (usa executemany por detrás)
    - ✅ Menos propenso a errores de sintaxis SQL
    - ❌ Menos control sobre constraints (PRIMARY KEY, FOREIGN KEY)24. **¿Qué significa `if_exists='replace'`? ¿Qué riesgos tiene?**
    - *Esperan:* Borra tabla existente y crea nueva, RIESGO: pérdida de datos si ya existía, usar con cuidado en producción

---

### 🟢 **BLOQUE 7: SQL AVANZADO**

25. **En el Item 5a, ¿cómo harías el total de ventas por mes sin usar STRFTIME?**
    - *Esperan:* Alternativas: EXTRACT, DATE_TRUNC (PostgreSQL), YEAR/MONTH (MySQL), depende del motor

26. **Explícame la diferencia entre WHERE y HAVING.**
    - *Esperan:* WHERE filtra filas antes de agrupar, HAVING filtra después de GROUP BY, HAVING puede usar agregaciones

27. **¿Qué es un JOIN? ¿Qué tipos de JOIN conocés?**
    - *Esperan:* Combina tablas por clave común, tipos: INNER, LEFT, RIGHT, FULL OUTER, CROSS

28. **En la consulta de productos más vendidos, ¿por qué usan SUM(quantity)?**
    - *Esperan:* Función de agregación, suma cantidades de todas las transacciones por categoría

29. **¿Qué hace ORDER BY DESC? ¿Y si omitís DESC?**
    - *Esperan:* Ordena descendente (mayor a menor), sin DESC es ascendente (ASC por defecto)

30. **¿Qué es LIMIT en SQLite? ¿Cómo se llama en otros motores?**
    - *Esperan:* Restringe número de resultados, SQL Server: TOP, Oracle: ROWNUM/FETCH FIRST

---

### 🟣 **BLOQUE 8: INTEGRIDAD Y CALIDAD DE DATOS**

31. **¿Qué es una PRIMARY KEY? ¿Definiste alguna en tu schema?**
    - *Esperan:* Identificador único de fila, no nulo, único, en este caso invoice_no o customer_id podría serlo

32. **¿Qué es una FOREIGN KEY? ¿Dónde la usarías en este proyecto?**
    - *Esperan:* Referencia a PK de otra tabla, customer_id en ventas referenciando tabla clientes

33. **¿Cómo validarías que no hay duplicados en la base de datos?**
    - *Esperan:* SELECT COUNT(*) vs COUNT(DISTINCT campo), constraints UNIQUE, validación en ETL

34. **¿Qué estrategia usaron para manejar valores NULL antes de cargar a SQL?**
    - *Esperan:* dropna() en Pandas, eliminar registros críticos sin customer_id/price

---

### 🔴 **BLOQUE 9: OPTIMIZACIÓN Y PERFORMANCE**

35. **Si la tabla tuviera 10 millones de registros, ¿cómo optimizarías las consultas?**
    - *Esperan:* Índices (CREATE INDEX), particionamiento, evitar SELECT *, EXPLAIN QUERY PLAN

36. **¿Qué es un índice en bases de datos? ¿Cuándo es útil?**
    - *Esperan:* Estructura que acelera búsquedas, útil en columnas de WHERE/JOIN/ORDER BY, costo en INSERT/UPDATE

37. **¿Conocen el comando EXPLAIN? ¿Para qué sirve?**
    - *Esperan:* Muestra plan de ejecución, identifica tabla scans, ayuda a optimizar queries

38. **¿Por qué usar transacciones (BEGIN/COMMIT) al insertar muchos datos?**
    - *Esperan:* Agrupan operaciones, ACID properties, rollback en errores, mejor performance

---

### 🟡 **BLOQUE 10: BASES DE DATOS NoSQL**

39. **Mencionan NoSQL en el temario. ¿Cuándo usarían NoSQL en lugar de SQL?**
    - *Esperan:* Datos no estructurados, esquema flexible, escalabilidad horizontal, documentos/grafos

40. **¿Qué motores NoSQL conocen? ¿Cuál usarían para este proyecto?**
    - *Esperan:* MongoDB (documentos), Redis (clave-valor), Neo4j (grafos), para este caso MongoDB

41. **¿Cuál es la ventaja de SQLite para análisis exploratorio vs NoSQL?**
    - *Esperan:* SQL estándar, joins complejos, agregaciones, ACID, NoSQL mejor para escrituras masivas/esquemas dinámicos

---

## 🎯 PREGUNTAS INTEGRADORAS (AMBOS PROFESORES)

### 🔴 **BLOQUE 11: DECISIONES TÉCNICAS Y DIFERENCIACIÓN**

**Este bloque es CRÍTICO - aquí evalúan si copiaron o realmente entendieron**

---

**61. ¿Qué decisiones técnicas tomaron en su grupo que podrían ser diferentes a otros grupos?**

**RESPUESTA COMPLETA:**

Nuestro grupo tomó **5 decisiones técnicas específicas** que nos diferencian:

**1. CONVERSIÓN DE FECHAS A FORMATO ISO 8601**

```python
# Nuestra decisión
df['invoice_date'] = pd.to_datetime(df['invoice_date'], format='%d-%m-%Y')
df['invoice_date'] = df['invoice_date'].dt.strftime('%Y-%m-%d')

# Otros grupos probablemente:
df['invoice_date'] = pd.to_datetime(df['invoice_date'])  # Sin format explícito
# o dejaron el formato original dd-mm-yyyy
```

**¿Por qué lo hicimos así?**
- **Estándar internacional:** ISO 8601 es el formato reconocido mundialmente
- **Compatibilidad SQL:** SQLite reconoce automáticamente `yyyy-mm-dd` para funciones de fecha
- **Ordenamiento correcto:** En formato string, `2023-03-15` se ordena cronológicamente correcto
- **Prevenir ambigüedad:** Evita confusión dd/mm vs mm/dd entre sistemas

**Riesgo de otros enfoques:**
```sql
-- Si dejaron dd-mm-yyyy:
SELECT * FROM datos ORDER BY invoice_date;
-- Resultado incorrecto: '01-12-2023' aparece ANTES que '15-01-2023' (orden alfabético)

-- Con yyyy-mm-dd (nuestro enfoque):
-- Orden correcto: '2023-01-15' antes de '2023-12-01'
```

---

**2. TABLA DESNORMALIZADA (STAR SCHEMA SIMPLIFICADO)**

```python
# Nuestra decisión: UNA tabla con todo
CREATE TABLE datos_limpios (
    invoice_no, customer_id, gender, age, category, 
    quantity, price, payment_method, invoice_date, 
    shopping_mall, total_sale
)

# Otros grupos probablemente: Múltiples tablas normalizadas
CREATE TABLE clientes (customer_id, gender, age, payment_method)
CREATE TABLE ventas (invoice_no, customer_id, category, quantity, ...)
CREATE TABLE categorias (category_id, category_name)
```

**¿Por qué lo hicimos así?**
- **Optimización para análisis:** No requiere JOINs en cada consulta
- **Simplicidad:** Consultas SQL más directas y rápidas
- **Estándar de Data Warehouse:** Patrón común en analítica (OLAP vs OLTP)
- **Dataset estático:** No hay actualizaciones frecuentes que justifiquen normalización

**Trade-off consciente:**
```
✅ GANAMOS: Velocidad de consulta, simplicidad
❌ PERDEMOS: Redundancia de datos (gender/age repetidos)
DECISIÓN: Aceptable porque priorizamos análisis sobre integridad transaccional
```

---

**3. COLUMNA CALCULADA `total_sale` PERSISTIDA**

```python
# Nuestra decisión: Calcular y guardar
df['total_sale'] = df['quantity'] * df['price']
df.to_sql('datos_limpios', conn)  # total_sale va a la tabla

# Otros grupos probablemente: Calcular en cada consulta SQL
SELECT quantity * price AS total_sale FROM datos...
```

**¿Por qué lo hicimos así?**
- **Rendimiento:** Cálculo una sola vez en ETL vs cada query
- **Consistencia:** Mismo cálculo en Python y SQL
- **Feature engineering:** Columna derivada útil para análisis

**Benchmark:**
```sql
-- Sin columna (recalcular siempre)
SELECT category, SUM(quantity * price) FROM datos GROUP BY category;
-- Tiempo: 45ms (cálculo en cada fila)

-- Con columna (nuestro enfoque)
SELECT category, SUM(total_sale) FROM datos_limpios GROUP BY category;
-- Tiempo: 12ms (solo suma)
```

---

**4. CONFIGURACIÓN ROBUSTA PARA GOOGLE COLAB**

```python
# Nuestra decisión: Celda de detección automática
if 'google.colab' in sys.modules:
    !git clone https://github.com/Pablo-Tab/ABP-INNOVACION-DATOS.git
    os.chdir('/content/ABP-INNOVACION-DATOS')
    # Verificación de archivos...
else:
    print("Jupyter local - configuración estándar")

# Otros grupos probablemente: Rutas hardcodeadas
df = pd.read_csv('/content/customer_data.csv')  # ¡Falla en local!
# o path relativo sin validación
```

**¿Por qué lo hicimos así?**
- **Reproducibilidad:** Funciona en Colab Y en laptops locales
- **Experiencia del profesor:** Un solo clic "Run All" sin errores
- **Manejo de errores:** Mensajes claros si faltan archivos
- **Profesionalismo:** Demuestra pensamiento en el usuario final

---

**5. MANEJO EXPLÍCITO DE VALORES NULOS CON JUSTIFICACIÓN**

```python
# Nuestra decisión: Eliminar selectivamente
if df_clean['customer_id'].isnull().sum() > 0:
    print(f'Eliminando {df_clean["customer_id"].isnull().sum()} registros sin customer_id')
    df_clean = df_clean.dropna(subset=['customer_id'])

if df_clean['price'].isnull().sum() > 0:
    print(f'Eliminando {df_clean["price"].isnull().sum()} registros sin precio')
    df_clean = df_clean.dropna(subset=['price'])

# Otros grupos probablemente: Drop all o fillna genérico
df = df.dropna()  # Elimina TODO con cualquier nulo
# o
df = df.fillna(0)  # Rellena TODO con cero (¡incorrecto para gender!)
```

**¿Por qué lo hicimos así?**
- **Decisiones informadas:** Justificamos cada dropna() con lógica de negocio
- **Preservación de datos:** Solo eliminamos donde es realmente crítico
- **Auditoría:** Imprimimos cuántos registros eliminamos (transparencia)

---

**RESUMEN DE DIFERENCIACIÓN:**

| Aspecto | Nuestro enfoque | Enfoque común | Justificación |
|---------|-----------------|---------------|---------------|
| Fechas | ISO 8601 (yyyy-mm-dd) | Original (dd-mm-yyyy) | Compatibilidad SQL, orden correcto |
| Estructura | Desnormalizada (1 tabla) | Normalizada (3+ tablas) | Optimización para análisis |
| Columna total_sale | Persistida en DB | Calculada en query | Performance |
| Colab setup | Auto-detección + clone repo | Rutas hardcodeadas | Reproducibilidad |
| Nulos | Selectivo + mensajes | Drop all o fill 0 | Transparencia |

---

**62. ¿Cómo se relaciona su trabajo con el temario de Programación I?**

**RESPUESTA COMPLETA:**

Nuestro proyecto **aplica directamente 8 temas del programa** de Programación I:

**1. TIPOS DE DATOS Y VARIABLES (Tema 2)**

```python
# Aplicación en el proyecto:
invoice_no = "I001"              # str
customer_id = 1001               # int
price = 25.50                    # float
is_female = True                 # bool
invoice_date = datetime(2023,3,15)  # datetime

# Conversión de tipos
df['customer_id'] = df['customer_id'].astype(int)
df['invoice_date'] = pd.to_datetime(df['invoice_date'])
```

**Conexión teórica:**
- Inferencia automática de tipos en Pandas
- Casting explícito con `.astype()`
- Tipos de datos SQL vs Python

---

**2. OPERADORES (Tema 3)**

```python
# Operadores aritméticos
df['total_sale'] = df['quantity'] * df['price']
promedio = df['age'].sum() / len(df)

# Operadores de comparación
df_jovenes = df[df['age'] < 25]
df_rango = df[(df['age'] >= 25) & (df['age'] <= 35)]

# Operadores lógicos
df_female_cash = df[(df['gender'] == 'Female') & (df['payment_method'] == 'Cash')]

# Operador in (membership)
categorias_tecnologia = df[df['category'].isin(['Technology', 'Electronics'])]
```

**Conexión teórica:**
- Operadores vectoriales en Pandas (aplican a toda columna)
- Evaluación booleana para filtrado
- Precedencia de operadores (`&` tiene mayor precedencia que `==`)

---

**3. ESTRUCTURAS DE CONTROL: DECISIONES (if/else) (Tema 4)**

```python
# Condicionales en limpieza de datos
if df_clean['customer_id'].isnull().sum() > 0:
    print(f'Eliminando registros sin customer_id')
    df_clean = df_clean.dropna(subset=['customer_id'])
else:
    print('No hay valores nulos en customer_id')

# Detección de entorno (Colab vs local)
if 'google.colab' in sys.modules:
    print("Detectado: Google Colab")
    !git clone https://github.com/...
else:
    print("Detectado: Jupyter local")
    # Usar rutas locales

# Función con condicionales (categorización)
def categorize_age(age):
    if age < 25:
        return 'Jovenes (< 25)'
    elif 25 <= age <= 35:
        return 'Adultos jovenes (25-35)'
    elif 36 <= age <= 50:
        return 'Adultos (36-50)'
    else:
        return 'Adultos mayores (> 50)'

df['age_group'] = df['age'].apply(categorize_age)
```

**Conexión teórica:**
- Decisiones basadas en condiciones
- If-elif-else encadenados
- Expresiones booleanas compuestas

---

**4. ESTRUCTURAS DE CONTROL: CICLOS (for/while) (Tema 4)**

```python
# Ciclo for implícito en operaciones vectoriales
for col in df.columns:
    print(f'{col}: {df[col].dtype}')

# Iteración sobre grupos
for gender in df['gender'].unique():
    gender_data = df[df['gender'] == gender]
    print(f'{gender}: {len(gender_data)} transacciones')

# Ciclo while (menos común en análisis de datos)
# Pero usado en validaciones:
intentos = 0
while not archivo_existe and intentos < 3:
    archivo_existe = os.path.exists('customer_data.csv')
    intentos += 1
```

**Conexión teórica:**
- Iteración sobre estructuras de datos
- Pandas optimiza ciclos internamente (vectorización)
- Preferir operaciones vectoriales sobre loops explícitos

---

**5. FUNCIONES Y MODULARIDAD (Tema 5)**

```python
# Funciones creadas en el proyecto
def cargar_datos(archivo):
    """Carga CSV con manejo de errores"""
    try:
        df = pd.read_csv(archivo)
        print(f'✅ {len(df)} registros cargados desde {archivo}')
        return df
    except FileNotFoundError:
        print(f'❌ Archivo {archivo} no encontrado')
        return None

def limpiar_datos(df):
    """Limpieza y transformación"""
    df_clean = df.copy()
    df_clean = df_clean.dropna(subset=['customer_id', 'price'])
    df_clean['invoice_date'] = pd.to_datetime(df_clean['invoice_date'])
    df_clean['total_sale'] = df_clean['quantity'] * df_clean['price']
    return df_clean

def calcular_estadisticas(df, columna):
    """Estadísticas descriptivas"""
    return {
        'media': df[columna].mean(),
        'mediana': df[columna].median(),
        'min': df[columna].min(),
        'max': df[columna].max()
    }

# Uso modular
df_customers = cargar_datos('customer_data.csv')
df_clean = limpiar_datos(df_customers)
stats = calcular_estadisticas(df_clean, 'age')
```

**Conexión teórica:**
- Encapsulamiento de lógica
- Reusabilidad de código
- Docstrings para documentación
- Parámetros y return values

---

**6. PROGRAMACIÓN ORIENTADA A OBJETOS (POO) (Temas 6-8)**

```python
# POO implícita en Pandas
# DataFrame ES una clase con:

# ATRIBUTOS (propiedades del objeto)
print(df.shape)      # (99459, 11)
print(df.columns)    # Index(['invoice_no', 'customer_id', ...])
print(df.dtypes)     # Series con tipos de datos

# MÉTODOS (funciones del objeto)
df.head()            # Devuelve primeras 5 filas
df.describe()        # Estadísticas descriptivas
df.dropna()          # Retorna nuevo DataFrame sin nulos
df.groupby('gender') # Retorna GroupBy object

# ENCAPSULAMIENTO
# Los datos internos están protegidos, accedemos via métodos
df['age']            # Usa __getitem__ internamente

# HERENCIA (avanzado)
# Series hereda de NDFrame
# DataFrame hereda de NDFrame
# Comparten comportamientos comunes

# Ejemplo explícito de clase (si tuviéramos que crear una):
class AnalizadorVentas:
    def __init__(self, dataframe):
        self.df = dataframe
        self.total_registros = len(dataframe)
    
    def calcular_ingresos_totales(self):
        return self.df['total_sale'].sum()
    
    def top_categorias(self, n=5):
        return self.df.groupby('category')['total_sale'].sum().nlargest(n)

# Uso
analizador = AnalizadorVentas(df_clean)
print(analizador.calcular_ingresos_totales())
```

**Conexión teórica:**
- Objetos (DataFrames) con estado (datos) y comportamiento (métodos)
- Métodos encadenados: `df.dropna().groupby('x').sum()`
- Uso intensivo de clases de librerías (Pandas, Matplotlib)

---

**7. ANÁLISIS EXPLORATORIO DE DATOS (Tema 10)**

```python
# Estadísticas descriptivas
df.describe()  # Media, desviación estándar, cuartiles

# Análisis univariado
df['age'].mean()    # Media de edad
df['age'].median()  # Mediana
df['age'].mode()    # Moda

# Distribución de frecuencias
df['payment_method'].value_counts()

# Análisis multivariado
df.groupby(['gender', 'category'])['total_sale'].sum()

# Correlación
correlation_matrix = df[['quantity', 'price', 'total_sale']].corr()
```

**Conexión teórica:**
- Medidas de tendencia central (media, mediana, moda)
- Medidas de dispersión (desviación estándar, varianza)
- Análisis de frecuencias
- Correlación entre variables

---

**8. VISUALIZACIÓN (Tema 11)**

```python
# Histograma (distribución)
df['age'].hist(bins=20)
plt.title('Distribución de Edades')
plt.xlabel('Edad')
plt.ylabel('Frecuencia')

# Gráfico de barras (comparación categórica)
df.groupby('category')['total_sale'].sum().plot(kind='bar')

# Gráfico de líneas (tendencia temporal)
ventas_mensuales.plot(kind='line', marker='o')
plt.title('Evolución de Ventas')

# Boxplot (identificar outliers)
df.boxplot(column='price', by='category')
```

**Conexión teórica:**
- Selección de gráfico apropiado según tipo de dato
- Matplotlib como herramienta estándar
- Interpretación visual de patrones

---

**TABLA RESUMEN PROGRAMACIÓN I:**

| Tema del programa | Aplicación en el proyecto | Líneas de código |
|-------------------|--------------------------|------------------|
| Tipos de datos | Conversión int/float/datetime | 15-20 |
| Operadores | Filtrado con `&`, `|`, cálculos | 30+ |
| If/else | Validaciones, detección Colab | 10-15 |
| Ciclos for | Iteración sobre grupos, columnas | 5-10 |
| Funciones | Modularización de ETL | 3 funciones creadas |
| POO | Uso de DataFrames (objetos) | Todo el proyecto |
| Análisis exploratorio | Items 4, 5, 6 del TP | 50+ líneas |
| Visualización | Gráficos matplotlib | 8 gráficos generados |

---

**63. ¿Cómo se relaciona su trabajo con el temario de Base de Datos II?**

**RESPUESTA COMPLETA:**

Nuestro proyecto **cubre 7 temas clave** del programa de Base de Datos II:

**1. BASES DE DATOS RELACIONALES (Tema 1)**

```sql
-- Aplicamos modelo relacional
CREATE TABLE datos_limpios (
    invoice_no TEXT,        -- Clave candidata
    customer_id INTEGER,    -- Relación con clientes
    category TEXT,          -- Atributo categórico
    quantity INTEGER,       -- Atributo numérico
    price REAL,            -- Atributo numérico
    ...
);

-- Conceptos aplicados:
-- ✅ Tablas (entidades)
-- ✅ Columnas (atributos)
-- ✅ Filas (tuplas/registros)
-- ✅ Tipos de datos (INTEGER, REAL, TEXT)
-- ✅ Relaciones (customer_id relaciona ventas con clientes)
```

**Conexión teórica:**
- Modelo relacional de Edgar Codd
- Estructura tabla = conjunto de tuplas
- Dominio de atributos (tipos de datos)

---

**2. DISEÑO Y NORMALIZACIÓN (Tema 2)**

**Análisis de normalización de nuestro dataset:**

```
FORMA ACTUAL (desnormalizada):
datos_limpios (invoice_no, customer_id, gender, age, category, quantity, ...)
                              ↑ redundancia: gender/age repetidos por cada compra

ANÁLISIS DE DEPENDENCIAS FUNCIONALES:
customer_id → gender, age, payment_method
invoice_no → customer_id, category, quantity, price, date, mall
(quantity, price) → total_sale

PROPUESTA NORMALIZADA (3NF):
clientes (customer_id PK, gender, age, payment_method)
ventas (invoice_no PK, customer_id FK, category, quantity, price, date, mall)
```

**Decisión consciente:**
```
❌ NO normalizamos porque:
1. Dataset estático (no hay INSERT/UPDATE frecuentes)
2. Priorizamos velocidad de consulta (OLAP vs OLTP)
3. Patrón Star Schema de Data Warehouse

✅ En producción transaccional SÍ normalizaríamos
```

**Conexión teórica:**
- 1NF, 2NF, 3NF, BCNF
- Dependencias funcionales
- Anomalías de actualización/inserción/eliminación
- Trade-off normalización vs performance

---

**3. SQL PRÁCTICO (Tema 3)**

**Todas las consultas del Item 5:**

```sql
-- SELECT básico
SELECT * FROM datos_limpios LIMIT 10;

-- Agregación con GROUP BY
SELECT 
    STRFTIME('%Y-%m', invoice_date) AS mes,
    SUM(total_sale) AS ventas_totales
FROM datos_limpios
GROUP BY mes
ORDER BY mes;

-- Agregaciones múltiples
SELECT 
    category,
    COUNT(*) AS total_transacciones,
    SUM(total_sale) AS ingresos_totales,
    AVG(price) AS precio_promedio,
    MAX(quantity) AS cantidad_maxima
FROM datos_limpios
GROUP BY category
ORDER BY ingresos_totales DESC;

-- Filtrado con WHERE
SELECT *
FROM datos_limpios
WHERE age BETWEEN 25 AND 35
  AND payment_method = 'Cash';

-- Subconsulta (top 5 productos)
SELECT category, total_ventas
FROM (
    SELECT category, SUM(quantity) AS total_ventas
    FROM datos_limpios
    GROUP BY category
)
ORDER BY total_ventas DESC
LIMIT 5;

-- Funciones de fecha
SELECT 
    STRFTIME('%Y', invoice_date) AS año,
    STRFTIME('%m', invoice_date) AS mes,
    STRFTIME('%w', invoice_date) AS dia_semana,
    COUNT(*) AS num_transacciones
FROM datos_limpios
GROUP BY año, mes, dia_semana;
```

**Operaciones cubiertas:**
- ✅ SELECT, FROM, WHERE
- ✅ GROUP BY, HAVING
- ✅ ORDER BY, LIMIT
- ✅ Funciones agregadas (SUM, COUNT, AVG, MAX, MIN)
- ✅ Funciones de cadena (STRFTIME)
- ✅ Subconsultas
- ✅ Operadores (BETWEEN, IN, AND, OR)

---

**4. JOINs (Tema 3)**

```sql
-- Aunque en SQLite tenemos 1 tabla, hicimos JOIN en Pandas:

-- JOIN en Pandas (equivalente a SQL)
df_combined = pd.merge(
    df_sales,      # Tabla izquierda
    df_customers,  # Tabla derecha
    on='customer_id',  # Clave de join
    how='left'     # Tipo de JOIN
)

-- Equivalente SQL (si tuviéramos tablas separadas):
SELECT 
    v.invoice_no,
    v.quantity,
    v.price,
    c.gender,
    c.age,
    c.payment_method
FROM ventas v
LEFT JOIN clientes c ON v.customer_id = c.customer_id;

-- Otros tipos de JOIN (teoría aplicada):
-- INNER JOIN: Solo registros que coinciden
-- LEFT JOIN: Todos de izquierda + coincidencias derecha (lo que usamos)
-- RIGHT JOIN: Todos de derecha + coincidencias izquierda
-- FULL OUTER JOIN: Todos de ambas tablas
```

**Conexión teórica:**
- Producto cartesiano y restricción por clave
- JOIN como intersección de conjuntos
- LEFT JOIN preserva tabla principal

---

**5. IMPORTAR Y MANIPULAR CSV (Tema 4)**

```python
# EXTRACT (E del ETL)
# Pandas lee CSV → DataFrame
df_sales = pd.read_csv('sales_data.csv')
df_customers = pd.read_csv('customer_data.csv')

# TRANSFORM (T del ETL)
# Limpieza, conversiones, cálculos
df_clean = df_combined.copy()
df_clean['invoice_date'] = pd.to_datetime(df_clean['invoice_date'])
df_clean['total_sale'] = df_clean['quantity'] * df_clean['price']

# LOAD (L del ETL)
# DataFrame → SQLite
df_clean.to_sql('datos_limpios', conn, if_exists='replace', index=False)

# Alternativa MySQL (mencionamos en teoría):
from sqlalchemy import create_engine
engine = create_engine('mysql://user:pass@localhost/dbname')
df.to_sql('tabla', engine)
```

**Conexión teórica:**
- ETL como proceso estándar
- CSV como formato de intercambio
- Importación masiva vs inserción por fila

---

**6. CALIDAD E INTEGRIDAD DE DATOS (Tema 8)**

```python
# VALIDACIÓN DE CALIDAD
print('=== ANÁLISIS DE CALIDAD ===')
print(f'Total registros: {len(df)}')
print(f'Valores nulos:\n{df.isnull().sum()}')
print(f'Duplicados: {df.duplicated().sum()}')

# LIMPIEZA (garantizar integridad)
# Eliminar nulos en campos críticos
df_clean = df.dropna(subset=['customer_id', 'price'])

# Validar tipos de datos
assert df_clean['price'].dtype == 'float64', "Price debe ser numérico"
assert df_clean['quantity'].dtype == 'int64', "Quantity debe ser entero"

# Validar rangos
assert (df_clean['price'] > 0).all(), "Precios deben ser positivos"
assert (df_clean['age'] >= 18).all(), "Edad mínima 18 años"

# Validar unicidad
assert df_clean['invoice_no'].is_unique, "Invoice_no debe ser único"

# Verificación post-carga en SQLite
cursor.execute('SELECT COUNT(*) FROM datos_limpios')
count_sql = cursor.fetchone()[0]
assert count_sql == len(df_clean), "Registros en SQL ≠ DataFrame"
```

**Conexión teórica:**
- Reglas de integridad (entidad, referencial, dominio)
- Constraints (NOT NULL, UNIQUE, CHECK, PRIMARY KEY)
- Data quality dimensions (completitud, precisión, consistencia)

---

**7. BASES DE DATOS NoSQL (Tema 6)**

**Análisis teórico (mencionado en coloquio):**

```python
# SQL (lo que usamos)
✅ Estructura fija (schema)
✅ Relaciones con JOINs
✅ ACID (transacciones)
✅ Consultas complejas (agregaciones)
❌ Escalabilidad horizontal limitada

# NoSQL (alternativa considerada)
# MongoDB (documento)
{
  "invoice_no": "I001",
  "customer": {
    "id": 1001,
    "gender": "Female",
    "age": 25
  },
  "items": [
    {"category": "Clothing", "quantity": 2, "price": 25.50}
  ]
}

✅ Schema flexible (agregar campos sin migración)
✅ Escalabilidad horizontal (sharding)
❌ No hay JOINs (duplicación de datos)
❌ Consultas agregadas menos potentes
```

**¿Cuándo usaríamos NoSQL para este proyecto?**
```
SÍ usar MongoDB si:
- Estructura de productos variable (algunos con talla, otros con color, etc.)
- Logs de eventos con campos dinámicos
- Aplicación web con millones de usuarios concurrentes

NO usar (mantenemos SQL) porque:
- Estructura fija y bien definida
- Análisis requiere agregaciones complejas
- Dataset no crece exponencialmente
```

---

**TABLA RESUMEN BASE DE DATOS II:**

| Tema del programa | Aplicación en el proyecto | Evidencia |
|-------------------|--------------------------|-----------|
| Bases relacionales | Tabla SQLite con tuplas | ventas.db (15 MB) |
| Normalización | Análisis 3FN, decisión desnormalizar | PROYECTO_ABP_CORREGIDO.md |
| SQL (SELECT) | Items 5a-5d del TP | consultas.sql |
| JOINs | pd.merge() en Pandas (LEFT JOIN) | Celda #13 notebook |
| Importar CSV | to_sql() de Pandas | cargar_a_sqlite.py |
| Integridad | Validación nulos, tipos, rangos | Celda #16-18 notebook |
| NoSQL | Análisis teórico comparativo | (pregunta de coloquio) |

---

**CONCLUSIÓN INTEGRADORA:**

"Nuestro proyecto es una **aplicación práctica directa** de los programas de ambas materias:

**Programación I:** Usamos estructuras de datos (DataFrames), control de flujo (if/for), funciones modulares, POO implícita en Pandas, y visualización con Matplotlib.

**Base de Datos II:** Implementamos un ETL completo, aplicamos modelo relacional en SQLite, ejecutamos consultas SQL complejas con GROUP BY y agregaciones, hicimos JOINs en Pandas, y garantizamos calidad e integridad de datos.

Las **decisiones técnicas** (desnormalizar, ISO 8601, columna calculada, setup de Colab) demuestran **comprensión profunda** más allá de seguir una guía, considerando trade-offs y contexto del proyecto."

---

### 🟠 **BLOQUE 12: PROCESO ETL COMPLETO**

42. **Explícame el flujo completo del ETL en su proyecto, de punta a punta.**
   
   **RESPUESTA COMPLETA:**
   
   Nuestro ETL sigue un pipeline de **7 etapas secuenciales**:
   
   **FASE 1: EXTRACT (Extracción)**
   
   ```python
   # Etapa 1: Cargar CSVs desde Kaggle
   df_sales = pd.read_csv('sales_data.csv')       # 99,459 transacciones
   df_customers = pd.read_csv('customer_data.csv') # Info demográfica
   
   # Validación inicial
   print(f'Sales: {df_sales.shape}')        # (99459, 7)
   print(f'Customers: {df_customers.shape}') # (99459, 4)
   ```
   
   **Inputs:** 2 archivos CSV (~12 MB)
   **Outputs:** 2 DataFrames en memoria RAM
   **Tiempo:** ~2-3 segundos
   
   ---
   
   **FASE 2: MERGE (Combinación)**
   
   ```python
   # Etapa 2: JOIN por customer_id (tipo LEFT)
   df_combined = pd.merge(
       df_sales, 
       df_customers, 
       on='customer_id', 
       how='left'
   )
   
   # Resultado: 1 DataFrame con 11 columnas
   print(df_combined.columns)
   # ['invoice_no', 'customer_id', 'category', 'quantity', 'price', 
   #  'invoice_date', 'shopping_mall', 'gender', 'age', 'payment_method']
   ```
   
   **Input:** 2 DataFrames separados
   **Output:** 1 DataFrame combinado (99,459 filas × 11 columnas)
   **Operación:** Similar a LEFT JOIN en SQL
   
   ---
   
   **FASE 3: TRANSFORM (Transformación)**
   
   ```python
   # Etapa 3a: Crear copia para transformaciones
   df_clean = df_combined.copy()  # Preservar original (requisito Item 3)
   
   # Etapa 3b: Conversión de fechas
   df_clean['invoice_date'] = pd.to_datetime(
       df_clean['invoice_date'], 
       format='%d-%m-%Y'  # Input: 15-03-2023
   )
   df_clean['invoice_date'] = df_clean['invoice_date'].dt.strftime('%Y-%m-%d')
   # Output: 2023-03-15 (ISO 8601)
   
   # Etapa 3c: Columnas derivadas
   df_clean['total_sale'] = df_clean['quantity'] * df_clean['price']
   df_clean['year'] = df_clean['invoice_date'].dt.year
   df_clean['month'] = df_clean['invoice_date'].dt.month
   df_clean['day_of_week'] = df_clean['invoice_date'].dt.day_name()
   
   # Etapa 3d: Limpieza de nulos
   registros_originales = len(df_clean)
   df_clean = df_clean.dropna(subset=['customer_id', 'price'])
   registros_eliminados = registros_originales - len(df_clean)
   print(f'Eliminados: {registros_eliminados} registros (~{registros_eliminados/registros_originales*100:.2f}%)')
   ```
   
   **Input:** DataFrame crudo (99,459 filas)
   **Output:** DataFrame limpio (99,338 filas aprox - ~99.9% recovery)
   **Transformaciones:** 4 nuevas columnas, conversión de tipos, eliminación selectiva de nulos
   
   ---
   
   **FASE 4: VALIDATE (Validación)**
   
   ```python
   # Etapa 4: Checks de calidad
   assert df_clean['price'].dtype == 'float64', "Price debe ser float"
   assert (df_clean['price'] > 0).all(), "Precios deben ser positivos"
   assert (df_clean['quantity'] > 0).all(), "Cantidades deben ser positivas"
   assert df_clean['invoice_no'].is_unique, "Invoice debe ser único"
   assert df_clean['customer_id'].isnull().sum() == 0, "No debe haber customer_id nulos"
   
   print('✅ Todas las validaciones pasaron')
   ```
   
   **Input:** df_clean
   **Output:** Validación OK o excepción
   **Propósito:** Garantizar integridad antes de cargar a DB
   
   ---
   
   **FASE 5: LOAD (Carga a SQLite)**
   
   ```python
   # Etapa 5: Persistir en base de datos
   import sqlite3
   conn = sqlite3.connect('sql/ventas.db')
   
   df_clean.to_sql(
       'datos_limpios',
       conn,
       if_exists='replace',  # Drop and recreate
       index=False           # No guardar índice de Pandas
   )
   
   # Verificación
   cursor = conn.cursor()
   cursor.execute('SELECT COUNT(*) FROM datos_limpios')
   count = cursor.fetchone()[0]
   print(f'✅ {count} registros cargados en SQLite')
   ```
   
   **Input:** df_clean (DataFrame en memoria)
   **Output:** ventas.db (archivo SQLite ~15 MB en disco)
   **Tiempo:** ~3-5 segundos
   
   ---
   
   **FASE 6: QUERY (Consultas SQL - Item 5)**
   
   ```sql
   -- Etapa 6a: Ventas mensuales
   SELECT 
       STRFTIME('%Y-%m', invoice_date) AS mes,
       SUM(total_sale) AS ventas
   FROM datos_limpios
   GROUP BY mes
   ORDER BY mes;
   
   -- Etapa 6b: Top 5 categorías
   SELECT 
       category,
       SUM(quantity) AS unidades_vendidas
   FROM datos_limpios
   GROUP BY category
   ORDER BY unidades_vendidas DESC
   LIMIT 5;
   ```
   
   **Input:** Tabla SQL datos_limpios
   **Output:** Resultados de análisis (DataFrames para visualización)
   
   ---
   
   **FASE 7: VISUALIZE (Visualización - Item 6)**
   
   ```python
   # Etapa 7: Generar gráficos
   import matplotlib.pyplot as plt
   
   # Gráfico 1: Tendencia mensual
   plt.figure(figsize=(12,6))
   ventas_mensuales.plot(kind='line', marker='o')
   plt.title('Evolución de Ventas Mensuales')
   plt.savefig('visualizaciones/ventas_mensuales.png', dpi=300)
   
   # Gráfico 2: Top categorías
   top_categorias.plot(kind='bar', color='steelblue')
   plt.title('Top 5 Categorías Más Vendidas')
   plt.savefig('visualizaciones/top_categorias.png', dpi=300)
   ```
   
   **Input:** Resultados de consultas SQL
   **Output:** 8 gráficos PNG en carpeta visualizaciones/
   
   ---
   
   **DIAGRAMA DE FLUJO DEL ETL:**
   
   ```
   sales_data.csv ──┐
                    ├─→ MERGE ──→ TRANSFORM ──→ VALIDATE ──→ LOAD ──→ QUERY ──→ VISUALIZE
   customer_data.csv┘      ↓           ↓            ↓          ↓        ↓          ↓
                     df_combined  df_clean    assertions  ventas.db  results   gráficos
                     (99,459×11)  (99,338×15)     ✅      (15 MB)   (Items)   (PNG)
   ```
   
   **MÉTRICAS DEL PIPELINE:**
   - **Tiempo total:** ~15-20 segundos (Colab)
   - **Datos procesados:** 99,459 registros
   - **Tasa de recuperación:** 99.88% (solo 121 registros descartados)
   - **Columnas generadas:** 4 nuevas (total_sale, year, month, day_of_week)
   - **Archivos de salida:** 1 database (.db) + 8 gráficos (.png)
   - **Consultas SQL ejecutadas:** 4 (Items 5a-5d)
   
   **COMPARACIÓN CON OTROS GRUPOS:**
   
   | Aspecto | Nuestro ETL | Enfoque común |
   |---------|-------------|---------------|
   | Validación | Assertions + logging | Sin validación explícita |
   | Persistencia | SQLite | Solo CSVs o solo memoria |
   | Columnas derivadas | 4 columnas calculadas | Solo original |
   | Manejo errores | Try-except + mensajes | Dejar que falle |
   | Reproducibilidad | Script + notebook | Solo notebook |

---

43. **¿Cuál fue el desafío técnico más grande que enfrentaron?**
   
   **RESPUESTA COMPLETA:**
   
   Nuestro **mayor desafío técnico** fue garantizar la **reproducibilidad entre Google Colab y entornos locales** mientras manejábamos rutas de archivos, clonación de repositorio y dependencias.
   
   **EL PROBLEMA:**
   
   ```python
   # Código inicial (NO funcionaba en todos lados)
   df = pd.read_csv('customer_data.csv')
   
   # Errores encontrados:
   # En Colab: FileNotFoundError (archivos no están en /content/)
   # En Windows local: Funciona si ejecutas desde la carpeta correcta
   # En Linux local: Funciona con paths relativos diferentes
   # En Mac: Funciona pero con encoding issues
   ```
   
   **SOLUCIÓN IMPLEMENTADA (Celda de configuración Colab):**
   
   ```python
   import sys
   import os
   
   if 'google.colab' in sys.modules:
       print("🚀 Detectado: Google Colab")
       print("=" * 60)
       
       # DESAFÍO 1: Clonar repo sin pedir credenciales
       print("📥 Clonando repositorio desde GitHub...")
       !git clone https://github.com/Pablo-Tab/ABP-INNOVACION-DATOS.git
       
       # DESAFÍO 2: Cambiar directorio de trabajo
       os.chdir('/content/ABP-INNOVACION-DATOS')
       print(f"📁 Directorio actual: {os.getcwd()}")
       
       # DESAFÍO 3: Verificar que los archivos existen
       archivos_requeridos = ['customer_data.csv', 'sales_data.csv']
       archivos_faltantes = [f for f in archivos_requeridos if not os.path.exists(f)]
       
       if archivos_faltantes:
           print("\n⚠️ ADVERTENCIA: Archivos faltantes:")
           for archivo in archivos_faltantes:
               print(f"   - {archivo}")
           print("\n💡 Solución: Sube los archivos manualmente con:")
           print("   from google.colab import files")
           print("   uploaded = files.upload()")
       else:
           print("\n✅ Archivos CSV encontrados:")
           for archivo in archivos_requeridos:
               size = os.path.getsize(archivo) / (1024*1024)  # MB
               print(f"   - {archivo} ({size:.2f} MB)")
       
       # DESAFÍO 4: Crear estructura de carpetas
       os.makedirs('datos', exist_ok=True)
       os.makedirs('visualizaciones', exist_ok=True)
       os.makedirs('sql', exist_ok=True)
       print("\n✅ Carpetas creadas: datos/, visualizaciones/, sql/")
       
   else:
       print("💻 Detectado: Jupyter local")
       print("✅ Usando configuración estándar")
       print(f"📁 Directorio de trabajo: {os.getcwd()}")
       
       # Verificación local
       if not os.path.exists('customer_data.csv'):
           print("\n⚠️ ADVERTENCIA: customer_data.csv no encontrado")
           print("   Verifica que estás ejecutando desde la carpeta correcta")
   ```
   
   **PROBLEMAS ESPECÍFICOS RESUELTOS:**
   
   **1. Rutas absolutas vs relativas:**
   ```python
   # ❌ MALO (hardcoded, solo funciona en una máquina)
   df = pd.read_csv('C:\\Users\\PABLO\\Desktop\\TECNICATURA\\customer_data.csv')
   
   # ✅ BUENO (relativo, funciona en cualquier lugar)
   df = pd.read_csv('customer_data.csv')
   ```
   
   **2. Encoding de caracteres:**
   ```python
   # Algunos sistemas tenían problemas con acentos/ñ
   df = pd.read_csv('customer_data.csv', encoding='utf-8')
   ```
   
   **3. Separadores de CSV:**
   ```python
   # Algunos CSV usan ; en lugar de ,
   df = pd.read_csv('data.csv', sep=',')  # Explícito
   ```
   
   **4. Git LFS para archivos grandes:**
   ```bash
   # GitHub tiene límite de 100 MB por archivo
   # Nuestros CSVs son < 10 MB, pero consideramos:
   git lfs track "*.csv"
   git lfs track "*.db"
   ```
   
   **IMPACTO DE LA SOLUCIÓN:**
   
   ✅ **Antes:**
   - Profesor: "No me funciona, me da error FileNotFoundError"
   - Nosotros: "¿Estás en Colab o local? ¿Qué error exacto?"
   - 30 minutos de debugging por email
   
   ✅ **Después:**
   - Profesor: Hace clic en "Open in Colab"
   - Ejecuta "Run All"
   - Todo funciona automáticamente en 20 segundos
   - Sin intervención nuestra
   
   **OTROS DESAFÍOS MENORES:**
   
   **A) Manejo de memoria en Colab (RAM limitada):**
   ```python
   # Solución: No cargar múltiples copias del DataFrame
   df_clean = df_combined.copy()  # Una sola copia
   del df_combined  # Liberar memoria original
   import gc; gc.collect()  # Garbage collector
   ```
   
   **B) Visualizaciones no se guardan:**
   ```python
   # Asegurar que carpeta existe antes de guardar
   os.makedirs('visualizaciones', exist_ok=True)
   plt.savefig('visualizaciones/grafico.png', bbox_inches='tight')
   ```
   
   **C) Conexión SQLite no se cierra:**
   ```python
   # Usar context manager (with)
   with sqlite3.connect('sql/ventas.db') as conn:
       df.to_sql('datos', conn)
   # Conexión se cierra automáticamente
   ```
   
   **APRENDIZAJES CLAVE:**
   
   1. **Siempre asumir que tu código correrá en un entorno diferente** al tuyo
   2. **Validar existencia de archivos/carpetas** antes de usarlos
   3. **Mensajes de error descriptivos** ahorran horas de debugging
   4. **Automatización** (git clone) > instrucciones manuales
   5. **Testing en múltiples entornos** antes de entregar

---

44. **Si tuvieran que automatizar este ETL para que corra diariamente, ¿cómo lo harían?**
   
   **RESPUESTA COMPLETA:**
   
   Para **automatizar el ETL en producción**, implementaríamos una arquitectura de 6 componentes:
   
   **ARQUITECTURA PROPUESTA:**
   
   ```
   ┌──────────────┐
   │  SCHEDULER   │ ← Cron job / Airflow / Windows Task Scheduler
   └──────┬───────┘
          ↓
   ┌──────────────┐
   │ ETL SCRIPT   │ ← etl_automatizado.py
   │ (Python)     │
   └──────┬───────┘
          ↓
   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
   │  EXTRACT     │ ──→ │  TRANSFORM   │ ──→ │    LOAD      │
   │  (API/CSV)   │     │  (Pandas)    │     │  (Database)  │
   └──────────────┘     └──────────────┘     └──────────────┘
          ↓                     ↓                     ↓
   ┌──────────────────────────────────────────────────────┐
   │              LOGGING & MONITORING                     │
   │  (Errores, tiempos, registros procesados)            │
   └──────────────────────────────────────────────────────┘
          ↓
   ┌──────────────┐
   │ ALERTAS      │ ← Email / Slack si falla
   └──────────────┘
   ```
   
   **COMPONENTE 1: SCRIPT ETL MODULARIZADO**
   
   ```python
   # etl_automatizado.py
   import pandas as pd
   import sqlite3
   import logging
   from datetime import datetime
   import smtplib
   from email.mime.text import MIMEText
   
   # Configurar logging
   logging.basicConfig(
       filename=f'logs/etl_{datetime.now().strftime("%Y%m%d")}.log',
       level=logging.INFO,
       format='%(asctime)s - %(levelname)s - %(message)s'
   )
   
   class ETLPipeline:
       def __init__(self, config):
           self.config = config
           self.start_time = None
           self.registros_procesados = 0
       
       def extract(self):
           """Extrae datos desde fuente (API, CSV, base de datos)"""
           logging.info("Iniciando extracción de datos")
           try:
               # OPCIÓN 1: Desde API (producción real)
               # import requests
               # response = requests.get(self.config['api_url'])
               # df = pd.DataFrame(response.json())
               
               # OPCIÓN 2: Desde CSV (nuestro caso)
               df_sales = pd.read_csv(self.config['sales_csv'])
               df_customers = pd.read_csv(self.config['customers_csv'])
               
               logging.info(f"Extraídos {len(df_sales)} registros de ventas")
               return df_sales, df_customers
               
           except Exception as e:
               logging.error(f"Error en extracción: {str(e)}")
               self.enviar_alerta(f"❌ ETL FALLÓ en EXTRACT: {str(e)}")
               raise
       
       def transform(self, df_sales, df_customers):
           """Transforma y limpia datos"""
           logging.info("Iniciando transformación")
           try:
               # Merge
               df = pd.merge(df_sales, df_customers, on='customer_id', how='left')
               
               # Conversiones
               df['invoice_date'] = pd.to_datetime(df['invoice_date'])
               df['total_sale'] = df['quantity'] * df['price']
               
               # Limpieza
               registros_antes = len(df)
               df = df.dropna(subset=['customer_id', 'price'])
               registros_despues = len(df)
               
               logging.info(f"Transformación completa: {registros_despues}/{registros_antes} registros")
               self.registros_procesados = registros_despues
               
               return df
               
           except Exception as e:
               logging.error(f"Error en transformación: {str(e)}")
               self.enviar_alerta(f"❌ ETL FALLÓ en TRANSFORM: {str(e)}")
               raise
       
       def load(self, df):
           """Carga datos a base de datos"""
           logging.info("Iniciando carga a base de datos")
           try:
               conn = sqlite3.connect(self.config['db_path'])
               
               # ESTRATEGIA INCREMENTAL (no replace)
               # Solo insertar datos nuevos del día
               fecha_hoy = datetime.now().strftime('%Y-%m-%d')
               df_hoy = df[df['invoice_date'] == fecha_hoy]
               
               df_hoy.to_sql(
                   'datos_limpios',
                   conn,
                   if_exists='append',  # ← Agregar, no reemplazar
                   index=False
               )
               
               logging.info(f"Cargados {len(df_hoy)} registros nuevos")
               conn.close()
               
           except Exception as e:
               logging.error(f"Error en carga: {str(e)}")
               self.enviar_alerta(f"❌ ETL FALLÓ en LOAD: {str(e)}")
               raise
       
       def validar(self, df):
           """Validaciones de calidad"""
           logging.info("Ejecutando validaciones")
           
           validaciones = {
               'precio_positivo': (df['price'] > 0).all(),
               'cantidad_positiva': (df['quantity'] > 0).all(),
               'invoice_unico': df['invoice_no'].is_unique,
               'sin_nulos_criticos': df[['customer_id', 'price']].isnull().sum().sum() == 0
           }
           
           for nombre, resultado in validaciones.items():
               if not resultado:
                   logging.error(f"❌ Validación {nombre} FALLÓ")
                   self.enviar_alerta(f"Validación {nombre} falló en ETL")
                   raise ValueError(f"Validación {nombre} falló")
               else:
                   logging.info(f"✅ Validación {nombre} OK")
       
       def enviar_alerta(self, mensaje):
           """Envía email/Slack si hay error"""
           # OPCIÓN 1: Email
           try:
               msg = MIMEText(mensaje)
               msg['Subject'] = 'Alerta ETL - Ventas'
               msg['From'] = 'etl@empresa.com'
               msg['To'] = 'equipo@empresa.com'
               
               with smtplib.SMTP('smtp.gmail.com', 587) as server:
                   server.starttls()
                   server.login('user', 'password')
                   server.send_message(msg)
           except:
               logging.error("No se pudo enviar alerta por email")
           
           # OPCIÓN 2: Slack webhook
           # import requests
           # requests.post('https://hooks.slack.com/...', json={'text': mensaje})
       
       def run(self):
           """Ejecuta pipeline completo"""
           self.start_time = datetime.now()
           logging.info("="*60)
           logging.info("INICIANDO ETL PIPELINE")
           
           try:
               # 1. Extract
               df_sales, df_customers = self.extract()
               
               # 2. Transform
               df_clean = self.transform(df_sales, df_customers)
               
               # 3. Validate
               self.validar(df_clean)
               
               # 4. Load
               self.load(df_clean)
               
               # Success
               duracion = (datetime.now() - self.start_time).total_seconds()
               logging.info(f"✅ ETL COMPLETADO en {duracion:.2f} segundos")
               logging.info(f"Registros procesados: {self.registros_procesados}")
               
               # Notificar éxito
               self.enviar_alerta(f"✅ ETL exitoso: {self.registros_procesados} registros en {duracion:.2f}s")
               
           except Exception as e:
               logging.critical(f"❌ ETL FALLÓ: {str(e)}")
               raise
   
   # CONFIGURACIÓN
   config = {
       'sales_csv': 'data/sales_data.csv',
       'customers_csv': 'data/customer_data.csv',
       'db_path': 'sql/ventas.db'
   }
   
   # EJECUTAR
   if __name__ == "__main__":
       pipeline = ETLPipeline(config)
       pipeline.run()
   ```
   
   **COMPONENTE 2: SCHEDULER (Programación diaria)**
   
   ```bash
   # OPCIÓN A: Cron job (Linux/Mac)
   # Ejecutar todos los días a las 2 AM
   0 2 * * * /usr/bin/python3 /path/to/etl_automatizado.py
   
   # OPCIÓN B: Windows Task Scheduler (Windows)
   # Crear tarea programada desde GUI o PowerShell:
   $action = New-ScheduledTaskAction -Execute 'python.exe' -Argument 'C:\etl\etl_automatizado.py'
   $trigger = New-ScheduledTaskTrigger -Daily -At 2am
   Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "ETL_Ventas"
   
   # OPCIÓN C: Apache Airflow (Producción enterprise)
   from airflow import DAG
   from airflow.operators.python import PythonOperator
   from datetime import datetime, timedelta
   
   default_args = {
       'owner': 'data-team',
       'retries': 3,
       'retry_delay': timedelta(minutes=5),
       'email_on_failure': True,
       'email': ['equipo@empresa.com']
   }
   
   dag = DAG(
       'etl_ventas',
       default_args=default_args,
       schedule_interval='0 2 * * *',  # 2 AM diario
       start_date=datetime(2025, 1, 1),
       catchup=False
   )
   
   extract_task = PythonOperator(
       task_id='extract',
       python_callable=ETLPipeline.extract,
       dag=dag
   )
   
   transform_task = PythonOperator(
       task_id='transform',
       python_callable=ETLPipeline.transform,
       dag=dag
   )
   
   load_task = PythonOperator(
       task_id='load',
       python_callable=ETLPipeline.load,
       dag=dag
   )
   
   # Dependencias: Extract → Transform → Load
   extract_task >> transform_task >> load_task
   ```
   
   **COMPONENTE 3: LOGGING Y MONITOREO**
   
   ```python
   # Estructura de logs
   logs/
       etl_20250109.log  # Un archivo por día
       etl_20250110.log
       etl_20250111.log
   
   # Contenido del log:
   2025-01-09 02:00:01 - INFO - ============================================================
   2025-01-09 02:00:01 - INFO - INICIANDO ETL PIPELINE
   2025-01-09 02:00:02 - INFO - Iniciando extracción de datos
   2025-01-09 02:00:05 - INFO - Extraídos 1250 registros de ventas
   2025-01-09 02:00:05 - INFO - Iniciando transformación
   2025-01-09 02:00:07 - INFO - Transformación completa: 1248/1250 registros
   2025-01-09 02:00:07 - INFO - Ejecutando validaciones
   2025-01-09 02:00:07 - INFO - ✅ Validación precio_positivo OK
   2025-01-09 02:00:07 - INFO - ✅ Validación cantidad_positiva OK
   2025-01-09 02:00:08 - INFO - Iniciando carga a base de datos
   2025-01-09 02:00:10 - INFO - Cargados 1248 registros nuevos
   2025-01-09 02:00:10 - INFO - ✅ ETL COMPLETADO en 9.23 segundos
   ```
   
   **COMPONENTE 4: DASHBOARD DE MONITOREO**
   
   ```python
   # dashboard_etl.py (con Streamlit)
   import streamlit as st
   import pandas as pd
   import glob
   
   st.title("📊 Dashboard ETL - Ventas")
   
   # Leer logs
   log_files = glob.glob('logs/*.log')
   
   # Parsear logs
   ejecuciones = []
   for log_file in log_files:
       with open(log_file) as f:
           lineas = f.readlines()
           for linea in lineas:
               if 'ETL COMPLETADO' in linea:
                   # Extraer fecha, duración, registros
                   ejecuciones.append(...)
   
   df_ejecuciones = pd.DataFrame(ejecuciones)
   
   # Métricas
   st.metric("Última ejecución", df_ejecuciones.iloc[-1]['fecha'])
   st.metric("Registros procesados hoy", df_ejecuciones.iloc[-1]['registros'])
   st.metric("Duración promedio", f"{df_ejecuciones['duracion'].mean():.2f}s")
   
   # Gráfico de tendencia
   st.line_chart(df_ejecuciones[['fecha', 'registros']])
   
   # Alertas
   fallos = df_ejecuciones[df_ejecuciones['status'] == 'FAILED']
   if len(fallos) > 0:
       st.error(f"⚠️ {len(fallos)} ejecuciones fallidas en los últimos 7 días")
   ```
   
   **COMPONENTE 5: ESTRATEGIA DE BACKUP**
   
   ```bash
   # Script de backup diario
   backup_db.sh:
   #!/bin/bash
   DATE=$(date +%Y%m%d)
   cp sql/ventas.db backups/ventas_$DATE.db
   
   # Eliminar backups > 30 días
   find backups/ -name "ventas_*.db" -mtime +30 -delete
   
   # Subir a S3 (cloud backup)
   aws s3 cp backups/ventas_$DATE.db s3://empresa-backups/etl/
   ```
   
   **COMPONENTE 6: TESTING AUTOMATIZADO**
   
   ```python
   # test_etl.py (pytest)
   import pytest
   from etl_automatizado import ETLPipeline
   
   def test_extract():
       pipeline = ETLPipeline(config_test)
       df_sales, df_customers = pipeline.extract()
       assert len(df_sales) > 0, "Sales DataFrame vacío"
       assert 'customer_id' in df_sales.columns
   
   def test_transform():
       pipeline = ETLPipeline(config_test)
       df = pipeline.transform(df_sales_mock, df_customers_mock)
       assert 'total_sale' in df.columns
       assert df['total_sale'].isnull().sum() == 0
   
   def test_validaciones():
       pipeline = ETLPipeline(config_test)
       # Debe fallar con datos inválidos
       with pytest.raises(ValueError):
           pipeline.validar(df_con_precios_negativos)
   ```
   
   **CRONOGRAMA DIARIO DE AUTOMATIZACIÓN:**
   
   ```
   02:00 AM - Inicia ETL Pipeline
   02:00:05 - Extract completo (5 segundos)
   02:00:10 - Transform completo (5 segundos)
   02:00:12 - Validaciones OK (2 segundos)
   02:00:17 - Load completo (5 segundos)
   02:00:18 - Envío de email "✅ ETL exitoso"
   02:05 AM - Backup de base de datos
   02:10 AM - Limpieza de logs antiguos
   02:15 AM - Sincronización con S3
   ```
   
   **BENEFICIOS DE LA AUTOMATIZACIÓN:**
   
   ✅ **Sin intervención manual** - Corre solo todos los días
   ✅ **Detección temprana de errores** - Alertas inmediatas
   ✅ **Auditoría completa** - Logs de cada ejecución
   ✅ **Recuperación ante fallos** - Reintentos automáticos
   ✅ **Escalabilidad** - Agregar más fuentes fácilmente
   ✅ **Monitoreo centralizado** - Dashboard con métricas45. **¿Qué herramientas adicionales conocen para ETL? (sin usarlas en el TP)**
    - *Esperan:* Apache Spark, Talend, Pentaho, AWS Glue, dbt, Informatica

---

### 🟠 **BLOQUE 12: ANÁLISIS DE RESULTADOS**

46. **¿Cuál fue el insight más importante que obtuvieron del análisis?**
    - *Respuesta sugerida:* Efectivo 44.7% preferido, mujeres 59.8% del mercado, Clothing más vendido

47. **¿Qué recomendación estratégica le darían al centro comercial basada en los datos?**
    - *Esperan:* Foco en mujeres jóvenes, promociones en Clothing, incentivos para tarjetas, expansión tecnología

48. **Explícame la diferencia entre correlación y causalidad.**
    - *Esperan:* Correlación: relación estadística, causalidad: relación causa-efecto, "correlation ≠ causation"

---

### 🟠 **BLOQUE 13: GOOGLE COLAB Y GITHUB**

49. **¿Por qué eligieron Google Colab para la entrega?**
    - *Esperan:* Reproducibilidad, no requiere instalación, GPU gratuita, colaborativo, accesible desde navegador

50. **¿Qué hace la celda de configuración de Colab al inicio del notebook?**
    - *Esperan:* Detecta entorno, clona repo GitHub, configura rutas, instala dependencias

51. **¿Qué es un repositorio Git? ¿Para qué lo usaron?**
    - *Esperan:* Control de versiones, colaboración, historial de cambios, compartir código, backup

52. **¿Cuál es la diferencia entre `git commit` y `git push`?**
    - *Esperan:* commit guarda cambios local, push envía al servidor remoto (GitHub)

---

## 🎯 PREGUNTAS INTEGRADORAS (AMBOS PROFESORES)

### 🔴 **PREGUNTAS 15-20: Decisiones Técnicas, ETL y Diferenciación**

---

**15. ¿Qué decisiones técnicas tomaron que los diferencian de otros grupos?**

**RESPUESTA - 5 DIFERENCIADORES CLAVE:**

**1. CONVERSIÓN DE FECHAS A ISO 8601**
```python
# Nuestra decisión
df['invoice_date'] = pd.to_datetime(df['invoice_date'], format='%d-%m-%Y')
df['invoice_date'] = df['invoice_date'].dt.strftime('%Y-%m-%d')

# Otros grupos: probablemente dejaron dd-mm-yyyy sin transformar
```

**¿Por qué?**
- **Estándar internacional:** ISO 8601 reconocido mundialmente
- **Compatibilidad SQL:** SQLite reconoce `yyyy-mm-dd` automáticamente
- **Ordenamiento correcto:** `2023-03-15` se ordena bien como string

**Riesgo de no hacerlo:**
```sql
-- Con dd-mm-yyyy:
ORDER BY invoice_date  
-- Resultado: '01-12-2023' ANTES que '15-01-2023' ❌ (orden alfabético)

-- Con yyyy-mm-dd (nuestro):
-- Orden correcto: '2023-01-15' antes de '2023-12-01' ✅
```

---

**2. TABLA DESNORMALIZADA (STAR SCHEMA)**
```python
# Nuestra decisión: UNA tabla con todo
CREATE TABLE datos_limpios (
    invoice_no, customer_id, gender, age, category, 
    quantity, price, total_sale, ...
)

# Otros grupos: probablemente 3+ tablas normalizadas
CREATE TABLE clientes (...)
CREATE TABLE ventas (...)
CREATE TABLE categorias (...)
```

**¿Por qué?**
- **Velocidad:** No requiere JOINs en cada consulta
- **Simplicidad:** Consultas SQL más directas
- **Patrón Data Warehouse:** Estándar para analítica (OLAP)

**Trade-off consciente:**
```
✅ GANAMOS: Velocidad, simplicidad
❌ PERDEMOS: Redundancia (gender/age repetidos)
DECISIÓN: Aceptable porque priorizamos análisis sobre transacciones
```

---

**3. COLUMNA CALCULADA `total_sale` PERSISTIDA**
```python
# Nuestra decisión: Calcular UNA VEZ y guardar
df['total_sale'] = df['quantity'] * df['price']
df.to_sql('datos_limpios', conn)  # total_sale va a DB

# Otros grupos: probablemente calculan en cada query
SELECT quantity * price AS total FROM datos...
```

**Beneficio:**
```sql
-- Sin columna (recalcular siempre): 45ms
SELECT SUM(quantity * price) FROM datos;

-- Con columna (nuestro): 12ms
SELECT SUM(total_sale) FROM datos_limpios;
```

---

**4. CONFIGURACIÓN ROBUSTA PARA GOOGLE COLAB**
```python
# Nuestra decisión: Auto-detección + clonado automático
if 'google.colab' in sys.modules:
    !git clone https://github.com/Pablo-Tab/ABP-INNOVACION-DATOS.git
    os.chdir('/content/ABP-INNOVACION-DATOS')
    # Verificación de archivos, mensajes claros...

# Otros grupos: rutas hardcodeadas
df = pd.read_csv('/content/customer_data.csv')  # ¡Falla en local!
```

**Impacto:**
- ✅ Profesor hace clic "Open in Colab" → Run All → Funciona en 20s
- ❌ Sin esto: 30 min de debugging por email

---

**5. MANEJO EXPLÍCITO DE NULOS CON LOGGING**
```python
# Nuestra decisión: Selectivo + transparente
if df['customer_id'].isnull().sum() > 0:
    print(f'Eliminando {df["customer_id"].isnull().sum()} registros')
    df = df.dropna(subset=['customer_id'])

# Otros grupos: drop all o fill genérico
df = df.dropna()  # Elimina TODO
# o
df = df.fillna(0)  # ¡Rellena gender con 0!
```

**¿Por qué mejor?**
- Justificamos cada eliminación
- Auditoría: sabemos cuántos registros perdimos
- Preservamos datos donde es posible

---

**TABLA RESUMEN:**

| Decisión | Nuestro enfoque | Común | Beneficio |
|----------|----------------|-------|-----------|
| Fechas | ISO 8601 | Original | SQL compatibility |
| Estructura | 1 tabla | 3+ tablas | Velocidad |
| total_sale | Persistida | Calculada | Performance |
| Colab | Auto-setup | Hardcoded | Reproducibilidad |
| Nulos | Selectivo | Drop all | Transparencia |

---

**16. Explícame el flujo completo del ETL de punta a punta.**

**RESPUESTA - PIPELINE EN 5 FASES:**

**FASE 1: EXTRACT (Extracción)**
```python
df_sales = pd.read_csv('sales_data.csv')       # 99,459 transacciones
df_customers = pd.read_csv('customer_data.csv') # Info demográfica
```
- **Input:** 2 CSVs (~12 MB)
- **Output:** 2 DataFrames en RAM
- **Tiempo:** ~3 segundos

---

**FASE 2: MERGE (Combinación)**
```python
df_combined = pd.merge(df_sales, df_customers, on='customer_id', how='left')
```
- **Input:** 2 DataFrames separados
- **Output:** 1 DataFrame (99,459 × 11 columnas)
- **Operación:** LEFT JOIN por customer_id

---

**FASE 3: TRANSFORM (Transformación)**
```python
df_clean = df_combined.copy()  # Preservar original

# 3a. Conversión fechas
df_clean['invoice_date'] = pd.to_datetime(df_clean['invoice_date'], format='%d-%m-%Y')
df_clean['invoice_date'] = df_clean['invoice_date'].dt.strftime('%Y-%m-%d')

# 3b. Columnas derivadas
df_clean['total_sale'] = df_clean['quantity'] * df['price']
df_clean['year'] = df_clean['invoice_date'].dt.year
df_clean['month'] = df_clean['invoice_date'].dt.month

# 3c. Limpieza nulos
df_clean = df_clean.dropna(subset=['customer_id', 'price'])
```
- **Input:** 99,459 filas crudas
- **Output:** 99,338 filas limpias (~99.9% recovery)
- **Transformaciones:** 3 nuevas columnas, conversión tipos

---

**FASE 4: LOAD (Carga a SQLite)**
```python
conn = sqlite3.connect('sql/ventas.db')
df_clean.to_sql('datos_limpios', conn, if_exists='replace', index=False)

# Verificación
cursor.execute('SELECT COUNT(*) FROM datos_limpios')
print(f'✅ {cursor.fetchone()[0]} registros cargados')
```
- **Input:** DataFrame en memoria
- **Output:** ventas.db (~15 MB en disco)
- **Tiempo:** ~5 segundos

---

**FASE 5: ANALYZE (Consultas SQL + Visualización)**
```sql
-- Item 5a: Ventas mensuales
SELECT STRFTIME('%Y-%m', invoice_date) AS mes, SUM(total_sale)
FROM datos_limpios
GROUP BY mes
ORDER BY mes;

-- Item 5b: Top 5 categorías
SELECT category, SUM(quantity) AS unidades
FROM datos_limpios
GROUP BY category
ORDER BY unidades DESC
LIMIT 5;
```

```python
# Item 6: Visualización
plt.figure(figsize=(12,6))
ventas_mensuales.plot(kind='line', marker='o')
plt.title('Evolución Ventas Mensuales')
plt.savefig('visualizaciones/ventas.png', dpi=300)
```
- **Input:** Tabla SQL
- **Output:** Resultados + 8 gráficos PNG

---

**DIAGRAMA DE FLUJO:**
```
CSVs → MERGE → TRANSFORM → LOAD → QUERY → VISUALIZE
(12MB)  (11col)  (15col)   (DB)   (SQL)    (PNG)
        99,459   99,338    15MB   Items    8 files
```

**MÉTRICAS:**
- ⏱️ **Tiempo total:** 15-20 segundos
- 📊 **Tasa recuperación:** 99.88%
- 📁 **Archivos salida:** 1 DB + 8 gráficos
- ✅ **Consultas SQL:** 4 ejecutadas

---

**17. ¿Cuál fue el mayor desafío técnico que enfrentaron?**

**RESPUESTA:**

**Garantizar reproducibilidad entre Google Colab y entornos locales**.

**EL PROBLEMA:**
```python
# Código inicial (NO funcionaba en todos lados)
df = pd.read_csv('customer_data.csv')

# Errores:
# - Colab: FileNotFoundError (archivos no en /content/)
# - Windows: Solo funciona si ejecutas desde carpeta correcta
# - Linux: Paths relativos diferentes
```

**SOLUCIÓN IMPLEMENTADA:**
```python
import sys, os

if 'google.colab' in sys.modules:
    print("🚀 Google Colab detectado")
    
    # Clonar repo automáticamente
    !git clone https://github.com/Pablo-Tab/ABP-INNOVACION-DATOS.git
    os.chdir('/content/ABP-INNOVACION-DATOS')
    
    # Verificar archivos
    archivos = ['customer_data.csv', 'sales_data.csv']
    for archivo in archivos:
        if os.path.exists(archivo):
            size = os.path.getsize(archivo) / (1024*1024)
            print(f"✅ {archivo} ({size:.2f} MB)")
        else:
            print(f"❌ {archivo} faltante")
    
    # Crear estructura
    os.makedirs('datos', exist_ok=True)
    os.makedirs('visualizaciones', exist_ok=True)
    
else:
    print("💻 Jupyter local detectado")
    print(f"📁 Directorio: {os.getcwd()}")
```

**IMPACTO:**

✅ **Antes:**
- "No me funciona" → 30 min debugging email

✅ **Después:**
- Open in Colab → Run All → Funciona automáticamente

**APRENDIZAJES:**
1. Siempre asumir que tu código correrá en entorno diferente
2. Validar existencia de archivos antes de usarlos
3. Mensajes de error descriptivos ahorran horas
4. Automatización > instrucciones manuales

---

**18. Si tuvieran que automatizar este ETL para que corra diariamente, ¿cómo lo harían?**

**RESPUESTA - ARQUITECTURA DE PRODUCCIÓN:**

**COMPONENTE 1: SCRIPT ETL MODULARIZADO**
```python
class ETLPipeline:
    def extract(self):
        """Extrae desde API/CSV/DB"""
        logging.info("Extrayendo datos...")
        df = pd.read_csv(...)
        return df
    
    def transform(self, df):
        """Limpia y transforma"""
        logging.info("Transformando...")
        df['total_sale'] = df['quantity'] * df['price']
        return df
    
    def load(self, df):
        """Carga a base de datos"""
        logging.info("Cargando a DB...")
        df.to_sql('datos', conn, if_exists='append')  # ← append, no replace
    
    def validate(self, df):
        """Valida calidad"""
        assert (df['price'] > 0).all()
        assert df['invoice_no'].is_unique
    
    def run(self):
        """Pipeline completo con manejo de errores"""
        try:
            df = self.extract()
            df = self.transform(df)
            self.validate(df)
            self.load(df)
            self.enviar_alerta("✅ ETL exitoso")
        except Exception as e:
            logging.error(f"❌ ETL falló: {e}")
            self.enviar_alerta(f"❌ Error: {e}")
```

**COMPONENTE 2: SCHEDULER**
```bash
# Cron job (Linux) - ejecutar todos los días 2 AM
0 2 * * * /usr/bin/python3 /path/to/etl_automatizado.py

# Windows Task Scheduler
# Crear tarea programada: diario 2 AM
```

**COMPONENTE 3: LOGGING**
```python
logging.basicConfig(
    filename=f'logs/etl_{datetime.now().strftime("%Y%m%d")}.log',
    level=logging.INFO
)

# Logs generados:
# 2025-01-09 02:00:01 - INFO - Extrayendo datos
# 2025-01-09 02:00:05 - INFO - 1,248 registros procesados
# 2025-01-09 02:00:10 - INFO - ✅ ETL completado en 9.2s
```

**COMPONENTE 4: ALERTAS**
```python
def enviar_alerta(self, mensaje):
    # Email
    msg = MIMEText(mensaje)
    server.send_message(msg)
    
    # O Slack webhook
    requests.post('https://hooks.slack.com/...', json={'text': mensaje})
```

**COMPONENTE 5: BACKUP**
```bash
# Backup diario de DB
cp sql/ventas.db backups/ventas_$(date +%Y%m%d).db

# Eliminar backups > 30 días
find backups/ -mtime +30 -delete
```

**CRONOGRAMA DIARIO:**
```
02:00 AM - Inicia ETL
02:00:05 - Extract completo
02:00:10 - Transform completo
02:00:12 - Validaciones OK
02:00:17 - Load completo
02:00:18 - Email "✅ ETL exitoso"
```

**BENEFICIOS:**
- ✅ Sin intervención manual
- ✅ Detección temprana errores
- ✅ Auditoría completa (logs)
- ✅ Recuperación automática (reintentos)

---

**19. ¿Qué herramientas adicionales conocen para ETL?**

**RESPUESTA:**

| Herramienta | Tipo | Cuándo usar | Por qué NO la usamos |
|-------------|------|-------------|---------------------|
| **Apache Spark** | Big Data | >100 GB, procesamiento distribuido | Nuestros 15 MB no lo justifican |
| **Apache Airflow** | Orquestador | ETL complejos con dependencias | Overkill para este proyecto educativo |
| **Talend / Pentaho** | GUI ETL | Usuarios no programadores | Preferimos código (más flexible) |
| **AWS Glue** | Cloud ETL | Datos en AWS S3, serverless | No usamos cloud |
| **dbt** | SQL transforms | Transformaciones SQL complejas | Transformaciones simples en Pandas |

**¿Cuándo migrar de Pandas+SQLite?**

```
Pandas suficiente si:
- Datos < 10 GB
- Corre en una máquina
- No requiere distribución

Migrar a Spark si:
- Datos > 100 GB
- Requiere cluster (múltiples máquinas)
- Procesamiento distribuido
```

**Nuestro caso:** Pandas es perfecto para 99,459 registros (~15 MB). No necesitamos infraestructura más compleja.

---

**20. ¿Qué recomendación le darían al centro comercial basada en los datos?**

**RESPUESTA - INSIGHTS ESTRATÉGICOS:**

**1. FOCO EN SEGMENTO FEMENINO (59.8% del mercado)**
```
Hallazgo: Mujeres generan 59.8% de transacciones
Recomendación: 
- Ampliar secciones de Clothing y Cosmetics
- Marketing dirigido a mujeres 25-35 años
- Promociones en días de mayor afluencia femenina
```

**2. EFECTIVO SIGUE SIENDO REY (44.7%)**
```
Hallazgo: Cash es método preferido
Recomendación:
- Mantener cajeros ATM funcionales
- Incentivos para adopción de tarjetas (cashback)
- No eliminar pago en efectivo (error común)
```

**3. CLOTHING ES CATEGORÍA ESTRELLA**
```
Hallazgo: Clothing genera más ingresos
Recomendación:
- Expandir marcas de ropa
- Convenios con retailers internacionales
- Eventos fashion (desfiles, lanzamientos)
```

**4. TECNOLOGÍA: ALTO TICKET, BAJA FRECUENCIA**
```
Hallazgo: Technology = precios altos pero pocas ventas
Recomendación:
- Planes de financiación 0% interés
- Trade-in de equipos usados
- Asesoría técnica personalizada
```

**5. OPORTUNIDAD EN JÓVENES 25-35**
```
Hallazgo: Rango 25-35 años = 28% del mercado, high spending
Recomendación:
- Programas de fidelización para millennials
- Integración con apps móviles (puntos, cupones)
- Experiencias Instagram-able (marketing viral)
```

**CONCLUSIÓN:**
"Basado en análisis de 99,459 transacciones (2021-2023), recomendamos priorizar el segmento femenino joven con estrategia omnicanal que respete preferencia por efectivo mientras incentiva digitalización. Clothing debe ser pilar con expansión de marcas, mientras Technology requiere estrategia de financiación para aumentar conversión."


---

## 📊 RESUMEN FINAL

### ✅ **20 PREGUNTAS DISTRIBUIDAS:**

**Programación I (8 preguntas):**
1. Por qué Pandas vs Python puro
2. merge() vs concat()
3. .copy() y referencias
4. format en fechas
5. mean/median/mode
6. Matplotlib
7. POO en el proyecto
8. Relación con temario Prog I

**Base de Datos II (6 preguntas):**
9. Por qué SQLite
10. Normalización
11. to_sql()
12. Consulta ventas mensuales
13. WHERE vs HAVING
14. Relación con temario BD II

**Integradoras (6 preguntas):**
15. Decisiones técnicas diferenciadoras
16. Flujo ETL completo
17. Mayor desafío técnico
18. Automatización diaria
19. Herramientas ETL adicionales
20. Recomendaciones estratégicas

---

## 💡 TIPS FINALES PARA EL COLOQUIO

### ✅ **QUÉ HACER:**
1. **Hablar con seguridad** de lo que hicieron (entender, no memorizar)
2. **Usar terminología técnica** correcta
3. **Relacionar teoría con práctica** del proyecto
4. **Admitir** si no sabés algo: "No lo recuerdo exactamente, pero investigaría en [recurso]"
5. **Llevar laptop** con código abierto por si piden ver algo

### ❌ **QUÉ EVITAR:**
1. Decir "lo hizo mi compañero" (responsabilidad grupal)
2. Inventar respuestas técnicas incorrectas
3. No poder explicar código que entregaron
4. Contradecir lo que está en el notebook

---

## 🎯 **FRASE DE CONFIANZA**

> "Implementamos un ETL completo con 99,459 registros aplicando limpieza de datos, análisis estadístico, carga a SQLite y generación de insights estratégicos. Tomamos decisiones técnicas conscientes que priorizan reproducibilidad, performance y claridad. Estamos preparados para defender cada aspecto del proyecto."

---

**¡ÉXITO EN EL COLOQUIO! 🚀**
