import csv
csv_path = 'c:/Users/Daniel/Downloads/reporte/estudiantes_16-12-2025 (1).csv'
statuses = set()
with open(csv_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    for row in reader:
        if 'IETAC' in row.get('Institución', '').upper():
            statuses.add(f"'{row.get('Estado')}'")

print(f"Unique Statuses for IETAC: {statuses}")
