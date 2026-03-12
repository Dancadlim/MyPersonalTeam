import React, { useState, useEffect } from 'react';

const Typewriter = ({ text, speed = 15 }) => {
    const [displayedText, setDisplayedText] = useState('');

    useEffect(() => {
        setDisplayedText('');
    }, [text]);

    useEffect(() => {
        if (displayedText.length < text.length) {
            const timeout = setTimeout(() => {
                setDisplayedText(text.slice(0, displayedText.length + 1));
            }, speed);
            return () => clearTimeout(timeout);
        }
    }, [displayedText, text, speed]);

    return <span>{displayedText}</span>;
};

export default Typewriter;
