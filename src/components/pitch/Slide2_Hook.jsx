import React from 'react';
import { motion } from 'framer-motion';
import { Users, UserMinus, UserX } from 'lucide-react';

export default function Slide2_Hook() {
    return (
        <div className="flex flex-col items-center justify-center text-center h-full w-full">
            <motion.h1
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="text-7xl font-bold mb-20 text-white"
            >
                Quem cuida de você?
            </motion.h1>

            <div className="flex justify-around w-full max-w-5xl px-8">

                {/* Stage 1: Practicing Sports */}
                <motion.div
                    initial={{ opacity: 0, y: 50 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 }}
                    className="flex flex-col items-center"
                >
                    <div className="flex space-x-2 text-green-400 mb-4">
                        <Users size={64} />
                        <Users size={64} />
                        <Users size={64} />
                    </div>
                    <p className="text-xl text-gray-400">Praticam Esporte</p>
                    <p className="text-3xl font-bold mt-2">100%</p>
                </motion.div>

                {/* Stage 2: Has Trainer */}
                <motion.div
                    initial={{ opacity: 0, y: 50 }}
                    animate={{ opacity: 0.5, y: 0 }} // Faded out to represent drop
                    transition={{ delay: 1.5 }}
                    className="flex flex-col items-center opacity-50"
                >
                    <div className="flex space-x-2 text-yellow-400 mb-4">
                        <Users size={64} />
                        <UserMinus size={64} className="text-gray-700" />
                        <UserMinus size={64} className="text-gray-700" />
                    </div>
                    <p className="text-xl text-gray-500">Com Personal Trainer</p>
                    <p className="text-3xl font-bold mt-2 text-yellow-600">~15%</p>
                </motion.div>

                {/* Stage 3: Has Team */}
                <motion.div
                    initial={{ opacity: 0, y: 50 }}
                    animate={{ opacity: 1, y: 0 }} // Back to full opacity for impact
                    transition={{ delay: 3 }}
                    className="flex flex-col items-center"
                >
                    <div className="flex space-x-2 text-red-500 mb-4">
                        <UserX size={64} />
                        <UserX size={64} />
                        <Users size={64} className="text-transparent" /> {/* Spacer */}
                    </div>
                    <p className="text-xl text-red-400">Com Equipe Completa</p>
                    <p className="text-5xl font-black mt-2 text-red-500">{"<"}1%</p>
                </motion.div>

            </div>
        </div>
    );
}
