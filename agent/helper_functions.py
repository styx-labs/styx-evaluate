import re
from langchain_core.messages import HumanMessage, SystemMessage
from agent.azure_openai import llm
from langsmith import traceable
from agent.types import (
    RecommendationOutput,
    TraitEvaluationOutput,
)
from agent.prompts import (
    recommendation_prompt,
    trait_evaluation_prompt,
)


@traceable(name="get_recommendation")
def get_recommendation(
    job_description: str, candidate_full_name: str, completed_sections: str
) -> RecommendationOutput:
    structured_llm = llm.with_structured_output(RecommendationOutput)
    return structured_llm.invoke(
        [
            SystemMessage(
                content=recommendation_prompt.format(
                    job_description=job_description,
                    candidate_full_name=candidate_full_name,
                    completed_sections=completed_sections,
                )
            ),
            HumanMessage(
                content="Write a recommendation on how good of a fit the candidate is for the job based on the provided information."
            ),
        ]
    )


@traceable(name="get_trait_evaluation")
def get_trait_evaluation(
    trait: str,
    trait_description: str,
    candidate_full_name: str,
    candidate_context: str,
    source_str: str,
    trait_type: str = "SCORE",  # Default to SCORE for backward compatibility
    value_type: str = None,
) -> TraitEvaluationOutput:
    """
    Evaluate a candidate on a specific trait.

    Args:
        trait: The name of the trait
        trait_description: Description of the trait and how to evaluate it
        candidate_full_name: The candidate's full name
        candidate_context: Basic context about the candidate
        source_str: String containing all relevant sources about the candidate
        trait_type: Type of trait (BOOLEAN, SCORE)
    """
    structured_llm = llm.with_structured_output(TraitEvaluationOutput)

    # Build the evaluation prompt based on trait type
    type_specific_instructions = ""
    if trait_type == "BOOLEAN":
        type_specific_instructions = (
            "Evaluate if the candidate meets this requirement (true/false)."
        )
    elif trait_type == "SCORE":
        type_specific_instructions = "Rate the candidate from 0-10 on this trait."

    return structured_llm.invoke(
        [
            SystemMessage(
                content=trait_evaluation_prompt.format(
                    section=trait,
                    trait_description=trait_description,
                    candidate_full_name=candidate_full_name,
                    candidate_context=candidate_context,
                    source_str=source_str,
                    trait_type=trait_type,
                    type_specific_instructions=type_specific_instructions,
                    value_type=value_type,
                )
            ),
            HumanMessage(
                content="Evaluate the candidate on this trait based on the provided information."
            ),
        ]
    )
