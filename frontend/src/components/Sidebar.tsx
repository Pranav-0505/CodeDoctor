import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Code2,
  FolderSearch,
  Activity,
  Syringe,
  Dna,
  ShieldAlert,
  Zap,
  History,
  Settings,
  BookOpen,
  Layers,
  Home,
  UserCheck
} from 'lucide-react';

const NAV_ITEMS = [
  { path: '/', label: 'Landing Page', icon: Home },
  { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/analyzer', label: 'Code Analyzer', icon: Code2 },
  { path: '/scanner', label: 'Project Scanner', icon: FolderSearch },
  { path: '/surgery', label: 'Code Surgery', icon: Syringe },
  { path: '/error-dna', label: 'Error DNA', icon: Dna },
  { path: '/health', label: 'Health Report', icon: Activity },
  { path: '/security', label: 'Security Doctor', icon: ShieldAlert },
  { path: '/performance', label: 'Performance Doctor', icon: Zap },
  { path: '/history', label: 'Scan History', icon: History },
  { path: '/platforms', label: 'Platforms & Adapters', icon: Layers },
  { path: '/api-docs', label: 'API Reference', icon: BookOpen },
  { path: '/settings', label: 'Settings', icon: Settings },
  { path: '/login', label: 'Login', icon: UserCheck }
];

export const Sidebar: React.FC = () => {
  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-900/60 backdrop-blur-md flex flex-col justify-between p-4 sticky top-16 h-[calc(100vh-4rem)] overflow-y-auto">
      <div className="space-y-1">
        <div className="px-3 py-2 text-xs font-semibold text-slate-500 uppercase tracking-wider">
          Platform Workspace
        </div>
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-gradient-to-r from-cyan-500/20 to-blue-500/10 text-cyan-400 border border-cyan-500/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`
              }
            >
              <Icon className="w-4 h-4" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </div>

      <div className="mt-6 pt-4 border-t border-slate-800/80 px-3 py-2 text-xs text-slate-500 text-center">
        Diagnose • Repair • Verify • Improve
      </div>
    </aside>
  );
};
