# ESTRUCTURA DOCUMENTO WORD - TRABAJO PRÁCTICO ETL

## FORMATO REQUERIDO:
- **Letra:** Arial 12
- **Interlineado:** 1.5
- **Márgenes:** Normales (2.5 cm)

---

## CARÁTULA (Página 1)

```
[Centrado, Arial 14, Negrita]

INSTITUTO SUPERIOR POLITÉCNICO CÓRDOBA (ISPC)
TECNICATURA SUPERIOR EN CIENCIA DE DATOS E INTELIGENCIA ARTIFICIAL

[Espacio]

TRABAJO PRÁCTICO
Exploración, Transformación y Limpieza de Datos utilizando Pandas

Proceso ETL para Análisis de Datos de Ventas y Clientes

[Espacio]

Espacio Curricular: INNOVACIÓN DE DATOS

Profesores:
- Alejandro Mainero (Programación I)
- Carlos Charletti (Base de Datos II)

[Espacio]

Integrantes:
- Paola García (DNI: 29463402)
- Pablo Taborda (DNI: 28270596)
- Julio Orjindo (DNI: 26482639)
- Rodenas Elías Gabriel (DNI: 36356976)

[Espacio]

Cohorte: 2025
Fecha: Octubre 2025
```

---

## ÍNDICE (Página 2)

```
ÍNDICE

1. Introducción .................................................. 3
2. FASE 1: Extracción de Datos (Extract) ........................ 4
   2.1. Item 1: Carga de archivos CSV ........................... 4
   2.2. Item 2: Descripción del proceso ......................... 5
   2.3. Item 3: Concatenación de DataFrames .................... 6
3. FASE 2: Transformación de Datos (Transform) ................. 7
   3.1. Limpieza y preparación .................................. 7
   3.2. Item 4: Transformaciones adicionales .................... 8
       3.2.1. Item 4a: Modo de pago más frecuente ............... 8
       3.2.2. Item 4b: Modo de pago por género .................. 9
       3.2.3. Item 4c: Pagos rango 25-35 años ................... 10
       3.2.4. Item 4d: Pagos utilizados por mujeres ............. 11
       3.2.5. Item 4e: Precios por categoría .................... 12
   3.3. Item 5: Documentación transformaciones .................. 13
4. FASE 3: Limpieza de Datos (Load) ............................ 14
   4.1. Item 6: DataFrame limpio final .......................... 14
5. FASE 4: Análisis Exploratorio ............................... 15
   5.1. Visualizaciones ......................................... 15
   5.2. Análisis estadístico .................................... 18
6. Carga de Datos y Consultas SQL .............................. 20
   6.1. Esquema de base de datos ................................ 20
   6.2. Consultas SQL ........................................... 21
7. Conclusiones y Recomendaciones .............................. 23
8. Bibliografía ................................................ 25
```

---

## CONTENIDO (Página 3 en adelante)

### **1. INTRODUCCIÓN** (1 página)

```
[Arial 12, Justificado]

El presente trabajo práctico tiene como objetivo aplicar el proceso ETL 
(Extracción, Transformación y Limpieza) sobre datos reales de ventas y 
clientes del mercado de Estambul, Turquía.

Dataset utilizado: "Customer Shopping Dataset" de Kaggle
Período: Enero 2021 - Marzo 2023
Registros: 99,459 transacciones
Ubicación: 10 shopping malls de Estambul

El análisis se estructura en cuatro fases principales:
1. Extracción de datos desde archivos CSV
2. Transformación y limpieza de datos
3. Carga de datos procesados
4. Análisis exploratorio y visualización

Este trabajo simula una consultoría estratégica real para una entidad 
financiera interesada en comprender el comportamiento de medios de pago 
en el mercado turco.
```

---

### **2. FASE 1: EXTRACCIÓN DE DATOS** (3-4 páginas)

#### **2.1. Item 1: Carga de archivos CSV**

```
[Incluir código Python]

# Item 1: Cargar datos de clientes
try:
    df_customers = pd.read_csv('../customer_data.csv')
    print('Datos de clientes cargados exitosamente')
    print(f'Total de registros: {len(df_customers)}')
    print(f'Columnas: {list(df_customers.columns)}')
except Exception as e:
    print(f'Error al cargar customer_data.csv: {e}')

[Incluir CAPTURA de pantalla del output]
```

