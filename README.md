# ATS Resume Checker

A web app that evaluates resumes against job roles using `Google Gemini API - version 1.5 flash`.  
It simulates an Applicant Tracking System (ATS) and provides:

- ATS Score (0–100)
- Key strengths
- Missing keywords
- Actionable feedback

## Tech Stack
- **Python (Flask)** – Backend
- **Google Gemini API (version 1.5 flash)** – AI-powered resume evaluation
- **HTML/CSS/JS** – Frontend UI


## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/KaviyapriyaMathi/ats-resume-checker-gemini.git
   cd ats-resume-checker-gemini
    ```
2. Set up environment variables:
   - Update your `Google Gemini API key` in the `.env` file:
     ```
     API_KEY =
     ```
3. Run the Flask app:
    ```bash
    python app.py
    ```