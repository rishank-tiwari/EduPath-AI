import React from 'react';
import { Link } from 'react-router-dom';
import { GraduationCap, ShieldCheck, ArrowRight } from 'lucide-react';
import { APP_CONFIG } from '../constants/config';

export function Footer() {
  return (
    <footer className="mt-auto bg-dark border-t border-dark-hover pt-12 pb-8 text-sm text-canvas/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 border-b border-canvas/15 pb-8">
          {/* Brand Info */}
          <div className="space-y-2 max-w-sm">
            <Link to="/" className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-lg bg-orange text-dark flex items-center justify-center font-extrabold shadow-subtle">
                <GraduationCap className="w-5 h-5" />
              </div>
              <span className="font-extrabold text-xl text-canvas tracking-tight">{APP_CONFIG.name}</span>
            </Link>
            <p className="text-xs text-canvas/70 leading-relaxed font-normal">
              Personalized learning &amp; skill gap intelligence for ambitious tech careers.
            </p>
          </div>

          {/* Core Footer Links */}
          <nav className="flex flex-wrap items-center gap-6 text-xs font-bold font-mono uppercase tracking-wider">
            <Link to="/my-path" className="text-canvas/80 hover:text-orange transition-colors">
              1. Roadmap
            </Link>
            <a href="/#how-it-works" className="text-canvas/80 hover:text-orange transition-colors">
              2. How It Works
            </a>
            <a href="/#skills" className="text-canvas/80 hover:text-orange transition-colors">
              3. Features
            </a>
            <Link to="/learning-guide" className="text-skyblue hover:text-orange transition-colors">
              4. Learning Guide
            </Link>
          </nav>
        </div>

        {/* Bottom Bar */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-canvas/60">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-orange" />
            <span>© 2026 EduPath. All rights reserved.</span>
          </div>
          <div className="flex items-center gap-4 font-mono text-[11px] font-bold">
            <span className="text-skyblue">{APP_CONFIG.hackathon}</span>
            <span>•</span>
            <span className="text-orange">EduPath AI Engine</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
