import os
import json
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# ----------------------------
# Setup
# ----------------------------
load_dotenv(".env")
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ----------------------------
# Score resume with Gemini
# ----------------------------
def score_resume(pdf_path: str, job_role: str) -> dict:
    uploaded_file = genai.upload_file(pdf_path)

    prompt = f"""
    You are an Applicant Tracking System (ATS) evaluator.
    Compare the uploaded resume against the given job role.

    Return your answer strictly in JSON with this structure:
    {{
        "ATS_score": number (0-100),
        "key_strengths": [list of strings],
        "missing_keywords": [list of strings],
        "feedback": "string"
    }}

    Job role:
    {job_role}
    """

    response = model.generate_content([uploaded_file, prompt])
    raw_output = response.text.strip()

    if raw_output.startswith("```"):
        raw_output = raw_output.split("```", 2)[1]
        if raw_output.startswith("json"):
            raw_output = raw_output[len("json"):].strip()

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        return {"error": "Could not parse model output", "raw_response": response.text}


# ----------------------------
# Routes
# ----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        job_role = request.form.get("job_role")
        file = request.files.get("resume")

        if not job_role or not file:
            return jsonify({"error": "Please upload a resume and enter job role."})

        pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(pdf_path)

        result = score_resume(pdf_path, job_role)
        return jsonify(result)

    return render_template("index.html")


# ----------------------------
# Run App
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
