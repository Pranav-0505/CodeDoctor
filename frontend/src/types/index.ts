export type SeverityLevel = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'INFO';

export type ErrorCategory = 
  | 'SYNTAX'
  | 'TYPE'
  | 'LOGIC'
  | 'RUNTIME'
  | 'MEMORY'
  | 'SECURITY'
  | 'PERFORMANCE'
  | 'STYLE'
  | 'DEPENDENCY'
  | 'CONFIGURATION'
  | 'UNKNOWN';

export interface DiagnosticItem {
  id: string;
  rule_id: string;
  language: string;
  file: string;
  line: number;
  column: number;
  severity: SeverityLevel;
  category: ErrorCategory;
  title: string;
  message: string;
  root_cause?: string;
  explanation?: string;
  impact?: string;
  confidence: number;
  suggested_fix?: string;
  corrected_code?: string;
  verification_status: string;
  is_root_cause: boolean;
  parent_issue_id?: string;
}

export interface DiagnosticResponse {
  scan_id: string;
  file_path: string;
  language: string;
  total_issues: number;
  critical_issues: number;
  security_issues: number;
  performance_issues: number;
  health_score: number;
  issues: DiagnosticItem[];
  root_causes: DiagnosticItem[];
  cascading_issues: DiagnosticItem[];
  learning_level: string;
}

export interface HealthScoreBreakdown {
  overall_score: number;
  correctness_score: number;
  security_score: number;
  maintainability_score: number;
  performance_score: number;
  quality_score: number;
}

export interface HealthReportResponse {
  project_id?: number;
  project_name?: string;
  scanned_files_count: number;
  scores: HealthScoreBreakdown;
  critical_issues_count: number;
  total_issues_count: number;
  recommendations: string[];
}

export interface User {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  learning_level: string;
  is_active: boolean;
  is_admin: boolean;
}
