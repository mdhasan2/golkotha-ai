# Phase 1 — Refactor Foundation

## Objective

Introduce clean architectural boundaries while preserving the current
GolKotha AI prediction behavior.

No new machine-learning, adversarial, explainability, or RAG behavior is
introduced during this phase.

## Current Workflow

Raw fixture data
→ DatasetBuilder
→ pandas dataset
→ XGBoost Trainer
→ Predictor
→ Streamlit UI

## Target Workflow

Raw fixture data
→ Infrastructure DatasetBuilder
→ Application TrainModel use case
→ Infrastructure XGBoostTrainer
→ Trained model
→ Infrastructure XGBoostPredictor
→ Application PredictMatch use case
→ Domain MatchPrediction
→ Streamlit presentation

## Layer Responsibilities

### Domain

Contains application concepts that are independent of frameworks.

Examples:

- Team
- Match
- MatchFeatures
- MatchPrediction
- PredictionProbability
- MatchOutcome

The domain layer must not depend on XGBoost, pandas, Streamlit, APIs, or
filesystem access.

### Application

Contains use cases and interface definitions.

Examples:

- TrainModel
- PredictMatch
- ModelTrainerPort
- MatchPredictorPort
- DatasetBuilderPort

The application layer coordinates behavior but does not implement external
technology.

### Infrastructure

Implements interfaces using external libraries and services.

Examples:

- XGBoostTrainer
- XGBoostPredictor
- JoblibModelRepository
- API-Football clients
- CSV or Parquet repositories

### Presentation

Collects user input and displays results.

Examples:

- StreamlitService
- Streamlit pages
- UI formatting

The presentation layer must not train models or call predict_proba directly.

## Dependency Direction

presentation → application → domain

infrastructure → application and domain

domain → no project layer

## Behavior-Preservation Requirements

The refactor is complete only when:

1. The same dataset rows are produced.
2. The same feature columns are used.
3. Feature column order is preserved.
4. The same target labels are used.
5. The same XGBoost parameters are used.
6. The same model probabilities are produced within floating-point tolerance.
7. The same winner is displayed.
8. The Streamlit progress value is a native Python float.
9. No adversarial or explainability behavior has been added yet.

## Future Extension Points

Phase 2 can add:

- AttackPort
- FeatureAttack
- PredictionComparison
- RobustnessMetrics
- ExplanationPort
- RecommendationPort
- RAG security advisor

These components should integrate through application interfaces rather than
being called directly from Streamlit.

## Final reference architecture

┌─────────────────────────────────────────────┐
│              Presentation                   │
│                                             │
│  StreamlitService                           │
│  - collects features                        │
│  - calls PredictMatch                       │
│  - displays probabilities                   │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│              Application                    │
│                                             │
│  TrainModel                                 │
│  PredictMatch                               │
│                                             │
│  ModelTrainerPort                           │
│  MatchPredictorPort                         │
│  DatasetBuilderPort                         │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│                 Domain                      │
│                                             │
│  MatchFeatures                              │
│  MatchPrediction                            │
│  PredictionProbability                      │
│  MatchOutcome                               │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│              Infrastructure                 │
│                                             │
│  XGBoostTrainer                             │
│  XGBoostPredictor                           │
│  DatasetBuilder                             │
│  JoblibModelRepository                      │
│  API-Football services                      │
└────────────── implements ports ─────────────┘

## Phase 1 completion checklist

[ ] Domain dataclasses added
[ ] Application interfaces added
[ ] TrainModel use case added
[ ] PredictMatch use case added
[ ] Existing XGBoost trainer wrapped
[ ] Existing predictor wrapped
[ ] Streamlit no longer calls predict_proba directly
[ ] NumPy float values converted to Python float
[ ] Feature order preserved
[ ] Existing numeric labels preserved
[ ] Old imports continue working through adapters
[ ] Unit tests pass
[ ] Old and new probability outputs match
[ ] No attack logic added
[ ] No SHAP logic added
[ ] No RAG logic added