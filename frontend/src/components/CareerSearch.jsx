import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from './Card';
import { Button } from './Button';
import { SUGGESTED_ROLES } from '../constants/demoData';
import { Search, ArrowRight } from 'lucide-react';

export function CareerSearch() {
  const [selectedRole, setSelectedRole] = useState('AI/ML Engineer');
  const navigate = useNavigate();

  const handleAnalyze = (e) => {
    e.preventDefault();
    navigate('/dashboard');
  };

  return (
    <section className="py-8">
      <Card className="p-8 md:p-12 bg-surface-soft border-border-subtle shadow-card space-y-6 text-center max-w-4xl mx-auto">
        <div className="space-y-2">
          <span className="text-xs font-mono uppercase tracking-wider text-orange-text font-extrabold">
            Career Goal Discovery
          </span>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-dark tracking-tight">
            Where do you want your career to go?
          </h2>
          <p className="text-sm text-content-secondary max-w-lg mx-auto font-medium">
            Select or search for your target role to generate a real-time skill gap roadmap.
          </p>
        </div>

        <form onSubmit={handleAnalyze} className="flex flex-col sm:flex-row gap-3 max-w-xl mx-auto">
          <div className="relative flex-1">
            <Search className="w-5 h-5 text-content-muted absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={selectedRole}
              onChange={(e) => setSelectedRole(e.target.value)}
              placeholder="What role are you aiming for?"
              className="w-full pl-11 pr-4 py-3 rounded-md bg-surface border border-border-medium text-dark placeholder:text-content-muted text-sm font-bold focus:outline-none focus:border-orange focus:ring-2 focus:ring-orange/30 transition-colors shadow-subtle"
            />
          </div>
          <Button type="submit" variant="primary" size="lg" className="gap-2 font-extrabold">
            <span>Analyze My Path</span>
            <ArrowRight className="w-4.5 h-4.5" />
          </Button>
        </form>

        <div className="space-y-2.5 pt-2">
          <div className="text-xs text-content-muted font-bold">Suggested Career Paths</div>
          <div className="flex flex-wrap items-center justify-center gap-2">
            {SUGGESTED_ROLES.map((role) => (
              <button
                key={role}
                onClick={() => setSelectedRole(role)}
                className={`px-3.5 py-1.5 rounded-full text-xs font-bold border transition-all ${
                  selectedRole === role
                    ? 'bg-orange text-dark border-orange-hover shadow-subtle'
                    : 'bg-surface text-dark border-border-subtle hover:border-orange/60'
                }`}
              >
                {role}
              </button>
            ))}
          </div>
        </div>
      </Card>
    </section>
  );
}
