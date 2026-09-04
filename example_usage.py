"""
Ejemplos de uso para análisis de estereotipos de género en mangas.
"""

from image_processor import MangaGenderStereotypeAnalyzer
import json
import os


def analizar_manga_individual():
    """Analizar un manga individual."""
    print("\n🎨 ANÁLISIS INDIVIDUAL DE MANGA\n")
    
    manga_path = "manga_ejemplo.jpg"
    manga_title = "Titulo del Manga"
    
    if not os.path.exists(manga_path):
        print(f"⚠️  Archivo no encontrado: {manga_path}")
        return
    
    # Crear analizador
    analyzer = MangaGenderStereotypeAnalyzer(manga_path, manga_title)
    
    # Realizar análisis
    results = analyzer.analyze_all()
    
    # Mostrar resultados principales
    print(f"Manga: {manga_title}")
    print(f"Nivel de Estereotipo: {results['stereotype_descriptor']}")
    print(f"Segmento Demográfico: {results['demographic_label']}")
    print(f"Sexualización Promedio: {results['sexualization']['total_sexualization']:.2f}/3")


def analizar_sexualizacion_detallada():
    """Análisis detallado de sexualización."""
    print("\n👗 ANÁLISIS DETALLADO DE SEXUALIZACIÓN\n")
    
    manga_path = "manga_ejemplo.jpg"
    
    if not os.path.exists(manga_path):
        print(f"⚠️  Archivo no encontrado: {manga_path}")
        return
    
    analyzer = MangaGenderStereotypeAnalyzer(manga_path)
    
    # Analizar cada aspecto de sexualización
    vestimenta = analyzer.analyze_revealing_clothing()
    poses = analyzer.analyze_suggestive_poses()
    enfoque = analyzer.analyze_body_part_focus()
    
    sexualization_labels = {
        0: "Ausente",
        1: "Bajo",
        2: "Medio",
        3: "Alto"
    }
    
    print(f"VI1.1 - Vestimenta Reveladora: {vestimenta} ({sexualization_labels[vestimenta]})")
    print(f"VI1.2 - Poses Sugerentes: {poses} ({sexualization_labels[poses]})")
    print(f"VI1.3 - Enfoque en Partes del Cuerpo: {enfoque} ({sexualization_labels[enfoque]})")
    print(f"\nPromedio de Sexualización: {(vestimenta + poses + enfoque) / 3:.2f}/3")


def analizar_caracteristicas_esteticas():
    """Análisis de características estéticas."""
    print("\n✨ ANÁLISIS DE CARACTERÍSTICAS ESTÉTICAS\n")
    
    manga_path = "manga_ejemplo.jpg"
    
    if not os.path.exists(manga_path):
        print(f"⚠️  Archivo no encontrado: {manga_path}")
        return
    
    analyzer = MangaGenderStereotypeAnalyzer(manga_path)
    
    codigo, detalles = analyzer.analyze_aesthetic_characteristics()
    
    aesthetic_labels = {
        0: "Baja",
        1: "Medio-baja",
        2: "Medio-alta",
        3: "Alta"
    }
    
    print(f"Nivel de Presencia Estética: {codigo} ({aesthetic_labels[codigo]})")
    print(f"Características Femeninas: {detalles.get('femeninas', 0)}")
    print(f"Características Masculinas: {detalles.get('masculinas', 0)}")


