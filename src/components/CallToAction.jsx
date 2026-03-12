import React from 'react';
import { ArrowRight, User, Dumbbell, Activity, Heart, Brain, Mail } from 'lucide-react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

const CallToAction = () => {
    return (
        <section className="relative py-24 px-4 sm:px-6 lg:px-8 overflow-hidden">
            {/* Background Gradient */}
            <div className="absolute inset-0 bg-gradient-to-br from-brand-dark via-brand-darker to-blue-900 z-0"></div>

            {/* Decorative Nodes (Floating back) */}
            <motion.div animate={{ y: [0, -10, 0] }} transition={{ repeat: Infinity, duration: 4, ease: "easeInOut" }} className="absolute top-10 left-10 text-white/5 animate-float-slow"><Dumbbell className="w-24 h-24" /></motion.div>
            <motion.div animate={{ y: [0, 10, 0] }} transition={{ repeat: Infinity, duration: 5, ease: "easeInOut", delay: 1 }} className="absolute bottom-10 right-10 text-white/5 animate-float-slow-reverse"><Activity className="w-32 h-32" /></motion.div>
            <motion.div animate={{ y: [0, -10, 0] }} transition={{ repeat: Infinity, duration: 3, ease: "easeInOut", delay: 0.5 }} className="absolute top-1/2 right-0 text-white/5 transform translate-x-1/2"><Brain className="w-64 h-64" /></motion.div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
                className="max-w-4xl mx-auto relative z-10 text-center"
            >
                <div className="inline-flex items-center justify-center p-3 mb-8 rounded-full bg-brand-primary/20 border border-brand-primary/50 backdrop-blur-sm">
                    <User className="w-5 h-5 text-brand-primary mr-2" />
                    <span className="text-brand-primary font-semibold tracking-wide uppercase text-sm">Vagas Limitadas para o Beta</span>
                </div>

                <h2 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-white tracking-tight mb-6">
                    Pronto para Recrutar Seu <br />
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">
                        Conselho de Especialistas?
                    </span>
                </h2>

                <p className="text-xl text-gray-300 mb-10 max-w-2xl mx-auto">
                    O consenso chegou: É hora de atualizar sua saúde. Pare de treinar sozinho e comece a treinar com um time.
                </p>

                <form className="max-w-lg mx-auto flex flex-col sm:flex-row gap-4 mb-8">
                    <input
                        type="email"
                        placeholder="Seu melhor e-mail"
                        className="flex-1 px-6 py-4 rounded-full bg-white/10 border border-white/20 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-brand-primary focus:border-transparent transition"
                    />
                    <button className="px-8 py-4 bg-brand-primary hover:bg-blue-600 text-white font-bold rounded-full shadow-lg transform transition hover:scale-105 flex items-center justify-center gap-2">
                        Entrar na Lista
                        <ArrowRight className="w-5 h-5" />
                    </button>
                </form>

                <div className="flex flex-col sm:flex-row items-center justify-center gap-6 text-sm text-gray-500">
                    <Link to="/login" className="hover:text-white transition">Testar Chat MVP</Link>
                    <span className="hidden sm:inline">•</span>
                    <a href="#" className="hover:text-white transition">Para Treinadores</a>
                    <span className="hidden sm:inline">•</span>
                    <a href="#" className="hover:text-white transition">A Ciência Por Trás</a>
                </div>
            </motion.div>
        </section>
    );
};

export default CallToAction;
