import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from rag.loader import load_document
from rag.splitter import split_documents
from rag.vector_store import create_vector_store

upload_bp = Blueprint("upload",__name__)
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {".txt",".pdf",".docx"}
os.makedirs(UPLOAD_FOLDER,exist_ok=True)


@upload_bp.route("/upload",methods=["POST"])
def upload_file():
    print("\n--- DEBUG: New Request Received ---")
    print(f"Request Files keys: {list(request.files.keys())}")
    print(f"Request Form data: {list(request.form.keys())}")
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if not file.filename:
        return jsonify({"error": "No file selected"}), 400

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        return jsonify({"error": ("Unsupported file type. ""Only .txt, .pdf and .docx ""files are supported.")}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER,filename)
    file.save(file_path)

    try:
        documents = load_document(file_path)
        chunks = split_documents(documents)

        if not chunks:
            return jsonify({ "error": "No text found in document."}), 400

        vector_store = create_vector_store(chunks)
        vector_store.save_local("/home/arvind/rag-knowledge-assistant", "knowledeg_databse")

        return jsonify({ "message": "File uploaded successfully",
                                "filename": filename,
                                "documents": len(documents),
                                "chunks": len(chunks)
                            }), 200


    except Exception as e:
        return jsonify({"error": str(e)}), 500