import React from 'react';
import { motion } from 'framer-motion';
import { Dumbbell, Activity, Apple, Heart, Brain, ArrowDown } from 'lucide-react';

const AgentNode = ({ icon: Icon, color, label, delay, position }) => (
    <motion.div
        className={`absolute flex flex-col items-center justify-center ${position}`}
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ delay, type: "spring", stiffness: 200, damping: 20 }}
    >
        <div className={`w-28 h-28 rounded-full bg-gray-900 border-4 ${color} flex items-center justify-center z-20 shadow-[0_0_30px_rgba(0,0,0,0.5)]`}>
            <Icon size={40} className="text-white" />
        </div>
        <div className={`mt-4 px-4 py-2 bg-gray-900/80 rounded-full border border-gray-700 text-white font-bold backdrop-blur-md z-20`}>
            {label}
        </div>
    </motion.div>
);

const ConnectionLine = ({ rotation, delay }) => (
    <motion.div
        className="absolute top-1/2 left-1/2 w-[250px] h-[2px] bg-gradient-to-r from-cyan-500/0 via-cyan-500 to-cyan-500/0 origin-left z-0"
        style={{ rotate: rotation }}
        initial={{ scaleX: 0, opacity: 0 }}
        animate={{ scaleX: 1, opacity: 1 }}
        transition={{ delay, duration: 1 }}
    />
);

export default function Slide5_Solution() {
    return (
        <div className="relative w-full h-full flex items-center justify-center overflow-hidden">

            {/* Central Consensus Engine */}
            <motion.div
                className="z-10 relative flex flex-col items-center"
                initial={{ scale: 0.5, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: 2, duration: 0.8 }}
            >
                <div className="w-48 h-48 rounded-full bg-gradient-to-br from-cyan-600 to-blue-700 flex items-center justify-center shadow-[0_0_100px_rgba(0,255,255,0.3)] animate-pulse-slow">
                    <Brain size={80} className="text-white" />
                </div>
                <h1 className="mt-8 text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-white tracking-tight">
                    CONSENSO
                </h1>
                <p className="text-cyan-200 uppercase tracking-[0.5em] text-sm mt-2">Junta Médica de IA</p>
            </motion.div>

            {/* Agents Orbiting */}
            <div className="absolute inset-0 w-full h-full">
                {/* Top Left - Personal */}
                <AgentNode
                    icon={Dumbbell}
                    color="border-red-500 shadow-red-500/30"
                    label="Treinador"
                    position="top-[15%] left-[20%]"
                    delay={0.2}
                />
                <ConnectionLine rotation="145deg" delay={2.5} /> {/* Visual approximation */}

                {/* Top Right - Nutri */}
                <AgentNode
                    icon={Apple}
                    color="border-green-500 shadow-green-500/30"
                    label="Nutricionista"
                    position="top-[15%] right-[20%]"
                    delay={0.4}
                />

                {/* Bottom Left - Physio */}
                <AgentNode
                    icon={Activity}
                    color="border-blue-500 shadow-blue-500/30"
                    label="Fisioterapeuta"
                    position="bottom-[15%] left-[20%]"
                    delay={0.6}
                />

                {/* Bottom Right - Wellness */}
                <AgentNode
                    icon={Heart}
                    color="border-yellow-500 shadow-yellow-500/30"
                    label="Bem-Estar"
                    position="bottom-[15%] right-[20%]"
                    delay={0.8}
                />
            </div>

            {/* Connecting Beams (Simplified visual) */}
            <motion.svg className="absolute inset-0 w-full h-full pointer-events-none z-0" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 2.5 }}>
                {/* Draw lines from center to positions. Approximated coordinates based on % above */}
                <line x1="50%" y1="50%" x2="25%" y2="25%" stroke="url(#grad)" strokeWidth="2" strokeDasharray="5,5" />
                <line x1="50%" y1="50%" x2="75%" y2="25%" stroke="url(#grad)" strokeWidth="2" strokeDasharray="5,5" />
                <line x1="50%" y1="50%" x2="25%" y2="75%" stroke="url(#grad)" strokeWidth="2" strokeDasharray="5,5" />
                <line x1="50%" y1="50%" x2="75%" y2="75%" stroke="url(#grad)" strokeWidth="2" strokeDasharray="5,5" />

                <defs>
                    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor="#22d3ee" stopOpacity="0" />
                        <stop offset="50%" stopColor="#22d3ee" stopOpacity="1" />
                        <stop offset="100%" stopColor="#22d3ee" stopOpacity="0" />
                    </linearGradient>
                </defs>
            </motion.svg>

            {/* Veto/Approve Examples - Appearing one by one */}
            <motion.div
                className="absolute top-1/2 left-10 transform -translate-y-1/2 bg-red-900/80 border border-red-500 p-4 rounded-xl max-w-xs text-sm"
                initial={{ x: -50, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 3.5 }}
            >
                <strong className="text-red-400 block mb-1">VETO (Fisio):</strong>
                "Treino de alto impacto vetado devido ao joelho do Mario."
            </motion.div>

            <motion.div
                className="absolute top-1/2 right-10 transform -translate-y-1/2 bg-green-900/80 border border-green-500 p-4 rounded-xl max-w-xs text-sm"
                initial={{ x: 50, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 4.5 }}
            >
                <strong className="text-green-400 block mb-1">AJUSTE (Nutri):</strong>
                "Aumento de carboidrato para dia de jogo da Cátia."
            </motion.div>

        </div>
    );
}
