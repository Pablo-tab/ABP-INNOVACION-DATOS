# 📚 GUÍA DE CONVERSIÓN A PDF - DOCUMENTACIÓN TÉCNICA

## 🎯 OPCIONES DISPONIBLES

Tienes **3 formas** de convertir los archivos Markdown (.md) a PDF con formato hermoso:

---

## ✨ OPCIÓN 1: Script Python Automático (RECOMENDADO)

### Instalación de dependencias:

```powershell
# En el terminal de VS Code:
cd "C:\Users\PABLO\Desktop\TECNICATURA\ABP INNOVACION\DOCUMENTACION_TECNICA"

# Activar entorno virtual
..\venv\Scripts\activate

# Instalar bibliotecas necesarias
pip install markdown weasyprint pygments
```

### Si tienes problemas con WeasyPrint en Windows:

1. **Descargar GTK3:**
   - Ir a: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
   - Descargar el instalador más reciente (por ejemplo: `gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe`)
   - Ejecutar el instalador

2. **Instalar WeasyPrint:**
   ```powershell
   pip install weasyprint
   ```

### Ejecución:

```powershell
# Ejecutar el script
python generar_libro_pdf.py
```

### Opciones del script:

Cuando ejecutes el script, te preguntará:
```
¿Qué deseas generar?
  1. PDFs individuales por módulo (8 archivos PDF separados)
  2. Libro completo (UN PDF con todos los módulos - ~100 páginas)
  3. Ambos (recomendado)
```

**Opción 3** es la recomendada: genera todo.

### Resultado:

Se creará la carpeta `PDF_GENERADOS/` con:
- ✅ 8 PDFs individuales (uno por cada módulo)
- ✅ `LIBRO_COMPLETO_DOCUMENTACION_ETL.pdf` (~12-15 MB, ~100-120 páginas)

---

## 📘 OPCIÓN 2: Extensión de VS Code (MÁS FÁCIL)

### Paso 1: Instalar extensión

1. En VS Code: `Ctrl + Shift + X`
2. Buscar: **"Markdown PDF"**
3. Instalar la extensión de **yzane** (la más popular)

### Paso 2: Convertir archivos

**Para un módulo individual:**
1. Abrir cualquier archivo .md (por ejemplo: `01_CONFIGURACION_ENTORNO.md`)
2. Click derecho en el editor
3. Seleccionar: **"Markdown PDF: Export (pdf)"**
4. Se generará el PDF en la misma carpeta

**Para múltiples archivos:**
1. Abrir cada archivo .md
2. Repetir el proceso anterior
3. Se generarán 8 PDFs (uno por módulo)

### Configuración ya incluida:

Ya creé el archivo `.vscode/settings.json` con configuración profesional:
- ✅ Formato A4
- ✅ Márgenes apropiados
- ✅ Encabezados y pies de página
- ✅ Alta calidad (100%)

---

## 🌐 OPCIÓN 3: Herramientas Online (SIN INSTALACIÓN)

Si no quieres instalar nada, usa estas webs:

### Dillinger.io (Recomendado)

1. Ir a: https://dillinger.io/
2. Click en "Import from" → "Disk"
3. Seleccionar un archivo .md
4. Click en "Export as" → "PDF"
5. Repetir para cada módulo

### StackEdit

1. Ir a: https://stackedit.io/
2. Click en el ícono de carpeta (izquierda)
3. "Import from disk"
4. Seleccionar archivo .md
5. Click en el menú (☰) → "Export as PDF"

### Markdown to PDF

1. Ir a: https://www.markdowntopdf.com/
2. Arrastrar archivo .md o hacer click en "Choose file"
3. Click en "Convert"
4. Descargar el PDF generado

---

## 🎨 CARACTERÍSTICAS DEL PDF GENERADO

Usando el **script Python** (`generar_libro_pdf.py`), obtendrás PDFs con:

### ✨ Formato profesional:
- ✅ Tipografía clara y legible (Segoe UI)
- ✅ Títulos con colores y decoraciones
- ✅ Tablas con gradientes y sombras
- ✅ Bloques de código con sintaxis resaltada
- ✅ Emojis y símbolos visuales
- ✅ Márgenes apropiados para impresión

### 📄 Estructura de libro:
- ✅ Portada hermosa con gradiente
- ✅ Encabezado en cada página (título del documento)
- ✅ Pie de página con numeración ("Página X de Y")
- ✅ Autor y GitHub en cada página
- ✅ Saltos de página automáticos entre capítulos
- ✅ Índice de contenidos (TOC)

### 🎯 Elementos visuales:
- ✅ Títulos H1 con fondo degradado
- ✅ Íconos de emojis antes de cada título
- ✅ Tablas con encabezados en azul
- ✅ Código con fondo oscuro tipo VS Code
- ✅ Enlaces activos (clickeables en el PDF)
- ✅ Citas con borde lateral azul

---

## 📊 COMPARACIÓN DE OPCIONES

