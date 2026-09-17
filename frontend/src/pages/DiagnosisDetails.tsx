import React from 'react';
import { Stethoscope, CheckCircle2, Shield, AlertTriangle } from 'lucide-react';

export const DiagnosisDetails: React.FC = () => {
  return (
    <div className="space-y-6 p-6">
      <div className="border border-slate-800 rounded-2xl bg-slate-900/80 p-6 glass-panel space-y-4">
        <h1 className="text-xl font-extrabold text-white">Diagnosis Details & Root Cause Graph</h1>
        <p className="text-xs text-slate-400">Detailed breakdown of single and cascading error diagnostics</p>

        <div className="p-4 border border-rose-900/50 bg-rose-950/20 rounded-xl space-y-3">
          <div className="flex items-center space-x-2 text-rose-400 font-bold text-sm">
            <AlertTriangle className="w-5 h-5" />
            <span>PRIMARY ROOT CAUSE: PRED-001 Out-of-Bounds Index Access</span>
          </div>
          <p className="text-xs text-slate-300">
            List 'items' statically initialized with 3 elements (indices 0, 1, 2). Accessing index 5 triggers IndexError at runtime.
          </p>
        </div>
      </div>
    </div>
  );
};
