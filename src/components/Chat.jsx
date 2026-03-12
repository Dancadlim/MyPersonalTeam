import React, { useState, useEffect, useRef } from 'react';
import { GoogleGenAI } from '@google/genai';
import { Send, User, Bot, Loader2 } from 'lucide-react';
import Typewriter from './Typewriter';

const SYSTEM_INSTRUCTION = `Você é um personal trainer de elite, muito atencioso, conversando com um novo aluno. 
O objetivo do sistema é descobrir o "Tópico Principal" atual sobre o aluno, mas VOCÊ deve investigar a fundo usando sua experiência prática.

REGRAS DE CONDUTA:
1. Faça APENAS UMA PERGUNTA POR VEZ. Nunca envie uma lista de perguntas.
2. SEJA PROFUNDO: Não aceite a primeira resposta rasa. Se o aluno quer "perder peso", investigue quanto, desde quando, o que tentou antes. Se joga "futebol", investigue a posição, estilo de jogo, dificuldades físicas no campo.
3. Seja sempre humano, empático e de respostas curtas (tamanho de uma mensagem de WhatsApp).

COMO AVANÇAR DE TÓPICO:
O sistema só avança para a próxima etapa master quando você digitar exatamente "[NEXT]" na sua resposta.
- NUNCA use [NEXT] precocemente. Você tem a OBRIGAÇÃO ABSOLUTA de fazer PELO MENOS 5 perguntas investigativas profundas (em turnos separados) antes de encerrar o assunto. Só depois de 5 trocas de mensagem sobre o MESMO tópico você pode avançar.
- Quando a investigação do tópico atual estiver ESGOTADA, faça um breve elogio ou conclusão e adicione "[NEXT]" no final da mensagem.
- SE VOCÊ ESCREVER "[NEXT]", VERIFIQUE SE NÃO HÁ NENHUMA PERGUNTA NO SEU TEXTO. Quando usar [NEXT], não encerre com pergunta, apenas afirme que compreendeu e coloque a tag.`;

const MAIN_QUESTIONS = [
    "Oi! Estou aqui para coletar suas informações e fazer um treino ultra-personalizado. Me fala, qual o seu objetivo principal ao usar nosso serviço?",
    "Que legal! O próximo passo é entender sua rotina. Como são seus horários diários, tem equipamento em casa ou vai pra academia?",
    "Entendido. E sobre seu corpo: você tem alguma lesão antiga, dor ao fazer movimentos específicos, ou alguma deficiência física?",
    "Perfeito. Pra fechar nossa ficha inicial: você tem alergia a algum medicamento ou restrição alimentar muito forte?"
];

// Initialize GenAI client safely
const apiKey = import.meta.env.VITE_GEMINI_API_KEY;
const ai = apiKey ? new GoogleGenAI({ apiKey }) : null;

