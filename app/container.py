
from dataclasses import dataclass
from typing import Any

from application.mapper.prediction_context_mapper import PredictionContextMapper
from application.ports.llm_port import LLMPort
from application.use_cases.generate_security_recommendations import (
    GenerateSecurityRecommendations,
)
from application.use_cases.predict_match import PredictMatch
from application.use_cases.train_model import TrainModel


from infrastructure.ml.xgboost_trainer import XGBoostTrainer
from infrastructure.ml.xgboost_predictor import XGBoostPredictor
from infrastructure.llm.llm_factory import build_llm

from infrastructure.rag.chroma_vector_store import (
    ChromaVectorStore
)

from infrastructure.rag.citation_parser import CitationParser
from infrastructure.rag.security_prompt_builder import (
    SecurityPromptBuilder
)

from infrastructure.rag.security_query_builder import (
    SecurityQueryBuilder
)

from infrastructure.rag.sentence_transformer_embeddings import (
    SentenceTransformerEmbeddingService
)


@dataclass(frozen=True)
class TrainingContainer:
    train_model: TrainModel

@dataclass(frozen=True)
class PredictionContainer:
    predict_match: PredictMatch

@dataclass(frozen=True)
class LLMContainer:
    llm: LLMPort

@dataclass(frozen=True)
class AdvisorContainer:
    generate_security_recommendations: (
        GenerateSecurityRecommendations
    )

def build_training_container() -> TrainingContainer:
    trainer = XGBoostTrainer()

    return TrainingContainer(
        train_model=TrainModel(trainer),
    )

def build_prediction_container(
    model: Any,
) -> PredictionContainer:
    predictor = XGBoostPredictor(model)

    return PredictionContainer(
        predict_match=PredictMatch(
            predictor=predictor
        ),
    )

def build_advisor_container() -> AdvisorContainer:

    embeddings = SentenceTransformerEmbeddingService()

    vector_store = ChromaVectorStore(
        persist_directory="knowledge/vector_store",
        collection_name="golkotha_ai_security",
    )

    llm = build_llm()

    query_builder = SecurityQueryBuilder()

    prompt_builder = SecurityPromptBuilder()

    citation_parser = CitationParser()

    predict_context_mapper = PredictionContextMapper()

    generate_security_recommendations = GenerateSecurityRecommendations(
        embedding_service=embeddings,
        vector_store=vector_store,
        llm=llm,
        prompt_builder=prompt_builder,
        query_builder=query_builder,
        citation_parser=citation_parser,
        predict_context_mapper=predict_context_mapper,
    )

    return AdvisorContainer(
        generate_security_recommendations=generate_security_recommendations,
    )