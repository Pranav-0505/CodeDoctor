import React from 'react';

interface DiffViewerProps {
  diffPatch: string;
}

export const DiffViewer: React.FC<DiffViewerProps> = ({ diffPatch }) => {
  const lines = diffPatch.split('\n');

  return (
    <div className="border border-slate-800 rounded-xl bg-slate-950 p-4 font-mono text-xs overflow-x-auto leading-6 shadow-inner">
      <div className="text-slate-500 font-bold mb-2 pb-1 border-b border-slate-800 uppercase tracking-wider text-[10px]">
        Unified Diff Preview (Code Surgery Patch)
      </div>
      {lines.map((line, idx) => {
        let bgClass = 'text-slate-400';
        if (line.startsWith('+')) bgClass = 'bg-emerald-950/40 text-emerald-400 font-semibold px-1 rounded';
        else if (line.startsWith('-')) bgClass = 'bg-rose-950/40 text-rose-400 font-semibold px-1 rounded';
        else if (line.startsWith('@@')) bgClass = 'text-cyan-400 font-bold';

        return (
          <div key={idx} className={bgClass}>
            {line}
          </div>
        );
      })}
    </div>
  );
};
