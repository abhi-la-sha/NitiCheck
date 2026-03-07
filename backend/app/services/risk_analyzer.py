import re
import uuid
from typing import List, Dict, Tuple, Optional
from app.models.schemas import Clause
from app.utils.text_cleaner import extract_numbers
from app.services.ml_classifier import ml_classifier


class RiskAnalyzer:
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
        r"\bzero\s+interest\b",
    ]

    RISK_PATTERNS: Dict[str, Dict] = {
        "high_interest": {
            "keywords": [
                r"interest\s+rate",
                r"apr\s*(?:of|is|at)?",
                r"annual\s+percentage\s+rate",
                r"interest\s+charged",
                r"rate\s+of\s+interest",
            ],
            "threshold": 18.0,
            "risk_type": "High Interest Rate",
            "base_severity": "High",
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
                r"origination\s+fee",
            ],
            "risk_type": "Hidden Fees",
            "base_severity": "Medium",
        },
        "penalty_clauses": {
            "keywords": [
                r"penalty",
                r"penal\s+interest",
                r"default\s+rate",
                r"penalty\s+charge",
                r"penalty\s+fee",
                r"breach\s+penalty",
                r"violation\s+penalty",
            ],
            "risk_type": "Penalty Clauses",
            "base_severity": "High",
        },
        "auto_renewal": {
            "keywords": [
                r"auto[-\s]?renew",
                r"automatic\s+renewal",
                r"auto[-\s]?extend",
                r"automatic\s+extension",
                r"renew\s+automatically",
                r"continuous\s+renewal",
            ],
            "risk_type": "Auto-Renewal",
            "base_severity": "Medium",
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
                r"reserve\s+the\s+right\s+to\s+terminate",
            ],
            "risk_type": "One-Sided Termination",
            "base_severity": "High",
        },
        "arbitration_clause": {
            "keywords": [
                r"binding\s+arbitration",
                r"mandatory\s+arbitration",
                r"waive\s+right\s+to\s+sue",
                r"class\s+action\s+waiver",
                r"dispute\s+resolution\s+by\s+arbitration",
            ],
            "risk_type": "Arbitration Clause",
            "base_severity": "Low",
        },
        "variable_rate": {
            "keywords": [
                r"variable\s+rate",
                r"adjustable\s+rate",
                r"rate\s+may\s+change",
                r"rate\s+subject\s+to\s+change",
                r"floating\s+rate",
            ],
            "risk_type": "Variable Interest Rate",
            "base_severity": "Medium",
        },
        "prepayment_penalty": {
            "keywords": [
                r"prepayment\s+penalty",
                r"early\s+payment\s+penalty",
                r"prepayment\s+charge",
                r"early\s+termination\s+fee",
            ],
            "risk_type": "Prepayment Penalty",
            "base_severity": "Medium",
        },
    }

    @staticmethod
    def analyze_document(text: str) -> List[Clause]:
        if not text or len(text.strip()) < 50:
            return []

        from app.utils.text_cleaner import split_into_clauses

        clauses = split_into_clauses(text, min_length=30)
        identified_risks: List[Clause] = []
        seen_clauses: set = set()

        for clause_text in clauses:
            clause_lower = clause_text.lower()
            clause_id = str(uuid.uuid4())

            # ✅ ML prediction (SAFE location)
            try:
                ml_label, ml_confidence = ml_classifier.predict(clause_text)
            except Exception:
                ml_label, ml_confidence = "LOW_RISK", 0.0

            # ML high-risk signal
            ml_high_confidence = (
                ml_label.upper() in ["HIGH", "HIGH_RISK"]
                and ml_confidence > 0.80
            )

            for pattern_key, pattern_config in RiskAnalyzer.RISK_PATTERNS.items():
                matches = RiskAnalyzer._check_pattern(
                    clause_lower,
                    clause_text,
                    pattern_config,
                )

                if matches:
                    severity, explanation = matches

                    # ✅ Hybrid boost
                    if ml_high_confidence and severity != "High":
                        severity = "High"
                        explanation += (
                            " ML analysis also indicates elevated risk."
                        )

                    clause_hash = hash(
                        clause_text[:100] + pattern_config["risk_type"]
                    )
                    if clause_hash in seen_clauses:
                        continue
                    seen_clauses.add(clause_hash)

                    identified_risks.append(
                        Clause(
                            clause_id=clause_id,
                            text=clause_text[:500],
                            risk_type=pattern_config["risk_type"],
                            severity=severity,
                            explanation=explanation,
                        )
                    )
                    break
            
            if ml_high_confidence:
                clause_hash = hash(clause_text[:100] + "ml_high_risk")
                if clause_hash not in seen_clauses:
                    seen_clauses.add(clause_hash)
                    
                    identified_risks.append(
                        Clause(
                            clause_id=clause_id,
                            text=clause_text[:500],
                            risk_type="ML Detected Risk",
                            severity="High",
                            explanation="ML model flagged this clause as high risk.",
                        )
                    )

        return identified_risks
    
    @staticmethod
    def _check_pattern(
    clause_lower: str,
    clause_text: str,
    pattern_config: Dict,
) -> Optional[Tuple[str, str]]:
        keyword_found = any(
        re.search(keyword, clause_lower)
        for keyword in pattern_config["keywords"]
        )

        if not keyword_found:
            return None

        severity = pattern_config.get("base_severity", "Medium")
        explanation = f"This clause indicates {pattern_config['risk_type']}."

        if "threshold" in pattern_config:
            numbers = extract_numbers(clause_text)
            for num in numbers:
                if num > pattern_config["threshold"]:
                    severity = "High"
                    explanation = (
                        f"Interest rate {num}% exceeds safe threshold "
                        f"of {pattern_config['threshold']}%."
                    )
                    break
        
        return severity, explanation

