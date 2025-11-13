# 📘 MÓDULO 1: CONFIGURACIÓN DEL ENTORNO DE DESARROLLO

**Proyecto:** Análisis ETL - Entidad Financiera  
**Equipo:** Paola Garcia, Pablo Taborda, Julio Orjindo, Rodenas Elias Gabriel  
**Fecha:** Octubre-Noviembre 2025

---

## 🎯 OBJETIVO

Configurar el entorno de desarrollo completo para realizar un proyecto de análisis ETL (Extract, Transform, Load) con Python, incluyendo:
- Editor de código (VS Code)
- Control de versiones (Git/GitHub)
- Entorno Python con sus librerías
- Integración con Google Colab

---

## 📋 PASO 1: INSTALACIÓN DE HERRAMIENTAS BASE

### 1.1 Visual Studio Code (VS Code)

**¿Qué es?** Editor de código gratuito de Microsoft, ideal para proyectos Python.

**Instalación:**
1. Descargar desde: https://code.visualstudio.com/
2. Ejecutar instalador (Windows: `VSCodeUserSetup-x64-1.x.x.exe`)
3. Durante instalación, marcar opciones:
   - ✅ "Add to PATH"
   - ✅ "Create a desktop icon"
   - ✅ "Add 'Open with Code' action"

**Verificación:**
```powershell
# Abrir PowerShell y ejecutar:
code --version
```

**Salida esperada:**
```
1.84.2
commitid
x64
```

---

### 1.2 Python

**¿Qué es?** Lenguaje de programación para análisis de datos.

**Instalación:**
1. Descargar desde: https://www.python.org/downloads/
2. Versión recomendada: Python 3.11.x o superior
3. Durante instalación:
   - ✅ **IMPORTANTE:** Marcar "Add Python to PATH"
   - Seleccionar "Install Now"

**Verificación:**
```powershell
# Abrir PowerShell y ejecutar:
python --version
```

**Salida esperada:**
```
Python 3.11.6
```

---

### 1.3 Git

**¿Qué es?** Sistema de control de versiones para rastrear cambios en el código.

**Instalación:**
1. Descargar desde: https://git-scm.com/download/win
2. Durante instalación, usar opciones por defecto
3. En "Adjusting your PATH environment":
   - Seleccionar: "Git from the command line and also from 3rd-party software"

**Verificación:**
```powershell
# Abrir PowerShell y ejecutar:
git --version
```

**Salida esperada:**
```
git version 2.42.0.windows.2
```

---

## 📋 PASO 2: EXTENSIONES DE VS CODE

### 2.1 Extensión de Python

**¿Para qué sirve?** Autocompletado, depuración y ejecución de código Python.

**Instalación:**
1. Abrir VS Code
2. Presionar `Ctrl + Shift + X` (abre panel de extensiones)
3. Buscar: `Python`
4. Instalar la extensión de **Microsoft** (tiene logo de Python)

**Publisher:** `ms-python.python`

---

### 2.2 Extensión Jupyter

**¿Para qué sirve?** Ejecutar notebooks (archivos `.ipynb`) dentro de VS Code.

**Instalación:**
1. En panel de extensiones (`Ctrl + Shift + X`)
2. Buscar: `Jupyter`
3. Instalar la extensión de **Microsoft**

**Publisher:** `ms-toolsai.jupyter`

---

### 2.3 Extensión GitLens (Opcional pero recomendada)

**¿Para qué sirve?** Visualizar historial de cambios en Git de forma gráfica.

**Instalación:**
1. Buscar: `GitLens`
2. Instalar extensión de **GitKraken**

**Publisher:** `eamodio.gitlens`

---

## 📋 PASO 3: CREAR REPOSITORIO EN GITHUB

### 3.1 Crear cuenta en GitHub

1. Ir a: https://github.com/
2. Click en "Sign up"
3. Seguir pasos (correo, contraseña, username)
4. Verificar email

**Usuario creado:** `Pablo-Tab`

---

### 3.2 Crear nuevo repositorio

1. Una vez logueado, click en botón verde "New" (arriba izquierda)
2. Configurar:
   - **Repository name:** `ABP-INNOVACION-DATOS`
   - **Description:** "Proyecto ETL - Análisis de Medios de Pago"
   - **Visibility:** ✅ Public (para que el profesor pueda verlo)
   - ⬜ NO marcar "Add README" (lo crearemos nosotros)
   - ⬜ NO agregar .gitignore aún
3. Click en "Create repository"

**URL del repositorio:** `https://github.com/Pablo-Tab/ABP-INNOVACION-DATOS`

---

## 📋 PASO 4: CONFIGURAR GIT LOCALMENTE

### 4.1 Configurar identidad

**¿Por qué?** Git necesita saber quién hace los cambios.

