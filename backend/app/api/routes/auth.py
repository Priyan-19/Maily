from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import generate_state

from app.integrations.gmail.oauth import (
    exchange_code_for_credentials,
    get_google_authorization_url,
)

from app.integrations.gmail.service import get_gmail_profile

from app.repositories.user_repository import get_or_create_user

from app.repositories.email_account_repository import (
    get_or_create_email_account,
)


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


# Temporary OAuth state storage mapping state -> code_verifier.
# We will replace this with proper session/state storage later.
_oauth_states: dict[str, str] = {}


@router.get("/google")
def google_login():

    state = generate_state()

    authorization_url, code_verifier = get_google_authorization_url(state)

    _oauth_states[state] = code_verifier

    return RedirectResponse(
        url=authorization_url
    )


@router.get("/google/callback")
def google_callback(
    request: Request,
    code: str,
    state: str,
    db: Session = Depends(get_db),
):

    # -----------------------------------
    # 1. Validate OAuth state & extract code_verifier
    # -----------------------------------

    if state not in _oauth_states:

        raise HTTPException(
            status_code=400,
            detail="Invalid OAuth state.",
        )

    code_verifier = _oauth_states.pop(state)

    try:

        # -----------------------------------
        # 2. Exchange authorization code
        # -----------------------------------

        authorization_response = str(request.url)

        credentials = exchange_code_for_credentials(
            authorization_response=authorization_response,
            state=state,
            code_verifier=code_verifier,
        )

        # -----------------------------------
        # 3. Get Gmail profile
        # -----------------------------------

        profile = get_gmail_profile(
            credentials
        )

        gmail_email = profile.get(
            "emailAddress"
        )

        if not gmail_email:

            raise HTTPException(
                status_code=400,
                detail="Could not determine Gmail account.",
            )

        # -----------------------------------
        # 4. Create/Get User
        # -----------------------------------

        user = get_or_create_user(
            db=db,
            email=gmail_email,
            name=gmail_email.split("@")[0],
        )

        # -----------------------------------
        # 5. Save OAuth credentials
        # -----------------------------------

        email_account = get_or_create_email_account(
            db=db,
            user_id=user.id,
            email_address=gmail_email,
            access_token=credentials.token,
            refresh_token=credentials.refresh_token,
            token_expiry=credentials.expiry,
            provider="google",
        )

        return RedirectResponse(
            url="http://localhost:5173/?auth=success"
        )

    except HTTPException:
        raise

    except Exception as exc:

        db.rollback()

        print(
            f"Google OAuth error: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=f"Google authentication failed: {exc}",
        )