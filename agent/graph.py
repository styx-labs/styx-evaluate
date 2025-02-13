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


def evaluate_trait(state: EvaluationState):
    content = get_trait_evaluation(
        state.trait,
        state.candidate_profile,
        state.source_str,
        state.custom_instructions,
        state.job,
    )

    return {
        "completed_traits": [
            {
                "trait": state.trait.trait,
                "content": content.evaluation,
                "value": content.value,
                "required": state.trait.required,
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
    completed_traits_dict = {trait["trait"]: trait for trait in state.completed_traits}

    # Map traits in order while tracking counts
    ordered_traits = []
    required_met = 0
    optional_met = 0

    for trait in state.job.key_traits:
        if completed_trait := completed_traits_dict.get(trait.trait):
            ordered_traits.append(
                {
                    "section": completed_trait["trait"],
                    "content": completed_trait["content"],
                    "value": completed_trait["value"],
                    "required": completed_trait["required"],
                }
            )

            if completed_trait["value"]:
                if completed_trait["required"]:
                    required_met += 1
                else:
                    optional_met += 1

    return {
        "traits": ordered_traits,
        "required_met": required_met,
        "optional_met": optional_met,
    }


def initiate_evaluation(state: EvaluationState):
    return [
        Send("evaluate_trait", state.model_copy(update={"trait": trait}))
        for trait in state.job.key_traits
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
