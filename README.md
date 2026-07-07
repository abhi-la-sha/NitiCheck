# 🛡️ NitiCheck  
**AI-Powered Document Risk Analyzer for Financial, Legal & Medical Policies**

NitiCheck is an intelligent document analysis platform that helps users **understand hidden risks, unfair clauses, and complex terms** in documents by converting dense policy language into **clear, actionable insights**.

Built with a modern full-stack architecture, NitiCheck currently focuses on **financial documents** and is designed to scale seamlessly to **legal and medical documents** in future iterations.

---

## 🚀 Why NitiCheck?

Most people blindly accept:
- Loan agreements  
- Insurance policies  
- Terms & Conditions  
- Subscription contracts  

…because they’re **long, complex, and intimidating**.

NitiCheck solves this by:
- Detecting **risky or unfavorable clauses**
- Explaining them in **plain language**
- Assigning **risk levels** for quick understanding
- Giving users clarity **before they sign**

---

## ✨ Key Features

- 📄 Upload PDF or DOCX documents
- 🔍 Automatic clause extraction
- ⚠️ Risk detection using rule-based analysis
- 📊 Visual risk summary and severity indicators
- 🧠 Plain-language explanations of complex terms
- 🔐 Privacy-first (no cloud storage of documents)
- 🌐 Ready for legal & medical domain expansion

---

## 🧠 Risk Types Detected (Current)

- High Interest Rate clauses  
- Hidden Fees & Charges  
- Penalty Clauses  
- Auto-Renewal Conditions  
- One-Sided Termination Rights  
- Arbitration Clauses  
- Variable Interest Rates  
- Prepayment Penalties  

---

## 🧱 System Architecture

→ Frontend (React + Vite)  
→ REST API  
→ Backend (FastAPI)

---

## 🖥️ Frontend Architecture

**Tech Stack**
- React + TypeScript
- Vite
- Tailwind CSS

---

## ⚙️ Backend Architecture

**Tech Stack**
- FastAPI
- Pydantic
- PyPDF2
- python-docx

---

## 🔁 API Overview

**POST /api/analyze**

Processes uploaded documents and returns structured risk analysis.

---

## 🔐 Privacy & Security

- No document storage
- In-memory processing only
- No third-party uploads

---

## 🛣️ Future Roadmap

- Legal & medical document analysis
- LLM-assisted reasoning
- Multi-language support

---

## 👩‍💻 Author

**Abhilasha Kamal**

---

## License
This project is licensed under the MIT License.

