import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { Header } from './components/Header';
import { Sidebar } from './components/Sidebar';

import { LandingPage } from './pages/LandingPage';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { Dashboard } from './pages/Dashboard';
import { CodeAnalyzer } from './pages/CodeAnalyzer';
import { ProjectScanner } from './pages/ProjectScanner';
import { DiagnosisDetails } from './pages/DiagnosisDetails';
import { CodeSurgery } from './pages/CodeSurgery';
import { ErrorDnaPage } from './pages/ErrorDnaPage';
import { HealthReport } from './pages/HealthReport';
import { SecurityReport } from './pages/SecurityReport';
import { PerformanceReport } from './pages/PerformanceReport';
import { HistoryPage } from './pages/HistoryPage';
import { SettingsPage } from './pages/SettingsPage';
import { ApiDocsPage } from './pages/ApiDocsPage';
import { PlatformIntegrations } from './pages/PlatformIntegrations';

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public Landing & Auth pages */}
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Authenticated Dashboard layout */}
          <Route
            path="/*"
            element={
              <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100">
                <Header />
                <div className="flex flex-1">
                  <Sidebar />
                  <main className="flex-1 bg-slate-950/90 overflow-y-auto">
                    <Routes>
                      <Route path="/dashboard" element={<Dashboard />} />
                      <Route path="/analyzer" element={<CodeAnalyzer />} />
                      <Route path="/scanner" element={<ProjectScanner />} />
                      <Route path="/details" element={<DiagnosisDetails />} />
                      <Route path="/surgery" element={<CodeSurgery />} />
                      <Route path="/error-dna" element={<ErrorDnaPage />} />
                      <Route path="/health" element={<HealthReport />} />
                      <Route path="/security" element={<SecurityReport />} />
                      <Route path="/performance" element={<PerformanceReport />} />
                      <Route path="/history" element={<HistoryPage />} />
                      <Route path="/platforms" element={<PlatformIntegrations />} />
                      <Route path="/api-docs" element={<ApiDocsPage />} />
                      <Route path="/settings" element={<SettingsPage />} />
                    </Routes>
                  </main>
                </div>
              </div>
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
};
