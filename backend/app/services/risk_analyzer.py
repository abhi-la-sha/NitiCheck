"""
Risk analysis service using rule-based and heuristic patterns.
Analyzes financial documents for various risk indicators.
"""
import re
import uuid
from typing import List, Dict, Tuple, Optional
from app.models.schemas import Clause
from app.utils.text_cleaner import extract_numbers


class RiskAnalyzer:
    """
    Analyzes text for financial risk indicators using pattern matching
    and heuristic rules.
    """
    
    # Negative context indicators that negate risk (e.g., "no penalty", "penalty waived")
    NEGATIVE_INDICATORS = [
        r"\bno\s+",
        r"\bnot\s+",
        r"\bwithout\s+",
        r"\bwaived?\b",
        r"\bexempt\b",
        r"\bexcluded\b",
        r"\bnot\s+applicable\b",
        r"\bdoes\s+not\s+",
        r"\bwill\s+not\s+",
        r"\bshall\s+not\s+",
        r"\bmay\s+not\s+",
        r"\bcannot\b",
        r"\bprohibited\b",
        r"\bforbidden\b",
        r"\bunavailable\b",
        r"\bnot\s+subject\s+to\b",
        r"\bnot\s+liable\s+for\b",
        r"\bno\s+charge\s+for\b",
        r"\bno\s+fee\s+for\b",
        r"\bno\s+penalty\b",
        r"\bpenalty\s+waived\b",
        r"\bfee\s+waived\b",
        r"\bno\s+interest\b",
        r"\binterest\s+free\b",
        r"\bzero\s+interest\b"
    ]
    
    # Risk pattern definitions
    RISK_PATTERNS: Dict[str, Dict] = {
        "high_interest": {
            "keywords": [
                r"interest\s+rate",
                r"apr\s*(?:of|is|at)?",
                r"annual\s+percentage\s+rate",
                r"interest\s+charged",
                r"rate\s+of\s+interest"
            ],
            "threshold": 18.0,  # Percentage threshold for high interest
            "risk_type": "High Interest Rate",
            "base_severity": "High"
        },
        "hidden_fees": {
            "keywords": [
                r"hidden\s+fee",
                r"administrative\s+fee",
                r"processing\s+fee",
                r"service\s+charge",
                r"convenience\s+fee",
                r"maintenance\s+fee",
                r"annual\s+fee",
                r"late\s+fee",
                r"overdraft\s+fee",
                r"transaction\s+fee",
                r"application\s+fee",
                r"origination\s+fee"
            ],
            "risk_type": "Hidden Fees",
            "base_severity": "Medium"
        },
        "penalty_clauses": {
            "keywords": [
                r"penalty",
                r"penal\s+interest",
                r"default\s+rate",
                r"penalty\s+charge",
                r"penalty\s+fee",
                r"breach\s+penalty",
                r"violation\s+penalty"
            ],
            "risk_type": "Penalty Clauses",
            "base_severity": "High"
        },
        "auto_renewal": {
            "keywords": [
                r"auto[-\s]?renew",
                r"automatic\s+renewal",
                r"auto[-\s]?extend",
                r"automatic\s+extension",
                r"renew\s+automatically",
                r"continuous\s+renewal"
            ],
            "risk_type": "Auto-Renewal",
            "base_severity": "Medium"
        },
        "one_sided_termination": {
            "keywords": [
                r"sole\s+discretion",
                r"without\s+notice",
                r"terminate\s+at\s+any\s+time",
                r"termination\s+without\s+cause",
                r"unilateral\s+termination",
                r"terminate\s+immediately",
                r"at\s+our\s+discretion",
                r"we\s+may\s+terminate",
                r"reserve\s+the\s+right\s+to\s+terminate"
            ],
            "risk_type": "One-Sided Termination",
            "base_severity": "High"
        },
        "arbitration_clause": {
            "keywords": [
                r"binding\s+arbitration",
                r"mandatory\s+arbitration",
                r"waive\s+right\s+to\s+sue",
                r"class\s+action\s+waiver",
                r"dispute\s+resolution\s+by\s+arbitration"
            ],
            "risk_type": "Arbitration Clause",
            "base_severity": "Low"
        },
        "variable_rate": {
            "keywords": [
                r"variable\s+rate",
                r"adjustable\s+rate",
                r"rate\s+may\s+change",
                r"rate\s+subject\s+to\s+change",
                r"floating\s+rate"
            ],
            "risk_type": "Variable Interest Rate",
            "base_severity": "Medium"
        },
        "prepayment_penalty": {
            "keywords": [
                r"prepayment\s+penalty",
                r"early\s+payment\s+penalty",
                r"prepayment\s+charge",
                r"early\s+termination\s+fee"
            ],
            "risk_type": "Prepayment Penalty",
            "base_severity": "Medium"
        }
    }
    
    @staticmethod
    def analyze_document(text: str) -> List[Clause]:
        """
        Analyze document text and identify risk clauses.
        
        Args:
            text: Full document text
            
        Returns:
            List of identified risk clauses
        """
        if not text or len(text.strip()) < 50:
            return []
        
        # Normalize text for pattern matching
        normalized_text = text.lower()
        
        # Split text into clauses for analysis
        from app.utils.text_cleaner import split_into_clauses
        clauses = split_into_clauses(text, min_length=30)
        
        identified_risks: List[Clause] = []
        seen_clauses: set = set()  # Avoid duplicates
        
        # Analyze each clause
        for clause_text in clauses:
            clause_lower = clause_text.lower()
            clause_id = str(uuid.uuid4())
            
            # Check each risk pattern
            for pattern_key, pattern_config in RiskAnalyzer.RISK_PATTERNS.items():
                matches = RiskAnalyzer._check_pattern(
                    clause_lower,
                    clause_text,
                    pattern_config
                )
                
                if matches:
                    severity, explanation = matches
                    
                    # Create unique identifier for this clause
                    clause_hash = hash(clause_text[:100] + pattern_config["risk_type"])
                    if clause_hash in seen_clauses:
                        continue
                    seen_clauses.add(clause_hash)
                    
                    identified_risks.append(Clause(
                        clause_id=clause_id,
                        text=clause_text[:500],  # Limit text length
                        risk_type=pattern_config["risk_type"],
                        severity=severity,
                        explanation=explanation
                    ))
                    break  # One risk per clause to avoid duplicates
        
        return identified_risks
    
    @staticmethod
    def _has_negative_context(clause_lower: str, keyword_match_pos: int) -> bool:
        """
        Check if the keyword match is in a negative context.
        
        Args:
            clause_lower: Lowercase clause text
            keyword_match_pos: Position where keyword was found
            
        Returns:
            True if negative context detected (e.g., "no penalty"), False otherwise
        """
        # Check a window of text before the keyword (up to 50 characters)
        context_start = max(0, keyword_match_pos - 50)
        context_before = clause_lower[context_start:keyword_match_pos]
        
        # Check for negative indicators in the context
        for negative_pattern in RiskAnalyzer.NEGATIVE_INDICATORS:
            if re.search(negative_pattern, context_before, re.IGNORECASE):
                return True
        
        return False
    
    @staticmethod
    def _check_pattern(
        clause_lower: str,
        clause_original: str,
        pattern_config: Dict
    ) -> Optional[Tuple[str, str]]:
        """
        Check if clause matches a risk pattern, considering context.
        
        Returns:
            Tuple of (severity, explanation) if match found, None otherwise
        """
        keywords = pattern_config["keywords"]
        risk_type = pattern_config["risk_type"]
        base_severity = pattern_config.get("base_severity", "Medium")
        
        # Check if any keyword matches
        matched_keyword = None
        match_position = -1
        for keyword_pattern in keywords:
            match = re.search(keyword_pattern, clause_lower, re.IGNORECASE)
            if match:
                matched_keyword = keyword_pattern
                match_position = match.start()
                break
        
        if not matched_keyword:
            return None
        
        # Check for negative context (e.g., "no penalty", "penalty waived")
        if RiskAnalyzer._has_negative_context(clause_lower, match_position):
            return None  # Skip this match - it's negated
        
        # Special handling for interest rate patterns
        if "interest" in risk_type.lower() and "threshold" in pattern_config:
            threshold = pattern_config["threshold"]
            numbers = extract_numbers(clause_original)
            
            # Check if any number exceeds threshold
            high_rate_found = False
            for num in numbers:
                if num >= threshold:
                    high_rate_found = True
                    severity = "High"
                    explanation = (
                        f"Identified interest rate of {num}% which exceeds "
                        f"the typical threshold of {threshold}%. This is considered "
                        f"a high interest rate that may result in significant "
                        f"financial burden over time."
                    )
                    return (severity, explanation)
            
            # If interest mentioned but rate is below threshold, still flag as medium
            if not high_rate_found:
                severity = "Medium"
                explanation = (
                    f"Interest rate clause identified. Review the specific rate "
                    f"and terms carefully to understand the total cost of borrowing."
                )
                return (severity, explanation)
        
        # Generate explanation based on risk type
        explanation = RiskAnalyzer._generate_explanation(
            risk_type,
            base_severity,
            clause_original
        )
        
        return (base_severity, explanation)
    
    @staticmethod
    def _generate_explanation(
        risk_type: str,
        severity: str,
        clause_text: str
    ) -> str:
        """Generate plain English explanation for identified risk."""
        
        explanations = {
            "High Interest Rate": (
                "This clause mentions interest rates. High interest rates can "
                "significantly increase the total amount you'll pay over time. "
                "Compare this rate with market standards and consider the impact "
                "on your financial obligations."
            ),
            "Hidden Fees": (
                "This clause mentions additional fees beyond the principal amount. "
                "These fees can add up over time and increase the total cost. "
                "Review all fee structures carefully to understand the complete "
                "financial commitment."
            ),
            "Penalty Clauses": (
                "This clause contains penalty provisions that may be triggered "
                "if you fail to meet certain conditions. Penalties can result in "
                "additional charges, increased interest rates, or other financial "
                "consequences. Understand the conditions that trigger penalties."
            ),
            "Auto-Renewal": (
                "This clause indicates automatic renewal of the agreement. "
                "You may be bound to continue the contract unless you take "
                "specific action to cancel. Be aware of renewal dates and "
                "cancellation procedures."
            ),
            "One-Sided Termination": (
                "This clause allows one party (typically the lender/service provider) "
                "to terminate the agreement with minimal notice or at their discretion. "
                "This creates an imbalance of power and may leave you without "
                "adequate protection or recourse."
            ),
            "Arbitration Clause": (
                "This clause requires disputes to be resolved through arbitration "
                "rather than court. This may limit your ability to pursue legal "
                "action or participate in class action lawsuits. Understand your "
                "rights and options for dispute resolution."
            ),
            "Variable Interest Rate": (
                "This clause indicates that the interest rate can change over time. "
                "Variable rates may increase, potentially raising your payments "
                "significantly. Understand the factors that determine rate changes "
                "and potential maximum rates."
            ),
            "Prepayment Penalty": (
                "This clause imposes penalties for paying off the loan early. "
                "This can discourage early repayment and may result in additional "
                "costs if you want to pay off the debt ahead of schedule."
            )
        }
        
        return explanations.get(
            risk_type,
            f"This clause contains terms that may pose a {severity.lower()} risk. "
            f"Review carefully and consider seeking professional advice."
        )