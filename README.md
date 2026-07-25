# GolKotha AI

> An AI Security Lab for demonstrating Machine Learning, Explainable AI (XAI), Adversarial Machine Learning (AML), and Retrieval-Augmented Generation (RAG).

## Overview

GolKotha AI is an educational AI Security Lab that demonstrates how modern AI systems can be evaluated, attacked, explained, and secured.

The project began as a machine learning application for predicting football match outcomes and has evolved into a modular platform for AI security research using Clean Architecture and SOLID principles.

The lab allows users to:

* Train and evaluate machine learning models
* Explain model predictions using SHAP
* Demonstrate adversarial attacks against AI models
* Generate grounded security recommendations using Retrieval-Augmented Generation (RAG)

---

## Architecture

```
                ┌────────────────────────────┐
                │      Presentation Layer    │
                │      Streamlit UI/API      │
                └──────────────┬─────────────┘
                               │
                ┌──────────────▼─────────────┐
                │      Application Layer     │
                │        Use Cases           │
                └──────────────┬─────────────┘
                               │
                ┌──────────────▼─────────────┐
                │        Domain Layer        │
                │ Entities • Ports • Models  │
                └──────────────┬─────────────┘
                               │
                ┌──────────────▼─────────────┐
                │    Infrastructure Layer    │
                │ ML • APIs • Vector Store   │
                └────────────────────────────┘
```

---

## Project Structure

```
golkotha-ai/
│
├── app/
├── application/
├── clients/
├── data/
├── docs/
├── domain/
├── features/
├── infrastructure/
├── ml/
├── models/
├── presentation/
├── services/
├── tests/
│
├── api.py
├── config.py
├── enums.py
├── main.py
└── pyproject.toml
```

---

## Features

### Machine Learning

* Feature engineering
* Dataset creation
* XGBoost prediction model
* Model evaluation

---

### Explainable AI (XAI)

* SHAP Feature Importance
* SHAP Waterfall plots
* Global explanations
* Local explanations

---

### Adversarial Machine Learning (AML)

Planned demonstrations include:

* FGSM
* PGD
* Feature manipulation attacks
* Prediction comparison
* Attack visualization

---

### Retrieval-Augmented Generation (RAG)

The recommendation engine uses security knowledge from:

* MITRE ATLAS
* NIST AI Risk Management Framework
* OWASP Top 10 for LLM Applications
* IBM Adversarial Robustness Toolbox (ART)
* Microsoft AI Security Guidance
* Academic adversarial ML research

The generated recommendations are grounded using retrieved documentation and citations.

---

## Current Development Status

| Phase                                  | Status         |
| -------------------------------------- | -------------- |
| Phase 1 – Clean Architecture Refactor  | ✅ Complete     |
| Phase 2 – Explainable AI               | ⏭ Deferred     |
| Phase 3 – Adversarial ML               | ⏭ Deferred     |
| Phase 4 – Security Evaluation          | ⏭ Deferred     |
| Phase 5 – RAG Security Recommendations | 🚧 In Progress |

---

## Technology Stack

* Python
* Streamlit
* XGBoost
* Pandas
* NumPy
* Scikit-learn
* SHAP
* ChromaDB (planned)
* Sentence Transformers (planned)
* LangChain (planned)

---

## Installation

```bash
git clone https://github.com/mdhasan2/golkotha-ai.git

cd golkotha-ai

uv sync
```

or

```bash
pip install -e .
```

---

## Running the Application

```bash
python main.py
```

or

```bash
streamlit run app/streamlit_app.py
```

---

## Research Goal

This project demonstrates the complete lifecycle of AI security:

1. Train a machine learning model.
2. Explain how the model makes decisions.
3. Attack the model using adversarial techniques.
4. Measure the impact of the attack.
5. Retrieve trusted security guidance.
6. Generate grounded AI security recommendations.

---

## Roadmap

* Complete RAG implementation
* Build vector database
* Implement document ingestion pipeline
* Add embedding generation
* Implement semantic retrieval
* Add citation-aware recommendation generation
* Expand adversarial attack library
* Add additional explainability techniques
* Improve evaluation dashboards

---

## License

This repository is intended for educational and research purposes.
