import React, { useState, useEffect } from 'react';
import { User, Dumbbell, Activity, ShieldAlert, CheckCircle, RefreshCw, Trophy, Play, HeartPulse, Brain } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const HowItWorks = () => {
    const scenarios = {
        sports: [
            {
                step: "Passo 0: Contexto Esportivo",
                icon: <Trophy className="w-6 h-6 text-white" />,
                agent: "Treinador Esportivo",
                agentColor: "bg-orange-500",
                content: (
                    <div>
                        <div className="text-xs text-gray-400 mb-1">Entrada: "Jogo Tênis 2x na semana e sinto o ombro."</div>
                        <div className="font-semibold text-orange-300">Diretriz: "Prioridade em estabilidade de manguito e potência rotacional."</div>
                    </div>
                )
            },
            {
                step: "Passo 1: A Proposta",
                icon: <Dumbbell className="w-6 h-6 text-white" />,
                agent: "Personal Trainer",
                agentColor: "bg-red-500",
                content: (
                    <div>
                        <div className="font-semibold text-white">Sugestão: "Supino Reto com Barra (4x8) para força bruta."</div>
                    </div>
                )
            },
            {
                step: "Passo 2: O Veto",
                icon: <ShieldAlert className="w-6 h-6 text-white" />,
                agent: "Fisioterapeuta",
                agentColor: "bg-blue-500",
                isVeto: true,
                content: (
                    <div>
                        <div className="flex items-center gap-2 text-red-400 font-bold mb-1"><ShieldAlert className="w-4 h-4" /> VETO</div>
                        <div className="text-gray-300">"Risco: Supino barra trava a escápula. Perigoso para quem já tem dor no ombro."</div>
                        <div className="text-blue-300">"Ajuste: Supino com Halteres (mais liberdade) + Rotação Externa."</div>
                    </div>
                )
            },
            {
                step: "Passo 3: O Combustível",
                icon: <div className="text-white">⚡</div>,
                agent: "Nutricionista",
                agentColor: "bg-emerald-500",
                content: (
                    <div>
                        <div className="text-emerald-300 font-semibold mb-1">Performance</div>
                        <div className="text-gray-300">"Tênis exige explosão. Adicionando Beta-Alanina e Carboidrato de rápida absorção pré-jogo."</div>
                    </div>
                )
            },
            {
                step: "Passo 4: O Mental",
                icon: <HeartPulse className="w-6 h-6 text-white" />,
                agent: "Agente de Bem-Estar",
                agentColor: "bg-purple-500",
                content: (
                    <div>
                        <div className="text-purple-300 font-semibold mb-1">Recuperação & Foco</div>
                        <div className="text-gray-300">"Monitorando VFC. Carga de treino reduzida na véspera dos jogos para frescor neuromuscular."</div>
                    </div>
                )
            },
            {
                step: "Passo 5: O Consenso",
                icon: <CheckCircle className="w-6 h-6 text-white" />,
                agent: "Sistema",
                agentColor: "bg-brand-primary",
                isConsensus: true,
                content: (
                    <div className="bg-green-500/10 p-4 rounded-lg border border-green-500/30">
                        <div className="text-green-400 font-bold mb-1">PROTOCOL ADEQUADO</div>
                        <div className="text-white">"Força Específica + Prevenção de Lesão + Timing Nutricional."</div>
                    </div>
                )
            }
        ],
        general: [
            {
                step: "Passo 1: A Proposta Base",
                icon: <Dumbbell className="w-6 h-6 text-white" />,
                agent: "Personal Trainer",
                agentColor: "bg-red-500",
                content: (
                    <div>
                        <div className="text-xs text-gray-400 mb-1">Objetivo: "Hipertrofia Acelerada"</div>
                        <div className="font-semibold text-white">Sugestão: "Treino ABC 6x na semana (Alto Volume). Foco em carga máxima."</div>
                    </div>
                )
            },
            {
                step: "Passo 2: A Proteção",
                icon: <ShieldAlert className="w-6 h-6 text-white" />,
                agent: "Fisioterapeuta",
                agentColor: "bg-blue-500",
                isVeto: true,
                content: (
                    <div>
                        <div className="flex items-center gap-2 text-red-400 font-bold mb-1"><ShieldAlert className="w-4 h-4" /> ALERTA</div>
                        <div className="text-gray-300">"Histórico de lombar e 8h sentado/dia. Agachamento livre com carga máxima é perigoso agora."</div>
                        <div className="text-blue-300">"Ajuste: Mudando para Agachamento Unilateral e fortalecimento de Core prévio."</div>
                    </div>
                )
            },
            {
                step: "Passo 3: O Combustível",
                icon: <div className="text-white">🍏</div>,
                agent: "Nutricionista",
                agentColor: "bg-emerald-500",
                content: (
                    <div>
                        <div className="text-emerald-300 font-semibold mb-1">Aporte Calórico</div>
                        <div className="text-gray-300">"Para sustentar esse volume com segurança, precisamos de superávit. Adicionando refeição intra-treino."</div>
                    </div>
                )
            },
            {
                step: "Passo 4: A Realidade",
                icon: <HeartPulse className="w-6 h-6 text-white" />,
                agent: "Agente de Bem-Estar",
                agentColor: "bg-purple-500",
                content: (
                    <div>
                        <div className="text-purple-300 font-semibold mb-1">Analise de Rotina</div>
                        <div className="text-gray-300">"Usuário tem reuniões até tarde na quinta-feira. Treino de perna movido para sábado para garantir descanso."</div>
                    </div>
                )
            },
            {
                step: "Passo 5: O Consenso",
                icon: <CheckCircle className="w-6 h-6 text-white" />,
                agent: "Sistema",
                agentColor: "bg-brand-primary",
                isConsensus: true,
                content: (
                    <div className="bg-green-500/10 p-4 rounded-lg border border-green-500/30">
                        <div className="text-green-400 font-bold mb-1">PLANO FINAL</div>
                        <div className="text-white">"Treino 5x Seguro + Dieta Ajustada + Descanso Otimizado."</div>
                    </div>
                )
            }
        ]
    };

    const [simulationState, setSimulationState] = useState('idle'); // idle, choosing, running, completed
    const [visibleCount, setVisibleCount] = useState(0);
    const [activeScenario, setActiveScenario] = useState([]);

    const startChoice = () => {
        setSimulationState('choosing');
    };

    const runScenario = (type) => {
        // Randomize specific scenario if we had multiple variants, for now hardcoded types
        setActiveScenario(scenarios[type]);
        setSimulationState('running');
        setVisibleCount(0);
    };

    useEffect(() => {
        if (simulationState === 'running') {
            if (visibleCount < activeScenario.length) {
                const timer = setTimeout(() => {
                    setVisibleCount((prev) => prev + 1);
                }, 2000); // 2.0 seconds per step
                return () => clearTimeout(timer);
            } else {
                setSimulationState('completed');
            }
        }
    }, [simulationState, visibleCount, activeScenario.length]);

    return (
        <section className="py-20 bg-brand-darker relative overflow-hidden px-4 sm:px-6 lg:px-8">
            {/* Background decorations */}
            <div className="absolute top-0 right-0 w-1/3 h-full bg-blue-900/10 blur-3xl pointer-events-none"></div>
            <div className="absolute bottom-0 left-0 w-1/3 h-full bg-emerald-900/10 blur-3xl pointer-events-none"></div>

            <div className="max-w-4xl mx-auto relative z-10">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    className="text-center mb-16"
                >
                    <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
                        Por Dentro do <span className="text-brand-primary">Motor de Consenso</span>
                    </h2>
                    <p className="text-xl text-gray-400 mb-8 max-w-2xl mx-auto">
                        Assista seu time debater em tempo real. Nenhuma decisão é tomada isoladamente.
                    </p>

                    <AnimatePresence mode="wait">
                        {simulationState === 'idle' && (
                            <motion.button
                                key="start-btn"
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.9 }}
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={startChoice}
                                className="inline-flex items-center gap-2 px-8 py-4 bg-brand-primary hover:bg-blue-600 text-white font-bold rounded-full shadow-lg transition text-lg animate-pulse"
                            >
                                <Play className="w-5 h-5 fill-current" />
                                Simular Debate
                            </motion.button>
                        )}

                        {simulationState === 'choosing' && (
                            <motion.div
                                key="choice-card"
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -20 }}
                                className="bg-white/5 backdrop-blur-md border border-white/10 p-8 rounded-2xl max-w-lg mx-auto shadow-2xl"
                            >
                                <h3 className="text-xl font-bold text-white mb-6">Seu objetivo envolve melhorar performance em um esporte específico?</h3>
                                <div className="flex gap-4 justify-center">
                                    <button
                                        onClick={() => runScenario('sports')}
                                        className="flex-1 py-3 px-6 bg-orange-500 hover:bg-orange-600 text-white font-bold rounded-xl transition flex flex-col items-center gap-2"
                                    >
                                        <Trophy className="w-6 h-6" />
                                        <span>Sim! (Tênis, Corrida...)</span>
                                    </button>
                                    <button
                                        onClick={() => runScenario('general')}
                                        className="flex-1 py-3 px-6 bg-brand-dark hover:bg-gray-800 border border-white/10 text-white font-bold rounded-xl transition flex flex-col items-center gap-2"
                                    >
                                        <Dumbbell className="w-6 h-6" />
                                        <span>Não (Academia/Estilo de Vida)</span>
                                    </button>
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </motion.div>

                <div className="relative min-h-[600px]">
                    {/* Background Gray Line (Always Visible) */}
                    <div className="absolute left-8 sm:left-1/2 top-0 bottom-0 w-0.5 bg-gray-800 transform -translate-x-1/2"></div>

                    {/* Fluid Red Line (The "Scanner") */}
                    {simulationState === 'running' && (
                        <motion.div
                            initial={{ height: 0 }}
                            animate={{ height: "100%" }}
                            transition={{ duration: activeScenario.length * 2, ease: "linear" }}
                            className="absolute left-8 sm:left-1/2 top-0 w-0.5 bg-gradient-to-b from-red-600 to-red-400 shadow-[0_0_15px_rgba(239,68,68,0.8)] transform -translate-x-1/2 z-10"
                        >
                            {/* Glowing Head (Laser Tip) */}
                            <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 translate-y-1/2 w-3 h-3 bg-red-500 rounded-full shadow-[0_0_20px_rgba(239,68,68,1)] animate-pulse"></div>
                        </motion.div>
                    )}

                    <div className="space-y-12 pb-12">
                        {simulationState !== 'idle' && simulationState !== 'choosing' && activeScenario.map((item, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{
                                    opacity: index <= visibleCount ? 1 : 0.1,
                                    y: index <= visibleCount ? 0 : 20,
                                    filter: index <= visibleCount ? "blur(0px)" : "blur(4px)"
                                }}
                                transition={{ duration: 0.5 }}
                                className={`relative flex flex-col sm:flex-row items-start ${index % 2 === 0 ? 'sm:flex-row-reverse' : ''} gap-8`}
                            >
                                {/* Timeline Dot */}
                                <div className={`absolute left-8 sm:left-1/2 transform -translate-x-1/2 mt-6 z-20 transition-all duration-500 ${index <= visibleCount ? 'scale-100' : 'scale-0'}`}>
                                    <div className={`w-4 h-4 bg-brand-darker border-2 ${item.isVeto ? 'border-red-500' : item.isConsensus ? 'border-green-500' : 'border-brand-primary'} rounded-full relative`}>
                                        {index === visibleCount && simulationState === 'running' && (
                                            <span className={`absolute inset-0 rounded-full ${item.isVeto ? 'bg-red-500' : 'bg-brand-primary'} animate-ping opacity-75`}></span>
                                        )}
                                    </div>
                                </div>

                                {/* Content Bubble */}
                                <div className="w-full sm:w-1/2 pl-20 sm:pl-0">
                                    <div className={`relative bg-brand-dark/40 backdrop-blur-sm border ${item.isVeto ? 'border-red-500/50 shadow-[0_0_15px_rgba(239,68,68,0.2)]' : item.isConsensus ? 'border-green-500/50 shadow-[0_0_15px_rgba(34,197,94,0.2)]' : 'border-white/10'} p-6 rounded-2xl shadow-xl transition-all duration-500 group ${index <= visibleCount ? 'translate-x-0' : index % 2 === 0 ? 'translate-x-10' : '-translate-x-10'}`}>

                                        {/* Connector Line/Arrow */}
                                        <div className={`hidden sm:block absolute top-8 w-4 h-4 bg-white/5 border-t border-l ${item.isVeto ? 'border-red-500/50' : item.isConsensus ? 'border-green-500/50' : 'border-white/10'} transform rotate-45 ${index % 2 === 0 ? '-right-2' : '-left-2'} `}></div>

                                        {/* Header */}
                                        <div className="flex items-center gap-3 mb-4">
                                            <div className={`w-10 h-10 ${item.agentColor} rounded-full flex items-center justify-center shadow-lg relative`}>
                                                {item.icon}
                                            </div>
                                            <div>
                                                <div className="text-xs text-gray-400 uppercase tracking-widest">{item.step}</div>
                                                <div className="font-bold text-white">{item.agent}</div>
                                            </div>
                                        </div>

                                        {/* Body */}
                                        <div className="text-sm text-gray-300">
                                            {item.content}
                                        </div>
                                    </div>
                                </div>

                                {/* Empty side for layout balance */}
                                <div className="hidden sm:block w-1/2"></div>
                            </motion.div>
                        ))}
                    </div>
                </div>

                <div className="mt-16 text-center">
                    {simulationState === 'completed' && (
                        <motion.button
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            onClick={startChoice}
                            className="inline-flex items-center gap-2 px-6 py-3 bg-white/5 hover:bg-white/10 border border-white/20 rounded-full text-white transition font-medium"
                        >
                            <RefreshCw className="w-4 h-4" />
                            Testar Outro Cenário
                        </motion.button>
                    )}
                </div>
            </div>
        </section>
    );
};

export default HowItWorks;
