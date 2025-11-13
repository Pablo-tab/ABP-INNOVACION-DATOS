# 📘 GUÍA COMPLETA: JUPYTER NOTEBOOK Y CÓDIGOS PRINCIPALES DEL PROYECTO ETL

## 📑 ÍNDICE
1. [¿Qué es Jupyter Notebook?](#que-es-jupyter)
2. [Estructura de un Notebook](#estructura-notebook)
3. [Códigos principales del proyecto](#codigos-principales)
4. [Librerías utilizadas](#librerias)
5. [Comandos esenciales](#comandos-esenciales)

---

## 🎯 ¿QUÉ ES JUPYTER NOTEBOOK? {#que-es-jupyter}

**Jupyter Notebook** es un entorno interactivo de programación que permite:
- Escribir y ejecutar código Python **celda por celda**
- Combinar código, texto explicativo (Markdown) y visualizaciones en un solo documento
- Ejecutar código de forma **incremental** (no necesitas correr todo de una vez)
- Ver resultados inmediatamente después de cada ejecución

### **Ventajas para proyectos ETL:**
✅ Ideal para análisis exploratorio de datos (EDA)  
✅ Permite documentar el proceso paso a paso  
✅ Puedes ejecutar y probar código por partes  
✅ Visualizaciones integradas (gráficos se muestran directamente)  
✅ Compatible con Google Colab (notebook en la nube)

---

## 📋 ESTRUCTURA DE UN NOTEBOOK {#estructura-notebook}

Un notebook se organiza en **celdas** de dos tipos:

### **1. Celdas de Markdown (texto explicativo)**
```markdown
# Título Principal
## Subtítulo
**Texto en negrita**
- Lista con viñetas
```

### **2. Celdas de Código (Python)**
```python
# Esto es código Python ejecutable
import pandas as pd
df = pd.read_csv('datos.csv')
print(df.head())
```

### **Cómo ejecutar celdas:**
- **Shift + Enter**: Ejecuta la celda y pasa a la siguiente
- **Ctrl + Enter**: Ejecuta la celda y permanece en ella
- **Alt + Enter**: Ejecuta la celda y crea una nueva debajo

---

## 💻 CÓDIGOS PRINCIPALES DEL PROYECTO ETL {#codigos-principales}

### **FASE 1: IMPORTAR LIBRERÍAS**

```python
# Importar bibliotecas necesarias
import pandas as pd           # Manipulación de datos (DataFrames)
import numpy as np            # Operaciones matemáticas y arrays
import matplotlib.pyplot as plt  # Crear gráficos y visualizaciones
import sqlite3                # Conectar con bases de datos SQLite
from datetime import datetime # Manejar fechas y tiempos
import warnings
warnings.filterwarnings('ignore')  # Ocultar advertencias molestas

# Configuración de visualización
plt.style.use('default')
plt.rcParams['figure.figsize'] = (12, 6)  # Tamaño de gráficos
plt.rcParams['font.size'] = 10             # Tamaño de fuente

print('✅ Bibliotecas importadas correctamente')
print(f'Pandas version: {pd.__version__}')
print(f'NumPy version: {np.__version__}')
```

**¿Qué hace este código?**
- Importa todas las herramientas (librerías) que necesitamos
- Configura el tamaño y estilo de los gráficos
- Verifica que las librerías se cargaron correctamente

---

### **FASE 2: CARGAR DATOS DESDE CSV**

```python
# Cargar archivos CSV a DataFrames de Pandas
df_customers = pd.read_csv('../customer_data.csv')
df_sales = pd.read_csv('../sales_data.csv')

print(f'✅ customer_data.csv cargado (Registros: {len(df_customers)})')
print(f'✅ sales_data.csv cargado (Registros: {len(df_sales)})')

# Ver las primeras 5 filas
print(df_customers.head())
```

**¿Qué hace este código?**
- `pd.read_csv()`: Lee archivos CSV y los convierte en DataFrames
- `len(df)`: Cuenta cuántas filas tiene el DataFrame
- `.head()`: Muestra las primeras 5 filas para inspeccionar los datos

---

### **FASE 3: ANÁLISIS EXPLORATORIO DE DATOS (EDA)**

```python
# Información general del DataFrame
print(df_customers.info())

# Estadísticas descriptivas
print(df_customers.describe())

# Verificar valores nulos
print(df_customers.isnull().sum())

# Ver columnas del DataFrame
print(df_customers.columns)
```

**¿Qué hace cada método?**
- `.info()`: Muestra tipos de datos, cantidad de valores no nulos, memoria usada
- `.describe()`: Calcula promedio, mínimo, máximo, desviación estándar
- `.isnull().sum()`: Cuenta cuántos valores nulos hay en cada columna
- `.columns`: Lista los nombres de todas las columnas

---

### **FASE 4: UNIR DATAFRAMES (JOIN)**

```python
# Unir dos DataFrames usando una columna común
df_combined = pd.merge(df_sales, df_customers, on='customer_id', how='left')

print(f'✅ DataFrames unidos exitosamente')
print(f'Total de registros: {len(df_combined)}')
print(f'Total de columnas: {len(df_combined.columns)}')
```

**¿Qué hace este código?**
- `pd.merge()`: Une dos DataFrames (como un JOIN en SQL)
- `on='customer_id'`: Especifica la columna clave para relacionar
- `how='left'`: Tipo de JOIN (mantiene todos los registros de df_sales)

**Tipos de JOIN:**
- `how='left'`: Mantiene todas las filas de la tabla izquierda
- `how='right'`: Mantiene todas las filas de la tabla derecha
- `how='inner'`: Solo mantiene coincidencias en ambas tablas
- `how='outer'`: Mantiene todas las filas de ambas tablas

---

### **FASE 5: LIMPIEZA DE DATOS**

```python
# Crear copia para no modificar el original
df_clean = df_combined.copy()

# Eliminar filas con valores nulos en columnas críticas
df_clean = df_clean.dropna(subset=['customer_id', 'price'])

# Verificar duplicados
print(f'Duplicados encontrados: {df_clean.duplicated().sum()}')

# Eliminar duplicados (si existen)
df_clean = df_clean.drop_duplicates()

print(f'Registros después de limpieza: {len(df_clean)}')
```

**¿Qué hace este código?**
- `.copy()`: Crea una copia independiente del DataFrame
- `.dropna(subset=['col'])`: Elimina filas con valores nulos en columnas específicas
- `.duplicated()`: Identifica filas duplicadas
- `.drop_duplicates()`: Elimina filas duplicadas

---

### **FASE 6: TRANSFORMACIÓN DE DATOS**

#### **Convertir fechas:**
```python
# Convertir columna de texto a tipo datetime
df_clean['invoice_date'] = pd.to_datetime(df_clean['invoice_date'], format='%d-%m-%Y')

# Extraer componentes de fecha
df_clean['year'] = df_clean['invoice_date'].dt.year
df_clean['month'] = df_clean['invoice_date'].dt.month
df_clean['day_of_week'] = df_clean['invoice_date'].dt.day_name()

print(f'Rango de fechas: {df_clean["invoice_date"].min()} a {df_clean["invoice_date"].max()}')
```

**¿Qué hace este código?**
- `pd.to_datetime()`: Convierte texto a formato fecha
- `.dt.year`: Extrae el año de una fecha
- `.dt.month`: Extrae el mes (número)
- `.dt.day_name()`: Extrae el nombre del día de la semana

---

#### **Crear columnas calculadas:**
```python
# Calcular el total de venta
df_clean['total_sale'] = df_clean['quantity'] * df_clean['price']

print(f'Total de ventas: ${df_clean["total_sale"].sum():,.2f}')
```

---

#### **Categorizar datos:**
```python
# Crear función de categorización
def categorize_age(age):
    if age < 25:
        return 'Jovenes (< 25)'
    elif 25 <= age <= 35:
        return 'Adultos jovenes (25-35)'
    elif 36 <= age <= 50:
        return 'Adultos (36-50)'
    else:
        return 'Adultos mayores (> 50)'

# Aplicar función a toda la columna
df_clean['age_group'] = df_clean['age'].apply(categorize_age)

# Ver distribución de grupos
print(df_clean['age_group'].value_counts())
```

**¿Qué hace este código?**
- `def`: Define una función personalizada
- `.apply()`: Aplica una función a cada valor de una columna
- `.value_counts()`: Cuenta cuántas veces aparece cada valor único

---

### **FASE 7: ANÁLISIS Y AGREGACIONES**

```python
# Contar valores únicos
payment_counts = df_final['payment_method'].value_counts()
print(payment_counts)

# Agrupar y calcular estadísticas
price_by_category = df_final.groupby('category')['price'].agg([
    ('Precio_Minimo', 'min'),
    ('Precio_Maximo', 'max'),
    ('Precio_Promedio', 'mean'),
    ('Precio_Mediana', 'median')
]).round(2)

print(price_by_category)

# Tabla cruzada (crosstab)
payment_by_gender = pd.crosstab(df_final['gender'], df_final['payment_method'])
print(payment_by_gender)

# Filtrar datos
df_25_35 = df_final[(df_final['age'] >= 25) & (df_final['age'] <= 35)]
print(f'Registros entre 25-35 años: {len(df_25_35)}')
```

**¿Qué hace cada método?**
- `.value_counts()`: Cuenta frecuencia de cada valor único
- `.groupby()`: Agrupa datos por una columna
- `.agg()`: Aplica múltiples funciones de agregación
- `pd.crosstab()`: Crea tabla de frecuencias cruzadas
- Filtros con condiciones: `df[df['col'] > valor]`

---

### **FASE 8: VISUALIZACIONES**

#### **Gráfico de barras:**
```python
import matplotlib.pyplot as plt

# Crear figura
plt.figure(figsize=(10, 6))

# Obtener datos
payment_counts = df_final['payment_method'].value_counts()

# Crear gráfico de barras
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
plt.bar(payment_counts.index, payment_counts.values, color=colors)

# Configurar títulos y etiquetas
plt.title('Distribución de Métodos de Pago', fontsize=14, fontweight='bold')
plt.xlabel('Método de Pago')
plt.ylabel('Cantidad de Transacciones')

# Agregar valores sobre barras
for i, v in enumerate(payment_counts.values):
    plt.text(i, v + 500, str(v), ha='center', fontweight='bold')

# Ajustar diseño
plt.tight_layout()

# Guardar gráfico
plt.savefig('../visualizaciones/01_metodos_pago.png', dpi=300, bbox_inches='tight')

# Mostrar gráfico
plt.show()

print('✅ Gráfico guardado: 01_metodos_pago.png')
```

---

#### **Histograma:**
```python
plt.figure(figsize=(12, 6))

# Crear histograma
plt.hist(df_final['age'], bins=30, color='#45B7D1', edgecolor='black', alpha=0.7)

# Agregar líneas de referencia
plt.axvline(df_final['age'].mean(), color='red', linestyle='--', linewidth=2, 
            label=f'Media: {df_final["age"].mean():.1f}')
plt.axvline(df_final['age'].median(), color='green', linestyle='--', linewidth=2, 
            label=f'Mediana: {df_final["age"].median():.1f}')

plt.title('Distribución de Edades de los Clientes', fontsize=14, fontweight='bold')
plt.xlabel('Edad')
plt.ylabel('Frecuencia')
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('../visualizaciones/03_distribucion_edades.png', dpi=300)
plt.show()
```

---

#### **Gráfico de líneas (evolución temporal):**
```python
# Agrupar por año y mes
monthly_sales = df_final.groupby(['year', 'month'])['total_sale'].sum().reset_index()

# Crear columna de fecha
monthly_sales['date'] = pd.to_datetime(monthly_sales[['year', 'month']].assign(day=1))

# Crear gráfico
plt.figure(figsize=(14, 6))
plt.plot(monthly_sales['date'], monthly_sales['total_sale'], 
         marker='o', linewidth=2, color='#4ECDC4')

plt.title('Evolución de Ventas Mensuales', fontsize=14, fontweight='bold')
plt.xlabel('Fecha')
plt.ylabel('Ventas Totales ($)')
plt.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('../visualizaciones/08_evolucion_ventas.png', dpi=300)
plt.show()
```

---

### **FASE 9: GUARDAR RESULTADOS**

```python
# Guardar DataFrame limpio en CSV
output_path = '../datos/datos_limpios.csv'
df_final.to_csv(output_path, index=False, encoding='utf-8')

print(f'✅ DataFrame guardado en: {output_path}')
print(f'Total de registros: {len(df_final)}')
```

**Parámetros importantes:**
- `index=False`: No guarda el índice (números de fila) en el CSV
- `encoding='utf-8'`: Codificación para caracteres especiales (tildes, ñ)

---

## 📚 LIBRERÍAS UTILIZADAS {#librerias}

### **1. PANDAS (`import pandas as pd`)**

**¿Para qué sirve?**
Manipulación y análisis de datos estructurados (tablas).

**Comandos principales:**
```python
pd.read_csv('archivo.csv')        # Leer archivo CSV
pd.merge(df1, df2, on='col')      # Unir DataFrames
df.head()                         # Primeras 5 filas
df.tail()                         # Últimas 5 filas
df.info()                         # Información del DataFrame
df.describe()                     # Estadísticas descriptivas
df.isnull().sum()                 # Contar valores nulos
df.drop_duplicates()              # Eliminar duplicados
df.dropna()                       # Eliminar filas con nulos
df.value_counts()                 # Contar valores únicos
df.groupby('col')                 # Agrupar datos
df.sort_values('col')             # Ordenar por columna
df[df['col'] > 100]               # Filtrar datos
df['nueva_col'] = df['col1'] * 2  # Crear nueva columna
```

---

### **2. NUMPY (`import numpy as np`)**

**¿Para qué sirve?**
Operaciones matemáticas y manejo de arrays (listas numéricas).

**Comandos principales:**
```python
np.mean([1, 2, 3, 4])            # Calcular promedio
np.median([1, 2, 3, 4])          # Calcular mediana
np.std([1, 2, 3, 4])             # Desviación estándar
np.sum([1, 2, 3, 4])             # Suma total
np.min([1, 2, 3, 4])             # Valor mínimo
np.max([1, 2, 3, 4])             # Valor máximo
```

---

### **3. MATPLOTLIB (`import matplotlib.pyplot as plt`)**

**¿Para qué sirve?**
Crear gráficos y visualizaciones.

**Comandos principales:**
```python
plt.figure(figsize=(10, 6))      # Crear figura con tamaño
plt.bar(x, y)                    # Gráfico de barras
plt.hist(data, bins=30)          # Histograma
plt.plot(x, y)                   # Gráfico de líneas
plt.scatter(x, y)                # Gráfico de dispersión
plt.title('Título')              # Agregar título
plt.xlabel('Eje X')              # Etiqueta eje X
plt.ylabel('Eje Y')              # Etiqueta eje Y
plt.legend()                     # Agregar leyenda
plt.grid()                       # Agregar cuadrícula
plt.savefig('grafico.png')       # Guardar gráfico
plt.show()                       # Mostrar gráfico
```

---

### **4. SQLITE3 (`import sqlite3`)**

**¿Para qué sirve?**
Conectar con bases de datos SQLite.

**Comandos principales:**
```python
# Conectar a base de datos
conn = sqlite3.connect('ventas.db')

# Ejecutar consulta SQL
df = pd.read_sql_query("SELECT * FROM tabla", conn)

# Guardar DataFrame en tabla SQL
df.to_sql('nombre_tabla', conn, if_exists='replace', index=False)

# Cerrar conexión
conn.close()
```

---

## 🔧 COMANDOS ESENCIALES DE JUPYTER {#comandos-esenciales}

### **Atajos de teclado:**

**Modo Comando (presiona ESC primero):**
- `A`: Insertar celda arriba
- `B`: Insertar celda abajo
- `D D`: Eliminar celda
- `M`: Convertir celda a Markdown
- `Y`: Convertir celda a código
- `Z`: Deshacer eliminación de celda

**Modo Edición (presiona ENTER):**
- `Ctrl + /`: Comentar/descomentar línea
- `Tab`: Autocompletar código
- `Shift + Tab`: Ver documentación de función

**Ejecución:**
- `Shift + Enter`: Ejecutar celda y pasar a la siguiente
- `Ctrl + Enter`: Ejecutar celda sin moverse
- `Alt + Enter`: Ejecutar celda y crear nueva debajo

---

### **Comandos mágicos de Jupyter:**

```python
# Ver variables en memoria
%whos

# Medir tiempo de ejecución
%time código_aquí

# Ejecutar script externo
%run script.py

# Limpiar salida de celda
from IPython.display import clear_output
clear_output()

# Mostrar gráfico en el notebook
%matplotlib inline
```

---

## 📊 RESUMEN DEL FLUJO ETL EN JUPYTER

```
┌─────────────────────────────────────────────────────┐
│  1. IMPORTAR LIBRERÍAS                              │
│     import pandas, numpy, matplotlib                │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  2. EXTRACT (Extracción)                            │
│     df = pd.read_csv('datos.csv')                   │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  3. ANÁLISIS EXPLORATORIO                           │
│     df.head(), df.info(), df.describe()             │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  4. TRANSFORM (Transformación)                      │
│     - Limpieza de nulos: df.dropna()                │
│     - Conversión fechas: pd.to_datetime()           │
│     - Cálculos: df['nueva'] = df['a'] * df['b']    │
│     - Categorización: df.apply(función)             │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  5. ANÁLISIS Y VISUALIZACIÓN                        │
│     - Agregaciones: groupby(), value_counts()       │
│     - Gráficos: plt.bar(), plt.hist(), plt.plot()   │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  6. LOAD (Carga)                                    │
│     - CSV: df.to_csv()                              │
│     - SQL: df.to_sql()                              │
└─────────────────────────────────────────────────────┘
```

---

## 🎓 CONSEJOS PARA TRABAJAR EN JUPYTER

### **Buenas prácticas:**

1. **Ejecuta las celdas en orden secuencial** (de arriba a abajo)
   - Jupyter recuerda las variables en el orden que ejecutas

2. **Reinicia el kernel si algo sale mal:**
   - Menú → Kernel → Restart & Clear Output

3. **Guarda frecuentemente:**
   - `Ctrl + S` o menú File → Save

4. **Comenta tu código:**
   ```python
   # Esto es un comentario explicativo
   df = pd.read_csv('datos.csv')  # Comentario al final de línea
   ```

5. **Usa nombres descriptivos:**
   ```python
   # ❌ MAL
   df1, df2, x, y
   
   # ✅ BIEN
   df_customers, df_sales, total_ventas, promedio_edad
   ```

6. **Divide procesos complejos en celdas separadas:**
   - Una celda por operación principal
   - Más fácil de debuggear y entender

7. **Agrega celdas Markdown explicativas:**
   - Documenta qué hace cada sección
   - Explica decisiones de limpieza

---

## 🔍 DEBUGGING EN JUPYTER

### **Si algo no funciona:**

1. **Ver el error completo:**
   - Lee el mensaje de error de abajo hacia arriba
   - La última línea suele decir qué falló

2. **Verificar tipos de datos:**
   ```python
   print(df['columna'].dtype)
   print(type(variable))
   ```

3. **Verificar valores:**
   ```python
   print(df['columna'].unique())
   print(df['columna'].value_counts())
   ```

4. **Ver primeras filas después de cada transformación:**
   ```python
   print(df.head())
   ```

5. **Verificar dimensiones:**
   ```python
   print(f'Shape: {df.shape}')  # (filas, columnas)
   ```

---

## ✅ CHECKLIST DE VERIFICACIÓN

Antes de dar por terminado tu notebook ETL:

- [ ] Todas las celdas ejecutan sin errores
- [ ] Las celdas están en orden lógico (Extract → Transform → Load)
- [ ] Hay celdas Markdown explicando cada fase
- [ ] Los gráficos se muestran correctamente
- [ ] Los archivos de salida se guardan correctamente
- [ ] No hay variables temporales innecesarias
- [ ] El código está comentado adecuadamente
- [ ] Los resultados coinciden con lo esperado

---

## 🚀 EJEMPLO COMPLETO: MINI ETL EN JUPYTER

```python
# ===================================
# CELDA 1: IMPORTAR LIBRERÍAS
# ===================================
import pandas as pd
import matplotlib.pyplot as plt

# ===================================
# CELDA 2: CARGAR DATOS
# ===================================
df = pd.read_csv('ventas.csv')
print(f'✅ Datos cargados: {len(df)} registros')

# ===================================
# CELDA 3: EXPLORAR DATOS
# ===================================
print(df.head())
print(df.info())
print(df.isnull().sum())

# ===================================
# CELDA 4: LIMPIAR DATOS
# ===================================
# Eliminar nulos
df_clean = df.dropna(subset=['precio', 'cantidad'])

# Calcular total
df_clean['total'] = df_clean['precio'] * df_clean['cantidad']

print(f'✅ Limpieza completa: {len(df_clean)} registros')

# ===================================
# CELDA 5: ANÁLISIS
# ===================================
ventas_por_categoria = df_clean.groupby('categoria')['total'].sum()
print(ventas_por_categoria)

# ===================================
# CELDA 6: VISUALIZACIÓN
# ===================================
plt.figure(figsize=(10, 6))
plt.bar(ventas_por_categoria.index, ventas_por_categoria.values)
plt.title('Ventas por Categoría')
plt.xlabel('Categoría')
plt.ylabel('Total Ventas ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('ventas_categoria.png')
plt.show()

# ===================================
# CELDA 7: GUARDAR RESULTADOS
# ===================================
df_clean.to_csv('datos_limpios.csv', index=False)
print('✅ Archivo guardado: datos_limpios.csv')
```

---

## 📖 RECURSOS ADICIONALES

### **Documentación oficial:**
- Pandas: https://pandas.pydata.org/docs/
- NumPy: https://numpy.org/doc/
- Matplotlib: https://matplotlib.org/stable/contents.html
- Jupyter: https://jupyter.org/documentation

### **Cheat Sheets (hojas de referencia rápida):**
- Pandas Cheat Sheet: https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf
- Matplotlib Cheat Sheet: https://matplotlib.org/cheatsheets/

---

## 🎯 RESUMEN FINAL

**Jupyter Notebook es como un cuaderno digital donde:**
- Escribes código Python en celdas
- Lo ejecutas paso a paso
- Ves resultados inmediatamente
- Documentas todo el proceso
- Guardas gráficos y análisis

**Para el proyecto ETL usamos:**
- **Pandas** → Manipular tablas (DataFrames)
- **NumPy** → Cálculos matemáticos
- **Matplotlib** → Crear gráficos
- **SQLite** → Guardar en base de datos

**Flujo típico:**
1. Importar librerías
2. Cargar datos (CSV)
3. Explorar y limpiar
4. Transformar y calcular
5. Analizar y visualizar
6. Guardar resultados

---

**📌 ESTE DOCUMENTO CUBRE TODO LO QUE NECESITÁS SABER PARA TU COLOQUIO**

¡Guarda este archivo como referencia rápida! 🚀
