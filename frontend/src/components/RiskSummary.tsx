import { useMemo } from "react";
import { AlertTriangle, AlertCircle, Info, BarChart3, TrendingUp } from "lucide-react";
import { Clause, RiskSeverity } from "@/types/document";
import { cn } from "@/lib/utils";

interface RiskSummaryProps {
  clauses: Clause[];
}

export function RiskSummary({ clauses }: RiskSummaryProps) {
  const stats = useMemo(() => {
    const byType: Record<string, { total: number; high: number; medium: number; low: number }> = {};
    let high = 0, medium = 0, low = 0;

    clauses.forEach((clause) => {
      if (!byType[clause.risk_type]) {
        byType[clause.risk_type] = { total: 0, high: 0, medium: 0, low: 0 };
      }
      byType[clause.risk_type].total++;
      byType[clause.risk_type][clause.severity.toLowerCase() as 'high' | 'medium' | 'low']++;

      if (clause.severity === "High") high++;
      else if (clause.severity === "Medium") medium++;
      else low++;
    });

    return { byType, high, medium, low, total: clauses.length };
  }, [clauses]);

  const riskScore = useMemo(() => {
    const score = (stats.high * 3 + stats.medium * 2 + stats.low * 1) / (stats.total * 3) * 100;
    return Math.round(score);
  }, [stats]);

  const getRiskLevel = (score: number): { label: string; color: string } => {
    if (score >= 70) return { label: "High Risk", color: "text-risk-high" };
    if (score >= 40) return { label: "Moderate Risk", color: "text-risk-medium" };
    return { label: "Low Risk", color: "text-risk-low" };
  };

  const riskLevel = getRiskLevel(riskScore);

  return (
    <div className="bg-panel rounded-xl border border-panel-border shadow-panel h-full flex flex-col">
      <div className="px-5 py-4 border-b border-border flex items-center gap-3">
        <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-secondary">
          <BarChart3 className="w-4 h-4 text-muted-foreground" />
        </div>
        <h2 className="font-semibold text-foreground">Risk Summary</h2>
      </div>

      <div className="flex-1 overflow-y-auto p-5 space-y-6 scrollbar-thin">
        {/* Risk Score */}
        <div className="bg-secondary/50 rounded-xl p-5 text-center">
          <div className="flex items-center justify-center gap-2 mb-2">
            <TrendingUp className={cn("w-5 h-5", riskLevel.color)} />
            <span className={cn("text-sm font-medium", riskLevel.color)}>
              {riskLevel.label}
            </span>
          </div>
          <div className="text-4xl font-bold text-foreground mb-1">
            {riskScore}
            <span className="text-lg text-muted-foreground font-normal">/100</span>
          </div>
          <p className="text-xs text-muted-foreground">Overall Risk Score</p>
        </div>

        {/* Severity Breakdown */}
        <div>
          <h3 className="text-sm font-medium text-foreground mb-3">By Severity</h3>
          <div className="grid grid-cols-3 gap-3">
            <SeverityCard
              icon={AlertTriangle}
              label="High"
              count={stats.high}
              variant="high"
            />
            <SeverityCard
              icon={AlertCircle}
              label="Medium"
              count={stats.medium}
              variant="medium"
            />
            <SeverityCard
              icon={Info}
              label="Low"
              count={stats.low}
              variant="low"
            />
          </div>
        </div>

        {/* By Risk Type */}
        <div>
          <h3 className="text-sm font-medium text-foreground mb-3">By Category</h3>
          <div className="space-y-2">
            {Object.entries(stats.byType).map(([type, counts]) => (
              <div
                key={type}
                className="flex items-center justify-between p-3 bg-secondary/30 rounded-lg"
              >
                <span className="text-sm font-medium text-foreground">{type}</span>
                <div className="flex items-center gap-2">
                  {counts.high > 0 && (
                    <span className="risk-badge-high text-xs px-1.5 py-0.5 rounded">
                      {counts.high}
                    </span>
                  )}
                  {counts.medium > 0 && (
                    <span className="risk-badge-medium text-xs px-1.5 py-0.5 rounded">
                      {counts.medium}
                    </span>
                  )}
                  {counts.low > 0 && (
                    <span className="risk-badge-low text-xs px-1.5 py-0.5 rounded">
                      {counts.low}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Total Clauses */}
        <div className="pt-4 border-t border-border">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Total Clauses Analyzed</span>
            <span className="font-semibold text-foreground">{stats.total}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

interface SeverityCardProps {
  icon: typeof AlertTriangle;
  label: string;
  count: number;
  variant: "high" | "medium" | "low";
}

function SeverityCard({ icon: Icon, label, count, variant }: SeverityCardProps) {
  const variantStyles = {
    high: "bg-risk-high-bg border-risk-high/20",
    medium: "bg-risk-medium-bg border-risk-medium/20",
    low: "bg-risk-low-bg border-risk-low/20",
  };

  const iconStyles = {
    high: "text-risk-high",
    medium: "text-risk-medium",
    low: "text-risk-low",
  };

  return (
    <div className={cn(
      "p-3 rounded-lg border text-center",
      variantStyles[variant]
    )}>
      <Icon className={cn("w-5 h-5 mx-auto mb-1", iconStyles[variant])} />
      <div className="text-2xl font-bold text-foreground">{count}</div>
      <div className="text-xs text-muted-foreground">{label}</div>
    </div>
  );
}
