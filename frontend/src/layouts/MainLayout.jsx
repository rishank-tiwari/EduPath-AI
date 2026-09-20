import React from 'react';
import { Outlet } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';
import { AgentActivityModal } from '../components/AgentActivityModal';

export function MainLayout() {
  return (
    <div className="min-h-screen flex flex-col bg-canvas text-content-primary selection:bg-orange selection:text-dark">
      <Navbar />
      <main className="flex-1">
        <Outlet />
      </main>
      <Footer />
      <AgentActivityModal />
    </div>
  );
}
