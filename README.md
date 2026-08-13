# 🛡️ GolKotha AI Security Lab

> An AI Security Lab for demonstrating Machine Learning, Retrieval-Augmented Generation (RAG). AI Security evaluation, and monitoring, with Explainable AI (XAI) and Adversarial Machine Learning (AML) planned as future extensions.

## Overview

<!-- GolKotha AI is an educational AI Security Lab that demonstrates how modern AI systems can be evaluated, attacked, explained, and secured. -->

GolKotha AI began as a machine learning application for predicting football match outcomes and has evolved into an educational AI Security Lab built using Clean Architecture and SOLID principles.

The project demonstrate how a traditional machine application can be extended with AI security capabilities.

The current implementation combines:

- ⚽ XGBoost-based football match prediction
- 🔎 Retrieval-Augmented Generation (RAG)
- 🛡️ AI-generated security assessments
- 📚 Citation-grounded security recommendations
- 👍👎 Human feedback collection
- 📊 RAG evaluation
- 📈 Operational monitoring

<!-- The lab allows users to:

* Train and evaluate machine learning models
* Explain model predictions using SHAP
* Demonstrate adversarial attacks against AI models
* Generate grounded security recommendations using Retrieval-Augmented Generation (RAG) -->

Explainable AI using SHAP and adversarial testing using FGSM are planned extenstions.

---

## Current Workflow

```text
Football Match Data
        │
        ▼
Feature Engineering
        │
        ▼
XGBoost Model
        │
        ▼
Baseline Prediction
        │
        ├─────────────────────────────┐
        │                             │
        ▼                             ▼
Prediction Context             Security Knowledge Base
        │                             │
        │                       Vector Retrieval
        │                             │
        └──────────────┬──────────────┘
                       ▼
               RAG Security Advisor
                       │
                       ▼
              Grounded Recommendation
                       │
              ┌────────┴─────────┐
              ▼                  ▼
           Citations          Feedback
                                 │
                                 ▼
                         Monitoring Database
                                 │
                                 ▼
                         Monitoring Dashboard
```

---

## Architecture

GolKotha AI follows Clean Architecture to seperate domain logic from infrastructure and presentation concerns.

```
                ┌────────────────────────────┐
                │      Presentation Layer    │
                │      Streamlit UI          │
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
                │ ML • RAG • DB • LLM • APIs │
                └────────────────────────────┘
```

This design keeps the core application independent of technologies such as Streamlit, SQLite, ChromaDB, and the LLM provider.

---

# Features

## 1. 📊 Baseline Machine Learning Model

The baseline workflow builds football match features and uses an XGBoost classifier to predict the match outcome.

The interface displays:

- Prediction
- Predicted-team confidence
- Probability for each team
- Probability distribution

### Example

![Baseline Model](docs/images/baseline-model.png)

The current demonstration prdicts a match between Argentina and Spain and displays the probability assigned to each outcome.

<!-- 
* Feature engineering
* Dataset creation
* XGBoost prediction model
* Model evaluation -->

---

## 2. 🔍 Explainable AI (XAI)

**Status: Deferred / Planned**

SHAP explainability is planned to provide:

- Local prediction explanations
- Global feature importance
- SHAP Waterfall plots
- Feature contribution analysis

The UI already reserves an Explainability stage so it can be integrated into the existing workflow.

<!-- * SHAP Feature Importance
* SHAP Waterfall plots
* Global explanations
* Local explanations -->

---

## 3. ⚔️ Adversarial Machine Learning (AML)

**Status: Deferred / Planned**

The adversarial ML stage will deomonstrate how intentionally modified inputs affect model bahavior.

The initial planned implementation uses IBM Adversarial Robustness Toolbox (ART) and FGSM.

Planned capabilities include:

- Configurable FGSM epsilon
- Original vs. attacked prediction
- Probability comparison
- Attack success measurement
- Adversarial robustness analysis

<!-- Planned demonstrations include:

* FGSM
* PGD
* Feature manipulation attacks
* Prediction comparison
* Attack visualization -->

---

## 4. 🛡️ AI Security Advisor

The AI Security Advisor evaluates the available model and prediction context and generates a security assessment.

![AI Security Advisor](docs/images/security-advisor.png)

The assessment includes:

- Executive summary
- Preliminary risk level
- Security findings
- Recommended limitations
- Supporting RAG references

Because SHAP and adversarial testing are currently deferred, the application explicitly identifies the assessment as a **baseline-only security assessment**.

## 5. 📚 Retrieval-Augmented Generation (RAG)

GolKotha AI uses Retrieval-Augmented Generation to ground security recommendations in trusted AI security documentation.

The knowledge base can contain guidance from sources such as:

* MITRE ATLAS
* NIST AI Risk Management Framework
* OWASP Top 10 for LLM Applications
* IBM Adversarial Robustness Toolbox (ART)
* Microsoft AI Security Guidance
* Academic adversarial ML research

The RAG workflow is apporximately: 

```text
Security Assessment Request
        │
        ▼
Security Query Builder
        │
        ▼
Embedding Model
        │
        ▼
Chroma Vector Store
        │
        ▼
Relevant Security Chunks
        │
        ▼
Security Prompt Builder
        │
        ▼
LLM
        │
        ▼
Grounded Recommendation
        │
        ▼
Citation Validation
```

### Grounded References

The applicatoin exposes the references supporting the generated recommendation.

![RAG References](docs/images/rag-references.png)

This makes it possible to trace recommendations back to retrived security guidance instead of relying entirely on unsupported LLM output.

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

## Current Development Status

| Phase                                  | Status         |
| -------------------------------------- | -------------- |
| Phase 1 – Clean Architecture Refactor  | ✅ Complete     |
| Phase 2 – Explainable AI               | ⏭ Deferred     |
| Phase 3 – Adversarial ML               | ⏭ Deferred     |
| Phase 4 – Security Evaluation          | ⏭ Deferred     |
| Phase 5 – RAG Security Recommendations | 🚧 In Progress |

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

# Demo

# Disclaimer

## License

This repository is intended for educational and research purposes.
