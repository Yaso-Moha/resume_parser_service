from sentence_transformers import SentenceTransformer, util
import torch

# Load MiniLM-v5 model once at startup
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

@app.route("/filter-parsed-resumes", methods=["POST"])
def filter_parsed_resumes():
    try:
        data = request.get_json()
        filter_q = data.get("filter_query", "").strip()
        resumes = data.get("parsed_resumes", [])

        if not filter_q or not resumes:
            return jsonify({"matches": []})

        # Encode the filter query
        query_embedding = embedding_model.encode(filter_q, convert_to_tensor=True)

        matches = []
        for resume in resumes:
            filename = resume.get("filename", "")
            full_text = resume.get("full_text", "")
            if not full_text:
                continue

            # Truncate to avoid unnecessary computation
            text_snippet = full_text[:8000]

            # Encode the resume text
            resume_embedding = embedding_model.encode(text_snippet, convert_to_tensor=True)

            # Calculate cosine similarity
            cosine_score = util.cos_sim(query_embedding, resume_embedding).item()

            # If similarity is above threshold (tune as needed)
            if cosine_score >= 0.6:
                matches.append(filename)

        return jsonify({"matches": matches})

    except Exception as e:
        print("🛑 Filtering error:", e)
        return jsonify({"error": str(e)}), 500
