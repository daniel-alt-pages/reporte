import React from 'react';
import { motion } from 'framer-motion';
import { Phone, Mail, User, School, GraduationCap, CheckCircle2, XCircle, KeyRound, Cake, AlertTriangle, UserX, AlertOctagon, Copy } from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs) {
    return twMerge(clsx(inputs));
}

export function StudentCard({ student, toggleStatus }) {
    // Use explicit gender from data
    const isFemale = student.gender === 'female';

    // Avatar colors based on gender
    const avatarClass = isFemale
        ? 'bg-pink-100 text-pink-600'
        : 'bg-blue-100 text-blue-600';

    // Generate Professional WhatsApp Message
    const getAuditMessage = () => {
        const firstName = student.name.split(' ')[0];
        let msg = `Hola ${firstName}, cordial saludo.\n\n`;

        msg += `Te escribimos para validar tu información en la plataforma educativa:\n`;
        msg += `🔑 Usuario: ${student.email}\n`;
        if (student.recovery_code) msg += `🔐 Código Recuperación: ${student.recovery_code}\n`;

        if (student.analysis) {
            msg += `\n⚠️ *Novedad Encontrada:* \n`;
            if (student.analysis.status === 'missing') {
                msg += `No encontramos tu registro activo en la plataforma. Por favor confirma si ya te registraste.`;
            } else if (student.analysis.status === 'duplicate') {
                msg += `Tu usuario aparece DUPLICADO en la plataforma. Por favor reporta esto a soporte técnico.`;
            } else if (student.analysis.status === 'extra') {
                msg += `Tu nombre registrado en plataforma "${student.name}" no coincide con la lista oficial. Por favor verifica si está escrito correctamente.`;
            } else if (student.analysis.status === 'warning') {
                msg += `Tu nombre en plataforma "${student.platform_name}" tiene errores de escritura. Debería ser: "${student.name}".`;
            }
        }

        msg += `\n\nPor favor, ingresa y valida tus datos.`;
        return encodeURIComponent(msg);
    };

    const whatsappLink = `https://wa.me/57${student.phone}?text=${getAuditMessage()}`;

    return (
        <motion.div
            layout
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            whileHover={{ y: -4 }}
            transition={{ duration: 0.2 }}
            className={cn(
                "bg-white rounded-2xl p-5 shadow-sm border border-slate-100 flex flex-col justify-between h-full relative group transition-all",
                "hover:shadow-md hover:border-blue-200",
                student.status === 'inactive' && "opacity-75 grayscale-[0.5]"
            )}
        >
            <div className="absolute top-4 right-4 z-10 opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                    onClick={() => toggleStatus(student.id)}
                    className="p-1.5 rounded-full bg-white shadow-sm border border-slate-100 text-slate-400 hover:text-blue-600 hover:bg-slate-50 transition-colors"
                    title={student.status === 'active' ? "Desactivar" : "Activar"}
                >
                    {student.status === 'active' ? <CheckCircle2 size={18} className="text-green-500" /> : <XCircle size={18} className="text-red-500" />}
                </button>
            </div>

            {student.analysis && student.analysis.status !== 'ok' && (
                <div className={cn(
                    "mb-4 p-3 rounded-xl flex items-start gap-2 text-xs font-medium border",
                    student.analysis.status === 'missing' && "bg-red-50 text-red-700 border-red-200",
                    student.analysis.status === 'duplicate' && "bg-purple-50 text-purple-700 border-purple-200",
                    student.analysis.status === 'extra' && "bg-orange-50 text-orange-700 border-orange-200",
                    student.analysis.status === 'warning' && "bg-yellow-50 text-yellow-700 border-yellow-200"
                )}>
                    {student.analysis.status === 'missing' && <AlertOctagon size={16} className="shrink-0" />}
                    {student.analysis.status === 'duplicate' && <Copy size={16} className="shrink-0" />}
                    {student.analysis.status === 'extra' && <UserX size={16} className="shrink-0" />}
                    {student.analysis.status === 'warning' && <AlertTriangle size={16} className="shrink-0" />}
                    <span>{student.analysis.message}</span>
                </div>
            )}

            <div>
                <div className="flex items-start gap-4 mb-4">
                    <div className={cn("w-14 h-14 rounded-2xl flex items-center justify-center text-2xl shadow-sm flex-shrink-0 select-none transition-colors", avatarClass)}>
                        {/* Simple gender icon or initial could go here, sticking to icon for gender differentiation */}
                        <User size={24} />
                    </div>
                    <div className="min-w-0 flex-1 pt-1">
                        <div className="flex items-center gap-2 mb-1">
                            <span className={cn(
                                "inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border",
                                student.status === 'active'
                                    ? "bg-green-50 text-green-700 border-green-200"
                                    : "bg-red-50 text-red-700 border-red-200"
                            )}>
                                <span className={cn("w-1.5 h-1.5 rounded-full", student.status === 'active' ? "bg-green-500" : "bg-red-500")} />
                                {student.status === 'active' ? 'Activo' : 'Inactivo'}
                            </span>
                        </div>
                        <h3 className="font-bold text-slate-800 text-base leading-tight truncate w-full" title={student.name}>
                            {student.name}
                        </h3>
                        <p className="text-xs text-slate-400 mt-1 font-mono">ID: {student.id}</p>
                    </div>
                </div>

                <div className="space-y-2 mb-5">
                    <InfoRow icon={Mail} text={student.email || 'Sin correo'} href={student.email ? `mailto:${student.email}` : undefined} />

                    <InfoRow icon={Phone} text={student.phone || 'Sin teléfono'} />

                    {student.recovery_code && (
                        <InfoRow icon={KeyRound} text={<span className="font-mono tracking-wider text-blue-600 bg-blue-50 px-1 rounded">{student.recovery_code}</span>} />
                    )}

                    {student.birthdate && (
                        <InfoRow icon={Cake} text={student.birthdate} />
                    )}
                </div>
            </div>

            <a
                href={whatsappLink}
                target="_blank"
                rel="noreferrer"
                className={cn(
                    "mt-auto w-full text-white text-center font-medium py-3 px-4 rounded-xl transition-all duration-300 flex items-center justify-center gap-2 shadow-lg",
                    isFemale
                        ? "bg-pink-500 hover:bg-pink-600 shadow-pink-200 hover:shadow-pink-300"
                        : "bg-blue-600 hover:bg-blue-700 shadow-blue-200 hover:shadow-blue-300"
                )}
            >
                <Phone size={18} />
                <span>Contactar</span>
            </a>
        </motion.div>
    );
}

function InfoRow({ icon: Icon, label, text, href }) {
    const content = (
        <>
            <Icon size={14} className="text-slate-400 group-hover:text-slate-500 transition-colors shrink-0" />
            <div className="flex flex-col min-w-0">
                {label && <span className="text-[10px] uppercase font-bold text-slate-400 leading-none mb-0.5">{label}</span>}
                <span className="truncate text-xs font-medium text-slate-600 leading-tight">{text}</span>
            </div>
        </>
    );

    if (href) {
        return (
            <a href={href} className="flex items-start gap-3 bg-slate-50 p-2.5 rounded-xl border border-slate-100 hover:bg-slate-100 transition-colors group">
                {content}
            </a>
        );
    }

    return (
        <div className="flex items-start gap-3 bg-slate-50 p-2.5 rounded-xl border border-slate-100 group">
            {content}
        </div>
    );
}
