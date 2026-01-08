import { Shield } from "lucide-react";

export function Header() {
  return (
    <header className="bg-header text-header-foreground">
      <div className="container mx-auto px-6 py-5">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-primary/20">
            <Shield className="w-5 h-5 text-primary-foreground" />
          </div>
          <div>
            <h1 className="text-xl font-semibold tracking-tight">
              NitiCheck
            </h1>
            <p className="text-sm text-header-foreground/70">
              Understand financial documents in plain language
            </p>
          </div>
        </div>
      </div>
    </header>
  );
}
