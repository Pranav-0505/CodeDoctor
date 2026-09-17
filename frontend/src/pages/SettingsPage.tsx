import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Settings as SettingsIcon, Save, Key, Sliders, Shield } from 'lucide-react';

export const SettingsPage: React.FC = () => {
  const { learningLevel, setLearningLevel } = useAuth();
  const [apiKey, setApiKey] = useState('');
  const [saved, setSaved] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="space-y-6 p-6">
      <div className="border border-slate-800 rounded-2xl bg-slate-900/80 p-6 glass-panel space-y-6 max-w-3xl">
        <div className="flex items-center space-x-3 border-b border-slate-800 pb-4">
          <SettingsIcon className="w-6 h-6 text-cyan-400" />
          <div>
            <h1 className="text-xl font-extrabold text-white">Platform Settings</h1>
            <p className="text-xs text-slate-400">Configure AI keys, learning modes, and verification safety options</p>
          </div>
        </div>

        <form onSubmit={handleSave} className="space-y-6">
          {/* Learning Tier Selection */}
          <div className="space-y-2">
            <label className="block text-xs font-semibold text-slate-300">Explanation Learning Mode Tier</label>
            <select
              value={learningLevel}
              onChange={(e) => setLearningLevel(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs font-semibold text-white outline-none"
            >
              <option value="Beginner">Beginner (Plain language explanations & fundamentals)</option>
              <option value="Intermediate">Intermediate (Runtime state & standard fixes)</option>
              <option value="Advanced">Advanced (Static bounds analysis & AST rules)</option>
            </select>
          </div>

          {/* Gemini AI API Key */}
          <div className="space-y-2">
            <label className="block text-xs font-semibold text-slate-300 flex items-center space-x-1">
              <Key className="w-4 h-4 text-cyan-400" />
              <span>Google Gemini AI API Key (Optional for AI Enhancement)</span>
            </label>
            <input
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="Paste your GEMINI_API_KEY here..."
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-white outline-none focus:border-cyan-500"
            />
            <p className="text-[11px] text-slate-500">
              Code Doctor functions 100% offline using deterministic rule analyzers even without an AI key.
            </p>
          </div>

          {/* Save Button */}
          <div className="pt-2 flex items-center space-x-4">
            <button
              type="submit"
              className="px-6 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-extrabold text-xs rounded-xl shadow cyan-glow flex items-center space-x-2"
            >
              <Save className="w-4 h-4" />
              <span>Save Settings</span>
            </button>

            {saved && (
              <span className="text-xs font-bold text-emerald-400 animate-pulse">
                ✓ Settings saved successfully!
              </span>
            )}
          </div>
        </form>
      </div>
    </div>
  );
};
