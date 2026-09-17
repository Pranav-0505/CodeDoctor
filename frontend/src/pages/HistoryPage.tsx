import React, { useEffect, useState } from 'react';
import { fetchScanHistory } from '../services/api';
import { History as HistoryIcon, FileCode } from 'lucide-react';

export const HistoryPage: React.FC = () => {
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    fetchScanHistory().then(setHistory).catch(() => {});
  }, []);

  return (
    <div className="space-y-6 p-6">
      <div className="border border-slate-800 rounded-2xl bg-slate-900/80 p-6 glass-panel space-y-4">
        <div className="flex items-center space-x-3">
          <HistoryIcon className="w-6 h-6 text-cyan-400" />
          <div>
            <h1 className="text-xl font-extrabold text-white">Diagnostic Scan History</h1>
            <p className="text-xs text-slate-400">Complete audit trail of past code and project scans</p>
          </div>
        </div>

        <div className="space-y-3 pt-4">
          {history.length === 0 ? (
            <div className="text-xs text-slate-500 p-8 text-center border border-slate-800 rounded-xl bg-slate-950">
              No historical scan records available yet.
            </div>
          ) : (
            history.map((scan, idx) => (
              <div key={idx} className="p-4 border border-slate-800 rounded-xl bg-slate-950 text-xs flex items-center justify-between">
                <div className="space-y-1">
                  <span className="font-bold text-white flex items-center space-x-2">
                    <FileCode className="w-4 h-4 text-cyan-400" />
                    <span>{scan.file_path}</span>
                  </span>
                  <span className="text-slate-500 block">Language: {scan.language} • Platform: {scan.platform}</span>
                </div>
                <div className="text-right space-y-1">
                  <span className="font-extrabold text-cyan-400 block text-sm">{scan.health_score}/100</span>
                  <span className="text-slate-400 block">{scan.total_issues} issues detected</span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
