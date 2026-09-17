import axios from 'axios';
import { DiagnosticResponse, HealthReportResponse } from '../types';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

export const analyzeCode = async (
  code: string,
  language: string = 'python',
  learningLevel: string = 'Beginner'
): Promise<DiagnosticResponse> => {
  const resp = await api.post('/analyze', {
    code,
    language,
    file_path: `snippet.${language === 'javascript' ? 'js' : 'py'}`,
    learning_level: learningLevel,
    platform: 'web'
  });
  return resp.data;
};

export const generateFix = async (code: string, issueId: string, ruleId: string, line: number) => {
  const resp = await api.post('/fix', {
    code,
    issue_id: issueId,
    rule_id: ruleId,
    line
  });
  return resp.data;
};

export const verifyFix = async (originalCode: string, patchedCode: string, ruleId?: string) => {
  const resp = await api.post('/verify', {
    original_code: originalCode,
    patched_code: patchedCode,
    language: 'python',
    rule_id: ruleId
  });
  return resp.data;
};

export const fetchHealthScore = async (): Promise<HealthReportResponse> => {
  const resp = await api.get('/health-score');
  return resp.data;
};

export const fetchErrorDna = async () => {
  const resp = await api.get('/error-dna');
  return resp.data;
};

export const fetchScanHistory = async () => {
  const resp = await api.get('/history');
  return resp.data;
};

export const fetchPlatforms = async () => {
  const resp = await api.get('/platforms');
  return resp.data;
};

export const fetchLanguages = async () => {
  const resp = await api.get('/languages');
  return resp.data;
};
