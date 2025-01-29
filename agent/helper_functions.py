from langchain_core.messages import HumanMessage, SystemMessage
from agent.azure_openai import llm
from langsmith import traceable
from agent.types import (
    RecommendationOutput,
    TraitEvaluationOutput,
    FitOutput,
)
from agent.prompts import (
    recommendation_prompt,
    boolean_trait_evaluation_prompt,
    fit_prompt,
)


@traceable(name="get_recommendation")
def get_recommendation(
    job_description: str,
    candidate_full_name: str,
    completed_sections: str,
    custom_instructions: str,
) -> RecommendationOutput:
    structured_llm = llm.with_structured_output(RecommendationOutput)
    return structured_llm.invoke(
        [
            SystemMessage(
                content=recommendation_prompt.format(
                    job_description=job_description,
                    candidate_full_name=candidate_full_name,
                    completed_sections=completed_sections,
                    custom_instructions=custom_instructions
                    if custom_instructions
                    else "",
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
    custom_instructions: str,
) -> TraitEvaluationOutput:
    """
    Evaluate a candidate on a specific trait.

    Args:
        trait: The name of the trait
        trait_description: Description of the trait and how to evaluate it
        candidate_full_name: The candidate's full name
        candidate_context: Basic context about the candidate
        source_str: String containing all relevant sources about the candidate
        custom_instructions: Custom instructions for the evaluation
    """
    structured_llm = llm.with_structured_output(TraitEvaluationOutput)

    return structured_llm.invoke(
        [
            SystemMessage(
                content=boolean_trait_evaluation_prompt.format(
                    section=trait,
                    trait_description=trait_description,
                    candidate_full_name=candidate_full_name,
                    candidate_context=candidate_context,
                    source_str=source_str,
                    custom_instructions=custom_instructions
                    if custom_instructions
                    else "",
                )
            ),
            HumanMessage(
                content="Evaluate the candidate on this trait based on the provided information."
            ),
        ]
    )


@traceable(name="get_fit")
def get_fit(
    job_description: str,
    ideal_profiles: list[str],
    candidate_full_name: str,
    candidate_context: str,
    source_str: str,
    custom_instructions: str,
) -> FitOutput:
    structured_llm = llm.with_structured_output(FitOutput)
    ideal_profiles_str = ""
    for i, profile in enumerate(ideal_profiles):
        ideal_profiles_str += f"Ideal profile {i+1}:\n {profile}\n"
        ideal_profiles_str += f"==============================================\n"
    return structured_llm.invoke(
        [
            SystemMessage(
                content=fit_prompt.format(
                    job_description=job_description,
                    ideal_profiles=ideal_profiles_str,
                    candidate_full_name=candidate_full_name,
                    candidate_context=candidate_context,
                    source_str=source_str,
                    custom_instructions=custom_instructions
                    if custom_instructions
                    else "",
                )
            ),
            HumanMessage(content=""),
        ]
    )
