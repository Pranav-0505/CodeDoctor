import React, { createContext, useContext, useState, useEffect } from 'react';
import { User } from '../types';

interface AuthContextType {
  user: User | null;
  learningLevel: string;
  setLearningLevel: (level: string) => void;
  login: (username: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>({
    id: 1,
    username: 'developer',
    email: 'developer@codedoctor.io',
    full_name: 'Senior Lead Architect',
    learning_level: 'Beginner',
    is_active: true,
    is_admin: true
  });
  const [learningLevel, setLearningLevel] = useState<string>('Beginner');

  const login = (username: string) => {
    setUser({
      id: 1,
      username,
      email: `${username}@codedoctor.io`,
      learning_level: learningLevel,
      is_active: true,
      is_admin: true
    });
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, learningLevel, setLearningLevel, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
};