def comparar_multiples_mangas():
    """Comparar estereotipos entre múltiples mangas."""
    print("\n📊 COMPARACIÓN DE MÚLTIPLES MANGAS\n")
    
    mangas = [
        ("manga1.jpg", "Manga A"),
        ("manga2.jpg", "Manga B"),
        ("manga3.jpg", "Manga C"),
    ]
    
    resultados = []
    
    for ruta, titulo in mangas:
        if not os.path.exists(ruta):
            print(f"⚠️  {titulo} no encontrado")
            continue
        
        try:
            analyzer = MangaGenderStereotypeAnalyzer(ruta, titulo)
            results = analyzer.analyze_all()
            
            resultados.append({
                'titulo': titulo,
                'estereotipo_codigo': results['gender_stereotype_internalization'],
                'estereotipo_label': results['stereotype_descriptor'],
                'sexualizacion': results['sexualization']['total_sexualization'],
                'demografico': results['demographic_label']
            })
            
            print(f"✓ {titulo} analizado")
        
        except Exception as e:
            print(f"✗ Error en {titulo}: {str(e)}")
    
    # Mostrar tabla comparativa
    if resultados:
        print("\n" + "="*100)
        print("TABLA COMPARATIVA")
        print("="*100)
        print(f"{'Manga':<15} | {'Estereotipo':<5} | {'Sexualización':<12} | {'Segmento':<20}")
        print("-"*100)
        
        for r in resultados:
            print(f"{r['titulo']:<15} | {r['estereotipo_codigo']:<5} | {r['sexualizacion']:<12.2f} | {r['demografico']:<20}")


def generar_reporte_batch():
    """Generar reportes para múltiples mangas."""
    print("\n📝 PROCESAMIENTO POR LOTES\n")
    
    directorio = "./mangas/"
    
    if not os.path.exists(directorio):
        print(f"⚠️  Directorio no encontrado: {directorio}")
        return
    
    extensiones = ('.jpg', '.jpeg', '.png')
    
    for archivo in os.listdir(directorio):
        if archivo.lower().endswith(extensiones):
            ruta = os.path.join(directorio, archivo)
            
            try:
                analyzer = MangaGenderStereotypeAnalyzer(ruta, archivo)
                results = analyzer.analyze_all()
                
                # Generar reporte
                reporte_output = f"reportes/{archivo}_reporte.txt"
                os.makedirs("reportes", exist_ok=True)
                analyzer.generate_analysis_report(reporte_output)
                
                # Generar visualización
                visual_output = f"reportes/{archivo}_analisis.png"
                analyzer.visualize_analysis(visual_output)
                
                print(f"✓ {archivo}: Estereotipo {results['gender_stereotype_internalization']}/3")
            
            except Exception as e:
                print(f"✗ {archivo}: {str(e)}")


def exportar_resultados_json():
    """Exportar resultados en formato JSON."""
    print("\n💾 EXPORTAR RESULTADOS EN JSON\n")
    
    manga_path = "manga_ejemplo.jpg"
    manga_title = "Manga de Prueba"
    
    if not os.path.exists(manga_path):
        print(f"⚠️  Archivo no encontrado")
        return
    
    analyzer = MangaGenderStereotypeAnalyzer(manga_path, manga_title)
    results = analyzer.analyze_all()
    
    # Exportar JSON
    with open("analisis_resultado.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("✓ Resultados exportados a: analisis_resultado.json")
    print(json.dumps(results, indent=2, ensure_ascii=False))


def menu_interactivo():
    """Menú interactivo."""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║  ANÁLISIS DE ESTEREOTIPOS DE GÉNERO EN MANGAS             ║
    ║                                                            ║
    ║  Variables analizadas:                                    ║
    ║  - VI1: Nivel de Sexualización                           ��
    ║  - VI2: Presencia Estética                               ║
    ║  - VI3: Segmentación de Mercado                          ║
    ║  - Variable Dependiente: Internalización de Estereotipo  ║
    ╚════════════════════════════════════════════════════════════╝
    
    1. Analizar manga individual
    2. Análisis detallado de sexualización
    3. Análisis de características estéticas
    4. Comparar múltiples mangas
    5. Generar reportes por lotes
    6. Exportar resultados en JSON
    7. Salir
    """)
    
    opciones = {
        '1': analizar_manga_individual,
        '2': analizar_sexualizacion_detallada,
        '3': analizar_caracteristicas_esteticas,
        '4': comparar_multiples_mangas,
        '5': generar_reporte_batch,
        '6': exportar_resultados_json,
    }
    
    while True:
        opcion = input("\nSelecciona una opción (1-7): ").strip()
        
        if opcion == '7':
            print("¡Hasta luego! 👋")
            break
        elif opcion in opciones:
            try:
                opciones[opcion]()
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        else:
            print("⚠️  Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    menu_interactivo()