```powershell
# Ejecutar en PowerShell:
git config --global user.name "Pablo Taborda"
git config --global user.email "tu_email@ejemplo.com"
```

**Verificar configuración:**
```powershell
git config --global --list
```

---

### 4.2 Crear carpeta del proyecto

```powershell
# Navegar a Desktop
cd Desktop

# Crear carpeta TECNICATURA si no existe
mkdir TECNICATURA
cd TECNICATURA

# Crear carpeta del proyecto
mkdir "ABP INNOVACION"
cd "ABP INNOVACION"
```

**Ruta final:** `C:\Users\PABLO\Desktop\TECNICATURA\ABP INNOVACION`

---

### 4.3 Inicializar repositorio Git

```powershell
# Dentro de la carpeta del proyecto:
git init
```

**Salida:**
```
Initialized empty Git repository in C:/Users/PABLO/Desktop/TECNICATURA/ABP INNOVACION/.git/
```

**¿Qué hace?** Crea una carpeta oculta `.git/` que rastrea todos los cambios.

---

### 4.4 Conectar con GitHub

```powershell
# Agregar repositorio remoto (cambiar Pablo-Tab por tu usuario):
git remote add origin https://github.com/Pablo-Tab/ABP-INNOVACION-DATOS.git

# Configurar rama principal como 'main':
git branch -M main

# Verificar conexión:
git remote -v
```

**Salida esperada:**
```
origin  https://github.com/Pablo-Tab/ABP-INNOVACION-DATOS.git (fetch)
origin  https://github.com/Pablo-Tab/ABP-INNOVACION-DATOS.git (push)
```

---

## 📋 PASO 5: CREAR ENTORNO VIRTUAL PYTHON

### 5.1 ¿Por qué un entorno virtual?

Un entorno virtual aísla las librerías de Python del proyecto para:
- Evitar conflictos entre versiones
- Tener control de dependencias
- Facilitar replicación del proyecto

### 5.2 Crear entorno virtual

```powershell
# Dentro de la carpeta del proyecto:
python -m venv venv
```

**¿Qué hace?** Crea carpeta `venv/` con una instalación limpia de Python.

---

### 5.3 Activar entorno virtual

```powershell
# En PowerShell:
.\venv\Scripts\Activate.ps1
```

**Posible error:** "Execution of scripts is disabled on this system"

**Solución:**
```powershell
# Ejecutar PowerShell como Administrador y ejecutar:
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Entorno activado cuando veas:**
```
(venv) PS C:\Users\PABLO\Desktop\TECNICATURA\ABP INNOVACION>
```

---

## 📋 PASO 6: INSTALAR LIBRERÍAS PYTHON

### 6.1 Crear archivo requirements.txt

**¿Qué es?** Lista de todas las librerías necesarias con sus versiones.

```powershell
# Crear archivo:
code requirements.txt
```

**Contenido del archivo:**
```txt
pandas==2.1.1
numpy==1.26.0
matplotlib==3.8.0
openpyxl==3.1.2
jupyter==1.0.0
notebook==7.0.4
```

---

### 6.2 Instalar librerías

```powershell
# Con entorno activado (debe verse (venv) al inicio):
pip install -r requirements.txt
```

**¿Qué hace cada librería?**

| Librería | Función |
|----------|---------|
| **pandas** | Manipulación de datos (DataFrames, CSV, Excel) |
| **numpy** | Operaciones numéricas y arrays |
| **matplotlib** | Crear gráficos y visualizaciones |
| **openpyxl** | Leer/escribir archivos Excel (.xlsx) |
| **jupyter** | Entorno interactivo para notebooks |
| **notebook** | Interfaz web de Jupyter |

**Tiempo estimado:** 2-3 minutos

---

### 6.3 Verificar instalación

```powershell
# Listar librerías instaladas:
pip list
```

**Deberías ver:**
```
Package         Version
--------------- -------
pandas          2.1.1
numpy           1.26.0
matplotlib      3.8.0
...
```

---

## 📋 PASO 7: CREAR ESTRUCTURA DE CARPETAS

### 7.1 Estructura del proyecto

```powershell
# Crear carpetas necesarias:
mkdir notebooks
mkdir datos
mkdir sql
mkdir visualizaciones
```

**Estructura final:**
```
ABP INNOVACION/
├── venv/              # Entorno virtual (no se sube a GitHub)
├── notebooks/         # Notebooks Jupyter (.ipynb)
├── datos/             # Datos originales y procesados (.csv)
├── sql/               # Scripts SQL (schema.sql, consultas.sql)
├── visualizaciones/   # Gráficos generados (.png)
├── requirements.txt   # Dependencias del proyecto
└── README.md          # Documentación principal
```

---

## 📋 PASO 8: CONFIGURAR .gitignore

### 8.1 ¿Qué es .gitignore?

Archivo que indica qué carpetas/archivos NO subir a GitHub (datos sensibles, archivos grandes, entorno virtual).

### 8.2 Crear archivo .gitignore

```powershell
# Crear archivo:
code .gitignore
```

**Contenido:**
```
# Entorno virtual
venv/
env/
.venv/

