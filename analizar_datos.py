#!/usr/bin/env python
"""
Script de visualización de datos del keylogger educativo.
Este script analiza los datos recopilados por el keylogger simple y genera visualizaciones
para fines educativos y de análisis.
"""

import os
import re
from datetime import datetime
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
import webbrowser  # Añadido para abrir automáticamente el reporte HTML


def load_text_log(file_path):
    """
    Carga un archivo de log de texto y extrae información estructurada.
    
    Args:
        file_path (str): Ruta al archivo de texto con logs
        
    Returns:
        list: Lista de entradas de log estructuradas
    """
    entries = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Extraer timestamp, ventana y contenido
                match = re.match(r'\[(.*?)\] \((.*?)\) (.*)', line)
                if match:
                    timestamp, window, content = match.groups()
                    entries.append({
                        'timestamp': timestamp,
                        'window': window,
                        'content': content.strip()
                    })
    except FileNotFoundError:
        print(f"Error: El archivo {file_path} no existe.")
    
    return entries


def analyze_window_activity(entries):
    """
    Analiza la actividad por ventana/aplicación.
    
    Args:
        entries (list): Lista de entradas de log estructuradas
        
    Returns:
        dict: Estadísticas de actividad por ventana
    """
    window_stats = defaultdict(lambda: {'count': 0, 'chars': 0})
    
    for entry in entries:
        window = entry['window']
        content = entry['content']
        
        window_stats[window]['count'] += 1
        window_stats[window]['chars'] += len(content)
    
    return dict(window_stats)


def analyze_keystroke_distribution(entries):
    """
    Analiza la distribución horaria de la actividad de escritura.
    
    Args:
        entries (list): Lista de entradas de log estructuradas
        
    Returns:
        dict: Actividad por hora del día
    """
    hourly_activity = defaultdict(int)
    
    for entry in entries:
        try:
            timestamp = entry['timestamp']
            dt = datetime.fromisoformat(timestamp)
            hour = dt.hour
            hourly_activity[hour] += len(entry['content'])
        except (ValueError, KeyError):
            pass  # Ignorar entradas con formato de tiempo incorrecto
    
    return dict(hourly_activity)


def analyze_content_metrics(entries):
    """
    Analiza métricas del contenido escrito.
    
    Args:
        entries (list): Lista de entradas de log estructuradas
        
    Returns:
        dict: Diversas métricas del contenido
    """
    all_content = " ".join([entry['content'] for entry in entries])
    
    # Contar palabras únicas
    words = re.findall(r'\b\w+\b', all_content.lower())
    word_counter = Counter(words)
    
    # Longitud promedio de entradas
    avg_length = sum([len(entry['content']) for entry in entries]) / len(entries) if entries else 0
    
    return {
        'total_chars': len(all_content),
        'total_words': len(words),
        'unique_words': len(word_counter),
        'avg_entry_length': avg_length,
        'most_common_words': word_counter.most_common(10)
    }


