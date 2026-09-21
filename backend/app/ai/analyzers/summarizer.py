from app.ai.chains.summary_chain import get_analysis_chain, get_summary_chain
from app.schemas.analysis import EmailAnalysis


def summarize_email(
    subject: str,
    sender: str,
    body: str,
    target_language: str = "English",
) -> str:

    if not body.strip():
        return "No readable email content was found."

    chain = get_summary_chain()

    result = chain.invoke(
        {
            "subject": subject,
            "sender": sender,
            "body": body,
            "target_language": target_language,
        }
    )

    return result.content


def analyze_email(
    subject: str,
    sender: str,
    body: str,
) -> EmailAnalysis:

    if not body.strip():
        return EmailAnalysis(
            summary="No readable email content was found.",
            language="Unknown",
            importance="low",
            actions=[],
            deadlines=[],
        )

    chain = get_analysis_chain()

    result = chain.invoke(
        {
            "subject": subject,
            "sender": sender,
            "body": body,
        }
    )

    return result