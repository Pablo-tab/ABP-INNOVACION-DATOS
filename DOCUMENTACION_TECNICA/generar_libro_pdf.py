"""
╔══════════════════════════════════════════════════════════════════════════════╗
║   GENERADOR DE PDF PROFESIONAL PARA DOCUMENTACIÓN TÉCNICA                   ║
║   Proyecto: ETL TSCDIA 2025                                                  ║
║   Autor: Pablo Tab                                                           ║
║   Fecha: 8 de noviembre de 2025                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

Este script convierte archivos Markdown (.md) a PDFs hermosos con formato de libro.

REQUISITOS:
    pip install markdown weasyprint pygments

USO:
    python generar_libro_pdf.py

SALIDA:
    - PDFs individuales por módulo
    - UN PDF completo con todos los módulos (LIBRO_COMPLETO.pdf)
"""

import os
from pathlib import Path
from datetime import datetime

# Intentar importar bibliotecas necesarias
try:
    import markdown
    from weasyprint import HTML, CSS
    from pygments.formatters import HtmlFormatter
    LIBS_OK = True
except ImportError as e:
    LIBS_OK = False
    print("❌ ERROR: Faltan bibliotecas requeridas")
    print(f"\nDetalles: {e}")
    print("\n📦 SOLUCIÓN: Instala las dependencias con:")
    print("   pip install markdown weasyprint pygments")
    print("\n💡 Si tienes problemas con weasyprint en Windows:")
    print("   1. Descarga GTK3: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases")
    print("   2. Instala GTK3")
    print("   3. Ejecuta: pip install weasyprint")
    input("\nPresiona Enter para salir...")
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

# CSS PROFESIONAL para el PDF
CSS_PROFESIONAL = """
@page {
    size: A4;
    margin: 2.5cm 2cm 2.5cm 2cm;
    
    @bottom-center {
        content: "Página " counter(page) " de " counter(pages);
        font-size: 9pt;
        color: #666;
    }
    
    @bottom-right {
        content: "Pablo Tab - @Pablo-Tab";
        font-size: 8pt;
        color: #999;
    }
    
    @top-center {
        content: "📊 Documentación Técnica - Proyecto ETL TSCDIA 2025";
        font-size: 9pt;
        color: #3498db;
        font-weight: bold;
        border-bottom: 1px solid #ddd;
        padding-bottom: 5px;
    }
}

/* Tipografía base */
body {
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.7;
    color: #2c3e50;
    hyphens: auto;
}

/* Títulos con estilo */
h1 {
    color: #1a1a1a;
    font-size: 26pt;
    font-weight: 700;
    border-bottom: 4px solid #3498db;
    padding-bottom: 15px;
    margin-top: 40px;
    margin-bottom: 25px;
    page-break-before: always;
    page-break-after: avoid;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 20px;
    border-radius: 8px;
}

h1:first-of-type {
    page-break-before: avoid;
}

h1::before {
    content: "📘 ";
    font-size: 28pt;
}

h2 {
    color: #2c3e50;
    font-size: 18pt;
    font-weight: 600;
    border-bottom: 2px solid #95a5a6;
    padding-bottom: 10px;
    margin-top: 30px;
    margin-bottom: 18px;
    page-break-after: avoid;
}

h2::before {
    content: "📋 ";
    color: #3498db;
}

h3 {
    color: #34495e;
    font-size: 14pt;
    font-weight: 600;
    margin-top: 22px;
    margin-bottom: 12px;
    page-break-after: avoid;
}

h3::before {
    content: "▸ ";
    color: #3498db;
}

h4 {
    color: #555;
    font-size: 12pt;
    font-weight: 600;
    margin-top: 18px;
    margin-bottom: 10px;
}

/* Párrafos */
p {
    margin: 10px 0;
    text-align: justify;
    orphans: 3;
    widows: 3;
}

/* Listas mejoradas */
ul, ol {
    margin: 12px 0;
    padding-left: 25px;
}

li {
    margin: 8px 0;
    line-height: 1.6;
}

ul li::marker {
    color: #3498db;
    font-weight: bold;
}

/* Código inline */
code {
    background-color: #fff5f5;
    color: #c7254e;
    padding: 3px 7px;
    border-radius: 4px;
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    font-size: 10pt;
    border: 1px solid #ffe0e0;
}

/* Bloques de código */
pre {
    background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
    color: #f8f8f2;
    padding: 18px;
    border-radius: 8px;
    overflow-x: auto;
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    font-size: 9pt;
    line-height: 1.5;
    margin: 18px 0;
    border-left: 5px solid #3498db;
    box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    page-break-inside: avoid;
}

pre code {
    background-color: transparent;
    padding: 0;
    color: #f8f8f2;
    border: none;
}

/* Tablas profesionales */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
    font-size: 10pt;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    page-break-inside: avoid;
}

thead {
    background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
    color: white;
}

th {
    padding: 12px;
    text-align: left;
    font-weight: 600;
    border: 1px solid #2980b9;
}

td {
    padding: 10px 12px;
    border: 1px solid #ddd;
}

tr:nth-child(even) {
    background-color: #f8f9fa;
}

/* Citas */
blockquote {
    border-left: 5px solid #3498db;
    padding: 12px 18px;
    margin: 18px 0;
    background-color: #ecf0f1;
    color: #34495e;
    font-style: italic;
    border-radius: 0 5px 5px 0;
    page-break-inside: avoid;
}

/* Separadores */
hr {
    border: none;
    height: 2px;
    background: linear-gradient(to right, transparent, #3498db, transparent);
    margin: 30px 0;
}

/* Enlaces */
a {
    color: #3498db;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

/* Checkmarks */
.task-list-item {
    list-style-type: none;
}

/* Evitar saltos de página indeseados */
.no-break {
    page-break-inside: avoid;
}

/* Portada especial */
.portada {
    text-align: center;
    padding: 150px 30px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 15px;
    margin-bottom: 50px;
    page-break-after: always;
}

.portada h1 {
    font-size: 32pt;
    border: none;
    color: white;
    margin: 20px 0;
    background: none;
}

.portada p {
    font-size: 14pt;
    margin: 15px 0;
}

/* Emojis */
.emoji {
    font-size: 1.2em;
}
"""

