from app.services.ml_classifier import ml_classifier

text = "The bank may charge a penalty of 5% for late payment."

label, confidence = ml_classifier.predict(text)

print("Label:", label)
print("Confidence:", confidence)