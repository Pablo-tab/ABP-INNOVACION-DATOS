# 🚀 GUÍA RÁPIDA: GITHUB Y GOOGLE COLAB

## 📦 **SUBIR PROYECTO A GITHUB**

### **Paso 1: Inicializar repositorio Git**

```bash
# Navegar a la carpeta del proyecto
cd "C:\Users\PABLO\Desktop\TECNICATURA\ABP INNOVACION"

# Inicializar repositorio
git init

# Agregar todos los archivos
git add .

# Primer commit
git commit -m "Proyecto ETL completo - Análisis Medios de Pago Estambul"
```

### **Paso 2: Crear repositorio en GitHub**

1. Ve a https://github.com
2. Click en **"New repository"**
3. Nombre: `ABP-INNOVACION-DATOS`
4. Descripción: `Proyecto ETL - Análisis de Medios de Pago (TSCDIA 2025)`
5. Selecciona: **Public** (para que sea accesible)
6. **NO marques** "Initialize with README" (ya tenemos uno)
7. Click **"Create repository"**

### **Paso 3: Conectar repositorio local con GitHub**

```bash
# Reemplaza TU_USUARIO con tu username de GitHub
git remote add origin https://github.com/TU_USUARIO/ABP-INNOVACION-DATOS.git

# Subir archivos
git branch -M main
git push -u origin main
```

### **Paso 4: Verificar archivos subidos**

Deberías ver en GitHub:
- ✅ `customer_data.csv` y `sales_data.csv` (datasets)
- ✅ `notebooks/analisis_etl.ipynb` (notebook principal)
- ✅ `sql/schema.sql` y `sql/consultas.sql`
- ✅ `README.md` (documentación)
- ✅ Todos los archivos .md de documentación
- ✅ Scripts Python (.py)

---

## 🔗 **PREPARAR NOTEBOOK PARA GOOGLE COLAB**

### **Paso 1: Agregar celda inicial para Colab**

Inserta esta celda AL PRINCIPIO del notebook (antes de la primera celda):

```python
# ========================================
# CONFIGURACIÓN PARA GOOGLE COLAB
# ========================================
# Ejecutar SOLO si estás en Google Colab
# Si ejecutas en Jupyter local, SALTAR esta celda

import sys

if 'google.colab' in sys.modules:
    print("🚀 Ejecutando en Google Colab")
    
    # 1. Clonar repositorio desde GitHub
    !git clone https://github.com/TU_USUARIO/ABP-INNOVACION-DATOS.git
    
    # 2. Cambiar directorio de trabajo
    import os
    os.chdir('/content/ABP-INNOVACION-DATOS')
    
    # 3. Verificar archivos
    !ls -la
    
    print("✅ Repositorio clonado correctamente")
    print("✅ Los archivos CSV están disponibles en el directorio actual")
else:
    print("💻 Ejecutando en Jupyter local")
    print("✅ Usando archivos CSV del directorio actual")
```

### **Paso 2: Modificar rutas de archivos**

En las celdas donde cargas CSV, cambiar rutas absolutas a relativas:

**ANTES (local):**
```python
df_customers = pd.read_csv('../customer_data.csv')
df_sales = pd.read_csv('../sales_data.csv')
```

**DESPUÉS (compatible con Colab):**
```python
# Detectar entorno y ajustar rutas
import os
if 'google.colab' in sys.modules:
    # En Colab: archivos en raíz del repo
    df_customers = pd.read_csv('customer_data.csv')
    df_sales = pd.read_csv('sales_data.csv')
else:
    # En local: archivos en directorio padre
    df_customers = pd.read_csv('../customer_data.csv')
    df_sales = pd.read_csv('../sales_data.csv')
```

### **Paso 3: Crear badge de Colab en README**

Agrega esto al inicio de `README.md`:

```markdown
# 📊 PROYECTO ETL - ANÁLISIS DE MEDIOS DE PAGO ESTAMBUL

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TU_USUARIO/ABP-INNOVACION-DATOS/blob/main/notebooks/analisis_etl.ipynb)

**Consultoría Estratégica para Entidad Financiera**
```

### **Paso 4: Crear carpetas en Colab**

Agrega esta celda después de la configuración inicial:

```python
# Crear carpetas necesarias (solo en Colab)
if 'google.colab' in sys.modules:
    import os
    os.makedirs('datos', exist_ok=True)
    os.makedirs('visualizaciones', exist_ok=True)
    print("✅ Carpetas creadas: datos/ y visualizaciones/")
```

---

## 📋 **CHECKLIST ANTES DE SUBIR A GITHUB**

