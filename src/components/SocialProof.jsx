import React from 'react';
import { Quote, Trophy, Users, Briefcase, Star, CheckCircle } from 'lucide-react';
import { motion } from 'framer-motion';

const SocialProof = () => {
    const testimonials = [
        {
            name: "Rafael M.",
            role: "Atleta Amador (Ironman)",
            quote: "Eu treinava muito, mas errado. A IA cruzou meus dados do Strava com minha rotina de sono e cortou 30% do meu volume. Resultado: baixei meu tempo em 40min sem lesões.",
            image: "https://images.unsplash.com/photo-1599058945522-28d584b6f0ff?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80", // Athlete
            badge: <Trophy className="w-4 h-4 text-yellow-400" />,
            badgeText: "Recorde Pessoal"
        },
        {
            name: "Dra. Juliana S.",
            role: "Advogada & Crossfiteira",
            quote: "Minha agenda é o caos. O 'Agente de Bem-Estar' remarca meus treinos automaticamente quando tenho reuniões tarde. É a primeira vez que não desisto no segundo mês.",
            image: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80", // Professional woman
            badge: <Briefcase className="w-4 h-4 text-blue-400" />,
            badgeText: "Consistência 100%"
        },
        {
            name: "Carlos E.",
            role: "Treinador de Boxe",
            quote: "Eu uso com meus alunos. A IA cuida da nutrição e recuperação, e eu foco na técnica. Meus atletas nunca chegaram tão inteiros nas lutas.",
            image: "https://images.unsplash.com/photo-1548690312-e3b507d8c110?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80", // Coach
            badge: <Users className="w-4 h-4 text-green-400" />,
            badgeText: "Parceiro Pro"
        }
    ];

    return (
        <section className="py-20 bg-brand-dark px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    className="text-center mb-16"
                >
                    <h2 className="text-3xl sm:text-4xl font-bold text-white mb-6">
                        Quem Usa Não Volta para o "Genérico"
                    </h2>
                    <p className="text-xl text-gray-400 max-w-2xl mx-auto">
                        De atletas de elite a executivos sem tempo. O resultado é o mesmo: performance real.
                    </p>
                </motion.div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {testimonials.map((item, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, y: 50 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: index * 0.2, duration: 0.6 }}
                            className="bg-brand-darker p-8 rounded-2xl relative border border-white/5 hover:border-brand-primary/30 transition duration-300 group"
                        >
                            <Quote className="absolute top-6 right-6 w-8 h-8 text-brand-primary/20 group-hover:text-brand-primary/40 transition" />

                            <div className="flex items-center gap-4 mb-6">
                                <img src={item.image} alt={item.name} className="w-14 h-14 rounded-full object-cover border-2 border-brand-primary" />
                                <div>
                                    <h4 className="text-white font-bold">{item.name}</h4>
                                    <span className="text-xs text-brand-primary font-medium tracking-wide flex items-center gap-1">
                                        {item.role}
                                    </span>
                                </div>
                            </div>

                            <p className="text-gray-300 italic leading-relaxed mb-6">
                                "{item.quote}"
                            </p>

                            <div className="inline-flex items-center gap-2 px-3 py-1 bg-white/5 rounded-full border border-white/10 text-xs font-semibold text-gray-300 group-hover:bg-brand-primary/10 group-hover:border-brand-primary/30 group-hover:text-brand-primary transition">
                                {item.badge}
                                {item.badgeText}
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default SocialProof;
