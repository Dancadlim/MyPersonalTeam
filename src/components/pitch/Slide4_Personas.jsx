import React from 'react';
import { motion } from 'framer-motion';
import { Activity, Zap, Frown, TrendingUp } from 'lucide-react';

export default function Slide4_Personas() {
    return (
        <div className="flex flex-col items-center justify-center h-full w-full max-w-7xl mx-auto">
            <div className="grid grid-cols-2 gap-12 w-full h-[600px]">

                {/* Persona 1: Mario */}
                <motion.div
                    className="relative bg-gradient-to-br from-gray-800 to-gray-900 rounded-[2rem] p-10 flex flex-col justify-between overflow-hidden"
                    initial={{ x: -50, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                >
                    <div className="absolute top-0 right-0 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl -mr-16 -mt-16"></div>

                    <div>
                        <div className="flex items-center gap-4 mb-6">
                            <div className="w-20 h-20 bg-gray-700 rounded-full flex items-center justify-center text-3xl">👨🏻</div>
                            <div>
                                <h2 className="text-4xl font-bold text-white">Mario</h2>
                                <p className="text-blue-400 text-xl">38 Anos • Futebol de Fim de Semana</p>
                            </div>
                        </div>

                        <ul className="space-y-6 text-xl text-gray-300">
                            <li className="flex items-start gap-3">
                                <Frown className="text-red-400 shrink-0 mt-1" />
                                <span>Vive com <strong className="text-white">dor no joelho</strong> pós-jogo.</span>
                            </li>
                            <li className="flex items-start gap-3">
                                <Activity className="text-gray-500 shrink-0 mt-1" />
                                <span>Não faz academia: acha "genérico e chato".</span>
                            </li>
                            <li className="flex items-start gap-3">
                                <span className="text-2xl">🚫</span>
                                <span>Acha que saúde de alta performance "não é pra ele".</span>
                            </li>
                        </ul>
                    </div>

                    <div className="bg-black/30 p-4 rounded-xl text-center border border-gray-700">
                        <span className="text-red-400 font-bold">O Problema:</span> Falta de Fortalecimento Específico
                    </div>
                </motion.div>

                {/* Persona 2: Cátia */}
                <motion.div
                    className="relative bg-gradient-to-br from-gray-800 to-gray-900 rounded-[2rem] p-10 flex flex-col justify-between overflow-hidden"
                    initial={{ x: 50, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: 0.3 }}
                >
                    <div className="absolute top-0 right-0 w-64 h-64 bg-purple-500/10 rounded-full blur-3xl -mr-16 -mt-16"></div>

                    <div>
                        <div className="flex items-center gap-4 mb-6">
                            <div className="w-20 h-20 bg-gray-700 rounded-full flex items-center justify-center text-3xl">👱‍♀️</div>
                            <div>
                                <h2 className="text-4xl font-bold text-white">Cátia</h2>
                                <p className="text-purple-400 text-xl">Beach Tennis + Musculação</p>
                            </div>
                        </div>

                        <ul className="space-y-6 text-xl text-gray-300">
                            <li className="flex items-start gap-3">
                                <TrendingUp className="text-yellow-400 shrink-0 mt-1" />
                                <span>Dedica-se muito, mas <strong className="text-white">estagnou (platô)</strong>.</span>
                            </li>
                            <li className="flex items-start gap-3">
                                <Zap className="text-gray-500 shrink-0 mt-1" />
                                <span>Treino da academia não ajuda na explosão da areia.</span>
                            </li>
                            <li className="flex items-start gap-3">
                                <span className="text-2xl">🔄</span>
                                <span>Esforço desalinhado com o objetivo.</span>
                            </li>
                        </ul>
                    </div>

                    <div className="bg-black/30 p-4 rounded-xl text-center border border-gray-700">
                        <span className="text-yellow-400 font-bold">O Problema:</span> Falta de Integração entre Práticas
                    </div>
                </motion.div>

            </div>
        </div>
    );
}
