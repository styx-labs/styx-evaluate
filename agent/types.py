from typing import List, Annotated, Optional, Union
from typing_extensions import TypedDict
import operator
from pydantic import BaseModel, Field
from enum import Enum


class TraitType(str, Enum):
    BOOLEAN = "BOOLEAN"
    SCORE = "SCORE"

    @classmethod
    def _missing_(cls, value: str):
        # Handle uppercase values by converting to lowercase
        if isinstance(value, str):
            return cls(value.upper())
        return None
    

class KeyTrait(BaseModel):
    trait: str
    description: str
    trait_type: TraitType
    value_type: Optional[str] = None
    required: bool = True

class SearchQuery(BaseModel):
    search_query: str = Field(None, description="Query for web search.")


class RecommendationOutput(BaseModel):
    recommendation: str


class TraitEvaluationOutput(BaseModel):
    value: Union[bool, int]  # Can be boolean, score (0-10)
    evaluation: str
    trait_type: str  # The type of trait being evaluated (BOOLEAN, SCORE)


class EvaluationState(TypedDict):
    source_str: str
    job_description: str
    candidate_context: str
    candidate_full_name: str
    key_traits: List[KeyTrait]
    completed_sections: Annotated[
        list, operator.add
    ]  # This is for parallelizing section writing
    recommendation: str
    summary: str
    overall_score: float
    section: str  # This is for parallelizing section writing
    section_description: str  # This is for parallelizing section writing
    source: str  # This is for parallelizing source validation
    citations: list[dict]


class EvaluationInputState(TypedDict):
    source_str: str
    job_description: str
    candidate_context: str
    candidate_full_name: str
    key_traits: list[KeyTrait]
    citations: list[dict]


class EvaluationOutputState(TypedDict):
    citations: list[dict]
    sections: list[dict]
    summary: str
    overall_score: float
    source_str: str
