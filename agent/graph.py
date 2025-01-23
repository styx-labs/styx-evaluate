from langgraph.constants import Send
from langgraph.graph import START, END, StateGraph
from agent.helper_functions import (
    get_recommendation,
    get_trait_evaluation,
    get_fit,
)
from agent.types import (
    EvaluationState,
    EvaluationInputState,
    EvaluationOutputState,
)
from agent.types import LinkedInProfile


def evaluate_trait(state: EvaluationState):
    trait = state["trait"]  # This should be the full KeyTrait object
    source_str = state["source_str"]
    candidate_full_name = state["candidate_full_name"]
    candidate_profile = LinkedInProfile.from_dict(state["candidate_profile"])
    num_traits = len(state["key_traits"])

    content = get_trait_evaluation(
        trait.trait,  # Access as object attribute
        trait.description,  # Access as object attribute
        candidate_full_name,
        candidate_profile.to_context_string(),
        source_str,
        trait_type=trait.trait_type,
    )

    if trait.trait_type == "TraitType.SCORE":
        # Ensure numeric value for score type
        value = (
            float(content.value)
            if isinstance(content.value, str)
            else content.value
        )
        normalized_score = value
    else:
        # Handle both string and boolean representations
        value = (
            float(content.value)
            if isinstance(content.value, str)
            else content.value
        )
        # 1 is yes, -1 is no, 0 is maybe
        if value == 1:
            normalized_score = 10
        elif value == -1:
            normalized_score = 0
        else:
            normalized_score = 10 / (num_traits + 1)  # Some weird math so that yeses are always weighted more than maybes

    return {
        "completed_sections": [
            {
                "section": trait.trait,
                "content": content.evaluation,
                "value": content.value,
                "trait_type": trait.trait_type,
                "normalized_score": normalized_score,
                "required": trait.required,
            }
        ]
    }


def write_recommendation(state: EvaluationState):
    candidate_full_name = state["candidate_full_name"]
    completed_sections = state["completed_sections"]
    job_description = state["job_description"]
    completed_sections_str = "\n\n".join([s["content"] for s in completed_sections])
    source_str = state["source_str"]
    ideal_profiles = state["ideal_profiles"]
    candidate_profile = LinkedInProfile.from_dict(state["candidate_profile"])

    summary = get_recommendation(
        job_description, candidate_full_name, completed_sections_str
    ).recommendation

    fit = get_fit(
        job_description,
        ideal_profiles,
        candidate_full_name,
        candidate_profile.to_context_string(),
        source_str,
    )

    overall_score = sum([s["normalized_score"] for s in completed_sections])
    overall_score += fit.fit_score

    return {"summary": summary, "overall_score": overall_score, "fit": fit}


def compile_evaluation(state: EvaluationState):
    key_traits = state["key_traits"]
    completed_sections = state["completed_sections"]
    citations = state["citations"]
    ordered_sections = []

    for trait in key_traits:
        for section in completed_sections:
            if section["section"] == trait.trait:
                ordered_section = {
                    "section": section["section"],
                    "content": section["content"],
                    "trait_type": section["trait_type"],
                    "value": section["value"],
                    "normalized_score": section["normalized_score"],
                    "required": section["required"],
                }
                ordered_sections.append(ordered_section)

    return {"sections": ordered_sections, "citations": citations}


def initiate_evaluation(state: EvaluationState):
    return [
        Send(
            "evaluate_trait",
            {"trait": t, **state},  # Pass the entire KeyTrait object
        )
        for t in state["key_traits"]
    ]


def dummy_start(state: EvaluationState):
    return {}


builder = StateGraph(
    EvaluationState, input=EvaluationInputState, output=EvaluationOutputState
)

builder.add_node("dummy_start", dummy_start)
builder.add_node("evaluate_trait", evaluate_trait)
builder.add_node("write_recommendation", write_recommendation)
builder.add_node("compile_evaluation", compile_evaluation)

builder.add_edge(START, "dummy_start")
builder.add_conditional_edges("dummy_start", initiate_evaluation, ["evaluate_trait"])
builder.add_edge("evaluate_trait", "write_recommendation")
builder.add_edge("write_recommendation", "compile_evaluation")
builder.add_edge("compile_evaluation", END)

graph = builder.compile()
