import csv
csv_path = 'c:/Users/Daniel/Downloads/reporte/estudiantes_16-12-2025 (1).csv'
ids = []
names = []
with open(csv_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    for row in reader:
        if 'IETAC' in row.get('Institución', '').upper():
            ids.append(row.get('Número Documento', '').strip())
            names.append(row.get('Nombre', '').strip())

from collections import Counter
dup_ids = [item for item, count in Counter(ids).items() if count > 1]
dup_names = [item for item, count in Counter(names).items() if count > 1]

print(f"Dup IDs: {dup_ids}")
print(f"Dup Names: {dup_names}")
