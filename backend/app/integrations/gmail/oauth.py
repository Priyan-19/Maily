import os

# Allow HTTP for local development only.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

from google_auth_oauthlib.flow import Flow

from app.core.config import settings


def create_google_flow(state: str | None = None) -> Flow:
    """
    Create a Google OAuth flow.
    """

    client_config = {
        "web": {
            "client_id": settings.google_client_id,
            "client_secret": settings.google_client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [settings.google_redirect_uri],
        }
    }

    flow = Flow.from_client_config(
        client_config,
        scopes=settings.scopes,
        state=state,
    )

    flow.redirect_uri = settings.google_redirect_uri

    return flow


def get_google_authorization_url(state: str) -> tuple[str, str]:
    """
    Generate Google's authorization URL and return (authorization_url, code_verifier).
    """

    flow = create_google_flow(state)

    authorization_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )

    return authorization_url, flow.code_verifier


def exchange_code_for_credentials(
    authorization_response: str,
    state: str,
    code_verifier: str | None = None,
):
    """
    Exchange Google's authorization response for credentials.
    """

    flow = create_google_flow(state)

    if code_verifier:
        flow.code_verifier = code_verifier

    flow.fetch_token(
        authorization_response=authorization_response
    )

    return flow.credentials