### **Archivos obligatorios:**
- ✅ `README.md` (documentación principal)
- ✅ `.gitignore` (ya creado)
- ✅ `customer_data.csv` (dataset clientes)
- ✅ `sales_data.csv` (dataset ventas)
- ✅ `notebooks/analisis_etl.ipynb` (notebook principal)
- ✅ `sql/schema.sql` (estructura BD)
- ✅ `sql/consultas.sql` (queries)

### **Archivos opcionales pero recomendados:**
- ✅ `INFORME_FINAL_CONSULTORIA.md`
- ✅ `INFORME EJECUTIVO.docx`
- ✅ `cargar_a_sqlite.py`
- ✅ `analizar_datos_reales.py`
- ✅ `analisis_profundo_pagos.py`
- ✅ Todos los archivos de documentación (.md)

### **Archivos a NO subir:**
- ❌ `ventas_estambul.db` (base de datos - se regenera)
- ❌ `.ipynb_checkpoints/` (archivos temporales de Jupyter)
- ❌ `__pycache__/` (archivos temporales de Python)
- ❌ `.vscode/` (configuración de editor)

---

## 🧪 **PROBAR NOTEBOOK EN COLAB**

### **Paso 1: Abrir desde GitHub**

1. Ve a tu repositorio en GitHub
2. Navega a `notebooks/analisis_etl.ipynb`
3. Click en el botón **"Open in Colab"** (si agregaste el badge)

**O manualmente:**
1. Ve a https://colab.research.google.com
2. Click **"GitHub"**
3. Pega URL: `https://github.com/TU_USUARIO/ABP-INNOVACION-DATOS`
4. Selecciona `notebooks/analisis_etl.ipynb`

### **Paso 2: Ejecutar**

1. Click **"Runtime > Run all"**
2. Esperar a que se clone el repositorio
3. Verificar que los CSV se carguen correctamente
4. Ver resultados y gráficos

### **Paso 3: Descargar resultados**

```python
# Al final del notebook, agregar:
if 'google.colab' in sys.modules:
    from google.colab import files
    
    # Descargar CSV limpio
    files.download('datos/datos_limpios.csv')
    
    # Descargar visualizaciones
    import zipfile
    with zipfile.ZipFile('visualizaciones.zip', 'w') as zipf:
        for i in range(1, 11):
            zipf.write(f'visualizaciones/{i:02d}_*.png')
    files.download('visualizaciones.zip')
```

---

## 🔧 **SOLUCIÓN A PROBLEMAS COMUNES**

### **Problema 1: CSV no se encuentra en Colab**

**Error:** `FileNotFoundError: [Errno 2] No such file or directory: 'customer_data.csv'`

**Solución:**
```python
# Verificar ruta actual
import os
print(os.getcwd())
print(os.listdir('.'))

# Si los CSV están en subcarpeta:
df_customers = pd.read_csv('./customer_data.csv')
```

### **Problema 2: Repositorio muy grande para GitHub**

**Error:** `remote: error: File customer_data.csv is 100.00 MB; this exceeds GitHub's file size limit`

**Solución:**
```bash
# Instalar Git LFS (Large File Storage)
git lfs install
git lfs track "*.csv"
git add .gitattributes
git commit -m "Track large CSV files with LFS"
git push
```

### **Problema 3: Matplotlib no muestra gráficos en Colab**

**Solución:**
```python
# Agregar al inicio del notebook
%matplotlib inline
import matplotlib.pyplot as plt
```

---

## 📧 **COMPARTIR CON PROFESORES**

### **Opción 1: Link de GitHub**
```
https://github.com/TU_USUARIO/ABP-INNOVACION-DATOS
```

### **Opción 2: Link directo a Colab**
```
https://colab.research.google.com/github/TU_USUARIO/ABP-INNOVACION-DATOS/blob/main/notebooks/analisis_etl.ipynb
```

### **Opción 3: Descargar ZIP desde GitHub**
1. Ve al repositorio
2. Click **"Code" > "Download ZIP"**
3. Enviar ZIP por email/campus

---

## ✅ **COMANDOS RÁPIDOS DE RESUMEN**

```bash
# Inicializar y subir a GitHub
cd "C:\Users\PABLO\Desktop\TECNICATURA\ABP INNOVACION"
git init
git add .
git commit -m "Proyecto ETL completo"
git remote add origin https://github.com/TU_USUARIO/ABP-INNOVACION-DATOS.git
git push -u origin main

# Actualizar cambios posteriores
git add .
git commit -m "Actualización: [describir cambios]"
git push
```

---

**¡Listo para compartir tu trabajo! 🎉**
