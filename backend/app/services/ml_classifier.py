import joblib
from pathlib import Path
from typing import Tuple

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "risk_classifier.pkl"

class MLClauseClassifier:
    def __init__(self):
        self.model: Optional[object] = None
        self._load_model()
    
    def _load_model(self):
        try:
            self.model = joblib.load(MODEL_PATH)
            print(f"ML model loaded from: {MODEL_PATH}")
        except Exception as e:
            print(f"Failed to load ML model: {e}")
            self.model = None

    def predict(self, text: str) -> Tuple[str, float]:
        if self.model is None:
            return "LOW_RISK", 0.0

        probs = self.model.predict_proba([text])[0]
        label = self.model.predict([text])[0]
        confidence = float(max(probs))
        return label, confidence

ml_classifier = MLClauseClassifier()