from typing import Annotated, Optional
import operator
from .linkedin import LinkedInProfile
from .jobs import Job, KeyTrait
from .serializable import SerializableModel


class EvaluationState(SerializableModel):
    # Input
    source_str: str
    candidate_profile: LinkedInProfile
    job: Job
    citations: list[dict]
    custom_instructions: Optional[str] = None

    # Intermediate
    completed_traits: Annotated[list[dict], operator.add] = []
    trait: Optional[KeyTrait] = None

    # Output
    citations: Optional[list[dict]] = None
    traits: Optional[list[dict]] = None
    summary: Optional[str] = None
    required_met: Optional[int] = None
    optional_met: Optional[int] = None
    fit: Optional[int] = None


class EvaluationInputState(SerializableModel):
    source_str: str
    candidate_profile: LinkedInProfile
    job: Job
    citations: list[dict]
    custom_instructions: Optional[str] = None


class EvaluationOutputState(SerializableModel):
    citations: list[dict]
    traits: list[dict]
    summary: str
    required_met: int
    optional_met: int
    source_str: str
    fit: int
