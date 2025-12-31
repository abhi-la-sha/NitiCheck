import { DocumentAnalysis } from "@/types/document";
import.meta.env;

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function analyzeDocument(file: File): Promise<DocumentAnalysis> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/api/analyze`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Document Analysis Failed");
  }

  return (await response.json()) as DocumentAnalysis;
}

