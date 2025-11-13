# 📊 PROYECTO ETL - ANÁLISIS DE MEDIOS DE PAGO ESTAMBUL

**Consultoría Estratégica para Entidad Financiera**

**TSCDIA 2025 - Innovación de Datos**

---

## 👥 **EQUIPO DE TRABAJO**

- **Paola García** (DNI: 29463402)
- **Pablo Taborda** (DNI: 28270596)
- **Julio Orjindo** (DNI: 26482639)
- **Rodenas Elías Gabriel** (DNI: 36356976)

**Profesores:**
- Alejandro Mainero (Programación I)
- Carlos Charletti (Base de Datos II)

---

## 📁 **ESTRUCTURA DEL PROYECTO**

```
ABP INNOVACION/
│
├── 📄 ARCHIVOS DE DATOS
│   ├── customer_data.csv          ✅ Dataset original clientes (99,459 registros)
│   ├── sales_data.csv             ✅ Dataset original ventas (99,459 registros)
│   └── datos/
│       └── datos_limpios.csv      ✅ Dataset procesado (99,338 registros)
│
├── 📓 NOTEBOOKS JUPYTER
│   └── notebooks/
│       └── analisis_etl.ipynb     ✅ PRINCIPAL - Todo el proceso ETL
│
├── 🗄️ BASE DE DATOS SQL
│   ├── sql/
│   │   ├── schema.sql             ✅ Estructura de BD SQLite
│   │   └── consultas.sql          ✅ 17 consultas SQL
│   └── ventas_estambul.db         ⚙️ (Se genera al ejecutar cargar_a_sqlite.py)
│
├── 🐍 SCRIPTS PYTHON
│   ├── cargar_a_sqlite.py         ✅ Automatiza carga a SQLite
│   ├── analizar_datos_reales.py   ✅ Análisis rápido de datos
│   └── analisis_profundo_pagos.py ✅ Análisis evolutivo de medios de pago
│
├── 📊 VISUALIZACIONES
│   └── visualizaciones/
│       ├── 01_metodos_pago.png               ⚙️ (Generadas al ejecutar notebook)
│       ├── 02_pago_por_genero.png
│       ├── 03_distribucion_edades.png
│       ├── ...
│       ├── evolucion_mensual_pagos.png       ⚙️ (Script profundo)
│       ├── comparacion_anual_pagos.png
│       └── pago_por_rango_precio.png
│
├── 📋 INFORMES Y DOCUMENTACIÓN
│   ├── informe/
│   │   └── INFORME_ESTRATEGICO_ENTIDAD_FINANCIERA.txt  ✅ Informe consultaría
│   ├── CHECKLIST_DATOS_EXTERNOS.txt   ✅ Lista investigación
│   ├── PROYECTO ABP.docx              📝 (POR COMPLETAR)
│   ├── Evidencia Aprendizaje N° 3.pdf ✅ Consigna del TP
│   └── README.md                      ✅ Este archivo
│
└── ❌ ARCHIVOS A ELIMINAR
    ├── customer_data.csv.zip          ❌ (Ya descomprimido)
    ├── sales_data.csv.zip             ❌ (Ya descomprimido)
    └── ESTRUCTURA ABP (7).docx        ❌ (Duplicado/innecesario)
```

---

## 🎯 **FLUJO DE TRABAJO RECOMENDADO**

### **PASO 1: Ejecutar Notebook Principal** ⭐
```bash
# Abrir Jupyter Notebook
jupyter notebook notebooks/analisis_etl.ipynb

# Ejecutar todas las celdas en orden
# Esto generará:
# - datos/datos_limpios.csv
# - 10 visualizaciones PNG
# - Resultados del análisis ETL
```

### **PASO 2: Cargar a Base de Datos SQLite**
```bash
python cargar_a_sqlite.py

# Esto creará:
# - ventas_estambul.db (base de datos)
# - Validaciones de carga
```

### **PASO 3: Análisis Profundo** (Opcional pero recomendado)
```bash
# Análisis rápido
python analizar_datos_reales.py

# Análisis evolutivo de medios de pago
python analisis_profundo_pagos.py

# Genera 3 gráficos adicionales:
# - evolucion_mensual_pagos.png
# - comparacion_anual_pagos.png
# - pago_por_rango_precio.png
```

### **PASO 4: Consultar Base de Datos**
```bash
# Opción 1: DB Browser for SQLite (GUI)
# Abrir: ventas_estambul.db
# Ejecutar consultas de: sql/consultas.sql

# Opción 2: Línea de comandos
sqlite3 ventas_estambul.db
.read sql/consultas.sql
```

### **PASO 5: Completar Documentación**
1. Investigar datos externos (usar `CHECKLIST_DATOS_EXTERNOS.txt`)
2. Completar `PROYECTO ABP.docx`
3. Tomar capturas del notebook ejecutado
4. Preparar presentación final

---

## 📊 **DATOS DEL ANÁLISIS**

### **Volumen de Datos**
- **Total registros:** 99,338 transacciones válidas
- **Período:** Enero 2021 - Marzo 2023 (27 meses)
- **Clientes únicos:** ~99,000
- **Shopping Malls:** 10 centros comerciales
- **Categorías:** 8 (Clothing, Shoes, Technology, etc.)

### **Hallazgos Clave**
- **Cash domina:** 44.7% de transacciones
- **Mujeres:** 59.8% del mercado
- **Edad promedio:** 43.4 años
- **Categoría líder:** Clothing ($113.8M en ventas)
- **Tecnología:** Precio promedio más alto ($3,157)

---

## 🛠️ **REQUISITOS TÉCNICOS**

