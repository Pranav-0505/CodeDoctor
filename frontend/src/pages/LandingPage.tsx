import React from 'react';
import { Link } from 'react-router-dom';
import { Stethoscope, Shield, Zap, Code2, ArrowRight, CheckCircle, Terminal, Layers } from 'lucide-react';

export const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-between">
      {/* Top Bar */}
      <nav className="h-20 border-b border-slate-800/80 px-8 flex items-center justify-between max-w-7xl mx-auto w-full">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center text-white shadow-lg cyan-glow">
            <Stethoscope className="w-6 h-6" />
          </div>
          <span className="text-xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-200 to-cyan-400 bg-clip-text text-transparent">
            CODE DOCTOR
          </span>
        </div>
        <div className="flex items-center space-x-4">
          <Link to="/login" className="text-sm font-semibold text-slate-300 hover:text-white px-4 py-2">
            Sign In
          </Link>
          <Link to="/dashboard" className="text-sm font-bold bg-cyan-500 hover:bg-cyan-400 text-slate-950 px-5 py-2.5 rounded-lg shadow cyan-glow transition-all">
            Launch Platform
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="max-w-6xl mx-auto px-6 py-20 text-center space-y-8 flex-1 flex flex-col justify-center">
        <div className="inline-flex items-center space-x-2 px-4 py-1.5 rounded-full border border-cyan-500/30 bg-cyan-950/40 text-cyan-400 text-xs font-semibold mx-auto">
          <Stethoscope className="w-4 h-4" />
          <span>Universal Intelligent Code Diagnosis & Repair Platform</span>
        </div>

        <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight leading-tight max-w-4xl mx-auto">
          Diagnose. Repair. Verify. <br />
          <span className="bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-500 bg-clip-text text-transparent">
            Improve Software Health.
          </span>
        </h1>

        <p className="text-slate-400 text-lg max-w-2xl mx-auto leading-relaxed">
          Platform-independent intelligent code diagnosis ecosystem. Root cause analysis, predictive bug detection, Code Surgery repair, and developer Error DNA analytics across IDEs, Web, and CLI.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
          <Link to="/analyzer" className="w-full sm:w-auto px-8 py-4 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 text-slate-950 font-extrabold text-base shadow-lg cyan-glow flex items-center justify-center space-x-2 hover:scale-105 transition-all">
            <span>Diagnose Code Now</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
          <Link to="/scanner" className="w-full sm:w-auto px-8 py-4 rounded-xl border border-slate-800 bg-slate-900/60 text-slate-200 font-bold text-base hover:bg-slate-800 transition-all flex items-center justify-center space-x-2">
            <Terminal className="w-5 h-5 text-cyan-400" />
            <span>Scan Project</span>
          </Link>
        </div>

        {/* Core Pillars */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 pt-16 text-left">
          <div className="p-6 rounded-2xl border border-slate-800/80 bg-slate-900/40 glass-panel space-y-3">
            <Code2 className="w-8 h-8 text-cyan-400" />
            <h3 className="font-bold text-lg text-white">Universal Error Model</h3>
            <p className="text-xs text-slate-400 leading-relaxed">Normalizes Python, JS, C++, and Java syntax, runtime, and type errors into a single diagnostic schema.</p>
          </div>
          <div className="p-6 rounded-2xl border border-slate-800/80 bg-slate-900/40 glass-panel space-y-3">
            <Shield className="w-8 h-8 text-emerald-400" />
            <h3 className="font-bold text-lg text-white">Code Surgery & Repair</h3>
            <p className="text-xs text-slate-400 leading-relaxed">Generates minimal patches, unified diffs, and executes safe verification before applying fixes.</p>
          </div>
          <div className="p-6 rounded-2xl border border-slate-800/80 bg-slate-900/40 glass-panel space-y-3">
            <Zap className="w-8 h-8 text-amber-400" />
            <h3 className="font-bold text-lg text-white">Predictive Analysis</h3>
            <p className="text-xs text-slate-400 leading-relaxed">Detects potential out-of-bounds index access, null pointer dereferences, and infinite loops before execution.</p>
          </div>
          <div className="p-6 rounded-2xl border border-slate-800/80 bg-slate-900/40 glass-panel space-y-3">
            <Layers className="w-8 h-8 text-purple-400" />
            <h3 className="font-bold text-lg text-white">Platform Independent</h3>
            <p className="text-xs text-slate-400 leading-relaxed">Core engine connects seamlessly to Web App, REST API, CLI, VS Code, JetBrains, and CI/CD pipelines.</p>
          </div>
        </div>
      </main>

      <footer className="border-t border-slate-800 py-6 text-center text-xs text-slate-500">
        © 2026 Code Doctor Platform. Universal Intelligent Code Diagnosis Ecosystem.
      </footer>
    </div>
  );
};
