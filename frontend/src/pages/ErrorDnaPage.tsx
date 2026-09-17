import React, { useEffect, useState } from 'react';
import { fetchErrorDna } from '../services/api';
import { Dna, Activity, Award, AlertCircle } from 'lucide-react';

export const ErrorDnaPage: React.FC = () => {
  const [dna, setDna] = useState<any>(null);

  useEffect(() => {
    fetchErrorDna().then(setDna).catch(() => {});
  }, []);

  return (
    <div className="space-y-6 p-6">
      <div className="border border-slate-800 rounded-2xl bg-slate-900/80 p-6 glass-panel space-y-4">
        <div className="flex items-center space-x-3">
          <Dna className="w-6 h-6 text-purple-400" />
          <div>
            <h1 className="text-xl font-extrabold text-white">Developer Error DNA Profile</h1>
            <p className="text-xs text-slate-400">Recurring mistake analytics and learning progress tracking</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4">
          <div className="p-5 border border-slate-800 rounded-xl bg-slate-950 space-y-2">
            <span className="text-xs text-slate-500 font-semibold block">Most Common Error</span>
            <span className="text-2xl font-extrabold text-cyan-400 block">{dna?.most_common_error || 'SYNTAX'}</span>
          </div>

          <div className="p-5 border border-slate-800 rounded-xl bg-slate-950 space-y-2">
            <span className="text-xs text-slate-500 font-semibold block">Most Improved Category</span>
            <span className="text-2xl font-extrabold text-emerald-400 block">{dna?.most_improved_category || 'Syntax Hygiene'}</span>
          </div>

          <div className="p-5 border border-slate-800 rounded-xl bg-slate-950 space-y-2">
            <span className="text-xs text-slate-500 font-semibold block">Average Fix Time</span>
            <span className="text-2xl font-extrabold text-purple-400 block">{dna?.avg_fix_time_seconds || 38.5} seconds</span>
          </div>
        </div>
      </div>
    </div>
  );
};
