<h1>Async PDF Report Generator</h1>

<p>A simple service that creates PDF reports from HTML templates in the background so your API stays fast and responsive.</p>

<hr>

<h2>Features</h2>

<ul>
  <li><b>Fast Responses</b>: Requests run in the background without blocking the API.</li>
  <li><b>HTML & CSS Templates</b>: Style reports using standard HTML and Jinja2 templates.</li>
  <li><b>Job Tracking</b>: Monitor report status (<code>pending</code>, <code>completed</code>, <code>failed</code>) anytime.</li>
  <li><b>Pure Python</b>: Uses <code>xhtml2pdf</code> for easy setup without native C++ dependencies.</li>
</ul>

<hr>

<h2>Instructions</h2>

<ol>
  <li>
    <b>Clone the project:</b>
<pre><code>git clone https://github.com/maryamashrafcs/pdf-report-generator.git
cd pdf-report-generator</code></pre>
  </li>
  <li>
    <b>Set up and activate virtual environment:</b>
<pre><code>python -m venv venv
.\venv\Scripts\Activate.ps1</code></pre>
  </li>
  <li>
    <b>Install dependencies:</b>
<pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li>
    <b>Start the application:</b>
<pre><code>uvicorn main:app --reload</code></pre>
  </li>
  <li>Open <code>http://127.0.0.1:8000/docs</code> in your browser to access the API documentation.</li>
</ol>

<hr>

<h2>How to Use</h2>

<ol>
  <li><b>Create a Report</b>: Send a <code>POST</code> request to <code>/api/reports</code> with a <code>user_id</code>. Copy the returned <code>report_id</code>.</li>
  <li><b>Check Status</b>: Send a <code>GET</code> request to <code>/api/reports/{report_id}</code> until status is <code>completed</code>.</li>
  <li><b>Download PDF</b>: Send a <code>GET</code> request to <code>/api/reports/{report_id}/download</code> to save your file.</li>
</ol>