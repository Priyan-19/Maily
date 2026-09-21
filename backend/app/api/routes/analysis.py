from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.email_analysis import EmailAnalysis
from app.services.analysis_service import analyze_and_save_email


router = APIRouter(
    prefix="/api/analysis",
    tags=["Analysis"],
)


@router.post("/email/{email_id}")
def analyze_email_endpoint(
    email_id: int,
    db: Session = Depends(get_db),
):
    try:
        analysis = analyze_and_save_email(
            db=db,
            email_id=email_id,
        )

        return {
            "id": analysis.id,
            "email_id": analysis.email_id,
            "summary": analysis.summary,
            "language": analysis.language,
            "category": analysis.category,
            "importance": analysis.importance,
            "actions": analysis.actions,
            "deadlines": analysis.deadlines,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )