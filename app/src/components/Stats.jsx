import React from 'react';
import { Users, UserCheck, UserX } from 'lucide-react';

export function Stats({ stats }) {
    return (
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
            <div className="bg-blue-600 rounded-2xl p-4 text-white shadow-lg shadow-blue-200 flex items-center justify-between">
                <div>
                    <p className="text-blue-100 text-sm font-medium mb-1">Total Estudiantes</p>
                    <h3 className="text-3xl font-bold">{stats.total}</h3>
                </div>
                <div className="bg-blue-500/30 p-3 rounded-xl">
                    <Users size={24} />
                </div>
            </div>

            <div className="bg-green-100 rounded-2xl p-4 border border-green-200 flex items-center justify-between">
                <div>
                    <p className="text-green-600 text-sm font-medium mb-1">Activos</p>
                    <h3 className="text-3xl font-bold text-green-700">{stats.active}</h3>
                </div>
                <div className="bg-green-200 p-3 rounded-xl text-green-700">
                    <UserCheck size={24} />
                </div>
            </div>

            <div className="bg-slate-100 rounded-2xl p-4 border border-slate-200 flex items-center justify-between">
                <div>
                    <p className="text-slate-500 text-sm font-medium mb-1">Inactivos</p>
                    <h3 className="text-3xl font-bold text-slate-700">{stats.inactive}</h3>
                </div>
                <div className="bg-slate-200 p-3 rounded-xl text-slate-600">
                    <UserX size={24} />
                </div>
            </div>
        </div>
    );
}
