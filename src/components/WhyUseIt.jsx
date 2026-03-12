import React from 'react';
import { AlertTriangle, TrendingDown, Activity, ShieldAlert, Brain, CircleDollarSign } from 'lucide-react';
import { motion } from 'framer-motion';

const WhyUseIt = () => {
    const cards = [
        {
            title: "A Barreira Financeira",
            stat: "R$ 3.200",
            desc: "é o custo mensal médio de uma equipe multidisciplinar (Personal, Nutri, Fisioterapeuta).",
            insight: "Nós democratizamos a alta performance por uma fração desse valor.",
            source: "Relatório de Custos e Mercado 2025",
            icon: <CircleDollarSign className="w-8 h-8 text-green-400" />,
            borderColor: "border-green-500/50"
        },
        {
            title: "O Novo Antidepressivo",
            stat: "1.5x",
            desc: "mais eficaz que medicação para depressão leve e ansiedade.",
            insight: "Brasil é o país mais ansioso do mundo. Seu treino é sua terapia biológica.",
            source: "British Journal of Sports Medicine / OMS",
            icon: <Brain className="w-8 h-8 text-purple-400" />,
            borderColor: "border-purple-500/50"
        },
        {
            title: "O Risco da Moda",
            stat: "48%",
            desc: "dos praticantes de Beach Tennis já sofreram lesões por falta de preparo específico.",
            insight: "Mudar de esporte exige mudar de treino. O genérico te machuca.",
            source: "Epidemiologia Esportiva 2025",
            icon: <ShieldAlert className="w-8 h-8 text-red-500" />,
            borderColor: "border-red-500/50"
        },
        {
            title: "O Paradoxo do Suplemento",
            stat: "91%",
            desc: "tomam suplementos, mas 64% não têm orientação nutricional profissional.",
            insight: "Você está gastando dinheiro caro para produzir urina cara. Otimize.",
            source: "Panorama Setorial Fitness Brasil 2025",
            icon: <AlertTriangle className="w-8 h-8 text-yellow-500" />,
            borderColor: "border-yellow-500/50"
        }
    ];

    const container = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: {
                staggerChildren: 0.2
            }
        }
    };

    const item = {
        hidden: { opacity: 0, y: 50 },
        visible: { opacity: 1, y: 0, transition: { duration: 0.6 } }
    };

    return (
        <section className="py-20 bg-brand-dark px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    className="text-center mb-16"
                >
                    <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
                        Isso não é Luxo. É <span className="text-red-500">Sobrevivência</span>.
                    </h2>
                    <p className="text-xl text-gray-400">
                        Os dados do Relatório Estratégico 2025 mostram por que você precisa de um time agora.
                    </p>
                </motion.div>

                <motion.div
                    variants={container}
                    initial="hidden"
                    whileInView="visible"
                    viewport={{ once: true, margin: "-100px" }}
                    className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-8"
                >
                    {cards.map((card, index) => (
                        <motion.div variants={item} key={index} className={`bg-brand-darker p-8 rounded-2xl border ${card.borderColor} hover:border-opacity-100 transition duration-300 transform hover:-translate-y-2 flex flex-col h-full relative overflow-hidden group shadow-2xl`}>

                            {/* Header: Icon + Label */}
                            <div className="flex justify-between items-start mb-6">
                                <div className="bg-white/5 p-3 rounded-xl group-hover:bg-white/10 transition">
                                    {card.icon}
                                </div>
                                <div className="text-right">
                                    <div className="text-[10px] text-gray-500 uppercase tracking-[0.2em] font-bold mb-1">DADO CRÍTICO</div>
                                    <div className="text-[10px] text-gray-600 font-mono">{card.source}</div>
                                </div>
                            </div>

                            {/* Stat Block with Title First */}
                            <div className="mb-4">
                                <h3 className="text-xl font-bold text-gray-200 leading-tight mb-2">{card.title}</h3>
                                <div className="text-5xl font-black text-white tracking-tighter mb-1">{card.stat}</div>
                            </div>

                            {/* Description */}
                            <p className="text-gray-400 text-sm leading-relaxed mb-8 flex-grow">
                                {card.desc}
                            </p>

                            {/* Insight Footer */}
                            <div className="bg-brand-dark/50 border border-white/5 p-4 rounded-xl mt-auto relative overflow-hidden">
                                <div className="absolute left-0 top-0 bottom-0 w-1 bg-brand-primary"></div>
                                <span className="text-brand-primary text-[10px] font-bold uppercase mb-1 block tracking-wider">O Insight</span>
                                <p className="text-sm text-gray-300 italic">
                                    "{card.insight}"
                                </p>
                            </div>
                        </motion.div>
                    ))}
                </motion.div>
            </div>
        </section>
    );
};

export default WhyUseIt;