| Característica | Script Python | VS Code Extension | Online |
|----------------|---------------|-------------------|--------|
| **Instalación** | Requiere pip | 1 click | No requiere |
| **Calidad PDF** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Formato libro** | ✅ Completo | ⚠️ Básico | ⚠️ Básico |
| **Portada** | ✅ Hermosa | ❌ No | ❌ No |
| **Múltiples archivos** | ✅ Automático | ⚠️ Manual | ⚠️ Manual |
| **Libro completo** | ✅ Un PDF | ❌ No | ❌ No |
| **Personalización** | ✅ Total | ⚠️ Limitada | ❌ Mínima |
| **Velocidad** | Medio (1-2 min) | Rápido (10 seg) | Variable |

**Recomendación:** 
- 🥇 **Script Python** para el PDF final de entrega (máxima calidad)
- 🥈 **VS Code** para revisiones rápidas
- 🥉 **Online** si no puedes instalar nada

---

## 🚀 FLUJO DE TRABAJO RECOMENDADO

### Para entrega al profesor:

1. **Generar libro completo con Python:**
   ```powershell
   python generar_libro_pdf.py
   # Seleccionar opción 2 (Libro completo)
   ```

2. **Revisar el PDF:**
   - Abrir `PDF_GENERADOS/LIBRO_COMPLETO_DOCUMENTACION_ETL.pdf`
   - Verificar que todo se vea bien
   - Revisar que no falten páginas

3. **Entregar:**
   - Subir el PDF completo al aula virtual
   - O compartir link de Google Drive
   - O imprimir si se requiere físico

### Para compartir con compañeros:

**Opción A - PDFs individuales:**
```powershell
python generar_libro_pdf.py
# Seleccionar opción 1
```
- Permite que cada uno lea solo los módulos que necesita

**Opción B - Libro completo:**
- Más fácil de distribuir (1 solo archivo)
- Formato profesional de libro
- ~12-15 MB (fácil de enviar por email/WhatsApp)

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### Error: "No module named 'markdown'"

```powershell
pip install markdown weasyprint pygments
```

### Error: "OSError: cannot load library 'gobject-2.0-0'"

**Solución:** Instalar GTK3 para Windows
1. https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
2. Descargar e instalar
3. Reiniciar terminal
4. `pip install weasyprint` nuevamente

### Error: "Permission denied" al guardar PDF

**Solución:** Cerrar el PDF si está abierto en un visor

### PDF se ve mal o sin formato

**Solución:** Usar el script Python (`generar_libro_pdf.py`) en lugar de extensiones

---

## 📁 ARCHIVOS CREADOS

En la carpeta `DOCUMENTACION_TECNICA/`:

```
DOCUMENTACION_TECNICA/
├── 00_INDICE.md                      # Índice de módulos
├── 01_CONFIGURACION_ENTORNO.md       # Módulo 1
├── 02_CARGA_DATOS.md                 # Módulo 2
├── ... (más módulos)
├── generar_libro_pdf.py              # Script de conversión ⭐
├── style.css                         # CSS profesional
├── .vscode/
│   └── settings.json                 # Config VS Code
└── PDF_GENERADOS/                    # Se crea al ejecutar script
    ├── 00_INDICE.pdf
    ├── 01_CONFIGURACION_ENTORNO.pdf
    ├── ... (más PDFs)
    └── LIBRO_COMPLETO_DOCUMENTACION_ETL.pdf  # ⭐ PRINCIPAL
```

---

## ✅ CHECKLIST DE GENERACIÓN

Antes de entregar, verifica:

```
✅ PDF generado sin errores
✅ Todas las páginas presentes (~100-120)
✅ Portada con información correcta
✅ Tablas se ven bien formateadas
✅ Código legible y con colores
✅ Imágenes/emojis visibles
✅ Numeración de páginas correcta
✅ Enlaces funcionan (si el PDF lo soporta)
✅ Sin páginas en blanco extras
✅ Tamaño razonable (< 20 MB)
```

---

## 💡 CONSEJOS FINALES

### Para impresión:
- Imprimir a doble cara (ahorra papel)
- Usar calidad "Normal" (no Draft)
- Verificar márgenes antes de imprimir

### Para digital:
- El PDF es searchable (se puede buscar texto)
- Los enlaces son clickeables
- Perfecto para compartir por email o Drive
- Compatible con todos los visores de PDF

### Para presentación:
- Usar el libro completo (más profesional)
- Tener una copia digital de respaldo
- Practicar navegación rápida entre secciones

---

## 🎓 RESULTADO FINAL

Con el **script Python**, obtendrás un PDF profesional de ~100-120 páginas que:

- 📚 Se ve como un libro técnico profesional
- 🎨 Tiene formato hermoso y colores
- 📖 Es fácil de leer y navegar
- ✨ Impresiona por su calidad visual
- 🎯 Demuestra profesionalismo

**¡Perfecto para entregar al profesor o compartir con compañeros!**

---

**Creado:** 8 de noviembre de 2025  
**Autor:** Pablo Tab  
**Proyecto:** ETL TSCDIA 2025
