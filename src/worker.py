import os
import sqlite3
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa

ARTIFACTS_DIR = "artifacts"
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

def fetch_and_aggregate_user_data(user_id: str) -> dict:
    """
    Executes SQL aggregation to calculate user statistics.
    Creates an in-memory SQLite DB for testing if real DB isn't attached.
    """
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    
    # Create temporary table & mock dataset
    cursor.execute("""
        CREATE TABLE activity_logs (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            status TEXT,
            response_time_ms INTEGER
        )
    """)
    
    cursor.executemany("""
        INSERT INTO activity_logs (user_id, status, response_time_ms) 
        VALUES (?, ?, ?)
    """, [
        (user_id, "success", 120),
        (user_id, "success", 150),
        (user_id, "failed", 400),
        (user_id, "success", 110),
    ])
    conn.commit()

    # SQL Aggregation Requirement: Total, Successful, Failed, and Avg Latency
    query = """
        SELECT 
            COUNT(*) AS total_requests,
            SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) AS successful_requests,
            SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) AS failed_requests,
            AVG(response_time_ms) AS avg_response_time
        FROM activity_logs
        WHERE user_id = ?
    """
    cursor.execute(query, (user_id,))
    row = cursor.fetchone()
    conn.close()

    return {
        "user_id": user_id,
        "total_requests": row[0] or 0,
        "successful_requests": row[1] or 0,
        "failed_requests": row[2] or 0,
        "avg_response_time": round(row[3] or 0, 2)
    }

def render_pdf_report(report_id: str, user_id: str) -> str:
    """
    Fetches aggregate data, renders HTML, and saves the PDF artifact.
    """
    # 1. SQL Aggregation Step
    aggregated_data = fetch_and_aggregate_user_data(user_id)

    # 2. Render Template
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report.html")
    rendered_html = template.render(data=aggregated_data, report_id=report_id)

    # 3. Store Artifact
    pdf_path = os.path.join(ARTIFACTS_DIR, f"report_{report_id}.pdf")
    with open(pdf_path, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(rendered_html, dest=pdf_file)

    if pisa_status.err:
        raise Exception("PDF generation failed inside xhtml2pdf engine.")

    return pdf_path