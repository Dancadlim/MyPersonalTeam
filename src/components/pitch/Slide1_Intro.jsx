import React from 'react';
import { motion } from 'framer-motion';

export default function Slide1_Intro() {
    return (
        <div className="flex flex-col items-center justify-center text-center h-full max-w-6xl w-full">
            <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ duration: 1, ease: "easeOut" }}
                className="mb-8"
            >
                <span className="text-8xl font-black bg-clip-text text-transparent bg-gradient-to-r from-blue-500 via-cyan-400 to-teal-300 drop-shadow-lg p-2">
                    My Personal Team
                </span>
            </motion.div>

            <motion.p
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.5, duration: 0.8 }}
                className="text-3xl text-gray-300 font-light tracking-widest uppercase"
            >
                O Primeiro Conselho de Saúde <br />
                <span className="font-bold text-white">Multi-Agente</span> do Mundo
            </motion.p>

            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 0.5 }}
                transition={{ delay: 1.5, duration: 1, repeat: Infinity, repeatType: "reverse" }}
                className="absolute bottom-12 text-sm uppercase tracking-[0.3em]"
            >
                Pressione Espaço para Iniciar
            </motion.div>
        </div>
    );
}
