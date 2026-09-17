import React, { useState } from 'react';
import { api } from '../services/api';
import { FolderSearch, FileCode, CheckCircle2, AlertTriangle, ShieldAlert, Zap } from 'lucide-react';

export const ProjectScanner: React.FC = () => {
  const [projectPath, setProjectPath] = useState('c:/Users/Admin/Desktop/CodeDoctor/examples');
  const [loading, setLoading] = useState(false);
  const [scanResult, setScanResult] = useState<any>(null);

  const handleScan = async () => {
    setLoading(true);
    try {
      const resp = await api.post('/project/scan', {
        project_path: projectPath,
        project_name: 'Demo Workspace'
      });
      setScanResult(resp.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 p-6">
      <div className="border border-slate-800 rounded-2xl bg-slate-900/80 p-6 glass-panel space-y-4">
        <div className="flex items-center space-x-3">
          <FolderSearch className="w-6 h-6 text-cyan-400" />
          <div>
            <h1 className="text-xl font-extrabold text-white">Project Scanner</h1>
            <p className="text-xs text-slate-400">Scan entire projects respecting .gitignore and folder exclusion rules</p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <input
            type="text"
            value={projectPath}
            onChange={(e) => setProjectPath(e.target.value)}
            placeholder="Path to project directory"
            className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-white focus:border-cyan-500 outline-none"
          />
          <button
            onClick={handleScan}
            disabled={loading}
            className="px-6 py-3 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-extrabold text-sm shadow cyan-glow"
          >
            {loading ? 'Scanning Project...' : 'Start Project Scan'}
          </button>
        </div>
      </div>

      {scanResult && (
        <div className="space-y-6">
          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="p-5 border border-slate-800 rounded-xl bg-slate-900/80 glass-panel">
              <span className="text-xs text-slate-400 font-semibold block">Files Scanned</span>
              <span className="text-3xl font-extrabold text-cyan-400 mt-1 block">{scanResult.scanned_files_count}</span>
            </div>

            <div className="p-5 border border-slate-800 rounded-xl bg-slate-900/80 glass-panel">
              <span className="text-xs text-slate-400 font-semibold block">Total Issues</span>
              <span className="text-3xl font-extrabold text-amber-400 mt-1 block">{scanResult.total_issues}</span>
            </div>

            <div className="p-5 border border-slate-800 rounded-xl bg-slate-900/80 glass-panel">
              <span className="text-xs text-slate-400 font-semibold block">Critical Issues</span>
              <span className="text-3xl font-extrabold text-rose-400 mt-1 block">{scanResult.critical_issues}</span>
            </div>

            <div className="p-5 border border-slate-800 rounded-xl bg-slate-900/80 glass-panel">
              <span className="text-xs text-slate-400 font-semibold block">Project Health Score</span>
              <span className="text-3xl font-extrabold text-emerald-400 mt-1 block">{scanResult.health_score} / 100</span>
            </div>
          </div>

          {/* Files Details List */}
          <div className="border border-slate-800 rounded-2xl bg-slate-900/80 p-6 glass-panel space-y-4">
            <h3 className="font-bold text-sm text-white">Scanned File Results</h3>
            <div className="space-y-3">
              {scanResult.file_results.map((res: any, i: number) => (
                <div key={i} className="p-4 border border-slate-800 rounded-xl bg-slate-950 text-xs space-y-2">
                  <div className="flex items-center justify-between font-bold">
                    <span className="text-cyan-400 flex items-center space-x-2">
                      <FileCode className="w-4 h-4" />
                      <span>{res.file_path}</span>
                    </span>
                    <span className="text-slate-400">Issues: {res.total_issues} | Health: {res.health_score}/100</span>
                  </div>
                  {res.issues && res.issues.map((iss: any, j: number) => (
                    <div key={j} className="text-slate-300 pl-6 text-[11px]">
                      • Line {iss.line}: [{iss.severity}] {iss.title} ({iss.category})
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
