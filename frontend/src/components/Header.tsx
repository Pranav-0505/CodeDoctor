import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Stethoscope, Shield, Zap, BookOpen, User as UserIcon } from 'lucide-react';

export const Header: React.FC = () => {
  const { learningLevel, setLearningLevel, user } = useAuth();

  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/80 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-40">
      <div className="flex items-center space-x-3">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center text-white shadow-lg cyan-glow">
          <Stethoscope className="w-5 h-5" />
        </div>
        <div>
          <span className="text-lg font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-200 to-cyan-400 bg-clip-text text-transparent">
            CODE DOCTOR
          </span>
          <span className="ml-2 text-xs font-semibold px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800">
            v1.0 ENGINE
          </span>
        </div>
      </div>

      <div className="flex items-center space-x-4">
        {/* Learning Mode Tier Selector */}
        <div className="flex items-center space-x-2 bg-slate-950 border border-slate-800 rounded-lg p-1">
          <BookOpen className="w-4 h-4 text-cyan-400 ml-2" />
          <span className="text-xs font-medium text-slate-400 mr-1">Level:</span>
          {(['Beginner', 'Intermediate', 'Advanced'] as const).map((lvl) => (
            <button
              key={lvl}
              onClick={() => setLearningLevel(lvl)}
              className={`px-2.5 py-1 text-xs font-semibold rounded-md transition-all ${
                learningLevel === lvl
                  ? 'bg-cyan-500 text-slate-950 font-bold shadow'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`}
            >
              {lvl}
            </button>
          ))}
        </div>

        {/* User Profile Badge */}
        {user && (
          <div className="flex items-center space-x-2 bg-slate-800/60 border border-slate-700/50 rounded-lg px-3 py-1.5 text-xs text-slate-200">
            <UserIcon className="w-4 h-4 text-cyan-400" />
            <span className="font-semibold">{user.username}</span>
          </div>
        )}
      </div>
    </header>
  );
};