def generar_portada():
    """Genera HTML de portada hermosa"""
    fecha = datetime.now().strftime("%d de %B de %Y")
    
    return f"""
    <div class="portada">
        <h1>📊 DOCUMENTACIÓN TÉCNICA COMPLETA</h1>
        <h2 style="color: white; border: none; font-size: 24pt; margin: 30px 0;">
            Proyecto ETL<br/>
            Entidad Financiera
        </h2>
        <p style="font-size: 16pt; margin-top: 40px;">
            <strong>Curso:</strong> Tratamiento y Seguridad de los Datos<br/>
            en Ingeniería Aplicada (TSCDIA)
        </p>
        <p style="font-size: 16pt;">
            <strong>Institución:</strong> Tecnicatura Superior en<br/>
            Ciencia de Datos e Inteligencia Artificial
        </p>
        <p style="font-size: 16pt; margin-top: 40px;">
            <strong>Autor:</strong> Pablo Tab<br/>
            <strong>GitHub:</strong> @Pablo-Tab
        </p>
        <p style="font-size: 14pt; margin-top: 50px; opacity: 0.9;">
            {fecha}
        </p>
        <p style="font-size: 12pt; margin-top: 30px; opacity: 0.8;">
            🔗 https://github.com/Pablo-Tab/ABP-INNOVACION-DATOS
        </p>
    </div>
    """

def convertir_md_a_html(archivo_md):
    """Convierte archivo Markdown a HTML con extensiones"""
    try:
        with open(archivo_md, 'r', encoding='utf-8') as f:
            contenido_md = f.read()
        
        # Convertir Markdown a HTML con extensiones
        html = markdown.markdown(
            contenido_md,
            extensions=[
                'fenced_code',
                'tables',
                'nl2br',
                'codehilite',
                'toc',
                'sane_lists',
                'smarty'
            ],
            extension_configs={
                'codehilite': {
                    'css_class': 'highlight',
                    'linenums': False
                }
            }
        )
        
        return html
    
    except Exception as e:
        print(f"❌ Error al leer {archivo_md}: {e}")
        return ""

