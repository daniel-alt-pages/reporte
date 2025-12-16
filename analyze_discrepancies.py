import csv
import unicodedata
from collections import Counter

# 1. Base de Datos Madre (Lista Completa proporcionada)
raw_madre_t_ext = """
IETAC | XIMENA ARIAS MANCO
IETAC | CAMILO ANDRÉS ARROYO CASTRO
IETAC | MARÍA ESTHER ACOSTA FERIA
IETAC | JAIRO MANUEL BALTAZAR VILLERO
IETAC | JHOANS SEBASTIÁN DURANGO ZABALA
IETAC | ELICEO ELI FUENTES DÍAZ
IETAC | LIZ VALERIA GIL HOYOS
IETAC | HAROLD IVÁN HOYOS VERGARA
IETAC | ISABELLA MANCHEGO LOZANO
IETAC | MARÍA ANGÉLICA MORELO VILLEROS
IETAC | HERNÁN ANDRÉS PALMERA PÉREZ
IETAC | ADRIANA LUCÍA ROJAS CORDERO
IETAC | JOHAN ANDRÉS SALCEDO BEDOYA
IETAC | ARNEDIS SIBAJA BEGAMBRE
IETAC | ALEXANDRA URZOLA MARTÍNEZ
IETAC | DANIEL ANDRÉS ZABALA MONTIEL
IETAC | LUIS MARIO ZABALA SÁNCHEZ
IETAC | RONALDO ANDRÉS ZULETA GUERRA
IETAC | KAREN SOFÍA ARRIETA VERGARA
IETAC | ANA BELÉN BARÓN CEBALLOS
IETAC | KAREN DAYANA CASTILLO PÉREZ
IETAC | JUAN DAVID CORREA HERNÁNDEZ
IETAC | LUIS DANIEL MENDOZA URIBE
IETAC | ALEXANDRA JULIO ROMERO
IETAC | YULISA RODRÍGUEZ RODRÍGUEZ
IETAC | VIVIANA MARCELA ROMERO ZÚÑIGA
IETAC | DAINER ANDRÉS SÁNCHEZ CASTRO
IETAC | MARIANA DE JESÚS CABADIA PARRA
IETAC | JANER CASTRO MONTALVO
IETAC | DAVIER ESTEBAN OTERO URANGO
IETAC | ELIANA MARCELA VERGARA GANDIA
IETAC | LUISA FERNANDA BARÓN LUCAS
IETAC | JORGE ANDRÉS PÉREZ MESTRA
IETAC | YULEIMIS MURILLO GÓMEZ
IETAC | NICOL TATIANA CERPA PEINADO
IETAC | DAYANA MICHEL PEÑA TORDECILLA
"""

def normalize(text):
    if not text: return ""
    # Quitar prefijo IETAC | si existe y espacios
    text = text.replace('IETAC |', '').strip().upper()
    # Quitar tildes para comparación (opcional, pero recomendado para evitar errores por 'María' vs 'Maria')
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

# Procesar Lista Madre
madre_names = []
for line in raw_madre_t_ext.strip().split('\n'):
    if line.strip():
        madre_names.append(normalize(line))

print(f"--- ANÁLISIS DE DISCREPANCIAS ---\n")
print(f"Total estudiantes en Lista Madre (Esperados): {len(madre_names)}")

# 2. Leer CSV de la Plataforma
csv_path = 'c:/Users/Daniel/Downloads/reporte/estudiantes_16-12-2025 (1).csv'
platform_students = []
platform_names_normalized = []

try:
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            # Filtrar solo IETAC para ser justos en la comparación
            inst = row.get('Institución', '').upper()
            if 'IETAC' in inst:
                raw_name = row.get('Nombre', '').strip()
                norm_name = normalize(raw_name)
                
                platform_students.append({
                    'original': raw_name,
                    'normalized': norm_name,
                    'id': row.get('Número Documento')
                })
                platform_names_normalized.append(norm_name)

    print(f"Total estudiantes IETAC en Plataforma (CSV): {len(platform_students)}")
    
    # 3. Análisis
    
    # A. Duplicados en Plataforma
    print(f"\n[1] DUPLICADOS EN PLATAFORMA:")
    counts = Counter(platform_names_normalized)
    duplicates = [name for name, count in counts.items() if count > 1]
    
    if duplicates:
        for name in duplicates:
            print(f"  ❌ {name} aparece {counts[name]} veces.")
    else:
        print("  ✅ No se encontraron duplicados por nombre.")

    # B. Faltantes (Están en Madre pero NO en Plataforma)
    print(f"\n[2] FALTANTES EN PLATAFORMA (NO REGISTRADOS):")
    missing_count = 0
    for m_name in madre_names:
        if m_name not in platform_names_normalized:
            print(f"  ⚠️  FALTA: {m_name}")
            missing_count += 1
    
    if missing_count == 0:
        print("  ✅ Todos los estudiantes de la lista madre están en la plataforma.")
    else:
        print(f"  Total faltantes: {missing_count}")

    # C. Sobrantes (Están en Plataforma pero NO en Madre - ¿Alumnos nuevos o errores?)
    print(f"\n[3] EXTRAS EN PLATAFORMA (NO ESTABAN EN LISTA MADRE):")
    extra_count = 0
    for p_name in platform_names_normalized:
        if p_name not in madre_names:
            print(f"  ℹ️  EXTRA: {p_name}")
            extra_count += 1
            
    if extra_count == 0:
        print("  ✅ No hay estudiantes extra.")

except Exception as e:
    print(f"Error al leer el archivo CSV: {e}")
