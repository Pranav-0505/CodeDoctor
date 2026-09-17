import React from 'react';
import { DiagnosticItem } from '../types';
import { GitCommit, ArrowRight, AlertTriangle, Layers } from 'lucide-react';

interface RootCauseGraphProps {
  rootCauses: DiagnosticItem[];
  cascadingIssues: DiagnosticItem[];
}

export const RootCauseGraph: React.FC<RootCauseGraphProps> = ({ rootCauses, cascadingIssues }) => {
  return (
    <div className="border border-slate-800 rounded-xl bg-slate-900/50 p-5 space-y-4 shadow-sm">
      <div className="flex items-center space-x-2 text-cyan-400 font-semibold text-sm">
        <Layers className="w-4 h-4" />
        <span>Cascading Root Cause Analysis Graph</span>
      </div>

      {rootCauses.length === 0 ? (
        <div className="text-xs text-slate-500 italic">No root cause dependencies identified.</div>
      ) : (
        <div className="space-y-3">
          {rootCauses.map((root) => (
            <div key={root.id} className="p-3 border border-rose-900/50 bg-rose-950/20 rounded-lg space-y-2">
              <div className="flex items-center space-x-2 text-xs font-bold text-rose-400">
                <AlertTriangle className="w-4 h-4" />
                <span>PRIMARY ROOT CAUSE: {root.title} (Line {root.line})</span>
              </div>
              <p className="text-xs text-slate-300 pl-6">{root.root_cause || root.message}</p>

              {cascadingIssues.filter(c => c.parent_issue_id === root.id || !c.is_root_cause).length > 0 && (
                <div className="pl-6 pt-2 space-y-1">
                  <div className="text-[11px] font-semibold text-slate-400 flex items-center space-x-1">
                    <ArrowRight className="w-3 h-3 text-cyan-400" />
                    <span>Cascading Downstream Consequences:</span>
                  </div>
                  {cascadingIssues.map((child) => (
                    <div key={child.id} className="text-xs text-slate-400 bg-slate-950/60 p-2 rounded border border-slate-800 flex items-center justify-between">
                      <span>• Line {child.line}: {child.title} ({child.category})</span>
                      <span className="text-[10px] text-amber-400 font-mono">Downstream</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
