from app.ai.chains.email_analysis import (
    get_action_chain,
    get_classification_chain,
    get_deadline_chain,
    get_email_analysis_chain,
    get_reply_chain,
)

from app.schemas.analysis import (
    ActionExtraction,
    DeadlineExtraction,
    EmailAnalysis,
    EmailClassification,
    ReplyGeneration,
)


def classify_email(
    subject: str,
    sender: str,
    body: str,
) -> EmailClassification:

    if not body.strip():
        return EmailClassification(
            category="other",
            importance="low",
        )

    chain = get_classification_chain()

    return chain.invoke(
        {
            "subject": subject,
            "sender": sender,
            "body": body,
        }
    )


def extract_actions(
    subject: str,
    sender: str,
    body: str,
) -> ActionExtraction:

    if not body.strip():
        return ActionExtraction(actions=[])

    chain = get_action_chain()

    return chain.invoke(
        {
            "subject": subject,
            "sender": sender,
            "body": body,
        }
    )


def extract_deadlines(
    subject: str,
    sender: str,
    body: str,
) -> DeadlineExtraction:

    if not body.strip():
        return DeadlineExtraction(deadlines=[])

    chain = get_deadline_chain()

    return chain.invoke(
        {
            "subject": subject,
            "sender": sender,
            "body": body,
        }
    )


def analyze_email(
    subject: str,
    sender: str,
    body: str,
    target_language: str = "English",
) -> EmailAnalysis:

    if not body.strip():
        return EmailAnalysis(
            summary="No readable email content was found.",
            language="unknown",
            category="other",
            importance="low",
            actions=[],
            deadlines=[],
        )

    chain = get_email_analysis_chain()

    return chain.invoke(
        {
            "subject": subject,
            "sender": sender,
            "body": body,
            "target_language": target_language,
        }
    )

def generate_reply(
    subject: str,
    sender: str,
    body: str,
    instructions: str = "",
) -> ReplyGeneration:

    if not body.strip():
        return ReplyGeneration(
            reply="Unable to generate a reply because the email content is empty."
        )

    chain = get_reply_chain()

    return chain.invoke(
        {
            "subject": subject,
            "sender": sender,
            "body": body,
            "instructions": instructions,
        }
    )