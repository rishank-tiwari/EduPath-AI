import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { Button } from './Button';
import { GraduationCap, Menu, X, ArrowRight, Bot, User, LogOut, LogIn } from 'lucide-react';
import { APP_CONFIG } from '../constants/config';

export function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const { toggleAgentModal, isAuthenticated, logoutUser } = useApp();

  const navLinks = [
    { name: 'Home', path: '/' },
    { name: 'My Path', path: '/my-path' },
    { name: 'Practice', path: '/practice' },
    { name: 'AI Mentor', path: '/mentor' },
    { name: 'Progress', path: '/progress' },
  ];

  const handleStartJourney = () => {
    if (isAuthenticated) {
      navigate('/onboarding');
    } else {
      navigate('/login', { state: { from: '/onboarding' } });
    }
  };

  return (
    <header className="sticky top-0 z-40 bg-canvas/95 backdrop-blur-md border-b border-border-subtle">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between gap-4">
        {/* Left Logo */}
        <Link to="/" className="flex items-center gap-2.5 group">
          <div className="w-10 h-10 rounded-lg bg-orange text-dark flex items-center justify-center font-bold shadow-subtle group-hover:bg-orange-hover transition-colors">
            <GraduationCap className="w-6 h-6" />
          </div>
          <div className="flex items-center gap-1.5">
            <span className="font-extrabold text-xl tracking-tight text-dark">{APP_CONFIG.name}</span>
            <span className="text-[10px] px-2 py-0.5 rounded-md bg-skyblue text-dark font-mono font-extrabold shadow-subtle">
              AI
            </span>
          </div>
        </Link>

        {/* Center Simplified Navigation (Desktop) */}
        <nav className="hidden md:flex items-center gap-1 bg-surface-soft p-1.5 rounded-xl border border-border-subtle">
          {navLinks.map((link) => {
            const isActive = location.pathname === link.path;
            return (
              <Link
                key={link.name}
                to={link.path}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-colors ${
                  isActive
                    ? 'bg-surface text-dark shadow-subtle'
                    : 'text-content-secondary hover:text-dark hover:bg-surface/50'
                }`}
              >
                {link.name}
              </Link>
            );
          })}
        </nav>

        {/* Right Action CTAs */}
        <div className="hidden md:flex items-center gap-3">
          <button
            onClick={toggleAgentModal}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-skyblue-light border border-skyblue-border text-skyblue-text font-bold text-xs hover:bg-skyblue/20 transition-colors"
          >
            <Bot className="w-4 h-4" />
            <span>View AI Activity</span>
          </button>

          {isAuthenticated ? (
            <>
              <Link to="/profile" className="p-2 rounded-xl bg-surface border border-border-subtle hover:border-orange text-dark transition-colors" title="Profile">
                <User className="w-4 h-4" />
              </Link>
              <button
                onClick={logoutUser}
                title="Log Out"
                className="p-2 rounded-xl bg-surface border border-border-subtle hover:bg-red-50 text-content-secondary hover:text-red-600 transition-colors"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </>
          ) : (
            <Link to="/login" className="px-3 py-1.5 text-xs font-bold text-dark hover:text-orange-text transition-colors flex items-center gap-1">
              <LogIn className="w-3.5 h-3.5" />
              <span>Log In</span>
            </Link>
          )}

          <Button variant="primary" size="sm" onClick={handleStartJourney} className="gap-1.5">
            <span>Start Journey</span>
            <ArrowRight className="w-4 h-4" />
          </Button>
        </div>

        {/* Mobile Hamburger */}
        <div className="flex md:hidden items-center gap-2">
          <button
            onClick={toggleAgentModal}
            className="p-2 rounded-lg bg-skyblue-light text-skyblue-text"
            aria-label="View AI Activity"
          >
            <Bot className="w-5 h-5" />
          </button>
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2 rounded-lg text-dark hover:bg-surface-soft"
            aria-label="Toggle navigation menu"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-border-subtle bg-surface px-4 pt-3 pb-6 space-y-4">
          <nav className="flex flex-col space-y-2">
            {navLinks.map((link) => (
              <Link
                key={link.name}
                to={link.path}
                onClick={() => setMobileMenuOpen(false)}
                className={`text-sm font-bold py-2 px-3 rounded-lg ${
                  location.pathname === link.path ? 'bg-orange-light text-dark' : 'text-content-secondary'
                }`}
              >
                {link.name}
              </Link>
            ))}
          </nav>

          <div className="pt-3 border-t border-border-subtle flex flex-col gap-2">
            <Link to="/onboarding" onClick={() => setMobileMenuOpen(false)}>
              <Button variant="primary" size="md" className="w-full justify-center">
                Build My Learning Path →
              </Button>
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
