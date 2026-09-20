import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import { mentorService } from '../services/mentorService';
import { Button } from '../components/Button';
import { Bot, Send, User, Sparkles, AlertCircle, Loader2 } from 'lucide-react';

export function AIMentorPage() {
  const { userId, userProfile, addAiLog } = useApp();
  const targetRole = userProfile?.target_role || 'AI/ML Engineer';

  const [inputQuery, setInputQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);

  const [messages, setMessages] = useState([
    {
      sender: 'mentor',
      text: `Hello! I'm your EduPath AI Mentor. I know you're working toward becoming a ${targetRole}. What can I explain or clarify for you today?`,
    },
  ]);

  const promptPills = [
    'Explain this in simple words',
    'Why am I learning this?',
    'Give me an example',
    'Give me a practice question',
    'What should I learn next?',
    'Why did my learning path change?',
  ];

  const handleSend = async (textToSend) => {
    const query = textToSend || inputQuery;
    if (!query.trim() || loading) return;

    setErrorMessage(null);
    const newMsgs = [...messages, { sender: 'user', text: query }];
    setMessages(newMsgs);
    setInputQuery('');
    setLoading(true);

    try {
      const response = await mentorService.sendMessage(userId || 'demo_user_1', query);

      setMessages((prev) => [
        ...prev,
        {
          sender: 'mentor',
          text: response.response,
          topic: response.context_topic,
          action: response.suggested_action,
          mode: response.response_mode,
        },
      ]);

      if (addAiLog) {
        addAiLog('✓ AI Mentor used learner context');
      }
    } catch (err) {
      console.error('Mentor API error:', err);
      setErrorMessage("Your mentor couldn't respond right now. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Header */}
      <div className="space-y-1">
        <div className="flex items-center gap-2">
          <span className="text-xs font-mono font-bold px-2.5 py-0.5 rounded bg-skyblue-light text-skyblue-text flex items-center gap-1">
            <Sparkles className="w-3.5 h-3.5 text-skyblue-text" />
            CONTEXT-AWARE AI MENTOR
          </span>
        </div>
        <h1 className="text-3xl font-extrabold text-dark tracking-tight">Your AI Mentor</h1>
        <p className="text-sm text-content-secondary font-medium">
          Ask anything about your learning path, skill gaps, or current task. Powered by real EduPath learner context.
        </p>
      </div>

      {/* Suggested Prompt Pills */}
      <div className="space-y-2">
        <span className="text-xs font-bold text-content-muted uppercase tracking-wider">
          Suggested Questions
        </span>
        <div className="flex flex-wrap gap-2">
          {promptPills.map((pill, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(pill)}
              disabled={loading}
              className="px-3 py-1.5 rounded-xl bg-surface border border-border-subtle text-xs font-bold text-content-secondary hover:border-orange hover:text-dark transition-colors disabled:opacity-50"
            >
              {pill}
            </button>
          ))}
        </div>
      </div>

      {/* Error Banner */}
      {errorMessage && (
        <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-xs text-red-700 flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0 text-red-600" />
          <span>{errorMessage}</span>
        </div>
      )}

      {/* Chat Container */}
      <div className="bg-surface border border-border-subtle rounded-2xl p-6 shadow-card flex flex-col h-[500px]">
        {/* Message Log */}
        <div className="flex-1 overflow-y-auto space-y-4 pr-2">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex items-start gap-3 ${
                msg.sender === 'user' ? 'flex-row-reverse' : ''
              }`}
            >
              <div
                className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 text-xs font-bold ${
                  msg.sender === 'user'
                    ? 'bg-orange text-dark'
                    : 'bg-dark text-canvas'
                }`}
              >
                {msg.sender === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              <div
                className={`p-4 rounded-2xl max-w-lg text-xs leading-relaxed font-medium space-y-2 ${
                  msg.sender === 'user'
                    ? 'bg-orange-light text-dark rounded-tr-none'
                    : 'bg-surface-soft border border-border-subtle text-dark rounded-tl-none'
                }`}
              >
                <div className="whitespace-pre-line">{msg.text}</div>
                {msg.sender === 'mentor' && msg.topic && (
                  <div className="pt-2 border-t border-border-subtle/50 flex items-center justify-between gap-2">
                    <span className="text-[10px] font-mono font-bold text-content-muted">
                      Topic: {msg.topic}
                    </span>
                    {msg.action && (
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-orange-light text-orange-text">
                        Next: {msg.action}
                      </span>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}

          {/* Loading Indicator */}
          {loading && (
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-dark text-canvas flex items-center justify-center shrink-0">
                <Bot className="w-4 h-4" />
              </div>
              <div className="p-4 rounded-2xl bg-surface-soft border border-border-subtle text-xs font-medium text-content-secondary flex items-center gap-2">
                <Loader2 className="w-4 h-4 animate-spin text-orange-text" />
                <span>Your mentor is thinking...</span>
              </div>
            </div>
          )}
        </div>

        {/* Input Bar */}
        <div className="pt-4 border-t border-border-subtle flex items-center gap-2">
          <input
            type="text"
            placeholder="Ask your AI Mentor a question..."
            value={inputQuery}
            onChange={(e) => setInputQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            disabled={loading}
            className="flex-1 px-4 py-3 rounded-xl border border-border-subtle bg-canvas text-xs font-medium focus:outline-none focus:border-orange disabled:opacity-50"
          />
          <Button variant="primary" size="md" onClick={() => handleSend()} disabled={loading} className="px-4">
            <Send className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
