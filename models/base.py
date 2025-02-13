from typing import Union
from pydantic import BaseModel


class RecommendationOutput(BaseModel):
    recommendation: str


class TraitEvaluationOutput(BaseModel):
    value: Union[bool]
    evaluation: str


class FitOutput(BaseModel):
    fit_score: int  # score 0-4
    reasoning: str