# Archivos de Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Jupyter Notebook
.ipynb_checkpoints/

# Archivos del sistema
.DS_Store
Thumbs.db
desktop.ini

# Archivos temporales
*.tmp
*.swp
*~

# Archivos grandes (opcional)
*.csv
!datos/datos_limpios.csv
```

**Nota:** La línea `!datos/datos_limpios.csv` permite subir SOLO ese CSV específico.

---

## 📋 PASO 9: CREAR README.md

### 9.1 ¿Qué es README.md?

Archivo en formato Markdown que explica el proyecto. Es lo primero que se ve en GitHub.

### 9.2 Crear archivo README.md

```powershell
code README.md
```

**Contenido básico:**
```markdown
# 📊 Proyecto ETL - Análisis de Medios de Pago

## 🎯 Objetivo
Realizar análisis ETL completo de datos de clientes y ventas de una entidad financiera.

## 👥 Equipo
- Paola Garcia
- Pablo Taborda
- Julio Orjindo
- Rodenas Elias Gabriel

## 🛠️ Tecnologías
- Python 3.11
- Pandas, NumPy, Matplotlib
- Jupyter Notebook
- SQLite
- Git/GitHub

## 📁 Estructura del Proyecto
```
ABP-INNOVACION-DATOS/
├── notebooks/          # Notebooks Jupyter
├── datos/              # Datasets
├── sql/                # Scripts SQL
├── visualizaciones/    # Gráficos
└── requirements.txt    # Dependencias
```

## 🚀 Cómo ejecutar
1. Clonar repositorio: `git clone https://github.com/Pablo-Tab/ABP-INNOVACION-DATOS.git`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Abrir notebook: `jupyter notebook notebooks/analisis_etl.ipynb`

## 📚 Documentación
Ver carpeta `DOCUMENTACION_TECNICA/` para guías paso a paso.
```

---

## 📋 PASO 10: PRIMER COMMIT Y PUSH

### 10.1 Verificar archivos creados

```powershell
# Ver estado del repositorio:
git status
```

**Verás archivos en rojo (sin rastrear):**
```
Untracked files:
  .gitignore
  README.md
  requirements.txt
  ...
```

---

### 10.2 Agregar archivos al staging area

```powershell
# Agregar todos los archivos:
git add .
```

**¿Qué hace?** Prepara archivos para el commit (guardar cambios).

---

### 10.3 Crear primer commit

```powershell
# Crear commit con mensaje descriptivo:
git commit -m "Initial commit - Estructura base del proyecto"
```

**Salida:**
```
[main (root-commit) a1b2c3d] Initial commit - Estructura base del proyecto
 5 files changed, 123 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 README.md
 create mode 100644 requirements.txt
 ...
```

---

### 10.4 Subir a GitHub

```powershell
# Push al repositorio remoto:
git push -u origin main
```

**Primera vez:** GitHub pedirá autenticación (usuario/contraseña o token).

**Salida exitosa:**
```
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
...
To https://github.com/Pablo-Tab/ABP-INNOVACION-DATOS.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## ✅ RESULTADO FINAL

### Verificar en GitHub

1. Ir a: `https://github.com/Pablo-Tab/ABP-INNOVACION-DATOS`
2. Deberías ver:
   - ✅ README.md visualizado
   - ✅ Carpetas: notebooks, datos, sql, visualizaciones
   - ✅ Archivos: .gitignore, requirements.txt

---

## 🎓 RESUMEN DE COMANDOS PRINCIPALES

| Comando | Descripción |
|---------|-------------|
| `code --version` | Verificar instalación de VS Code |
| `python --version` | Verificar versión de Python |
| `git --version` | Verificar instalación de Git |
| `git init` | Inicializar repositorio Git |
| `git remote add origin <url>` | Conectar con GitHub |
| `python -m venv venv` | Crear entorno virtual |
| `.\venv\Scripts\Activate.ps1` | Activar entorno (Windows) |
| `pip install -r requirements.txt` | Instalar dependencias |
| `git add .` | Agregar archivos al staging |
| `git commit -m "mensaje"` | Guardar cambios localmente |
| `git push origin main` | Subir cambios a GitHub |

---

## 🔄 PRÓXIMOS PASOS

Ver **MÓDULO 2: OBTENCIÓN Y CARGA DE DATOS** para:
- Descargar datasets
- Cargarlos en Python
- Exploración inicial con Pandas

---

**Documento creado:** 8 de noviembre de 2025  
**Parte de:** Documentación Técnica Completa - Proyecto ETL TSCDIA
