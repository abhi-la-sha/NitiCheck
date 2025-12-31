"""
Pydantic models for request/response validation.
Matches frontend TypeScript interfaces.
"""
from typing import Literal
from pydantic import BaseModel, Field


class Clause(BaseModel):
    """Represents a single risk clause found in the document."""
    clause_id: str = Field(..., description="Unique identifier for the clause")
    text: str = Field(..., description="The actual text of the clause")
    risk_type: str = Field(..., description="Category of risk (e.g., 'High Interest Rate', 'Hidden Fees')")
    severity: Literal["Low", "Medium", "High"] = Field(..., description="Risk severity level")
    explanation: str = Field(..., description="Plain English explanation of the risk")


class DocumentAnalysis(BaseModel):
    """Response model for document analysis endpoint."""
    clauses: list[Clause] = Field(..., description="List of identified risk clauses")

