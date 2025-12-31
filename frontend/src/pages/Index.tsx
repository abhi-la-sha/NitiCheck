import { useState } from "react";
import { Header } from "@/components/Header";
import { FileUpload } from "@/components/FileUpload";
import { DocumentViewer } from "@/components/DocumentViewer";
import { RiskSummary } from "@/components/RiskSummary";
import { Disclaimer } from "@/components/Disclaimer";
import { DocumentAnalysis } from "@/types/document";
import { analyzeDocument } from "@/services/api";
import { useToast } from "@/hooks/use-toast";

export default function Index() {
  const [analysis, setAnalysis] = useState<DocumentAnalysis | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [fileName, setFileName] = useState<string>("");
  const { toast } = useToast();

  const handleFileSelect = async (file: File) => {
    setIsLoading(true);
    setFileName(file.name);

    try {
      const result= await analyzeDocument(file)
      setAnalysis(result);
    } catch (error) {
      toast({
        title: "Analysis Failed",
        description: "Unable to analyze the document. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Header />

      <main className="flex-1 container mx-auto px-6 py-8">
        {!analysis ? (
          <div className="max-w-2xl mx-auto">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-semibold text-foreground mb-2">
                Upload Your Document
              </h2>
              <p className="text-muted-foreground">
                Upload a financial document to identify and understand risky clauses
              </p>
            </div>
            <FileUpload onFileSelect={handleFileSelect} isLoading={isLoading} />
            
            <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
              <FeatureCard
                title="Identify Risks"
                description="Automatically detect clauses that may not be in your best interest"
              />
              <FeatureCard
                title="Plain Language"
                description="Complex legal terms explained in everyday language"
              />
              <FeatureCard
                title="Risk Scoring"
                description="Visual risk indicators help you understand severity at a glance"
              />
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-14rem)]">
            <div className="lg:col-span-2 min-h-0">
              <DocumentViewer clauses={analysis.clauses} documentName={fileName} />
            </div>
            <div className="min-h-0">
              <RiskSummary clauses={analysis.clauses} />
            </div>
          </div>
        )}
      </main>

      <Disclaimer />
    </div>
  );
}

function FeatureCard({ title, description }: { title: string; description: string }) {
  return (
    <div className="p-6 rounded-xl bg-card border border-border">
      <h3 className="font-semibold text-foreground mb-2">{title}</h3>
      <p className="text-sm text-muted-foreground">{description}</p>
    </div>
  );
}
