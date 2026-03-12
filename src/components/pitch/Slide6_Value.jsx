import React from 'react';
import { motion } from 'framer-motion';
import { Check, X } from 'lucide-react';

export default function Slide6_Value() {
    return (
        <div className="flex flex-col items-center justify-center h-full w-full max-w-6xl mx-auto">
            <h1 className="text-5xl font-bold mb-20">Democratizando a Elite</h1>

            <div className="flex items-center justify-center gap-12 w-full">

                {/* Old Way */}
                <motion.div
                    className="w-1/3 bg-gray-800 rounded-3xl p-8 opacity-50 grayscale"
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 0.5, scale: 1 }}
                    transition={{ duration: 0.5 }}
                >
                    <h2 className="text-2xl text-gray-400 mb-6">Equipe Humana</h2>
                    <ul className="space-y-4 mb-8 text-gray-500">
                        <li className="flex items-center gap-3"><Check size={20} /> Personal Trainer</li>
                        <li className="flex items-center gap-3"><Check size={20} /> Nutricionista</li>
                        <li className="flex items-center gap-3"><Check size={20} /> Fisioterapeuta</li>
                        <li className="flex items-center gap-3"><Check size={20} /> Agenda Coordenada</li>
                    </ul>
                    <div className="text-4xl font-bold text-gray-400 line-through decoration-red-500 decoration-4">
                        R$ 3.200<span className="text-lg font-normal">/mês</span>
                    </div>
                </motion.div>

                {/* VS Badge */}
                <div className="text-2xl font-black bg-white text-black w-16 h-16 rounded-full flex items-center justify-center z-10 shrink-0">
                    VS
                </div>

                {/* New Way */}
                <motion.div
                    className="w-1/3 bg-gradient-to-b from-cyan-900 to-blue-900 rounded-3xl p-10 border-2 border-cyan-400 shadow-[0_0_50px_rgba(34,211,238,0.3)] relative overflow-hidden"
                    initial={{ opacity: 0, scale: 1.1, y: 20 }}
                    animate={{ opacity: 1, scale: 1.1, y: 0 }}
                    transition={{ delay: 0.5, type: "spring" }}
                >
                    <div className="absolute top-0 right-0 bg-yellow-400 text-black font-bold px-4 py-1 text-xs uppercase tracking-wider">
                        Consenso IA
                    </div>

                    <h2 className="text-3xl text-white font-bold mb-6">My Personal Team</h2>
                    <ul className="space-y-4 mb-10 text-cyan-100">
                        <li className="flex items-center gap-3"><Check size={20} className="text-cyan-400" /> 5 Agentes Especialistas</li>
                        <li className="flex items-center gap-3"><Check size={20} className="text-cyan-400" /> Debate em Tempo Real</li>
                        <li className="flex items-center gap-3"><Check size={20} className="text-cyan-400" /> 100% Personalizado</li>
                        <li className="flex items-center gap-3"><Check size={20} className="text-cyan-400" /> Disponível 24/7</li>
                    </ul>
                    <div className="text-6xl font-black text-white">
                        R$ 49,90<span className="text-lg font-normal text-cyan-200">/mês</span>
                    </div>
                </motion.div>

            </div>

            <motion.p
                className="mt-24 text-xl text-gray-400 tracking-wide"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 1.5 }}
            >
                Segurança e Performance não são mais um luxo.
            </motion.p>
        </div>
    );
}
