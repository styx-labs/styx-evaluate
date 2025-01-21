from typing import List, Annotated, Optional, Union
from typing_extensions import TypedDict
import operator
from pydantic import BaseModel, Field
from enum import Enum
from datetime import date


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


class AILinkedinJobDescription(BaseModel):
    role_summary: str
    skills: List[str]
    requirements: List[str]
    sources: List[str]


class LinkedInExperience(BaseModel):
    title: str
    company: str
    description: Optional[str] = None
    starts_at: Optional[date] = None
    ends_at: Optional[date] = None
    location: Optional[str] = None
    summarized_job_description: Optional[AILinkedinJobDescription] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title=data["title"],
            company=data["company"],
            description=data["description"],
            starts_at=data["starts_at"],
            ends_at=data["ends_at"],
            location=data["location"],
            summarized_job_description=AILinkedinJobDescription.from_dict(
                data["summarized_job_description"]
            )
            if data["summarized_job_description"]
            else None,
        )


class LinkedInEducation(BaseModel):
    school: str
    degree_name: Optional[str] = None
    field_of_study: Optional[str] = None
    starts_at: Optional[date] = None
    ends_at: Optional[date] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            school=data["school"],
            degree_name=data["degree_name"],
            field_of_study=data["field_of_study"],
            starts_at=data["starts_at"],
            ends_at=data["ends_at"],
        )


class LinkedInProfile(BaseModel):
    full_name: str
    occupation: Optional[str] = None
    headline: Optional[str] = None
    summary: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    public_identifier: str
    experiences: List[LinkedInExperience] = []
    education: List[LinkedInEducation] = []

    def to_context_string(self) -> str:
        """Convert the profile to a formatted string context."""
        context = ""
        if self.occupation:
            context += f"Current Occupation: {self.occupation}\n"
        if self.headline:
            context += f"Headline: {self.headline}\n"
        if self.summary:
            context += f"Summary: {self.summary}\n"
        if self.city:
            context += f"City: {self.city}\n"

        for exp in self.experiences:
            context += f"Experience: {exp.title} at {exp.company}"
            if exp.description:
                context += f" - {exp.description}"
            context += "\n"

            if exp.summarized_job_description:
                context += f"Likely Job Description: {exp.summarized_job_description.role_summary}\n"
                context += (
                    f"Skills: {', '.join(exp.summarized_job_description.skills)}\n"
                )
                context += f"Requirements: {', '.join(exp.summarized_job_description.requirements)}\n"

        for edu in self.education:
            context += (
                f"Education: {edu.school}; {edu.degree_name} in {edu.field_of_study}\n"
            )
        return context

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            full_name=data["full_name"],
            occupation=data["occupation"],
            headline=data["headline"],
            summary=data["summary"],
            city=data["city"],
            country=data["country"],
            public_identifier=data["public_identifier"],
            experiences=data["experiences"],
            education=data["education"],
        )


class EvaluationState(TypedDict):
    source_str: str
    job_description: str
    candidate_context: str
    candidate_profile: LinkedInProfile
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
    candidate_profile: LinkedInProfile
    candidate_full_name: str
    key_traits: list[KeyTrait]
    citations: list[dict]


class EvaluationOutputState(TypedDict):
    citations: list[dict]
    sections: list[dict]
    summary: str
    overall_score: float
    source_str: str
    candidate_profile: LinkedInProfile