### **Python 3.8+**
```bash
pip install pandas numpy matplotlib sqlite3
```

### **Jupyter Notebook**
```bash
pip install jupyter
```

### **Opcional: DB Browser for SQLite**
- Descargar: https://sqlitebrowser.org/

---

## 📝 **ENTREGABLES DEL PROYECTO**

### ✅ **COMPLETADOS:**
1. Notebook Jupyter con proceso ETL completo
2. DataFrames de extracción (clientes, ventas, combinado)
3. DataFrame limpio final (datos_limpios.csv)
4. Base de datos SQLite con esquema
5. 17 consultas SQL documentadas
6. 13 visualizaciones profesionales
7. Scripts de automatización
8. Informe estratégico para entidad financiera
9. Análisis evolutivo de medios de pago

### 📝 **POR COMPLETAR:**
1. ~~Documento PROYECTO ABP.docx~~ (Siguiente paso)
2. ~~Investigación de datos externos~~ (Checklist creado)
3. ~~Bibliografía técnica~~ (Esperando tu input)
4. ~~Capturas de pantalla del notebook~~ (Al ejecutar)
5. ~~Presentación final~~ (Opcional)

---

## 🎓 **CUMPLIMIENTO DE REQUISITOS**

### ✅ **Extracción de Datos (Items 1-3)**
- [x] Item 1: Carga de CSVs en DataFrames distintos
- [x] Item 2: Descripción del proceso de extracción
- [x] Item 3: Concatenación (merge) de DataFrames

### ✅ **Transformación de Datos (Items 4-5)**
- [x] Item 4a: Modo de pago más frecuente
- [x] Item 4b: Categorización por género
- [x] Item 4c: Pagos rango 25-35 años
- [x] Item 4d: Pagos más usados por mujeres
- [x] Item 4e: Precios por categoría
- [x] Item 5: Documentación de transformaciones

### ✅ **Limpieza de Datos (Item 6)**
- [x] Item 6: DataFrame limpio con restricciones de integridad

### ✅ **Base de Datos SQL**
- [x] Esquema de BD (schema.sql)
- [x] Consultas SQL equivalentes a transformaciones
- [x] Script de carga automatizada

### ✅ **Análisis Exploratorio**
- [x] Comportamiento por género
- [x] Comportamiento por edad
- [x] Precios por categoría
- [x] Análisis temporal
- [x] Visualizaciones profesionales

### ✅ **Síntesis y Conclusiones**
- [x] Resumen ejecutivo
- [x] Conclusiones basadas en datos reales
- [x] Recomendaciones estratégicas
- [x] Plan de acción con ROI

---

## 🔍 **DIFERENCIACIÓN DEL PROYECTO**

### **Enfoque Único: Consultoría Estratégica**
A diferencia de otros grupos que solo harán ETL básico, este proyecto:

1. **Simula una consultoría real** para una entidad financiera
2. **Análisis temporal:** Evolución 2021-2023 (no solo foto estática)
3. **Estrategia CVL:** Plan de migración efectivo → digital
4. **ROI calculado:** Inversión $1.04M, retorno 51.3%
5. **Productos futuros:** NFC, Wallets, BNPL, Biométricos
6. **Segmentación profunda:** Por valor, categoría, mall, día
7. **Calendario táctico:** Promociones mes a mes
8. **Datos externos:** Contexto macroeconómico y demográfico

---

## 📚 **BIBLIOGRAFÍA**

### **Bases de Datos**
- **Silberschatz, Abraham; Korth, Henry F.; Sudarshan, S.** (2006). *Fundamentos de Bases de Datos* (5ª Edición). McGraw Hill.
- **Ullman, Jeffrey** (1999). *Introducción a los Sistemas de Bases de Datos*. Prentice Hall.

### **Estadística y Análisis de Datos**
- **ISPC** (2025). *Fundamentos de estadística y probabilidad aplicada al análisis de datos*. Instituto Superior Politécnico Córdoba.
- **ISPC** (2025). *Apunte de Analítica de Datos - Estadística Descriptiva*. Instituto Superior Politécnico Córdoba.

### **Fuentes de Datos**
- **Kaggle Dataset** (2023). *Customer Shopping Dataset - Retail Sales Data*. Istanbul Shopping Malls (2021-2023).
  - URL: https://www.kaggle.com/datasets/mehmettahiraslan/customer-shopping-dataset

### **Herramientas y Tecnología**
- **McKinney, Wes** (2022). *Python for Data Analysis* (3rd Edition). O'Reilly Media.
- **Pandas Documentation** (2025). pandas.pydata.org
- **SQLite Documentation** (2025). sqlite.org/docs.html
- **Matplotlib Documentation** (2025). matplotlib.org

---

## 📚 **PRÓXIMOS PASOS**

1. **✅ Ejecutar notebook completo** (tomar capturas)
2. **⏳ Investigar datos externos** (usar checklist)
3. **✅ Bibliografía incorporada** 
4. **⏳ Completar PROYECTO ABP.docx**
5. **✅ Archivos innecesarios eliminados**

---

## 💡 **TIPS PARA LA PRESENTACIÓN**

- Mostrar el **INFORME_ESTRATEGICO** como deliverable principal
- Enfatizar el **ROI y plan de acción** (diferenciador)
- Usar las **visualizaciones** para ilustrar hallazgos
- Mencionar **datos externos investigados** (contexto)
- Destacar **productos futuros** (visión prospectiva)

---

## 📞 **CONTACTO DEL EQUIPO**

**Correo del proyecto:** [Agregar email]
**Repositorio:** [Agregar GitHub si aplica]

---

**Última actualización:** Octubre 2025
**Versión:** 1.0