**Resultado:**
- Dataset clientes: 99,459 registros, 4 columnas
- Dataset ventas: 99,459 registros, 9 columnas

[Repetir para sales_data.csv]

#### **2.2. Item 2: Descripción del proceso**

```
[Explicación del proceso]

El proceso de extracción consistió en:

1. Uso de pd.read_csv() de la librería Pandas
2. Manejo de excepciones con try-except
3. Exploración inicial con:
   - .head(): primeras 5 filas
   - .info(): tipos de datos y valores nulos
   - .describe(): estadísticas descriptivas
   - .isnull().sum(): conteo de valores faltantes

[Incluir CAPTURAS de .info() y .describe() de ambos DataFrames]
```

#### **2.3. Item 3: Concatenación de DataFrames**

```
[Código + Explicación]

Se utilizó pd.merge() para realizar un JOIN por customer_id:

df_combined = pd.merge(df_sales, df_customers, on='customer_id', how='left')

[Incluir CAPTURA de df_combined.head()]

Resultado: 99,459 registros con 12 columnas combinadas.

NOTA IMPORTANTE: Los DataFrames originales (df_customers y df_sales) 
se mantienen sin modificar según lo requerido en la consigna.
```

---

### **3. FASE 2: TRANSFORMACIÓN** (8-10 páginas)

#### **3.2.1. Item 4a: Modo de pago más frecuente**

```
[Código Python]

payment_counts = df_clean['payment_method'].value_counts()
print(payment_counts)

[Incluir CAPTURA del output]

[Incluir GRÁFICO 01: Distribución métodos de pago]

RESULTADO:
- Cash: 44,397 transacciones (44.7%) ← MÁS FRECUENTE
- Credit Card: 34,898 transacciones (35.1%)
- Debit Card: 20,043 transacciones (20.2%)

INTERPRETACIÓN:
El efectivo domina el mercado con 44.7%, representando una oportunidad 
significativa para la digitalización de pagos.
```

[REPETIR ESTRUCTURA PARA ITEMS 4b, 4c, 4d, 4e]

Cada item debe incluir:
1. Código Python utilizado
2. Captura de pantalla del output
3. Gráfico correspondiente (si aplica)
4. Interpretación de resultados

---

### **4. FASE 3: LIMPIEZA** (2-3 páginas)

```
[Código + Capturas + Explicación]

Item 6: Se creó DataFrame final con 15 columnas seleccionadas:
- 99,338 registros (99.88% del dataset original)
- 121 registros eliminados por valores nulos (0.12%)

[Incluir tabla de restricciones de integridad]

Restricción                  | Validación
---------------------------- | -----------
Precios negativos            | 0 registros
Cantidades negativas         | 0 registros
Edades fuera rango (18-100)  | 0 registros
Valores nulos campos críticos| 0 registros

[Captura de df_final.head() e info()]
```

---

### **5. ANÁLISIS EXPLORATORIO** (4-5 páginas)

```
Se generaron 10 visualizaciones clave:

[Insertar los 10 gráficos PNG con títulos y numeración]

Gráfico 1: Distribución de Métodos de Pago
[Imagen 01_metodos_pago.png]

Interpretación: El efectivo representa 44.7% de transacciones...

[Repetir para cada gráfico]

Matriz de Correlación (Gráfico 10):
- Correlación fuerte: quantity vs total_sale (0.89)
- Correlación moderada: price vs total_sale (0.61)
- Correlación débil: age vs variables financieras
```

---

### **6. SQL** (2-3 páginas)

```
[Incluir código SQL]

6.1. ESQUEMA DE BASE DE DATOS

CREATE TABLE datos_limpios (
    invoice_no TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    gender TEXT CHECK(gender IN ('Male', 'Female')),
    age INTEGER CHECK(age >= 18 AND age <= 100),
    ...
);

[Capturas de SQLite o queries ejecutadas]

6.2. CONSULTAS SQL EQUIVALENTES A ITEMS 4a-4e

-- Item 4a: Modo de pago más frecuente
SELECT payment_method, COUNT(*) as total
FROM datos_limpios
GROUP BY payment_method
ORDER BY total DESC;

[Incluir resultado de ejecución]
```

