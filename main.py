import uuid
from datetime import datetime
from typing import Dict
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(
    title="Async PDF Report Pipeline",
    description="Asynchronous PDF report generation using FastAPI background tasks and WeasyPrint."
)

# In-memory status store
reports_db: Dict[str, dict] = {}

class ReportRequest(BaseModel):
    user_id: str

def execute_report_job(report_id: str, user_id: str):
    from src.worker import render_pdf_report
    try:
        reports_db[report_id]["status"] = "processing"
        filepath = render_pdf_report(report_id, user_id)
        
        reports_db[report_id]["status"] = "completed"
        reports_db[report_id]["artifact_path"] = filepath
        reports_db[report_id]["completed_at"] = datetime.utcnow().isoformat()
    except Exception as err:
        reports_db[report_id]["status"] = "failed"
        reports_db[report_id]["error"] = str(err)

@app.post("/api/reports", status_code=202)
def request_report(payload: ReportRequest, background_tasks: BackgroundTasks):
    report_id = str(uuid.uuid4())
    reports_db[report_id] = {
        "id": report_id,
        "user_id": payload.user_id,
        "status": "pending",
        "artifact_path": None,
        "error": None,
        "created_at": datetime.utcnow().isoformat()
    }

    background_tasks.add_task(execute_report_job, report_id, payload.user_id)

    return {
        "message": "Report generation enqueued successfully",
        "report_id": report_id,
        "status_url": f"/api/reports/{report_id}"
    }

@app.get("/api/reports/{report_id}")
def check_status(report_id: str):
    report = reports_db.get(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report ID not found")

    download_url = f"/api/reports/{report_id}/download" if report["status"] == "completed" else None

    return {
        "id": report["id"],
        "user_id": report["user_id"],
        "status": report["status"],
        "download_url": download_url,
        "error": report["error"]
    }

@app.get("/api/reports/{report_id}/download")
def download_pdf(report_id: str):
    report = reports_db.get(report_id)
    if not report or report["status"] != "completed":
        raise HTTPException(status_code=400, detail="Report is not ready or failed generation")

    return FileResponse(
        path=report["artifact_path"],
        media_type="application/pdf",
        filename=f"Report_{report_id[:8]}.pdf"
    )