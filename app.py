import os
from flask import Flask, render_template, request, jsonify, send_file
from advanced_resume_analyzer import analyze_resume, generate_pdf_report, roles
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', roles=list(roles.keys()))

@app.route('/analyze', methods=['POST'])
def analyze():
    name = request.form.get('name')
    email = request.form.get('email')
    role = request.form.get('role')
    pdf_file = request.files.get('pdf')

    if not name or not email or not role or not pdf_file:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        result = analyze_resume(name, email, role, pdf_file)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    # Since we can't reliably store state without sessions/DB, we re-analyze for download or expect JSON data.
    # A simpler way is to let the frontend POST the JSON results back to get the PDF.
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        pdf_bytes = generate_pdf_report(data)
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name='AI_Resume_Analysis_Report.pdf'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
