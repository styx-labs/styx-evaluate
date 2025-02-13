from langgraph.constants import Send
from langgraph.graph import START, END, StateGraph
from agent.helper_functions import (
    get_trait_evaluation,
    get_fit,
)
from models.evaluation import (
    EvaluationState,
    EvaluationInputState,
    EvaluationOutputState,
)


def evaluate_section(state: EvaluationState):
    content = get_trait_evaluation(
        state.section,
        state.candidate_profile,
        state.source_str,
        state.custom_instructions,
        state.job,
    )

    return {
        "completed_sections": [
            {
                "section": state.section.trait,
                "content": content.evaluation,
                "value": content.value,
                "required": state.section.required,
            }
        ]
    }


def write_recommendation(state: EvaluationState):
    fit = get_fit(
        state.job,
        state.candidate_profile,
        state.source_str,
        state.custom_instructions,
    )

    return {
        "summary": fit.reasoning,
        "fit": fit.fit_score,
    }


def compile_evaluation(state: EvaluationState):
    # Create lookup dict for completed traits
    completed_sections_dict = {
        section["section"]: section for section in state.completed_sections
    }

    # Map sections in order while tracking counts
    ordered_sections = []
    required_met = 0
    optional_met = 0

    for trait in state.job.key_traits:
        if completed_section := completed_sections_dict.get(trait.trait):
            ordered_sections.append(
                {
                    "section": completed_section["section"],
                    "content": completed_section["content"],
                    "value": completed_section["value"],
                    "required": completed_section["required"],
                }
            )

            if completed_section["value"]:
                if completed_section["required"]:
                    required_met += 1
                else:
                    optional_met += 1

    return {
        "sections": ordered_sections,
        "required_met": required_met,
        "optional_met": optional_met,
    }


def initiate_evaluation(state: EvaluationState):
    return [
        Send("evaluate_section", state.model_copy(update={"section": section}))
        for section in state.job.key_traits
    ]


def dummy_start(state: EvaluationState):
    return {}


builder = StateGraph(
    EvaluationState, input=EvaluationInputState, output=EvaluationOutputState
)

builder.add_node("dummy_start", dummy_start)
builder.add_node("evaluate_section", evaluate_section)
builder.add_node("write_recommendation", write_recommendation)
builder.add_node("compile_evaluation", compile_evaluation)

builder.add_edge(START, "dummy_start")
builder.add_conditional_edges("dummy_start", initiate_evaluation, ["evaluate_section"])
builder.add_edge("evaluate_section", "write_recommendation")
builder.add_edge("write_recommendation", "compile_evaluation")
builder.add_edge("compile_evaluation", END)

graph = builder.compile()
