import React from 'react';
import { BookOpen, ExternalLink, Code2 } from 'lucide-react';

export const ApiDocsPage: React.FC = () => {
  return (
    <div className="space-y-6 p-6">
      <div className="border border-slate-800 rounded-2xl bg-slate-900/80 p-6 glass-panel space-y-6">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center space-x-3">
            <BookOpen className="w-6 h-6 text-cyan-400" />
            <div>
              <h1 className="text-xl font-extrabold text-white">Code Doctor REST API Specification</h1>
              <p className="text-xs text-slate-400">OpenAPI versioned endpoints (`/api/v1`)</p>
            </div>
          </div>
          <a
            href="http://127.0.0.1:8000/docs"
            target="_blank"
            rel="noreferrer"
            className="px-4 py-2 bg-cyan-950 hover:bg-cyan-900 text-cyan-400 border border-cyan-800 text-xs font-bold rounded-lg flex items-center space-x-2"
          >
            <span>Open Swagger UI</span>
            <ExternalLink className="w-4 h-4" />
          </a>
        </div>

        <div className="space-y-4 text-xs font-mono">
          <div className="p-4 border border-slate-800 rounded-xl bg-slate-950 space-y-1">
            <span className="text-emerald-400 font-bold">POST /api/v1/analyze</span>
            <p className="text-slate-400 font-sans">Submit source code snippet for AST and static diagnostic analysis.</p>
          </div>

          <div className="p-4 border border-slate-800 rounded-xl bg-slate-950 space-y-1">
            <span className="text-emerald-400 font-bold">POST /api/v1/fix</span>
            <p className="text-slate-400 font-sans">Generate minimal Code Surgery patch and unified diff preview.</p>
          </div>

          <div className="p-4 border border-slate-800 rounded-xl bg-slate-950 space-y-1">
            <span className="text-emerald-400 font-bold">POST /api/v1/verify</span>
            <p className="text-slate-400 font-sans">Execute safe static verification on generated patches.</p>
          </div>

          <div className="p-4 border border-slate-800 rounded-xl bg-slate-950 space-y-1">
            <span className="text-cyan-400 font-bold">GET /api/v1/health-score</span>
            <p className="text-slate-400 font-sans">Retrieve weighted Code Health Score breakdown.</p>
          </div>

          <div className="p-4 border border-slate-800 rounded-xl bg-slate-950 space-y-1">
            <span className="text-cyan-400 font-bold">GET /api/v1/error-dna</span>
            <p className="text-slate-400 font-sans">Retrieve developer Error DNA profile and mistake analytics.</p>
          </div>
        </div>
      </div>
    </div>
  );
};
