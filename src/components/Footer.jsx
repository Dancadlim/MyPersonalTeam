import React from 'react';
import { User, Dumbbell, Activity, Heart, Brain, Send } from 'lucide-react';

const Footer = () => {
    return (
        <footer className="relative bg-gradient-to-t from-brand-primary/20 to-brand-darker pt-24 pb-12 overflow-hidden px-4 sm:px-6 lg:px-8">
            {/* Visual Decoration: Floating Nodes returning to center */}
            <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-20">
                <div className="absolute top-1/4 left-1/4 animate-bounce duration-[3s]"><Dumbbell className="w-12 h-12 text-white" /></div>
                <div className="absolute top-1/3 right-1/4 animate-bounce duration-[4s]"><Activity className="w-10 h-10 text-brand-primary" /></div>
                <div className="absolute bottom-1/3 left-1/3 animate-bounce duration-[5s]"><Heart className="w-8 h-8 text-yellow-500" /></div>
            </div>

            <div className="relative z-10 max-w-4xl mx-auto text-center">
                <h2 className="text-4xl sm:text-5xl font-extrabold text-white mb-6">
                    Pronto para Recrutar Seu <br />
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">Conselho de Especialistas?</span>
                </h2>

                <p className="text-xl text-gray-300 mb-10 max-w-2xl mx-auto">
                    O consenso chegou: É hora de atualizar sua saúde.
                </p>

                <div className="max-w-md mx-auto mb-12">
                    <form className="flex flex-col sm:flex-row gap-4" onSubmit={(e) => e.preventDefault()}>
                        <input
                            type="email"
                            placeholder="Seu melhor e-mail"
                            className="flex-1 px-6 py-4 rounded-full bg-white/10 border border-white/20 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-brand-primary backdrop-blur-sm"
                        />
                        <button className="px-8 py-4 bg-brand-primary hover:bg-blue-600 text-white font-bold rounded-full shadow-lg transform transition hover:scale-105 flex items-center justify-center gap-2">
                            Entrar na Lista <Send className="w-4 h-4" />
                        </button>
                    </form>
                    <p className="mt-4 text-sm text-gray-500">Junte-se a 5.000+ pessoas na lista de espera.</p>
                </div>

                <div className="flex flex-wrap justify-center gap-6 sm:gap-12 text-sm font-medium text-gray-400 pt-12 border-t border-white/10">
                    <a href="#" className="hover:text-white transition">Baixar MVP (Beta)</a>
                    <a href="#" className="hover:text-white transition">Para Treinadores</a>
                    <a href="#" className="hover:text-white transition">A Ciência Por Trás</a>
                </div>

                <div className="mt-12 text-xs text-gray-600">
                    © 2026 My Personal Team. Todos os direitos reservados.
                </div>
            </div>
        </footer>
    );
};

export default Footer;
