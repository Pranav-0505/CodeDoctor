import React, { useState } from 'react';
import { CodeEditor } from '../components/CodeEditor';
import { DiffViewer } from '../components/DiffViewer';
import { RootCauseGraph } from '../components/RootCauseGraph';
import { analyzeCode, generateFix, verifyFix } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { DiagnosticResponse, DiagnosticItem } from '../types';
import { Stethoscope, Play, Syringe, CheckCircle2, AlertTriangle, Shield, Zap, Sparkles } from 'lucide-react';

const INITIAL_PYTHON_DEMO = `# Code Doctor Demo — Multi-Issue Diagnostic Sample
items = [10, 20, 30]

# 1. Predictive IndexError (Accessed at index 5 when length is 3)
val = items[5]

# 2. Security Doctor: Exposed API Secret Key
API_KEY = "sk-1234567890abcdef12345678"

# 3. Performance Doctor: Deeply Nested Loops
for i in range(5):
    for j in range(5):
        for k in range(5):
            print(i, j, k)
`;

export const CodeAnalyzer: React.FC = () => {
  const { learningLevel } = useAuth();
  const [code, setCode] = useState(INITIAL_PYTHON_DEMO);
  const [language, setLanguage] = useState('python');
  const [diagnostics, setDiagnostics] = useState<DiagnosticResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeFix, setActiveFix] = useState<{ issueId: string; patched: string; diff: string } | null>(null);
  const [verificationResult, setVerificationResult] = useState<any>(null);

  const handleRunAnalysis = async () => {
    setLoading(true);
    setActiveFix(null);
    setVerificationResult(null);
    try {
      const res = await analyzeCode(code, language, learningLevel);
      setDiagnostics(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handlePreviewFix = async (item: DiagnosticItem) => {
    try {
      const res = await generateFix(code, item.id, item.rule_id, item.line);
      setActiveFix({
        issueId: item.id,
        patched: res.patched_code,
        diff: res.diff_patch
      });
      setVerificationResult(null);
    } catch (err) {
      console.error(err);
    }
  };

  const handleVerifyFix = async (item: DiagnosticItem) => {
    if (!activeFix) return;
    try {
      const res = await verifyFix(code, activeFix.patched, item.rule_id);
      setVerificationResult(res);
    } catch (err) {
      console.error(err);
    }
  };

  const handleApplyFix = () => {
    if (activeFix) {
      setCode(activeFix.patched);
      setActiveFix(null);
      setVerificationResult(null);
    }
  };

  return (
    <div className="space-y-6 p-6">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border border-slate-800 rounded-2xl bg-slate-900/80 p-5 glass-panel">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-cyan-950 border border-cyan-800 flex items-center justify-center text-cyan-400">
            <Stethoscope className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-xl font-extrabold text-white">Interactive Code Surgery Analyzer</h1>
            <p className="text-xs text-slate-400">Split-screen diagnostic workspace with real-time root cause resolution</p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs font-semibold text-white outline-none"
          >
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
            <option value="generic">C++ / Java / Generic</option>
          </select>

          <button
            onClick={handleRunAnalysis}
            disabled={loading}
            className="px-6 py-2.5 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-extrabold text-xs shadow cyan-glow flex items-center space-x-2 transition-all"
          >
            <Play className="w-4 h-4" />
            <span>{loading ? 'Diagnosing...' : 'Diagnose Code'}</span>
          </button>
        </div>
      </div>

      {/* Split Screen Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* LEFT PANEL: CODE EDITOR */}
        <div className="space-y-4">
          <div className="flex items-center justify-between text-xs text-slate-400 font-semibold px-1">
            <span>Source Code Buffer</span>
            <span>{language.toUpperCase()} • Level: {learningLevel}</span>
          </div>
          <CodeEditor code={code} onChange={setCode} language={language} />

          {/* Diff Patch Preview when Fix Preview Active */}
          {activeFix && (
            <div className="space-y-3 pt-2">
              <DiffViewer diffPatch={activeFix.diff} />
              <div className="flex items-center space-x-3">
                <button
                  onClick={() => handleVerifyFix(diagnostics!.issues[0])}
                  className="px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs rounded-lg shadow flex items-center space-x-1"
                >
                  <Sparkles className="w-4 h-4" />
                  <span>Verify Fix</span>
                </button>
                <button
                  onClick={handleApplyFix}
                  disabled={verificationResult && !verificationResult.passed}
                  className="px-4 py-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-extrabold text-xs rounded-lg shadow flex items-center space-x-1"
                >
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Apply Fix</span>
                </button>
              </div>

              {verificationResult && (
                <div className={`p-3 rounded-lg text-xs font-semibold border ${
                  verificationResult.passed
                    ? 'bg-emerald-950/40 border-emerald-800 text-emerald-300'
                    : 'bg-rose-950/40 border-rose-800 text-rose-300'
                }`}>
                  Status: {verificationResult.status} • {verificationResult.details}
                </div>
              )}
            </div>
          )}
        </div>

        {/* RIGHT PANEL: DIAGNOSIS RESULTS */}
        <div className="space-y-4">
          <div className="flex items-center justify-between text-xs text-slate-400 font-semibold px-1">
            <span>Diagnosis & Treatment Panel</span>
            {diagnostics && (
              <span className="text-cyan-400 font-bold">
                Health Score: {diagnostics.health_score}/100
              </span>
            )}
          </div>

          {!diagnostics ? (
            <div className="border border-slate-800 rounded-xl bg-slate-900/40 p-12 text-center text-slate-500 text-xs space-y-3">
              <Stethoscope className="w-8 h-8 mx-auto text-slate-600" />
              <p>Click "Diagnose Code" to inspect syntax, logic, security, and performance problems.</p>
            </div>
          ) : (
            <div className="space-y-4 overflow-y-auto max-h-[640px] pr-1">
              {/* Root Cause Graph Component */}
              <RootCauseGraph
                rootCauses={diagnostics.root_causes}
                cascadingIssues={diagnostics.cascading_issues}
              />

              {/* Diagnostic Cards */}
              {diagnostics.issues.map((item) => (
                <div key={item.id} className="border border-slate-800 rounded-xl bg-slate-900/90 p-5 space-y-3 glass-panel">
                  <div className="flex items-center justify-between border-b border-slate-800/80 pb-2">
                    <div className="flex items-center space-x-2">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-extrabold ${
                        item.severity === 'CRITICAL' || item.severity === 'HIGH'
                          ? 'bg-rose-950 text-rose-400 border border-rose-800'
                          : 'bg-amber-950 text-amber-400 border border-amber-800'
                      }`}>
                        {item.severity}
                      </span>
                      <span className="text-xs font-bold text-white">{item.title}</span>
                    </div>
                    <span className="text-[11px] text-slate-400 font-mono">Line {item.line}:{item.column}</span>
                  </div>

                  <div className="text-xs space-y-1 text-slate-300">
                    <div><span className="text-slate-500 font-semibold">Message:</span> {item.message}</div>
                    <div><span className="text-slate-500 font-semibold">Explanation ({learningLevel}):</span> {item.explanation}</div>
                    <div><span className="text-slate-500 font-semibold">Confidence:</span> {Math.round(item.confidence * 100)}%</div>
                  </div>

                  <div className="flex items-center space-x-2 pt-2 border-t border-slate-800/60">
                    <button
                      onClick={() => handlePreviewFix(item)}
                      className="px-3 py-1.5 bg-cyan-950 hover:bg-cyan-900 border border-cyan-800 text-cyan-300 font-bold text-xs rounded-md flex items-center space-x-1"
                    >
                      <Syringe className="w-3.5 h-3.5" />
                      <span>Preview Fix</span>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
