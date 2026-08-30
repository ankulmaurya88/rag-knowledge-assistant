from flask import Blueprint, request, jsonify
from rag.retriever import create_retriever
from rag.qa import format_documents
from rag import store
from rag.vector_store import load_vector_store

ask_bp = Blueprint("ask",__name__)
@ask_bp.route("/ask", methods=["POST"])
def ask_question():

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required."}), 400

        question = data.get("question","").strip()
        if not question:
            return jsonify({"error": "Question is required."}), 400

        vector_store = load_vector_store("/home/arvind/rag-knowledge-assistant")

        retriever = create_retriever(vector_store, k=3)
        documents = retriever.invoke(question)
        context = format_documents(documents)
        print('context---', context)
        answer = store.qa_chain.invoke({"context": context,"question": question})
        sources = []
        for document in documents:
            sources.append({
                                "source": document.metadata.get("source","Unknown"),
                                "chunk_id": document.metadata.get("chunk_id"),
                                "page": document.metadata.get("page")
                            })


        # return jsonify({ "question": question,"answer": answer,"sources": sources}), 200
        return jsonify({ "question": question,"answer": answer}), 200


    except Exception as e:

        import traceback
        traceback.print_exc()
        print("ASK ERROR:", e)

        return jsonify({"error": str(e)}), 500