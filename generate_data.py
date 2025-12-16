import csv
import json
import os
import unicodedata
from difflib import SequenceMatcher
from collections import Counter

# 1. Base de Datos Madre
madre_db_text = """
IETAC | XIMENA ARIAS MANCO	Mujer	3213841433	13/11/2009
IETAC | CAMILO ANDRÉS ARROYO CASTRO	Hombre	3235647879	05/04/2010
IETAC | MARÍA ESTHER ACOSTA FERIA	Mujer	3105118499	24/10/2009
IETAC | JAIRO MANUEL BALTAZAR VILLERO	Hombre	3146676105	11/10/2009
IETAC | JHOANS SEBASTIÁN DURANGO ZABALA	Hombre	3137974214	20/10/2009
IETAC | ELICEO ELI FUENTES DÍAZ	Hombre	3217064315	19/08/2009
IETAC | LIZ VALERIA GIL HOYOS	Mujer	3234030521	18/10/2009
IETAC | HAROLD IVÁN HOYOS VERGARA	Hombre	3122860764	19/03/2008
IETAC | ISABELLA MANCHEGO LOZANO	Mujer	3206191655	08/05/2010
IETAC | MARÍA ANGÉLICA MORELO VILLEROS	Mujer	3234365594	13/08/2007
IETAC | HERNÁN ANDRÉS PALMERA PÉREZ	Hombre	3234839571	02/06/2007
IETAC | ADRIANA LUCÍA ROJAS CORDERO	Mujer	3148090148	04/03/2010
IETAC | JOHAN ANDRÉS SALCEDO BEDOYA	Hombre	3204750293	10/10/2010
IETAC | ARNEDIS SIBAJA BEGAMBRE	Mujer	3107241623	14/10/2009
IETAC | ALEXANDRA URZOLA MARTÍNEZ	Mujer	3235640423	23/03/2009
IETAC | DANIEL ANDRÉS ZABALA MONTIEL	Hombre	3128989638	04/03/2010
IETAC | LUIS MARIO ZABALA SÁNCHEZ	Hombre	3114262393	10/04/2010
IETAC | RONALDO ANDRÉS ZULETA GUERRA	Hombre	3127038167	07/04/2010
IETAC | KAREN SOFÍA ARRIETA VERGARA	Mujer	3104004760	07/09/2010
IETAC | ANA BELÉN BARÓN CEBALLOS	Mujer	3133984933	01/03/2010
IETAC | KAREN DAYANA CASTILLO PÉREZ	Mujer	3148177142	17/04/2010
IETAC | JUAN DAVID CORREA HERNÁNDEZ	Hombre	3217229477	30/09/2007
IETAC | LUIS DANIEL MENDOZA URIBE	Hombre	3105074210	11/02/2009
IETAC | ALEXANDRA JULIO ROMERO	Mujer	3216335419	10/02/2010
IETAC | YULISA RODRÍGUEZ RODRÍGUEZ	Mujer	3237650952	10/09/2009
IETAC | VIVIANA MARCELA ROMERO ZÚÑIGA	Mujer	3108218930	16/01/2010
IETAC | DAINER ANDRÉS SÁNCHEZ CASTRO	Hombre	3145180611	19/06/2009
IETAC | MARIANA DE JESÚS CABADIA PARRA	Mujer	3148441560	06/02/2008
IETAC | JANER CASTRO MONTALVO	Hombre	3105353181	03/04/2009
IETAC | DAVIER ESTEBAN OTERO URANGO	Hombre	3148945915	06/07/2007
IETAC | ELIANA MARCELA VERGARA GANDIA	Mujer	3025714175	21/06/2008
IETAC | LUISA FERNANDA BARÓN LUCAS	Mujer	3114062955	15/12/2008
IETAC | JORGE ANDRÉS PÉREZ MESTRA	Hombre	3146640429	14/03/2010
IETAC | YULEIMIS MURILLO GÓMEZ	Mujer	3218863178	12/10/2004
IETAC | NICOL TATIANA CERPA PEINADO	Mujer	3012478928	17/12/2008
IETAC | DAYANA MICHEL PEÑA TORDECILLA	Mujer	3218976781	06/05/2010
"""

def normalize(text):
    if not text: return ""
    text = text.replace('IETAC |', '').strip().upper()
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

def normalize_strict(text):
    return normalize(text).replace(" ", "")

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

