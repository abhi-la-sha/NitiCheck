import { useState } from "react";
import { AlertTriangle, AlertCircle, Info, ChevronDown } from "lucide-react";
import { Clause, RiskSeverity } from "@/types/document";
import { cn } from "@/lib/utils";

interface ClauseHighlightProps {
  clause: Clause;
  index: number;
}

const severityConfig: Record<RiskSeverity, {
  icon: typeof AlertTriangle;
  containerClass: string;
  badgeClass: string;
  iconClass: string;
}> = {
  High: {
    icon: AlertTriangle,
    containerClass: "clause-highlight-high",
    badgeClass: "risk-badge-high",
    iconClass: "text-risk-high",
  },
  Medium: {
    icon: AlertCircle,
    containerClass: "clause-highlight-medium",
    badgeClass: "risk-badge-medium",
    iconClass: "text-risk-medium",
  },
  Low: {
    icon: Info,
    containerClass: "clause-highlight-low",
    badgeClass: "risk-badge-low",
    iconClass: "text-risk-low",
  },
};

export function ClauseHighlight({ clause, index }: ClauseHighlightProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const config = severityConfig[clause.severity];
  const Icon = config.icon;

  return (
    <div
      className={cn(
        "rounded-lg p-4 transition-all duration-200 cursor-pointer animate-fade-in",
        config.containerClass,
        isExpanded && "shadow-panel-hover"
      )}
      style={{ animationDelay: `${index * 50}ms` }}
      onClick={() => setIsExpanded(!isExpanded)}
    >
      <div className="flex items-start gap-3">
        <Icon className={cn("w-5 h-5 mt-0.5 flex-shrink-0", config.iconClass)} />
        
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-2 flex-wrap">
            <span className={cn(
              "inline-flex items-center px-2 py-0.5 rounded text-xs font-medium",
              config.badgeClass
            )}>
              {clause.severity} Risk
            </span>
            <span className="text-xs font-medium text-muted-foreground bg-secondary px-2 py-0.5 rounded">
              {clause.risk_type}
            </span>
          </div>

          <p className="text-sm text-foreground leading-relaxed">
            {clause.text}
          </p>

          {isExpanded && (
            <div className="mt-4 pt-4 border-t border-border/50 animate-fade-in">
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">
                Plain Language Explanation
              </p>
              <p className="text-sm text-foreground/90 leading-relaxed">
                {clause.explanation}
              </p>
            </div>
          )}
        </div>

        <ChevronDown 
          className={cn(
            "w-4 h-4 text-muted-foreground transition-transform duration-200 flex-shrink-0",
            isExpanded && "rotate-180"
          )} 
        />
      </div>
    </div>
  );
}
