from typing import List, Annotated, Optional
from typing_extensions import TypedDict
import operator
from .base import KeyTrait
from .linkedin import LinkedInProfile


class EvaluationState(TypedDict):
    source_str: str
    job_description: str
    ideal_profiles: list[str]
    candidate_context: str
    candidate_profile: LinkedInProfile
    candidate_full_name: str
    key_traits: List[KeyTrait]
    completed_sections: Annotated[list, operator.add]
    recommendation: str
    summary: str
    overall_score: float
    section: str
    section_description: str
    source: str
    citations: list[dict]
    fit: int
    custom_instructions: Optional[str] = None
    career_analysis: Optional[dict] = None


class EvaluationInputState(TypedDict):
    source_str: str
    job_description: str
    ideal_profiles: list[str]
    candidate_context: str
    candidate_profile: LinkedInProfile
    candidate_full_name: str
    key_traits: list[KeyTrait]
    citations: list[dict]
    custom_instructions: Optional[str] = None
    career_analysis: Optional[dict] = None


class EvaluationOutputState(TypedDict):
    citations: list[dict]
    sections: list[dict]
    summary: str
    required_met: int
    optional_met: int
    source_str: str
    candidate_profile: LinkedInProfile
    fit: int
