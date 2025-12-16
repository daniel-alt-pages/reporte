import { Users, UserCheck, UserX, AlertTriangle } from 'lucide-react';

const Card = ({ label, count, icon: Icon, colorClass, filterType, isActive, onFilter }) => (
    <button
        onClick={() => onFilter(filterType)}
        className={`rounded-2xl p-4 flex items-center justify-between transition-all w-full text-left relative overflow-hidden group ${colorClass} ${isActive ? 'ring-2 ring-offset-2 ring-blue-500 scale-[1.02]' : 'hover:scale-[1.01]'}`}
    >
        <div className="relative z-10">
            <p className="opacity-90 text-sm font-medium mb-1">{label}</p>
            <h3 className="text-3xl font-bold">{count}</h3>
        </div>
        <div className="p-3 rounded-xl bg-white/20 relative z-10 backdrop-blur-sm">
            <Icon size={24} />
        </div>
    </button>
);

export function Stats({ stats, onFilter, currentFilter }) {
    return (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 mb-6">
            <Card
                label="Total"
                count={stats.total}
                icon={Users}
                colorClass="bg-gradient-to-br from-slate-700 to-slate-900 text-white shadow-lg shadow-slate-200"
                filterType="all"
                isActive={currentFilter === 'all'}
                onFilter={onFilter}
            />
            <Card
                label="Activos"
                count={stats.active}
                icon={UserCheck}
                colorClass="bg-gradient-to-br from-green-500 to-green-600 text-white shadow-lg shadow-green-200"
                filterType="active"
                isActive={currentFilter === 'active'}
                onFilter={onFilter}
            />
            <Card
                label="Inactivos"
                count={stats.inactive}
                icon={UserX}
                colorClass="bg-gradient-to-br from-red-500 to-red-600 text-white shadow-lg shadow-red-200"
                filterType="inactive"
                isActive={currentFilter === 'inactive'}
                onFilter={onFilter}
            />
            <Card
                label="Novedades"
                count={stats.issues}
                icon={AlertTriangle}
                colorClass="bg-gradient-to-br from-yellow-400 to-orange-500 text-white shadow-lg shadow-orange-200"
                filterType="issues"
                isActive={currentFilter === 'issues'}
                onFilter={onFilter}
            />
        </div>
    );
}
