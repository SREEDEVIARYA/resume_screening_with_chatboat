import os
import uuid

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session
)

from werkzeug.utils import secure_filename

from agents.orchestrator import RecruitmentOrchestrator

from chatbot.chatbot_engine import RecruitmentChatbot


# ==================================
# 1. FLASK CONFIGURATION
# ==================================

app = Flask(__name__)

app.secret_key = "resume_screening_secret_key"

app.config["UPLOAD_FOLDER"] = "uploads"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


# ==================================
# 2. INITIALIZE AI AGENTS
# ==================================

orchestrator = RecruitmentOrchestrator()

chatbot = RecruitmentChatbot()


# Temporary storage for candidate results
SCREENING_STORE = {}


# ==================================
# 3. HOMEPAGE
# ==================================

@app.route("/")
def home():

    return render_template("index.html")


# ==================================
# 4. RESUME SCREENING
# ==================================

@app.route("/screen", methods=["POST"])
def screen():

    job_description = request.form.get(
        "job_description", ""
    ).strip()

    files = request.files.getlist("resumes")

    if not job_description or not any(
        file.filename for file in files
    ):

        return "Please enter a job description and upload resumes."

    resume_paths = []

    for file in files:

        if not file.filename.lower().endswith(".pdf"):
            continue

        # Generate unique filename
        filename = secure_filename(file.filename)

        unique_filename = (
            str(uuid.uuid4()) + "_" + filename
        )

        path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            unique_filename
        )

        file.save(path)

        resume_paths.append(path)

    if not resume_paths:

        return "Please upload at least one valid PDF resume."

    # ==================================
    # START MULTI-AGENT WORKFLOW
    # ==================================

    results = orchestrator.run(
        resume_paths,
        job_description
    )

    # ==================================
    # STORE SCREENING RESULTS
    # ==================================

    screening_id = str(uuid.uuid4())

    SCREENING_STORE[screening_id] = results

    session["screening_id"] = screening_id

    # ==================================
    # DISPLAY RESULTS
    # ==================================

    return render_template(
        "results.html",
        results=results
    )


# ==================================
# 5. CHATBOT PAGE
# ==================================

@app.route("/chatbot")
def chatbot_page():

    screening_id = session.get("screening_id")

    if not screening_id or screening_id not in SCREENING_STORE:

        return "Please complete resume screening first."

    return render_template("chatbot.html")


# ==================================
# 6. CHATBOT API
# ==================================

@app.route("/api/chat", methods=["POST"])
def chat_api():

    data = request.get_json(silent=True) or {}

    message = data.get("message", "").strip()

    if not message:

        return jsonify({
            "error": "Please enter a message."
        }), 400

    # Get current screening session
    screening_id = session.get("screening_id")

    if not screening_id or screening_id not in SCREENING_STORE:

        return jsonify({
            "error": "Please upload resumes and complete screening first."
        }), 400

    # Get candidate information
    candidates = SCREENING_STORE[screening_id]

    # Generate chatbot response
    response = chatbot.get_response(
        message,
        candidates
    )

    return jsonify({
        "response": response
    })


# ==================================
# 7. RUN APPLICATION
# ==================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )