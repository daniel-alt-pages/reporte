import csv
import json
import os

csv_path = 'c:/Users/Daniel/Downloads/reporte/estudiantes_16-12-2025 (1).csv'
html_path = 'c:/Users/Daniel/Downloads/reporte/index.html'

# HTML Template (Split into parts to inject data)
html_part1 = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Directorio Estudiantes IETAC</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- SweetAlert2 -->
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Outfit', 'sans-serif'],
                    },
                    colors: {
                        ietac: {
                            blue: '#1e3a8a',
                            yellow: '#fbbf24',
                            light: '#f3f4f6'
                        }
                    }
                }
            }
        }
    </script>
    <style>
        body {
            font-family: 'Outfit', sans-serif;
            background-color: #f8fafc;
        }
        .glass-header {
            background: rgba(30, 58, 138, 0.95);
            backdrop-filter: blur(10px);
        }
        .card-hover {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .card-hover:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px -8px rgba(0, 0, 0, 0.15);
        }
        .filter-btn {
            transition: all 0.2s;
        }
        .filter-btn.active {
            background-color: #1e3a8a;
            color: white;
            border-color: #1e3a8a;
        }
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
    </style>
</head>
<body class="min-h-screen flex flex-col">

    <!-- Header -->
    <header class="glass-header text-white shadow-lg sticky top-0 z-50 transition-all duration-300">
        <div class="container mx-auto px-4 py-4">
            <div class="flex flex-col lg:flex-row justify-between items-center gap-4">
                
                <!-- Logo & Title -->
                <div class="flex items-center space-x-3 w-full lg:w-auto justify-center lg:justify-start">
                    <div class="bg-yellow-400 p-2 rounded-lg text-blue-900 shadow-lg glow">
                        <i class="fas fa-graduation-cap text-2xl"></i>
                    </div>
                    <div>
                        <h1 class="text-2xl font-bold tracking-tight">Directorio IETAC</h1>
                        <p class="text-xs text-blue-200 font-medium tracking-wide">Gestión de Contactos Estudiantiles</p>
                    </div>
                </div>

                <!-- Filters & Search Container -->
                <div class="flex flex-col md:flex-row gap-3 w-full lg:w-auto items-center">
                    
                    <!-- Search Bar -->
                    <div class="relative w-full md:w-64 group">
                        <input type="text" id="searchInput" placeholder="Buscar por nombre o ID..." 
                            class="w-full pl-10 pr-4 py-2.5 rounded-xl text-gray-800 bg-blue-800/50 border border-blue-700/50 placeholder-blue-300 text-white focus:bg-white focus:text-gray-900 focus:outline-none focus:ring-2 focus:ring-yellow-400 transition-all shadow-inner">
                        <i class="fas fa-search absolute left-3 top-3.5 text-blue-300 group-focus-within:text-gray-400 transition-colors"></i>
                    </div>

                    <!-- Filter Group -->
                    <div class="flex bg-blue-800/50 p-1 rounded-xl border border-blue-700/50 backdrop-blur-sm overflow-x-auto max-w-full">
                        <button onclick="setFilter('all')" id="btn-all" class="filter-btn active px-4 py-1.5 rounded-lg text-sm font-medium text-blue-100 hover:bg-white/10 whitespace-nowrap">
                            Todos
                        </button>
                        <button onclick="setFilter('active')" id="btn-active" class="filter-btn px-4 py-1.5 rounded-lg text-sm font-medium text-blue-100 hover:bg-white/10 flex items-center gap-2 whitespace-nowrap">
                            <span class="w-2 h-2 rounded-full bg-green-400"></span> Activos
                        </button>
                        <button onclick="setFilter('inactive')" id="btn-inactive" class="filter-btn px-4 py-1.5 rounded-lg text-sm font-medium text-blue-100 hover:bg-white/10 flex items-center gap-2 whitespace-nowrap">
                            <span class="w-2 h-2 rounded-full bg-red-400"></span> Inactivos
                        </button>
                    </div>

                </div>
            </div>
            
            <!-- Stats Bar (Compact) -->
            <div class="mt-4 pt-3 border-t border-blue-800/50 flex justify-between items-center text-xs text-blue-200">
                <div class="flex gap-4">
                    <span>Total: <b id="totalCount" class="text-white">0</b></span>
                    <span>Activos: <b id="activeCount" class="text-green-300">0</b></span>
                    <span>Inactivos: <b id="inactiveCount" class="text-red-300">0</b></span>
                </div>
                 <button onclick="resetData()" class="text-blue-300 hover:text-white underline" title="Restaurar datos originales">
                    <i class="fas fa-sync-alt mr-1"></i> Resetear
                </button>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-8 flex-grow">
        
        <div id="studentsGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <!-- Cards generated by JS -->
        </div>

        <div id="noResults" class="hidden flex flex-col items-center justify-center py-20 text-center opacity-0 transition-opacity duration-300">
            <div class="bg-gray-100 p-6 rounded-full mb-4">
                <i class="fas fa-search text-4xl text-gray-400"></i>
            </div>
            <h3 class="text-xl text-gray-700 font-bold mb-2">No se encontraron resultados</h3>
            <p class="text-gray-500 max-w-xs mx-auto">Intenta ajustar tu búsqueda o cambia los filtros seleccionados.</p>
            <button onclick="setFilter('all'); document.getElementById('searchInput').value=''; renderStudents();" class="mt-6 px-6 py-2 bg-blue-900 text-white rounded-lg hover:bg-blue-800 transition shadow-lg">
                Limpiar filtros
            </button>
        </div>

    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200 text-gray-500 py-8 mt-auto">
        <div class="container mx-auto px-4 text-center">
            <p class="mb-2 font-medium">IETAC &copy; 2024</p>
            <p class="text-sm">Plataforma de Gestión Estudiantil</p>
        </div>
    </footer>

    <script>
        // Datos Inyectados
