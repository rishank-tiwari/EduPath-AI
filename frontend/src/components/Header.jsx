import React from 'react';
import { useLocation } from 'react-router-dom';
import { Menu, Search, Sparkles, SlidersHorizontal } from 'lucide-react';
import { HealthBadge } from './HealthBadge';
import { Button } from './Button';

export function Header({ onOpenMobileMenu }) {
  const location = useLocation();

  const getPageTitle = (path) => {
    switch (path) {
      case '/':
        return { title: 'Career Intelligence Overview', category: 'Agent Workspace' };
      case '/dashboard':
        return { title: 'Adaptive Learning Path Dashboard', category: 'Learning Loop' };
      default:
        return { title: 'Workspace Context', category: 'EduPath Agent' };
    }
  };

  const { title, category } = getPageTitle(location.pathname);

  return (
    <header className="sticky top-0 z-30 bg-surface/90 backdrop-blur-md border-b border-border-subtle px-4 lg:px-8 h-16 flex items-center justify-between gap-4">
      {/* Left: Mobile Toggle & Page Context Title */}
      <div className="flex items-center gap-3">
        <button
          onClick={onOpenMobileMenu}
          className="p-2 rounded-md text-content-secondary hover:text-content-primary hover:bg-surface-secondary lg:hidden"
          aria-label="Open sidebar navigation"
        >
          <Menu className="w-5 h-5" />
        </button>
        <div>
          <div className="text-[10px] font-mono uppercase tracking-wider text-content-muted">{category}</div>
          <h1 className="text-base font-bold text-content-primary tracking-tight leading-tight">{title}</h1>
        </div>
      </div>

      {/* Right: Search Input, Health Indicator & Action Button */}
      <div className="flex items-center gap-3">
        <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-md bg-canvas border border-border-subtle text-xs text-content-muted w-48 lg:w-64">
          <Search className="w-3.5 h-3.5 text-content-muted" />
          <span className="truncate">Search skills or targets...</span>
        </div>

        <HealthBadge />

        <Button variant="accent" size="sm" className="hidden md:inline-flex">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Ask AI Agent</span>
        </Button>
      </div>
    </header>
  );
}
