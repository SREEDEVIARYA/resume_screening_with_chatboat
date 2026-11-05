
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


# ==================================
# 1. FLASK CONFIGURATION
# ==================================

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "change-this-secret-key"
)

app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


# ==================================
# 2. LAZY AI INITIALIZATION
# ==================================

orchestrator = None
chatbot = None


def get_orchestrator():

    global orchestrator

    if orchestrator is None:

        from agents.orchestrator import RecruitmentOrchestrator

        orchestrator = RecruitmentOrchestrator()

    return orchestrator


def get_chatbot():

    global chatbot

    if chatbot is None:

        from chatbot.chatbot_engine import RecruitmentChatbot

        chatbot = RecruitmentChatbot()

    return chatbot


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

    valid_files = [
        file for file in files
        if file.filename and file.filename.lower().endswith(".pdf")
    ]

    if not job_description or not valid_files:

        return "Please enter a job description and upload PDF resumes."

    resume_paths = []

    try:

        for file in valid_files:

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

        # Initialize agents only when screening is requested
        ai_orchestrator = get_orchestrator()

        results = ai_orchestrator.run(
            resume_paths,
            job_description
        )

        screening_id = str(uuid.uuid4())

        SCREENING_STORE[screening_id] = results

        session["screening_id"] = screening_id

        return render_template(
            "results.html",
            results=results
        )

    except Exception as e:

        app.logger.exception("Resume screening failed")

        return "Resume screening failed. Please check the server logs.", 500

    finally:

        # Remove temporary uploaded PDF files after processing
        for path in resume_paths:

            if os.path.exists(path):

                os.remove(path)


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

    screening_id = session.get("screening_id")

    if not screening_id or screening_id not in SCREENING_STORE:

        return jsonify({
            "error": "Please upload resumes and complete screening first."
        }), 400

    try:

        candidates = SCREENING_STORE[screening_id]

        # Initialize chatbot only when chat is requested
        ai_chatbot = get_chatbot()

        response = ai_chatbot.get_response(
            message,
            candidates
        )

        return jsonify({
            "response": response
        })

    except Exception:

        app.logger.exception("Chatbot request failed")

        return jsonify({
            "error": "Unable to generate response. Please try again."
        }), 500


# ==================================
# 7. ERROR HANDLING
# ==================================

@app.errorhandler(413)
def file_too_large(error):

    return "Uploaded files exceed the 50 MB limit.", 413


# ==================================
# 8. LOCAL DEVELOPMENT
# ==================================

if __name__ == "__main__":

    app.run(
        debug=False,
        port=5000
    )
