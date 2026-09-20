import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from './Button';
import { Card } from './Card';
import { ArrowRight } from 'lucide-react';

export function CTASection() {
  return (
    <section className="py-16">
      <Card className="p-10 md:p-16 bg-orange border-orange-hover shadow-floating text-center max-w-4xl mx-auto space-y-6">
        <div className="space-y-3">
          <h2 className="text-3xl sm:text-5xl font-extrabold text-dark tracking-tight">
            Stop wondering what to learn next.
          </h2>
          <p className="text-base text-dark/90 max-w-lg mx-auto font-medium">
            Give EduPath your goal. We'll help you find the path.
          </p>
        </div>

        <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
          <Link to="/dashboard">
            <Button size="lg" variant="dark" className="gap-2 font-extrabold">
              <span>Build My Learning Path</span>
              <ArrowRight className="w-4.5 h-4.5" />
            </Button>
          </Link>
          <a href="#how-it-works">
            <Button size="lg" variant="secondary" className="gap-2">
              <span>Explore EduPath</span>
            </Button>
          </a>
        </div>
      </Card>
    </section>
  );
}
