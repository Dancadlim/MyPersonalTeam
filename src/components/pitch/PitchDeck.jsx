import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

// Import slides (we will create these next)
import Slide1_Intro from './Slide1_Intro';
import Slide2_Hook from './Slide2_Hook';
import Slide3_Problem from './Slide3_Problem';
import Slide4_Personas from './Slide4_Personas';
import Slide5_Solution from './Slide5_Solution';
import Slide6_Value from './Slide6_Value';

const SLIDES = [
  Slide1_Intro,
  Slide2_Hook,
  Slide3_Problem,
  Slide4_Personas,
  Slide5_Solution,
  Slide6_Value,
];

export default function PitchDeck() {
  const [currentSlide, setCurrentSlide] = useState(0);

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'ArrowRight' || e.key === 'Space') {
        setCurrentSlide((prev) => Math.min(prev + 1, SLIDES.length - 1));
      } else if (e.key === 'ArrowLeft') {
        setCurrentSlide((prev) => Math.max(prev - 1, 0));
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const CurrentSlideComponent = SLIDES[currentSlide];

  return (
    <div className="relative w-screen h-screen bg-black overflow-hidden text-white font-sans selection:bg-cyan-500 selection:text-black">
      {/* Progress Bar */}
      <div className="absolute top-0 left-0 w-full h-1 bg-gray-900 z-50">
        <motion.div 
          className="h-full bg-cyan-500"
          initial={{ width: 0 }}
          animate={{ width: `${((currentSlide + 1) / SLIDES.length) * 100}%` }}
          transition={{ duration: 0.5 }}
        />
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={currentSlide}
          initial={{ opacity: 0, x: 100 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -100 }}
          transition={{ duration: 0.5, ease: "easeInOut" }}
          className="w-full h-full flex items-center justify-center p-8"
        >
          <CurrentSlideComponent />
        </motion.div>
      </AnimatePresence>

      {/* Navigation Hint */}
      <div className="absolute bottom-4 right-4 text-gray-600 text-xs opacity-50">
        Use Arrow Keys or Space to Navigate • Slide {currentSlide + 1}/{SLIDES.length}
      </div>
    </div>
  );
}
