import React, { useState, useEffect } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';
import { User, Menu, X } from 'lucide-react';
import { Link } from 'react-router-dom';

const Navbar = () => {
    const { scrollY } = useScroll();
    const [isScrolled, setIsScrolled] = useState(false);
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    useEffect(() => {
        return scrollY.on("change", (latest) => {
            setIsScrolled(latest > 50);
        });
    }, [scrollY]);

    // Background animation variants
    const navVariants = {
        hidden: {
            backgroundColor: "rgba(10, 10, 10, 0)",
            backdropFilter: "blur(0px)",
            borderBottom: "1px solid rgba(255, 255, 255, 0)"
        },
        visible: {
            backgroundColor: "rgba(10, 10, 10, 0.8)",
            backdropFilter: "blur(12px)",
            borderBottom: "1px solid rgba(255, 255, 255, 0.1)"
        }
    };

    return (
        <motion.nav
            variants={navVariants}
            animate={isScrolled ? "visible" : "hidden"}
            transition={{ duration: 0.3 }}
            className="fixed top-0 left-0 right-0 z-50 px-6 py-4"
        >
            <div className="max-w-7xl mx-auto flex items-center justify-between">

                {/* Logo */}
                <div className="flex items-center gap-2">
                    <div className="w-8 h-8 bg-brand-primary rounded-lg flex items-center justify-center">
                        <User className="w-5 h-5 text-white" />
                    </div>
                    <span className="text-xl font-bold text-white tracking-tight">
                        My Personal <span className="text-brand-primary">Team</span>
                    </span>
                </div>

                {/* Desktop Menu */}
                <div className="hidden md:flex items-center gap-8">
                    <a href="#" className="text-sm font-medium text-gray-300 hover:text-white transition">O Conselho</a>
                    <a href="#" className="text-sm font-medium text-gray-300 hover:text-white transition">Como Funciona</a>
                    <a href="#" className="text-sm font-medium text-gray-300 hover:text-white transition">Resultados</a>

                    {/* Future Page Placeholder */}
                    <a href="#" className="text-sm font-medium text-gray-400 hover:text-brand-primary transition">Para Treinadores</a>
                </div>

                {/* CTA Button */}
                <div className="hidden md:block">
                    <Link to="/login" className="px-5 py-2 inline-block bg-white text-brand-dark font-bold rounded-full hover:bg-gray-200 transition text-sm">
                        Login MVP
                    </Link>
                </div>

                {/* Mobile Menu Toggle */}
                <div className="md:hidden">
                    <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="text-white">
                        {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
                    </button>
                </div>
            </div>

            {/* Mobile Menu Dropdown */}
            {isMobileMenuOpen && (
                <div className="absolute top-full left-0 right-0 bg-brand-darker border-b border-white/10 p-6 md:hidden flex flex-col gap-4 shadow-2xl">
                    <a href="#" className="text-gray-300 hover:text-white font-medium">O Conselho</a>
                    <a href="#" className="text-gray-300 hover:text-white font-medium">Como Funciona</a>
                    <a href="#" className="text-gray-300 hover:text-white font-medium">Resultados</a>
                    <a href="#" className="text-brand-primary hover:text-brand-primary/80 font-medium">Para Treinadores</a>
                    <Link to="/login" className="w-full py-3 text-center inline-block bg-brand-primary text-white font-bold rounded-xl mt-2">
                        Login MVP
                    </Link>
                </div>
            )}
        </motion.nav>
    );
};

export default Navbar;
