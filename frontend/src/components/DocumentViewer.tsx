import { FileText } from "lucide-react";
import { Clause } from "@/types/document";
import { ClauseHighlight } from "./ClauseHighlight";

interface DocumentViewerProps {
  clauses: Clause[];
  documentName?: string;
}

export function DocumentViewer({ clauses, documentName }: DocumentViewerProps) {
  const sortedClauses = [...clauses].sort((a, b) => {
    const severityOrder = { High: 0, Medium: 1, Low: 2 };
    return severityOrder[a.severity] - severityOrder[b.severity];
  });

  return (
    <div className="bg-panel rounded-xl border border-panel-border shadow-panel h-full flex flex-col">
      <div className="px-5 py-4 border-b border-border flex items-center gap-3">
        <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-secondary">
          <FileText className="w-4 h-4 text-muted-foreground" />
        </div>
        <div>
          <h2 className="font-semibold text-foreground">Document Analysis</h2>
          {documentName && (
            <p className="text-xs text-muted-foreground">{documentName}</p>
          )}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-5 space-y-3 scrollbar-thin">
        {sortedClauses.map((clause, index) => (
          <ClauseHighlight key={clause.clause_id} clause={clause} index={index} />
        ))}
      </div>
    </div>
  );
}