"""

html_part2 = """
        // Estado
        let students = [];
        let currentFilter = 'all';

        // DOM
        const grid = document.getElementById('studentsGrid');
        const searchInput = document.getElementById('searchInput');
        const noResults = document.getElementById('noResults');
        
        function init() {
            loadStudents();
            renderStudents();
            updateStats();
        }

        function loadStudents() {
            const stored = localStorage.getItem('ietac_students_v3');
            if (stored) {
                students = JSON.parse(stored);
            } else {
                students = [...defaultStudents];
                saveStudents();
            }
        }

        function saveStudents() {
            localStorage.setItem('ietac_students_v3', JSON.stringify(students));
            updateStats();
        }

        function resetData() {
            Swal.fire({
                title: '¿Restaurar datos?',
                text: "Esto cargará la lista completa original.",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#1e3a8a',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sí, restaurar'
            }).then((result) => {
                if (result.isConfirmed) {
                    students = [...defaultStudents];
                    saveStudents();
                    renderStudents();
                    Swal.fire('Restaurado', 'Base de datos reiniciada.', 'success');
                }
            });
        }

        function toggleStatus(id) {
            const idx = students.findIndex(s => s.id === id);
            if (idx !== -1) {
                students[idx].active = !students[idx].active;
                saveStudents();
                renderStudents(searchInput.value);
            }
        }

        function setFilter(filter) {
            currentFilter = filter;
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById(`btn-${filter}`).classList.add('active');
            renderStudents(searchInput.value);
        }

        function updateStats() {
            const total = students.length;
            const active = students.filter(s => s.active).length;
            const inactive = total - active;
            document.getElementById('totalCount').textContent = total;
            document.getElementById('activeCount').textContent = active;
            document.getElementById('inactiveCount').textContent = inactive;
        }

        function renderStudents(searchText = '') {
            grid.innerHTML = '';
            
            const filtered = students.filter(student => {
                const matchesSearch = student.name.toLowerCase().includes(searchText.toLowerCase()) || 
                                    student.id.includes(searchText);
                let matchesStatus = true;
                if (currentFilter === 'active') matchesStatus = student.active;
                if (currentFilter === 'inactive') matchesStatus = !student.active;
                return matchesSearch && matchesStatus;
            });

            if (filtered.length === 0) {
                noResults.classList.remove('hidden');
                setTimeout(() => noResults.classList.remove('opacity-0'), 50);
            } else {
                noResults.classList.add('hidden');
                noResults.classList.add('opacity-0');
            }

            // Avatar colors based on name length to be deterministic but varied
            const colors = [
                'bg-red-100 text-red-600', 'bg-orange-100 text-orange-600', 
                'bg-amber-100 text-amber-600', 'bg-green-100 text-green-600', 
                'bg-teal-100 text-teal-600', 'bg-cyan-100 text-cyan-600',
                'bg-blue-100 text-blue-600', 'bg-indigo-100 text-indigo-600', 
                'bg-violet-100 text-violet-600', 'bg-fuchsia-100 text-fuchsia-600', 
                'bg-pink-100 text-pink-600', 'bg-rose-100 text-rose-600'
            ];

            filtered.forEach(student => {
                // Determine Avatar
                const colorIndex = student.name.length % colors.length;
                const avatarBg = colors[colorIndex];
                
                // Initials
                const initials = student.name.split(' ').map(n => n[0]).slice(0, 2).join('').toUpperCase();

                const statusColor = student.active ? 'bg-green-100 text-green-700 border-green-200' : 'bg-red-100 text-red-700 border-red-200';
                const statusText = student.active ? 'Activo' : 'Inactivo';
                const statusIcon = student.active ? 'fa-check-circle' : 'fa-times-circle';

                const whatsappMsg = encodeURIComponent(`Hola ${student.name.split(' ')[0]}, cordial saludo.`);
                const whatsappLink = `https://wa.me/57${student.phone}?text=${whatsappMsg}`;

                const card = document.createElement('div');
                card.className = `bg-white rounded-2xl shadow-sm p-5 card-hover border border-gray-100 flex flex-col justify-between h-full relative group overflow-hidden ${!student.active ? 'opacity-75 grayscale-[0.8] hover:grayscale-0 hover:opacity-100 transition-all' : ''}`;
                
                card.innerHTML = `
                    <div class="absolute top-4 right-4 z-10">
                        <button onclick="toggleStatus('${student.id}')" 
                                class="w-8 h-8 rounded-full bg-white shadow-sm border border-gray-100 flex items-center justify-center text-gray-400 hover:text-blue-600 hover:bg-blue-50 transition-colors"
                                title="Cambiar estado">
                            <i class="fas fa-power-off"></i>
                        </button>
                    </div>

                    <div>
                        <div class="flex items-start space-x-4 mb-4">
                            <div class="w-12 h-12 rounded-xl ${avatarBg} flex items-center justify-center text-sm font-bold shadow-sm flex-shrink-0 select-none">
                                ${initials}
                            </div>
                            <div class="pt-0.5 min-w-0">
                                <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider ${statusColor} border mb-1">
                                    <i class="fas ${statusIcon}"></i> ${statusText}
                                </span>
                                <h3 class="font-bold text-gray-800 text-md leading-tight group-hover:text-blue-800 transition-colors truncate w-full" title="${student.name}">${student.name}</h3>
                                <p class="text-xs text-gray-400 mt-0.5 font-mono">ID: ${student.id}</p>
                            </div>
                        </div>
                        
                        <div class="space-y-2 mb-5">
                            <div class="flex items-center text-sm text-gray-600 bg-gray-50/50 p-2 rounded-lg border border-gray-100/50">
                                <i class="fas fa-envelope w-5 text-gray-400 text-xs"></i>
                                <span class="truncate text-xs font-medium" title="${student.email}">${student.email || 'Sin correo'}</span>
                            </div>
                            <div class="flex items-center text-sm text-gray-600 bg-gray-50/50 p-2 rounded-lg border border-gray-100/50">
                                <i class="fas fa-phone w-5 text-gray-400 text-xs"></i>
                                <span class="text-xs font-medium">${student.phone || 'Sin teléfono'}</span>
                            </div>
                        </div>
                    </div>

                    <a href="${whatsappLink}" target="_blank" 
                       class="block w-full bg-slate-800 hover:bg-green-600 text-white text-center font-medium py-2 px-4 rounded-lg transition-all duration-300 flex items-center justify-center space-x-2 shadow-md hover:shadow-lg group/btn">
                        <i class="fab fa-whatsapp text-lg group-hover/btn:scale-110 transition-transform"></i>
                        <span>Contactar</span>
                    </a>
                `;
                grid.appendChild(card);
            });
        }

        searchInput.addEventListener('input', (e) => renderStudents(e.target.value));
        init();
    </script>
