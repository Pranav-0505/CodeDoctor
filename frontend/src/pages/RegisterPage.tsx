import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Stethoscope, Lock, User as UserIcon, Mail } from 'lucide-react';

export const RegisterPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login(username || 'developer');
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen bg-[#050816] flex items-center justify-center p-6 relative overflow-hidden">
      <div className="w-full max-w-md border border-cyan-500/20 rounded-2xl bg-[#0b1220]/95 p-8 space-y-6 shadow-2xl shadow-cyan-500/10">
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center text-white mx-auto shadow-lg cyan-glow">
            <Stethoscope className="w-7 h-7" />
          </div>
          <h2 className="text-2xl font-extrabold text-white">Create Developer Account</h2>
          <p className="text-xs text-slate-400">Join the universal intelligent code diagnosis platform</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1">Username</label>
            <div className="relative">
              <UserIcon className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                style={{
                  color: '#ffffff',
                  WebkitTextFillColor: '#ffffff',
                  backgroundColor: '#090d16',
                }}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-3 py-2 text-sm text-white focus:border-cyan-500 outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1">Email</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                style={{
                  color: '#ffffff',
                  WebkitTextFillColor: '#ffffff',
                  backgroundColor: '#090d16',
                }}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-3 py-2 text-sm text-white focus:border-cyan-500 outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                style={{
                  color: '#ffffff',
                  WebkitTextFillColor: '#ffffff',
                  backgroundColor: '#090d16',
                }}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-3 py-2 text-sm text-white focus:border-cyan-500 outline-none"
              />
            </div>
          </div>

          <button
            type="submit"
            className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-extrabold py-3 rounded-lg shadow-lg shadow-cyan-500/30 transition-all"
            style={{
              background: 'linear-gradient(90deg, #06b6d4, #2563eb)',
              color: '#ffffff',
              boxShadow: '0 0 25px rgba(6, 182, 212, 0.35)',
            }}
          >
            Register Account
          </button>
        </form>

        <div className="text-center text-xs text-slate-500">
          Already have an account?{' '}
          <Link to="/login" className="text-cyan-400 hover:underline font-semibold">
            Sign In
          </Link>
        </div>
      </div>
    </div>
  );
};
