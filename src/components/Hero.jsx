import React from 'react';
import { Activity, Heart, Brain, Dumbbell, User, Trophy } from 'lucide-react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

const Hero = () => {
    return (
        <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-b from-brand-darker to-brand-dark pt-20 pb-20 px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl w-full grid grid-cols-1 lg:grid-cols-2 gap-12 items-center z-10">

                {/* Copy Section */}
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    className="space-y-8 text-center lg:text-left"
                >
                    <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-tight">
                        <span className="block text-white">Cinco Especialistas.</span>
                        <span className="block text-brand-primary">Um Consenso.</span>
                        <span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">
                            Seu Plano Perfeito.
                        </span>
                    </h1>

                    <motion.p
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.4, duration: 0.8 }}
                        className="text-lg sm:text-xl text-gray-300 max-w-2xl mx-auto lg:mx-0"
                    >
                        Pare de adivinhar. Tenha um <strong>Conselho de 5 Especialistas de IA</strong> dedicados exclusivamente à sua biologia e rotina. Treino, Nutrição e Recuperação em perfeita sintonia.
                    </motion.p>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.6, duration: 0.5 }}
                        className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4"
                    >
                        <Link to="/login" className="w-full sm:w-auto text-center inline-block px-8 py-4 bg-brand-primary hover:bg-blue-600 text-white font-bold rounded-full shadow-lg transform transition hover:scale-105">
                            Iniciar Minha Sessão com o Conselho
                        </Link>
                        <button className="w-full sm:w-auto inline-block px-8 py-4 bg-transparent border border-gray-600 hover:border-white text-gray-300 hover:text-white font-semibold rounded-full transition">
                            Veja Como Funciona
                        </button>
                    </motion.div>
                </motion.div>

                {/* Visual / Animation Section */}
                <div className="relative h-[400px] sm:h-[500px] flex items-center justify-center">
                    {/* User Node (Center) */}
                    <div className="relative z-20 w-24 h-24 bg-white rounded-full flex items-center justify-center shadow-[0_0_30px_rgba(255,255,255,0.3)]">
                        <User className="w-12 h-12 text-brand-darker" />
                        <div className="absolute inset-0 rounded-full border-2 border-white/50 animate-ping opacity-20"></div>
                    </div>

                    {/* Orbit Container */}
                    <div className="absolute inset-0 flex items-center justify-center animate-orbit">
                        {/* Agent 1: Personal Trainer (Red) - Top */}
                        <motion.div whileHover={{ scale: 1.2 }} className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 w-16 h-16 bg-red-500 rounded-full flex items-center justify-center shadow-lg transform -rotate-0 cursor-pointer z-30">
                            <Dumbbell className="w-8 h-8 text-white" />
                            <div className="absolute top-16 left-1/2 w-0.5 h-[calc(50%-4rem)] bg-gradient-to-b from-red-500/50 to-transparent origin-top pointer-events-none"></div>
                        </motion.div>

                        {/* Agent 2: Physiotherapist (Blue) - Top Right */}
                        <motion.div whileHover={{ scale: 1.2 }} className="absolute top-[30%] right-[10%] w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center shadow-lg transform -rotate-[72deg] cursor-pointer z-30">
                            <Activity className="w-8 h-8 text-white" />
                        </motion.div>

                        {/* Agent 3: Nutritionist (Green) - Bottom Right */}
                        <motion.div whileHover={{ scale: 1.2 }} className="absolute bottom-[10%] right-[20%] w-16 h-16 bg-emerald-500 rounded-full flex items-center justify-center shadow-lg transform -rotate-[144deg] cursor-pointer z-30">
                            <div className="text-2xl">🍏</div>
                        </motion.div>

                        {/* Agent 4: Wellness Coach (Yellow) - Bottom Left */}
                        <motion.div whileHover={{ scale: 1.2 }} className="absolute bottom-[10%] left-[20%] w-16 h-16 bg-yellow-500 rounded-full flex items-center justify-center shadow-lg transform -rotate-[216deg] cursor-pointer z-30">
                            <Heart className="w-8 h-8 text-white" />
                        </motion.div>

                        {/* Agent 5: Biomedical Analyst (Purple) - Top Left */}
                        <motion.div whileHover={{ scale: 1.2 }} className="absolute top-[30%] left-[10%] w-16 h-16 bg-purple-500 rounded-full flex items-center justify-center shadow-lg transform -rotate-[288deg] cursor-pointer z-30">
                            <Brain className="w-8 h-8 text-white" />
                        </motion.div>

                        {/* Agent 6: Sports Coach (Orange) - New Position */}
                        <motion.div whileHover={{ scale: 1.2 }} className="absolute top-[50%] left-[-5%] w-16 h-16 bg-orange-500 rounded-full flex items-center justify-center shadow-lg transform -rotate-[320deg] cursor-pointer z-30">
                            <Trophy className="w-8 h-8 text-white" />
                        </motion.div>
                    </div>

                    {/* Connecting Lines (Static for now, implies connectivity) */}
                    <div className="absolute inset-0 pointer-events-none">
                        <svg className="w-full h-full opacity-30">
                            <circle cx="50%" cy="50%" r="30%" fill="none" stroke="currentColor" strokeWidth="1" className="text-gray-700" strokeDasharray="5,5" />
                        </svg>
                    </div>

                </div>
            </div>
        </section>
    );
};

export default Hero;