madre_data = []
for line in madre_db_text.strip().split('\n'):
    parts = line.split('\t')
    if len(parts) >= 2:
        raw_name = parts[0].replace('IETAC |', '').strip()
        madre_data.append({
            'name': raw_name,
            'norm': normalize(raw_name),
            'strict_norm': normalize_strict(raw_name),
            'gender': 'female' if 'Mujer' in parts[1] else 'male',
            'phone': parts[2].strip() if len(parts) > 2 else "",
            'birthdate': parts[3].strip() if len(parts) > 3 else "",
            'status': 'missing' 
        })

csv_path = 'c:/Users/Daniel/Downloads/reporte/estudiantes_16-12-2025 (1).csv'
json_path = 'c:/Users/Daniel/Downloads/reporte/src/data/students.json' 
os.makedirs(os.path.dirname(json_path), exist_ok=True)

final_list = []
# Tracks IDs to detect duplicates
id_counts = Counter()
# First Pass to count IDs
with open(csv_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    for row in reader:
        if 'IETAC' in row.get('Institución', '').upper():
             id_counts[row.get('Número Documento', '').strip()] += 1

try:
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        
        for row in reader:
            if 'IETAC' not in row.get('Institución', '').upper():
                continue
            
            doc_id = row.get('Número Documento', '').strip()
            # Allow duplicates this time, but flag them
            
            p_name = row.get('Nombre', '').strip().title()
            p_norm = normalize(p_name)
            p_strict = normalize_strict(p_name)
            
            # IMPROVED MATCHING LOGIC
            best_match = None
            highest_score = 0.0
            
            for m_student in madre_data:
                if p_strict == m_student['strict_norm']:
                    best_match = m_student
                    highest_score = 1.0
                    break
                score = similar(p_norm, m_student['norm'])
                if score > highest_score:
                    highest_score = score
                    best_match = m_student
            
            MATCH_THRESHOLD = 0.6
            
            student = {
                'id': doc_id,
                'email': row.get('Usuario', '').strip(),
                'recovery_code': row.get('Código Recuperación', '').strip(),
                'status': 'active' if row.get('Estado', '').lower() == 'activo' else 'inactive',
                'platform_name': p_name
            }

            if best_match and highest_score >= MATCH_THRESHOLD:
                best_match['status'] = 'found'
                student['name'] = best_match['name'].title()
                student['gender'] = best_match['gender']
                student['birthdate'] = best_match['birthdate']
                p_phone = row.get('Teléfono', '').replace('+57', '').strip()
                student['phone'] = best_match['phone'] or p_phone
                
                if highest_score < 1.0 or p_norm != best_match['norm']:
                     if p_name.upper() != best_match['name'].upper():
                        student['analysis'] = {
                            'status': 'warning',
                            'message': f"Nombre en plataforma '{p_name}' tiene errores. Corrección: '{best_match['name']}'"
                        }
                     else:
                         student['analysis'] = {'status': 'ok'}
                else:
                    student['analysis'] = {'status': 'ok'}
            else:
                student['name'] = p_name
                student['gender'] = 'male' 
                student['phone'] = row.get('Teléfono', '').replace('+57', '').strip()
                student['analysis'] = {
                    'status': 'extra',
                    'message': "POSIBLE EXTRA: No coincide con Lista Madre oficial."
                }

            # CHECK FOR DUPLICATES
            if id_counts[doc_id] > 1:
                # If there's already an analysis, prepend/append or override priority
                current_msg = student['analysis'].get('message', '')
                student['analysis']['status'] = 'duplicate'
                student['analysis']['message'] = f"DUPLICADO: Este ID ({doc_id}) aparece {id_counts[doc_id]} veces."

            final_list.append(student)

    # Add completely missing
    for m in madre_data:
        if m['status'] == 'missing':
             final_list.append({
                'id': 'SIN_REGISTRO',
                'name': m['name'].title(),
                'email': '',
                'phone': m['phone'],
                'gender': m['gender'],
                'birthdate': m['birthdate'],
                'status': 'inactive',
                'analysis': {
                    'status': 'missing',
                    'message': "CRÍTICO: Estudiante oficial NO encontrado en plataforma."
                }
            })

    def sort_key(s):
        priority = {'missing': 0, 'duplicate': 0, 'extra': 1, 'warning': 2, 'ok': 3}
        return priority.get(s.get('analysis', {}).get('status', 'ok'), 99)

    final_list.sort(key=sort_key)

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)
    
    print(f"Generated Audit Dups Report: {len(final_list)} entries.")

except Exception as e:
    print(f"Error: {e}")
