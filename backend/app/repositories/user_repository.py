from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:

    statement = select(User).where(
        User.email == email
    )

    return db.scalar(statement)


def create_user(
    db: Session,
    email: str,
    name: str | None = None,
) -> User:

    user = User(
        email=email,
        name=name,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_or_create_user(
    db: Session,
    email: str,
    name: str | None = None,
) -> User:

    user = get_user_by_email(
        db=db,
        email=email,
    )

    if user:
        return user

    return create_user(
        db=db,
        email=email,
        name=name,
    )