import { Info } from "lucide-react";

export function Disclaimer() {
  return (
    <footer className="border-t border-border bg-secondary/30">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-start gap-3 max-w-4xl mx-auto">
          <Info className="w-4 h-4 text-muted-foreground flex-shrink-0 mt-0.5" />
          <p className="text-xs text-muted-foreground leading-relaxed">
            <strong className="font-medium">Disclaimer:</strong> This tool provides general 
            information about financial document terms and is intended for educational purposes 
            only. It does not constitute financial, legal, or professional advice. Always consult 
            with qualified professionals before making financial decisions. The analysis may not 
            capture all risks or nuances in your specific documents.
          </p>
        </div>
      </div>
    </footer>
  );
}
