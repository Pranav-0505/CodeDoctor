import React from 'react';
import { Zap, Clock, Cpu } from 'lucide-react';

export const PerformanceReport: React.FC = () => {
  return (
    <div className="space-y-6 p-6">
      <div className="border border-slate-800 rounded-2xl bg-slate-900/80 p-6 glass-panel space-y-4">
        <div className="flex items-center space-x-3">
          <Zap className="w-6 h-6 text-amber-400" />
          <div>
            <h1 className="text-xl font-extrabold text-white">Performance Doctor Report</h1>
            <p className="text-xs text-slate-400">Algorithmic complexity analysis, nested loops, and expensive call detection</p>
          </div>
        </div>

        <div className="space-y-3 pt-4">
          <div className="p-4 border border-slate-800 rounded-xl bg-slate-950 text-xs flex items-center justify-between">
            <div className="space-y-1">
              <span className="font-bold text-white block">PERF-001: Deeply Nested Loops</span>
              <p className="text-slate-400">Flags triple-nested loops creating O(N^3) time complexity bottlenecks.</p>
            </div>
            <span className="px-2 py-1 bg-amber-950 text-amber-400 border border-amber-800 rounded font-bold">ACTIVE RULE</span>
          </div>
        </div>
      </div>
    </div>
  );
};
