export type RiskSeverity = "Low" | "Medium" | "High";

export interface Clause {
  clause_id: string;
  text: string;
  risk_type: string;
  severity: RiskSeverity;
  explanation: string;
}

export interface DocumentAnalysis {
  clauses: Clause[];
}

export interface RiskCount {
  type: string;
  count: number;
  highCount: number;
  mediumCount: number;
  lowCount: number;
}