---

### **7. CONCLUSIONES** (3-4 páginas)

```
HALLAZGOS PRINCIPALES:

1. CASH DOMINANTE (44.7%)
   - 44,397 transacciones mensuales en efectivo
   - Oportunidad de $113M anuales para digitalización
   - Comportamiento estable 2021-2023 (sin cambio natural)

2. SEGMENTO FEMENINO CRÍTICO (59.8%)
   - Mujeres dominan el mercado
   - Mismo comportamiento de pago que hombres
   - Target prioritario para estrategias comerciales

3. EDAD NO PREDICE DIGITALIZACIÓN
   - Jóvenes 25-35 años: 44.6% cash (igual que general)
   - Incentivos económicos > apelaciones tecnológicas

4. CLOTHING + SHOES = 74% VENTAS
   - Clothing: $113.8M (líder absoluto)
   - Technology: Ticket promedio más alto ($3,157)
   - Focalización clara en 3 categorías

RECOMENDACIONES ESTRATÉGICAS:

[Incluir tabla de recomendaciones del INFORME_FINAL_CONSULTORIA.md]

Estrategia                | Inversión | ROI proyectado
------------------------- | --------- | --------------
Migración Cash→Digital    | $1M       | 51.3% año 1
Segmento Premium (>$5K)   | $500K     | 80-120%
Alianzas Retailers        | $200K     | Valor lifetime
Producto BNPL             | $300K     | $8-12M año 2

VALIDACIÓN PROCESO ETL:
✅ Extracción: 2 CSV → 99,459 registros
✅ Transformación: 6 operaciones documentadas
✅ Limpieza: 99.88% datos válidos
✅ Análisis: 10 visualizaciones + estadísticas
```

---

### **8. BIBLIOGRAFÍA** (1 página)

```
BIBLIOGRAFÍA

Fuentes Académicas:

[1] Silberschatz, A., Korth, H. F., & Sudarshan, S. (2006). 
    Fundamentos de Bases de Datos (5ª ed.). McGraw-Hill.

[2] Ullman, J. D., & Widom, J. (1999). 
    Introducción a los Sistemas de Bases de Datos. Prentice Hall.

[3] Instituto Superior Politécnico Córdoba (ISPC). (2024-2025). 
    Fundamentos de estadística y probabilidad aplicada al análisis de datos. 
    Material didáctico.

[4] Instituto Superior Politécnico Córdoba (ISPC). (2024-2025). 
    Apunte de Analítica de Datos - Estadística Descriptiva. 
    Material didáctico.

Fuentes de Datos:

[5] Kaggle Dataset (2023). Customer Shopping Dataset - Retail Sales Data. 
    Istanbul Shopping Malls (2021-2023).
    URL: https://www.kaggle.com/datasets/mehmettahiraslan/customer-shopping-dataset

Herramientas y Tecnología:

[6] McKinney, Wes (2022). Python for Data Analysis (3rd Edition). 
    O'Reilly Media.

[7] Pandas Documentation (2025). pandas.pydata.org

[8] SQLite Documentation (2025). sqlite.org/docs.html

[9] Matplotlib Documentation (2025). matplotlib.org
```

---

## TIPS PARA FORMATEAR EN WORD:

1. **Estilos predefinidos:**
   - Título 1: Arial 14, Negrita, Color Azul oscuro
   - Título 2: Arial 12, Negrita
   - Texto normal: Arial 12, Justificado

2. **Código Python:**
   - Fuente: Courier New 10
   - Color: Gris oscuro (#333333)
   - Fondo: Gris claro (#F5F5F5)

3. **Tablas:**
   - Estilo "Tabla con cuadrícula"
   - Encabezado con fondo azul claro

4. **Imágenes:**
   - Centradas
   - Pie de figura: Arial 10, Cursiva
   - Numeración: "Figura 1:", "Figura 2:", etc.

5. **Márgenes y espaciado:**
   - Entre secciones: 2 líneas
   - Antes de imágenes: 1 línea
   - Después de imágenes: 1 línea

---

TOTAL ESTIMADO: 25-30 páginas