</body>
</html>
"""

# Parsing Logic
students = []
try:
    with open(csv_path, 'r', encoding='utf-8-sig') as f: # Changed to utf-8-sig to handle BOM
        # Read lines first to safely get keys
        lines = f.readlines()
        if not lines:
            print("CSV Empty")
            exit(1)
            
        reader = csv.DictReader(lines, delimiter=';')
        
        # Debug: Print fields
        print(f"Fields found: {reader.fieldnames}")
        
        for row in reader:
            # Flexible Key Access
            # Get values safe for None
            nombre = row.get('Nombre')
            doc = row.get('Número Documento')
            
            if not nombre or not doc:
                continue
            
            # Clean phone (remove spaces, +57)
            raw_phone = row.get('Teléfono', '')
            phone = raw_phone.replace('+57', '').replace(' ', '').strip() if raw_phone else ''
            
            # Status
            raw_status = row.get('Estado', '')
            active = raw_status.strip().lower() == 'activo' if raw_status else True
            
            # Email (prefer Usuario, fallback to email rec)
            email = row.get('Usuario')
            if not email:
                email = row.get('Email Recuperación', '')
            
            student = {
                'name': nombre.strip().title(),
                'email': email.strip() if email else '',
                'id': str(doc).strip(),
                'phone': phone,
                'active': active
            }
            students.append(student)

except Exception as e:
    print(f"Error parsing CSV: {e}")
    # Fallback to empty
    students = []

# Generate JS Object
students_js = "        const defaultStudents = " + json.dumps(students, ensure_ascii=False) + ";"

# Combine
full_html = html_part1 + students_js + html_part2

# Write
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"Successfully updated index.html with {len(students)} students.")
