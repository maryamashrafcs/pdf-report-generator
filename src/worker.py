import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa

# Initialize Jinja2 Template Engine
templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
env = Environment(loader=FileSystemLoader(templates_dir))

def render_pdf_report(report_id: str, user_id: str) -> str:
    # Ensure artifacts directory exists
    artifacts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "artifacts")
    os.makedirs(artifacts_dir, exist_ok=True)

    # 1. Load and render HTML template
    template = env.get_template("report.html")
    html_out = template.render(
        report_id=report_id,
        user_id=user_id,
        timestamp=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    )

    # 2. Output PDF Path
    pdf_filename = f"report_{report_id}.pdf"
    pdf_path = os.path.join(artifacts_dir, pdf_filename)

    # 3. Generate PDF via xhtml2pdf (Pure Python)
    with open(pdf_path, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(html_out, dest=pdf_file)

    if pisa_status.err:
        raise RuntimeError("Failed to render PDF using xhtml2pdf")

    return pdf_path