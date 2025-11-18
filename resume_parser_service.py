# ------------------------------
#       resume_parser_service.py
# ------------------------------

import os
import shutil
import tempfile
import json

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from zipfile import ZipFile
from pdfminer.high_level import extract_text
from PyPDF2 import PdfReader

from dotenv import load_dotenv
load_dotenv()

import openai

openai_api_key = os.environ.get("OPENAI_API_KEY", "").strip()
if not openai_api_key:
    raise RuntimeError("ERROR: Please set the OPENAI_API_KEY environment variable.")

client = openai.OpenAI(api_key=openai_api_key)

app = Flask(__name__)
CORS(app)

# ─── /upload-resumes (identical to your existing code) ─────────────────────────
@app.route("/upload-resumes", methods=["POST"])
def upload_resumes():
    temp_dir = tempfile.mkdtemp(prefix="resumes_")
    parsed = []

    try:
        if "files" in request.files:
            files_list = request.files.getlist("files")

            if len(files_list) == 1 and files_list[0].filename.lower().endswith(".zip"):
                zf = files_list[0]
                zip_path = os.path.join(temp_dir, zf.filename)
                zf.save(zip_path)
                with ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(temp_dir)
            else:
                for upload_file in files_list:
                    if upload_file.filename.lower().endswith(".pdf"):
                        save_path = os.path.join(temp_dir, upload_file.filename)
                        os.makedirs(os.path.dirname(save_path), exist_ok=True)
                        upload_file.save(save_path)

        for root, _, files in os.walk(temp_dir):
            for fname in files:
                if not fname.lower().endswith(".pdf"):
                    continue

                full_path = os.path.join(root, fname)
                try:
                    text = ""
                    try:
                        text = extract_text(full_path) or ""
                    except:
                        reader = PdfReader(full_path)
                        for page in reader.pages:
                            page_txt = page.extract_text()
                            if page_txt:
                                text += page_txt

                    if not text.strip():
                        raise ValueError("No text extracted")

                    cleaned = " ".join(text.strip().split())
                    snippet = cleaned[:300] + ("…" if len(cleaned) > 300 else "")

                    parsed.append({
                        "filename": fname,
                        "full_text": text,
                        "snippet": snippet
                    })
                except Exception as e:
                    print(f"⛔ Failed to parse '{fname}': {e}")
                    continue

        return jsonify({"parsed_resumes": parsed})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        try:
            shutil.rmtree(temp_dir)
        except:
            pass


@app.route("/resume-file/<path:filename>", methods=["GET"])
def serve_resume_file(filename):
    uploads_folder = os.path.join(os.getcwd(), "uploads")
    return send_from_directory(uploads_folder, filename, as_attachment=False)


@app.route("/filter-parsed-resumes", methods=["POST"])
def filter_parsed_resumes():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Invalid JSON."}), 400

        filter_q = data.get("filter_query", "").strip()
        resumes = data.get("parsed_resumes", [])

        if not filter_q or not resumes:
            return jsonify({"matches": []})

        prompt_header = f"""
You are an expert recruiter. The user’s requirement (case‐insensitive) is:
  \"{filter_q}\"

First, identify each separate constraint in the requirement. Then, for each resume:
  • Check whether the resume meets *all* constraints.
  • Matching must be case‐insensitive (e.g. “arabic” vs “Arabic” → both match).
  • Only list filenames that satisfy every requirement.

Reply EXACTLY with a JSON array of matching filenames. If none match, reply with [].

Below is a JSON list of resumes. Each resume has:
  {{ "filename": <string>, "full_text": <string> }}

Example reply format:
["resume_3.pdf", "resume_42.pdf"]
"""

        truncated_list = []
        for r in resumes:
            fname = r.get("filename")
            full_text = r.get("full_text", "")
            small_text = full_text[:8000]
            truncated_list.append({
                "filename": fname,
                "full_text": small_text
            })

        json_resumes = json.dumps(truncated_list, indent=2)
        full_prompt = prompt_header + "\nResumes:\n" + json_resumes

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant that selects resumes."},
                {"role": "user",   "content": full_prompt}
            ],
            temperature=0.0,
            max_tokens=512
        )

        ai_text = response.choices[0].message.content.strip()
        try:
            matches = json.loads(ai_text)
            if not isinstance(matches, list):
                matches = []
        except:
            matches = []

        return jsonify({"matches": matches})

    except Exception as e:
        print("🛑 Filtering error:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/extract-cv-text", methods=["POST"])
def extract_cv_text():
    if "file" not in request.files:
        return jsonify({ "error": "No file part in request." }), 400

    file = request.files["file"]
    filename = file.filename.lower()

    temp_dir = tempfile.mkdtemp(prefix="cv_")
    save_path = os.path.join(temp_dir, filename)
    file.save(save_path)

    try:
        text = ""

        if filename.endswith(".pdf"):
            try:
                text = extract_text(save_path)
            except:
                reader = PdfReader(save_path)
                for page in reader.pages:
                    page_txt = page.extract_text()
                    if page_txt:
                        text += page_txt

        elif filename.endswith(".docx"):
            import mammoth
            with open(save_path, "rb") as docx_file:
                result = mammoth.extract_raw_text(docx_file)
                text = result.value

        else:
            return jsonify({ "error": "Unsupported file type. Use PDF or DOCX." }), 400

        cleaned = " ".join(text.strip().split())
        return jsonify({ "text": cleaned })

    except Exception as e:
        return jsonify({ "error": str(e) }), 500

    finally:
        try:
            shutil.rmtree(temp_dir)
        except:
            pass


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(host="0.0.0.0", port=5001, debug=True)
