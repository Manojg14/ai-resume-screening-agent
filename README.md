# 🤖 AI Resume Screening Agent

An NLP-based Resume Screening Agent built with **Python, Flask, and Scikit-learn** that analyzes resumes against a Job Description (JD), calculates candidate scores, ranks multiple candidates, and generates screening reports.

This project was developed as part of the **ROOMAN AI Challenge — Junior AI Research Associate Selection Round**.

---

## 🎯 Project Objective

Recruiters often need to manually review many resumes for a single job opening.

This project automates the initial resume screening process.

The recruiter provides:

- A Job Description
- One or more resumes

The system then:

1. Extracts text from resumes.
2. Preprocesses the text.
3. Calculates NLP similarity between the JD and resume.
4. Extracts and matches required skills.
5. Compares required and candidate experience.
6. Checks education requirements.
7. Calculates a final score.
8. Generates a recommendation.
9. Ranks multiple candidates.
10. Generates downloadable reports.

---

## 🏆 ROOMAN AI CHALLENGE

### Selected Agent

**Resume Screening Agent — Intermediate**

### Challenge Requirements

The selected agent should:

- Parse resumes in PDF/DOCX/Text formats.
- Extract skills, experience, and education.
- Compare resumes against a Job Description using NLP similarity.
- Rank candidates.
- Provide scored output with reasoning.
- Handle 10+ resumes.
- Generate structured output.

This project implements these capabilities using an NLP-based hybrid scoring approach.

---

# 🚀 Features

### 📄 Resume Parsing

Supports:

- PDF
- DOCX
- TXT

### 🧠 NLP Similarity

Uses:

- TF-IDF Vectorization
- Cosine Similarity

to calculate the relevance between the Job Description and resume.

### 🛠️ Skill Matching

Identifies:

- Matched skills
- Missing skills
- Skill match percentage

### 💼 Experience Matching

Extracts required experience from the Job Description and compares it with candidate experience.

### 🎓 Education Matching

Checks candidate education against the requirements specified in the Job Description.

### 📊 Candidate Ranking

Multiple resumes can be analyzed and ranked based on their final scores.

### 📑 Reports

Generates:

- CSV report
- Excel report
- PDF report

### 🌐 Flask Web Application

Provides a simple web interface for:

- JD input
- Single resume analysis
- Multiple resume analysis
- Candidate ranking
- Report downloads

---

# 🧠 System Workflow

```text
                  Job Description
                         │
                         ▼
                ┌─────────────────┐
                │  JD Processing  │
                └────────┬────────┘
                         │
                         │
       ┌─────────────────┴──────────────────┐
       │                                    │
       ▼                                    ▼
 Resume Upload                         Multiple Resumes
       │                                    │
       ▼                                    ▼
 PDF / DOCX / TXT                    Batch Processing
       │                                    │
       └────────────────┬───────────────────┘
                        ▼
                 Resume Parser
                        │
                        ▼
                Text Preprocessing
                        │
            ┌───────────┼───────────┐
            ▼           ▼           ▼
       NLP Similarity  Skills    Experience
            │           │           │
            └───────────┼───────────┘
                        ▼
                Education Matching
                        │
                        ▼
                  Final Score
                        │
                        ▼
                Recommendation
                        │
                        ▼
                Candidate Ranking
                        │
             ┌──────────┼──────────┐
             ▼          ▼          ▼
          Dashboard    CSV     Excel / PDF
