import React, { useState, useEffect, useMemo } from 'react';
import { Search, RotateCcw, LayoutGrid, Users, Building2, SlidersHorizontal, X } from 'lucide-react';
import { AnimatePresence, motion } from 'framer-motion';
import { StudentCard } from './components/StudentCard';
import { Stats } from './components/Stats';
import initialData from './data/students.json';

function App() {
    const [students, setStudents] = useState(() => {
        // Reset version to ensure clean data load from new source
        const saved = localStorage.getItem('ietac_official_v8');
        return saved ? JSON.parse(saved) : initialData;
    });

    const [search, setSearch] = useState('');
    const [statusFilter, setStatusFilter] = useState('all');
    const [genderFilter, setGenderFilter] = useState('all');
    const [isSearchOpen, setIsSearchOpen] = useState(false);

    useEffect(() => {
        localStorage.setItem('ietac_official_v8', JSON.stringify(students));
    }, [students]);

    const toggleStatus = (id) => {
        setStudents(prev => prev.map(s =>
            s.id === id ? { ...s, status: s.status === 'active' ? 'inactive' : 'active' } : s
        ));
    };

    const resetData = () => {
        if (confirm('¿Restaurar lista oficial?')) {
            setStudents(initialData);
            setSearch('');
            setStatusFilter('all');
            setGenderFilter('all');
        }
    };

    const filteredStudents = useMemo(() => {
        return students.filter(s => {
            const matchesSearch = s.name.toLowerCase().includes(search.toLowerCase()) ||
                s.id.includes(search) ||
                s.phone.includes(search);

            const matchesStatus = statusFilter === 'all' || s.status === statusFilter;
            const matchesGender = genderFilter === 'all' || s.gender === genderFilter;

            return matchesSearch && matchesStatus && matchesGender;
        });
    }, [students, search, statusFilter, genderFilter]);

    const stats = useMemo(() => ({
        total: filteredStudents.length,
        active: filteredStudents.filter(s => s.status === 'active').length,
        inactive: filteredStudents.filter(s => s.status === 'inactive').length
    }), [filteredStudents]);

    return (
        <div className="min-h-screen bg-slate-50/50 pb-20 font-sans">

            {/* Simplified Header */}
            <header className="sticky top-0 z-40 glass-header border-b border-slate-200/60 backdrop-blur-md">
                <div className="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
                    <div className="flex items-center gap-3">
                        <div className="bg-gradient-to-br from-blue-900 to-blue-800 p-2.5 rounded-xl text-yellow-400 shadow-md">
                            <Building2 size={20} strokeWidth={2.5} />
                        </div>
                        <div className="flex flex-col">
                            <h1 className="text-lg font-extrabold text-slate-900 leading-none tracking-tight">Directorio</h1>
                            <span className="text-[10px] font-bold text-blue-700 bg-blue-50 px-1.5 py-0.5 rounded-md self-start mt-0.5 border border-blue-100">
                                IETAC OFICIAL
                            </span>
                        </div>
                    </div>

                    <div className="flex items-center gap-3 text-xs font-medium text-slate-500 bg-slate-100/80 px-3 py-1.5 rounded-full border border-slate-200/50">
                        <span className="flex items-center gap-1.5 ">
                            <Users size={14} />
                            {stats.total}
                        </span>
                        <span className="text-slate-300">|</span>
                        <button onClick={resetData} className="hover:text-blue-600 transition-colors">
                            <RotateCcw size={14} />
                        </button>
                    </div>
                </div>
            </header>

            {/* Floating Action Button for Search */}
            <motion.button
                whileTap={{ scale: 0.9 }}
                onClick={() => setIsSearchOpen(true)}
                className="fixed bottom-6 right-6 z-50 bg-blue-600 text-white p-4 rounded-full shadow-lg shadow-blue-600/30 hover:bg-blue-700 transition-colors flex items-center justify-center p-4 border border-blue-500"
            >
                <Search size={24} />
            </motion.button>

            {/* Search Overlay/Modal */}
            <AnimatePresence>
                {isSearchOpen && (
                    <>
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            onClick={() => setIsSearchOpen(false)}
                            className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50"
                        />
                        <motion.div
                            initial={{ y: "100%" }}
                            animate={{ y: 0 }}
                            exit={{ y: "100%" }}
                            transition={{ type: "spring", damping: 25, stiffness: 300 }}
                            className="fixed bottom-0 left-0 right-0 z-50 bg-white rounded-t-3xl shadow-2xl border-t border-slate-100 max-h-[85vh] overflow-y-auto"
                        >
                            <div className="max-w-2xl mx-auto p-6 space-y-6 pb-10">
                                <div className="flex items-center justify-between mb-2">
                                    <h2 className="text-xl font-bold text-slate-900">Filtrar y Buscar</h2>
                                    <button onClick={() => setIsSearchOpen(false)} className="p-2 bg-slate-100 rounded-full text-slate-500 hover:bg-slate-200">
                                        <X size={20} />
                                    </button>
                                </div>

                                <div className="relative">
                                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
                                    <input
                                        autoFocus
                                        type="text"
                                        placeholder="Nombre, ID, o teléfono..."
                                        value={search}
                                        onChange={(e) => setSearch(e.target.value)}
                                        className="w-full pl-11 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-lg"
                                    />
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div className="space-y-2">
                                        <label className="text-sm font-semibold text-slate-700 ml-1">Estado</label>
                                        <div className="flex flex-col bg-slate-50 p-1.5 rounded-xl border border-slate-200 gap-1">
                                            {['all', 'active', 'inactive'].map((f) => (
                                                <button
                                                    key={f}
                                                    onClick={() => setStatusFilter(f)}
                                                    className={`px-3 py-2 rounded-lg text-sm font-medium transition-all text-left flex items-center justify-between ${statusFilter === f
                                                        ? 'bg-white text-blue-700 shadow-sm border border-blue-100'
                                                        : 'text-slate-500 hover:bg-white/50'
                                                        }`}
                                                >
                                                    <span>{f === 'all' ? 'Todos' : f === 'active' ? 'Activos' : 'Inactivos'}</span>
                                                    {statusFilter === f && <div className="w-2 h-2 rounded-full bg-blue-500"></div>}
                                                </button>
                                            ))}
                                        </div>
                                    </div>

                                    <div className="space-y-2">
                                        <label className="text-sm font-semibold text-slate-700 ml-1">Género</label>
                                        <div className="flex flex-col bg-slate-50 p-1.5 rounded-xl border border-slate-200 gap-1">
                                            {[{ v: 'all', l: 'Todos' }, { v: 'male', l: 'Hombres' }, { v: 'female', l: 'Mujeres' }].map((g) => (
                                                <button
                                                    key={g.v}
                                                    onClick={() => setGenderFilter(g.v)}
                                                    className={`px-3 py-2 rounded-lg text-sm font-medium transition-all text-left flex items-center justify-between ${genderFilter === g.v
                                                        ? 'bg-white text-blue-700 shadow-sm border border-blue-100'
                                                        : 'text-slate-500 hover:bg-white/50'
                                                        }`}
                                                >
                                                    <span>{g.l}</span>
                                                    {genderFilter === g.v && <div className="w-2 h-2 rounded-full bg-blue-500"></div>}
                                                </button>
                                            ))}
                                        </div>
                                    </div>
                                </div>

                                <div className="pt-2">
                                    <button
                                        onClick={() => setIsSearchOpen(false)}
                                        className="w-full py-3.5 bg-blue-600 text-white font-bold rounded-xl shadow-lg shadow-blue-600/20 active:scale-[0.98] transition-all"
                                    >
                                        Ver {filteredStudents.length} Resultados
                                    </button>
                                </div>
                            </div>
                        </motion.div>
                    </>
                )}
            </AnimatePresence>

            <main className="max-w-7xl mx-auto px-4 py-8">

                <Stats stats={stats} />

                {filteredStudents.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                        {filteredStudents.map(student => (
                            <StudentCard
                                key={student.id}
                                student={student}
                                toggleStatus={toggleStatus}
                            />
                        ))}
                    </div>
                ) : (
                    <div className="flex flex-col items-center justify-center py-20 text-center border-2 border-dashed border-slate-200 rounded-3xl bg-slate-50/30">
                        <div className="bg-white p-4 rounded-xl mb-3 shadow-sm">
                            <LayoutGrid className="text-slate-300" size={40} />
                        </div>
                        <h3 className="font-bold text-slate-900 text-lg">Sin resultados</h3>
                        <p className="text-slate-500 text-sm mb-4">Intenta ajustar tu búsqueda o filtros.</p>
                        <button
                            onClick={() => { setSearch(''); setStatusFilter('all'); setGenderFilter('all'); setIsSearchOpen(true); }}
                            className="px-4 py-2 bg-slate-900 text-white text-sm font-medium rounded-lg hover:bg-slate-800 transition-colors"
                        >
                            Limpiar filtros
                        </button>
                    </div>
                )}

            </main>
        </div>
    );
}

export default App;
