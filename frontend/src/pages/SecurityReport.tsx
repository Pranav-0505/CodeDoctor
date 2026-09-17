import React from 'react';
import { ShieldAlert, Lock, AlertOctagon, CheckCircle2 } from 'lucide-react';

export const SecurityReport: React.FC = () => {
  return (
    <div className="space-y-6 p-6">
      <div className="border border-slate-800 rounded-2xl bg-slate-900/80 p-6 glass-panel space-y-4">
        <div className="flex items-center space-x-3">
          <ShieldAlert className="w-6 h-6 text-emerald-400" />
          <div>
            <h1 className="text-xl font-extrabold text-white">Security Doctor Report</h1>
            <p className="text-xs text-slate-400">Hardcoded secret scanning, SQL injection risk analysis, dynamic exec rules</p>
          </div>
        </div>

        <div className="space-y-3 pt-4">
          <div className="p-4 border border-slate-800 rounded-xl bg-slate-950 text-xs flex items-center justify-between">
            <div className="space-y-1">
              <span className="font-bold text-white block">SEC-001: Exposed Hardcoded Secrets</span>
              <p className="text-slate-400">Checks for plaintext API keys, passwords, and JWT tokens in source code.</p>
            </div>
            <span className="px-2 py-1 bg-emerald-950 text-emerald-400 border border-emerald-800 rounded font-bold">ACTIVE RULE</span>
          </div>

          <div className="p-4 border border-slate-800 rounded-xl bg-slate-950 text-xs flex items-center justify-between">
            <div className="space-y-1">
              <span className="font-bold text-white block">SEC-002: SQL Injection Vulnerability</span>
              <p className="text-slate-400">Detects unparameterized string formatting inside SQL queries.</p>
            </div>
            <span className="px-2 py-1 bg-emerald-950 text-emerald-400 border border-emerald-800 rounded font-bold">ACTIVE RULE</span>
          </div>

          <div className="p-4 border border-slate-800 rounded-xl bg-slate-950 text-xs flex items-center justify-between">
            <div className="space-y-1">
              <span className="font-bold text-white block">SEC-004: Unsafe Command Execution</span>
              <p className="text-slate-400">Flags dynamic eval(), exec(), and os.system() code evaluation calls.</p>
            </div>
            <span className="px-2 py-1 bg-emerald-950 text-emerald-400 border border-emerald-800 rounded font-bold">ACTIVE RULE</span>
          </div>
        </div>
      </div>
    </div>
  );
};