def generar_pdf_individual(archivo_md):
    """Genera PDF individual para cada módulo"""
    print(f"📄 Convirtiendo {archivo_md}...")
    
    try:
        html_contenido = convertir_md_a_html(INPUT_DIR / archivo_md)
        
        if not html_contenido:
            print(f"⚠️ Archivo vacío o con errores: {archivo_md}")
            return
        
        # HTML completo con estilo
        html_completo = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>{archivo_md.replace('.md', '')}</title>
            <style>{CSS_PROFESIONAL}</style>
        </head>
        <body>
            {html_contenido}
        </body>
        </html>
        """
        
        # Nombre del PDF de salida
        nombre_pdf = archivo_md.replace('.md', '.pdf')
        ruta_pdf = OUTPUT_DIR / nombre_pdf
        
        # Generar PDF con WeasyPrint
        HTML(string=html_completo).write_pdf(ruta_pdf)
        
        tamaño_mb = ruta_pdf.stat().st_size / (1024 * 1024)
        print(f"   ✅ Generado: {ruta_pdf.name} ({tamaño_mb:.2f} MB)")
        
    except Exception as e:
        print(f"   ❌ Error al convertir {archivo_md}: {e}")

def generar_libro_completo():
    """Genera UN PDF completo con TODOS los módulos"""
    print("\n" + "="*80)
    print("📚 GENERANDO LIBRO COMPLETO...")
    print("="*80)
    
    try:
        # Generar portada
        html_total = generar_portada()
        
        # Agregar cada módulo
        for i, archivo in enumerate(ARCHIVOS, 1):
            ruta_archivo = INPUT_DIR / archivo
            
            if not ruta_archivo.exists():
                print(f"⚠️ Archivo no encontrado: {archivo}")
                continue
            
            print(f"   📖 Agregando módulo {i}/8: {archivo}")
            html_contenido = convertir_md_a_html(ruta_archivo)
            html_total += html_contenido
            
            # Agregar salto de página después de cada módulo (excepto el último)
            if i < len(ARCHIVOS):
                html_total += '<div style="page-break-after: always;"></div>'
        
        # HTML completo del libro
        html_completo = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Documentación Técnica Completa - Proyecto ETL TSCDIA 2025</title>
            <style>{CSS_PROFESIONAL}</style>
        </head>
        <body>
            {html_total}
        </body>
        </html>
        """
        
        # Guardar HTML temporal (útil para debug)
        html_temp = OUTPUT_DIR / "libro_completo.html"
        with open(html_temp, 'w', encoding='utf-8') as f:
            f.write(html_completo)
        print(f"\n   💾 HTML temporal guardado: {html_temp.name}")
        
        # Generar PDF
        ruta_pdf = OUTPUT_DIR / "LIBRO_COMPLETO_DOCUMENTACION_ETL.pdf"
        print(f"\n   🔨 Generando PDF... (esto puede tomar 1-2 minutos)")
        
        HTML(string=html_completo).write_pdf(ruta_pdf)
        
        tamaño_mb = ruta_pdf.stat().st_size / (1024 * 1024)
        
        print("\n" + "="*80)
        print(f"✅ ¡LIBRO COMPLETO GENERADO CON ÉXITO!")
        print(f"📚 Archivo: {ruta_pdf.name}")
        print(f"📊 Tamaño: {tamaño_mb:.2f} MB")
        print(f"📄 Páginas: ~100-120 páginas")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ ERROR al generar libro completo: {e}")
        print("\n💡 Sugerencias:")
        print("   1. Verifica que todos los archivos .md existan")
        print("   2. Verifica que WeasyPrint esté instalado correctamente")
        print("   3. Revisa el HTML temporal para identificar problemas")

def main():
    """Función principal"""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*20 + "GENERADOR DE PDF PROFESIONAL" + " "*30 + "║")
    print("║" + " "*78 + "║")
    print("║" + "  Proyecto: ETL TSCDIA 2025" + " "*51 + "║")
    print("║" + "  Autor: Pablo Tab" + " "*61 + "║")
    print("╚" + "="*78 + "╝\n")
    
    if not LIBS_OK:
        return
    
    # Verificar que existan los archivos
    archivos_encontrados = sum(1 for a in ARCHIVOS if (INPUT_DIR / a).exists())
    print(f"📂 Directorio de entrada: {INPUT_DIR}")
    print(f"📂 Directorio de salida: {OUTPUT_DIR}")
    print(f"📝 Archivos encontrados: {archivos_encontrados}/{len(ARCHIVOS)}\n")
    
    if archivos_encontrados == 0:
        print("❌ No se encontraron archivos .md para convertir")
        return
    
    # Preguntar qué desea generar
    print("¿Qué deseas generar?")
    print("  1. PDFs individuales por módulo")
    print("  2. Libro completo (UN PDF con todos los módulos)")
    print("  3. Ambos (recomendado)")
    print()
    
    opcion = input("Selecciona opción (1/2/3) [3]: ").strip() or "3"
    
    print("\n" + "="*80)
    
    # Generar según opción
    if opcion in ["1", "3"]:
        print("📄 GENERANDO PDFs INDIVIDUALES...")
        print("="*80 + "\n")
        
        for archivo in ARCHIVOS:
            if (INPUT_DIR / archivo).exists():
                generar_pdf_individual(archivo)
            else:
                print(f"⚠️ Omitiendo: {archivo} (no encontrado)")
        
        print(f"\n✅ PDFs individuales completados")
    
    if opcion in ["2", "3"]:
        generar_libro_completo()
    
    # Resumen final
    print("\n" + "="*80)
    print("📊 RESUMEN:")
    archivos_pdf = list(OUTPUT_DIR.glob("*.pdf"))
    print(f"   📚 PDFs generados: {len(archivos_pdf)}")
    print(f"   📁 Ubicación: {OUTPUT_DIR}")
    print(f"   💾 Tamaño total: {sum(f.stat().st_size for f in archivos_pdf) / (1024*1024):.2f} MB")
    print("="*80)
    
    print("\n✨ ¡PROCESO COMPLETADO CON ÉXITO!")
    print("\n💡 SIGUIENTES PASOS:")
    print("   1. Abre el archivo LIBRO_COMPLETO_DOCUMENTACION_ETL.pdf")
    print("   2. Revisa el formato y contenido")
    print("   3. ¡Comparte la documentación con tus compañeros!")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
    finally:
        input("\nPresiona Enter para salir...")
