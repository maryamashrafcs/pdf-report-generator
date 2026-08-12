```markdown
# Async PDF Report Generator

A simple service that creates PDF reports from HTML templates in the background so your API stays fast and responsive.

## Features
- **Fast Responses**: Requests run in the background without blocking the API.
- **HTML & CSS Templates**: Style reports using standard HTML and Jinja2 templates.
- **Job Tracking**: Monitor report status (`pending`, `completed`, `failed`) anytime.
- **Pure Python**: Uses `xhtml2pdf` for easy setup without native C++ dependencies.

## Instructions

1. **Clone the project:**
   ```powershell
   git clone <YOUR_GITHUB_REPOSITORY_URL>
   cd pdf-report-generator

```

2. **Set up and activate virtual environment:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1

```


3. **Install dependencies:**
```powershell
pip install -r requirements.txt

```


4. **Start the application:**
```powershell
uvicorn main:app --reload

```


5. Open `http://127.0.0.1:8000/docs` in your browser to access the API documentation.

## How to Use

1. **Create a Report**: Send a `POST` request to `/api/reports` with a `user_id`. Copy the returned `report_id`.
2. **Check Status**: Send a `GET` request to `/api/reports/{report_id}` until status is `completed`.
3. **Download PDF**: Send a `GET` request to `/api/reports/{report_id}/download` to save your file.