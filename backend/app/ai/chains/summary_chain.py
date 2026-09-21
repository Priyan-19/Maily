from langchain_core.runnables import Runnable

from app.ai.llm import get_llm, get_structured_llm
from app.ai.prompts.analysis_prompt import analysis_prompt
from app.ai.prompts.summary_prompt import summary_prompt


def get_summary_chain() -> Runnable:
    llm = get_llm()

    return summary_prompt | llm

def get_analysis_chain() -> Runnable:
    llm = get_structured_llm()

    return analysis_prompt | llm