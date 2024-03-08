from fastapi import APIRouter, Depends
from starlette.background import BackgroundTasks

from src.tasks.tasks import send_email_report
from src.auth.auth import current_user


router = APIRouter(prefix="/report")


@router.get("/financial/starlette")
def get_financial_report_starlette(background_tasks: BackgroundTasks, user=Depends(current_user)):
    """Sending email by utilizing background tasks from starlette"""
    
    background_tasks.add_task(send_email_report, user.email)
    return {
        "status": 200,
        "data": "Email sent successfully",
        "details": None
    }


@router.get("/financial/celery")
def get_financial_report_celery(user=Depends(current_user)):
    """Sending email by utilizing celery"""

    send_email_report.delay(user.email)
    return {
        "status": 200,
        "data": "Email sent successfully",
        "details": None
    }
