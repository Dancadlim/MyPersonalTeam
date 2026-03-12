import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = (e) => {
        e.preventDefault();
        // For this mock login, we just accept any non-empty input
        if (username && password) {
            console.log('Login successful');
            navigate('/chat');
        }
    };

    return (
        <div className="min-h-screen bg-brand-darker flex justify-center items-center font-sans">
            <div className="bg-brand-dark p-8 rounded-lg shadow-xl w-full max-w-md border border-brand-accent/20">
                <h2 className="text-3xl font-bold mb-6 text-white text-center">Login to My Personal Team</h2>
                <form onSubmit={handleLogin} className="space-y-4">
                    <div>
                        <label className="block text-brand-light mb-2 text-sm">Username</label>
                        <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="w-full p-3 rounded bg-brand-darker border border-brand-accent/50 text-white focus:outline-none focus:border-brand-primary transition-colors"
                            placeholder="Enter any username"
                            required
                        />
                    </div>
                    <div>
                        <label className="block text-brand-light mb-2 text-sm">Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full p-3 rounded bg-brand-darker border border-brand-accent/50 text-white focus:outline-none focus:border-brand-primary transition-colors"
                            placeholder="Enter any password"
                            required
                        />
                    </div>
                    <button
                        type="submit"
                        className="w-full bg-brand-primary hover:bg-brand-primary/80 text-brand-darker font-bold py-3 rounded transition-colors mt-6"
                    >
                        Log In
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Login;
