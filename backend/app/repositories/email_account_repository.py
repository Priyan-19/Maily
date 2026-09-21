from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.email_account import EmailAccount


def get_email_account(
    db: Session,
    user_id: int,
    email_address: str,
) -> EmailAccount | None:

    statement = select(EmailAccount).where(
        EmailAccount.user_id == user_id,
        EmailAccount.email_address == email_address,
    )

    return db.scalar(statement)


def create_email_account(
    db: Session,
    user_id: int,
    email_address: str,
    access_token: str,
    refresh_token: str | None,
    token_expiry: datetime | None,
    provider: str = "google",
) -> EmailAccount:

    email_account = EmailAccount(
        user_id=user_id,
        provider=provider,
        email_address=email_address,
        access_token=access_token,
        refresh_token=refresh_token,
        token_expiry=token_expiry,
    )

    db.add(email_account)
    db.commit()
    db.refresh(email_account)

    return email_account


def get_or_create_email_account(
    db: Session,
    user_id: int,
    email_address: str,
    access_token: str,
    refresh_token: str | None,
    token_expiry: datetime | None,
    provider: str = "google",
) -> EmailAccount:

    email_account = get_email_account(
        db=db,
        user_id=user_id,
        email_address=email_address,
    )

    if email_account:
        email_account.access_token = access_token

        if refresh_token:
            email_account.refresh_token = refresh_token

        email_account.token_expiry = token_expiry

        db.commit()
        db.refresh(email_account)

        return email_account

    return create_email_account(
        db=db,
        user_id=user_id,
        email_address=email_address,
        access_token=access_token,
        refresh_token=refresh_token,
        token_expiry=token_expiry,
        provider=provider,
    )