const Chat = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const messagesEndRef = useRef(null);

    // Create a chat session abstraction since the Node SDK doesn't have a built-in one yet
    // We keep the history to send on every request
    const [chatHistory, setChatHistory] = useState([
        { role: 'user', parts: [{ text: SYSTEM_INSTRUCTION }] },
        { role: 'model', parts: [{ text: "Compreendido. Agirei como um treinador engajado. Tenho a obrigação de fazer pelo menos 5 perguntas profundas, uma por vez, sobre o tópico atual. Não darei [NEXT] antes disso. E quando der [NEXT], será afirmando a conclusão do tópico, sem novas perguntas." }] }
    ]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Start the chat by asking the first question
    useEffect(() => {
        if (messages.length === 0) {
            appendMessage('model', MAIN_QUESTIONS[0]);
        }
    }, []);

    const appendMessage = (role, text) => {
        setMessages(prev => [...prev, { role, text }]);
        // Also update the hidden history we send to Gemini
        setChatHistory(prev => [...prev, { role, parts: [{ text }] }]);
    };

    const handleSend = async (e) => {
        e?.preventDefault();
        if (!input.trim() || isLoading) return;

        const userText = input.trim();
        setInput('');
        appendMessage('user', userText);
        setIsLoading(true);

        try {
            if (!ai) {
                throw new Error("A chave API do Gemini não foi encontrada! Configure o .env.local e reinicie o servidor.");
            }

            // Prepare the history for the API call
            // We append the new user message here manually because state update is async
            const currentHistory = [...chatHistory, { role: 'user', parts: [{ text: userText }] }];

            const response = await ai.models.generateContent({
                model: 'gemini-3-flash-preview',
                contents: currentHistory,
            });

            let responseText = response.text || '';

            // Check for the [NEXT] trigger
            if (responseText.includes('[NEXT]')) {
                // Clean up the response to remove the token
                responseText = responseText.replace(/\[NEXT\]/g, '').trim();

                // Output the cleaned response if there's any text left besides [NEXT]
                if (responseText) {
                    appendMessage('model', responseText);
                }

                // Advance the state machine
                const nextIndex = currentQuestionIndex + 1;
                if (nextIndex < MAIN_QUESTIONS.length) {
                    setCurrentQuestionIndex(nextIndex);
                    // Small delay so it feels like two distinct messages
                    setTimeout(() => {
                        appendMessage('model', "Perfeito! Agora mudando de assunto: " + MAIN_QUESTIONS[nextIndex]);
                    }, 800);
                } else {
                    // Finished all questions
                    setTimeout(() => {
                        appendMessage('model', "Anotado! Já coletamos todas as informações principais. Nossos profissionais vão montar seu treino ultra-personalizado agora. Tem mais alguma dúvida?");
                    }, 800);
                }
            } else {
                // Normal response, Gemini is still interrogating the current topic
                appendMessage('model', responseText);
            }

        } catch (error) {
            console.error("Error calling Gemini API:", error);
            appendMessage('model', "Ocorreu um erro ao processar sua mensagem. Verifique a API Key no seu `.env.local`.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-screen bg-brand-darker text-white font-sans">
            {/* Header */}
            <header className="bg-brand-dark p-4 shadow-md flex justify-between items-center border-b border-brand-accent/20">
                <h1 className="text-xl font-bold">Avaliação Personalizada</h1>
                <div className="text-sm text-brand-light">Etapa {Math.min(currentQuestionIndex + 1, MAIN_QUESTIONS.length)} de {MAIN_QUESTIONS.length}</div>
            </header>

            {/* Chat Messages Area */}
            <main className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((msg, index) => (
                    <div
                        key={index}
                        className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                        <div
                            className={`max-w-[80%] rounded-2xl p-4 flex gap-3 shadow-lg ${msg.role === 'user'
                                ? 'bg-brand-primary text-brand-darker rounded-tr-none'
                                : 'bg-brand-dark border border-brand-accent/30 text-brand-light rounded-tl-none'
                                }`}
                        >
                            <div className="mt-1 flex-shrink-0">
                                {msg.role === 'user' ? <User size={20} /> : <Bot size={20} className="text-brand-accent" />}
                            </div>
                            <div className="whitespace-pre-wrap leading-relaxed">
                                {msg.role === 'model' ? (
                                    <Typewriter text={msg.text} speed={20} />
                                ) : (
                                    msg.text
                                )}
                            </div>
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex justify-start">
                        <div className="bg-brand-dark border border-brand-accent/30 rounded-2xl p-4 rounded-tl-none flex gap-3 text-brand-light">
                            <Bot size={20} className="text-brand-accent" />
                            <div className="flex items-center gap-2">
                                <Loader2 className="animate-spin" size={16} />
                                <span>Analisando resposta...</span>
                            </div>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </main>

            {/* Input Area */}
            <footer className="p-4 bg-brand-dark border-t border-brand-accent/20">
                <form onSubmit={handleSend} className="max-w-4xl mx-auto flex gap-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        disabled={isLoading}
                        placeholder="Digite sua resposta..."
                        className="flex-1 bg-brand-darker border border-brand-accent/50 rounded-full px-6 py-3 focus:outline-none focus:border-brand-primary transition-colors disabled:opacity-50"
                    />
                    <button
                        type="submit"
                        disabled={isLoading || !input.trim()}
                        className="bg-brand-primary hover:bg-brand-primary/80 disabled:bg-brand-primary/50 text-brand-darker rounded-full p-4 flex items-center justify-center transition-colors"
                    >
                        <Send size={20} />
                    </button>
                </form>
            </footer>
        </div>
    );
};

export default Chat;
