import React from 'react';
import { Card } from './Card';
import { PRODUCT_CAPABILITY_METRICS } from '../constants/demoData';

export function MetricStrip() {
  return (
    <section className="py-8">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {PRODUCT_CAPABILITY_METRICS.map((metric, idx) => (
          <Card key={metric.number} hoverEffect className="p-6 bg-surface border-border-subtle space-y-3">
            <div className={`text-4xl font-extrabold font-mono tracking-tight ${idx % 2 === 0 ? 'text-orange' : 'text-skyblue-text'}`}>
              {metric.number}
            </div>
            <h3 className="text-base font-extrabold text-dark tracking-tight">
              {metric.title}
            </h3>
            <p className="text-xs text-content-secondary leading-relaxed font-normal">
              {metric.description}
            </p>
          </Card>
        ))}
      </div>
    </section>
  );
}
