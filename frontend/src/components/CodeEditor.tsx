import React from 'react';

interface CodeEditorProps {
  code: string;
  onChange: (value: string) => void;
  language?: string;
  readOnly?: boolean;
}

export const CodeEditor: React.FC<CodeEditorProps> = ({ code, onChange, readOnly = false }) => {
  const lines = code.split('\n');

  return (
    <div className="relative border border-slate-800 rounded-xl bg-slate-950 overflow-hidden font-mono text-sm shadow-inner flex">
      {/* Line Numbers */}
      <div className="w-12 bg-slate-900/80 border-r border-slate-800/80 py-3 text-right pr-3 select-none text-slate-600 text-xs leading-6">
        {lines.map((_, i) => (
          <div key={i}>{i + 1}</div>
        ))}
      </div>

      {/* Code Textarea */}
      <textarea
        value={code}
        onChange={(e) => onChange(e.target.value)}
        readOnly={readOnly}
        spellCheck={false}
        className="w-full bg-transparent text-slate-100 p-3 outline-none resize-none code-font leading-6 min-h-[360px]"
      />
    </div>
  );
};
