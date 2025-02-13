from langchain_core.messages import HumanMessage, SystemMessage
from services.llms import llm
from langsmith import traceable
from models.base import (
    TraitEvaluationOutput,
    FitOutput,
)
from models.jobs import Job, KeyTrait
from models.linkedin import LinkedInProfile
from agent.prompts import (
    trait_evaluation_prompt,
    fit_prompt,
)


@traceable(name="get_trait_evaluation")
def get_trait_evaluation(
    trait: KeyTrait,
    candidate_profile: LinkedInProfile,
    source_str: str,
    custom_instructions: str,
    job: Job,
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
                content=trait_evaluation_prompt.format(
                    trait=trait.trait,
                    trait_description=trait.description,
                    candidate_full_name=candidate_profile.full_name,
                    candidate_context=candidate_profile.to_context_string(),
                    source_str=source_str if source_str != "linkedin_only" else "",
                    custom_instructions=custom_instructions,
                    pipeline_feedback=[
                        str(feedback) for feedback in job.pipeline_feedback
                    ],
                    calibrated_profiles=[
                        str(calibrated_profile)
                        for calibrated_profile in job.calibrated_profiles
                    ],
                )
            ),
            HumanMessage(content=""),
        ]
    )


@traceable(name="get_fit")
def get_fit(
    job: Job,
    candidate_profile: LinkedInProfile,
    source_str: str,
    custom_instructions: str,
) -> FitOutput:
    structured_llm = llm.with_structured_output(FitOutput)
    return structured_llm.invoke(
        [
            SystemMessage(
                content=fit_prompt.format(
                    job_description=job.job_description,
                    calibrated_profiles=[
                        str(calibrated_profile)
                        for calibrated_profile in job.calibrated_profiles
                    ],
                    pipeline_feedback=[
                        str(feedback) for feedback in job.pipeline_feedback
                    ],
                    candidate_full_name=candidate_profile.full_name,
                    candidate_context=candidate_profile.to_context_string(),
                    source_str=source_str,
                    custom_instructions=custom_instructions,
                )
            ),
            HumanMessage(content=""),
        ]
    )
