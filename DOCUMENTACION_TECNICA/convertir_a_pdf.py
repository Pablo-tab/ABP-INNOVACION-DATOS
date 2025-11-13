"""
Script MEJORADO para convertir archivos Markdown a PDF con formato PROFESIONAL tipo LIBRO
Requiere: pip install markdown pdfkit weasyprint pygments
También requiere wkhtmltopdf: https://wkhtmltopdf.org/downloads.html

INSTALACIÓN RÁPIDA:
    pip install markdown pdfkit weasyprint pygments

USO:
    python convertir_a_pdf.py
"""

import os
from pathlib import Path
from datetime import datetime

try:
    import markdown
    from weasyprint import HTML, CSS
    from pygments.formatters import HtmlFormatter
except ImportError:
    print("❌ ERROR: Faltan bibliotecas requeridas")
    print("\n📦 Instala las dependencias con:")
    print("   pip install markdown weasyprint pygments")
    exit(1)

# Configuración
INPUT_DIR = Path(__file__).parent
OUTPUT_DIR = INPUT_DIR / "PDF_GENERADOS"
OUTPUT_DIR.mkdir(exist_ok=True)

# Archivos a convertir (en orden)
ARCHIVOS = [
    "00_INDICE.md",
    "01_CONFIGURACION_ENTORNO.md",
    "02_CARGA_DATOS.md",
    "03_LIMPIEZA_TRANSFORMACION.md",
    "04_ANALISIS_VISUALIZACIONES.md",
    "05_IMPLEMENTACION_SQL.md",
    "06_GITHUB_COLAB.md",
    "07_TROUBLESHOOTING_RESUMEN.md"
]

# CSS para formato de libro
CSS_STYLE = """
<style>
    @page {
        size: A4;
        margin: 2cm;
    }
    
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 11pt;
        line-height: 1.6;
        color: #333;
        max-width: 800px;
        margin: 0 auto;
    }
    
    h1 {
        color: #2c3e50;
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
        margin-top: 30px;
        page-break-before: always;
    }
    
    h2 {
        color: #34495e;
        border-bottom: 2px solid #95a5a6;
        padding-bottom: 8px;
        margin-top: 25px;
    }
    
    h3 {
        color: #7f8c8d;
        margin-top: 20px;
    }
    
    code {
        background-color: #f4f4f4;
        padding: 2px 6px;
        border-radius: 3px;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 90%;
    }
    
    pre {
        background-color: #2d2d2d;
        color: #f8f8f2;
        padding: 15px;
        border-radius: 5px;
        overflow-x: auto;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 9pt;
        line-height: 1.4;
    }
    
    pre code {
        background-color: transparent;
        padding: 0;
        color: #f8f8f2;
    }
    
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
        font-size: 10pt;
    }
    
    th {
        background-color: #3498db;
        color: white;
        padding: 12px;
        text-align: left;
        border: 1px solid #2980b9;
    }
    
    td {
        padding: 10px;
        border: 1px solid #ddd;
    }
    
    tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    
    blockquote {
        border-left: 4px solid #3498db;
        padding-left: 20px;
        margin-left: 0;
        color: #555;
        font-style: italic;
    }
    
    hr {
        border: none;
        border-top: 2px solid #ecf0f1;
        margin: 30px 0;
    }
    
    ul, ol {
        margin: 15px 0;
        padding-left: 30px;
    }
    
    li {
        margin: 8px 0;
    }
    
    a {
        color: #3498db;
        text-decoration: none;
    }
    
    a:hover {
        text-decoration: underline;
    }
    
    .page-break {
        page-break-after: always;
    }
</style>
"""

def convertir_md_a_html(archivo_md):
    """Convierte archivo Markdown a HTML"""
    with open(archivo_md, 'r', encoding='utf-8') as f:
        contenido_md = f.read()
    
    # Convertir Markdown a HTML
    html = markdown2.markdown(
        contenido_md,
        extras=[
            "fenced-code-blocks",
            "tables",
            "break-on-newline",
            "code-friendly",
            "header-ids"
        ]
    )
    
    return html

def generar_pdf_individual(archivo_md):
    """Genera PDF individual para cada módulo"""
    print(f"Convirtiendo {archivo_md}...")
    
    try:
        html = convertir_md_a_html(INPUT_DIR / archivo_md)
        html_completo = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            {CSS_STYLE}
        </head>
        <body>
            {html}
        </body>
        </html>
        """
        
        # Nombre del PDF de salida
        nombre_pdf = archivo_md.replace('.md', '.pdf')
        ruta_pdf = OUTPUT_DIR / nombre_pdf
        
        # Opciones de pdfkit
        options = {
            'page-size': 'A4',
            'margin-top': '20mm',
            'margin-right': '20mm',
            'margin-bottom': '20mm',
            'margin-left': '20mm',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None
        }
        
        # Generar PDF
        pdfkit.from_string(html_completo, str(ruta_pdf), options=options)
        print(f"✅ Generado: {ruta_pdf}")
        
    except Exception as e:
        print(f"❌ Error al convertir {archivo_md}: {e}")

def generar_pdf_completo():
    """Genera UN PDF con todos los módulos"""
    print("\nGenerando PDF completo del libro...")
    
    try:
        html_total = ""
        
        for archivo in ARCHIVOS:
            print(f"Agregando {archivo} al libro...")
            html = convertir_md_a_html(INPUT_DIR / archivo)
            html_total += html + '<div class="page-break"></div>\n'
        
        html_completo = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Documentación Técnica Completa - Proyecto ETL</title>
            {CSS_STYLE}
        </head>
        <body>
            {html_total}
        </body>
        </html>
        """
        
        ruta_pdf = OUTPUT_DIR / "LIBRO_COMPLETO_DOCUMENTACION_ETL.pdf"
        
        options = {
            'page-size': 'A4',
            'margin-top': '20mm',
            'margin-right': '20mm',
            'margin-bottom': '20mm',
            'margin-left': '20mm',
            'encoding': "UTF-8",
            'enable-local-file-access': None,
            'footer-center': '[page] de [topage]',
            'footer-font-size': '8',
        }
        
        pdfkit.from_string(html_completo, str(ruta_pdf), options=options)
        print(f"\n✅ LIBRO COMPLETO generado: {ruta_pdf}")
        
    except Exception as e:
        print(f"❌ Error al generar libro completo: {e}")

if __name__ == "__main__":
    print("=" * 80)
    print("CONVERSIÓN DE DOCUMENTACIÓN MARKDOWN A PDF")
    print("=" * 80)
    
    # Opción 1: PDFs individuales
    print("\n1. Generando PDFs individuales por módulo...")
    for archivo in ARCHIVOS:
        if (INPUT_DIR / archivo).exists():
            generar_pdf_individual(archivo)
        else:
            print(f"⚠️ Archivo no encontrado: {archivo}")
    
    # Opción 2: PDF completo (libro)
    print("\n" + "=" * 80)
    generar_pdf_completo()
    
    print("\n" + "=" * 80)
    print(f"✅ PROCESO COMPLETADO")
    print(f"📁 PDFs generados en: {OUTPUT_DIR}")
    print("=" * 80)
