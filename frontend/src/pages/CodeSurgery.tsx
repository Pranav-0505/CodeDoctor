import React from 'react';
import { Syringe, CheckCircle2, ShieldCheck, RefreshCw } from 'lucide-react';

export const CodeSurgery: React.FC = () => {
  return (
    <div className="space-y-6 p-6">
      <div className="border border-slate-800 rounded-2xl bg-slate-900/80 p-6 glass-panel space-y-4">
        <div className="flex items-center space-x-3">
          <Syringe className="w-6 h-6 text-cyan-400" />
          <div>
            <h1 className="text-xl font-extrabold text-white">Code Surgery Repair System</h1>
            <p className="text-xs text-slate-400">Minimal patches, unified diff previews, and safe verification before changes are applied</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4">
          <div className="p-4 border border-slate-800 rounded-xl bg-slate-950 text-xs space-y-2">
            <span className="font-bold text-cyan-400 block">1. Problem Identification</span>
            <p className="text-slate-400">Locates exact AST line and rule ID causing exception or hazard.</p>
          </div>
          <div className="p-4 border border-slate-800 rounded-xl bg-slate-950 text-xs space-y-2">
            <span className="font-bold text-purple-400 block">2. Unified Diff Preview</span>
            <p className="text-slate-400">Generates minimal diff without overwriting entire file buffers.</p>
          </div>
          <div className="p-4 border border-slate-800 rounded-xl bg-slate-950 text-xs space-y-2">
            <span className="font-bold text-emerald-400 block">3. Safe Verification</span>
            <p className="text-slate-400">Re-parses syntax and re-runs rules to guarantee zero new errors.</p>
          </div>
        </div>
      </div>
    </div>
  );
};
