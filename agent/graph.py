from langgraph.constants import Send
from langgraph.graph import START, END, StateGraph
from agent.helper_functions import (
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

    content = get_trait_evaluation(
        trait.trait,  # Access as object attribute
        trait.description,  # Access as object attribute
        candidate_full_name,
        candidate_profile.to_context_string(),
        source_str,
    )

    return {
        "completed_sections": [
            {
                "section": trait.trait,
                "content": content.evaluation,
                "value": content.value,
                "required": trait.required,
            }
        ]
    }


def write_recommendation(state: EvaluationState):
    candidate_full_name = state["candidate_full_name"]
    job_description = state["job_description"]
    source_str = state["source_str"]
    ideal_profiles = state["ideal_profiles"]
    candidate_profile = LinkedInProfile.from_dict(state["candidate_profile"])

    fit = get_fit(
        job_description,
        ideal_profiles,
        candidate_full_name,
        candidate_profile.to_context_string(),
        source_str,
    )

    return {
        "summary": fit.reasoning,
        "fit": fit.fit_score,
    }


def compile_evaluation(state: EvaluationState):
    key_traits = state["key_traits"]
    completed_sections = state["completed_sections"]
    citations = state["citations"]
    ordered_sections = []

    required_met = 0
    optional_met = 0

    for trait in key_traits:
        for section in completed_sections:
            if section["section"] == trait.trait:
                ordered_section = {
                    "section": section["section"],
                    "content": section["content"],
                    "value": section["value"],
                    "required": section["required"],
                }
                ordered_sections.append(ordered_section)
                if section["required"] and section["value"]:
                    required_met += 1
                elif not section["required"] and section["value"]:
                    optional_met += 1

    return {
        "sections": ordered_sections,
        "citations": citations,
        "required_met": required_met,
        "optional_met": optional_met,
    }


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
