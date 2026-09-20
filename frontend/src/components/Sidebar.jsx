import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  GraduationCap,
  LayoutDashboard,
  Brain,
  Target,
  BookOpen,
  Code2,
  Award,
  LineChart,
  Bot,
  Settings,
  User,
  X,
} from 'lucide-react';
import { cn } from '../utils/cn';
import { APP_CONFIG } from '../constants/config';

export function Sidebar({ isOpen, onClose }) {
  const navItems = [
    { name: 'Overview', path: '/', icon: LayoutDashboard },
    { name: 'My Skills', path: '/skills', icon: Brain, isPlaceholder: true },
    { name: 'Skill Gaps', path: '/skill-gaps', icon: Target, isPlaceholder: true },
    { name: 'Learning Path', path: '/dashboard', icon: BookOpen },
    { name: 'Practice', path: '/practice', icon: Code2, isPlaceholder: true },
    { name: 'Assessments', path: '/assessments', icon: Award, isPlaceholder: true },
    { name: 'Progress', path: '/progress', icon: LineChart, isPlaceholder: true },
    { name: 'AI Mentor', path: '/mentor', icon: Bot, isPlaceholder: true },
  ];

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-surface-dark/30 backdrop-blur-xs lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={cn(
          'fixed top-0 left-0 bottom-0 z-50 w-64 bg-surface border-r border-border-subtle flex flex-col transition-transform duration-200 ease-in-out lg:translate-x-0 lg:static lg:z-auto',
          isOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        {/* Brand Header */}
        <div className="flex items-center justify-between h-16 px-5 border-b border-border-subtle">
          <NavLink to="/" className="flex items-center gap-2.5 group">
            <div className="w-7 h-7 rounded-md bg-terracotta text-content-inverse flex items-center justify-center font-bold">
              <GraduationCap className="w-4 h-4" />
            </div>
            <div className="flex items-center gap-1.5">
              <span className="font-bold text-sm tracking-tight text-content-primary">{APP_CONFIG.name}</span>
              <span className="text-[10px] px-1.5 py-0.2 rounded bg-terracotta-light text-terracotta font-mono font-medium">
                AI
              </span>
            </div>
          </NavLink>
          <button
            onClick={onClose}
            className="p-1 rounded-md text-content-muted hover:text-content-primary hover:bg-surface-secondary lg:hidden"
            aria-label="Close menu"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Primary Navigation */}
        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          <div className="px-3 pb-2 text-[10px] font-mono font-semibold tracking-wider text-content-muted uppercase">
            Workspace
          </div>
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.name}
                to={item.path}
                onClick={onClose}
                className={({ isActive }) =>
                  cn(
                    'flex items-center justify-between px-3 py-2 rounded-md text-xs font-medium transition-colors group',
                    isActive
                      ? 'bg-surface-secondary text-content-primary font-semibold border-l-2 border-terracotta pl-[10px]'
                      : 'text-content-secondary hover:text-content-primary hover:bg-surface-hover'
                  )
                }
              >
                <div className="flex items-center gap-2.5">
                  <Icon className="w-4 h-4 text-content-secondary group-hover:text-content-primary transition-colors" />
                  <span>{item.name}</span>
                </div>
                {item.isPlaceholder && (
                  <span className="text-[9px] px-1.5 py-0.2 rounded bg-surface-secondary text-content-muted font-mono">
                    Soon
                  </span>
                )}
              </NavLink>
            );
          })}
        </nav>

        {/* Bottom User / Settings Section */}
        <div className="p-3 border-t border-border-subtle space-y-1 bg-canvas/40">
          <NavLink
            to="/settings"
            onClick={onClose}
            className="flex items-center gap-2.5 px-3 py-2 rounded-md text-xs font-medium text-content-secondary hover:text-content-primary hover:bg-surface transition-colors"
          >
            <Settings className="w-4 h-4" />
            <span>Settings</span>
          </NavLink>
          <div className="flex items-center justify-between px-3 py-2 rounded-md bg-surface border border-border-subtle">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded-full bg-warm-light text-content-primary border border-warm/40 flex items-center justify-center font-bold text-[10px]">
                EP
              </div>
              <div className="text-xs">
                <div className="font-semibold text-content-primary leading-none">Learner Workspace</div>
                <div className="text-[10px] text-content-muted mt-0.5">Free Tier Agent</div>
              </div>
            </div>
            <User className="w-3.5 h-3.5 text-content-muted" />
          </div>
        </div>
      </aside>
    </>
  );
}
