import React from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle, TrendingDown } from 'lucide-react';

export default function Slide3_Problem() {
    return (
        <div className="flex flex-col items-center justify-center h-full w-full max-w-7xl mx-auto px-4">
            <motion.p
                className="text-gray-400 text-xl tracking-widest uppercase mb-12"
                initial={{ opacity: 0 }} animate={{ opacity: 1 }}
            >
                O Panorama Fitness Brasil 2025
            </motion.p>

            <div className="grid grid-cols-2 gap-16 w-full">
                {/* Stat 1 */}
                <motion.div
                    className="bg-gray-900/50 p-12 rounded-3xl border border-gray-800 backdrop-blur-sm"
                    initial={{ x: -100, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: 0.2 }}
                >
                    <div className="text-8xl font-black text-white mb-4">64%</div>
                    <p className="text-3xl text-gray-300 leading-snug">
                        Treinam <span className="text-red-400 font-bold">sem orientação nutricional</span>.
                    </p>
                    <p className="mt-6 text-gray-500 text-lg">Abastecem a máquina sem saber como ela funciona.</p>
                </motion.div>

                {/* Stat 2 */}
                <motion.div
                    className="bg-gray-900/50 p-12 rounded-3xl border border-gray-800 backdrop-blur-sm relative overflow-hidden"
                    initial={{ x: 100, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: 0.4 }}
                >
                    <div className="absolute top-0 right-0 p-8 opacity-10">
                        <AlertTriangle size={150} className="text-yellow-500" />
                    </div>
                    <div className="text-8xl font-black text-yellow-400 mb-4">91%</div>
                    <p className="text-3xl text-gray-300 leading-snug">
                        Tomam suplementos <span className="text-yellow-400 font-bold">por conta própria</span>.
                    </p>
                    <p className="mt-6 text-gray-500 text-lg">Risco de saúde e gasto financeiro ineficiente.</p>
                </motion.div>
            </div>

            <motion.div
                className="mt-20 p-6 bg-red-900/20 border border-red-500/30 rounded-xl flex items-center gap-6"
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1 }}
            >
                <TrendingDown size={40} className="text-red-400" />
                <div className="text-left">
                    <p className="text-red-300 font-semibold text-xl">A Barreira Financeira</p>
                    <p className="text-white text-2xl">Custo de Equipe Multidisciplinar: <span className="font-black">R$ 3.200 / mês</span></p>
                </div>
            </motion.div>
        </div>
    );
}
