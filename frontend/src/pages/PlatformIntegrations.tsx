import React, { useEffect, useState } from 'react';
import { fetchPlatforms } from '../services/api';
import { Layers, CheckCircle2, Clock } from 'lucide-react';

export const PlatformIntegrations: React.FC = () => {
  const [platforms, setPlatforms] = useState<any[]>([]);

  useEffect(() => {
    fetchPlatforms().then(setPlatforms).catch(() => {});
  }, []);

  return (
    <div className="space-y-6 p-6">
      <div className="border border-slate-800 rounded-2xl bg-slate-900/80 p-6 glass-panel space-y-4">
        <div className="flex items-center space-x-3">
          <Layers className="w-6 h-6 text-cyan-400" />
          <div>
            <h1 className="text-xl font-extrabold text-white">Platform Integrations & IDE Adapters</h1>
            <p className="text-xs text-slate-400">Target platform ecosystem connecting to Code Doctor Core Engine</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4">
          {platforms.map((p, idx) => (
            <div key={idx} className="p-4 border border-slate-800 rounded-xl bg-slate-950 text-xs space-y-2 flex items-center justify-between">
              <div>
                <span className="font-bold text-white block">{p.name}</span>
                <span className="text-slate-500 font-mono">Adapter ID: {p.id}</span>
              </div>
              <span className={`px-2.5 py-1 rounded text-[10px] font-bold ${
                p.status === 'ACTIVE'
                  ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
                  : 'bg-slate-900 text-slate-500 border border-slate-800'
              }`}>
                {p.status}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
