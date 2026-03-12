import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Hero from './components/Hero';
import WhyUseIt from './components/WhyUseIt';
import HowItWorks from './components/HowItWorks';
import SocialProof from './components/SocialProof';
import CallToAction from './components/CallToAction';
import Navbar from './components/Navbar';
import Login from './components/Login';
import Chat from './components/Chat';

function LandingPage() {
  return (
    <div className="min-h-screen bg-brand-darker text-white font-sans overflow-x-hidden">
      <Navbar />
      <Hero />
      <WhyUseIt />
      <HowItWorks />
      <SocialProof />
      <CallToAction />
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/chat" element={<Chat />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