def generate_visualizations(window_stats, hourly_activity, content_metrics, output_dir="./out"):
    """
    Genera visualizaciones gráficas de los datos analizados.
    
    Args:
        window_stats (dict): Estadísticas por ventana
        hourly_activity (dict): Actividad por hora
        content_metrics (dict): Métricas del contenido
        output_dir (str): Directorio donde guardar los gráficos
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Gráfico de actividad por ventana
    if window_stats:
        plt.figure(figsize=(12, 6))
        windows = list(window_stats.keys())
        if len(windows) > 10:
            # Si hay más de 10 ventanas, mostrar solo las 10 más activas
            sorted_stats = sorted(window_stats.items(), key=lambda x: x[1]['chars'], reverse=True)
            windows = [item[0] for item in sorted_stats[:10]]
            counts = [window_stats[window]['chars'] for window in windows]
        else:
            counts = [stats['chars'] for stats in window_stats.values()]
        
        plt.barh(windows, counts)
        plt.xlabel('Caracteres escritos')
        plt.ylabel('Ventana/Aplicación')
        plt.title('Volumen de Escritura por Ventana')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'actividad_por_ventana.png'))
        print(f"Gráfico guardado: {os.path.join(output_dir, 'actividad_por_ventana.png')}")
        plt.close()
    
    # 2. Gráfico de actividad por hora
    if hourly_activity:
        plt.figure(figsize=(10, 6))
        hours = sorted(hourly_activity.keys())
        activity = [hourly_activity[hour] for hour in hours]
        
        plt.bar(hours, activity)
        plt.xlabel('Hora del día')
        plt.ylabel('Caracteres escritos')
        plt.title('Actividad de Escritura por Hora')
        plt.xticks(range(0, 24))
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'actividad_por_hora.png'))
        print(f"Gráfico guardado: {os.path.join(output_dir, 'actividad_por_hora.png')}")
        plt.close()
    
    # 3. Palabras más comunes
    if content_metrics and 'most_common_words' in content_metrics:
        plt.figure(figsize=(10, 6))
        words = [word for word, _ in content_metrics['most_common_words']]
        counts = [count for _, count in content_metrics['most_common_words']]
        
        plt.barh(words, counts)
        plt.xlabel('Frecuencia')
        plt.ylabel('Palabra')
        plt.title('Palabras Más Utilizadas')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'palabras_frecuentes.png'))
        print(f"Gráfico guardado: {os.path.join(output_dir, 'palabras_frecuentes.png')}")
        plt.close()


def generate_html_report(window_stats, hourly_activity, content_metrics, output_dir="./out"):
    """
    Genera un informe HTML con los resultados del análisis y lo guarda en el directorio de salida.
    
    Args:
        window_stats (dict): Estadísticas por ventana
        hourly_activity (dict): Actividad por hora
        content_metrics (dict): Métricas del contenido
        output_dir (str): Directorio donde guardar el informe HTML
    
    Returns:
        str: Ruta del archivo HTML generado
    """
    os.makedirs(output_dir, exist_ok=True)
    report_file = os.path.join(output_dir, 'reporte_keylogger.html')
    
    # Formatear datos para el HTML
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Preparar datos de ventanas más activas
    window_rows = ""
    if window_stats:
        sorted_windows = sorted(window_stats.items(), key=lambda x: x[1]['chars'], reverse=True)
        for i, (window, stats) in enumerate(sorted_windows[:10], 1):
            window_rows += f'''<tr>
                <td>{i}</td>
                <td>{window}</td>
                <td>{stats['count']}</td>
                <td>{stats['chars']}</td>
            </tr>'''
    
    # Preparar datos de palabras más comunes
    word_rows = ""
    if content_metrics and 'most_common_words' in content_metrics:
        for i, (word, count) in enumerate(content_metrics['most_common_words'][:10], 1):
            word_rows += f'''<tr>
                <td>{i}</td>
                <td>{word}</td>
                <td>{count}</td>
            </tr>'''
    
    # Crear el HTML
    html_content = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informe del Keylogger Educativo</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            color: #333;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1, h2 {{
            color: #2c3e50;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        .stats-container {{
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            margin-bottom: 20px;
        }}
        .stat-box {{
            background-color: #f8f9fa;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 15px;
            width: calc(25% - 15px);
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 5px;
            color: #3498db;
        }}
        .stat-label {{
            color: #7f8c8d;
            font-size: 14px;
        }}
        .chart-container {{
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            margin-top: 30px;
        }}
        .chart-item {{
            width: 100%;
            margin-bottom: 30px;
        }}
        .chart-item img {{
            width: 100%;
            border: 1px solid #ddd;
            border-radius: 3px;
        }}
        footer {{
            margin-top: 40px;
            text-align: center;
            color: #7f8c8d;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Informe de Análisis del Keylogger Educativo</h1>
        <p>Reporte generado el: {timestamp}</p>
        
        <h2>Resumen de Actividad</h2>
        <div class="stats-container">
            <div class="stat-box">
                <div class="stat-value">{sum(stats['count'] for stats in window_stats.values()) if window_stats else 0}</div>
                <div class="stat-label">Entradas registradas</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{content_metrics.get('total_chars', 0)}</div>
                <div class="stat-label">Caracteres totales</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{content_metrics.get('total_words', 0)}</div>
                <div class="stat-label">Palabras totales</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{len(window_stats) if window_stats else 0}</div>
                <div class="stat-label">Ventanas detectadas</div>
            </div>
        </div>
        
        <h2>Aplicaciones/Ventanas Más Activas</h2>
        <table>
            <tr>
                <th>#</th>
                <th>Ventana</th>
                <th>Entradas</th>
                <th>Caracteres</th>
            </tr>
            {window_rows}
        </table>
        
        <h2>Palabras Más Utilizadas</h2>
        <table>
            <tr>
                <th>#</th>
                <th>Palabra</th>
                <th>Frecuencia</th>
            </tr>
            {word_rows}
        </table>
        
        <h2>Visualizaciones</h2>
        <div class="chart-container">
            <div class="chart-item">
                <h3>Actividad por Ventana</h3>
                <img src="actividad_por_ventana.png" alt="Gráfico de actividad por ventana">
            </div>
            <div class="chart-item">
                <h3>Distribución Horaria</h3>
                <img src="actividad_por_hora.png" alt="Gráfico de distribución horaria">
            </div>
            <div class="chart-item">
                <h3>Palabras Más Frecuentes</h3>
                <img src="palabras_frecuentes.png" alt="Gráfico de palabras frecuentes">
            </div>
        </div>
        
        <footer>
            <p>Desarrollado por Erick Lasluisa - 2025</p>
        </footer>
    </div>
</body>
</html>
'''
    
    # Guardar el HTML a un archivo
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Informe HTML guardado en: {report_file}")
    return report_file


def print_report(window_stats, hourly_activity, content_metrics):
    """
    Imprime un informe con los resultados del análisis.
    
    Args:
        window_stats (dict): Estadísticas por ventana
        hourly_activity (dict): Actividad por hora
        content_metrics (dict): Métricas del contenido
    """
    print("\n" + "=" * 50)
    print(" INFORME DE ANÁLISIS DEL KEYLOGGER EDUCATIVO ")
    print("=" * 50)
    
    # 1. Resumen de actividad
    print("\n--- RESUMEN DE ACTIVIDAD ---")
    total_entries = sum(stats['count'] for stats in window_stats.values()) if window_stats else 0
    total_chars = content_metrics.get('total_chars', 0)
    total_words = content_metrics.get('total_words', 0)
    print(f"Total de entradas registradas: {total_entries}")
    print(f"Total de caracteres escritos: {total_chars}")
    print(f"Total de palabras escritas: {total_words}")
    print(f"Aplicaciones/Ventanas detectadas: {len(window_stats) if window_stats else 0}")
    
    # 2. Top ventanas más activas
    if window_stats:
        print("\n--- TOP VENTANAS MÁS ACTIVAS ---")
        sorted_windows = sorted(window_stats.items(), key=lambda x: x[1]['chars'], reverse=True)
        for i, (window, stats) in enumerate(sorted_windows[:5], 1):
            print(f"{i}. {window}: {stats['count']} entradas, {stats['chars']} caracteres")
    
    # 3. Distribución temporal
    if hourly_activity:
        print("\n--- DISTRIBUCIÓN HORARIA ---")
        most_active_hour = max(hourly_activity.items(), key=lambda x: x[1])
        print(f"Hora más activa: {most_active_hour[0]}:00 ({most_active_hour[1]} caracteres)")
        print("Top 3 horas con mayor actividad:")
        sorted_activity = sorted(hourly_activity.items(), key=lambda x: x[1], reverse=True)
        for i, (hour, activity) in enumerate(sorted_activity[:3], 1):
            print(f"{i}. {hour}:00 - {activity} caracteres")
    
    # 4. Análisis de contenido
    if content_metrics:
        print("\n--- ANÁLISIS DE CONTENIDO ---")
        print(f"Longitud promedio de entrada: {content_metrics.get('avg_entry_length', 0):.2f} caracteres")
        print(f"Palabras únicas utilizadas: {content_metrics.get('unique_words', 0)}")
        
        if 'most_common_words' in content_metrics:
            print("\n--- PALABRAS MÁS UTILIZADAS ---")
            for i, (word, count) in enumerate(content_metrics['most_common_words'][:5], 1):
                print(f"{i}. '{word}': {count} veces")
    
    print("\n" + "=" * 50)
    print(" VISUALIZACIONES GUARDADAS EN EL DIRECTORIO './out' ")
    print("=" * 50 + "\n")


def main():
    print("Analizador de Datos del Keylogger Educativo")
    print("===========================================")
    
    # Verificar existencia de archivos
    text_log_path = "./out/key_log.txt"
    
    if not os.path.exists(text_log_path):
        if os.path.exists("./out"):
            files = [f for f in os.listdir("./out") if f.endswith(".txt")]
            if files:
                text_log_path = os.path.join("./out", files[0])
                print(f"Usando archivo alternativo: {text_log_path}")
            else:
                print("Error: No se encontraron archivos de log para analizar.")
                print("Ejecute primero el keylogger para generar registros.")
                return
        else:
            print("Error: No se encontró el directorio out/ con logs para analizar.")
            print("Ejecute primero el keylogger para generar registros.")
            return
    
    # Cargar datos
    print(f"Cargando datos de texto desde {text_log_path}...")
    entries = load_text_log(text_log_path)
    print(f"  - {len(entries)} entradas cargadas")
    
    if not entries:
        print("No se encontraron entradas para analizar.")
        return
    
    # Analizar datos
    print("\nAnalizando patrones de uso por ventana...")
    window_stats = analyze_window_activity(entries)
    
    print("Analizando distribución horaria de actividad...")
    hourly_activity = analyze_keystroke_distribution(entries)
    
    print("Analizando métricas de contenido...")
    content_metrics = analyze_content_metrics(entries)
    
    # Generar visualizaciones
    print("\nGenerando visualizaciones...")
    generate_visualizations(window_stats, hourly_activity, content_metrics)
    
    # Imprimir informe
    print_report(window_stats, hourly_activity, content_metrics)
    
    # Generar informe HTML
    print("\nGenerando informe HTML...")
    html_report = generate_html_report(window_stats, hourly_activity, content_metrics)
    
    # Preguntar si quiere abrir el informe HTML
    open_browser = input("\n¿Desea abrir el informe HTML en su navegador? (s/n): ").lower() == 's'
    if open_browser:
        print(f"Abriendo informe en el navegador: {html_report}")
        webbrowser.open('file://' + os.path.abspath(html_report))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAnálisis interrumpido por el usuario.")
    except Exception as e:
        print(f"\nError durante el análisis: {str(e)}")
    finally:
        input("\nPresione Enter para salir...")
